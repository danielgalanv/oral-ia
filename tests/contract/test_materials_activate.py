"""Contract test for POST .../activate and .../deactivate — FR-011, FR-013."""

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
def test_activate_processed_document_returns_200(app_client, seeded_course):
    doc_id = _upload(app_client, seeded_course).json()["id"]
    r = app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")
    assert r.status_code == 200
    assert r.json()["status"] == "active"


@pytest.mark.contract
def test_activate_not_processed_document_returns_409(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "blank.pdf", "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course},
            files={"file": ("blank.pdf", fh, "application/pdf")},
        )
    doc_id = r.json()["id"]
    assert r.json()["status"] == "not_processable"

    r2 = app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")
    assert r2.status_code == 409


@pytest.mark.contract
def test_deactivate_is_reversible(app_client, seeded_course):
    doc_id = _upload(app_client, seeded_course).json()["id"]
    app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")

    r_deactivate = app_client.post(f"/api/v1/materials/documents/{doc_id}/deactivate")
    assert r_deactivate.status_code == 200
    assert r_deactivate.json()["status"] == "inactive"

    r_reactivate = app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")
    assert r_reactivate.status_code == 200
    assert r_reactivate.json()["status"] == "active"
