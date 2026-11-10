"""US4: an agent raises/errors instead of producing a valid output — the incident is
traced and the last valid CognitiveState version is preserved (FR-018)."""

from __future__ import annotations

import pytest

from oralia.application.orchestration import turn_orchestrator
from oralia.domain.agents.agent import AgentContractSchema
from oralia.infrastructure.db import models
from tests.t090_policy_helpers import configure_test_recipients


class BrokenTestAgent:
    contract = AgentContractSchema(
        agent_id="broken-test-agent",
        version="1.0.0",
        purpose="test double that always raises instead of returning a valid AgentResult",
        input_schema_ref="AgentRequest",
        output_schema_ref="AgentResult",
        timeout_ms=1000,
    )

    async def execute(self, request, cancellation):
        raise RuntimeError("simulated schema-invalid output")


@pytest.fixture()
def broken_interpreter(monkeypatch):
    monkeypatch.setitem(turn_orchestrator.AGENT_REGISTRY, "interpreter", BrokenTestAgent())


@pytest.mark.failure
def test_invalid_output_is_traced_and_state_preserved(app_client, seeded_activity, broken_interpreter):
    configure_test_recipients(app_client, seeded_activity, recipients=("part-invalid001",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-invalid001", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]

    r = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "provoca un error"})
    assert r.status_code == 200

    trace = app_client.get(f"/api/v1/sessions/{sid}/trace").json()
    error_events = [
        e
        for e in trace["trace_events"]
        if e["agent_id"] == "interpreter" and e["payload"]["status"] == "error"
    ]
    assert len(error_events) == 1

    Session = app_client.__db_sessionmaker__
    db = Session()
    state = db.get(models.CognitiveState, sid)
    # The failed agent's (nonexistent) output never reached CognitiveState.
    assert state.current_input == ""
    assert db.get(models.SessionDeletionReceipt, sid).reason == "no_consent"
    assert state.participant_response in (None, "")
    session = db.get(models.Session, sid)
    assert session.status == "closed_error_safe"
    db.close()
