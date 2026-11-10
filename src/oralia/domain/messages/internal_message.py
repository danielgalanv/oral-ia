"""InternalMessage schema (contracts/agent-contract.md, Constitution Principio II)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class InternalMessage(BaseModel):
    id: str
    session_id: str
    turn_id: str
    sender_agent_id: str
    receiver_agent_id: str
    type: str
    objective: str
    content: dict[str, Any] = Field(default_factory=dict)
    evidences: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    priority: int = 0
    valid_until: datetime | None = None
    expected_response: str = ""
    success_condition: str = ""
