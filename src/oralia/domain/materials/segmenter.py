"""Deterministic, reproducible text segmentation (research.md §5, FR-007).

No third-party chunking framework, no randomness: the same input blocks plus the same
configuration always produce the same fragments, in the same order, byte for byte.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

DEFAULT_CHUNK_SIZE = 800
DEFAULT_OVERLAP = 100


@dataclass(frozen=True)
class ExtractedBlock:
    text: str
    location_ref: str


@dataclass(frozen=True)
class Segment:
    text: str
    location_ref: str
    sequence_index: int


def _split_paragraphs(text: str) -> list[str]:
    return [p for p in text.split("\n\n") if p.strip()]


def _split_sentences(paragraph: str) -> list[str]:
    # Deterministic, dependency-free sentence split — good enough for chunk boundaries,
    # not a linguistic parser.
    parts = re.split(r"(?<=[.!?])\s+", paragraph.strip())
    return [p for p in parts if p]


def _pack(units: list[str], chunk_size: int) -> list[str]:
    chunks: list[str] = []
    current = ""
    for unit in units:
        candidate = f"{current} {unit}".strip() if current else unit
        if len(candidate) <= chunk_size or not current:
            current = candidate
        else:
            chunks.append(current)
            current = unit
        while len(current) > chunk_size:
            chunks.append(current[:chunk_size])
            current = current[chunk_size:]
    if current:
        chunks.append(current)
    return chunks


def _chunk_block_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if len(text) <= chunk_size:
        return [text]
    paragraphs = _split_paragraphs(text) or [text]
    units: list[str] = []
    for paragraph in paragraphs:
        if len(paragraph) <= chunk_size:
            units.append(paragraph)
        else:
            units.extend(_split_sentences(paragraph))
    chunks = _pack(units, chunk_size)
    if overlap <= 0 or len(chunks) <= 1:
        return chunks
    overlapped = [chunks[0]]
    for chunk in chunks[1:]:
        tail = overlapped[-1][-overlap:]
        overlapped.append(f"{tail}{chunk}" if tail else chunk)
    return overlapped


def segment_blocks(
    blocks: list[ExtractedBlock],
    *,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> list[Segment]:
    """Same ``blocks`` + same ``chunk_size``/``overlap`` → same output, always (FR-007)."""

    segments: list[Segment] = []
    index = 0
    for block in blocks:
        for chunk_text in _chunk_block_text(block.text, chunk_size, overlap):
            if not chunk_text.strip():
                continue
            segments.append(Segment(text=chunk_text, location_ref=block.location_ref, sequence_index=index))
            index += 1
    return segments
