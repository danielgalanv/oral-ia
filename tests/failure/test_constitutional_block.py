"""US3 Escenario B: a (test-double) agent proposes an academically prohibited output;
the constitutional control blocks it before it reaches the participant (FR-014, FR-015).

This feature's real Interpreter is deterministic and only echoes participant input
(research.md §2) — it has no generation logic capable of producing a grade on its own.
To exercise the blocking path faithfully to User Story 3 ("un agente de prueba propone
una salida..."), we monkeypatch the live interpreter registry entry with a misbehaving
test double, exactly the scenario the story describes.
"""

from __future__ import annotations

import pytest

from oralia.application.orchestration import turn_orchestrator
from oralia.domain.agents.agent_contract import AgentResult
from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
    canonical_policy_sha256,
)
from oralia.domain.policies.output_template_catalog import (
    DEFAULT_OUTPUT_TEMPLATE_CATALOG,
    SAFE_TECHNICAL_FALLBACK,
    OutputTemplateEntry,
)
from oralia.infrastructure.db import models


def _authorize_exact_candidate(
    app_client,
    activity_id: str,
    monkeypatch: pytest.MonkeyPatch,
    *,
    participant_code: str,
    echo: str,
) -> str:
    candidate = turn_orchestrator._response_text_for_intent("respond", echo)
    entry = OutputTemplateEntry.from_text(
        template_id=f"h02-candidate-{participant_code}",
        version=1,
        message_type="normal",
        text=candidate,
        topic_ref="activity",
        purpose_ref="h02_test",
        action_ref="respond",
    )
    policy = OutputAuthorizationPolicy.model_validate(
        {
            "schema_version": 1,
            "policy_id": f"h02-policy-{participant_code}",
            "policy_version": 1,
            "allowed_recipients": [participant_code],
            "allowed_disclosures": [],
            "allowed_scopes": {
                "topics": [entry.topic_ref],
                "purposes": [entry.purpose_ref],
                "actions": [entry.action_ref],
            },
            "general_knowledge_allowed": False,
            "allowed_templates": [[entry.template_id, entry.version]],
            "allowed_operational_messages": [],
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
    catalog = DEFAULT_OUTPUT_TEMPLATE_CATALOG.extended((entry,))
    monkeypatch.setattr(
        turn_orchestrator,
        "_catalog_for_activity",
        lambda _activity: (catalog, entry, SAFE_TECHNICAL_FALLBACK),
    )
    return candidate


class MisbehavingTestAgent:
    """A test agent that always proposes a grade — the forbidden output (Escenario B)."""

    contract = turn_orchestrator.DeterministicInterpreter.contract

    async def execute(self, request, cancellation):
        return AgentResult(status="ok", output={"intent": "respond", "echo": "nota: 9"}, confidence=1.0)


@pytest.fixture()
def misbehaving_interpreter(monkeypatch):
    monkeypatch.setitem(turn_orchestrator.AGENT_REGISTRY, "interpreter", MisbehavingTestAgent())


class _EchoAgent:
    """A test agent that echoes whatever text it's constructed with — used to exercise
    the normal path with a specific H02 phrase (seguimiento de H02, ronda 4), not just
    the pre-H02 "nota: 9" pattern already covered above."""

    contract = turn_orchestrator.DeterministicInterpreter.contract

    def __init__(self, echo: str) -> None:
        self._echo = echo

    async def execute(self, request, cancellation):
        return AgentResult(status="ok", output={"intent": "respond", "echo": self._echo}, confidence=1.0)


@pytest.mark.failure
def test_h02_reinforced_phrase_blocked_in_integration(app_client, seeded_activity, monkeypatch):
    """Extends the existing 'nota: 9' integration case (already blocked before H02) with
    a phrase that only a *reinforced* pattern catches — proves the reinforcement is
    wired into the real turn pipeline, not just exercised via evaluate() directly."""

    echo = "Te otorgo un sobresaliente."
    monkeypatch.setitem(turn_orchestrator.AGENT_REGISTRY, "interpreter", _EchoAgent(echo))
    _authorize_exact_candidate(
        app_client,
        seeded_activity,
        monkeypatch,
        participant_code="part-block003",
        echo=echo,
    )

    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-block003", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]

    r = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "cualquier cosa"})
    assert r.status_code == 200
    body = r.json()
    assert body["blocked"] is True
    assert body["output_text"] is None

    trace = app_client.get(f"/api/v1/sessions/{sid}/trace").json()
    turn_id = body["turn_id"]
    block_events = [
        e
        for e in trace["trace_events"]
        if e["event_type"] == "constitutional_block" and e["turn_id"] == turn_id
    ]
    assert len(block_events) == 1
    assert "assigns_grade" in block_events[0]["payload"]["reasons"]


@pytest.mark.failure
def test_h02_legitimate_phrase_not_blocked_in_integration(app_client, seeded_activity, monkeypatch):
    """A phrase that resembles the H02 patterns (mentions a fraction and an evaluated
    item) but is not a grade — confirms the reinforced rules don't over-block through
    the real turn pipeline either, not only via direct evaluate() calls."""

    echo = "En este ejercicio la probabilidad es 9/10."
    monkeypatch.setitem(
        turn_orchestrator.AGENT_REGISTRY,
        "interpreter",
        _EchoAgent(echo),
    )
    candidate = _authorize_exact_candidate(
        app_client,
        seeded_activity,
        monkeypatch,
        participant_code="part-block004",
        echo=echo,
    )

    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-block004", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]

    r = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "cualquier cosa"})
    assert r.status_code == 200
    body = r.json()
    assert "blocked" not in body  # omitted entirely when not blocked, per the API contract
    assert body["output_text"] == candidate
    assert "9/10" in body["output_text"]


@pytest.mark.failure
def test_blocked_output_never_reaches_participant(
    app_client, seeded_activity, misbehaving_interpreter, monkeypatch
):
    _authorize_exact_candidate(
        app_client,
        seeded_activity,
        monkeypatch,
        participant_code="part-block001",
        echo="nota: 9",
    )
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-block001", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]

    r = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "cualquier cosa"})
    assert r.status_code == 200
    body = r.json()
    assert body["blocked"] is True
    assert body["output_text"] is None


@pytest.mark.failure
def test_block_cause_is_recorded_traceably(app_client, seeded_activity, misbehaving_interpreter, monkeypatch):
    _authorize_exact_candidate(
        app_client,
        seeded_activity,
        monkeypatch,
        participant_code="part-block002",
        echo="nota: 9",
    )
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-block002", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]
    turn = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "cualquier cosa"})
    turn_id = turn.json()["turn_id"]

    trace = app_client.get(f"/api/v1/sessions/{sid}/trace").json()
    block_events = [
        e
        for e in trace["trace_events"]
        if e["event_type"] == "constitutional_block" and e["turn_id"] == turn_id
    ]
    assert len(block_events) == 1
    assert "assigns_grade" in block_events[0]["payload"]["reasons"]

    detail = app_client.get(f"/api/v1/sessions/{sid}").json()
    assert detail["turns"][0]["verification_verdict"] == "block"
