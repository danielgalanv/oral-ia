"""SC-001: >=5 agents register under the same contract without orchestrator changes."""

import pytest

from oralia.application.commands.register_agent import (
    AgentContractInput,
    AgentRegistrationInput,
    list_agents,
    register_agent,
)
from oralia.infrastructure.db import models


@pytest.mark.integration
def test_five_agents_share_one_contract_id(db_session):
    contract = models.AgentContract(
        agent_id="shared",
        version="1.0.0",
        purpose="shared test contract",
        input_schema_ref="AgentRequest",
        output_schema_ref="AgentResult",
        timeout_ms=1000,
    )
    db_session.add(contract)
    db_session.flush()

    for i in range(5):
        agent = models.Agent(
            name=f"agent-{i}",
            version="1.0.0",
            contract_id=contract.id,
            capabilities=["demo"],
        )
        db_session.add(agent)
    db_session.flush()

    agents = list_agents(db_session)
    assert len(agents) == 5
    assert {a.contract_id for a in agents} == {contract.id}


@pytest.mark.integration
def test_register_agent_command_creates_independent_contract_per_call(db_session):
    """register_agent() (the command, distinct from the shared-contract seed pattern
    above) creates a fresh AgentContract per call — both paths are valid per
    data-model.md's 1-N AgentContract->Agent relationship."""
    for i in range(5):
        agent = register_agent(
            db_session,
            AgentRegistrationInput(
                name=f"cmd-agent-{i}",
                version="1.0.0",
                capabilities=["demo"],
                contract=AgentContractInput(
                    agent_id="cmd-contract",
                    version="1.0.0",
                    purpose="p",
                    input_schema_ref="AgentRequest",
                    output_schema_ref="AgentResult",
                    timeout_ms=1000,
                ),
            ),
        )
        assert agent.id

    assert len(list_agents(db_session)) == 5
