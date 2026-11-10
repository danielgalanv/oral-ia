"""TraceEvent logging (FR-016, FR-024): every execution/decision/error/state-change is
persisted as a structured, observable record — never as free-form model reasoning."""

from __future__ import annotations

from typing import Any

import structlog
from sqlalchemy.orm import Session as SASession

from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow

logger = structlog.get_logger("oralia.trace")


def record_event(
    db: SASession,
    *,
    session_id: str,
    event_type: str,
    turn_id: str | None = None,
    agent_id: str | None = None,
    payload: dict[str, Any] | None = None,
    latency_ms: int | None = None,
    resource_usage: dict[str, Any] | None = None,
    memory_category: str = "episodic",
) -> models.TraceEvent:
    """Persist one TraceEvent and mirror it to structured (structlog) output.

    ``payload`` MUST NOT contain free-form model reasoning (FR-024) — callers pass only
    structured results (verdicts, decisions, error codes), never raw chain-of-thought.
    """

    event = models.TraceEvent(
        session_id=session_id,
        turn_id=turn_id,
        event_type=event_type,
        agent_id=agent_id,
        payload=payload or {},
        latency_ms=latency_ms,
        resource_usage=resource_usage,
        memory_category=memory_category,
        created_at=utcnow(),
    )
    db.add(event)
    db.flush()

    logger.info(
        event_type,
        session_id=session_id,
        turn_id=turn_id,
        agent_id=agent_id,
        latency_ms=latency_ms,
        memory_category=memory_category,
    )
    return event


def reconstruct_trace(db: SASession, session_id: str) -> list[models.TraceEvent]:
    """Full trace for a session, chronological (US6, FR-020)."""
    return (
        db.query(models.TraceEvent)
        .filter(models.TraceEvent.session_id == session_id)
        .order_by(models.TraceEvent.created_at.asc())
        .all()
    )
