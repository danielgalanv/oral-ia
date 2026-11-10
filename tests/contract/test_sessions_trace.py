"""Contract test for GET /api/v1/sessions/{id}/trace — contracts/api-tecnica.md, FR-016."""

import pytest

from tests.t090_policy_helpers import configure_test_recipients


@pytest.mark.contract
def test_trace_includes_events_and_state_patches(app_client, seeded_activity):
    configure_test_recipients(app_client, seeded_activity, recipients=("part-trace002",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-trace002", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]
    app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "hola"})

    trace = app_client.get(f"/api/v1/sessions/{sid}/trace")
    assert trace.status_code == 200
    body = trace.json()
    assert "trace_events" in body and "state_patches" in body
    assert len(body["trace_events"]) > 0
    assert len(body["state_patches"]) > 0


@pytest.mark.contract
def test_trace_for_unknown_session_is_empty_not_error(app_client):
    r = app_client.get("/api/v1/sessions/does-not-exist/trace")
    assert r.status_code == 200
    assert r.json() == {"trace_events": [], "state_patches": []}
