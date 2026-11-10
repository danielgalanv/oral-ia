"""Failure test: fundamentación dice `fundamentada` pero coherencia dice `block` → el
resultado combinado es `block` (tabla de severidad, research.md §5)."""

from __future__ import annotations

import pytest

from oralia.domain.agents.agent_contract import AgentResult
from oralia.domain.agents.coherence_verifier_agent import CoherenceVerifierAgent
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material


async def _always_block(self, request, cancellation):
    return AgentResult(
        status="ok",
        output={
            "verdict": "block",
            "incident_types": ["contradiccion"],
            "recovery_action": "pedir_aclaracion",
        },
        confidence=None,
        trace={"verdict": "block"},
    )


@pytest.mark.failure
def test_coherence_block_overrides_grounding_fundamentada(
    app_client, self_study_activity, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr(CoherenceVerifierAgent, "execute", _always_block)

    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["doubt_resolution"], participant_code="est-severity-001"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-severity-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    response = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        # Grounded directly in the uploaded material — GroundingVerifierAgent (Feature
        # 002, unchanged) MUST classify this "fundamentada" on its own.
        json={"text": "¿Qué contiene el documento de prueba?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body.get("blocked") is True

    trace = app_client.get(f"/api/v1/sessions/{session_id}/trace").json()
    combined_event = next(e for e in trace["trace_events"] if e["event_type"] == "verification_combined")
    assert combined_event["payload"]["grounding_verdict"] == "fundamentada"
    assert combined_event["payload"]["coherence_verdict"] == "block"
    assert combined_event["payload"]["combined_outcome"] == "block"
    assert combined_event["payload"]["severity_source"] == "coherence"
