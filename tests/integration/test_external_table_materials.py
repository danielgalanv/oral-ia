"""Explicit technical rehearsal of frozen external fictitious teacher drafts.

Never publish proposed teaching units or instructor guides; no normal/demo DB use.
"""

import hashlib
import json
import os
from pathlib import Path

import pytest

from oralia.infrastructure.db import models
from oralia.infrastructure.documents.docx_extractor import DocxExtractor
from oralia.infrastructure.documents.pdf_extractor import PdfExtractor
from oralia.infrastructure.documents.pptx_extractor import PptxExtractor
from tests.table_fixtures import NOTE

BASE = Path(__file__).parents[2] / "specs/010-guided-dialogue"
INPUTS = json.loads((BASE / "table-extraction-inputs.json").read_text(encoding="utf-8"))
MIMES = {
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".pdf": "application/pdf",
}


@pytest.mark.skipif(not os.environ.get("ORALIA_TABLE_REHEARSAL"), reason="explicit external draft rehearsal")
@pytest.mark.parametrize("item", INPUTS, ids=lambda i: i["filename"])
def test_frozen_external_draft_ingestion_and_locations(app_client, seeded_course, item):
    path = Path(item["snapshot"])
    payload = path.read_bytes()
    assert hashlib.sha256(payload).hexdigest() == item["sha256"]
    extractor = {".docx": DocxExtractor, ".pptx": PptxExtractor, ".pdf": PdfExtractor}[item["suffix"]]()
    blocks = extractor.extract(str(path))
    assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
    native_table_count = 0
    if item["suffix"] == ".docx":
        from docx import Document

        native_table_count = len(Document(str(path))._element.body.xpath(".//w:tbl"))
    elif item["suffix"] == ".pptx":
        from pptx import Presentation

        native_table_count = sum(
            len(slide._element.xpath(".//a:tbl")) for slide in Presentation(str(path)).slides
        )
    report = {
        "filename": item["filename"],
        "sha256": item["sha256"],
        "technical_only": True,
        "human_approved": False,
        "conversation_tested": False,
        "block_count": len(blocks),
        "table_cell_locations": [b.location_ref for b in blocks if "tabla" in b.location_ref],
    }
    response = app_client.post(
        "/api/v1/materials/documents",
        data={"course_id": seeded_course, "activity_configuration_ids": ["external-draft-only"]},
        files={"file": (item["filename"], payload, MIMES[item["suffix"]])},
    )
    assert response.status_code == 201, response.text
    document = response.json()
    assert document["status"] == "processed"
    with app_client.__db_sessionmaker__() as db:
        fragments = (
            db.query(models.MaterialFragment)
            .filter_by(document_id=document["id"])
            .order_by(models.MaterialFragment.sequence_index)
            .all()
        )
        report["fragment_count"] = len(fragments)
        assert fragments and all(f.document_version == 1 and f.course_id == seeded_course for f in fragments)
        assert NOTE not in "\n".join(f.text for f in fragments)
        if native_table_count:
            assert report["table_cell_locations"]
            assert any("tabla" in f.location_ref for f in fragments)
        if item["suffix"] == ".pptx":
            table = [b for b in blocks if "diapositiva 12, tabla 1" in b.location_ref]
            assert len(table) == 24
            assert any(b.text.startswith("007") and "fila 3, columna 1" in b.location_ref for b in table)
            assert any(b.text.startswith("1000") and "fila 4, columna 1" in b.location_ref for b in table)
            assert any(b.text.startswith("3,5") and "fila 5, columna 1" in b.location_ref for b in table)
    assert app_client.post(f"/api/v1/materials/documents/{document['id']}/activate").status_code == 200
    query = app_client.post(
        "/api/v1/materials/query",
        json={
            "query_text": "casos cantidad formato rango aceptación",
            "course_id": seeded_course,
            "activity_configuration_id": "external-draft-only",
            "max_fragments": 10,
            "time_budget_ms": 5000,
        },
    )
    assert query.status_code == 200 and query.json()["fragments"]
    assert all(f["document_id"] == document["id"] and f["location_ref"] for f in query.json()["fragments"])
    report["native_table_count"] = native_table_count
    with app_client.__db_sessionmaker__() as db:
        for fragment in query.json()["fragments"]:
            fragment_id = fragment.get("fragment_id") or fragment.get("id")
            assert fragment_id
            stored = db.get(models.MaterialFragment, fragment_id)
            assert stored.document_id == document["id"] and stored.location_ref == fragment["location_ref"]
            assert stored.text == fragment["text"]
    report["query_fragments"] = [
        {"id": f["fragment_id"] if "fragment_id" in f else f.get("id"), "location_ref": f["location_ref"]}
        for f in query.json()["fragments"]
    ]
    assert app_client.post(f"/api/v1/materials/documents/{document['id']}/deactivate").status_code == 200
    out = Path(os.environ["ORALIA_TABLE_REHEARSAL"])
    out.mkdir(parents=True, exist_ok=True)
    target = out / (item["filename"] + ".json")
    assert not target.exists()
    report["outcome"] = "passed"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
