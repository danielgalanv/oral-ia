"""FR-012, FR-011a, FR-012b: end a session (voluntary or limit-reached) and generate the
descriptive-only technical summary, releasing the single-active-session lock."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import update
from sqlalchemy.orm import Session as SASession

from oralia.application.services import session_lock_service
from oralia.application.services.technical_summary_service import generate_summary
from oralia.application.services.trace_service import record_event
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from oralia.infrastructure.telemetry import resources

CONFIRMATION_MESSAGE = "Tu sesión ha finalizado. Gracias por participar."


@dataclass(frozen=True, slots=True)
class SessionCloseOutcome:
    """Result of the atomic active-to-terminal transition claim."""

    session: models.Session
    transition_won: bool


def close_session_with_outcome(
    db: SASession,
    session: models.Session,
    *,
    status: str = "closed_voluntary",
    defer_privacy: bool = False,
    retained_scope: frozenset[str] | None = None,
) -> SessionCloseOutcome:
    ended_at = utcnow()
    claimed = db.execute(
        update(models.Session)
        .where(models.Session.id == session.id, models.Session.status == "active")
        .values(status=status, ended_at=ended_at)
    )
    if claimed.rowcount != 1:
        db.expire(session)
        db.refresh(session)
        return SessionCloseOutcome(session=session, transition_won=False)
    db.refresh(session)
    db.flush()

    session.technical_summary_ref = generate_summary(db, session)
    db.add(session)

    session_lock_service.release(db, session)

    record_event(
        db,
        session_id=session.id,
        event_type="session_closed",
        payload={"status": status},
        memory_category="episodic",
        resource_usage=resources.as_dict(),
    )

    if not defer_privacy:
        from oralia.application.services.session_privacy_service import finalize_session_privacy

        finalize_session_privacy(db, session, retained_scope=retained_scope)
    return SessionCloseOutcome(session=session, transition_won=True)


def close_session(
    db: SASession, session: models.Session, *, status: str = "closed_voluntary"
) -> models.Session:
    """Close a session while preserving the historical session-only return API."""

    return close_session_with_outcome(db, session, status=status).session


def end_session_voluntarily(
    db: SASession, session: models.Session, *, retained_scope: frozenset[str] | None = None
) -> models.Session:
    return close_session_with_outcome(
        db, session, status="closed_voluntary", retained_scope=retained_scope
    ).session
