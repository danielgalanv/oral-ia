"""PPTX text extraction via ``python-pptx`` (research.md §4). Location reference: slide."""

from __future__ import annotations

from pptx import Presentation

from oralia.domain.materials.segmenter import ExtractedBlock


class PptxExtractor:
    def extract(self, file_path: str) -> list[ExtractedBlock]:
        presentation = Presentation(file_path)
        blocks: list[ExtractedBlock] = []
        for slide_number, slide in enumerate(presentation.slides, start=1):
            texts = []
            for shape in slide.shapes:
                if shape.has_text_frame:
                    shape_text = shape.text_frame.text.strip()
                    if shape_text:
                        texts.append(shape_text)
            combined = "\n\n".join(texts).strip()
            if combined:
                blocks.append(ExtractedBlock(text=combined, location_ref=f"diapositiva {slide_number}"))
        return blocks
