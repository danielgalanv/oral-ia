"""Strict environment configuration for bounded local speech processing."""

import os
from dataclasses import dataclass

MAX_AUDIO_BYTES = 10 * 1024 * 1024
MAX_AUDIO_DURATION_SECONDS = 300.0
MAX_SYNTHESIZED_AUDIO_BYTES = 10 * 1024 * 1024


def _positive_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if value < 1:
        raise ValueError(f"{name} must be positive")
    return value


def _threshold() -> float:
    raw = os.getenv("ORALIA_STT_LOW_CONFIDENCE_THRESHOLD", "0.6")
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError("ORALIA_STT_LOW_CONFIDENCE_THRESHOLD must be numeric") from exc
    if not 0.0 <= value <= 1.0:
        raise ValueError("ORALIA_STT_LOW_CONFIDENCE_THRESHOLD must be between 0 and 1")
    return value


@dataclass(frozen=True, slots=True)
class SpeechSettings:
    stt_model: str | None
    stt_device: str
    stt_compute_type: str
    tts_voice: str | None
    low_confidence_threshold: float
    worker_capacity: int
    stt_timeout_ms: int
    tts_timeout_ms: int


def settings() -> SpeechSettings:
    return SpeechSettings(
        stt_model=os.getenv("ORALIA_STT_MODEL") or None,
        stt_device=os.getenv("ORALIA_STT_DEVICE", "cpu"),
        stt_compute_type=os.getenv("ORALIA_STT_COMPUTE_TYPE", "int8"),
        tts_voice=os.getenv("ORALIA_TTS_VOICE") or None,
        low_confidence_threshold=_threshold(),
        worker_capacity=_positive_int("ORALIA_SPEECH_WORKER_CAPACITY", 1),
        stt_timeout_ms=_positive_int("ORALIA_STT_TIMEOUT_MS", 60_000),
        tts_timeout_ms=_positive_int("ORALIA_TTS_TIMEOUT_MS", 30_000),
    )


__all__ = [
    "MAX_AUDIO_BYTES",
    "MAX_AUDIO_DURATION_SECONDS",
    "MAX_SYNTHESIZED_AUDIO_BYTES",
    "SpeechSettings",
    "settings",
]
