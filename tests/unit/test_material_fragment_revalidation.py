"""T099 (Feature 002, follow-up to T085) — unit-level coverage of
`get_currently_valid_fragment`, the shared revalidation policy used by
`self_study_agency_composer.py` to decide whether a previously-enqueued fragment id
is still safe to reuse. Deterministic and fast (no HTTP/embeddings) — complements
`tests/integration/test_self_study_pending_fragment_revalidation.py`'s end-to-end
reproductions, and in particular gives the "fragment row deleted" case a precise,
unambiguous check that the integration fixture's coincidental content similarity
cannot mask (a stale fallback there can happen to reuse a different, genuinely valid
fragment of the same tiny document, which text-based assertions alone cannot always
tell apart from a deliberate reseed)."""

from __future__ import annotations

from oralia.domain.agents.material_retriever_agent import get_currently_valid_fragment
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow


def _make_course_document_fragment(db, *, activity_id: str, course_id: str | None = None):
    course = models.Course(name="Curso T099", subject_code="T099")
    db.add(course)
    db.flush()
    resolved_course_id = course_id or course.id
    document = models.MaterialDocument(
        course_id=resolved_course_id,
        filename="t099.pdf",
        content_hash="h",
        mime_type="application/pdf",
        size_bytes=1,
        status="active",
        activity_configuration_ids=[activity_id],
    )
    db.add(document)
    db.flush()
    fragment = models.MaterialFragment(
        document_id=document.id,
        document_version=1,
        text="Fragmento T099 de prueba.",
        location_ref="p1",
        sequence_index=0,
        embedding_ref="e1",
        course_id=resolved_course_id,
        activity_configuration_ids=[activity_id],
        indexing_status="indexed",
    )
    db.add(fragment)
    db.flush()
    return course, document, fragment


def test_valid_fragment_is_returned(db_session):
    course, _document, fragment = _make_course_document_fragment(db_session, activity_id="act-1")
    result = get_currently_valid_fragment(
        db_session, fragment.id, course_id=course.id, activity_configuration_id="act-1"
    )
    assert result is not None
    assert result.id == fragment.id


def test_document_inactive_is_rejected(db_session):
    course, document, fragment = _make_course_document_fragment(db_session, activity_id="act-1")
    document.status = "inactive"
    db_session.add(document)
    db_session.flush()
    assert (
        get_currently_valid_fragment(
            db_session, fragment.id, course_id=course.id, activity_configuration_id="act-1"
        )
        is None
    )


def test_document_retired_is_rejected(db_session):
    course, document, fragment = _make_course_document_fragment(db_session, activity_id="act-1")
    document.retired_at = utcnow()
    db_session.add(document)
    db_session.flush()
    assert (
        get_currently_valid_fragment(
            db_session, fragment.id, course_id=course.id, activity_configuration_id="act-1"
        )
        is None
    )


def test_fragment_expired_is_rejected(db_session):
    course, _document, fragment = _make_course_document_fragment(db_session, activity_id="act-1")
    fragment.valid_until = utcnow().replace(year=2000)
    db_session.add(fragment)
    db_session.flush()
    assert (
        get_currently_valid_fragment(
            db_session, fragment.id, course_id=course.id, activity_configuration_id="act-1"
        )
        is None
    )


def test_fragment_not_indexed_is_rejected(db_session):
    course, _document, fragment = _make_course_document_fragment(db_session, activity_id="act-1")
    fragment.indexing_status = "pending"
    db_session.add(fragment)
    db_session.flush()
    assert (
        get_currently_valid_fragment(
            db_session, fragment.id, course_id=course.id, activity_configuration_id="act-1"
        )
        is None
    )


def test_fragment_unassigned_from_activity_is_rejected(db_session):
    course, _document, fragment = _make_course_document_fragment(db_session, activity_id="act-1")
    fragment.activity_configuration_ids = []
    db_session.add(fragment)
    db_session.flush()
    assert (
        get_currently_valid_fragment(
            db_session, fragment.id, course_id=course.id, activity_configuration_id="act-1"
        )
        is None
    )


def test_fragment_different_course_is_rejected(db_session):
    course, _document, fragment = _make_course_document_fragment(db_session, activity_id="act-1")
    other_course = models.Course(name="Otro curso", subject_code="OTR")
    db_session.add(other_course)
    db_session.flush()
    assert (
        get_currently_valid_fragment(
            db_session, fragment.id, course_id=other_course.id, activity_configuration_id="act-1"
        )
        is None
    )


def test_document_different_course_is_rejected(db_session):
    """fragment.course_id matches, but its document's course_id does not — both MUST
    be checked independently, since they are denormalized separately in SQL."""
    course, document, fragment = _make_course_document_fragment(db_session, activity_id="act-1")
    other_course = models.Course(name="Otro curso doc", subject_code="OTR2")
    db_session.add(other_course)
    db_session.flush()
    document.course_id = other_course.id
    db_session.add(document)
    db_session.flush()
    assert (
        get_currently_valid_fragment(
            db_session, fragment.id, course_id=course.id, activity_configuration_id="act-1"
        )
        is None
    )


def test_deleted_fragment_row_is_rejected(db_session):
    """The precise case the HTTP-level reproduction cannot always distinguish from a
    legitimate reseed (a tiny fixture's fallback fragment can coincidentally look
    valid) — verified directly and unambiguously here: a missing row MUST return
    `None`, never fabricate or substitute anything."""
    course, _document, fragment = _make_course_document_fragment(db_session, activity_id="act-1")
    fragment_id = fragment.id
    db_session.delete(fragment)
    db_session.flush()
    assert (
        get_currently_valid_fragment(
            db_session, fragment_id, course_id=course.id, activity_configuration_id="act-1"
        )
        is None
    )


def test_none_filters_are_permissive(db_session):
    """`course_id=None`/`activity_configuration_id=None` MUST skip that specific
    check (mirrors `_authorized`'s treatment of an absent scope filter), not reject
    everything."""
    _course, _document, fragment = _make_course_document_fragment(db_session, activity_id="act-1")
    result = get_currently_valid_fragment(
        db_session, fragment.id, course_id=None, activity_configuration_id=None
    )
    assert result is not None
    assert result.id == fragment.id
