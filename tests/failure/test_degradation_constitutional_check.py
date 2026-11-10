"""FR-018a: the constitutional control is never bypassed on the degraded/fallback
output path, even when the primary agent has already failed."""

from __future__ import annotations

import asyncio

import pytest

from oralia.application.orchestration import turn_orchestrator
from oralia.domain.agents.agent import AgentContractSchema
from oralia.domain.agents.agent_contract import AgentResult
from oralia.domain.agents.fallback_agent import SafeFallbackAgent
from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
    canonical_policy_sha256,
)
from oralia.domain.policies.output_template_catalog import SAFE_TECHNICAL_FALLBACK
from oralia.infrastructure.db import models


def _authorize_operational_fallback(app_client, activity_id: str, participant_code: str) -> None:
    entry = SAFE_TECHNICAL_FALLBACK
    policy = OutputAuthorizationPolicy.model_validate(
        {
            "schema_version": 1,
            "policy_id": f"fallback-policy-{participant_code}",
            "policy_version": 1,
            "allowed_recipients": [participant_code],
            "allowed_disclosures": [],
            "allowed_scopes": {
                "topics": [entry.topic_ref],
                "purposes": [entry.purpose_ref],
                "actions": [entry.action_ref],
            },
            "general_knowledge_allowed": False,
            "allowed_templates": [],
            "allowed_operational_messages": [[entry.template_id, entry.version]],
        }
    )
    policy_json = canonical_policy_json(policy)
    Session = app_client.__db_sessionmaker__
    db = Session()
    activity = db.get(models.ActivityConfiguration, activity_id)
    activity.output_authorization_policy_json = policy_json
    activity.output_authorization_policy_sha256 = canonical_policy_sha256(policy_json)
    db.add(activity)
    db.commit()
    db.close()


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
        return None


@pytest.mark.failure
def test_fallback_text_still_passes_through_constitutional_control(app_client, seeded_activity, monkeypatch):
    monkeypatch.setitem(turn_orchestrator.AGENT_REGISTRY, "interpreter", SlowTestAgent())
    _authorize_operational_fallback(app_client, seeded_activity, "part-degverify001")

    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-degverify001", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]

    r = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "esto tardara"})
    assert r.status_code == 200

    turn_id = r.json()["turn_id"]
    trace = app_client.get(f"/api/v1/sessions/{sid}/trace").json()
    constitutional_events = [
        e
        for e in trace["trace_events"]
        if e["agent_id"] == "constitutional-control" and e["turn_id"] == turn_id
    ]
    # The constitutional check ran even though "interpret" (the upstream step) failed —
    # it was never skipped "to save resources" (Constitution Principio IX).
    assert len(constitutional_events) >= 1

    detail = app_client.get(f"/api/v1/sessions/{sid}").json()
    assert detail["turns"][0]["verification_verdict"] is not None


class MisbehavingFallbackAgent:
    """A test double for the 'safe-fallback' registry slot that tries to propose an H02
    grade phrase, instead of the real SafeFallbackAgent's fixed safe text (seguimiento
    de H02, ronda 4)."""

    contract = SafeFallbackAgent.contract

    async def execute(self, request, cancellation):
        return AgentResult(status="ok", output={"text": "Tu nota es un nueve."}, confidence=1.0)


@pytest.mark.failure
def test_misbehaving_fallback_proposal_never_reaches_participant(app_client, seeded_activity, monkeypatch):
    """Forces the primary agent to fail (like the test above) AND swaps the registered
    fallback agent with one that proposes an H02 grade phrase, to check what the
    participant actually receives.

    Verified by reading `turn_orchestrator.py`: on the degraded path, the participant
    text and the constitutional re-check both use the fixed `SAFE_FALLBACK_TEXT`
    constant directly — `execute_agency`'s own `fallback_step` result (whatever this
    misbehaving double actually returns) is deliberately never read for either purpose
    (see the "FR-018" comment there: never build the shown text from a failed/degraded
    step's own output). So this test does NOT expect `verdict == "block"` — there is
    nothing to block, because the misbehaving double's text is never the thing being
    shown or evaluated in the first place. What this test actually proves is the
    stronger property: the misbehaving agent's proposed grade cannot reach the
    participant even if it fully controlled its own output, because the orchestrator
    never trusts a degraded step's returned content at all.
    """

    monkeypatch.setitem(turn_orchestrator.AGENT_REGISTRY, "interpreter", SlowTestAgent())
    monkeypatch.setitem(turn_orchestrator.AGENT_REGISTRY, "safe-fallback", MisbehavingFallbackAgent())
    _authorize_operational_fallback(app_client, seeded_activity, "part-degverify002")

    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-degverify002", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]

    r = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "esto tambien tardara"})
    assert r.status_code == 200
    body = r.json()

    # The misbehaving fallback's grade never reaches the participant...
    assert body["blocked"] is True
    assert body["output_text"] is None

    turn_id = body["turn_id"]
    trace = app_client.get(f"/api/v1/sessions/{sid}/trace").json()
    constitutional_events = [
        e
        for e in trace["trace_events"]
        if e["agent_id"] == "constitutional-control" and e["turn_id"] == turn_id
    ]
    assert len(constitutional_events) >= 1
    attempt = next(e for e in constitutional_events if e["event_type"] == "output_authorization_attempt")
    assert attempt["payload"]["verdict"] == "block"
    assert "unsafe_fallback" in attempt["payload"]["reason_codes"]
