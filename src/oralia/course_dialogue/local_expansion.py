"""Bounded lab-only local RAG retrieval; no semantic or publication verdict."""

from dataclasses import dataclass

from oralia.course_dialogue.document_evidence import RetrievalBudget, RetrievalResult, retrieve_units


@dataclass(frozen=True)
class LocalEvidenceAttempts:
    initial: RetrievalResult
    expanded: RetrievalResult | None
    delivered: RetrievalResult
    reason: str
    semantic_sufficiency: str = "unverified"
    publication_allowed: bool = False


def retrieve_with_local_expansion(
    units,
    catalog,
    question,
    *,
    displayed_history=(),
    focus_change=False,
    insufficient=False,
    initial_budget=None,
    expanded_budget=None,
    lexical_profile="literal",
):
    """Re-query the authorized catalog once after an external insufficiency signal.

    Scores and the signal do not certify support, relevance, or completeness.
    The caller must review conflicts and sufficiency independently before any
    generated content is considered for publication.
    """
    if type(insufficient) is not bool:
        raise ValueError("insufficient must be an explicit boolean")
    if type(focus_change) is not bool:
        raise ValueError("focus_change must be an explicit boolean")
    first_budget = initial_budget or RetrievalBudget()
    second_budget = expanded_budget or RetrievalBudget(
        max_chars=10000, max_units=12, max_seed_units=8, max_neighbors=4
    )
    first_budget.validate()
    second_budget.validate()
    if (
        second_budget.max_chars < first_budget.max_chars
        or second_budget.max_units < first_budget.max_units
        or second_budget.max_seed_units < first_budget.max_seed_units
        or second_budget.max_neighbors < first_budget.max_neighbors
    ):
        raise ValueError("expanded budget must not shrink")
    initial = retrieve_units(
        units,
        catalog,
        question,
        displayed_history=displayed_history,
        focus_change=focus_change,
        budget=first_budget,
        lexical_profile=lexical_profile,
    )
    if not insufficient:
        return LocalEvidenceAttempts(initial, None, initial, "initial_only")
    expanded = retrieve_units(
        units,
        catalog,
        question,
        displayed_history=displayed_history,
        focus_change=focus_change,
        budget=second_budget,
        lexical_profile=lexical_profile,
        broaden_candidates=lexical_profile == "bilingual-v1",
    )
    selected = []
    seen = set()
    trace = [dict(row, phase="initial_retrieval") for row in initial.trace]
    trace.extend(dict(row, phase="expanded_retrieval") for row in expanded.trace)
    chars_used = 0
    for origin, result in (("retained_initial", initial), ("added_expanded", expanded)):
        for unit in result.units:
            if unit.id in seen:
                continue
            seen.add(unit.id)
            if (
                len(selected) >= second_budget.max_units
                or chars_used + len(unit.text) > second_budget.max_chars
            ):
                trace.append(
                    {
                        "unit_id": unit.id,
                        "decision": "omitted_merge_budget",
                        "origin": origin,
                        "phase": "delivery",
                    }
                )
                continue
            selected.append(unit)
            chars_used += len(unit.text)
            trace.append({"unit_id": unit.id, "decision": origin, "phase": "delivery"})
    delivered = RetrievalResult(
        tuple(selected),
        tuple(trace),
        chars_used,
        expanded.catalog_page_ids,
        expanded.catalog_documents,
        expanded.scope,
    )
    return LocalEvidenceAttempts(initial, expanded, delivered, "external_insufficiency_signal")
