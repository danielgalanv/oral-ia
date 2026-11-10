"""Contract test for POST /api/v1/materials/query — FR-017, FR-018 (happy path: full
provenance)."""

from __future__ import annotations

import pytest

from tests.conftest import MATERIALS_FIXTURES_DIR


def _upload_and_activate(app_client, course_id: str) -> str:
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": course_id, "activity_configuration_ids": ["act-1"]},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    doc_id = r.json()["id"]
    app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")
    return doc_id


@pytest.mark.contract
def test_query_returns_fragments_with_full_provenance(app_client, seeded_course):
    _upload_and_activate(app_client, seeded_course)

    r = app_client.post(
        "/api/v1/materials/query",
        json={
            "query_text": "documento de prueba para ORAL-IA",
            "course_id": seeded_course,
            "activity_configuration_id": "act-1",
            "max_fragments": 5,
            "time_budget_ms": 5000,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["fragments"]
    assert body["index_version"]
    for fragment in body["fragments"]:
        assert fragment["document_id"]
        assert fragment["document_version"] == 1
        assert fragment["location_ref"]
        assert fragment["text"]
        assert isinstance(fragment["relevance_score"], float)
