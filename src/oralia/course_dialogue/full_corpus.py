"""Explicitly reviewed, opt-in teacher-PDF catalog for laboratory diagnosis only."""

import hashlib
import json
from pathlib import Path

import pdfplumber

from oralia.course_dialogue.corpus import SELECTION, SOURCE_ROOT

DECISIONS = (
    Path(__file__).resolve().parents[3]
    / "specs/012-conversational-course-study/evidence/teacher-pdf-decisions.json"
)


def load_full_teacher_catalog(source_root=SOURCE_ROOT, decisions_path=DECISIONS):
    manifest = json.loads(decisions_path.read_text(encoding="utf-8"))
    if manifest["scope"] != "three_authorized_teacher_pdfs_lab_only":
        raise ValueError("unexpected teacher catalog scope")
    decisions = {row["page_id"]: row for row in manifest["entries"]}
    if len(decisions) != len(manifest["entries"]):
        raise ValueError("duplicate teacher page decision")
    result = []
    seen = set()
    for key, (filename, _selected) in SELECTION.items():
        path = source_root / filename
        original_sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
        with pdfplumber.open(path) as pdf:
            for page_number, pdf_page in enumerate(pdf.pages, 1):
                page_id = f"{key}:{page_number}"
                seen.add(page_id)
                decision = decisions.get(page_id)
                if not decision or decision["document_sha256"] != original_sha256:
                    raise ValueError("missing decision or changed teacher PDF")
                text = pdf_page.extract_text() or ""
                if not text.strip() or hashlib.sha256(text.encode()).hexdigest() != decision["text_sha256"]:
                    raise ValueError("teacher page extraction changed")
                if decision["decision"] in {"exclude", "quarantine"}:
                    continue
                if decision["decision"] != "include_lab":
                    raise ValueError("unreviewed teacher page")
                result.append(
                    {
                        "id": page_id,
                        "filename": filename,
                        "original_sha256": original_sha256,
                        "version": 1,
                        "page": page_number,
                        "text": text,
                        "text_sha256": decision["text_sha256"],
                        "derivation": "mechanical_text_extraction",
                        "teacher_review": "pending",
                        "corpus_scope": "three_authorized_teacher_pdfs_lab_reviewed_text",
                    }
                )
    if seen != set(decisions):
        raise ValueError("decision manifest does not match three teacher PDFs")
    return result
