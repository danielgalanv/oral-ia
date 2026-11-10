"""Single-writer material-index-rebuild enforcement (Edge Case, research.md §9).

Same pattern as ``session_lock_service.py``: acquiring is an atomic INSERT (unique
constraint violation on conflict), release is a plain UPDATE clearing the token back to
NULL. A second concurrent rebuild request is rejected explicitly rather than queued.
"""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as SASession

from oralia.infrastructure.db import models

ACTIVE_TOKEN = "ACTIVE"


class IndexRebuildAlreadyInProgress(RuntimeError):
    """Raised when a second index rebuild is attempted while one is already running."""


def acquire(db: SASession) -> models.IndexRebuildLock:
    lock = models.IndexRebuildLock(active_lock_token=ACTIVE_TOKEN)
    db.add(lock)
    try:
        db.flush()
    except IntegrityError as exc:
        db.rollback()
        raise IndexRebuildAlreadyInProgress("a material index rebuild is already in progress") from exc
    return lock


def release(db: SASession, lock: models.IndexRebuildLock) -> None:
    lock.active_lock_token = None
    db.add(lock)
    db.flush()
