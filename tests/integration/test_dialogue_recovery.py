"""Recovery requires an existing owner grant; teacher closure is explicit and atomic."""

from oralia.infrastructure.db import models


def test_owner_resume_lost_access_teacher_confirmation_and_single_close(app_client, seeded_activity):
    started = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "participant", "activity_configuration_id": seeded_activity},
    )
    assert started.status_code == 201
    sid = started.json()["session_id"]
    owned = app_client.get("/api/v1/auth/owned-session")
    assert owned.status_code == 200 and owned.json()["session"]["session_id"] == sid
    resumed = app_client.get(f"/api/v1/sessions/{sid}/resume")
    assert resumed.status_code == 200 and "access_token" not in resumed.json()
    app_client.cookies.clear()
    assert (
        app_client.get(
            f"/api/v1/sessions/{sid}/resume", params={"participant_code": "participant"}
        ).status_code
        == 401
    )
    assert (
        app_client.post(
            "/api/v1/auth/login", json={"secret": "fictional-installation-secret-005"}
        ).status_code
        == 200
    )
    assert app_client.get("/api/v1/auth/owned-session").json()["session"] is None
    assert app_client.get(f"/api/v1/sessions/{sid}/resume").status_code == 403
    active = app_client.get("/api/v1/governance/active-session")
    assert active.status_code == 200 and "participant_code" not in active.json()
    endpoint = f"/api/v1/governance/sessions/{sid}/close"
    assert (
        app_client.post(endpoint, json={"confirm": False, "reason": "owner_access_lost"}).status_code == 409
    )
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.Session, sid).status == "active"
    closed = app_client.post(endpoint, json={"confirm": True, "reason": "owner_access_lost"})
    assert closed.status_code == 200 and closed.json()["status"] == "closed_teacher_confirmed"
    assert (
        app_client.post(endpoint, json={"confirm": True, "reason": "abandoned"}).json()["transition_won"]
        is False
    )
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.Session, sid).active_lock_token is None
        assert (
            db.query(models.TraceEvent)
            .filter_by(session_id=sid, event_type="teacher_confirmed_close")
            .count()
            == 1
        )
        assert db.query(models.ConsentRecord).filter_by(session_id=sid).count() == 0
