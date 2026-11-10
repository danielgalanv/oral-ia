"""US7 integration test: after a rebuild, existing Evidence/GroundingVerificationResult/
MaterialConflictRecord references remain valid — no orphaned fragment ids (FR-016a)."""

from __future__ import annotations

import pytest

from tests.conftest import MATERIALS_FIXTURES_DIR


@pytest.mark.integration
def test_fragment_ids_preserved_across_rebuild(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course, "activity_configuration_ids": ["act-1"]},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    doc_id = r.json()["id"]
    app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")

    before = app_client.post(
        "/api/v1/materials/query",
        json={
            "query_text": "documento de prueba",
            "course_id": seeded_course,
            "activity_configuration_id": "act-1",
            "max_fragments": 5,
            "time_budget_ms": 5000,
        },
    ).json()
    before_ids = {f["fragment_id"] for f in before["fragments"]}
    assert before_ids

    r_rebuild = app_client.post("/api/v1/materials/index/rebuild")
    assert r_rebuild.status_code == 200
    assert r_rebuild.json()["index_version"] != before["index_version"]

    after = app_client.post(
        "/api/v1/materials/query",
        json={
            "query_text": "documento de prueba",
            "course_id": seeded_course,
            "activity_configuration_id": "act-1",
            "max_fragments": 5,
            "time_budget_ms": 5000,
        },
    ).json()
    after_ids = {f["fragment_id"] for f in after["fragments"]}
    assert after_ids == before_ids
