"""Contract test for POST /api/v1/materials/documents — contracts/material-retriever-
agent.md, FR-001..FR-005a."""

from __future__ import annotations

import pytest

from tests.conftest import MATERIALS_FIXTURES_DIR


@pytest.mark.contract
def test_upload_returns_201_pending_then_processed(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    assert r.status_code == 201
    body = r.json()
    assert body["status"] == "processed"
    assert body["content_hash"]
    assert body["mime_type"] == "application/pdf"


@pytest.mark.contract
def test_duplicate_upload_returns_409_with_conflict_token(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )

    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        r2 = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    assert r2.status_code == 409
    body = r2.json()
    assert body["detail"] == "possible duplicate"
    assert body["existing_document_id"]
    assert body["conflict_token"]
