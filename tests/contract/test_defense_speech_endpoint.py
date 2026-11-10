from oralia.infrastructure.db import models
from oralia.infrastructure.speech.synthesis_port import SynthesisOutcome
from tests.contract.test_defense_voice_and_speech import _session, _wav


class _RecordingTTS:
    calls: list[str] = []

    async def synthesize(self, text: str, *, language: str):
        del language
        self.calls.append(text)
        return SynthesisOutcome(ok=True, audio=_wav())


def _approved_turn(app_client, session_id: str) -> dict:
    response = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-turns",
        json={"text": "Separé generación y verificación."},
    )
    assert response.status_code == 200
    return response.json()


def test_speech_synthesizes_only_exact_approved_persisted_text(app_client, monkeypatch) -> None:
    from oralia.interfaces.api.routers import oral_defense

    _RecordingTTS.calls = []
    monkeypatch.setattr(oral_defense, "_synthesis_adapter_factory", _RecordingTTS)
    session_id = _session(app_client)
    turn = _approved_turn(app_client, session_id)
    response = app_client.post(turn["speech"]["url"])
    assert response.status_code == 200
    assert response.content == _wav()
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["x-oralia-text-sha256"] == turn["speech"]["text_sha256"]
    assert _RecordingTTS.calls == [turn["output_text"]]


def test_speech_fails_closed_if_persisted_text_no_longer_matches_proposal(app_client, monkeypatch) -> None:
    from oralia.interfaces.api.routers import oral_defense

    _RecordingTTS.calls = []
    monkeypatch.setattr(oral_defense, "_synthesis_adapter_factory", _RecordingTTS)
    session_id = _session(app_client)
    body = _approved_turn(app_client, session_id)
    Session = app_client.__db_sessionmaker__
    with Session() as db:
        turn = db.get(models.Turn, body["turn_id"])
        turn.output_text = "texto manipulado"
        db.commit()
    response = app_client.post(body["speech"]["url"])
    assert response.status_code == 404
    assert _RecordingTTS.calls == []


def test_null_or_blocked_output_has_no_speech_descriptor(app_client) -> None:
    session_id = _session(app_client)
    Session = app_client.__db_sessionmaker__
    with Session() as db:
        session = db.get(models.Session, session_id)
        activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
        activity.output_authorization_policy_json = None
        activity.output_authorization_policy_sha256 = None
        db.commit()
    response = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-turns", json={"text": "respuesta"}
    )
    assert response.status_code == 200
    assert response.json()["output_text"] is None
    assert response.json()["speech"] is None
    missing = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-turns/{response.json()['turn_id']}/speech"
    )
    assert missing.status_code == 404


def test_speech_rejects_a_verdict_linked_to_a_different_proposal(app_client, monkeypatch):
    from oralia.interfaces.api.routers import oral_defense

    _RecordingTTS.calls = []
    monkeypatch.setattr(oral_defense, "_synthesis_adapter_factory", _RecordingTTS)
    session_id = _session(app_client)
    body = _approved_turn(app_client, session_id)
    with app_client.__db_sessionmaker__() as db:
        turn = db.get(models.Turn, body["turn_id"])
        replacement = models.GeneratedProposal(
            turn_id=turn.id, generator_agent_id="unverified", content={"text": turn.output_text}
        )
        db.add(replacement)
        db.flush()
        turn.generated_proposal_id = replacement.id
        db.commit()
    assert app_client.post(body["speech"]["url"]).status_code == 404
    assert _RecordingTTS.calls == []


def test_speech_does_not_deliver_content_erased_by_a_concurrent_close(app_client, monkeypatch):
    from oralia.application.commands.end_defense_session import end_defense_session
    from oralia.interfaces.api.routers import oral_defense

    session_id = _session(app_client)
    body = _approved_turn(app_client, session_id)

    class FinishesAfterClose:
        async def synthesize(self, text, *, language):
            with app_client.__db_sessionmaker__() as closer:
                session = closer.get(models.Session, session_id)
                config = (
                    closer.query(models.DefenseActivityConfig)
                    .filter_by(activity_configuration_id=session.activity_configuration_id)
                    .one()
                )
                end_defense_session(closer, session, config)
                closer.commit()
            return SynthesisOutcome(ok=True, audio=_wav())

    monkeypatch.setattr(oral_defense, "_synthesis_adapter_factory", FinishesAfterClose)
    assert app_client.post(body["speech"]["url"]).status_code == 404


def test_disabled_and_failed_tts_do_not_change_approved_turn(app_client, monkeypatch) -> None:
    from oralia.interfaces.api.routers import oral_defense

    session_id = _session(app_client)
    body = _approved_turn(app_client, session_id)
    Session = app_client.__db_sessionmaker__
    with Session() as db:
        session = db.get(models.Session, session_id)
        config = (
            db.query(models.DefenseActivityConfig)
            .filter_by(activity_configuration_id=session.activity_configuration_id)
            .one()
        )
        config.voice_output_allowed = False
        db.commit()
    assert app_client.post(body["speech"]["url"]).status_code == 409

    class _FailedTTS:
        async def synthesize(self, text: str, *, language: str):
            del text, language
            return SynthesisOutcome(ok=False, error_code="timeout")

    monkeypatch.setattr(oral_defense, "_synthesis_adapter_factory", _FailedTTS)
    with Session() as db:
        session = db.get(models.Session, session_id)
        config = (
            db.query(models.DefenseActivityConfig)
            .filter_by(activity_configuration_id=session.activity_configuration_id)
            .one()
        )
        config.voice_output_allowed = True
        db.commit()
    assert app_client.post(body["speech"]["url"]).status_code == 503
    with Session() as db:
        turn = db.get(models.Turn, body["turn_id"])
        assert turn.output_text == body["output_text"]
        assert turn.status == "completed"
