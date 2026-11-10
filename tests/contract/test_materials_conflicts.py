"""Contract test for GET /materials/conflicts and POST /materials/conflicts/{id}/review
— FR-022a."""

from __future__ import annotations

import pytest

from tests.conftest import MATERIALS_FIXTURES_DIR


def _activate_conflicting_pair(app_client, course_id: str):
    with open(MATERIALS_FIXTURES_DIR / "conflict_a.md", "rb") as fh:
        ra = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": course_id, "activity_configuration_ids": ["act-1"]},
            files={"file": ("conflict_a.md", fh, "text/markdown")},
        )
    with open(MATERIALS_FIXTURES_DIR / "conflict_b.md", "rb") as fh:
        rb = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": course_id, "activity_configuration_ids": ["act-1"]},
            files={"file": ("conflict_b.md", fh, "text/markdown")},
        )
    app_client.post(f"/api/v1/materials/documents/{ra.json()['id']}/activate")
    app_client.post(f"/api/v1/materials/documents/{rb.json()['id']}/activate")
    return ra.json()["id"], rb.json()["id"]


@pytest.mark.contract
def test_conflicts_list_and_review(app_client, seeded_course):
    _activate_conflicting_pair(app_client, seeded_course)

    app_client.post(
        "/api/v1/materials/query",
        json={
            "query_text": "la capital de Testlandia",
            "course_id": seeded_course,
            "activity_configuration_id": "act-1",
            "max_fragments": 5,
            "time_budget_ms": 5000,
        },
    )

    r = app_client.get("/api/v1/materials/conflicts")
    assert r.status_code == 200
    conflicts = r.json()
    assert len(conflicts) == 1
    assert conflicts[0]["review_status"] == "pending_review"

    r2 = app_client.post(f"/api/v1/materials/conflicts/{conflicts[0]['id']}/review")
    assert r2.status_code == 200
    assert r2.json()["review_status"] == "reviewed"

    r3 = app_client.get("/api/v1/materials/conflicts")
    assert r3.json() == []
