import asyncio
import hashlib
import threading

import pytest
from pydantic import ValidationError

from oralia.domain.policies.output_template_catalog import (
    DEFAULT_OUTPUT_TEMPLATE_CATALOG,
    DEFENSE_DYNAMIC_OUTPUT,
)
from oralia.infrastructure.speech.blocking_speech_worker import BoundedSpeechWorker
from oralia.infrastructure.speech.synthesis_port import SynthesisOutcome
from oralia.infrastructure.speech.transcription_port import (
    TranscriptionOutcome,
    TranscriptionSegment,
)


def test_defense_template_resolves_by_complete_identity() -> None:
    resolved = DEFAULT_OUTPUT_TEMPLATE_CATALOG.resolve(*DEFENSE_DYNAMIC_OUTPUT.identity)
    assert resolved == DEFENSE_DYNAMIC_OUTPUT
    assert resolved.sha256 == hashlib.sha256(resolved.text.encode()).hexdigest()
    with pytest.raises(KeyError):
        DEFAULT_OUTPUT_TEMPLATE_CATALOG.resolve(resolved.template_id, resolved.version, "0" * 64)


def test_speech_contracts_are_closed_and_immutable() -> None:
    segment = TranscriptionSegment(text="hola", confidence=0.9)
    outcome = TranscriptionOutcome(ok=True, text="hola", segments=(segment,), overall_confidence=0.9)
    assert isinstance(outcome.segments, tuple)
    with pytest.raises(ValidationError):
        TranscriptionOutcome(ok=True, text="hola", unexpected=True)
    with pytest.raises(ValidationError):
        SynthesisOutcome(ok=True, audio=b"wav", unexpected=True)


@pytest.mark.asyncio
async def test_bounded_speech_worker_never_exceeds_capacity() -> None:
    worker = BoundedSpeechWorker(capacity=1)
    started = threading.Event()
    release = threading.Event()
    active = 0
    peak = 0
    lock = threading.Lock()

    def blocking() -> str:
        nonlocal active, peak
        with lock:
            active += 1
            peak = max(peak, active)
        started.set()
        release.wait(2)
        with lock:
            active -= 1
        return "ok"

    first = asyncio.create_task(worker.run(blocking))
    assert await asyncio.to_thread(started.wait, 1)
    second = asyncio.create_task(worker.run(blocking))
    await asyncio.sleep(0.02)
    assert peak == 1
    release.set()
    assert await first == "ok"
    assert await second == "ok"
    assert peak == 1
    worker.shutdown()
