"""Preparation contains sources and criteria, not an answer-producing fixture."""

import hashlib
import json
from pathlib import Path

from scripts.prepare_study_review_cpu import build_review


def test_prepared_review_is_not_an_executed_or_canned_answer_bank():
    root = Path(__file__).resolve().parents[2]
    folder = root / "specs/012-conversational-course-study/evidence/study-review-preparation-v1"
    raw = (folder / "review.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == (folder / "review.sha256").read_text()
    packet = json.loads(raw)
    assert [q["act"] for q in packet["questions"]] == [
        "explanation",
        "reformulation",
        "hypothetical_example",
        "topic_switch",
    ]
    assert packet["state"] == "prepared_not_executed_not_validated"
    assert packet["no_predefined_model_answers"] is True
    assert packet["publication_allowed"] is False
    assert packet["independent_semantic_evaluator_available"] is False
    assert all("answer" not in q and "response" not in q for q in packet["questions"])
    assert all(q["requires_shown_previous"] for q in packet["questions"][1:])
    assert all(ref in packet["reference_passages"] for q in packet["questions"] for ref in q["reference_ids"])
    for source in packet["reference_passages"].values():
        assert hashlib.sha256(source["text"].encode()).hexdigest() == source["text_sha256"]
    pages = [{"id": key, **value} for key, value in packet["reference_passages"].items()]
    assert build_review(pages) == packet
