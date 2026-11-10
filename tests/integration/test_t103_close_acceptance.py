"""Acceptance for preserving a safe terminal close while evaluating turn limits."""

from __future__ import annotations

from datetime import timedelta

import pytest

from oralia.application.commands import submit_study_turn as submit_module
from oralia.application.orchestration.study_turn_orchestrator import StudyTurnResult
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from tests.t090_policy_helpers import minimal_output_policy_columns


@pytest.mark.integration
async def test_limit_check_preserves_safe_close_and_does_not_generate_summary(
    db_session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    course = models.Course(name="Safe close", subject_code="SAFE")
    policy = models.RetentionPolicy(
        content_scope="session",
        retention_days=30,
        access_scope="profesor",
        purge_rule="manual",
    )
    participant = models.ParticipantCode(code="safe-close-participant")
    db_session.add_all([course, policy, participant])
    db_session.flush()
    activity = models.ActivityConfiguration(
        course_id=course.id,
        name="Safe close",
        subject="Safety",
        objective="Preserve the winning terminal state",
        mode="self_study",
        language="es",
        max_turns=1,
        max_duration_seconds=600,
        retention_policy_id=policy.id,
        **minimal_output_policy_columns(recipients=(participant.code,)),
    )
    db_session.add(activity)
    db_session.flush()
    db_session.add(
        models.SelfStudyActivityConfig(
            activity_configuration_id=activity.id,
            enabled_modes=["doubt_resolution"],
            summary_authorized=True,
            practice_reveals_solution=False,
            retention_authorized=True,
        )
    )
    session = models.Session(
        activity_configuration_id=activity.id,
        participant_code=participant.code,
        status="active",
    )
    db_session.add(session)
    db_session.flush()

    async def safe_closing_turn(db, active_session, _text):
        active_session.turn_count = 1
        active_session.status = "closed_error_safe"
        active_session.ended_at = utcnow() - timedelta(seconds=1)
        db.flush()
        return StudyTurnResult(
            turn_id="safe-turn",
            mode="doubt_resolution",
            dialogue_action="finish",
            output_text=None,
            blocked=True,
            state_version=None,
            status="blocked",
        )

    monkeypatch.setattr(submit_module, "run_study_turn", safe_closing_turn)
    result = await submit_module.submit_study_turn(db_session, session, "entrada")

    assert result.session_closed is True
    assert result.session_status == "closed_error_safe"
    assert result.study_summary is None
    assert session.status == "closed_error_safe"
    assert (
        db_session.query(models.TraceEvent)
        .filter_by(session_id=session.id, event_type="study_session_summary")
        .count()
        == 0
    )
