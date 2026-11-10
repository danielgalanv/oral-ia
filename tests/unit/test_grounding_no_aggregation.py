"""US3 unit test: grounding verdicts are never aggregated or persisted as a cross-session
participant signal (FR-023a) — the agent is stateless and writes nothing to
GroundingVerificationResult on its own."""

from __future__ import annotations

import uuid

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.grounding_verifier_agent import GroundingVerifierAgent
from oralia.infrastructure.db import models


async def test_repeated_calls_never_persist_or_influence_each_other(db_session):
    agent = GroundingVerifierAgent(db_session)
    evidence = [{"fragment_id": "f1", "text": "El agua hierve a cien grados a nivel del mar."}]

    for _ in range(5):
        result = await agent.execute(
            AgentRequest(
                session_id=uuid.uuid4(),
                turn_id=uuid.uuid4(),
                input={
                    "proposal_text": "El agua hierve a cien grados.",
                    "evidence": evidence,
                    "general_knowledge_allowed": False,
                },
            ),
            CancellationToken(),
        )
        # Identical input always yields the identical verdict — no hidden running state
        # (e.g. a tally of past no_fundamentada verdicts) can be influencing the outcome.
        assert result.output["verdict"] == "fundamentada"

    persisted = db_session.query(models.GroundingVerificationResult).count()
    assert persisted == 0
