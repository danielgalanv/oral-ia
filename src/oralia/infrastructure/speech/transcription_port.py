"""Structured port for local speech-to-text."""

from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field


class TranscriptionSegment(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    text: str
    start_ms: int | None = None
    end_ms: int | None = None
    confidence: float = Field(ge=0.0, le=1.0)


class TranscriptionOutcome(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    ok: bool
    text: str
    segments: tuple[TranscriptionSegment, ...] = ()
    overall_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    low_confidence: bool = False
    error_code: str | None = None


class TranscriptionPort(Protocol):
    async def transcribe(self, audio: bytes, *, language: str) -> TranscriptionOutcome: ...


__all__ = ["TranscriptionOutcome", "TranscriptionPort", "TranscriptionSegment"]
