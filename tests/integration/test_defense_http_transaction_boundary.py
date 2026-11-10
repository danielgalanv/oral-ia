import httpx

from oralia.interfaces.api.deps.db import get_db
from tests.t090_policy_helpers import minimal_output_policy


async def test_activity_identifier_is_never_published_before_a_failing_commit(app_client, seeded_activity):
    factory = app_client.__db_sessionmaker__
    with factory() as db:
        from oralia.infrastructure.db import models

        seeded = db.get(models.ActivityConfiguration, seeded_activity)
        course_id, retention_id = seeded.course_id, seeded.retention_policy_id

    def failing_commit():
        db = factory()
        try:
            yield db
            raise RuntimeError("injected commit failure")
        finally:
            db.rollback()
            db.close()

    app_client.app.dependency_overrides[get_db] = failing_commit
    transport = httpx.ASGITransport(app=app_client.app, raise_app_exceptions=False)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://test",
        headers={"Authorization": f"Bearer {app_client.app.state.local_access.issue('teacher')}"},
    ) as client:
        response = await client.post(
            "/api/v1/activities",
            json={
                "course_id": course_id,
                "retention_policy_id": retention_id,
                "name": "Uncommitted",
                "subject": "Demo",
                "objective": "Demo",
                "mode": "oral_defense",
                "language": "es",
                "max_turns": 5,
                "max_duration_seconds": 600,
                "output_authorization_policy": minimal_output_policy().model_dump(mode="json"),
            },
        )
    assert response.status_code == 500
    assert "id" not in response.text
    with factory() as db:
        assert db.query(models.ActivityConfiguration).filter_by(name="Uncommitted").count() == 0
