"""Contract test for GET /api/v1/activities/{id} — contracts/api-participante.md."""

import pytest


@pytest.mark.contract
def test_get_activity_public_view(app_client, seeded_activity):
    r = app_client.get(f"/api/v1/activities/{seeded_activity}")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == seeded_activity
    assert "name" in body and "objective" in body
    # Internal-only fields MUST NOT leak into the public participant view.
    assert "required_agent_ids" not in body
    assert "retention_policy_id" not in body


@pytest.mark.contract
def test_get_unknown_activity_returns_404(app_client):
    r = app_client.get("/api/v1/activities/does-not-exist")
    assert r.status_code == 404
