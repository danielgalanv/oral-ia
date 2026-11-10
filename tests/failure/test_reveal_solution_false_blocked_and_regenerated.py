"""Failure test: `reveals_solution=false` y la pregunta generada revela la solución →
bloqueada → regenerada → reserva determinista si se agotan los intentos (FR-013a)."""

from __future__ import annotations

import pytest

from oralia.domain.agents.agent_contract import AgentResult
from oralia.domain.agents.solution_non_disclosure_verifier_agent import SolutionNonDisclosureVerifierAgent
from oralia.infrastructure.db import models
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material


async def _always_block(self, request, cancellation):
    return AgentResult(
        status="ok",
        output={"verdict": "block", "overlap_score": 0.99},
        confidence=None,
        trace={"verdict": "block"},
    )


@pytest.mark.failure
def test_regeneration_exhausted_falls_back_to_deterministic_adapter(
    app_client, self_study_activity, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr(SolutionNonDisclosureVerifierAgent, "execute", _always_block)

    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["practice_questions"], participant_code="est-nondisc-001"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-nondisc-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    response = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "Ponme una pregunta de práctica"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["output_text"]
    assert body.get("blocked") is not True

    trace = app_client.get(f"/api/v1/sessions/{session_id}/trace").json()
    nd_events = [e for e in trace["trace_events"] if e["event_type"] == "non_disclosure_check"]
    assert len(nd_events) == 2, (
        "bounded regeneration MUST attempt exactly ORALIA_PRACTICE_REGEN_MAX_ATTEMPTS times"
    )
    assert all(e["payload"]["verdict"] == "block" for e in nd_events)

    generation_events = [e for e in trace["trace_events"] if e["event_type"] == "generation_call"]
    assert generation_events
    assert generation_events[-1]["payload"]["adapter"] == "deterministic"
    assert generation_events[-1]["payload"]["fallback_used"] is True

    Session = app_client.__db_sessionmaker__
    db = Session()
    question = (
        db.query(models.PracticeQuestion).filter(models.PracticeQuestion.session_id == session_id).one()
    )
    db.close()
    assert question.generator_used == "deterministic"
    assert question.non_disclosure_attempts == 2
