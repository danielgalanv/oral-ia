"""US6 integration test (Escenario D): two contradictory active materials produce both
evidences plus a flagged conflict on a related query (FR-022)."""

from __future__ import annotations

import pytest

from tests.conftest import MATERIALS_FIXTURES_DIR


@pytest.mark.integration
def test_query_over_contradictory_materials_returns_both_evidences_and_conflict(app_client, seeded_course):
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

    r = app_client.post(
        "/api/v1/materials/query",
        json={
            "query_text": "la capital de Testlandia",
            "course_id": seeded_course,
            "activity_configuration_id": "act-1",
            "max_fragments": 5,
            "time_budget_ms": 5000,
        },
    )
    body = r.json()
    document_ids = {f["document_id"] for f in body["fragments"]}
    assert ra.json()["id"] in document_ids
    assert rb.json()["id"] in document_ids
    assert body["conflicts"]
    assert set(body["conflicts"][0]["document_ids"]) == {ra.json()["id"], rb.json()["id"]}
