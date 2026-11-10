import pytest

from oralia.application.commands.end_defense_session import end_defense_session
from oralia.infrastructure.db import models
from tests.integration.test_defense_close_transition_outcome import _seed_active_defense


def test_config_cannot_authorize_retention_without_a_finite_period(app_client, seeded_activity):
    response = app_client.post(
        f"/api/v1/tecnica/activities/{seeded_activity}/defense-config",
        json={"initial_questions": ["Explica."], "transcript_retention_authorized": True},
    )
    assert response.status_code == 422


def test_legacy_config_without_finite_retention_fails_before_claiming_close(db_session):
    session_id, config_id = _seed_active_defense(db_session)
    session = db_session.get(models.Session, session_id)
    activity = db_session.get(models.ActivityConfiguration, session.activity_configuration_id)
    db_session.get(models.RetentionPolicy, activity.retention_policy_id).retention_days = None
    with pytest.raises(ValueError, match="finite"):
        end_defense_session(
            db_session,
            session,
            db_session.get(models.DefenseActivityConfig, config_id),
            retain=True,
            scope=["transcript"],
        )
    assert session.status == "active"
    assert db_session.query(models.ConsentRecord).count() == 0
