"""Read-only R04/R05 diagnosis and history ablation; no retrieval profile change."""

import hashlib
import json
from dataclasses import asdict
from pathlib import Path
from time import perf_counter
from unittest.mock import patch

from oralia.course_dialogue import local_expansion
from oralia.course_dialogue.context import plan_context
from oralia.course_dialogue.document_evidence import EvidenceUnit, PagePosition, retrieve_units
from oralia.course_dialogue.retrieval_terms import retrieval_terms

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
PACKET = EVIDENCE / "cpu-rag-progress-v1"
OUTPUT = EVIDENCE / "cpu-retrieval-gap-diagnosis-v1"


def explain_ranking(units, query, shown, result, *, broaden):
    """Reconstruct arithmetic from frozen code, explicitly separate from its trace."""
    query_terms = retrieval_terms(query)
    history_terms = retrieval_terms(" ".join(shown[-2:]))
    rows = []
    for unit in units:
        words = retrieval_terms(unit.text + " " + unit.heading)
        query_hits = query_terms & words
        history_hits = history_terms & words
        rows.append(
            {
                "unit_id": unit.id,
                "pages": [s.page_id for s in unit.positions],
                "query_hits": sorted(query_hits),
                "history_hits": sorted(history_hits),
                "query_score": 4 * len(query_hits),
                "history_score": len(history_hits),
                "score": 4 * len(query_hits) + len(history_hits),
            }
        )
    matches = [row for row in rows if row["query_hits"] or row["history_hits"]]
    strongest = max((len(row["query_hits"]) for row in matches), default=0)
    eligible = [row for row in matches if strongest < 2 or len(row["query_hits"]) >= 2]
    maximum = max((row["score"] for row in eligible), default=0)
    ties = sum(row["score"] == maximum for row in eligible)
    cutoff = maximum - (0 if ties >= 2 else 4) if eligible else 0
    if broaden:
        cutoff = min(cutoff, maximum / 2)
    selected = {unit.id for unit in result.units}
    for row in rows:
        if row["unit_id"] in selected:
            reason = "selected_including_possible_neighbor"
        elif not row["query_hits"] and not row["history_hits"]:
            reason = "no_lexical_match"
        elif strongest >= 2 and len(row["query_hits"]) < 2:
            reason = "below_two_query_concepts"
        elif row["score"] < cutoff:
            reason = "below_score_band"
        elif any(t["unit_id"] == row["unit_id"] and t["decision"] == "omitted_budget" for t in result.trace):
            reason = "explicit_budget_omission"
        else:
            reason = "eligible_not_selected_seed_or_neighbor_limit"
        row["reconstructed_decision"] = reason
    return {
        "reconstruction_not_original_trace": True,
        "query_terms": sorted(query_terms),
        "history_terms": sorted(history_terms),
        "strongest_query_concepts": strongest,
        "top_score": maximum,
        "cutoff": cutoff,
        "units": rows,
    }


def metrics(result, references):
    pages = {span.page_id for unit in result.units for span in unit.positions}
    ref = set(references)
    outside_units = [u for u in result.units if not any(s.page_id in ref for s in u.positions)]
    return {
        "reference_page_recall": len(ref & pages) / len(ref),
        "reference_pages_recovered": sorted(ref & pages),
        "reference_pages_missing": sorted(ref - pages),
        "delivered_pages": sorted(pages),
        "non_reference_pages": sorted(pages - ref),
        "non_reference_pages_are_not_certified_distractors": True,
        "chars": result.chars_used,
        "units": len(result.units),
        "chars_in_units_outside_reference_pages": sum(len(u.text) for u in outside_units),
        "explicit_budget_omissions": sum(t["decision"].startswith("omitted") for t in result.trace),
        "actual_trace": result.trace,
    }


def main():
    OUTPUT.mkdir(exist_ok=False)
    raw = (PACKET / "controls.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == (PACKET / "controls.sha256").read_text()
    packet = json.loads(raw)
    units = [
        EvidenceUnit(**{**r, "positions": tuple(PagePosition(**p) for p in r["positions"])})
        for r in packet["units"]
    ]
    cases = {case["id"]: case for case in packet["cases"]}
    records = []
    for key in ("R04", "R05"):
        case = cases[key]
        history = []
        if case.get("history_from"):
            previous = cases[case["history_from"]]
            history = [
                {
                    "input": previous["question"],
                    "displayed_text": previous["reference_passages"][0]["text"],
                    "display_kind": "candidate",
                    "displayed_kind": "laboratory_preview",
                }
            ]
        query = plan_context(case["question"], history).academic_query
        shown = tuple(row["displayed_text"] for row in history)
        conditions = []
        for label, supplied_history in (
            ("original_history", shown),
            ("history_terms_removed_query_unchanged", ()),
        ):
            times = []
            for _ in range(3):
                phase_times = []

                def measured(*args, phase_times=phase_times, **kwargs):
                    start = perf_counter()
                    result = retrieve_units(*args, **kwargs)
                    phase_times.append(
                        {
                            "phase": "expanded" if kwargs.get("broaden_candidates") else "initial",
                            "ms": (perf_counter() - start) * 1000,
                        }
                    )
                    return result

                start = perf_counter()
                with patch.object(local_expansion, "retrieve_units", measured):
                    attempts = local_expansion.retrieve_with_local_expansion(
                        units,
                        packet["pages"],
                        query,
                        displayed_history=supplied_history,
                        insufficient=True,
                        lexical_profile="bilingual-v1",
                    )
                times.append({"total_ms": (perf_counter() - start) * 1000, "retrieval_phases": phase_times})
            conditions.append(
                {
                    "condition": label,
                    "query": query,
                    "history_terms": list(supplied_history),
                    "initial": metrics(attempts.initial, case["references"]),
                    "expanded": metrics(attempts.delivered, case["references"]),
                    "initial_ranking": explain_ranking(
                        units, query, supplied_history, attempts.initial, broaden=False
                    ),
                    "expanded_ranking": explain_ranking(
                        units, query, supplied_history, attempts.expanded, broaden=True
                    ),
                    "timings_three_cpu_replays_not_model_or_semantic_trials": times,
                }
            )
        records.append(
            {
                "id": key,
                "question": case["question"],
                "resolved_query": query,
                "references_available": {
                    page: [asdict(u) for u in units if any(s.page_id == page for s in u.positions)]
                    for page in case["references"]
                },
                "conditions": conditions,
            }
        )
    result = {
        "records": records,
        "exposed_development_diagnostic_not_new_benchmark": True,
        "history_ablation_is_not_a_proposed_profile": True,
        "retrieval_profile_unchanged": "bilingual-v1",
        "weights_loaded": False,
        "cuda_initialized": False,
        "model_calls": 0,
        "control_sha256": hashlib.sha256(raw).hexdigest(),
    }
    (OUTPUT / "diagnosis.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    for record in records:
        for condition in record["conditions"]:
            target = condition["expanded"]
            print(
                record["id"],
                condition["condition"],
                target["reference_page_recall"],
                target["chars"],
                target["units"],
            )
        for row in record["conditions"][0]["expanded_ranking"]["units"]:
            if any(
                page in record["conditions"][0]["expanded"]["reference_pages_missing"]
                for page in row["pages"]
            ):
                print(
                    "missing-unit",
                    row["unit_id"],
                    row["query_score"],
                    row["history_score"],
                    row["score"],
                    row["reconstructed_decision"],
                )


if __name__ == "__main__":
    main()
