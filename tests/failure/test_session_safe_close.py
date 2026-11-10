"""US4: unsafe degradation closes once and preserves the safe terminal state."""

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
        return None


@pytest.fixture()
def slow_interpreter(monkeypatch):
    monkeypatch.setitem(turn_orchestrator.AGENT_REGISTRY, "interpreter", SlowTestAgent())


@pytest.mark.failure
def test_session_rejects_another_turn_after_unsafe_degradation(
    app_client, seeded_activity, monkeypatch, slow_interpreter
):
    configure_minimal_output_policy(app_client, seeded_activity, recipients=("part-safe001",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-safe001", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]

    degraded = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "esto falla"})
    assert degraded.status_code == 200

    # Restoring the agent cannot reopen a session already closed by the safety boundary.
    from oralia.domain.agents.interpreter_agent import DeterministicInterpreter

    monkeypatch.setitem(turn_orchestrator.AGENT_REGISTRY, "interpreter", DeterministicInterpreter())

    healthy = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "ahora funciona"})
    assert healthy.status_code == 404

    db = app_client.__db_sessionmaker__()
    session = db.get(models.Session, sid)
    assert session.status == "closed_error_safe"
    db.close()


@pytest.mark.failure
def test_session_can_still_be_closed_safely_after_degraded_turn(
    app_client, seeded_activity, slow_interpreter
):
    configure_minimal_output_policy(app_client, seeded_activity, recipients=("part-safe002",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-safe002", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]
    app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "esto falla"})

    r = app_client.post(f"/api/v1/sessions/{sid}/end")
    assert r.status_code == 200
    assert r.json()["status"] == "closed_error_safe"
