"""US5 Escenario D: two StatePatch attempts against the same base_version — only one is
applied, the other is rejected and traced, never silently overwritten (FR-019)."""

import pytest

from oralia.domain.cognitive_state.cognitive_state import get_or_create
from oralia.domain.cognitive_state.state_patch import apply_patch
from oralia.infrastructure.db import models


@pytest.fixture()
def seeded_session(db_session):
    """Deliberate historical NULL/NULL activity; state-patch conflict emits no output."""
    course = models.Course(name="C", subject_code="C1")
    policy = models.RetentionPolicy(content_scope="session", access_scope="profesor", purge_rule="manual")
    db_session.add_all([course, policy])
    db_session.flush()
    activity = models.ActivityConfiguration(
        course_id=course.id,
        name="A",
        subject="s",
        objective="o",
        mode="texto",
        language="es",
        max_turns=10,
        max_duration_seconds=600,
        retention_policy_id=policy.id,
    )
    db_session.add(activity)
    db_session.flush()
    assert activity.output_authorization_policy_json is None
    assert activity.output_authorization_policy_sha256 is None
    participant = models.ParticipantCode(code="part-conflict001")
    db_session.add(participant)
    db_session.flush()
    session = models.Session(activity_configuration_id=activity.id, participant_code=participant.code)
    db_session.add(session)
    db_session.flush()
    get_or_create(db_session, session.id, activity_ref=activity.id)
    db_session.flush()
    return session


@pytest.mark.failure
def test_only_one_of_two_concurrent_patches_is_applied(db_session, seeded_session):
    p1 = apply_patch(
        db_session,
        session_id=seeded_session.id,
        base_version=0,
        proposed_by_agent_id="agent-a",
        element_type="observation",
        payload={"current_input": "primero"},
    )
    p2 = apply_patch(
        db_session,
        session_id=seeded_session.id,
        base_version=0,  # stale — p1 already advanced the version
        proposed_by_agent_id="agent-b",
        element_type="observation",
        payload={"current_input": "segundo"},
    )

    assert p1.applied is True
    assert p2.applied is False
    assert p2.rejected_reason is not None

    state = db_session.get(models.CognitiveState, seeded_session.id)
    assert state.current_input == "primero"  # not silently overwritten by p2


@pytest.mark.failure
def test_rejected_patch_is_not_silently_dropped(db_session, seeded_session):
    apply_patch(
        db_session,
        session_id=seeded_session.id,
        base_version=0,
        proposed_by_agent_id="agent-a",
        element_type="observation",
        payload={"current_input": "primero"},
    )
    apply_patch(
        db_session,
        session_id=seeded_session.id,
        base_version=0,
        proposed_by_agent_id="agent-b",
        element_type="observation",
        payload={"current_input": "segundo"},
    )

    all_patches = (
        db_session.query(models.StatePatch).filter(models.StatePatch.session_id == seeded_session.id).all()
    )
    assert len(all_patches) == 2
    assert {p.applied for p in all_patches} == {True, False}
