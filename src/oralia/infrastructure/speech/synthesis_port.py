"""Structured port for local text-to-speech."""

from typing import Protocol

from pydantic import BaseModel, ConfigDict


class SynthesisOutcome(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    ok: bool
    audio: bytes | None = None
    media_type: str = "audio/wav"
    error_code: str | None = None


class SpeechSynthesisPort(Protocol):
    async def synthesize(self, text: str, *, language: str) -> SynthesisOutcome: ...


__all__ = ["SpeechSynthesisPort", "SynthesisOutcome"]
