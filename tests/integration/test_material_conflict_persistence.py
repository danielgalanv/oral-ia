"""US6 integration test: an unreviewed conflict keeps appearing as conflictive on
subsequent matching queries — no duplicate record created (FR-022b)."""

from __future__ import annotations

import pytest

from tests.conftest import MATERIALS_FIXTURES_DIR


@pytest.mark.integration
def test_unreviewed_conflict_persists_and_is_not_duplicated(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "conflict_a.md", "rb") as fh:
        ra = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course, "activity_configuration_ids": ["act-1"]},
            files={"file": ("conflict_a.md", fh, "text/markdown")},
        )
    with open(MATERIALS_FIXTURES_DIR / "conflict_b.md", "rb") as fh:
        rb = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course, "activity_configuration_ids": ["act-1"]},
            files={"file": ("conflict_b.md", fh, "text/markdown")},
        )
    app_client.post(f"/api/v1/materials/documents/{ra.json()['id']}/activate")
    app_client.post(f"/api/v1/materials/documents/{rb.json()['id']}/activate")

    query = {
        "query_text": "la capital de Testlandia",
        "course_id": seeded_course,
        "activity_configuration_id": "act-1",
        "max_fragments": 5,
        "time_budget_ms": 5000,
    }
    r1 = app_client.post("/api/v1/materials/query", json=query)
    r2 = app_client.post("/api/v1/materials/query", json=query)

    assert r1.json()["conflicts"]
    assert r2.json()["conflicts"]
    assert r1.json()["conflicts"][0]["conflict_record_id"] == r2.json()["conflicts"][0]["conflict_record_id"]

    conflicts = app_client.get("/api/v1/materials/conflicts").json()
    assert len(conflicts) == 1
