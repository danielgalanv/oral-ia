"""Ordered DOCX body paragraphs/native tables. Notes/comments are not body material.

Existing top-level paragraph references are retained. Table cells carry explicit
coordinates, bounded structural context and original text. No OCR or layout inference.
"""

from __future__ import annotations

import docx
from docx.table import Table
from docx.text.paragraph import Paragraph

from oralia.domain.materials.segmenter import ExtractedBlock
from oralia.infrastructure.documents.table_context import contextual_cell

MAX_TABLE_DEPTH = 4


def _grid_cells(row):
    return enumerate(row.cells, start=getattr(row, "grid_cols_before", 0) + 1)


def _table_blocks(table, *, path, section, depth, seen):
    if depth > MAX_TABLE_DEPTH:
        raise ValueError("DOCX: tablas anidadas superan cuatro niveles; simplifique la estructura.")
    first_row = {column: cell.text for column, cell in _grid_cells(table.rows[0])} if table.rows else {}
    for row_number, row in enumerate(table.rows, 1):
        cells = list(_grid_cells(row))
        row_start = cells[0][1].text if cells else ""
        for column, cell in cells:
            # python-docx repeats the same OOXML cell for horizontal/vertical
            # merges. Retaining element references prevents identity reuse.
            if cell._tc in seen:
                continue
            seen.add(cell._tc)
            location = f"{path}, fila {row_number}, columna {column} ({section[:60]})"
            if len(location) > 200:
                raise ValueError("DOCX: localización de tabla demasiado profunda; simplifique la estructura.")
            yield from _cell_blocks(
                cell,
                location=location,
                path=f"{path}/f{row_number}/c{column}",
                section=section,
                row_number=row_number,
                column=column,
                first_row=first_row,
                row_start=row_start,
                depth=depth,
                seen=seen,
            )


def _cell_blocks(cell, *, location, path, section, row_number, column, first_row, row_start, depth, seen):
    paragraphs = []
    nested_index = part = 0

    def flush():
        nonlocal part
        if not paragraphs:
            return []
        part += 1
        text = "\n".join(paragraphs)
        paragraphs.clear()
        return [
            ExtractedBlock(
                text=contextual_cell(
                    text, row=row_number, column=column, first_row=first_row, row_start=row_start
                ),
                location_ref=location + (f", parte {part}" if nested_index or part > 1 else ""),
            )
        ]

    for item in cell.iter_inner_content():
        if isinstance(item, Paragraph):
            text = item.text.strip()
            if text:
                paragraphs.append(text)
        elif isinstance(item, Table):
            nested_index += 1
            yield from flush()
            yield from _table_blocks(
                item, path=f"{path} > tabla {nested_index}", section=section, depth=depth + 1, seen=seen
            )
    yield from flush()


class DocxExtractor:
    def extract(self, file_path: str) -> list[ExtractedBlock]:
        document = docx.Document(file_path)
        blocks: list[ExtractedBlock] = []
        current_section = "documento"
        paragraph_index = table_index = 0
        seen = set()
        for item in document.iter_inner_content():
            if isinstance(item, Table):
                table_index += 1
                blocks.extend(
                    _table_blocks(
                        item, path=f"tabla {table_index}", section=current_section, depth=1, seen=seen
                    )
                )
                continue
            if not isinstance(item, Paragraph):
                continue
            paragraph_index += 1
            text = item.text.strip()
            if not text:
                continue
            style_name = item.style.name if item.style is not None else ""
            if style_name.lower().startswith("heading"):
                current_section = text
            blocks.append(
                ExtractedBlock(text=text, location_ref=f"párrafo {paragraph_index} ({current_section})")
            )
        return blocks
