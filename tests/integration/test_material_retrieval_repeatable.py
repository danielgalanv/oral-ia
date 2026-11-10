"""US2 integration test: identical query + config + index version returns the same
fragments in the same order (FR-020)."""

from __future__ import annotations

import pytest

from tests.conftest import MATERIALS_FIXTURES_DIR


@pytest.mark.integration
def test_repeated_identical_query_returns_same_order(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "sample.docx", "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course, "activity_configuration_ids": ["act-1"]},
            files={
                "file": (
                    "sample.docx",
                    fh,
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            },
        )
    doc_id = r.json()["id"]
    app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")

    payload = {
        "query_text": "parrafo con contenido de prueba",
        "course_id": seeded_course,
        "activity_configuration_id": "act-1",
        "max_fragments": 5,
        "time_budget_ms": 5000,
    }
    r1 = app_client.post("/api/v1/materials/query", json=payload)
    r2 = app_client.post("/api/v1/materials/query", json=payload)

    assert r1.status_code == r2.status_code == 200
    ids1 = [f["fragment_id"] for f in r1.json()["fragments"]]
    ids2 = [f["fragment_id"] for f in r2.json()["fragments"]]
    assert ids1 == ids2
    assert ids1  # sanity: the fixture must actually be retrievable
    assert r1.json()["index_version"] == r2.json()["index_version"]
