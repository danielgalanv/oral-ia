"""Lab-only multi-passage review records; structural witnesses are not entailment."""

import hashlib
from dataclasses import dataclass
from typing import Literal

from oralia.course_dialogue.document_evidence import EvidenceUnit

Status = Literal["supported", "unsupported", "unknown"]
ClaimType = Literal["documentary", "inference", "fictional_example"]


@dataclass(frozen=True)
class PassageWitness:
    unit_id: str
    start: int
    end: int
    quote: str


@dataclass(frozen=True)
class MultiPassageReview:
    answer_start: int
    answer_end: int
    claim_quote: str
    claim_type: ClaimType
    status: Status
    passages: tuple[PassageWitness, ...]
    premise_quotes: tuple[str, ...]
    rationale: str
    conflict_unresolved: bool = False
    publication_allowed: bool = False


@dataclass(frozen=True)
class ReviewBudget:
    max_passages: int = 5
    max_premises: int = 4
    max_passage_chars: int = 4000


def validate_review_set(
    answer: str,
    review: MultiPassageReview,
    available_units: tuple[EvidenceUnit, ...],
    source_pages: dict[str, dict],
    budget: ReviewBudget = ReviewBudget(),
) -> None:
    """Verify exact provenance and bounded shape, never semantic implication."""
    if review.publication_allowed:
        raise ValueError("lab review cannot publish")
    if review.claim_type not in ("documentary", "inference", "fictional_example") or review.status not in (
        "supported",
        "unsupported",
        "unknown",
    ):
        raise ValueError("invalid review label")
    if (
        type(review.answer_start) is not int
        or type(review.answer_end) is not int
        or not 0 <= review.answer_start < review.answer_end <= len(answer)
        or not review.claim_quote.strip()
        or answer[review.answer_start : review.answer_end] != review.claim_quote
    ):
        raise ValueError("claim span must be exact")
    if not 1 <= budget.max_passages <= 10 or not 0 <= budget.max_premises <= 10:
        raise ValueError("invalid review budget")
    if not 1 <= budget.max_passage_chars <= 20000:
        raise ValueError("invalid passage character budget")
    if len(review.passages) > budget.max_passages or len(review.premise_quotes) > budget.max_premises:
        raise ValueError("review witness count exceeds budget")
    if any(
        not isinstance(text, str) or not text.strip() or text not in answer for text in review.premise_quotes
    ) or len(set(review.premise_quotes)) != len(review.premise_quotes):
        raise ValueError("premises must be distinct exact answer text")
    units = {unit.id: unit for unit in available_units}
    if len(units) != len(available_units):
        raise ValueError("duplicate evidence unit")
    seen = set()
    chars_used = 0
    for witness in review.passages:
        if witness.unit_id not in units:
            raise ValueError("passage outside retrieved evidence")
        unit = units[witness.unit_id]
        if (
            type(witness.start) is not int
            or type(witness.end) is not int
            or not 0 <= witness.start < witness.end <= len(unit.text)
            or not isinstance(witness.quote, str)
            or not witness.quote.strip()
            or unit.text[witness.start : witness.end] != witness.quote
        ):
            raise ValueError("passage is not an exact unit span")
        key = (witness.unit_id, witness.start, witness.end)
        if key in seen:
            raise ValueError("duplicate passage")
        seen.add(key)
        chars_used += len(witness.quote)
        if hashlib.sha256(unit.text.encode()).hexdigest() != unit.text_sha256:
            raise ValueError("evidence unit text changed")
        for span in unit.positions:
            page = source_pages.get(span.page_id)
            if (
                page is None
                or page["filename"] != unit.document_id
                or page["original_sha256"] != unit.original_sha256
                or page["version"] != unit.version
                or page["page"] != span.page_number
            ):
                raise ValueError("evidence page identity changed")
            if span.bbox is None and (
                span.start is None
                or span.end is None
                or not 0 <= span.start < span.end <= len(page["text"])
                or page["text"][span.start : span.end] not in unit.text
            ):
                raise ValueError("evidence page text span changed")
            if span.bbox is not None and len(span.bbox) != 4:
                raise ValueError("invalid table box")
    if chars_used > budget.max_passage_chars:
        raise ValueError("passage characters exceed budget")
    if review.claim_type == "fictional_example" and review.passages:
        raise ValueError("fictional scenario cannot masquerade as literal source")
    if review.status == "supported":
        if review.claim_type != "fictional_example" and not review.passages:
            raise ValueError("supported academic claim requires documentary witnesses")
        if review.claim_type == "inference" and not review.premise_quotes:
            raise ValueError("supported inference requires explicit premises")
    elif not isinstance(review.rationale, str) or not review.rationale.strip():
        raise ValueError("unsupported or unknown requires a reason")
    if review.conflict_unresolved and review.status != "unknown":
        raise ValueError("unresolved source disagreement must remain unknown")
