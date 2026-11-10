"""FR-003, FR-004, FR-005: register an agent + its contract into the catalog."""

from __future__ import annotations

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session as SASession

from oralia.infrastructure.db import models


class AgentContractInput(BaseModel):
    agent_id: str
    version: str
    purpose: str
    input_schema_ref: str
    output_schema_ref: str
    timeout_ms: int
    preconditions: list[str] = Field(default_factory=list)
    postconditions: list[str] = Field(default_factory=list)
    allowed_sources: list[str] = Field(default_factory=list)
    allowed_tools: list[str] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)
    expected_cost: str = ""
    possible_errors: list[str] = Field(default_factory=list)
    confidence_semantics: str = ""
    success_criteria: list[str] = Field(default_factory=list)
    cancellation_policy: str = "cooperative, honors deadline_ms"
    trace_fields: list[str] = Field(default_factory=list)


class AgentRegistrationInput(BaseModel):
    name: str
    version: str
    capabilities: list[str] = Field(default_factory=list)
    contract: AgentContractInput


def register_agent(db: SASession, data: AgentRegistrationInput) -> models.Agent:
    contract = models.AgentContract(**data.contract.model_dump())
    db.add(contract)
    db.flush()

    agent = models.Agent(
        name=data.name,
        version=data.version,
        contract_id=contract.id,
        capabilities=data.capabilities,
        availability_status="available",
    )
    db.add(agent)
    db.flush()
    return agent


def list_agents(db: SASession) -> list[models.Agent]:
    return db.query(models.Agent).order_by(models.Agent.registered_at.asc()).all()


def get_agent(db: SASession, agent_id: str) -> models.Agent | None:
    return db.get(models.Agent, agent_id)
