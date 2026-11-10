"""US5 integration test: after replacing a version, new sessions only retrieve
fragments from the active version (FR-014, FR-015, SC-002/SC-003)."""

from __future__ import annotations

import pytest

from tests.conftest import MATERIALS_FIXTURES_DIR


@pytest.mark.integration
def test_query_after_replacement_only_returns_new_version(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        r1 = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course, "activity_configuration_ids": ["act-1"]},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    doc_id = r1.json()["id"]
    app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")

    with open(MATERIALS_FIXTURES_DIR / "sample_v2.pdf", "rb") as fh:
        r2 = app_client.post(
            f"/api/v1/materials/documents/{doc_id}/versions",
            files={"file": ("sample_v2.pdf", fh, "application/pdf")},
        )
    new_doc_id = r2.json()["id"]
    app_client.post(f"/api/v1/materials/documents/{new_doc_id}/activate")

    r3 = app_client.post(
        "/api/v1/materials/query",
        json={
            "query_text": "version del documento de prueba",
            "course_id": seeded_course,
            "activity_configuration_id": "act-1",
            "max_fragments": 10,
            "time_budget_ms": 5000,
        },
    )
    document_ids = {f["document_id"] for f in r3.json()["fragments"]}
    assert new_doc_id in document_ids
    assert doc_id not in document_ids
