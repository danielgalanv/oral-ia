"""Contract test for GET /api/v1/sessions/{id} — contracts/api-tecnica.md."""

import pytest

from tests.t090_policy_helpers import configure_minimal_output_policy, configure_test_recipients


@pytest.mark.contract
def test_get_active_session_detail_without_interrupting_it(app_client, seeded_activity):
    configure_minimal_output_policy(app_client, seeded_activity, recipients=("part-detail001",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-detail001", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]
    app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "hola"})

    detail = app_client.get(f"/api/v1/sessions/{sid}")
    assert detail.status_code == 200
    body = detail.json()
    assert body["session"]["status"] == "active"
    assert body["technical_summary"] is None  # not generated until closed (FR-012b)
    assert len(body["turns"]) == 1

    # Inspecting it did not interrupt the session — it's still usable.
    r2 = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "sigo aqui"})
    assert r2.status_code == 200


@pytest.mark.contract
def test_get_closed_session_includes_technical_summary(app_client, seeded_activity):
    configure_test_recipients(app_client, seeded_activity, recipients=("part-detail002",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-detail002", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]
    app_client.post(f"/api/v1/sessions/{sid}/end")

    detail = app_client.get(f"/api/v1/sessions/{sid}").json()
    assert detail["session"]["status"] == "closed_voluntary"
    assert detail["technical_summary"] is not None


@pytest.mark.contract
def test_get_unknown_session_returns_404(app_client):
    r = app_client.get("/api/v1/sessions/does-not-exist")
    assert r.status_code == 404
