"""Deterministic speech doubles; they never load a model or touch the filesystem."""

import io
import wave

from oralia.infrastructure.speech.synthesis_port import SynthesisOutcome
from oralia.infrastructure.speech.transcription_port import (
    TranscriptionOutcome,
    TranscriptionSegment,
)


class FakeTranscriptionAdapter:
    def __init__(self, outcome: TranscriptionOutcome | None = None) -> None:
        self.outcome = outcome or TranscriptionOutcome(
            ok=True,
            text="respuesta transcrita",
            segments=(
                TranscriptionSegment(
                    text="respuesta transcrita",
                    start_ms=0,
                    end_ms=1000,
                    confidence=0.99,
                ),
            ),
            overall_confidence=0.99,
            low_confidence=False,
        )
        self.calls = 0

    async def transcribe(self, audio: bytes, *, language: str) -> TranscriptionOutcome:
        del audio, language
        self.calls += 1
        return self.outcome


class FakeSpeechSynthesisAdapter:
    def __init__(self, outcome: SynthesisOutcome | None = None) -> None:
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as audio:
            audio.setnchannels(1)
            audio.setsampwidth(2)
            audio.setframerate(8000)
            audio.writeframes(b"\0\0" * 80)
        self.outcome = outcome or SynthesisOutcome(ok=True, audio=buffer.getvalue())
        self.calls: list[str] = []

    async def synthesize(self, text: str, *, language: str) -> SynthesisOutcome:
        del language
        self.calls.append(text)
        return self.outcome


__all__ = ["FakeSpeechSynthesisAdapter", "FakeTranscriptionAdapter"]
