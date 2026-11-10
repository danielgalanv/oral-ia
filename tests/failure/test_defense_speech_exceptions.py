from oralia.infrastructure.db import models
from tests.contract.test_defense_speech_endpoint import _approved_turn
from tests.contract.test_defense_voice_and_speech import _session, _wav


def test_stt_exception_records_failure_and_allows_text(app_client, monkeypatch):
    from oralia.interfaces.api.routers import oral_defense

    class Broken:
        async def transcribe(self, audio, *, language):
            raise TimeoutError("private detail")

    monkeypatch.setattr(oral_defense, "_transcription_adapter_factory", Broken)
    session_id = _session(app_client)
    response = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-turns/voice",
        files={"audio": ("answer.wav", _wav(), "audio/wav")},
    )
    assert response.status_code == 503
    with app_client.__db_sessionmaker__() as db:
        assert db.query(models.Transcript).count() == 0
        event = db.query(models.TraceEvent).filter_by(event_type="transcription_failed").one()
        assert "private detail" not in str(event.payload)
        assert db.get(models.Session, session_id).turn_count == 0
    assert _approved_turn(app_client, session_id)["output_text"]


def test_tts_exception_records_failure_without_changing_text(app_client, monkeypatch):
    from oralia.interfaces.api.routers import oral_defense

    class Broken:
        async def synthesize(self, text, *, language):
            raise TimeoutError("private detail")

    monkeypatch.setattr(oral_defense, "_synthesis_adapter_factory", Broken)
    session_id = _session(app_client)
    turn = _approved_turn(app_client, session_id)
    assert app_client.post(turn["speech"]["url"]).status_code == 503
    with app_client.__db_sessionmaker__() as db:
        assert db.query(models.TraceEvent).filter_by(event_type="tts_failed").count() == 1
        persisted = db.get(models.Turn, turn["turn_id"])
        assert persisted.status == "completed"
        assert persisted.output_text == turn["output_text"]
    continued = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-turns",
        json={"text": "La arquitectura separa generación y verificación."},
    )
    assert continued.status_code == 200
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.Session, session_id).turn_count == 2
