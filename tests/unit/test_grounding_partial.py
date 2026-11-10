"""US3 unit test: a proposal with only some claims supported is classified
parcialmente_fundamentada, naming the unsupported claims."""

from __future__ import annotations

import uuid

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.grounding_verifier_agent import GroundingVerifierAgent


async def test_partial_support_names_unsupported_claims():
    evidence = [{"fragment_id": "f1", "text": "Python es un lenguaje de programacion interpretado."}]
    proposal = "Python es un lenguaje de programacion. Java fue creado por marcianos verdes."
    result = await GroundingVerifierAgent().execute(
        AgentRequest(
            session_id=uuid.uuid4(),
            turn_id=uuid.uuid4(),
            input={"proposal_text": proposal, "evidence": evidence, "general_knowledge_allowed": False},
        ),
        CancellationToken(),
    )
    assert result.output["verdict"] == "parcialmente_fundamentada"
    assert any("marcianos" in c for c in result.output["unsupported_claims"])
    assert any("Python" in c for c in result.output["supported_claims"])
