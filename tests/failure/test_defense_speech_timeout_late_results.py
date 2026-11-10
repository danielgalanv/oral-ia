import asyncio
import io
import tempfile
import threading
import wave

import pytest
from starlette.datastructures import Headers, UploadFile

from oralia.infrastructure.db import models
from oralia.infrastructure.speech.config import SpeechSettings
from oralia.infrastructure.speech.faster_whisper_adapter import FasterWhisperTranscriptionAdapter
from oralia.infrastructure.speech.piper_adapter import PiperSpeechSynthesisAdapter
from tests.integration.test_defense_text_turn import _seed_defense


class _BlockingWorker:
    def __init__(self) -> None:
        self.entered = threading.Event()
        self.release = threading.Event()

    async def run(self, func, *args):
        del func, args
        self.entered.set()
        await asyncio.get_running_loop().run_in_executor(None, self.release.wait, 3)
        return object()


def _settings() -> SpeechSettings:
    return SpeechSettings(
        stt_model="local",
        stt_device="cpu",
        stt_compute_type="int8",
        tts_voice="local.onnx",
        low_confidence_threshold=0.6,
        worker_capacity=1,
        stt_timeout_ms=10,
        tts_timeout_ms=10,
    )


async def test_stt_and_tts_execution_timeout_discard_late_worker_values() -> None:
    stt_worker = _BlockingWorker()
    tts_worker = _BlockingWorker()
    stt = FasterWhisperTranscriptionAdapter(config=_settings(), worker=stt_worker)
    tts = PiperSpeechSynthesisAdapter(config=_settings(), worker=tts_worker)
    try:
        transcription = await stt.transcribe(b"audio", language="es")
        synthesis = await tts.synthesize("texto aprobado", language="es")
        assert transcription.ok is False and transcription.error_code == "timeout"
        assert synthesis.ok is False and synthesis.error_code == "timeout"
    finally:
        stt_worker.release.set()
        tts_worker.release.set()


def _wav() -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(8000)
        wav_file.writeframes(b"\0\0" * 80)
    return buffer.getvalue()


async def test_cancelled_upload_closes_rolled_spool_and_persists_no_late_result(
    db_session, monkeypatch
) -> None:
    from oralia.interfaces.api.routers import oral_defense

    started = asyncio.Event()
    release = asyncio.Event()

    class _CancelledSTT:
        async def transcribe(self, audio: bytes, *, language: str):
            del audio, language
            started.set()
            await release.wait()
            raise AssertionError("late STT result must be discarded")

    monkeypatch.setattr(oral_defense, "_transcription_adapter_factory", _CancelledSTT)
    session = _seed_defense(db_session)
    config = (
        db_session.query(models.DefenseActivityConfig)
        .filter_by(activity_configuration_id=session.activity_configuration_id)
        .one()
    )
    config.voice_input_allowed = True
    spool = tempfile.SpooledTemporaryFile(max_size=1)
    spool.write(_wav())
    spool.seek(0)
    assert spool._rolled is True
    upload = UploadFile(
        file=spool,
        filename="answer.wav",
        headers=Headers({"content-type": "audio/wav"}),
    )
    task = asyncio.create_task(oral_defense.post_defense_voice_turn(session.id, upload, db_session))
    await started.wait()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert spool.closed
    release.set()
    await asyncio.sleep(0)
    assert db_session.query(models.Transcript).filter_by(session_id=session.id).count() == 0
