"""Unit test: la comprobación de repetición compara solo contra el turno inmediatamente
anterior, no todo el historial (evita falsos positivos en concept_review, research.md
§5)."""

from __future__ import annotations

import uuid

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.coherence_verifier_agent import CoherenceVerifierAgent


def _request(proposal_text: str, prior_statements: list[str]):
    return AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        input={
            "proposal_text": proposal_text,
            "prior_statements": prior_statements,
            "active_sources": [],
            "concepts_addressed": [],
            "turn_number": 1,
            "max_turns": 10,
        },
    )


@pytest.mark.contract
async def test_only_the_immediately_prior_turn_counts_for_repetition():
    agent = CoherenceVerifierAgent()
    text = "La fotosíntesis convierte luz solar en energía química mediante clorofila."

    # `text` appears earlier in the (simulated) history but NOT as the immediately
    # prior turn — MUST NOT be flagged as repetition (only prior_statements[-1] matters).
    older_repeat_but_not_last = await agent.execute(
        _request(text, prior_statements=[text, "Un turno completamente distinto sobre otro tema."]),
        CancellationToken(),
    )
    assert older_repeat_but_not_last.output["verdict"] == "approved"

    # The SAME text as the immediately prior turn MUST be flagged.
    immediately_prior = await agent.execute(
        _request(text, prior_statements=["Un turno completamente distinto sobre otro tema.", text]),
        CancellationToken(),
    )
    assert immediately_prior.output["verdict"] == "reformulate"
    assert "repeticion" in immediately_prior.output["incident_types"]
