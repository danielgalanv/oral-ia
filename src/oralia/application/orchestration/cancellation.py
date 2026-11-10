"""Timeout/cancellation enforcement around a single agent execution (FR-018, US4).

A timeout or cancellation is turned into a well-formed AgentResult rather than an
exception escaping to the caller, so the orchestrator can always degrade in a controlled
way (Constitution Principio IX) instead of crashing the turn.
"""

from __future__ import annotations

import asyncio

from oralia.domain.agents.agent import Executable
from oralia.domain.agents.agent_contract import (
    AgentError,
    AgentRequest,
    AgentResult,
    CancellationToken,
)


async def run_with_deadline(
    agent: Executable,
    request: AgentRequest,
    cancellation: CancellationToken | None = None,
) -> AgentResult:
    """Execute ``agent`` honoring ``request.deadline_ms`` (research.md §2, FR-018)."""

    token = cancellation or CancellationToken()
    deadline_s = max(request.deadline_ms, 0) / 1000

    try:
        return await asyncio.wait_for(agent.execute(request, token), timeout=deadline_s)
    except TimeoutError:
        token.cancel()
        return AgentResult(
            status="timeout",
            output=None,
            confidence=None,
            error=AgentError(
                code="AGENT_TIMEOUT",
                message=f"agent exceeded deadline_ms={request.deadline_ms}",
                recoverable=True,
            ),
            trace={"agent_id": getattr(agent, "contract", None) and agent.contract.agent_id},
        )
    except asyncio.CancelledError:
        return AgentResult(
            status="cancelled",
            output=None,
            confidence=None,
            error=AgentError(code="AGENT_CANCELLED", message="execution cancelled", recoverable=True),
            trace={},
        )
    except Exception as exc:  # noqa: BLE001 — any agent failure must degrade, not crash the turn
        return AgentResult(
            status="error",
            output=None,
            confidence=None,
            error=AgentError(code="AGENT_ERROR", message=str(exc), recoverable=False),
            trace={},
        )
