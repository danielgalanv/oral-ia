"""US1 failure test: activation rejected when a document is not yet processed or is in
error (FR-011)."""

from __future__ import annotations

import pytest

from tests.conftest import MATERIALS_FIXTURES_DIR


@pytest.mark.failure
def test_activation_rejected_for_error_status(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "corrupt.pdf", "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course},
            files={"file": ("corrupt.pdf", fh, "application/pdf")},
        )
    assert r.status_code == 201
    body = r.json()
    assert body["status"] == "error"
    assert body["error_detail"]

    r2 = app_client.post(f"/api/v1/materials/documents/{body['id']}/activate")
    assert r2.status_code == 409


@pytest.mark.failure
def test_activation_rejected_for_pending_status(app_client, seeded_course):
    # A document that is still "pending_duplicate_review" MUST NOT be activatable either.
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        dup = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    token = dup.json()["conflict_token"]
    r = app_client.post(f"/api/v1/materials/documents/{token}/activate")
    assert r.status_code == 409
