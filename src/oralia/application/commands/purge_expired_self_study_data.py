"""Manual purge of Feature 003-derived data (FR-028/FR-028a)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from sqlalchemy.orm import Session as SASession

from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow


@dataclass
class PurgeResult:
    sessions_matching_criteria: int = 0
    sessions_with_rows_deleted: int = 0
    practice_questions_deleted: int = 0
    coherence_incidents_deleted: int = 0
    trace_events_deleted: int = 0


def purge_expired_self_study_data(db: SASession) -> PurgeResult:
    result = PurgeResult()
    now = utcnow()

    # Scoped to self-study sessions only (activities with a SelfStudyActivityConfig) —
    # a Feature 001-only session's TraceEvent rows MUST NOT be touched by this feature.
    sessions = (
        db.query(models.Session)
        .join(
            models.ActivityConfiguration,
            models.Session.activity_configuration_id == models.ActivityConfiguration.id,
        )
        .join(
            models.SelfStudyActivityConfig,
            models.SelfStudyActivityConfig.activity_configuration_id == models.ActivityConfiguration.id,
        )
        .filter(
            models.Session.ended_at.isnot(None),
        )
        .all()
    )

    for session in sessions:
        activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
        policy = db.get(models.RetentionPolicy, activity.retention_policy_id)
        config = (
            db.query(models.SelfStudyActivityConfig)
            .filter_by(activity_configuration_id=activity.id)
            .one()
        )
        finite_days = policy.retention_days if policy is not None else None
        purgeable_without_delay = config.retention_authorized is False
        purgeable_after_expiry = (
            config.retention_authorized is True
            and finite_days is not None
            and session.ended_at + timedelta(days=finite_days) < now
        )
        if not (purgeable_without_delay or purgeable_after_expiry):
            continue

        result.sessions_matching_criteria += 1

        practice_deleted = (
            db.query(models.PracticeQuestion)
            .filter(models.PracticeQuestion.session_id == session.id)
            .delete()
        )
        incidents_deleted = (
            db.query(models.CoherenceIncident)
            .filter(models.CoherenceIncident.session_id == session.id)
            .delete()
        )
        trace_deleted = (
            db.query(models.TraceEvent)
            .filter(
                models.TraceEvent.session_id == session.id,
                models.TraceEvent.event_type.in_(
                    (
                        "generation_call",
                        "non_disclosure_check",
                        "verification_combined",
                        "study_session_summary",
                        "agents_selected",
                    )
                ),
            )
            .delete(synchronize_session=False)
        )
        result.practice_questions_deleted += practice_deleted
        result.coherence_incidents_deleted += incidents_deleted
        result.trace_events_deleted += trace_deleted
        if practice_deleted + incidents_deleted + trace_deleted:
            result.sessions_with_rows_deleted += 1

    db.flush()
    return result
