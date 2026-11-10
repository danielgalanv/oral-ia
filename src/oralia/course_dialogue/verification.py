"""Source checks are independent of generation and never pretend entailment."""

from oralia.course_dialogue.contracts import Candidate


def inspect_candidate(candidate: Candidate, sources: dict[str, str]):
    failures = []
    for index, segment in enumerate(candidate.segments):
        source = sources.get(segment.source_id)
        if source is None or segment.source_quote not in source:
            failures.append({"segment": index, "reason": "missing_or_changed_source_witness"})
        if segment.kind == "literal" and segment.text != segment.source_quote:
            failures.append({"segment": index, "reason": "literal_not_exact"})
    return {
        "source_checks": not failures,
        "failures": failures,
        "independent_semantics": False,
        "publication_allowed": False,
        "reason": "G2_requires_independent_derived_claim_verification",
        "human_review": "pending",
        "voice_validation": "pending",
    }
