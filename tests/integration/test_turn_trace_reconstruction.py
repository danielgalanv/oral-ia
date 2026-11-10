"""FR-016: a completed turn's sequence is fully reconstructable from the trace."""

import pytest

from tests.t090_policy_helpers import configure_test_recipients


@pytest.mark.integration
def test_turn_sequence_reconstructable_from_trace(app_client, seeded_activity):
    configure_test_recipients(app_client, seeded_activity, recipients=("part-trace001",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-trace001", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]
    turn = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "reconstruye esto"})
    turn_id = turn.json()["turn_id"]

    trace = app_client.get(f"/api/v1/sessions/{sid}/trace").json()

    agent_events = [e for e in trace["trace_events"] if e["turn_id"] == turn_id]
    agent_ids = {e["agent_id"] for e in agent_events if e["agent_id"]}
    assert {"interpreter", "constitutional-control"}.issubset(agent_ids)

    assert any(p["applied"] for p in trace["state_patches"])

    detail = app_client.get(f"/api/v1/sessions/{sid}").json()
    assert detail["turns"][0]["id"] == turn_id
    assert detail["turns"][0]["dialogue_action"] is not None
    assert detail["turns"][0]["verification_verdict"] is not None
