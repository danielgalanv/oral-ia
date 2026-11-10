"""Acceptance matrix for explicit self-study retention authorization."""

from __future__ import annotations

import uuid
from datetime import timedelta

import pytest

from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from tests.t090_policy_helpers import minimal_output_policy_columns

_FEATURE_EVENTS = (
    "generation_call",
    "non_disclosure_check",
    "verification_combined",
    "study_session_summary",
    "agents_selected",
)
_SHARED_EVENTS = ("session_started", "session_closed", "agent_execution")


def _closed_session(
    app_client,
    *,
    retention_authorized: bool | None,
    retention_days: int | None,
    age_days: int = 10,
) -> tuple[str, str]:
    db = app_client.__db_sessionmaker__()
    suffix = uuid.uuid4().hex
    course = models.Course(name="Retention acceptance", subject_code=f"R{suffix[:8]}")
    policy = models.RetentionPolicy(
        content_scope="session",
        retention_days=retention_days,
        access_scope="profesor",
        purge_rule="manual",
    )
    participant = models.ParticipantCode(code=f"retention-{suffix}")
    db.add_all([course, policy, participant])
    db.flush()
    activity = models.ActivityConfiguration(
        course_id=course.id,
        name="Retention acceptance",
        subject="Retention",
        objective="Exercise the retention matrix",
        mode="self_study",
        language="es",
        max_turns=5,
        max_duration_seconds=600,
        retention_policy_id=policy.id,
        **minimal_output_policy_columns(recipients=(participant.code,)),
    )
    db.add(activity)
    db.flush()
    config = models.SelfStudyActivityConfig(
        activity_configuration_id=activity.id,
        enabled_modes=["doubt_resolution"],
        summary_authorized=False,
        practice_reveals_solution=False,
        retention_authorized=retention_authorized,
    )
    session = models.Session(
        activity_configuration_id=activity.id,
        participant_code=participant.code,
        status="closed_voluntary",
        ended_at=utcnow() - timedelta(days=age_days),
    )
    db.add_all([config, session])
    db.flush()
    db.commit()
    result = (activity.id, session.id)
    db.close()
    return result


def _add_events(app_client, session_id: str, event_types: tuple[str, ...]) -> None:
    db = app_client.__db_sessionmaker__()
    for event_type in event_types:
        db.add(
            models.TraceEvent(
                session_id=session_id,
                event_type=event_type,
                payload={},
                memory_category="episodic",
            )
        )
    db.commit()
    db.close()


@pytest.mark.contract
def test_not_authorized_purges_feature_rows_immediately_and_remains_eligible(app_client) -> None:
    _, session_id = _closed_session(
        app_client,
        retention_authorized=False,
        retention_days=None,
        age_days=0,
    )
    _add_events(app_client, session_id, _FEATURE_EVENTS + _SHARED_EVENTS)

    first = app_client.post("/api/v1/tecnica/self-study/purge-expired").json()
    second = app_client.post("/api/v1/tecnica/self-study/purge-expired").json()

    assert first["sessions_matching_criteria"] == 1
    assert first["sessions_with_rows_deleted"] == 1
    assert first["trace_events_deleted"] == len(_FEATURE_EVENTS)
    assert second["sessions_matching_criteria"] == 1
    assert second["sessions_with_rows_deleted"] == 0

    db = app_client.__db_sessionmaker__()
    remaining = {
        event.event_type
        for event in db.query(models.TraceEvent).filter_by(session_id=session_id).all()
    }
    db.close()
    assert remaining == set(_SHARED_EVENTS)


@pytest.mark.contract
@pytest.mark.parametrize(
    ("retention_authorized", "retention_days", "state"),
    [
        (None, 1, "undecided_preexisting"),
        (True, None, "invalid_authorized_without_policy"),
    ],
)
def test_non_purgeable_states_are_audited_without_side_effects(
    app_client,
    retention_authorized: bool | None,
    retention_days: int | None,
    state: str,
) -> None:
    activity_id, session_id = _closed_session(
        app_client,
        retention_authorized=retention_authorized,
        retention_days=retention_days,
    )
    _add_events(app_client, session_id, ("generation_call",))

    first_audit = app_client.get("/api/v1/tecnica/self-study/retention-audit").json()
    second_audit = app_client.get("/api/v1/tecnica/self-study/retention-audit").json()
    assert first_audit == second_audit
    assert {item["activity_configuration_id"] for item in first_audit[state]} == {activity_id}

    for _ in range(2):
        result = app_client.post("/api/v1/tecnica/self-study/purge-expired").json()
        assert result["sessions_matching_criteria"] == 0
        assert result["sessions_with_rows_deleted"] == 0

    db = app_client.__db_sessionmaker__()
    assert db.query(models.TraceEvent).filter_by(session_id=session_id).count() == 1
    db.close()


@pytest.mark.contract
def test_authorized_finite_retention_only_purges_after_expiry(app_client) -> None:
    _, expired_id = _closed_session(
        app_client,
        retention_authorized=True,
        retention_days=1,
        age_days=10,
    )
    _, current_id = _closed_session(
        app_client,
        retention_authorized=True,
        retention_days=30,
        age_days=1,
    )
    _add_events(app_client, expired_id, ("generation_call",))
    _add_events(app_client, current_id, ("generation_call",))

    result = app_client.post("/api/v1/tecnica/self-study/purge-expired").json()
    assert result["sessions_matching_criteria"] == 1
    assert result["sessions_with_rows_deleted"] == 1

    db = app_client.__db_sessionmaker__()
    assert db.query(models.TraceEvent).filter_by(session_id=expired_id).count() == 0
    assert db.query(models.TraceEvent).filter_by(session_id=current_id).count() == 1
    db.close()
