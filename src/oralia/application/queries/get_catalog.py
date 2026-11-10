"""FR-003: consultable catalog of agents and agencies."""

from __future__ import annotations

from sqlalchemy.orm import Session as SASession

from oralia.domain.agents.agent import AgentContractSchema, AgentDescriptor
from oralia.infrastructure.db import models


def list_agent_descriptors(db: SASession) -> list[AgentDescriptor]:
    agents = db.query(models.Agent).order_by(models.Agent.registered_at.asc()).all()
    result = []
    for agent in agents:
        contract = db.get(models.AgentContract, agent.contract_id)
        result.append(
            AgentDescriptor(
                id=agent.id,
                name=agent.name,
                version=agent.version,
                capabilities=agent.capabilities,
                availability_status=agent.availability_status,
                contract=AgentContractSchema(
                    agent_id=contract.agent_id,
                    version=contract.version,
                    purpose=contract.purpose,
                    input_schema_ref=contract.input_schema_ref,
                    output_schema_ref=contract.output_schema_ref,
                    preconditions=contract.preconditions,
                    postconditions=contract.postconditions,
                    allowed_sources=contract.allowed_sources,
                    allowed_tools=contract.allowed_tools,
                    permissions=contract.permissions,
                    timeout_ms=contract.timeout_ms,
                    expected_cost=contract.expected_cost,
                    possible_errors=contract.possible_errors,
                    confidence_semantics=contract.confidence_semantics,
                    success_criteria=contract.success_criteria,
                    cancellation_policy=contract.cancellation_policy,
                    trace_fields=contract.trace_fields,
                ),
            )
        )
    return result


def list_agency_summaries(db: SASession) -> list[dict]:
    agencies = db.query(models.Agency).all()
    return [
        {
            "id": a.id,
            "name": a.name,
            "version": a.version,
            "steps": a.steps,
            "verifiers_required": a.verifiers_required,
            "fallback_step": a.fallback_step,
            "termination_rule": a.termination_rule,
            "availability_status": a.availability_status,
        }
        for a in agencies
    ]
