"""Regression coverage for /speckit-converge Phase 11 findings: F1/T085 (Constitution
VIII, resource_usage captured but never exposed by the query layer) and F3/T087
(FR-007, the degraded-path constitutional re-check produced no InternalMessage)."""

import pytest

from oralia.infrastructure.db import models
from tests.t090_policy_helpers import configure_minimal_output_policy


@pytest.mark.integration
def test_resource_usage_exposed_by_session_detail_and_trace(app_client, seeded_activity):
    configure_minimal_output_policy(app_client, seeded_activity, recipients=("part-conv101",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-conv101", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]
    app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "hola"})

    detail = app_client.get(f"/api/v1/sessions/{sid}").json()
    assert detail["turns"][0]["resource_usage"] is not None
    assert set(detail["turns"][0]["resource_usage"].keys()) == {"cpu_percent", "memory_rss_mb"}

    trace = app_client.get(f"/api/v1/sessions/{sid}/trace").json()
    agent_events = [e for e in trace["trace_events"] if e["event_type"] == "agent_execution"]
    assert len(agent_events) > 0
    for e in agent_events:
        assert e["resource_usage"] is not None


@pytest.mark.integration
def test_degraded_path_constitutional_recheck_produces_internal_message(
    app_client, seeded_activity, monkeypatch
):
    import asyncio

    from oralia.application.orchestration import turn_orchestrator
    from oralia.domain.agents.agent import AgentContractSchema

    class SlowTestAgent:
        contract = AgentContractSchema(
            agent_id="slow-test-agent",
            version="1.0.0",
            purpose="always exceeds its own timeout",
            input_schema_ref="AgentRequest",
            output_schema_ref="AgentResult",
            timeout_ms=20,
        )

        async def execute(self, request, cancellation):
            await asyncio.sleep(1)

    monkeypatch.setitem(turn_orchestrator.AGENT_REGISTRY, "interpreter", SlowTestAgent())

    configure_minimal_output_policy(app_client, seeded_activity, recipients=("part-conv102",))

    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-conv102", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]
    turn = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "esto tardara"})
    turn_id = turn.json()["turn_id"]

    Session = app_client.__db_sessionmaker__
    db = Session()
    messages = (
        db.query(models.InternalMessage)
        .filter(
            models.InternalMessage.turn_id == turn_id,
            models.InternalMessage.receiver_agent_id == "constitutional-control",
        )
        .all()
    )
    db.close()

    assert len(messages) >= 1
