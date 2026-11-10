"""review_material_conflict command: professor marks a MaterialConflictRecord reviewed
(FR-022a)."""

from __future__ import annotations

from sqlalchemy.orm import Session as SASession

from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow


class ConflictNotFoundError(LookupError):
    pass


def list_conflicts(db: SASession, *, review_status: str | None = None) -> list[models.MaterialConflictRecord]:
    query = db.query(models.MaterialConflictRecord)
    if review_status is not None:
        query = query.filter(models.MaterialConflictRecord.review_status == review_status)
    return query.order_by(models.MaterialConflictRecord.created_at.desc()).all()


def review_material_conflict(db: SASession, conflict_id: str) -> models.MaterialConflictRecord:
    record = db.get(models.MaterialConflictRecord, conflict_id)
    if record is None:
        raise ConflictNotFoundError(conflict_id)
    record.review_status = "reviewed"
    record.reviewed_at = utcnow()
    db.add(record)
    db.flush()
    return record
