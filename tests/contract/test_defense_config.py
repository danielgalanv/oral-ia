from oralia.infrastructure.db import models


def test_configure_defense_activity_and_immutability(app_client, seeded_activity) -> None:
    response = app_client.post(
        f"/api/v1/tecnica/activities/{seeded_activity}/defense-config",
        json={"initial_questions": ["Explica el diseño."], "topics": ["diseño"]},
    )
    assert response.status_code == 201
    assert response.json()["initial_questions"] == ["Explica el diseño."]
    updated = app_client.post(
        f"/api/v1/tecnica/activities/{seeded_activity}/defense-config",
        json={"initial_questions": ["Otra pregunta."]},
    )
    assert updated.status_code == 200
    assert updated.json()["id"] == response.json()["id"]

    Session = app_client.__db_sessionmaker__
    with Session() as db:
        activity = db.get(models.ActivityConfiguration, seeded_activity)
        activity.immutable_since = activity.created_at
        db.commit()
    blocked = app_client.post(
        f"/api/v1/tecnica/activities/{seeded_activity}/defense-config",
        json={"initial_questions": ["Otra"]},
    )
    assert blocked.status_code == 409


def test_defense_config_requires_question_or_material(app_client, seeded_activity) -> None:
    response = app_client.post(
        f"/api/v1/tecnica/activities/{seeded_activity}/defense-config",
        json={"initial_questions": []},
    )
    assert response.status_code == 422
