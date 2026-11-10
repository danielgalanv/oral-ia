"""US4 Escenario C: an agent exceeds its timeout — FR-018 degrades without ever
applying a partial write to CognitiveState."""

from __future__ import annotations

import asyncio

import pytest

from oralia.application.orchestration import turn_orchestrator
from oralia.domain.agents.agent import AgentContractSchema
from oralia.infrastructure.db import models
from tests.t090_policy_helpers import configure_minimal_output_policy


class SlowTestAgent:
    contract = AgentContractSchema(
        agent_id="slow-test-agent",
        version="1.0.0",
        purpose="test double that always exceeds its own timeout",
        input_schema_ref="AgentRequest",
        output_schema_ref="AgentResult",
        timeout_ms=20,
    )

    async def execute(self, request, cancellation):
        await asyncio.sleep(1)
        return None  # never reached


@pytest.fixture()
def slow_interpreter(monkeypatch):
    monkeypatch.setitem(turn_orchestrator.AGENT_REGISTRY, "interpreter", SlowTestAgent())


@pytest.mark.failure
def test_timeout_does_not_leave_partial_state_change(app_client, seeded_activity, slow_interpreter):
    configure_minimal_output_policy(app_client, seeded_activity, recipients=("part-timeout001",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-timeout001", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]

    Session = app_client.__db_sessionmaker__
    db = Session()
    state_before = db.get(models.CognitiveState, sid)
    version_before = state_before.version if state_before else 0
    db.close()

    r = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "esto tardara demasiado"})
    assert r.status_code == 200
    body = r.json()
    assert body["dialogue_action"] == "finish"
    assert body["blocked"] is True
    assert body["output_text"] is None

    db = Session()
    state_after = db.get(models.CognitiveState, sid)
    # A sequence of clean, individually-typed patches (FR-009) — never a torn write
    # echoing the timed-out agent's (nonexistent) output.
    assert state_after.version > version_before
    assert state_after.current_input == ""
    assert db.get(models.SessionDeletionReceipt, sid).reason == "no_consent"
    assert state_after.participant_response in (None, "")
    session = db.get(models.Session, sid)
    assert session.status == "closed_error_safe"
    db.close()


@pytest.mark.failure
def test_timeout_produces_traceable_incident(app_client, seeded_activity, slow_interpreter):
    configure_minimal_output_policy(app_client, seeded_activity, recipients=("part-timeout002",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-timeout002", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]
    app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "lento"})

    trace = app_client.get(f"/api/v1/sessions/{sid}/trace").json()
    interpreter_events = [e for e in trace["trace_events"] if e["agent_id"] == "interpreter"]
    assert any(e["payload"]["status"] == "timeout" for e in interpreter_events)
