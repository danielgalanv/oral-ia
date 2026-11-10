"""Integration test: una propuesta que contradice una afirmación previa de la sesión se
bloquea/reformula, CoherenceIncident persistido con combined_verdict_source (FR-024)."""

from __future__ import annotations

import pytest

from oralia.domain.agents.agent_contract import AgentResult
from oralia.domain.agents.coherence_verifier_agent import CoherenceVerifierAgent
from oralia.infrastructure.db import models
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material


async def _always_contradiction(self, request, cancellation):
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


@pytest.mark.integration
def test_contradiction_blocks_and_persists_coherence_incident(
    app_client, self_study_activity, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr(CoherenceVerifierAgent, "execute", _always_contradiction)

    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["doubt_resolution"], participant_code="est-contradict-001"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-contradict-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    response = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Qué contiene el documento de prueba?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body.get("blocked") is True

    Session = app_client.__db_sessionmaker__
    db = Session()
    incidents = (
        db.query(models.CoherenceIncident).filter(models.CoherenceIncident.session_id == session_id).all()
    )
    db.close()
    assert len(incidents) == 1
    assert incidents[0].incident_type == "contradiccion"
    assert incidents[0].combined_verdict_source in ("coherence", "both")
    assert incidents[0].recovery_action == "pedir_aclaracion"
    assert incidents[0].affected_proposal_ref

    trace = app_client.get(f"/api/v1/sessions/{session_id}/trace").json()
    combined_events = [e for e in trace["trace_events"] if e["event_type"] == "verification_combined"]
    assert len(combined_events) == 1
    assert combined_events[0]["payload"]["combined_outcome"] == "block"
