"""Contract test: a query requesting an out-of-scope activity/course returns empty
fragments, never an error leaking existence of other materials (FR-019, FR-026)."""

from __future__ import annotations

import pytest

from tests.conftest import MATERIALS_FIXTURES_DIR


@pytest.mark.contract
def test_out_of_scope_activity_returns_empty_fragments_not_an_error(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course, "activity_configuration_ids": ["act-authorized"]},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    doc_id = r.json()["id"]
    app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")

    r2 = app_client.post(
        "/api/v1/materials/query",
        json={
            "query_text": "documento de prueba",
            "course_id": seeded_course,
            "activity_configuration_id": "act-NOT-authorized",
            "max_fragments": 5,
            "time_budget_ms": 5000,
        },
    )
    assert r2.status_code == 200
    assert r2.json()["fragments"] == []
