"""US4 integration test: a query for activity A never returns fragments belonging to
activity B (FR-019)."""

from __future__ import annotations

import pytest


@pytest.mark.integration
def test_query_for_activity_a_never_returns_activity_b_fragments(app_client, seeded_course):
    import io

    content_a = b"El contenido exclusivo de la actividad A menciona zorros voladores."
    content_b = b"El contenido exclusivo de la actividad B menciona tortugas cantoras."

    ra = app_client.post(
        "/api/v1/materials/documents",
        data={"course_id": seeded_course, "activity_configuration_ids": ["act-a"]},
        files={"file": ("doc_a.txt", io.BytesIO(content_a), "text/plain")},
    )
    rb = app_client.post(
        "/api/v1/materials/documents",
        data={"course_id": seeded_course, "activity_configuration_ids": ["act-b"]},
        files={"file": ("doc_b.txt", io.BytesIO(content_b), "text/plain")},
    )
    app_client.post(f"/api/v1/materials/documents/{ra.json()['id']}/activate")
    app_client.post(f"/api/v1/materials/documents/{rb.json()['id']}/activate")

    r = app_client.post(
        "/api/v1/materials/query",
        json={
            "query_text": "contenido exclusivo menciona",
            "course_id": seeded_course,
            "activity_configuration_id": "act-a",
            "max_fragments": 10,
            "time_budget_ms": 5000,
        },
    )
    assert r.status_code == 200
    document_ids = {f["document_id"] for f in r.json()["fragments"]}
    assert ra.json()["id"] in document_ids
    assert rb.json()["id"] not in document_ids
