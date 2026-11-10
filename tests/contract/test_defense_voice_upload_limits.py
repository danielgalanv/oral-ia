import io
import wave

from starlette.datastructures import UploadFile

from oralia.infrastructure.db import models
from tests.contract.test_defense_voice_and_speech import _STT, _session, _wav


def _long_wav(seconds: int = 301) -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(1)
        wav_file.setframerate(8000)
        wav_file.writeframes(b"\0" * (8000 * seconds))
    return buffer.getvalue()


def test_unknown_and_malformed_formats_never_reach_stt(app_client, monkeypatch) -> None:
    from oralia.interfaces.api.routers import oral_defense

    _STT.calls = 0
    monkeypatch.setattr(oral_defense, "_transcription_adapter_factory", _STT)
    session_id = _session(app_client)
    unknown = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-turns/voice",
        files={"audio": ("answer.bin", b"garbage", "application/octet-stream")},
    )
    malformed = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-turns/voice",
        files={"audio": ("answer.wav", b"not-wave", "audio/wav")},
    )
    assert unknown.status_code == malformed.status_code == 422
    assert _STT.calls == 0


def test_audio_over_300_seconds_never_reaches_stt(app_client, monkeypatch) -> None:
    from oralia.interfaces.api.routers import oral_defense

    _STT.calls = 0
    monkeypatch.setattr(oral_defense, "_transcription_adapter_factory", _STT)
    session_id = _session(app_client)
    response = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-turns/voice",
        files={"audio": ("answer.wav", _long_wav(), "audio/wav")},
    )
    assert response.status_code == 422
    assert _STT.calls == 0


def test_successful_voice_upload_persists_text_only(app_client, monkeypatch) -> None:
    from oralia.interfaces.api.routers import oral_defense

    monkeypatch.setattr(oral_defense, "_transcription_adapter_factory", _STT)
    session_id = _session(app_client)
    response = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-turns/voice",
        files={"audio": ("answer.wav", _wav(), "audio/wav")},
    )
    assert response.status_code == 200
    Session = app_client.__db_sessionmaker__
    with Session() as db:
        transcript = db.get(models.Transcript, response.json()["transcript_id"])
        assert transcript.raw_text
        assert not any("audio" in column.name for column in transcript.__table__.columns)


def test_multipart_spool_is_closed_after_success(app_client, monkeypatch) -> None:
    from oralia.interfaces.api.routers import oral_defense

    closed: list[bool] = []
    original_close = UploadFile.close

    async def recording_close(self):
        await original_close(self)
        closed.append(bool(self.file.closed))

    monkeypatch.setattr(UploadFile, "close", recording_close)
    monkeypatch.setattr(oral_defense, "_transcription_adapter_factory", _STT)
    session_id = _session(app_client)
    response = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-turns/voice",
        files={"audio": ("answer.wav", _wav(150), "audio/wav")},
    )
    assert response.status_code == 200
    assert closed and all(closed)
