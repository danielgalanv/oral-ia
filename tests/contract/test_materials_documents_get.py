"""Contract test for GET /api/v1/materials/documents and /{id} — FR-012."""

from __future__ import annotations

import pytest

from tests.conftest import MATERIALS_FIXTURES_DIR


def _upload(app_client, course_id: str, fixture: str = "sample.pdf"):
    with open(MATERIALS_FIXTURES_DIR / fixture, "rb") as fh:
        return app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": course_id},
            files={"file": (fixture, fh, "application/pdf")},
        )


@pytest.mark.contract
def test_list_documents_for_course(app_client, seeded_course):
    _upload(app_client, seeded_course)
    r = app_client.get("/api/v1/materials/documents", params={"course_id": seeded_course})
    assert r.status_code == 200
    assert len(r.json()) == 1


@pytest.mark.contract
def test_get_document_detail_includes_course_coverage(app_client, seeded_course):
    upload = _upload(app_client, seeded_course)
    doc_id = upload.json()["id"]
    r = app_client.get(f"/api/v1/materials/documents/{doc_id}")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == doc_id
    assert body["course_coverage"]["total_documents"] == 1
    assert body["course_coverage"]["processed_count"] == 1
    assert body["course_coverage"]["error_count"] == 0


@pytest.mark.contract
def test_get_unknown_document_returns_404(app_client):
    r = app_client.get("/api/v1/materials/documents/does-not-exist")
    assert r.status_code == 404
