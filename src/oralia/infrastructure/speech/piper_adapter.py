"""Optional local Piper adapter; voice bytes remain request-scoped."""

import asyncio
import io
import wave

from oralia.infrastructure.speech.blocking_speech_worker import (
    BoundedSpeechWorker,
    default_blocking_speech_worker,
)
from oralia.infrastructure.speech.config import (
    MAX_SYNTHESIZED_AUDIO_BYTES,
    SpeechSettings,
    settings,
)
from oralia.infrastructure.speech.synthesis_port import SynthesisOutcome


class PiperSpeechSynthesisAdapter:
    def __init__(
        self,
        *,
        config: SpeechSettings | None = None,
        worker: BoundedSpeechWorker | None = None,
    ) -> None:
        self._config = config or settings()
        self._worker = worker or default_blocking_speech_worker()

    def _synthesize_sync(self, text: str) -> SynthesisOutcome:
        if self._config.tts_voice is None:
            return SynthesisOutcome(ok=False, error_code="voice_not_configured")
        from piper import PiperVoice

        voice = PiperVoice.load(self._config.tts_voice)
        buffer = _BoundedBytesIO(MAX_SYNTHESIZED_AUDIO_BYTES)
        with wave.open(buffer, "wb") as wav_file:
            voice.synthesize_wav(text, wav_file)
        return SynthesisOutcome(ok=True, audio=buffer.getvalue())

    async def synthesize(self, text: str, *, language: str) -> SynthesisOutcome:
        del language
        try:
            return await asyncio.wait_for(
                self._worker.run(self._synthesize_sync, text),
                timeout=self._config.tts_timeout_ms / 1000,
            )
        except TimeoutError:
            return SynthesisOutcome(ok=False, error_code="timeout")
        except Exception:
            return SynthesisOutcome(ok=False, error_code="synthesis_failed")


class _BoundedBytesIO(io.BytesIO):
    def __init__(self, maximum: int) -> None:
        super().__init__()
        self._maximum = maximum

    def write(self, data: bytes) -> int:
        if self.tell() + len(data) > self._maximum:
            raise ValueError("synthesized audio exceeds configured limit")
        return super().write(data)


__all__ = ["PiperSpeechSynthesisAdapter"]
