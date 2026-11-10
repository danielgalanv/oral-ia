"""Integration test (closes /speckit-analyze finding F4): the coverage/error summary
for a course's material set matches the actual processing outcomes (FR-010)."""

from __future__ import annotations

import pytest

from tests.conftest import MATERIALS_FIXTURES_DIR


@pytest.mark.integration
def test_coverage_summary_reflects_mixed_processing_outcomes(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        good = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    with open(MATERIALS_FIXTURES_DIR / "blank.pdf", "rb") as fh:
        not_processable = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course},
            files={"file": ("blank.pdf", fh, "application/pdf")},
        )
    with open(MATERIALS_FIXTURES_DIR / "corrupt.pdf", "rb") as fh:
        errored = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course},
            files={"file": ("corrupt.pdf", fh, "application/pdf")},
        )

    assert good.json()["status"] == "processed"
    assert not_processable.json()["status"] == "not_processable"
    assert errored.json()["status"] == "error"

    r = app_client.get(f"/api/v1/materials/documents/{good.json()['id']}")
    coverage = r.json()["course_coverage"]
    assert coverage["total_documents"] == 3
    assert coverage["processed_count"] == 1
    assert coverage["error_count"] == 2
    assert coverage["by_status"] == {"processed": 1, "not_processable": 1, "error": 1}
