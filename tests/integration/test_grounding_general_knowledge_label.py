"""US3 integration test: general knowledge used when permitted is labeled distinctly
from grounded content (FR-024, FR-025)."""

from __future__ import annotations

import uuid

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.grounding_verifier_agent import GroundingVerifierAgent


@pytest.mark.integration
async def test_general_knowledge_allowed_changes_verdict_from_no_fundamentada_to_no_verificable():
    request_input = {
        "proposal_text": "Una afirmacion sin ningun respaldo documental disponible.",
        "evidence": [],
    }
    disallowed = await GroundingVerifierAgent().execute(
        AgentRequest(
            session_id=uuid.uuid4(),
            turn_id=uuid.uuid4(),
            input={**request_input, "general_knowledge_allowed": False},
        ),
        CancellationToken(),
    )
    allowed = await GroundingVerifierAgent().execute(
        AgentRequest(
            session_id=uuid.uuid4(),
            turn_id=uuid.uuid4(),
            input={**request_input, "general_knowledge_allowed": True},
        ),
        CancellationToken(),
    )

    assert disallowed.output["verdict"] == "no_fundamentada"
    assert allowed.output["verdict"] == "no_verificable"
    assert disallowed.output["verdict"] != allowed.output["verdict"]
