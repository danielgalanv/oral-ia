"""Unit-level edge cases for FR-001/FR-002 not already covered by
tests/integration/test_activity_immutability.py (versioning chains, defaults)."""

import pytest
from pydantic import ValidationError

from oralia.application.commands.create_activity import (
    ActivityConfigurationInput,
    GeneralKnowledgePolicyMismatch,
    create_activity,
)
from oralia.infrastructure.db import models
from tests.t090_policy_helpers import minimal_output_policy


@pytest.fixture()
def course_and_policy(db_session):
    course = models.Course(name="C", subject_code="C1")
    policy = models.RetentionPolicy(content_scope="session", access_scope="profesor", purge_rule="manual")
    db_session.add_all([course, policy])
    db_session.flush()
    return course, policy


def _input(course_id: str, policy_id: str, name: str) -> ActivityConfigurationInput:
    return ActivityConfigurationInput(
        course_id=course_id,
        name=name,
        subject="s",
        objective="o",
        mode="texto",
        language="es",
        max_turns=5,
        max_duration_seconds=100,
        retention_policy_id=policy_id,
        output_authorization_policy=minimal_output_policy(),
    )


def test_general_knowledge_allowed_defaults_false(db_session, course_and_policy):
    course, policy = course_and_policy
    activity = create_activity(db_session, _input(course.id, policy.id, "A"))
    assert activity.general_knowledge_allowed is False


def test_first_version_of_a_new_family_is_one(db_session, course_and_policy):
    course, policy = course_and_policy
    activity = create_activity(db_session, _input(course.id, policy.id, "A"))
    assert activity.version == 1
    assert activity.family_id is not None


def test_three_draft_edits_increment_version_each_time(db_session, course_and_policy):
    course, policy = course_and_policy
    v1 = create_activity(db_session, _input(course.id, policy.id, "A v1"))
    v2 = create_activity(db_session, _input(course.id, policy.id, "A v2"), family_id=v1.family_id)
    v3 = create_activity(db_session, _input(course.id, policy.id, "A v3"), family_id=v1.family_id)

    assert [v1.version, v2.version, v3.version] == [1, 2, 3]
    assert v1.family_id == v2.family_id == v3.family_id


def test_editing_with_unknown_family_id_starts_a_fresh_family_at_version_one(db_session, course_and_policy):
    course, policy = course_and_policy
    activity = create_activity(
        db_session, _input(course.id, policy.id, "A"), family_id="00000000-0000-0000-0000-000000000000"
    )
    # No prior version exists under that family_id, so it behaves like a new family.
    assert activity.version == 1


def test_new_configuration_requires_valid_output_policy(course_and_policy):
    course, policy = course_and_policy
    valid = _input(course.id, policy.id, "A").model_dump(mode="json")
    valid.pop("output_authorization_policy")
    with pytest.raises(ValidationError):
        ActivityConfigurationInput.model_validate(valid)

    valid["output_authorization_policy"] = {
        "schema_version": 999,
        "policy_id": "invalid",
        "policy_version": 1,
        "allowed_recipients": [],
        "allowed_disclosures": [],
        "allowed_scopes": {"topics": [], "purposes": [], "actions": []},
        "general_knowledge_allowed": False,
        "allowed_templates": [],
        "allowed_operational_messages": [],
    }
    with pytest.raises(ValidationError):
        ActivityConfigurationInput.model_validate(valid)


def test_general_knowledge_permission_must_match_policy(db_session, course_and_policy):
    course, policy = course_and_policy
    data = _input(course.id, policy.id, "A").model_copy(update={"general_knowledge_allowed": True})
    with pytest.raises(GeneralKnowledgePolicyMismatch):
        create_activity(db_session, data)
