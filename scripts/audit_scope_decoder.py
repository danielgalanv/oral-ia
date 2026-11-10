"""Offline backend capability audit; no model load, inference or historical repair."""

import json
from pathlib import Path

from oralia.course_dialogue.finite_schema import finite_json_outputs
from oralia.course_dialogue.scope_classifier import ScopeSelection
from oralia.course_dialogue.scope_classifier_v2 import ScopeSelectionV2

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
OUTPUT = EVIDENCE / "scope-decoder-audit-2026-10-26.json"


def finite_target_prototype(policy):
    """Enumerate legal tagged target decisions, not teaching content or truth."""
    outputs = [{"intent": "unclear"}, {"intent": "operation"}]
    for block in policy["included_blocks"]:
        outputs.append({"intent": "included", "block": block})
        outputs.append({"intent": "auxiliary", "anchor": block})
    for excluded in policy["excluded_as_standalone_blocks_for_this_activity"]:
        outputs.append({"intent": "excluded_standalone", "block": excluded})
        for included in policy["included_blocks"]:
            outputs.append({"intent": "mixed", "included_block": included, "excluded_block": excluded})
    return {"type": "object", "x-oralia-finite-outputs": [json.dumps(row) for row in outputs]}


def unique_literal_span(text, quote):
    """Exact match only; no correction, normalization, case folding or guessing."""
    if not quote:
        raise ValueError("empty literal")
    start = text.find(quote)
    if start < 0 or text.find(quote, start + 1) >= 0:
        raise ValueError("literal absent or ambiguous")
    return {"start": start, "end": start + len(quote), "quote": quote}


def main():
    if OUTPUT.exists():
        raise ValueError("preserve audit evidence")
    policy = json.loads((EVIDENCE / "course-scope-policy-v1.json").read_text(encoding="utf-8"))
    assert finite_json_outputs(ScopeSelection.model_json_schema()) is None
    assert finite_json_outputs(ScopeSelectionV2.model_json_schema()) is None
    generic_union = {
        "oneOf": [{"type": "object"}, {"type": "object"}],
        "discriminator": {"propertyName": "intent"},
    }
    assert finite_json_outputs(generic_union) is None
    finite = finite_json_outputs(finite_target_prototype(policy))
    assert len(finite) == 120
    decoded = [json.loads(value) for value in finite]
    assert all("standalone" not in row and "status" not in row for row in decoded)
    assert all("included" not in row and "excluded" not in row for row in decoded)
    assert all(set(row) == {"intent", "block"} for row in decoded if row["intent"] == "included")
    assert all(
        set(row) == {"intent", "included_block", "excluded_block"}
        for row in decoded
        if row["intent"] == "mixed"
    )
    literal = unique_literal_span("¿Pruebas? También diseño.", "También diseño")
    assert "¿Pruebas? También diseño."[literal["start"] : literal["end"]] == "También diseño"
    rejected = []
    for text, quote in [
        ("la prueba y la prueba", "la prueba"),
        ("pruebas", "Pruebas"),
        ("¿Qué estudia en general la Ingeniería del Software?", "Introducción a la Ingeniería del Software"),
        ("texto", ""),
    ]:
        try:
            unique_literal_span(text, quote)
        except ValueError:
            rejected.append(quote)
    assert len(rejected) == 4
    save = {
        "v1_general_schema_constrained": False,
        "v2_general_schema_constrained": False,
        "generic_discriminated_union_constrained": False,
        "finite_tagged_target_alternatives": len(finite),
        "finite_outputs_within_backend_limits": True,
        "prototype_has_no_conditional_null_fields": True,
        "exact_literal_host_offsets_checked": True,
        "absent_ambiguous_empty_literals_rejected": 4,
        "historical_n01_quote_still_rejected": True,
        "model_semantics_measured": False,
        "new_model_calls": 0,
        "publication_allowed": False,
    }
    OUTPUT.write_text(json.dumps(save, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        "Offline decoder audit passed: v1/v2 are hints; 120 finite tagged targets fit; literal guards reject."
    )


if __name__ == "__main__":
    main()
