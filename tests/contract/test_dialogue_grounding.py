from uuid import uuid4

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.grounding_verifier_agent import GroundingVerifierAgent


@pytest.mark.parametrize(
    "candidate,expected",
    [
        ("La validación comprueba campos y no guarda registros.", "fundamentada"),
        ("La validación no comprueba campos y no guarda registros.", "no_fundamentada"),
        ("La validación comprueba campos y guarda registros.", "no_fundamentada"),
    ],
)
async def test_v2_polarity_is_checked_per_conjunct_without_copied_evidence_exemption(candidate, expected):
    result = await GroundingVerifierAgent().execute(
        AgentRequest(
            session_id=uuid4(),
            turn_id=uuid4(),
            input={
                "dialogue_schema_version": 2,
                "proposal_text": candidate,
                "evidence": [
                    {"unit_id": "reviewed", "text": "La validación comprueba campos y no guarda registros."}
                ],
            },
        ),
        CancellationToken(),
    )
    assert result.output["verdict"] == expected
