"""TXT (direct read, location: line offset) and Markdown (heading-section parsing)
extractors (research.md §4)."""

from __future__ import annotations

import re

from oralia.domain.materials.segmenter import ExtractedBlock


class TxtExtractor:
    def extract(self, file_path: str) -> list[ExtractedBlock]:
        with open(file_path, encoding="utf-8", errors="replace") as handle:
            lines = handle.readlines()
        blocks: list[ExtractedBlock] = []
        for offset, line in enumerate(lines):
            text = line.strip()
            if text:
                blocks.append(ExtractedBlock(text=text, location_ref=f"línea {offset + 1}"))
        return blocks


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


class MarkdownExtractor:
    def extract(self, file_path: str) -> list[ExtractedBlock]:
        with open(file_path, encoding="utf-8", errors="replace") as handle:
            content = handle.read()

        blocks: list[ExtractedBlock] = []
        current_heading = "documento"
        current_lines: list[str] = []

        def flush() -> None:
            text = "\n".join(current_lines).strip()
            if text:
                blocks.append(ExtractedBlock(text=text, location_ref=current_heading))

        for line in content.splitlines():
            match = _HEADING_RE.match(line)
            if match:
                flush()
                current_heading = match.group(2).strip()
                current_lines = []
            else:
                current_lines.append(line)
        flush()
        return blocks
