"""Manual purge of expired Feature 004 retained data."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from sqlalchemy.orm import Session as SASession

from oralia.application.commands.end_defense_session import clear_summary_text
from oralia.application.services.defense_retention_service import erase_defense_content
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow


@dataclass
class DefensePurgeResult:
    sessions_matching_criteria: int = 0
    sessions_with_rows_deleted: int = 0
    transcripts_deleted: int = 0
    transcript_corrections_deleted: int = 0
    trace_events_deleted: int = 0


def purge_expired_defense_data(db: SASession) -> DefensePurgeResult:
    result = DefensePurgeResult()
    now = utcnow()
    rows = (
        db.query(models.Session, models.ActivityConfiguration, models.ConsentRecord)
        .join(
            models.ActivityConfiguration,
            models.Session.activity_configuration_id == models.ActivityConfiguration.id,
        )
        .join(
            models.DefenseActivityConfig,
            models.DefenseActivityConfig.activity_configuration_id == models.ActivityConfiguration.id,
        )
        .join(models.ConsentRecord, models.ConsentRecord.session_id == models.Session.id)
        .filter(
            models.ActivityConfiguration.mode == "oral_defense",
            models.Session.ended_at.isnot(None),
            models.ConsentRecord.decision == "retain",
        )
        .all()
    )
    for session, activity, consent in rows:
        policy = db.get(models.RetentionPolicy, activity.retention_policy_id)
        if (
            policy is None
            or policy.retention_days is None
            or session.ended_at + timedelta(days=policy.retention_days) >= now
        ):
            continue
        result.sessions_matching_criteria += 1
        retained_scope = frozenset(consent.scope or [])
        corrections_deleted = 0
        transcripts_deleted = 0
        summaries_deleted = 0
        auxiliary_deleted = 0
        if "transcript" in retained_scope:
            auxiliary_deleted = erase_defense_content(db, session.id)
            corrections_deleted = (
                db.query(models.TranscriptCorrection).filter_by(session_id=session.id).delete()
            )
            transcripts_deleted = db.query(models.Transcript).filter_by(session_id=session.id).delete()
        if "summary" in retained_scope:
            clear_summary_text(db, session.id)
            summaries_deleted = (
                db.query(models.TraceEvent)
                .filter_by(session_id=session.id, event_type="defense_session_summary")
                .delete()
            )
        result.transcript_corrections_deleted += corrections_deleted
        result.transcripts_deleted += transcripts_deleted
        result.trace_events_deleted += summaries_deleted
        if corrections_deleted + transcripts_deleted + summaries_deleted + auxiliary_deleted:
            result.sessions_with_rows_deleted += 1
    db.flush()
    return result


__all__ = ["DefensePurgeResult", "purge_expired_defense_data"]
