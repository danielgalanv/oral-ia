"""Diagnostic result categories must not turn class errors into semantic failures."""

import json
from pathlib import Path

import pytest

from oralia.course_dialogue.corpus import load_catalog
from scripts.closed_reference_claim_trial import finite_request, premise_options, source_options
from scripts.trial_chat_claim_reviewer import classify_mismatch

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    ("kind", "verdict", "expected", "reason"),
    [
        ("conclusion", "supported", {"kind": "general", "verdict": "supported"}, "classification_mismatch"),
        ("general", "supported", {"kind": "general", "verdict": "unsupported"}, "false_permission"),
        ("general", "unsupported", {"kind": "general", "verdict": "supported"}, "false_rejection"),
        ("general", "unknown", {"kind": "general", "verdict": "supported"}, "unknown_mismatch"),
        ("general", "supported", {"kind": "general", "verdict": "supported"}, None),
    ],
)
def test_distinct_claim_trial_outcomes(kind, verdict, expected, reason):
    assert classify_mismatch(kind, verdict, expected) == reason


def test_closed_references_are_real_and_oracle_is_absent_from_request():
    root = ROOT / "specs/012-conversational-course-study/evidence"
    inputs = json.loads((root / "chat-closed-ref-inputs.json").read_text(encoding="utf-8"))
    oracle = json.loads((root / "chat-closed-ref-oracle.json").read_text(encoding="utf-8"))
    pages = {page["id"]: page for page in load_catalog()}
    assert len(inputs["cases"]) == 4
    for case in inputs["cases"]:
        assert set(case["central_quotes"]) == set(oracle[case["id"]])
        for quote in case["central_quotes"]:
            assert case["answer"].count(quote) == 1
            sources = source_options(case, pages)
            assert all(
                value["source_passage"] in pages[value["source_id"]]["text"] for value in sources.values()
            )
            if case["kinds"][quote] == "conclusion":
                premises = premise_options(case, quote)
                assert premises and all(p in case["answer"] and p != quote for p in premises.values())
            request = finite_request(
                case, quote, pages, "verdict", ["supported", "unsupported", "unknown"], "judge", []
            )
            visible = json.loads(request.student_input)
            assert set(visible) == {"question", "answer", "claim_to_review", "fixed_kind", "options"}
            assert "expected" not in visible and "verdict" not in visible
