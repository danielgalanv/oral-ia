"""Generic executor for an AgencyDefinition's steps (FR-006, FR-018, US4).

Runs steps in dependency order, enforces each step's timeout via
``cancellation.run_with_deadline``, and on a non-"ok" result jumps to
``fallback_step`` if one is defined — otherwise the agency execution ends in a
"degraded"/"failed" outcome without ever leaving a torn/partial write to persisted
state (state writes happen one level up, in the TurnOrchestrator, only from a
completed StepOutcome).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from oralia.application.orchestration.cancellation import run_with_deadline
from oralia.domain.agencies.agency import AgencyDefinition, ExecutionStep
from oralia.domain.agents.agent import Executable
from oralia.domain.agents.agent_contract import AgentRequest, AgentResult


@dataclass
class StepOutcome:
    step_id: str
    agent_id: str
    result: AgentResult


@dataclass
class AgencyOutcome:
    status: str  # "completed" | "degraded" | "failed"
    steps: list[StepOutcome] = field(default_factory=list)
    fallback_used: bool = False


def _order_steps(steps: list[ExecutionStep]) -> list[ExecutionStep]:
    """Simple dependency-respecting order (Kahn's algorithm) — sufficient for the small,
    mostly-linear agencies this feature composes (Principio XI: no over-engineering)."""
    by_id = {s.step_id: s for s in steps}
    resolved: list[ExecutionStep] = []
    seen: set[str] = set()

    def visit(step: ExecutionStep) -> None:
        if step.step_id in seen:
            return
        for dep_id in step.depends_on:
            if dep_id in by_id:
                visit(by_id[dep_id])
        seen.add(step.step_id)
        resolved.append(step)

    for step in steps:
        visit(step)
    return resolved


async def execute_agency(
    agency: AgencyDefinition,
    agent_registry: dict[str, Executable],
    request_for_step,
) -> AgencyOutcome:
    """``request_for_step(step) -> AgentRequest`` builds the request for each step,
    letting the caller thread prior-step outputs into later steps' input."""

    outcome = AgencyOutcome(status="completed")
    by_id = {s.step_id: s for s in agency.steps}
    normal_steps = [s for s in agency.steps if s.step_id != agency.fallback_step]
    ordered = _order_steps(normal_steps)

    for step in ordered:
        agent = agent_registry.get(step.agent_id)
        if agent is None:
            outcome.status = "failed"
            outcome.steps.append(
                StepOutcome(
                    step_id=step.step_id,
                    agent_id=step.agent_id,
                    result=AgentResult(status="error", error=None, trace={"reason": "unknown agent"}),
                )
            )
            break

        request: AgentRequest = request_for_step(step, outcome)
        result = await run_with_deadline(agent, request)
        outcome.steps.append(StepOutcome(step_id=step.step_id, agent_id=step.agent_id, result=result))

        if result.status != "ok":
            if agency.fallback_step and not outcome.fallback_used:
                outcome.fallback_used = True
                outcome.status = "degraded"
                fallback = by_id.get(agency.fallback_step)
                if fallback is not None:
                    fb_agent = agent_registry.get(fallback.agent_id)
                    if fb_agent is not None:
                        fb_request = request_for_step(fallback, outcome)
                        fb_result = await run_with_deadline(fb_agent, fb_request)
                        outcome.steps.append(
                            StepOutcome(
                                step_id=fallback.step_id, agent_id=fallback.agent_id, result=fb_result
                            )
                        )
                # Stop the normal sequence here — later steps (e.g. a verifier) were
                # written assuming valid upstream output and MUST NOT run against the
                # failed step's stale/empty result (FR-018a: the caller is responsible
                # for re-running any mandatory check, such as the constitutional
                # control, against the fallback content instead).
                break
            outcome.status = "failed"
            break

    return outcome
