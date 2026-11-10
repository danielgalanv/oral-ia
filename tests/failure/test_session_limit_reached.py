"""FR-011a: session auto-closes and still produces a technical summary when the
turn/duration limit is reached, even without a voluntary end from the participant."""

import pytest

from oralia.infrastructure.db import models
from tests.t090_policy_helpers import configure_test_recipients, minimal_output_policy_columns


@pytest.mark.failure
def test_session_auto_closes_at_turn_limit(app_client):
    Session = app_client.__db_sessionmaker__
    db = Session()
    course = models.Course(name="C", subject_code="C1")
    policy = models.RetentionPolicy(content_scope="session", access_scope="profesor", purge_rule="manual")
    db.add_all([course, policy])
    db.flush()
    activity = models.ActivityConfiguration(
        course_id=course.id,
        name="Actividad con limite bajo",
        subject="Demo",
        objective="probar limite de turnos",
        mode="texto",
        language="es",
        max_turns=2,
        max_duration_seconds=3600,
        retention_policy_id=policy.id,
        **minimal_output_policy_columns(recipients=("part-limit001",)),
    )
    db.add(activity)
    db.commit()
    activity_id = activity.id
    db.close()

    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-limit001", "activity_configuration_id": activity_id},
    )
    sid = start.json()["session_id"]

    r1 = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "uno"})
    assert r1.status_code == 200

    r2 = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "dos"})
    assert r2.status_code == 200

    detail = app_client.get(f"/api/v1/sessions/{sid}").json()
    assert detail["session"]["status"] == "closed_limit_reached"
    assert detail["technical_summary"] is not None
    assert detail["technical_summary"]["turn_count"] == 2

    r3 = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "tres"})
    assert r3.status_code == 404


@pytest.mark.failure
def test_new_session_allowed_after_limit_reached_close(app_client, seeded_activity):
    Session = app_client.__db_sessionmaker__
    db = Session()
    activity = db.get(models.ActivityConfiguration, seeded_activity)
    activity.max_turns = 1
    db.add(activity)
    db.commit()
    db.close()

    configure_test_recipients(app_client, seeded_activity, recipients=("part-limit002", "part-limit003"))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-limit002", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]
    app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "unico turno permitido"})

    r = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-limit003", "activity_configuration_id": seeded_activity},
    )
    assert r.status_code == 201
