"""US5 integration test: a retired version's fragments remain intact and queryable as a
historical reference — replacement never deletes them (FR-015)."""

from __future__ import annotations

import pytest

from oralia.infrastructure.db import models
from tests.conftest import MATERIALS_FIXTURES_DIR


@pytest.mark.integration
def test_retired_version_fragments_remain_intact_after_replacement(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        r1 = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    doc_id = r1.json()["id"]
    app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")

    Session = app_client.__db_sessionmaker__
    db = Session()
    original_fragments = db.query(models.MaterialFragment).filter_by(document_id=doc_id).all()
    original_texts = sorted(f.text for f in original_fragments)
    db.close()
    assert original_texts

    with open(MATERIALS_FIXTURES_DIR / "sample_v2.pdf", "rb") as fh:
        app_client.post(
            f"/api/v1/materials/documents/{doc_id}/versions",
            files={"file": ("sample_v2.pdf", fh, "application/pdf")},
        )

    db = Session()
    document = db.get(models.MaterialDocument, doc_id)
    assert document.retired_at is not None
    surviving_fragments = db.query(models.MaterialFragment).filter_by(document_id=doc_id).all()
    surviving_texts = sorted(f.text for f in surviving_fragments)
    db.close()
    assert surviving_texts == original_texts
