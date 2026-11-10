"""Contract test for POST /api/v1/sessions/{id}/turns — FR-012, FR-013, FR-008."""

import pytest

from tests.access_helpers import own_session
from tests.t090_policy_helpers import configure_minimal_output_policy, configure_test_recipients


@pytest.mark.contract
def test_submit_turn_returns_dialogue_action_and_state_version(app_client, seeded_activity):
    configure_minimal_output_policy(app_client, seeded_activity, recipients=("part-turn001",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-turn001", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]

    r = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "Hola, tengo una duda"})
    assert r.status_code == 200
    body = r.json()
    assert body["dialogue_action"] in {
        "respond",
        "ask",
        "re_ask",
        "clarify",
        "acknowledge_missing_info",
        "summarize",
        "finish",
    }
    assert body["output_text"]
    assert body["state_version"] >= 1


@pytest.mark.contract
def test_submit_turn_on_unknown_session_returns_404(app_client):
    own_session(app_client, "does-not-exist")
    r = app_client.post("/api/v1/sessions/does-not-exist/turns", json={"text": "hola"})
    assert r.status_code == 404


@pytest.mark.contract
def test_submit_turn_on_closed_session_returns_404(app_client, seeded_activity):
    configure_test_recipients(app_client, seeded_activity, recipients=("part-turn002",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-turn002", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]
    app_client.post(f"/api/v1/sessions/{sid}/end")

    r = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "hola"})
    assert r.status_code == 404
