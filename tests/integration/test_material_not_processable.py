"""US1 integration test: a no-text PDF is marked not_processable, never silently
indexed (FR-003)."""

from __future__ import annotations

import pytest

from oralia.infrastructure.db import models
from tests.conftest import MATERIALS_FIXTURES_DIR


@pytest.mark.integration
def test_blank_pdf_marked_not_processable_and_never_indexed(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "blank.pdf", "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course},
            files={"file": ("blank.pdf", fh, "application/pdf")},
        )
    assert r.status_code == 201
    body = r.json()
    assert body["status"] == "not_processable"
    assert body["error_detail"]

    Session = app_client.__db_sessionmaker__
    db = Session()
    fragments = db.query(models.MaterialFragment).filter_by(document_id=body["id"]).all()
    db.close()
    assert fragments == []
