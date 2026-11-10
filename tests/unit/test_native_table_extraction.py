"""Native-table coverage, literal values and provenance independent of index scoring."""

import pytest

from oralia.domain.materials.segmenter import segment_blocks
from oralia.infrastructure.documents.docx_extractor import DocxExtractor
from oralia.infrastructure.documents.extractor import NotProcessableError, assert_processable
from oralia.infrastructure.documents.pptx_extractor import PptxExtractor
from tests.table_fixtures import NOTE, make_docx, make_pptx


@pytest.mark.parametrize("kind", ["docx", "pptx"])
def test_native_cells_are_ordered_located_and_preserve_literal_values(tmp_path, kind):
    path = (make_docx if kind == "docx" else make_pptx)(tmp_path / f"native.{kind}")
    extractor = DocxExtractor() if kind == "docx" else PptxExtractor()
    blocks = extractor.extract(str(path))
    cells = [b for b in blocks if "tabla 1" in b.location_ref]
    assert cells, "Processed text must not silently omit native tables"
    assert all(any(value in b.text for b in cells) for value in ["007", "1000", "3,5"])
    assert any(
        "fila 2" in b.location_ref and "columna 1" in b.location_ref and "007" in b.text for b in cells
    )
    before = next(i for i, b in enumerate(blocks) if "ANTES_TABLA" in b.text)
    first_cell = next(i for i, b in enumerate(blocks) if "tabla 1" in b.location_ref)
    assert before < first_cell and "DESPUES_TABLA" in blocks[-1].text
    assert NOTE not in "\n".join(b.text for b in blocks)
    assert all(len(b.location_ref) <= 200 for b in blocks)
    assert segment_blocks(blocks) == segment_blocks(extractor.extract(str(path)))


@pytest.mark.parametrize("kind", ["docx", "pptx"])
def test_merged_cells_have_one_origin_not_duplicate_coordinates(tmp_path, kind):
    path = (
        make_docx(tmp_path / "merge.docx", merge=True)
        if kind == "docx"
        else make_pptx(tmp_path / "merge.pptx", merged=True)
    )
    blocks = (DocxExtractor() if kind == "docx" else PptxExtractor()).extract(str(path))
    origin = [b for b in blocks if "fila 2" in b.location_ref and "columna 1" in b.location_ref]
    duplicate = [b for b in blocks if "fila 2" in b.location_ref and "columna 2" in b.location_ref]
    assert len(origin) == 1 and "007" in origin[0].text
    assert not duplicate


def test_docx_nested_cells_keep_inner_order(tmp_path):
    blocks = DocxExtractor().extract(str(make_docx(tmp_path / "nested.docx", nested=True)))
    positions = [
        next(i for i, b in enumerate(blocks) if text in b.text)
        for text in ["ANTES_ANIDADA", "NIVEL_ANIDADO_1", "DESPUES_ANIDADA"]
    ]
    assert positions == sorted(positions) and len(set(positions)) == 3


def test_deep_nesting_is_explicit_error_not_silent_partial_text(tmp_path):
    path = make_docx(tmp_path / "deep.docx", depth=4)
    with pytest.raises(ValueError, match="anidadas"):
        DocxExtractor().extract(str(path))


def test_pptx_grouped_native_table_is_read(tmp_path):
    blocks = PptxExtractor().extract(str(make_pptx(tmp_path / "group.pptx", group=True)))
    assert any("tabla 1" in b.location_ref and "007" in b.text for b in blocks)


def test_speaker_notes_are_never_material_or_sufficient_body(tmp_path):
    blocks = PptxExtractor().extract(str(make_pptx(tmp_path / "notes.pptx", notes_only=True)))
    assert not blocks
    with pytest.raises(NotProcessableError):
        assert_processable(blocks)


def test_plain_documents_keep_legacy_locations(tmp_path):
    from docx import Document
    from pptx import Presentation
    from pptx.util import Inches

    doc = Document()
    doc.add_heading("Sección", 1)
    doc.add_paragraph("Texto original suficientemente largo.")
    path = tmp_path / "plain.docx"
    doc.save(path)
    assert [b.location_ref for b in DocxExtractor().extract(str(path))] == [
        "párrafo 1 (Sección)",
        "párrafo 2 (Sección)",
    ]
    ppt = Presentation()
    slide = ppt.slides.add_slide(ppt.slide_layouts[6])
    box = slide.shapes.add_textbox(0, 0, Inches(5), Inches(1))
    box.text = "Texto original suficientemente largo."
    path = tmp_path / "plain.pptx"
    ppt.save(path)
    blocks = PptxExtractor().extract(str(path))
    assert len(blocks) == 1 and blocks[0].location_ref == "diapositiva 1"


def test_context_is_bounded_but_original_cell_is_not_truncated(tmp_path):
    from docx import Document

    doc = Document()
    table = doc.add_table(rows=2, cols=2)
    table.cell(0, 1).text = "REFERENCIA_LARGA_" * 50
    table.cell(1, 0).text = "CLAVE_LARGA_" * 50
    raw = "CONTENIDO_INTEGRO_" * 100
    table.cell(1, 1).text = raw
    path = tmp_path / "long.docx"
    doc.save(path)
    blocks = DocxExtractor().extract(str(path))
    target = next(b for b in blocks if "fila 2" in b.location_ref and "columna 2" in b.location_ref)
    assert target.text.startswith(raw)
    assert len(target.text) - len(raw) < 450
    assert any(b.text == "REFERENCIA_LARGA_" * 50 for b in blocks)
