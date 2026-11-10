"""Evaluate frozen references using lexical CPU retrieval only; no embeddings/model."""

import argparse
import hashlib
import json
from pathlib import Path

from oralia.course_dialogue.context import plan_context
from oralia.course_dialogue.document_evidence import EvidenceUnit, PagePosition
from oralia.course_dialogue.local_expansion import retrieve_with_local_expansion

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "specs/012-conversational-course-study/evidence/cpu-rag-progress-v1"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--profile", choices=["literal", "bilingual-v1"], default="literal")
    args = parser.parse_args()
    output = PACKET / args.output
    if output.parent != PACKET or output.exists():
        raise ValueError("new local evidence filename required")
    raw = (PACKET / "controls.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == (PACKET / "controls.sha256").read_text()
    packet = json.loads(raw)
    units = [
        EvidenceUnit(**{**row, "positions": tuple(PagePosition(**p) for p in row["positions"])})
        for row in packet["units"]
    ]
    cases = {case["id"]: case for case in packet["cases"]}
    records = []
    for case in cases.values():
        history = []
        if case.get("history_from"):
            previous = cases[case["history_from"]]
            history = [
                {
                    "input": previous["question"],
                    "displayed_text": previous["reference_passages"][0]["text"],
                    "displayed_kind": "laboratory_preview",
                    "display_kind": "candidate",
                }
            ]
        plan = plan_context(case["question"], history)
        attempts = retrieve_with_local_expansion(
            units,
            packet["pages"],
            plan.academic_query,
            displayed_history=tuple(row["displayed_text"] for row in history),
            focus_change=case.get("explicit_focus_change", False),
            insufficient=True,
            lexical_profile=args.profile,
        )

        def metrics(result, case=case):
            page_ids = {span.page_id for unit in result.units for span in unit.positions}
            reference = set(case["references"])
            return {
                "page_ids": sorted(page_ids),
                "reference_pages_recovered": sorted(reference & page_ids),
                "reference_page_recall": len(reference & page_ids) / len(reference),
                "reference_page_precision": len(reference & page_ids) / len(page_ids) if page_ids else 0,
                "documents": sorted({u.document_id for u in result.units}),
                "chars": result.chars_used,
                "units": len(result.units),
                "ids": [u.id for u in result.units],
                "trace": result.trace,
            }

        records.append(
            {
                "id": case["id"],
                "question": case["question"],
                "resolved_query": plan.academic_query,
                "focus_change": case.get("explicit_focus_change", False),
                "initial": metrics(attempts.initial),
                "expanded": metrics(attempts.delivered),
            }
        )
    result = {
        "control_sha256": hashlib.sha256(raw).hexdigest(),
        "lexical_profile": args.profile,
        "records": records,
        "mean_initial_reference_page_recall": sum(r["initial"]["reference_page_recall"] for r in records)
        / len(records),
        "mean_expanded_reference_page_recall": sum(r["expanded"]["reference_page_recall"] for r in records)
        / len(records),
        "reference_page_metrics_only_not_claim_support_or_response_coverage": True,
        "cpu_only_no_models_or_embeddings": True,
        "publication_allowed": False,
    }
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "initial_recall": result["mean_initial_reference_page_recall"],
                "expanded_recall": result["mean_expanded_reference_page_recall"],
                "cases": [
                    {
                        "id": r["id"],
                        "initial": r["initial"]["reference_page_recall"],
                        "expanded": r["expanded"]["reference_page_recall"],
                    }
                    for r in records
                ],
            }
        )
    )


if __name__ == "__main__":
    main()
