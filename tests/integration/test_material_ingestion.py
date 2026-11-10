"""US1 integration test: full upload → processed → activate flow for every supported
format (FR-001..FR-011)."""

from __future__ import annotations

import pytest

from tests.conftest import MATERIALS_FIXTURES_DIR

FIXTURES_BY_MIME = [
    ("sample.pdf", "application/pdf"),
    ("sample.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    ("sample.pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation"),
    ("sample.txt", "text/plain"),
    ("sample.md", "text/markdown"),
]


@pytest.mark.integration
@pytest.mark.parametrize("filename,mime_type", FIXTURES_BY_MIME)
def test_upload_process_activate_for_every_format(app_client, seeded_course, filename, mime_type):
    with open(MATERIALS_FIXTURES_DIR / filename, "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course},
            files={"file": (filename, fh, mime_type)},
        )
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["status"] == "processed"

    r_activate = app_client.post(f"/api/v1/materials/documents/{body['id']}/activate")
    assert r_activate.status_code == 200
    assert r_activate.json()["status"] == "active"
