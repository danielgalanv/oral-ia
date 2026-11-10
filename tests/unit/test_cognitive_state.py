"""Unit coverage for FR-009's minimum CognitiveState field set and StatePatch's
element-type tagging/validation rules — independent of the HTTP layer."""

import pytest

from oralia.domain.cognitive_state.cognitive_state import (
    ELEMENT_TYPES,
    MINIMUM_FIELDS,
    get_or_create,
    to_snapshot,
)
from oralia.domain.cognitive_state.state_patch import InvalidElementType, apply_patch
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
        **minimal_output_policy_columns(recipients=("part-unit001",)),
    )
    db_session.add(activity)
    db_session.flush()
    participant = models.ParticipantCode(code="part-unit001")
    db_session.add(participant)
    db_session.flush()
    session = models.Session(activity_configuration_id=activity.id, participant_code=participant.code)
    db_session.add(session)
    db_session.flush()
    return session


def test_minimum_fields_matches_fr009_list():
    # FR-009's 17-field minimum, verbatim (spec.md).
    expected = {
        "mode",
        "objective",
        "activity_ref",
        "permitted_materials",
        "current_input",
        "participant_response",
        "concepts_addressed",
        "concepts_pending",
        "intent_hypotheses",
        "retrieved_info",
        "open_questions",
        "summarized_history",
        "remaining_time",
        "turn_number",
        "incidents",
        "confidence",
        "next_action_proposed",
    }
    assert set(MINIMUM_FIELDS) == expected


def test_element_types_matches_fr009_list():
    expected = {
        "instruction",
        "observation",
        "participant_statement",
        "retrieved_info",
        "hypothesis",
        "inference",
        "decision",
        "check_result",
        "configuration",
    }
    assert set(ELEMENT_TYPES) == expected


def test_get_or_create_snapshot_exposes_every_minimum_field(db_session, seeded_session):
    row = get_or_create(db_session, seeded_session.id, activity_ref="act-1")
    db_session.flush()
    snapshot = to_snapshot(row)
    snapshot_fields = snapshot.model_dump().keys()
    assert set(MINIMUM_FIELDS).issubset(snapshot_fields)


def test_apply_patch_rejects_unknown_element_type(db_session, seeded_session):
    get_or_create(db_session, seeded_session.id, activity_ref="act-1")
    db_session.flush()
    with pytest.raises(InvalidElementType):
        apply_patch(
            db_session,
            session_id=seeded_session.id,
            base_version=0,
            proposed_by_agent_id="agent-a",
            element_type="not-a-real-type",
            payload={"current_input": "x"},
        )


def test_apply_patch_rejects_unknown_field_in_payload(db_session, seeded_session):
    get_or_create(db_session, seeded_session.id, activity_ref="act-1")
    db_session.flush()
    with pytest.raises(ValueError, match="unknown CognitiveState fields"):
        apply_patch(
            db_session,
            session_id=seeded_session.id,
            base_version=0,
            proposed_by_agent_id="agent-a",
            element_type="observation",
            payload={"not_a_real_field": "x"},
        )


def test_get_or_create_is_idempotent(db_session, seeded_session):
    row1 = get_or_create(db_session, seeded_session.id, activity_ref="act-1")
    db_session.flush()
    row2 = get_or_create(db_session, seeded_session.id, activity_ref="act-1")
    assert row1.session_id == row2.session_id
    assert row1.version == row2.version == 0
