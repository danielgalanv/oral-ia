"""Contract test for GET /api/v1/sessions — contracts/api-tecnica.md, FR-020."""

import pytest

from tests.t090_policy_helpers import configure_test_recipients


@pytest.mark.contract
def test_list_sessions_includes_active_and_closed(app_client, seeded_activity):
    configure_test_recipients(app_client, seeded_activity, recipients=("part-list001", "part-list002"))
    r1 = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-list001", "activity_configuration_id": seeded_activity},
    )
    sid1 = r1.json()["session_id"]
    app_client.post(f"/api/v1/sessions/{sid1}/end")

    r2 = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-list002", "activity_configuration_id": seeded_activity},
    )
    sid2 = r2.json()["session_id"]

    listed = app_client.get("/api/v1/sessions").json()
    ids = {s["id"] for s in listed}
    assert {sid1, sid2}.issubset(ids)


@pytest.mark.contract
def test_list_sessions_filter_by_status(app_client, seeded_activity):
    configure_test_recipients(app_client, seeded_activity, recipients=("part-list003",))
    r1 = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-list003", "activity_configuration_id": seeded_activity},
    )
    sid1 = r1.json()["session_id"]
    app_client.post(f"/api/v1/sessions/{sid1}/end")

    closed = app_client.get("/api/v1/sessions?status=closed_voluntary").json()
    assert any(s["id"] == sid1 for s in closed)
    assert all(s["status"] == "closed_voluntary" for s in closed)
