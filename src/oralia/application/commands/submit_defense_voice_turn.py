"""Transcribe one ephemeral audio upload without entering the cognitive pipeline."""

import asyncio

from sqlalchemy.orm import Session as SASession

from oralia.application.services.trace_service import record_event
from oralia.infrastructure.db import models
from oralia.infrastructure.speech.config import settings
from oralia.infrastructure.speech.transcription_port import TranscriptionOutcome, TranscriptionPort


class TranscriptionUnavailable(RuntimeError):
    pass


async def submit_defense_voice_turn(
    db: SASession,
    session: models.Session,
    audio: bytes,
    *,
    language: str,
    transcription_port: TranscriptionPort,
) -> models.Transcript:
    try:
        outcome = await asyncio.wait_for(
            transcription_port.transcribe(audio, language=language),
            timeout=settings().stt_timeout_ms / 1000,
        )
    except Exception:
        outcome = TranscriptionOutcome(ok=False, text="", error_code="transcription_failed")
    finally:
        del audio
    db.refresh(session)
    if session.status != "active":
        raise TranscriptionUnavailable("session_closed")
    if not outcome.ok:
        record_event(
            db,
            session_id=session.id,
            event_type="transcription_failed",
            payload={"reason": outcome.error_code or "unknown"},
            memory_category="metacognitive",
        )
        raise TranscriptionUnavailable(outcome.error_code or "transcription failed")
    transcript = models.Transcript(
        session_id=session.id,
        raw_text=outcome.text,
        segments=[item.model_dump(mode="json") for item in outcome.segments],
        overall_confidence=outcome.overall_confidence,
        low_confidence=outcome.low_confidence,
        status="awaiting_confirmation",
    )
    db.add(transcript)
    db.flush()
    record_event(
        db,
        session_id=session.id,
        event_type="transcription_recorded",
        payload={
            "transcript_id": transcript.id,
            "overall_confidence": transcript.overall_confidence,
            "low_confidence_segment_count": sum(
                1 for item in outcome.segments if item.confidence < settings().low_confidence_threshold
            ),
        },
        memory_category="procedural",
    )
    return transcript


__all__ = ["TranscriptionUnavailable", "submit_defense_voice_turn"]
