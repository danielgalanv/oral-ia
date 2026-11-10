"""DocumentExtractor interface, MIME dispatch, and not-processable detection
(research.md §4, FR-002, FR-003, FR-006)."""

from __future__ import annotations

import os
from typing import Protocol

from oralia.domain.materials.segmenter import ExtractedBlock

MIN_EXTRACTABLE_CHARS = 20

EXTENSION_MIME = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".txt": "text/plain",
    ".md": "text/markdown",
}

SUPPORTED_MIME_TYPES = set(EXTENSION_MIME.values())


class NotProcessableError(Exception):
    """FR-003: extracted text is empty or below the minimum readable-content threshold."""


class DocumentExtractor(Protocol):
    def extract(self, file_path: str) -> list[ExtractedBlock]: ...


def assert_processable(blocks: list[ExtractedBlock]) -> None:
    total_chars = sum(len(block.text.strip()) for block in blocks)
    if total_chars < MIN_EXTRACTABLE_CHARS:
        raise NotProcessableError(
            f"extracted text below minimum threshold ({total_chars} < {MIN_EXTRACTABLE_CHARS} chars)"
        )


def mime_type_for_filename(filename: str) -> str | None:
    ext = os.path.splitext(filename)[1].lower()
    return EXTENSION_MIME.get(ext)


def get_extractor(mime_type: str) -> DocumentExtractor:
    from oralia.infrastructure.documents.docx_extractor import DocxExtractor
    from oralia.infrastructure.documents.pdf_extractor import PdfExtractor
    from oralia.infrastructure.documents.pptx_extractor import PptxExtractor
    from oralia.infrastructure.documents.text_extractor import MarkdownExtractor, TxtExtractor

    registry: dict[str, DocumentExtractor] = {
        "application/pdf": PdfExtractor(),
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": DocxExtractor(),
        "application/vnd.openxmlformats-officedocument.presentationml.presentation": PptxExtractor(),
        "text/plain": TxtExtractor(),
        "text/markdown": MarkdownExtractor(),
    }
    extractor = registry.get(mime_type)
    if extractor is None:
        raise ValueError(f"unsupported mime type: {mime_type}")
    return extractor
