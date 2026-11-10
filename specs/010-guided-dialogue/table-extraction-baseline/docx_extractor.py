"""DOCX text extraction via ``python-docx`` (research.md §4).

Location reference: paragraph index plus the last-seen heading text as a section label.
"""

from __future__ import annotations

import docx

from oralia.domain.materials.segmenter import ExtractedBlock


class DocxExtractor:
    def extract(self, file_path: str) -> list[ExtractedBlock]:
        document = docx.Document(file_path)
        blocks: list[ExtractedBlock] = []
        current_section = "documento"
        for index, paragraph in enumerate(document.paragraphs, start=1):
            text = paragraph.text.strip()
            if not text:
                continue
            style_name = paragraph.style.name if paragraph.style is not None else ""
            if style_name.lower().startswith("heading"):
                current_section = text
            blocks.append(ExtractedBlock(text=text, location_ref=f"párrafo {index} ({current_section})"))
        return blocks
