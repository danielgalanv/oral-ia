"""Native synthetic Office tables; no rendering or response substitutions."""

from pathlib import Path

from docx import Document
from pptx import Presentation
from pptx.util import Inches

HEADERS = ["Entrada de cantidad", "Formato", "Rango", "Efecto esperado"]
ROWS = [
    ["007", "Admitido", "Siete es válido", "Intentar guardar"],
    ["1000", "Admitido", "Fuera de rango", "No guardar"],
    ["3,5", "No admitido", "No se evalúa", "Pedir entero"],
]
NOTE = "SOLUCION_DOCENTE_EN_NOTAS_NO_PUBLICAR_0123456789"


def make_docx(path: Path, *, nested=False, merge=False, depth=0):
    document = Document()
    document.add_heading("Casos de prueba ficticios", 1)
    document.add_paragraph("ANTES_TABLA: reglas de cantidad del programa ficticio.")
    table = document.add_table(rows=1, cols=4)
    for cell, text in zip(table.rows[0].cells, HEADERS, strict=True):
        cell.text = text
    for values in ROWS:
        for cell, text in zip(table.add_row().cells, values, strict=True):
            cell.text = text
    if merge:
        table.cell(1, 0).merge(table.cell(1, 1))
        table.cell(2, 2).merge(table.cell(3, 2))
    if nested or depth:
        cell = table.cell(1, 3)
        cell.text = "ANTES_ANIDADA"
        target = cell
        for i in range(depth or 1):
            inner = target.add_table(rows=1, cols=1)
            target = inner.cell(0, 0)
            target.text = f"NIVEL_ANIDADO_{i+1}"
        cell.add_paragraph("DESPUES_ANIDADA")
    document.add_paragraph("DESPUES_TABLA: las reglas requieren revisión docente.")
    document.save(path)
    return path


def make_pptx(path: Path, *, merged=False, group=False, notes_only=False):
    presentation = Presentation()
    slide = presentation.slides.add_slide(presentation.slide_layouts[6])
    if not notes_only:
        before = slide.shapes.add_textbox(Inches(0), Inches(0), Inches(7), Inches(1))
        before.text = "ANTES_TABLA: casos ficticios de cantidad."
        shape = slide.shapes.add_table(4, 4, Inches(0), Inches(1), Inches(9), Inches(3))
        table = shape.table
        for r, values in enumerate([HEADERS, *ROWS]):
            for c, text in enumerate(values):
                table.cell(r, c).text = text
        if merged:
            table.cell(1, 0).merge(table.cell(1, 1))
        if group:
            grouped = slide.shapes.add_group_shape()
            grouped.shapes._spTree.insert_element_before(shape._element, "p:extLst")
        after = slide.shapes.add_textbox(Inches(0), Inches(5), Inches(7), Inches(1))
        after.text = "DESPUES_TABLA: revisar las condiciones de aceptación."
    slide.notes_slide.notes_text_frame.text = NOTE
    presentation.save(path)
    return path
