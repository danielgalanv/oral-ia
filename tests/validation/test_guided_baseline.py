"""The v2 direct comparator is real, keeps T090/T150 and omits independent agents."""

import pytest

from oralia.application.services import guided_dialogue_service
from oralia.domain.agents.grounding_verifier_agent import GroundingVerifierAgent
from oralia.infrastructure.db import models
from oralia.validation.guided_baseline import run_direct_guided_turn
from tests.dialogue.api_fixture import checked, prepare_guided


@pytest.mark.parametrize("mode", ["self_study", "oral_defense"])
def test_actual_direct_baseline_preserves_gate_and_privacy(app_client, monkeypatch, mode):
    prepared = prepare_guided(app_client, mode=mode)
    sid = prepared["session"]["session_id"]
    monkeypatch.setattr(guided_dialogue_service, "run_guided_turn", run_direct_guided_turn)

    async def forbidden(*args, **kwargs):
        raise AssertionError("direct baseline must not call an independent grounding agent")

    monkeypatch.setattr(GroundingVerifierAgent, "execute", forbidden)
    endpoint = (
        f"/api/v1/sessions/{sid}/study-turns"
        if mode == "self_study"
        else f"/api/v1/defense-sessions/{sid}/defense-turns"
    )
    result = checked(
        app_client.post(
            endpoint, json={"text": "¿A qué temperatura hierve el agua?" if mode == "self_study" else ""}
        )
    )
    assert result["output_text"]
    assert result["dialogue_status"]["architecture"] == "direct_baseline_v2"
    assert result["dialogue_status"]["grounding_verdict"] == "not_executed_baseline"
    with app_client.__db_sessionmaker__() as db:
        turn = db.get(models.Turn, result["turn_id"])
        proposal = db.get(models.GeneratedProposal, turn.generated_proposal_id)
        verification = db.get(models.VerificationResult, turn.verification_result_id)
        assert proposal.content["text"] == result["output_text"]
        assert verification.verdict == "approved" and verification.proposal_id == proposal.id
    end = (
        f"/api/v1/sessions/{sid}/study-end"
        if mode == "self_study"
        else f"/api/v1/defense-sessions/{sid}/defense-end"
    )
    checked(app_client.post(end, json={"retain": False, "scope": []}))
    with app_client.__db_sessionmaker__() as db:
        state = db.get(models.CognitiveState, sid)
        assert state is None or state.dialogue_context is None
        assert db.get(models.Session, sid).active_lock_token is None
