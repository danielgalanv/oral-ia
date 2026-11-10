"""Contract test for POST /materials/documents/{id}/versions — FR-014, FR-015."""

from __future__ import annotations

import pytest

from tests.conftest import MATERIALS_FIXTURES_DIR


@pytest.mark.contract
def test_replace_version_returns_201_and_retires_previous(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        r1 = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    doc_id = r1.json()["id"]
    family_id = r1.json()["family_id"]

    with open(MATERIALS_FIXTURES_DIR / "sample_v2.pdf", "rb") as fh:
        r2 = app_client.post(
            f"/api/v1/materials/documents/{doc_id}/versions",
            files={"file": ("sample_v2.pdf", fh, "application/pdf")},
        )
    assert r2.status_code == 201
    body = r2.json()
    assert body["family_id"] == family_id
    assert body["version"] == 2
    assert body["status"] == "processed"

    r3 = app_client.get(f"/api/v1/materials/documents/{doc_id}")
    assert r3.json()["retired_at"] is not None
