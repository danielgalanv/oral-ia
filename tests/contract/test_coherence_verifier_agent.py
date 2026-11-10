"""Contract test for CoherenceVerifierAgent (approved/block/reformulate, umbrales
propios)."""

from __future__ import annotations

import uuid

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.coherence_verifier_agent import CoherenceVerifierAgent


def _request(
    proposal_text: str,
    prior_statements: list[str] | None = None,
    active_sources: list[str] | None = None,
    concepts_addressed: list[str] | None = None,
    turn_number: int = 1,
    max_turns: int = 10,
):
    return AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        input={
            "proposal_text": proposal_text,
            "prior_statements": prior_statements or [],
            "active_sources": active_sources or [],
            "concepts_addressed": concepts_addressed or [],
            "turn_number": turn_number,
            "max_turns": max_turns,
        },
    )


@pytest.mark.contract
async def test_output_shape_is_complete():
    agent = CoherenceVerifierAgent()
    result = await agent.execute(_request("La fotosíntesis convierte luz en energía."), CancellationToken())
    assert result.status == "ok"
    assert result.output["verdict"] in ("approved", "block", "reformulate")
    assert "incident_types" in result.output
    assert "recovery_action" in result.output


@pytest.mark.contract
async def test_no_prior_context_is_approved():
    agent = CoherenceVerifierAgent()
    result = await agent.execute(_request("La fotosíntesis convierte luz en energía."), CancellationToken())
    assert result.output["verdict"] == "approved"
    assert result.output["incident_types"] == []
    assert result.output["recovery_action"] is None


@pytest.mark.contract
async def test_contradiction_against_prior_statement_is_blocked():
    agent = CoherenceVerifierAgent()
    result = await agent.execute(
        _request(
            "La fotosíntesis no convierte luz en energía química.",
            prior_statements=["La fotosíntesis convierte luz en energía química."],
        ),
        CancellationToken(),
    )
    assert result.output["verdict"] == "block"
    assert "contradiccion" in result.output["incident_types"]
    assert result.output["recovery_action"] is not None


@pytest.mark.contract
async def test_repetition_against_immediately_prior_turn_is_reformulated():
    agent = CoherenceVerifierAgent()
    text = "La fotosíntesis convierte luz solar en energía química mediante clorofila."
    result = await agent.execute(_request(text, prior_statements=[text]), CancellationToken())
    assert result.output["verdict"] == "reformulate"
    assert "repeticion" in result.output["incident_types"]


@pytest.mark.parametrize("separator", [". ", "\n"])
async def test_unrelated_metadata_negation_is_not_a_material_contradiction(separator):
    result = await CoherenceVerifierAgent().execute(
        _request(
            "El agua hierve a 100 grados. Al calentarse pasa a vapor.",
            active_sources=[
                "Tema: cambios de estado del agua" + separator + "No contiene datos de personas.",
                "El agua hierve a 100 grados. Al calentarse pasa a vapor.",
            ],
        ),
        CancellationToken(),
    )
    assert result.output["verdict"] == "approved"


@pytest.mark.parametrize("context", ["prior_statements", "active_sources"])
async def test_sentence_scoping_still_blocks_explicit_conflict_even_with_negated_metadata(context):
    result = await CoherenceVerifierAgent().execute(
        _request(
            "El agua hierve a 100 grados. No contiene datos de personas.",
            **{context: ["El agua no hierve a 100 grados. No contiene datos de personas."]},
        ),
        CancellationToken(),
    )
    assert result.output["verdict"] == "block"
    assert "contradiccion" in result.output["incident_types"]


async def test_literal_material_does_not_exempt_other_conflicting_source():
    text = "El agua hierve a 100 grados."
    result = await CoherenceVerifierAgent().execute(
        _request(text, active_sources=[text, "El agua no hierve a 100 grados."]), CancellationToken()
    )
    assert result.output["verdict"] == "block"
