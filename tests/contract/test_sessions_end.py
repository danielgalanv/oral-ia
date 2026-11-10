"""Contract test for POST /api/v1/sessions/{id}/end — FR-012, FR-012b."""

import pytest

from tests.t090_policy_helpers import configure_minimal_output_policy


@pytest.mark.contract
def test_end_session_returns_confirmation_only_no_technical_detail(app_client, seeded_activity):
    configure_minimal_output_policy(app_client, seeded_activity, recipients=("part-end001",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-end001", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]
    app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "hola"})

    r = app_client.post(f"/api/v1/sessions/{sid}/end")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "closed_voluntary"
    assert "confirmation_message" in body
    # FR-012b: no grade, no technical/agent detail leaks into the participant response.
    assert "turn_count" not in body
    assert "agents" not in body
