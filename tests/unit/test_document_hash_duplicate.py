"""Unit tests for document-content-hash duplicate detection (FR-005)."""

from __future__ import annotations

from oralia.application.commands.ingest_material import compute_hash, find_duplicate
from oralia.infrastructure.db import models


def test_identical_bytes_produce_identical_hash():
    content = b"contenido identico de prueba"
    assert compute_hash(content) == compute_hash(content)


def test_different_bytes_produce_different_hash():
    assert compute_hash(b"contenido A") != compute_hash(b"contenido B")


def test_find_duplicate_matches_same_course_same_hash(db_session):
    course = models.Course(name="C", subject_code="C1")
    db_session.add(course)
    db_session.flush()

    content_hash = compute_hash(b"contenido de prueba")
    existing = models.MaterialDocument(
        course_id=course.id,
        filename="a.pdf",
        content_hash=content_hash,
        mime_type="application/pdf",
        size_bytes=10,
        status="processed",
    )
    db_session.add(existing)
    db_session.flush()

    found = find_duplicate(db_session, course_id=course.id, content_hash=content_hash)
    assert found is not None
    assert found.id == existing.id


def test_find_duplicate_scoped_to_course(db_session):
    course_a = models.Course(name="A", subject_code="A1")
    course_b = models.Course(name="B", subject_code="B1")
    db_session.add_all([course_a, course_b])
    db_session.flush()

    content_hash = compute_hash(b"mismo contenido, cursos distintos")
    existing = models.MaterialDocument(
        course_id=course_a.id,
        filename="a.pdf",
        content_hash=content_hash,
        mime_type="application/pdf",
        size_bytes=10,
        status="processed",
    )
    db_session.add(existing)
    db_session.flush()

    found_in_other_course = find_duplicate(db_session, course_id=course_b.id, content_hash=content_hash)
    assert found_in_other_course is None
