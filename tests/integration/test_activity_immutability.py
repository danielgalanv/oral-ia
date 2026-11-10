"""FR-002: an ActivityConfiguration becomes immutable once a Session uses it."""

import pytest

from oralia.application.commands.create_activity import (
    ActivityAlreadyImmutable,
    ActivityConfigurationInput,
    create_activity,
    mark_immutable_if_needed,
)
from oralia.infrastructure.db import models
from tests.t090_policy_helpers import minimal_output_policy


@pytest.mark.integration
def test_activity_immutable_after_first_session_use(db_session):
    course = models.Course(name="C", subject_code="C1")
    policy = models.RetentionPolicy(content_scope="session", access_scope="profesor", purge_rule="manual")
    db_session.add_all([course, policy])
    db_session.flush()

    activity = create_activity(
        db_session,
        ActivityConfigurationInput(
            course_id=course.id,
            name="A",
            subject="s",
            objective="o",
            mode="texto",
            language="es",
            max_turns=5,
            max_duration_seconds=100,
            retention_policy_id=policy.id,
            output_authorization_policy=minimal_output_policy(),
        ),
    )
    assert activity.immutable_since is None

    mark_immutable_if_needed(db_session, activity)
    assert activity.immutable_since is not None

    with pytest.raises(ActivityAlreadyImmutable):
        create_activity(
            db_session,
            ActivityConfigurationInput(
                course_id=course.id,
                name="A edited",
                subject="s",
                objective="o",
                mode="texto",
                language="es",
                max_turns=5,
                max_duration_seconds=100,
                retention_policy_id=policy.id,
                output_authorization_policy=minimal_output_policy(),
            ),
            family_id=activity.family_id,
        )


@pytest.mark.integration
def test_new_version_allowed_while_draft(db_session):
    course = models.Course(name="C", subject_code="C1")
    policy = models.RetentionPolicy(content_scope="session", access_scope="profesor", purge_rule="manual")
    db_session.add_all([course, policy])
    db_session.flush()

    v1 = create_activity(
        db_session,
        ActivityConfigurationInput(
            course_id=course.id,
            name="A v1",
            subject="s",
            objective="o",
            mode="texto",
            language="es",
            max_turns=5,
            max_duration_seconds=100,
            retention_policy_id=policy.id,
            output_authorization_policy=minimal_output_policy(),
        ),
    )
    v2 = create_activity(
        db_session,
        ActivityConfigurationInput(
            course_id=course.id,
            name="A v2",
            subject="s",
            objective="o",
            mode="texto",
            language="es",
            max_turns=5,
            max_duration_seconds=100,
            retention_policy_id=policy.id,
            output_authorization_policy=minimal_output_policy(),
        ),
        family_id=v1.family_id,
    )
    assert v2.version == 2
    assert v2.family_id == v1.family_id
