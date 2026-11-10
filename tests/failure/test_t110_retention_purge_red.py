"""T110 reproductions for retention authorization and feature-owned trace deletion."""

from __future__ import annotations

from datetime import timedelta

import pytest

from oralia.application.commands.purge_expired_self_study_data import (
    purge_expired_self_study_data,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from tests.t090_policy_helpers import minimal_output_policy_columns

_FEATURE_EVENTS = {
    "generation_call",
    "non_disclosure_check",
    "verification_combined",
    "study_session_summary",
    "agents_selected",
}
_SHARED_EVENTS = {"session_started", "session_closed", "agent_execution"}


def _closed_session(db_session, *, retention_days: int | None, retention_authorized: bool):
    course = models.Course(name="Retention course", subject_code="RET101")
    policy = models.RetentionPolicy(
        content_scope="session",
        retention_days=retention_days,
        access_scope="profesor",
        purge_rule="manual",
    )
    participant = models.ParticipantCode(code=f"retention-{retention_days}")
    db_session.add_all([course, policy, participant])
    db_session.flush()
    activity = models.ActivityConfiguration(
        course_id=course.id,
        name="Retention activity",
        subject="Retention",
        objective="Test retention",
        mode="self_study",
        language="es",
        max_turns=5,
        max_duration_seconds=600,
        retention_policy_id=policy.id,
        **minimal_output_policy_columns(recipients=(participant.code,)),
    )
    db_session.add(activity)
    db_session.flush()
    config = models.SelfStudyActivityConfig(
        activity_configuration_id=activity.id,
        enabled_modes=["doubt_resolution"],
        summary_authorized=False,
        practice_reveals_solution=False,
    )
    config.retention_authorized = retention_authorized
    session = models.Session(
        activity_configuration_id=activity.id,
        participant_code=participant.code,
        status="closed_voluntary",
        ended_at=utcnow() - timedelta(days=10),
    )
    db_session.add_all([config, session])
    db_session.flush()
    return session


@pytest.mark.failure
def test_explicit_false_is_purgeable_immediately_even_without_finite_period(db_session) -> None:
    session = _closed_session(
        db_session,
        retention_days=None,
        retention_authorized=False,
    )
    db_session.add(
        models.TraceEvent(
            session_id=session.id,
            event_type="generation_call",
            payload={},
            memory_category="episodic",
        )
    )
    db_session.flush()

    result = purge_expired_self_study_data(db_session)

    if hasattr(result, "sessions_evaluated"):
        assert result.sessions_evaluated == 0
    assert result.sessions_matching_criteria == 1
    assert result.sessions_with_rows_deleted == 1
    assert result.trace_events_deleted == 1


@pytest.mark.failure
def test_purge_deletes_only_feature_owned_trace_types(db_session) -> None:
    session = _closed_session(
        db_session,
        retention_days=1,
        retention_authorized=True,
    )
    for event_type in sorted(_FEATURE_EVENTS | _SHARED_EVENTS):
        db_session.add(
            models.TraceEvent(
                session_id=session.id,
                event_type=event_type,
                payload={},
                memory_category="episodic",
            )
        )
    db_session.flush()

    result = purge_expired_self_study_data(db_session)
    remaining = {
        event.event_type
        for event in db_session.query(models.TraceEvent).filter_by(session_id=session.id).all()
    }

    assert result.trace_events_deleted == len(_FEATURE_EVENTS)
    assert remaining == _SHARED_EVENTS
