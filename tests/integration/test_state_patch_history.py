"""US5/US6: the full StatePatch history (applied and rejected) is reconstructable and
chronologically ordered — the basis for both conflict audit and session reconstruction."""

import pytest

from oralia.domain.cognitive_state.cognitive_state import get_or_create
from oralia.domain.cognitive_state.state_patch import apply_patch, history_for_session
from oralia.infrastructure.db import models
from tests.t090_policy_helpers import minimal_output_policy_columns


@pytest.fixture()
def seeded_session(db_session):
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
        **minimal_output_policy_columns(recipients=("part-history001",)),
    )
    db_session.add(activity)
    db_session.flush()
    participant = models.ParticipantCode(code="part-history001")
    db_session.add(participant)
    db_session.flush()
    session = models.Session(activity_configuration_id=activity.id, participant_code=participant.code)
    db_session.add(session)
    db_session.flush()
    get_or_create(db_session, session.id, activity_ref=activity.id)
    db_session.flush()
    return session


@pytest.mark.integration
def test_history_includes_applied_and_rejected_in_order(db_session, seeded_session):
    apply_patch(
        db_session,
        session_id=seeded_session.id,
        base_version=0,
        proposed_by_agent_id="agent-a",
        element_type="observation",
        payload={"current_input": "uno"},
    )
    apply_patch(
        db_session,
        session_id=seeded_session.id,
        base_version=0,
        proposed_by_agent_id="agent-b",
        element_type="observation",
        payload={"current_input": "conflicto"},
    )
    apply_patch(
        db_session,
        session_id=seeded_session.id,
        base_version=1,
        proposed_by_agent_id="agent-a",
        element_type="decision",
        payload={"current_input": "dos"},
    )

    history = history_for_session(db_session, seeded_session.id)
    assert len(history) == 3
    assert [h.applied for h in history] == [True, False, True]
    assert [h.base_version for h in history] == [0, 0, 1]
    assert history == sorted(history, key=lambda p: p.created_at)


@pytest.mark.integration
def test_history_reconstructs_final_state_from_applied_patches_only(db_session, seeded_session):
    apply_patch(
        db_session,
        session_id=seeded_session.id,
        base_version=0,
        proposed_by_agent_id="agent-a",
        element_type="observation",
        payload={"current_input": "uno"},
    )
    apply_patch(
        db_session,
        session_id=seeded_session.id,
        base_version=0,
        proposed_by_agent_id="agent-b",
        element_type="observation",
        payload={"current_input": "ignorado"},
    )

    history = history_for_session(db_session, seeded_session.id)
    reconstructed_input = None
    for patch in history:
        if patch.applied:
            reconstructed_input = patch.payload.get("current_input", reconstructed_input)

    state = db_session.get(models.CognitiveState, seeded_session.id)
    assert reconstructed_input == state.current_input == "uno"
