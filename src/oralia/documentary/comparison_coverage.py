"""Optional candidate diversification, never a semantic support verifier."""

import math
import re

from oralia.domain.materials.query_excerpt import normalized, terms


def facets(question, history=(), focus_change=False):
    current = normalized(question)
    # An explicit new question is not an elliptical request to repeat the old comparison.
    explicit = bool(re.search(r"\b(?:como|que|cual|donde|cuando)\b", current)) and len(terms(question)) >= 3
    for text in [question, *([] if focus_change or explicit else reversed(history[-2:]))]:
        value = normalized(text)
        match = re.search(r"\bentre\s+(.+?)\s+y\s+([^?.!;]+)", value)
        if match is None:
            match = re.search(r"\bdiferencian\s+(.+?)\s+y\s+([^?.!;]+)", value)
        if match is None and "es lo mismo" in value:
            match = re.search(r"\b(?:sea|son|ser)\s+(.+?)\s+y\s+([^?.!;]+)", value)
        if match is not None:
            sides = [terms(part) for part in match.groups()]
            if all(sides) and sides[0] != sides[1]:
                return sides
    return []


def diversify(ranked, by_id, pages, question, history=(), focus_change=False):
    """Promote at most two existing pages using rare facet terms/headings.

    No corpus IDs, extra retrieval, semantic sufficiency or source modifications.
    Missing discriminative terms stay missing instead of matching generic words.
    """
    sides = facets(question, history, focus_change)
    unique = {}
    for identifier in ranked:
        page = pages[by_id[identifier]["page_id"]]
        unique.setdefault(page["id"], (identifier, page))
    values = list(unique.values())
    bodies = [terms(page["text"]) for _, page in values]
    headings = [terms(page["section"]) for _, page in values]
    promoted, missing = [], []
    for side in sides:
        weights = {
            term: math.log((len(values) + 1) / (1 + sum(term in body for body in bodies))) + 1
            for term in side
        }
        core = {term for term, weight in weights.items() if weight == max(weights.values())}
        scored = []
        for position, ((identifier, _), body, heading) in enumerate(
            zip(values, bodies, headings, strict=True)
        ):
            if not core & body:
                continue
            # Prefer a focused heading over an incidental mention or a specialised
            # techniques/checklist page. A stated purpose breaks same-heading ties.
            heading_match = side & heading
            precision = sum(weights[term] for term in heading_match) / (1 + len(heading - side))
            purpose = bool(
                re.search(r"\b(?:objetivo|purpose|aim)\s*:", normalized(values[position][1]["text"]))
            )
            score = 3 * precision + sum(weights[term] for term in side & body)
            if heading_match and purpose:
                score += 1
            scored.append((-score, position, identifier))
        if not scored:
            missing.append(sorted(side))
        else:
            identifier = min(scored)[2]
            if identifier not in promoted:
                promoted.append(identifier)
    return promoted + [identifier for identifier in ranked if identifier not in promoted], {
        "profile": "comparison-coverage/v1",
        "facets": [sorted(side) for side in sides],
        "unmatched_facets": missing,
        "promoted_candidates": promoted,
        "semantic_support": "unverified",
    }
