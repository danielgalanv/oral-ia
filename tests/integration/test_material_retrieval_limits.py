"""US2 integration test: max_fragments limit is respected."""

from __future__ import annotations

import io

import pytest


@pytest.mark.integration
def test_max_fragments_limit_is_respected(app_client, seeded_course):
    content = "\n".join(f"Linea numero {i} con contenido de prueba distinto." for i in range(10)).encode(
        "utf-8"
    )
    r = app_client.post(
        "/api/v1/materials/documents",
        data={"course_id": seeded_course, "activity_configuration_ids": ["act-1"]},
        files={"file": ("many_lines.txt", io.BytesIO(content), "text/plain")},
    )
    assert r.status_code == 201
    doc_id = r.json()["id"]
    app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")

    r2 = app_client.post(
        "/api/v1/materials/query",
        json={
            "query_text": "contenido de prueba",
            "course_id": seeded_course,
            "activity_configuration_id": "act-1",
            "max_fragments": 3,
            "time_budget_ms": 5000,
        },
    )
    assert r2.status_code == 200
    assert len(r2.json()["fragments"]) == 3
