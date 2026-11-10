"""AgentRequest / AgentResult / AgentError / CancellationToken.

Mirrors specs/001-core-cognitive-runtime/contracts/agent-contract.md exactly. This is the
one shape every agent — deterministic today, LLM-backed in a later feature — is invoked
through (Constitution Principio II/XI: components stay behind a replaceable interface).
"""

from __future__ import annotations

import asyncio
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

AgentResultStatus = Literal["ok", "error", "timeout", "cancelled"]


class AgentError(BaseModel):
    code: str
    message: str
    recoverable: bool = True


class AgentRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    session_id: UUID
    turn_id: UUID
    input: dict[str, Any] = Field(default_factory=dict)
    context: dict[str, Any] = Field(default_factory=dict)
    deadline_ms: int = 5000


class AgentResult(BaseModel):
    status: AgentResultStatus
    output: dict[str, Any] | None = None
    confidence: float | None = None
    error: AgentError | None = None
    trace: dict[str, Any] = Field(default_factory=dict)


class CancellationToken:
    """A single-shot, in-process cancellation signal (Constitution Principio IX)."""

    def __init__(self) -> None:
        self._event = asyncio.Event()

    def cancel(self) -> None:
        self._event.set()

    def is_cancelled(self) -> bool:
        return self._event.is_set()

    async def wait(self) -> None:
        await self._event.wait()
