"""US7 failure test (Escenario F): a corrupt or unextractable file ends in
error/not_processable with an actionable message, and the existing index keeps serving
queries normally (FR-027)."""

from __future__ import annotations

import pytest

from tests.conftest import MATERIALS_FIXTURES_DIR


def _query(app_client, course_id: str):
    return app_client.post(
        "/api/v1/materials/query",
        json={
            "query_text": "documento de prueba",
            "course_id": course_id,
            "activity_configuration_id": "act-1",
            "max_fragments": 5,
            "time_budget_ms": 5000,
        },
    )


@pytest.mark.failure
def test_failed_upload_does_not_affect_existing_index(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course, "activity_configuration_ids": ["act-1"]},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    doc_id = r.json()["id"]
    app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")

    before = _query(app_client, seeded_course).json()
    assert before["fragments"]

    with open(MATERIALS_FIXTURES_DIR / "corrupt.pdf", "rb") as fh:
        r2 = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course},
            files={"file": ("corrupt.pdf", fh, "application/pdf")},
        )
    assert r2.json()["status"] == "error"
    assert r2.json()["error_detail"]

    after = _query(app_client, seeded_course).json()
    assert [f["fragment_id"] for f in after["fragments"]] == [f["fragment_id"] for f in before["fragments"]]
