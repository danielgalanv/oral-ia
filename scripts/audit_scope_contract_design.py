"""Offline design probe only; no provider, inference, or reinterpretation of trial."""

import json
from pathlib import Path

from oralia.course_dialogue.scope_classifier import ScopeSelection, bind_selection

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
OUTPUT = EVIDENCE / "scope-contract-design-audit-2026-10-26.json"


def dependent_fields(primary_intent):
    """Illustrative v2 projection, not a semantic classifier or runnable successor."""
    return {
        "included_request": ("in_scope", False),
        "included_with_supporting_mention": ("in_scope", False),
        "excluded_standalone_request": ("out_of_scope", True),
        "included_and_excluded_standalone_requests": ("mixed", True),
        "unclear_request": ("uncertain_scope", False),
        "session_operation": ("operational", False),
    }[primary_intent]


def main():
    if OUTPUT.exists():
        raise ValueError("preserve previous audit")
    records = json.loads((EVIDENCE / "scope-classifier-resource-v2/records.json").read_text(encoding="utf-8"))
    policy = json.loads((EVIDENCE / "course-scope-policy-v1.json").read_text(encoding="utf-8"))
    first = json.loads(records[0]["request"]["student_input"])
    assert first["question"] == first["resolved_query_hint_not_authority"]
    assert first["shown_history"] == []
    assert all(isinstance(value, str) for value in first["included_blocks"])
    second_raw = json.loads(records[1]["exchange"]["raw_worker_response"])
    second = ScopeSelection.model_validate_json(second_raw["text"])
    assert second.status == "out_of_scope" and second.excluded_block == "gestion_configuracion"
    assert second.standalone is False
    rejected = False
    try:
        bind_selection(second, records[1]["input"]["text"], [], policy, first["policy_sha256"])
    except ValueError as error:
        rejected = str(error) == "scope exclusion is not standalone"
    assert rejected
    projections = {
        name: dependent_fields(name)
        for name in (
            "included_request",
            "included_with_supporting_mention",
            "excluded_standalone_request",
            "included_and_excluded_standalone_requests",
            "unclear_request",
            "session_operation",
        )
    }
    assert projections["included_with_supporting_mention"] == ("in_scope", False)
    assert projections["excluded_standalone_request"] == ("out_of_scope", True)
    assert projections["included_and_excluded_standalone_requests"] == ("mixed", True)
    unknown_rejected = False
    try:
        dependent_fields("foreign_intent")
    except KeyError:
        unknown_rejected = True
    assert unknown_rejected
    OUTPUT.write_text(
        json.dumps(
            {
                "source": "unchanged_first_trial_records",
                "s01_hint_equals_question": True,
                "s01_has_no_history": True,
                "included_blocks_are_ids_without_descriptions": True,
                "s02_original_still_rejected": rejected,
                "illustrative_v2_dependent_fields": projections,
                "foreign_primary_intent_rejected": unknown_rejected,
                "model_semantics_tested": False,
                "new_inferences": 0,
                "s01_fixed": False,
                "trial_outputs_repaired": False,
                "publication_allowed": False,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print("Offline audit passed; six projections, unknown intent rejected; original S02 still rejected.")


if __name__ == "__main__":
    main()
