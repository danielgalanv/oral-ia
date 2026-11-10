"""Build paquete-v3 = paquete-v2 + two public web pages captured once (no live fetching in class).

    python scripts/build_package_v3.py --captures <folder with the two downloaded .html files>

Never touches paquete-v2. Refuses to overwrite an existing paquete-v3. The new pages are extracted literally from the
captured HTML (no translation), assistant-reviewed against the HTML, with teacher acceptance still pending.
"""

import argparse
import hashlib
import json
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "materiales/docente/piloto-requisitos/paquete-v2"
V3 = ROOT / "materiales/docente/piloto-requisitos/paquete-v3"
ACCESS_DATE = "2026-11-07"
BLOCKS = {"p", "li", "h1", "h2", "h3", "blockquote"}

SOURCES = {
    "swbook-ieee": dict(
        capture="software-engineering-book-requirements-standard.html",
        filename="The IEEE standard for requirements documents",
        author="Ian Sommerville; Software Engineering 10th edition, companion website",
        edition="Suplemento web de la 10.ª edición; describe IEEE/ANSI 830-1998, no afirma ser la última edición del estándar; captura 07/11/2026",
        origin="https://software-engineering-book.com/web/requirements-standard/",
        conditions="Página pública del sitio del libro, captura local para consulta; sin licencia específica identificada en la página; no redistribución pública del paquete",
        domain="ingeniería de requisitos",
    ),
    "stse-requirements": dict(
        capture="st-andrews-stse-requirements-and-design.html",
        filename="Requirements and Design (Handbook of Socio-Technical Engineering)",
        author="Ian Sommerville, University of St Andrews",
        edition="Capítulo web del Socio-technical Systems Engineering Handbook; captura 07/11/2026",
        origin="https://archive.cs.st-andrews.ac.uk/STSE-Handbook/RequirementsandDesign/",
        conditions="Página pública del archivo de la Universidad de St Andrews, captura local para consulta; sin licencia específica identificada en la página; no redistribución pública del paquete",
        domain="ingeniería de requisitos",
    ),
}


