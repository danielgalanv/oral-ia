"""AgentContract / AgentDescriptor schemas (contracts/agent-contract.md) plus the async
execution protocol every registered agent implements."""

from __future__ import annotations

from typing import Protocol

from pydantic import BaseModel, Field

from oralia.domain.agents.agent_contract import AgentRequest, AgentResult, CancellationToken


class AgentContractSchema(BaseModel):
    agent_id: str
    version: str
    purpose: str
    input_schema_ref: str
    output_schema_ref: str
    preconditions: list[str] = Field(default_factory=list)
    postconditions: list[str] = Field(default_factory=list)
    allowed_sources: list[str] = Field(default_factory=list)
    allowed_tools: list[str] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)
    timeout_ms: int
    expected_cost: str = ""
    possible_errors: list[str] = Field(default_factory=list)
    confidence_semantics: str = ""
    success_criteria: list[str] = Field(default_factory=list)
    cancellation_policy: str = ""
    trace_fields: list[str] = Field(default_factory=list)


class AgentDescriptor(BaseModel):
    id: str
    name: str
    version: str
    contract: AgentContractSchema
    capabilities: list[str] = Field(default_factory=list)
    availability_status: str = "available"


class Executable(Protocol):
    """Every agent — deterministic stub today, LLM-backed later — implements this."""

    contract: AgentContractSchema

    async def execute(self, request: AgentRequest, cancellation: CancellationToken) -> AgentResult: ...
