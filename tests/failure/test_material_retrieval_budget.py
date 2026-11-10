"""US2 failure test: time_budget_ms exhausted returns partial results with an explicit
warning, not a timeout status (Edge Case)."""

from __future__ import annotations

import pytest

from tests.conftest import MATERIALS_FIXTURES_DIR


@pytest.mark.failure
def test_negative_time_budget_returns_ok_with_warning_not_timeout(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course, "activity_configuration_ids": ["act-1"]},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    doc_id = r.json()["id"]
    app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")

    r2 = app_client.post(
        "/api/v1/materials/query",
        json={
            "query_text": "documento de prueba",
            "course_id": seeded_course,
            "activity_configuration_id": "act-1",
            "max_fragments": 5,
            # Negative, not zero: elapsed time is never negative, so this deterministically
            # exceeds budget regardless of clock resolution — avoids a real flake where
            # time_budget_ms=0 could occasionally tie with an extremely fast elapsed time.
            "time_budget_ms": -1,
        },
    )
    assert r2.status_code == 200
    body = r2.json()
    assert any("presupuesto temporal agotado" in w for w in body["warnings"])
