from datetime import timedelta

import pytest

from oralia.application.commands.end_defense_session import end_defense_session
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from tests.integration.test_defense_retention_copies import _seed_copies


@pytest.mark.parametrize("scope", [[], ["transcript"], ["summary"], ["transcript", "summary"]])
def test_teacher_review_filters_scopes_and_has_no_owner_override(app_client, scope):
    factory = app_client.__db_sessionmaker__
    with factory() as db:
        sid, cfgid, marker = _seed_copies(db)
    # Teacher credentials alone do not grant participant operational access.
    assert app_client.get(f"/api/v1/defense-sessions/{sid}/defense-transcript").status_code == 403
    technical = app_client.get(f"/api/v1/sessions/{sid}")
    assert technical.status_code == 200 and marker not in technical.text
    with factory() as db:
        end_defense_session(
            db,
            db.get(models.Session, sid),
            db.get(models.DefenseActivityConfig, cfgid),
            retain=bool(scope),
            scope=scope,
        )
        db.commit()
    result = app_client.get(f"/api/v1/governance/sessions/{sid}")
    assert result.status_code == (200 if scope else 404)
    assert result.headers["cache-control"] == "no-store"
    if scope:
        body = result.json()
        assert bool(body["turns"]) == ("transcript" in scope)
        assert bool(body["summary"]) == ("summary" in scope)
        with factory() as db:
            db.get(models.Session, sid).ended_at = utcnow() - timedelta(days=2)
            db.commit()
        assert app_client.get(f"/api/v1/governance/sessions/{sid}").status_code == 404


def test_secret_validation_errors_and_unknown_fields_do_not_echo_credentials(monkeypatch):
    from fastapi.testclient import TestClient

    from oralia.interfaces.api.app import create_app

    secret = "fictional-secret-005" * 80
    monkeypatch.setenv("ORALIA_ADMIN_SECRET", "fictional-installation-secret-005")
    with TestClient(create_app()) as client:
        response = client.post("/api/v1/auth/login", json={"secret": secret})
        assert response.status_code == 422
        assert secret not in response.text


def test_owner_only_retention_never_grants_teacher_review_or_export(app_client):
    from tests.access_helpers import own_session

    with app_client.__db_sessionmaker__() as db:
        sid, cfgid, marker = _seed_copies(db)
        session = db.get(models.Session, sid)
        activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
        policy = db.get(models.RetentionPolicy, activity.retention_policy_id)
        policy.access_scope = "participant_only"
        end_defense_session(
            db, session, db.get(models.DefenseActivityConfig, cfgid), retain=True, scope=["transcript"]
        )
        db.commit()
    assert app_client.get(f"/api/v1/governance/sessions/{sid}").status_code == 404
    assert sid not in app_client.get("/api/v1/governance/sessions").text
    assert marker not in app_client.get(f"/api/v1/sessions/{sid}").text
    assert (
        app_client.post(
            "/api/v1/governance/exports",
            json={"session_ids": [sid], "include_free_text": True, "reviewed_free_text": True},
        ).status_code
        == 409
    )
    own_session(app_client, sid)
    assert marker in app_client.get(f"/api/v1/defense-sessions/{sid}/defense-transcript").text


def test_retention_content_scope_cannot_be_expanded_by_consent(app_client):
    from tests.access_helpers import own_session

    with app_client.__db_sessionmaker__() as db:
        sid, _, _ = _seed_copies(db)
        activity = db.get(models.ActivityConfiguration, db.get(models.Session, sid).activity_configuration_id)
        db.get(models.RetentionPolicy, activity.retention_policy_id).content_scope = "summary"
        db.commit()
    own_session(app_client, sid)
    notice = app_client.get(f"/api/v1/sessions/{sid}/privacy").json()
    assert notice["allowed_scopes"] == ["summary"]
    refused = app_client.post(
        f"/api/v1/defense-sessions/{sid}/defense-end", json={"retain": True, "scope": ["transcript"]}
    )
    assert refused.status_code == 422
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.Session, sid).status == "active"
        assert db.query(models.ConsentRecord).count() == 0
    allowed = app_client.post(
        f"/api/v1/defense-sessions/{sid}/defense-end", json={"retain": True, "scope": ["summary"]}
    )
    assert allowed.status_code == 200
