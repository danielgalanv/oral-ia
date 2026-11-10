"""A separate teacher-slide manifest cannot silently admit or rewrite pages."""

import hashlib
import json

import pytest

from oralia.course_dialogue import full_corpus
from oralia.course_dialogue.document_evidence import build_units, retrieve_units
from scripts import compare_course_chat


def test_full_teacher_catalog_respects_page_decisions_and_hashes(tmp_path, monkeypatch):
    source = tmp_path / "teacher.pdf"
    source.write_bytes(b"authorized teacher PDF fixture")
    texts = ["Título\nContenido docente.", "Duplicado\nContenido docente.", "Esquema\n"]
    decisions = ["include_lab", "exclude", "quarantine"]
    manifest = {
        "scope": "three_authorized_teacher_pdfs_lab_only",
        "entries": [
            {
                "page_id": f"teacher:{index}",
                "document_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
                "decision": decision,
            }
            for index, (text, decision) in enumerate(zip(texts, decisions, strict=True), 1)
        ],
    }
    manifest_path = tmp_path / "decisions.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    monkeypatch.setattr(full_corpus, "SELECTION", {"teacher": ("teacher.pdf", (1,))})

    class PDF:
        def __init__(self):
            self.pages = [
                type("Page", (), {"extract_text": lambda _self, value=text: value})() for text in texts
            ]

        def __enter__(self):
            return self

        def __exit__(self, *_):
            return False

    monkeypatch.setattr(full_corpus.pdfplumber, "open", lambda _path: PDF())
    result = full_corpus.load_full_teacher_catalog(tmp_path, manifest_path)
    assert [page["id"] for page in result] == ["teacher:1"]
    assert result[0]["teacher_review"] == "pending"
    manifest["entries"][0]["text_sha256"] = "changed"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="extraction changed"):
        full_corpus.load_full_teacher_catalog(tmp_path, manifest_path)


def test_runner_passes_table_enriched_catalog_to_request(monkeypatch):
    base = {
        "id": "teacher:1",
        "filename": "teacher.pdf",
        "original_sha256": "original",
        "version": 1,
        "page": 1,
        "text": "Tabla de plazos\n",
        "text_sha256": hashlib.sha256(b"Tabla de plazos\n").hexdigest(),
    }
    enriched = {
        **base,
        "tables": [{"bbox": (0, 0, 100, 100), "rows": [["plazo", "60 s"]]}],
    }
    units = build_units([enriched])
    monkeypatch.setattr(compare_course_chat, "load_full_teacher_catalog", lambda: [base])
    monkeypatch.setattr(compare_course_chat, "load_authorized_units", lambda **_kwargs: ([enriched], units))
    pages, catalog, prepared = compare_course_chat.prepare_catalog(True, True)
    assert pages is catalog and catalog[0]["tables"] == enriched["tables"]
    assert retrieve_units(prepared, catalog, "plazo").units == tuple(units)
