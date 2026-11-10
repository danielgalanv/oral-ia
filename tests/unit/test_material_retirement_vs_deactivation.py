"""US5 unit test: a retired version cannot be reactivated, while a merely-deactivated
one can (FR-013, FR-015)."""

from __future__ import annotations

import pytest

from oralia.application.commands.activate_material import (
    DocumentRetiredError,
    activate_material,
    deactivate_material,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow


def _make_processed_document(db) -> models.MaterialDocument:
    course = models.Course(name="C", subject_code="C1")
    db.add(course)
    db.flush()
    document = models.MaterialDocument(
        course_id=course.id,
        filename="f.pdf",
        content_hash="h",
        mime_type="application/pdf",
        size_bytes=1,
        status="processed",
    )
    db.add(document)
    db.flush()
    return document


def test_merely_deactivated_document_can_be_reactivated(db_session):
    document = _make_processed_document(db_session)
    activate_material(db_session, document.id)
    deactivate_material(db_session, document.id)

    reactivated = activate_material(db_session, document.id)
    assert reactivated.status == "active"


def test_retired_document_cannot_be_reactivated(db_session):
    document = _make_processed_document(db_session)
    activate_material(db_session, document.id)
    document.retired_at = utcnow()
    document.status = "inactive"
    db_session.add(document)
    db_session.flush()

    with pytest.raises(DocumentRetiredError):
        activate_material(db_session, document.id)
