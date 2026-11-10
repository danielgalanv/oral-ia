"""Optional local Faster Whisper adapter; the dependency is imported lazily."""

import asyncio
import io

from oralia.infrastructure.speech.blocking_speech_worker import (
    BoundedSpeechWorker,
    default_blocking_speech_worker,
)
from oralia.infrastructure.speech.config import SpeechSettings, settings
from oralia.infrastructure.speech.transcription_port import (
    TranscriptionOutcome,
    TranscriptionSegment,
)


class FasterWhisperTranscriptionAdapter:
    def __init__(
        self,
        *,
        config: SpeechSettings | None = None,
        worker: BoundedSpeechWorker | None = None,
    ) -> None:
        self._config = config or settings()
        self._worker = worker or default_blocking_speech_worker()

    def _transcribe_sync(self, audio: bytes, language: str) -> TranscriptionOutcome:
        if self._config.stt_model is None:
            return TranscriptionOutcome(ok=False, text="", error_code="model_not_configured")
        from faster_whisper import WhisperModel

        model = WhisperModel(
            self._config.stt_model,
            device=self._config.stt_device,
            compute_type=self._config.stt_compute_type,
            local_files_only=True,
        )
        raw_segments, _info = model.transcribe(io.BytesIO(audio), language=language)
        segments: list[TranscriptionSegment] = []
        for segment in raw_segments:
            confidence = max(0.0, min(1.0, 1.0 - float(getattr(segment, "no_speech_prob", 0.0))))
            segments.append(
                TranscriptionSegment(
                    text=segment.text,
                    start_ms=int(segment.start * 1000),
                    end_ms=int(segment.end * 1000),
                    confidence=confidence,
                )
            )
        text = "".join(item.text for item in segments).strip()
        overall = sum(item.confidence for item in segments) / len(segments) if segments else 0.0
        low = any(item.confidence < self._config.low_confidence_threshold for item in segments)
        return TranscriptionOutcome(
            ok=True,
            text=text,
            segments=tuple(segments),
            overall_confidence=overall,
            low_confidence=low,
        )

    async def transcribe(self, audio: bytes, *, language: str) -> TranscriptionOutcome:
        try:
            return await asyncio.wait_for(
                self._worker.run(self._transcribe_sync, audio, language),
                timeout=self._config.stt_timeout_ms / 1000,
            )
        except TimeoutError:
            return TranscriptionOutcome(ok=False, text="", error_code="timeout")
        except Exception:
            return TranscriptionOutcome(ok=False, text="", error_code="transcription_failed")


__all__ = ["FasterWhisperTranscriptionAdapter"]
