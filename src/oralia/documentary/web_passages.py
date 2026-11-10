"""Bounded literal windows, lexical ranking and neighbouring context; not a truth assessor."""

import hashlib
import re

from oralia.domain.materials.query_excerpt import terms

SEPARATOR = "\n\n[Pasaje separado del mismo documento]\n\n"


def select_web_passages(text, question, concept, history, budget, preferred_ranges=None):
    if not isinstance(text, str) or not 256 <= budget <= 8000:
        raise ValueError("Bounded source text and character budget required")
    eligible = preferred_ranges or ([[0, len(text)]] if text else [])
    previous_end = 0
    for a, b in eligible:
        if not 0 <= previous_end <= a < b <= len(text):
            raise ValueError("Foreign or overlapping source ranges")
        previous_end = b
    if sum(b - a for a, b in eligible) + max(0, len(eligible) - 1) * len(SEPARATOR) <= budget:
        selected = [tuple(span) for span in eligible]
    else:
        target = max(80, min(1400, (budget - 2 * len(SEPARATOR)) // 3))
        chunks = []
        for lower, upper in eligible:
            boundaries = sorted(
                {upper, *[lower + m.end() for m in re.finditer(r"\n|[.!?](?=\s)", text[lower:upper])]}
            )
            start = lower
            for end in boundaries:
                if end - start >= target:
                    chunks.append((start, end))
                    start = end
            if start < upper:
                chunks.append((start, upper))
        current, topic, previous = terms(question), terms(concept), terms(" ".join(history))
        ranking = []
        for index, (start, end) in enumerate(chunks):
            tokens = terms(text[start:end])
            score = 3 * len(tokens & current) + len(tokens & topic) + len(tokens & previous)
            if score:
                ranking.append((-score, index))
        chosen = set()

        def ranges(indices):
            merged = []
            for index in sorted(indices):
                start, end = chunks[index]
                if merged and merged[-1][1] == start:
                    merged[-1] = (merged[-1][0], end)
                else:
                    merged.append((start, end))
            return merged

        for _, index in sorted(ranking):
            # Add the matching chunk, then neighbouring conditions where budget permits.
            for candidate in (index, index + 1, index - 1):
                if not 0 <= candidate < len(chunks):
                    continue
                trial = chosen | {candidate}
                spans = ranges(trial)
                size = sum(end - start for start, end in spans) + max(0, len(spans) - 1) * len(SEPARATOR)
                if size <= budget:
                    chosen = trial
        selected = ranges(chosen)
    spans = [
        {"start": a, "end": b, "text": text[a:b], "sha256": hashlib.sha256(text[a:b].encode()).hexdigest()}
        for a, b in selected
    ]
    omitted = []
    cursor = 0
    for a, b in selected:
        if a > cursor:
            omitted.append([cursor, a])
        cursor = b
    if cursor < len(text):
        omitted.append([cursor, len(text)])
    return {
        "profile": "literal-web-passages/v1",
        "source_sha256": hashlib.sha256(text.encode()).hexdigest(),
        "source_characters": len(text),
        "spans": spans,
        "omitted_ranges": omitted,
        "text": SEPARATOR.join(s["text"] for s in spans),
    }
