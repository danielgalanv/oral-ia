import io
import wave

from oralia.infrastructure.db import models
from oralia.infrastructure.speech.synthesis_port import SynthesisOutcome
from oralia.infrastructure.speech.transcription_port import (
    TranscriptionOutcome,
    TranscriptionSegment,
)
from tests.access_helpers import own_session
from tests.integration.test_defense_text_turn import _seed_defense


def _wav(seconds: float = 0.05) -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(8000)
        wav_file.writeframes(b"\0\0" * int(8000 * seconds))
    return buffer.getvalue()


class _STT:
    calls = 0

    async def transcribe(self, audio: bytes, *, language: str):
        del audio, language
        type(self).calls += 1
        return TranscriptionOutcome(
            ok=True,
            text="Separé generación y verificación.",
            segments=(TranscriptionSegment(text="Separé", confidence=0.99),),
            overall_confidence=0.99,
        )


class _TTS:
    calls: list[str] = []

    async def synthesize(self, text: str, *, language: str):
        del language
        type(self).calls.append(text)
        return SynthesisOutcome(ok=True, audio=_wav())


def _session(app_client) -> str:
    Session = app_client.__db_sessionmaker__
    with Session() as db:
        session = _seed_defense(db)
        config = (
            db.query(models.DefenseActivityConfig)
            .filter_by(activity_configuration_id=session.activity_configuration_id)
            .one()
        )
        config.voice_input_allowed = True
        config.voice_output_allowed = True
        session_id = session.id
        db.commit()
    own_session(app_client, session_id)
    return session_id


def test_voice_confirmation_and_literal_speech_replay(app_client, monkeypatch) -> None:
    from oralia.interfaces.api.routers import oral_defense

    _STT.calls = 0
    _TTS.calls = []
    monkeypatch.setattr(oral_defense, "_transcription_adapter_factory", _STT)
    monkeypatch.setattr(oral_defense, "_synthesis_adapter_factory", _TTS)
    session_id = _session(app_client)
    provisional = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-turns/voice",
        files={"audio": ("answer.wav", _wav(), "audio/wav")},
    )
    assert provisional.status_code == 200
    assert "dialogue_action" not in provisional.json()
    confirmed = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-turns/voice/confirm",
        json={"transcript_id": provisional.json()["transcript_id"], "corrected_text": None},
    )
    assert confirmed.status_code == 200
    body = confirmed.json()
    assert body["speech"]["available"] is True
    first = app_client.post(body["speech"]["url"])
    second = app_client.post(body["speech"]["url"])
    assert first.status_code == second.status_code == 200
    assert first.content == _wav()
    with wave.open(io.BytesIO(first.content), "rb") as audio:
        assert audio.getnframes() > 0
    assert first.headers["cache-control"] == "no-store"
    assert _TTS.calls == [body["output_text"], body["output_text"]]


def test_oversized_audio_is_rejected_before_stt(app_client, monkeypatch) -> None:
    from oralia.interfaces.api.routers import oral_defense

    _STT.calls = 0
    monkeypatch.setattr(oral_defense, "_transcription_adapter_factory", _STT)
    session_id = _session(app_client)
    response = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-turns/voice",
        files={"audio": ("answer.wav", b"x" * (10 * 1024 * 1024 + 1), "audio/wav")},
    )
    assert response.status_code == 413
    assert _STT.calls == 0
