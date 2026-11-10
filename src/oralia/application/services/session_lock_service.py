"""Single-active-interactive-session enforcement (FR-012a, research.md §3).

Uses the ``active_lock_token`` unique-constraint column on Session: acquiring the lock is
an atomic INSERT (unique constraint violation on conflict), release is a plain UPDATE
that clears the token back to NULL.
"""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as SASession

from oralia.infrastructure.db import models

ACTIVE_TOKEN = "ACTIVE"


class SessionAlreadyActive(RuntimeError):
    """Raised when a second interactive session is attempted (FR-012a)."""


def acquire(db: SASession, session: models.Session) -> None:
    session.active_lock_token = ACTIVE_TOKEN
    db.add(session)
    try:
        db.flush()
    except IntegrityError as exc:
        db.rollback()
        raise SessionAlreadyActive("another interactive session is already active on this instance") from exc


def release(db: SASession, session: models.Session) -> None:
    session.active_lock_token = None
    db.add(session)
    db.flush()


def get_active_session(db: SASession) -> models.Session | None:
    return db.query(models.Session).filter(models.Session.active_lock_token == ACTIVE_TOKEN).one_or_none()
