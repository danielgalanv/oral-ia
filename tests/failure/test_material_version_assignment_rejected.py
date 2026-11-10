"""Failure test (closes /speckit-analyze finding F3): assigning a retired or inactive
material version to a new activity is rejected (FR-013a)."""

from __future__ import annotations

from oralia.application.commands.activate_material import (
    DocumentNotActiveError,
    activate_material,
    assign_to_activity,
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


def test_assign_to_activity_rejected_for_inactive_document(db_session):
    document = _make_processed_document(db_session)
    activate_material(db_session, document.id)
    deactivate_material(db_session, document.id)

    try:
        assign_to_activity(db_session, document.id, "act-new")
        raise AssertionError("expected DocumentNotActiveError")
    except DocumentNotActiveError:
        pass


def test_assign_to_activity_rejected_for_retired_document(db_session):
    document = _make_processed_document(db_session)
    activate_material(db_session, document.id)
    document.retired_at = utcnow()
    db_session.add(document)
    db_session.flush()

    try:
        assign_to_activity(db_session, document.id, "act-new")
        raise AssertionError("expected DocumentNotActiveError")
    except DocumentNotActiveError:
        pass


def test_assign_to_activity_succeeds_for_active_document(db_session):
    document = _make_processed_document(db_session)
    activate_material(db_session, document.id)

    updated = assign_to_activity(db_session, document.id, "act-new")
    assert "act-new" in updated.activity_configuration_ids
