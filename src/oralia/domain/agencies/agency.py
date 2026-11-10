"""AgencyDefinition / ExecutionStep schemas (contracts/agent-contract.md).

Principio IV enforcement lives here: an ExecutionStep with role "generator" MUST NOT
also carry role "verifier" for its own output within the same Agency.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

StepRole = Literal["retriever", "generator", "verifier", "decider", "presenter"]


class ExecutionStep(BaseModel):
    step_id: str
    agent_id: str
    role: StepRole
    depends_on: list[str] = Field(default_factory=list)
    parallelizable: bool = False


class AgencyDefinition(BaseModel):
    id: str
    name: str
    version: str
    steps: list[ExecutionStep]
    verifiers_required: list[str] = Field(default_factory=list)
    fallback_step: str | None = None
    termination_rule: str = ""

    @field_validator("steps")
    @classmethod
    def _no_agent_is_both_generator_and_verifier_for_itself(
        cls, steps: list[ExecutionStep]
    ) -> list[ExecutionStep]:
        by_agent: dict[str, set[str]] = {}
        for step in steps:
            by_agent.setdefault(step.agent_id, set()).add(step.role)
        for agent_id, roles in by_agent.items():
            if {"generator", "verifier"}.issubset(roles):
                raise ValueError(
                    f"agent {agent_id} cannot hold both generator and verifier roles "
                    "in the same Agency (Constitution Principio IV)"
                )
        return steps
