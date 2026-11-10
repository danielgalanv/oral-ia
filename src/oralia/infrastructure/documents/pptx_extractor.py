"""PPTX body text and native cells in stored shape order; speaker notes excluded.

A table is not reconstructed from an image. No automatic teacher-note/solution
publication, OCR, chart data or spatial reading-order inference is performed.
"""

from __future__ import annotations

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

from oralia.domain.materials.segmenter import ExtractedBlock
from oralia.infrastructure.documents.table_context import contextual_cell


def _ordered_shapes(shapes):
    stack = [iter(shapes)]
    while stack:
        shape = next(stack[-1], None)
        if shape is None:
            stack.pop()
        elif shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            stack.append(iter(shape.shapes))
        else:
            yield shape


def _flush_text(texts, location):
    combined = "\n\n".join(texts).strip()
    texts.clear()
    return [ExtractedBlock(text=combined, location_ref=location)] if combined else []


class PptxExtractor:
    def extract(self, file_path: str) -> list[ExtractedBlock]:
        presentation = Presentation(file_path)
        blocks: list[ExtractedBlock] = []
        for slide_number, slide in enumerate(presentation.slides, start=1):
            texts = []
            table_number = 0
            slide_location = f"diapositiva {slide_number}"

            for shape in _ordered_shapes(slide.shapes):
                if shape.has_table:
                    blocks.extend(_flush_text(texts, slide_location))
                    table_number += 1
                    table = shape.table
                    first_row = {c + 1: cell.text for c, cell in enumerate(table.rows[0].cells)}
                    for row_number, row in enumerate(table.rows, 1):
                        row_start = row.cells[0].text
                        for column, cell in enumerate(row.cells, 1):
                            if cell.is_spanned:
                                continue
                            text = cell.text.strip()
                            if text:
                                blocks.append(
                                    ExtractedBlock(
                                        text=contextual_cell(
                                            text,
                                            row=row_number,
                                            column=column,
                                            first_row=first_row,
                                            row_start=row_start,
                                        ),
                                        location_ref=(
                                            f"{slide_location}, tabla {table_number}, fila {row_number}, "
                                            f"columna {column}"
                                        ),
                                    )
                                )
                elif shape.has_text_frame:
                    shape_text = shape.text_frame.text.strip()
                    if shape_text:
                        texts.append(shape_text)
            blocks.extend(_flush_text(texts, slide_location))
        return blocks
