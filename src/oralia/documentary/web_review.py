"""Separate review contracts; structural witnesses do not certify semantics.

Reuses claim_review's exact-witness principle. No keyword-based contradiction
classifier and no generator self-approval are introduced here.
"""

from dataclasses import asdict, dataclass
from typing import Protocol


@dataclass(frozen=True)
class ReviewVerdict:
    status: str
    reviewer: str
    reason: str
    witnesses: tuple[tuple[str, str], ...] = ()
    simulated: bool = False


class ExternalSupportPort(Protocol):
    async def review(self, documents) -> ReviewVerdict: ...


class TeacherCompatibilityPort(Protocol):
    async def review(self, documents, teacher_pages) -> ReviewVerdict: ...


def _validate(verdict, statuses, sources):
    if (
        not isinstance(verdict, ReviewVerdict)
        or verdict.status not in statuses
        or not verdict.reviewer.strip()
        or not verdict.reason.strip()
    ):
        raise ValueError("typed independent review required")
    for identifier, quote in verdict.witnesses:
        if not quote or quote not in sources.get(identifier, ""):
            raise ValueError("missing exact review witness")
    if verdict.status != "unknown" and not verdict.witnesses:
        raise ValueError("substantive verdict requires witnesses")


async def review_web(documents, teacher_pages, *, support=None, compatibility=None, coverage_gaps=()):
    """Pass the whole supplied active catalog, never silently just first top-k.

    Caller binds/revalidates this catalog to the activity. Missing extraction and
    unavailable pages must appear in coverage_gaps. All resulting content remains
    outside generation: an evaluator still needs independent held-out evidence.
    """
    sources = {d["capture_sha256"]: "\n".join(d["fragments"]) for d in documents}
    unavailable = ReviewVerdict("unknown", "host/no-validated-evaluator", "semantic capability not validated")
    external = await support.review(documents) if support else unavailable
    teacher = await compatibility.review(documents, teacher_pages) if compatibility else unavailable
    _validate(external, {"supported", "rejected", "unknown"}, sources)
    _validate(teacher, {"compatible", "conflict", "unknown"}, {**sources, **teacher_pages})
    return {
        "external_support": asdict(external),
        "teacher_compatibility": asdict(teacher),
        "teacher_pages_reviewed": list(teacher_pages),
        "coverage_gaps": list(coverage_gaps),
        "source_independence": "not_established_by_hash_or_distinct_urls",
        "independent_semantics": False,
        "approved_content": [],
        "delivered_to_model": [],
        "publication_allowed": False,
        "reason": "semantic validation and existing FR-014/T090/T150 gates remain pending",
    }
