"""get_material_catalog query (FR-012): list/detail with processing status, plus a
per-course coverage/error summary (FR-010, /speckit-analyze finding F4/T080)."""

from __future__ import annotations

from sqlalchemy.orm import Session as SASession

from oralia.infrastructure.db import models

_ERROR_STATUSES = ("error", "not_processable")
_READY_STATUSES = ("processed", "active", "inactive")


def list_materials(db: SASession, *, course_id: str | None = None) -> list[models.MaterialDocument]:
    query = db.query(models.MaterialDocument)
    if course_id is not None:
        query = query.filter(models.MaterialDocument.course_id == course_id)
    return query.order_by(models.MaterialDocument.created_at.desc()).all()


def get_material(db: SASession, document_id: str) -> models.MaterialDocument | None:
    return db.get(models.MaterialDocument, document_id)


def get_coverage_summary(db: SASession, *, course_id: str) -> dict:
    """FR-010: how many of a course's uploaded documents finished processing cleanly vs.
    ended in ``error``/``not_processable`` — the professor-facing coverage signal."""

    documents = list_materials(db, course_id=course_id)
    by_status: dict[str, int] = {}
    for document in documents:
        by_status[document.status] = by_status.get(document.status, 0) + 1
    return {
        "total_documents": len(documents),
        "by_status": by_status,
        "processed_count": sum(by_status.get(status, 0) for status in _READY_STATUSES),
        "error_count": sum(by_status.get(status, 0) for status in _ERROR_STATUSES),
    }


def get_material_detail(db: SASession, document_id: str) -> dict | None:
    document = get_material(db, document_id)
    if document is None:
        return None
    return {
        "document": document,
        "course_coverage": get_coverage_summary(db, course_id=document.course_id),
    }
