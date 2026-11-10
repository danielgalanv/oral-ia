import pytest

from oralia.application.commands.configure_defense_activity import (
    DefenseActivityConfigInput,
    configure_defense_activity,
)
from oralia.domain.policies.output_authorization_policy import OutputAuthorizationPolicy
from oralia.domain.policies.output_template_catalog import (
    DEFAULT_OUTPUT_TEMPLATE_CATALOG,
    DEFENSE_CLARIFICATION,
    DEFENSE_LIMIT_CLOSE,
    DEFENSE_SUMMARY,
    DEFENSE_VOLUNTARY_CLOSE,
)
from oralia.infrastructure.db import models


def _policy(recipient: str) -> OutputAuthorizationPolicy:
    return OutputAuthorizationPolicy.model_validate(
        {
            "schema_version": 1,
            "policy_id": "defense",
            "policy_version": 1,
            "allowed_recipients": [recipient],
            "allowed_disclosures": [],
            "allowed_scopes": {
                "topics": ["activity"],
                "purposes": ["clarify_response"],
                "actions": ["clarify"],
            },
            "general_knowledge_allowed": False,
            "allowed_templates": [["defense-clarification", 1]],
            "allowed_operational_messages": [],
        }
    )


def test_configure_defense_persists_exact_immutable_policy(db_session) -> None:
    course = models.Course(name="D", subject_code="D")
    retention = models.RetentionPolicy(content_scope="session", access_scope="profesor", purge_rule="manual")
    db_session.add_all([course, retention])
    db_session.flush()
    activity = models.ActivityConfiguration(
        course_id=course.id,
        name="D",
        subject="D",
        objective="D",
        mode="oral_defense",
        language="es",
        max_turns=3,
        max_duration_seconds=60,
        retention_policy_id=retention.id,
    )
    db_session.add(activity)
    db_session.flush()
    configure_defense_activity(
        db_session,
        activity.id,
        DefenseActivityConfigInput(initial_questions=["Explica."], output_authorization_policy=_policy("p")),
    )
    assert activity.output_authorization_policy_json
    assert len(activity.output_authorization_policy_sha256) == 64


def test_catalog_requires_complete_identity_without_version_substitution() -> None:
    resolved = DEFAULT_OUTPUT_TEMPLATE_CATALOG.resolve(
        DEFENSE_CLARIFICATION.template_id,
        DEFENSE_CLARIFICATION.version,
        DEFENSE_CLARIFICATION.sha256,
    )
    assert resolved is DEFENSE_CLARIFICATION
    with pytest.raises(KeyError):
        DEFAULT_OUTPUT_TEMPLATE_CATALOG.resolve(
            DEFENSE_CLARIFICATION.template_id, 2, DEFENSE_CLARIFICATION.sha256
        )


@pytest.mark.parametrize("entry", (DEFENSE_LIMIT_CLOSE, DEFENSE_VOLUNTARY_CLOSE, DEFENSE_SUMMARY))
def test_close_and_summary_candidates_are_exact_catalog_entries(entry) -> None:
    assert DEFAULT_OUTPUT_TEMPLATE_CATALOG.resolve(entry.template_id, entry.version, entry.sha256) is entry
