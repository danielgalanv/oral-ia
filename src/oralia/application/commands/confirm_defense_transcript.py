"""Confirm/correct a provisional transcript, then enter the text pipeline once."""

from sqlalchemy.orm import Session as SASession

from oralia.application.commands.submit_defense_turn import submit_defense_turn
from oralia.application.services.trace_service import record_event
from oralia.infrastructure.db import models


class TranscriptNotConfirmable(ValueError):
    pass


async def confirm_defense_transcript(
    db: SASession,
    session: models.Session,
    transcript_id: str,
    corrected_text: str | None,
    *,
    closure_retain: bool = False,
    closure_scope: list[str] | None = None,
):
    transcript = db.get(models.Transcript, transcript_id)
    supersedes_transcript_id = None
    if session.status != "active":
        raise TranscriptNotConfirmable("session is no longer active")
    if (
        transcript is not None
        and transcript.session_id == session.id
        and transcript.status == "confirmed"
        and corrected_text is not None
        and corrected_text.strip()
    ):
        # A late revision is a new definitive input. The confirmed record and the
        # question already delivered from it remain immutable and reconstructible.
        supersedes_transcript_id = transcript.id
        transcript = models.Transcript(
            session_id=session.id,
            raw_text=transcript.raw_text,
            segments=transcript.segments,
            overall_confidence=transcript.overall_confidence,
            low_confidence=transcript.low_confidence,
            status="awaiting_confirmation",
        )
        db.add(transcript)
        db.flush()
    if (
        transcript is None
        or transcript.session_id != session.id
        or transcript.status != "awaiting_confirmation"
    ):
        raise TranscriptNotConfirmable("transcript is absent or no longer confirmable")
    definitive_text = transcript.raw_text
    if corrected_text is not None:
        if not corrected_text.strip():
            raise TranscriptNotConfirmable("corrected_text cannot be blank")
        correction = models.TranscriptCorrection(
            transcript_id=transcript.id,
            session_id=session.id,
            corrected_text=corrected_text,
        )
        db.add(correction)
        db.flush()
        definitive_text = corrected_text
        record_event(
            db,
            session_id=session.id,
            event_type="transcript_corrected",
            payload={
                "transcript_id": transcript.id,
                "correction_id": correction.id,
                "supersedes_transcript_id": supersedes_transcript_id,
            },
            memory_category="procedural",
        )
    transcript.status = "confirmed"
    db.add(transcript)
    result = await submit_defense_turn(
        db, session, definitive_text, closure_retain=closure_retain, closure_scope=closure_scope
    )
    if db.get(models.Transcript, transcript.id) is not None:
        transcript.turn_id = result.turn_id
        db.add(transcript)
    return result


__all__ = ["TranscriptNotConfirmable", "confirm_defense_transcript"]
