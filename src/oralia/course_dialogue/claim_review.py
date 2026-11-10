"""Lab-only validation of a human/model claim ledger, without judging truth.

This module is deliberately absent from participant runtime and publication gates.
Exact spans and source witnesses establish traceability, never entailment.
"""

from dataclasses import dataclass
from typing import Literal

Verdict = Literal["supported", "unsupported", "unknown"]
ClaimKind = Literal["fiction", "general", "conclusion"]


@dataclass(frozen=True)
class ClaimReview:
    start: int
    end: int
    quote: str
    kind: ClaimKind
    central: bool
    verdict: Verdict
    premise_quotes: tuple[str, ...] = ()
    source_id: str | None = None
    source_passage: str | None = None
    rationale: str = ""


def validate_review(
    answer: str,
    claims: tuple[ClaimReview, ...],
    pages: dict[str, str],
    required_central_quotes: tuple[str, ...],
) -> None:
    """Check ledger structure and provenance; never infer a verdict from a page."""
    if (
        not isinstance(answer, str)
        or not answer.strip()
        or not claims
        or not required_central_quotes
        or not any(claim.central for claim in claims)
    ):
        raise ValueError("answer and independently listed central claims required")
    if any(not isinstance(quote, str) or not quote.strip() for quote in required_central_quotes):
        raise ValueError("required central quotes must be nonempty text")
    if len(set(required_central_quotes)) != len(required_central_quotes):
        raise ValueError("duplicate required central claim")
    positions: set[tuple[int, int]] = set()
    for claim in claims:
        if (
            type(claim.start) is not int
            or type(claim.end) is not int
            or claim.start < 0
            or claim.end <= claim.start
            or claim.end > len(answer)
            or not isinstance(claim.quote, str)
            or not claim.quote.strip()
            or answer[claim.start : claim.end] != claim.quote
        ):
            raise ValueError("claim must quote an exact answer span")
        span = (claim.start, claim.end)
        if span in positions:
            raise ValueError("duplicate claim span")
        positions.add(span)
        if (
            type(claim.central) is not bool
            or claim.kind
            not in (
                "fiction",
                "general",
                "conclusion",
            )
            or claim.verdict
            not in (
                "supported",
                "unsupported",
                "unknown",
            )
        ):
            raise ValueError("invalid claim kind or verdict")
        if (
            not isinstance(claim.premise_quotes, tuple)
            or any(
                not isinstance(premise, str) or not premise.strip() or premise not in answer
                for premise in claim.premise_quotes
            )
            or len(set(claim.premise_quotes)) != len(claim.premise_quotes)
        ):
            raise ValueError("premise must quote this answer")
        if claim.source_id is None or claim.source_passage is None:
            if claim.source_id is not None or claim.source_passage is not None:
                raise ValueError("source identifier and passage must occur together")
            if claim.verdict == "supported" and claim.kind != "fiction":
                raise ValueError("supported non-fiction claim requires a source witness")
        elif (
            not isinstance(claim.source_id, str)
            or not isinstance(claim.source_passage, str)
            or claim.source_id not in pages
            or not claim.source_passage.strip()
            or claim.source_passage not in pages[claim.source_id]
        ):
            raise ValueError("source passage must occur on the identified original page")
        if claim.kind == "fiction" and (claim.source_id is not None or claim.verdict != "supported"):
            raise ValueError("fiction is only a declared assumption, without a source witness")
        if claim.kind == "conclusion" and claim.verdict == "supported" and not claim.premise_quotes:
            raise ValueError("supported conclusion requires explicit premises")
        if claim.verdict != "supported" and (
            not isinstance(claim.rationale, str) or not claim.rationale.strip()
        ):
            raise ValueError("unsupported or unknown claims require a reason")
    ordered = sorted(positions)
    if any(left[1] > right[0] for left, right in zip(ordered, ordered[1:], strict=False)):
        raise ValueError("claim spans overlap")
    central_quotes = [claim.quote for claim in claims if claim.central]
    if len(central_quotes) != len(required_central_quotes) or set(required_central_quotes) != set(
        central_quotes
    ):
        raise ValueError("central ledger does not cover frozen central claims")


def aggregate_review(
    answer: str,
    claims: tuple[ClaimReview, ...],
    pages: dict[str, str],
    required_central_quotes: tuple[str, ...],
) -> Verdict:
    """Fail closed; the result summarizes recorded labels, not semantic correctness."""
    validate_review(answer, claims, pages, required_central_quotes)
    if any(claim.verdict == "unsupported" for claim in claims):
        return "unsupported"
    if any(claim.verdict == "unknown" for claim in claims):
        return "unknown"
    return "supported"
