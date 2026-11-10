"""US4 failure test: an inactive, retired, or vigencia-expired material is never
returned regardless of query (FR-019, FR-019a)."""

from __future__ import annotations

from datetime import timedelta

import pytest

from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from tests.conftest import MATERIALS_FIXTURES_DIR


def _query(app_client, course_id: str):
    return app_client.post(
        "/api/v1/materials/query",
        json={
            "query_text": "documento de prueba",
            "course_id": course_id,
            "activity_configuration_id": "act-1",
            "max_fragments": 10,
            "time_budget_ms": 5000,
        },
    )


@pytest.mark.failure
def test_inactive_document_never_returned(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course, "activity_configuration_ids": ["act-1"]},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    doc_id = r.json()["id"]
    app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")
    app_client.post(f"/api/v1/materials/documents/{doc_id}/deactivate")

    r2 = _query(app_client, seeded_course)
    assert r2.json()["fragments"] == []


@pytest.mark.failure
def test_retired_document_never_returned(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course, "activity_configuration_ids": ["act-1"]},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    doc_id = r.json()["id"]
    app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")

    Session = app_client.__db_sessionmaker__
    db = Session()
    document = db.get(models.MaterialDocument, doc_id)
    document.retired_at = utcnow()
    document.status = "inactive"
    db.add(document)
    db.commit()
    db.close()

    r2 = _query(app_client, seeded_course)
    assert r2.json()["fragments"] == []


@pytest.mark.failure
def test_vigencia_expired_fragment_never_returned(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course, "activity_configuration_ids": ["act-1"]},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    doc_id = r.json()["id"]
    app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")

    Session = app_client.__db_sessionmaker__
    db = Session()
    fragments = db.query(models.MaterialFragment).filter_by(document_id=doc_id).all()
    for fragment in fragments:
        fragment.valid_until = utcnow() - timedelta(days=1)
        db.add(fragment)
    db.commit()
    db.close()

    r2 = _query(app_client, seeded_course)
    assert r2.json()["fragments"] == []