class Extractor(HTMLParser):
    """Text of the content blocks (headings, paragraphs, list items) in document order."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks, self._tag, self._buf, self._skip = [], None, [], 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self._skip += 1
        elif tag in BLOCKS:
            self._close()  # old-style HTML leaves <p> and <li> unclosed: a new block ends the previous one
            self._tag, self._buf = tag, []
        elif tag == "br" and self._tag:
            self._buf.append(" ")

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self._skip = max(0, self._skip - 1)
        elif tag == self._tag:
            self._close()

    def _close(self):
        if self._tag:
            text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
            if text:
                self.blocks.append((self._tag, text))
        self._tag = None

    def handle_data(self, data):
        if self._skip:
            return
        if self._tag is None and data.strip():
            self._tag, self._buf = "p", []  # loose text between blocks (old-style pages) is a paragraph
        if self._tag:
            self._buf.append(data)


def blocks_of(path):
    parser = Extractor()
    parser.feed(path.read_text(encoding="utf8", errors="replace"))
    return parser.blocks


def digest(data):
    return hashlib.sha256(data).hexdigest()


def row(doc_id, number, section, parts, source_sha, derivation, reason):
    text = "\n".join(t for _, t in parts)
    return dict(
        id=f"{doc_id}:{number}",
        page=number,
        section=section,
        text=text,
        raw_text=text,
        parts=[dict(tag=tag, text=t) for tag, t in parts],
        status="disponible",
        reason=reason,
        derivation=derivation,
        source_sha256=source_sha,
        text_sha256=digest(text.encode()),
        previous_status=None,
        qa_state="revisado_html_asistente",
    )


def ieee_rows(capture_path, source_sha):
    blocks = blocks_of(capture_path)
    start = next(i for i, (_, t) in enumerate(blocks) if t.startswith("The IEEE standard for requirements documents"))
    end = next((i for i, (_, t) in enumerate(blocks) if t.startswith("Copyright")), len(blocks))
    body = blocks[start:end]
    return [
        row(
            "swbook-ieee", 1, "The IEEE standard for requirements documents", body, source_sha,
            "HTML literal del artículo; sin traducción; page es ordinal",
            "Texto completo del artículo contrastado con el HTML capturado; estructura IEEE/ANSI 830-1998 literal",
        )
    ]


def stse_rows(capture_path, source_sha):
    blocks = blocks_of(capture_path)
    start = next(i for i, (tag, t) in enumerate(blocks) if tag == "h1" and t.startswith("Requirements and Design"))
    rows, section, parts, number = [], "Introducción", [], 0

    def flush():
        nonlocal parts, number
        useful = [(tag, t) for tag, t in parts if tag != "h2" and len(t) > 1]
        if useful and sum(len(t) for _, t in useful) > 80:
            number += 1
            rows.append(
                row(
                    "stse-requirements", number, section, [("h2", section)] + useful, source_sha,
                    "HTML por encabezados; sin traducción; page es ordinal de sección",
                    "Texto de la sección contrastado con el HTML capturado; sin navegación ni anuncios",
                )
            )
        parts = []

    for tag, text in blocks[start + 1 :]:
        if tag == "h2":
            flush()
            section = text
        elif tag in {"p", "li", "blockquote", "h3"}:
            parts.append((tag, text))
    flush()
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--captures", type=Path, required=True)
    args = parser.parse_args()
    if V3.exists():
        raise SystemExit("paquete-v3 ya existe; no se sobrescribe")
    shutil.copytree(V2, V3)
    manifest = json.loads((V2 / "manifest-v2.json").read_text(encoding="utf8"))
    builders = {"swbook-ieee": ieee_rows, "stse-requirements": stse_rows}
    added = []
    for doc_id, meta in SOURCES.items():
        source = args.captures / meta["capture"]
        target = V3 / "capturas" / meta["capture"]
        shutil.copyfile(source, target)
        source_sha = digest(target.read_bytes())
        rows = builders[doc_id](target, source_sha)
        extraction = V3 / "revisado" / f"{doc_id}.json"
        extraction.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf8")
        manifest["documents"].append(
            dict(
                id=doc_id, filename=meta["filename"], original=f"capturas/{meta['capture']}", author=meta["author"],
                edition=meta["edition"], domain=meta["domain"], sha256=source_sha, extraction=f"revisado/{doc_id}.json",
                extracted_pages=len(rows), status="complemento_seleccionado", access_date=ACCESS_DATE,
                teacher_acceptance="pendiente", origin=meta["origin"], conditions=meta["conditions"],
                available=len(rows), quarantine=0, extraction_sha256=digest(extraction.read_bytes()),
                extracted_units=len(rows), qa_states={"revisado_html_asistente": len(rows)},
            )
        )
        added.append((doc_id, [r["id"] for r in rows]))
    ids = dict(added)
    manifest["concepts"] += [
        dict(label="Estructura del documento de requisitos según el estándar IEEE/ANSI 830-1998", passages=ids["swbook-ieee"],
             limits="Describe el estándar histórico 830-1998; no es el estándar vigente ISO/IEC/IEEE 29148 ni la estructura de las diapositivas de Sommerville"),
        dict(label="Elicitación con trabajo de campo y etnografía (STSE)", passages=ids["stse-requirements"],
             limits="Capítulo de un manual de ingeniería sociotécnica; complementa, no sustituye, el material docente de elicitación"),
    ]
    manifest["package_id"] = "oralia-requisitos-20261107-v3"
    manifest["date"] = ACCESS_DATE
    manifest["available"] = manifest["available"] + sum(len(r) for _, r in added)
    manifest["predecessor"] = dict(path="../paquete-v2/manifest-v2.json", sha256=digest((V2 / "manifest-v2.json").read_bytes()))
    manifest["limitations"] = list(manifest["limitations"]) + [
        "v3 añade dos páginas web públicas capturadas una vez (suplemento IEEE 830-1998 del libro de Sommerville y capítulo STSE de St Andrews); revisión del extracto contra el HTML hecha por el asistente, aceptación docente pendiente.",
    ]
    manifest["review"] = "asistente: revisión técnica de extracción, no aprobación docente"
    (V3 / "manifest-v3.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf8")
    for doc_id, page_ids in added:
        print(doc_id, page_ids)


if __name__ == "__main__":
    main()
