"""Deterministic conflict-detection heuristic (research.md §7, FR-022): fragments from
different documents that share significant keywords but disagree via a negation marker
are flagged as conflicting. No NLI model — a directed, testable heuristic (Principio XI).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_MIN_SIGNIFICANT_WORD_LEN = 4
_OVERLAP_THRESHOLD = 0.3
_NEGATION_MARKERS = ("no es", "no son", "nunca", "jamás", "no fue", "no eran", "falso que")


def _significant_words(text: str) -> set[str]:
    words = re.findall(r"[a-záéíóúñü]+", text.lower())
    return {w for w in words if len(w) >= _MIN_SIGNIFICANT_WORD_LEN}


def _negation_count(text: str) -> int:
    lowered = text.lower()
    return sum(lowered.count(marker) for marker in _NEGATION_MARKERS)


@dataclass(frozen=True)
class ConflictCandidate:
    fragment_id: str
    document_id: str
    text: str


def detect_conflicts(fragments: list[ConflictCandidate]) -> list[tuple[ConflictCandidate, ConflictCandidate]]:
    """Pairs of fragments — from different documents, on the same topic, disagreeing via
    negation — flagged as conflicting."""

    pairs: list[tuple[ConflictCandidate, ConflictCandidate]] = []
    for i, a in enumerate(fragments):
        for b in fragments[i + 1 :]:
            if a.document_id == b.document_id:
                continue
            words_a, words_b = _significant_words(a.text), _significant_words(b.text)
            if not words_a or not words_b:
                continue
            overlap = len(words_a & words_b) / min(len(words_a), len(words_b))
            if overlap < _OVERLAP_THRESHOLD:
                continue
            if _negation_count(a.text) != _negation_count(b.text):
                pairs.append((a, b))
    return pairs
