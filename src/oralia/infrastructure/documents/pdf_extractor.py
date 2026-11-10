"""PDF text extraction via ``pdfplumber`` (research.md §4). Location reference: page."""

from __future__ import annotations

import pdfplumber

from oralia.domain.materials.segmenter import ExtractedBlock


class PdfExtractor:
    def extract(self, file_path: str) -> list[ExtractedBlock]:
        blocks: list[ExtractedBlock] = []
        with pdfplumber.open(file_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                text = (page.extract_text() or "").strip()
                if text:
                    blocks.append(ExtractedBlock(text=text, location_ref=f"página {page_number}"))
        return blocks
