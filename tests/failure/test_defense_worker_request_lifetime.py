import asyncio
import threading

import pytest

from oralia.application.commands.submit_defense_voice_turn import (
    TranscriptionUnavailable,
    submit_defense_voice_turn,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.speech.blocking_speech_worker import BoundedSpeechWorker
from oralia.infrastructure.speech.faster_whisper_adapter import FasterWhisperTranscriptionAdapter
from oralia.infrastructure.speech.transcription_port import TranscriptionOutcome
from tests.failure.test_defense_speech_timeout_late_results import _settings
from tests.integration.test_defense_text_turn import _seed_defense


@pytest.mark.parametrize("waiting", [False, True])
async def test_request_timeout_discards_waiting_or_running_speech_result(db_session, monkeypatch, waiting):
    session = _seed_defense(db_session)
    worker = BoundedSpeechWorker(capacity=1)
    entered = threading.Event()
    release = threading.Event()
    finished = threading.Event()
    calls = []

    def occupy():
        entered.set()
        release.wait(3)

    def transcribe(audio, language):
        calls.append(True)
        entered.set()
        release.wait(3)
        finished.set()
        return TranscriptionOutcome(ok=True, text="late result")

    occupying = None
    adapter = FasterWhisperTranscriptionAdapter(config=_settings(), worker=worker)
    monkeypatch.setattr(adapter, "_transcribe_sync", transcribe)
    try:
        if waiting:
            occupying = asyncio.create_task(worker.run(occupy))
            assert await asyncio.get_running_loop().run_in_executor(None, entered.wait, 2)
        with pytest.raises(TranscriptionUnavailable):
            await submit_defense_voice_turn(
                db_session, session, b"ephemeral", language="es", transcription_port=adapter
            )
        count_before = db_session.query(models.TraceEvent).count()
        release.set()
        if occupying:
            await occupying
        else:
            assert await asyncio.get_running_loop().run_in_executor(None, finished.wait, 2)
        await asyncio.sleep(0)
        assert len(calls) == int(not waiting)
        assert db_session.query(models.Transcript).count() == 0
        assert db_session.query(models.TranscriptCorrection).count() == 0
        assert db_session.query(models.TraceEvent).count() == count_before
        assert session.turn_count == 0
    finally:
        release.set()
        worker.shutdown()
