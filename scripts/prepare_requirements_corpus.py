"""Reproducible document extraction only; no models, vectors, or source mutation."""

import hashlib
import json
import re
from pathlib import Path

import pdfplumber
from lxml import html

from oralia.infrastructure.documents.pdf_extractor import PdfExtractor
from oralia.infrastructure.documents.pptx_extractor import PptxExtractor

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "materiales/docente/piloto-requisitos/paquete-v1"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_new(path, data):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)


def main():
    output = PACKAGE / "extracciones"
    output.mkdir(exist_ok=True)
    documents = []
    definitions = [
        (
            "docente-requisitos",
            "5 - Requisitos.pdf",
            "Docencia UPM; material adaptado de Ian Sommerville",
            "Curso 22-23; diapositivas con fecha 30/10/2014; adaptación sin edición declarada",
            "software",
        ),
        (
            "docente-procedimiento",
            "6 - Procedimiento requisitos.pdf",
            "Docencia UPM; procedimiento atribuido en p.2 a Junta de Andalucía",
            "Curso 22-23; sin revisión formal declarada",
            "software",
        ),
        (
            "nasa-seh",
            "nasa-handbook.pdf",
            "NASA; Steven R. Hirshorn (editor)",
            "NASA/SP-2016-6105 Rev 2; publicación NTRS 17/02/2017",
            "sistemas",
        ),
        (
            "sommerville",
            "Ch4 Req Eng.pptx",
            "Ian Sommerville",
            "Software Engineering 10; Chapter 4; 30/10/2014",
            "software",
        ),
    ]
    decisions = json.loads(
        (ROOT / "specs/012-conversational-course-study/evidence/teacher-pdf-decisions.json").read_text(
            encoding="utf-8"
        )
    )
    old = {r["page_id"]: r for r in decisions["entries"]}
    for doc_id, name, author, edition, domain in definitions:
        source = PACKAGE / "originales" / name
        source_hash = digest(source.read_bytes())
        extractor = PptxExtractor() if source.suffix == ".pptx" else PdfExtractor()
        blocks = extractor.extract(str(source))
        pages = {}
        for block in blocks:
            number = int(re.search(r"\d+", block.location_ref).group())
            pages.setdefault(number, []).append({"location": block.location_ref, "text": block.text})
        rows = []
        with pdfplumber.open(source) if source.suffix == ".pdf" else _null() as pdf:
            for number, parts in pages.items():
                raw = "\n\n".join(p["text"] for p in parts)
                row = dict(
                    id=f"{doc_id}:{number}",
                    page=number,
                    section=raw.splitlines()[0],
                    raw_text=raw,
                    text=raw,
                    parts=parts,
                    status="cuarentena",
                    reason="Pendiente de contraste visual en este paquete",
                    derivation="extracción mecánica; sin traducción",
                    source_sha256=source_hash,
                    text_sha256=digest(raw.encode()),
                )
                if doc_id.startswith("docente"):
                    key = "requirements" if doc_id == "docente-requisitos" else "procedure"
                    previous = old.get(f"{key}:{number}")
                    if previous:
                        if previous["document_sha256"] != source_hash:
                            raise ValueError("Changed teacher original")
                        row["historical_decision"] = previous
                if doc_id == "nasa-seh" and number in [207, 208, 209, 210, 211, 213]:
                    page = pdf.pages[number - 1]
                    # Reading-order derivative; preserve raw interleaved two-column extraction.
                    row["text"] = "\n\n".join(
                        page.crop(box).extract_text() or ""
                        for box in [
                            (0, 45, page.width / 2, page.height - 32),
                            (page.width / 2, 45, page.width, page.height - 32),
                        ]
                    )
                    row["derivation"] = (
                        "normalización de orden por dos columnas; raw_text conservado; sin traducción"
                    )
                    row["text_sha256"] = digest(row["text"].encode())
                rows.append(row)
        write_new(output / f"{doc_id}.json", rows)
        documents.append(
            dict(
                id=doc_id,
                filename=name,
                original=f"originales/{name}",
                author=author,
                edition=edition,
                domain=domain,
                sha256=source_hash,
                extraction=f"extracciones/{doc_id}.json",
                extracted_pages=len(rows),
                status="revision_tecnica_parcial",
                access_date="2026-10-27",
                teacher_acceptance="pendiente",
            )
        )
    capture = PACKAGE / "capturas/nasa-swe055.html"
    tree = html.fromstring(capture.read_bytes())
    content = tree.get_element_by_id("main-content")
    for element in content.xpath(".//script | .//style"):
        element.drop_tree()
    sections = []
    current = None
    # Preserve DOM text, list and cell boundaries; no navigation or hidden panel copies.
    for element in content.iter():
        if element.tag == "h1":
            current = {"section": " ".join(element.text_content().split()), "elements": []}
            sections.append(current)
        elif current is not None and element.tag in {"p", "li", "tr", "h2", "h3"}:
            if element.tag == "p" and any(p.tag in {"li", "tr"} for p in element.iterancestors()):
                continue
            text = (
                " | ".join(" ".join(c.text_content().split()) for c in element if c.tag in {"th", "td"})
                if element.tag == "tr"
                else " ".join(element.text_content().split())
            )
            if text:
                current["elements"].append({"tag": element.tag, "text": text})
    rows = []
    for i, section in enumerate(sections, 1):
        text = section["section"] + "\n" + "\n".join(p["text"] for p in section["elements"])
        rows.append(
            dict(
                id=f"nasa-swe055:{i}",
                page=i,
                section=section["section"],
                text=text,
                raw_text=text,
                parts=section["elements"],
                status="cuarentena",
                reason="Pendiente de contraste con HTML original",
                derivation="HTML por encabezados y elementos; sin traducción; page es ordinal de sección",
                source_sha256=digest(capture.read_bytes()),
                text_sha256=digest(text.encode()),
            )
        )
    write_new(output / "nasa-swe055.json", rows)
    documents.append(
        dict(
            id="nasa-swe055",
            filename="SWE-055 — Requirements Validation",
            original="capturas/nasa-swe055.html",
            author="NASA Software Engineering Handbook",
            edition="Ver D; SWE-055, NPR 7150.2 D §4.1.7; captura 27/10/2026",
            domain="software NASA",
            sha256=digest(capture.read_bytes()),
            extraction="extracciones/nasa-swe055.json",
            extracted_pages=len(rows),
            status="revision_tecnica_parcial",
            access_date="2026-10-27",
            teacher_acceptance="pendiente",
        )
    )
    write_new(
        PACKAGE / "manifest-initial.json",
        dict(package_id="oralia-requisitos-20261027-v1", documents=documents),
    )
    print([(d["id"], d["extracted_pages"]) for d in documents])


class _null:
    def __enter__(self):
        return None

    def __exit__(self, *args):
        return False


if __name__ == "__main__":
    main()
