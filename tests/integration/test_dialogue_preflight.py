"""Rejected entry must not create a participant, session, governance or active lock."""

import pytest

from oralia.application.commands.start_session import StartSessionInput, start_session
from oralia.infrastructure.db import models


@pytest.mark.parametrize("failure", ["recipient", "policy"])
def test_preflight_rejects_before_session_creation(app_client, seeded_activity, failure):
    with app_client.__db_sessionmaker__() as db:
        if failure == "policy":
            activity = db.get(models.ActivityConfiguration, seeded_activity)
            activity.output_authorization_policy_json = None
            activity.output_authorization_policy_sha256 = None
            db.flush()
        counts = {
            entity: db.query(entity).count()
            for entity in [models.Session, models.ParticipantCode, models.ActivityGovernance]
        }
        with pytest.raises(ValueError, match="recipient_not_allowed|activity_unavailable"):
            start_session(
                db,
                StartSessionInput(
                    participant_code="forbidden" if failure == "recipient" else "participant",
                    activity_configuration_id=seeded_activity,
                ),
            )
        db.flush()
        assert all(db.query(entity).count() == count for entity, count in counts.items())
        assert db.query(models.Session).filter(models.Session.active_lock_token.isnot(None)).count() == 0


def test_public_preflight_returns_closed_code_and_actionable_message(app_client, seeded_activity):
    response = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "not-allowed", "activity_configuration_id": seeded_activity},
    )
    assert response.status_code == 409
    detail = response.json()["detail"]
    assert detail["code"] == "recipient_not_allowed"
    assert "actividad" in detail["message"]
    with app_client.__db_sessionmaker__() as db:
        assert db.query(models.Session).count() == 0
