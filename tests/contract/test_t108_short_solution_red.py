"""T108 reproduction for one-token numeric solution disclosure."""

from __future__ import annotations

import asyncio
import uuid

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.solution_non_disclosure_verifier_agent import (
    SolutionNonDisclosureVerifierAgent,
)


def test_numeric_single_token_solution_is_blocked() -> None:
    result = asyncio.run(
        SolutionNonDisclosureVerifierAgent().execute(
            AgentRequest(
                session_id=uuid.uuid4(),
                turn_id=uuid.uuid4(),
                input={
                    "question_text": "La respuesta es 4.",
                    "internal_expected_answer": "4",
                },
            ),
            CancellationToken(),
        )
    )

    assert result.output["verdict"] == "block"
    assert result.output["overlap_score"] == 1.0

