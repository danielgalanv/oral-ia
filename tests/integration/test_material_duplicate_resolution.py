"""US1 integration test: uploading a duplicate hash returns 409, and both
link_existing/proceed_new resolutions behave per FR-005a."""

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


@pytest.mark.integration
def test_link_existing_never_processed_or_indexed_separately(app_client, seeded_course):
    _upload(app_client, seeded_course)
    dup = _upload(app_client, seeded_course)
    assert dup.status_code == 409
    token = dup.json()["conflict_token"]

    r = app_client.post(
        f"/api/v1/materials/documents/{token}/duplicate-resolution", json={"resolution": "link_existing"}
    )
    assert r.status_code == 200
    assert r.json()["status"] == "not_processable"

    # The linked (pending) document is not itself activatable — it is not a real document.
    r_activate = app_client.post(f"/api/v1/materials/documents/{token}/activate")
    assert r_activate.status_code == 409


@pytest.mark.integration
def test_proceed_new_creates_independently_activatable_document(app_client, seeded_course):
    first = _upload(app_client, seeded_course)
    dup = _upload(app_client, seeded_course)
    token = dup.json()["conflict_token"]

    r = app_client.post(
        f"/api/v1/materials/documents/{token}/duplicate-resolution", json={"resolution": "proceed_new"}
    )
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "processed"
    assert body["id"] != first.json()["id"]

    r_activate = app_client.post(f"/api/v1/materials/documents/{body['id']}/activate")
    assert r_activate.status_code == 200
