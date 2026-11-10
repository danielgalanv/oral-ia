"""FR-012, FR-012a, FR-011a: submit a text turn on an active session."""

from __future__ import annotations

from sqlalchemy.orm import Session as SASession

from oralia.application.orchestration.turn_orchestrator import TurnResult, run_turn
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow


class SessionNotActive(ValueError):
    pass


async def submit_turn(db: SASession, session: models.Session, text: str) -> TurnResult:
    if session.status != "active":
        raise SessionNotActive(f"session {session.id} is not active (status={session.status})")

    result = await run_turn(db, session, text)

    # FR-011a: auto-close once the turn/duration limit is reached, even though the
    # participant hasn't finalized voluntarily.
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    elapsed = (utcnow() - session.started_at).total_seconds()
    limit_reached = session.turn_count >= activity.max_turns or elapsed >= activity.max_duration_seconds

    if limit_reached and session.status == "active":
        from oralia.application.commands.end_session import close_session

        close_session(db, session, status="closed_limit_reached")

    return result
