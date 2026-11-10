"""Contract test for POST .../duplicate-resolution — FR-005a."""

from __future__ import annotations

import pytest

from tests.conftest import MATERIALS_FIXTURES_DIR


def _upload(app_client, course_id: str):
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        return app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": course_id},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )


@pytest.mark.contract
def test_link_existing_resolution(app_client, seeded_course):
    first = _upload(app_client, seeded_course)
    dup = _upload(app_client, seeded_course)
    token = dup.json()["conflict_token"]

    r = app_client.post(
        f"/api/v1/materials/documents/{token}/duplicate-resolution",
        json={"resolution": "link_existing"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["duplicate_of_document_id"] == first.json()["id"]
    assert body["status"] == "not_processable"


@pytest.mark.contract
def test_proceed_new_resolution_processes_as_distinct_document(app_client, seeded_course):
    first = _upload(app_client, seeded_course)
    dup = _upload(app_client, seeded_course)
    token = dup.json()["conflict_token"]

    r = app_client.post(
        f"/api/v1/materials/documents/{token}/duplicate-resolution",
        json={"resolution": "proceed_new"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["id"] != first.json()["id"]
    assert body["status"] == "processed"
    assert body["duplicate_of_document_id"] is None
