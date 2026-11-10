"""SC-008: an agent can be swapped for a contract-compatible replacement without any
change to the Agency definition or orchestrator code — only the catalog row changes."""

import pytest

from oralia.application.commands.register_agency import AgencyCompositionInput, register_agency
from oralia.domain.agencies.agency import ExecutionStep
from oralia.infrastructure.db import models


@pytest.mark.integration
def test_swap_agent_behind_same_contract_requires_no_agency_change(db_session):
    contract = models.AgentContract(
        agent_id="swap-contract",
        version="1.0.0",
        purpose="p",
        input_schema_ref="AgentRequest",
        output_schema_ref="AgentResult",
        timeout_ms=1000,
    )
    db_session.add(contract)
    db_session.flush()

    original = models.Agent(
        name="generator-v1", version="1.0.0", contract_id=contract.id, capabilities=["generate"]
    )
    db_session.add(original)
    db_session.flush()

    agency = register_agency(
        db_session,
        AgencyCompositionInput(
            name="Agency with swappable generator",
            version="1.0.0",
            steps=[ExecutionStep(step_id="s1", agent_id=original.id, role="generator")],
        ),
    )
    original_step_snapshot = agency.steps

    # Substitute: register a new Agent implementing the *same* contract, retire the old
    # one, and point the Agency's step at the replacement. No Agency-shape change, no
    # orchestrator code change — only which catalog Agent id the step targets.
    replacement = models.Agent(
        name="generator-v2", version="2.0.0", contract_id=contract.id, capabilities=["generate"]
    )
    db_session.add(replacement)
    original.availability_status = "unavailable"
    db_session.flush()

    agency.steps = [{**original_step_snapshot[0], "agent_id": replacement.id}]
    db_session.add(agency)
    db_session.flush()

    assert agency.steps[0]["agent_id"] == replacement.id
    assert agency.steps[0]["role"] == "generator"
    # The step's structural shape (role, dependencies) is untouched by the swap.
    assert {k: v for k, v in agency.steps[0].items() if k != "agent_id"} == {
        k: v for k, v in original_step_snapshot[0].items() if k != "agent_id"
    }
