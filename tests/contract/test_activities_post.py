"""Contract test for POST /api/v1/activities — contracts/api-tecnica.md, FR-001, FR-002."""

from datetime import UTC

import pytest

from oralia.infrastructure.db import models
from tests.t090_policy_helpers import minimal_output_policy


def _seed_course_and_policy(db):
    course = models.Course(name="C", subject_code="C1")
    policy = models.RetentionPolicy(content_scope="session", access_scope="profesor", purge_rule="manual")
    db.add_all([course, policy])
    db.flush()
    db.commit()
    return course, policy


@pytest.mark.contract
def test_create_activity_returns_201_with_version_1(app_client):
    Session = app_client.__db_sessionmaker__
    db = Session()
    course, policy = _seed_course_and_policy(db)
    db.close()

    payload = {
        "course_id": course.id,
        "name": "Actividad 1",
        "subject": "Demo",
        "objective": "probar",
        "mode": "texto",
        "language": "es",
        "max_turns": 10,
        "max_duration_seconds": 600,
        "retention_policy_id": policy.id,
        "output_authorization_policy": minimal_output_policy().model_dump(mode="json"),
    }
    r = app_client.post("/api/v1/activities", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["version"] == 1
    assert body["immutable_since"] is None


@pytest.mark.contract
def test_edit_immutable_activity_returns_409(app_client):
    Session = app_client.__db_sessionmaker__
    db = Session()
    course, policy = _seed_course_and_policy(db)

    payload = {
        "course_id": course.id,
        "name": "Actividad 2",
        "subject": "Demo",
        "objective": "probar",
        "mode": "texto",
        "language": "es",
        "max_turns": 10,
        "max_duration_seconds": 600,
        "retention_policy_id": policy.id,
        "output_authorization_policy": minimal_output_policy().model_dump(mode="json"),
    }
    r = app_client.post("/api/v1/activities", json=payload)
    family_id = r.json()["family_id"]

    activity = db.get(models.ActivityConfiguration, r.json()["id"])
    from datetime import datetime

    activity.immutable_since = datetime.now(UTC)
    db.add(activity)
    db.commit()
    db.close()

    r2 = app_client.post(f"/api/v1/activities?family_id={family_id}", json=payload)
    assert r2.status_code == 409
