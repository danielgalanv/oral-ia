"""SC-002: >=2 agencies reuse the same registered agents in different order/combination."""

import pytest

from oralia.application.commands.register_agency import AgencyCompositionInput, register_agency
from oralia.domain.agencies.agency import ExecutionStep
from oralia.infrastructure.db import models


@pytest.fixture()
def three_agents(db_session):
    contract = models.AgentContract(
        agent_id="shared",
        version="1.0.0",
        purpose="p",
        input_schema_ref="AgentRequest",
        output_schema_ref="AgentResult",
        timeout_ms=1000,
    )
    db_session.add(contract)
    db_session.flush()
    agents = []
    for name in ("retriever", "generator", "verifier"):
        agent = models.Agent(name=name, version="1.0.0", contract_id=contract.id, capabilities=[])
        db_session.add(agent)
        agents.append(agent)
    db_session.flush()
    return {a.name: a.id for a in agents}


@pytest.mark.integration
def test_two_agencies_reuse_same_agents_different_order(db_session, three_agents):
    agency_1 = register_agency(
        db_session,
        AgencyCompositionInput(
            name="A1",
            version="1.0.0",
            steps=[
                ExecutionStep(step_id="s1", agent_id=three_agents["retriever"], role="retriever"),
                ExecutionStep(step_id="s2", agent_id=three_agents["generator"], role="generator"),
                ExecutionStep(step_id="s3", agent_id=three_agents["verifier"], role="verifier"),
            ],
        ),
    )
    agency_2 = register_agency(
        db_session,
        AgencyCompositionInput(
            name="A2",
            version="1.0.0",
            steps=[
                ExecutionStep(step_id="s1", agent_id=three_agents["verifier"], role="retriever"),
                ExecutionStep(step_id="s2", agent_id=three_agents["generator"], role="generator"),
            ],
        ),
    )

    assert agency_1.id != agency_2.id
    agency_1_agents = {s["agent_id"] for s in agency_1.steps}
    agency_2_agents = {s["agent_id"] for s in agency_2.steps}
    assert agency_1_agents & agency_2_agents  # genuinely reused, not disjoint sets


@pytest.mark.integration
def test_generator_cannot_also_verify_its_own_output(db_session, three_agents):
    with pytest.raises(ValueError, match="generator and verifier"):
        register_agency(
            db_session,
            AgencyCompositionInput(
                name="Bad agency",
                version="1.0.0",
                steps=[
                    ExecutionStep(step_id="s1", agent_id=three_agents["generator"], role="generator"),
                    ExecutionStep(step_id="s2", agent_id=three_agents["generator"], role="verifier"),
                ],
            ),
        )
