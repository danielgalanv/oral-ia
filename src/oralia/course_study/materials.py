"""Mechanical page selection; originals stay untouched, no authored teaching units."""

import hashlib
import io
from pathlib import Path

import pypdfium2 as pdfium

DEFAULT_SOURCE = Path(
    "C:\Users\<usuario>\\OneDrive - Universidad Politécnica de Madrid\\Docencia\\Ingeniería "
    "del software\\22-23\\Traspis\\6 - Procedimiento requisitos.pdf"
)


def selected_material(source=DEFAULT_SOURCE):
    source = Path(source)
    raw = source.read_bytes()
    reader = pdfium.PdfDocument(raw)
    if len(reader) != 14:
        raise ValueError("El procedimiento esperado tiene14páginas; revise versión antes de preparar.")
    writer = pdfium.PdfDocument.new()
    output = io.BytesIO()
    try:
        writer.import_pages(reader, [9, 10, 11])
        writer.save(output)
        selected = output.getvalue()
    finally:
        writer.close()
        reader.close()
    return selected, {
        "original_name": source.name,
        "original_sha256": hashlib.sha256(raw).hexdigest(),
        "derived_name": "Procedimiento-requisitos-original-p10-12.pdf",
        "derived_sha256": hashlib.sha256(selected).hexdigest(),
        "pages": {"1": 10, "2": 11, "3": 12},
        "transformation": "mechanical page selection only; no authored content or teacher review inferred",
    }
