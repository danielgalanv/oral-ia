"""Lab ledger tests: structural safety, not semantic approval of its labels."""

import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from oralia.course_dialogue.claim_review import ClaimReview, aggregate_review
from oralia.course_dialogue.corpus import load_catalog

ROOT = Path(__file__).resolve().parents[2]
CONTROLS = ROOT / "specs/012-conversational-course-study/evidence/chat-claim-ledger-derived-controls.json"


def records():
    artifact = json.loads(CONTROLS.read_text(encoding="utf-8"))
    assert artifact["actual_transcript"] is False
    pages = {page["id"]: page["text"] for page in load_catalog()}
    return artifact["cases"], pages


def review_of(row):
    return tuple(
        ClaimReview(**{**claim, "premise_quotes": tuple(claim["premise_quotes"])}) for claim in row["claims"]
    )


def aggregate(row, claims, pages):
    return aggregate_review(row["answer"], claims, pages, tuple(row["required_central_quotes"]))


def test_derived_pairs_have_positive_and_negative_controls():
    cases, pages = records()
    assert len(cases) == 6
    decisions = {row["id"]: aggregate(row, review_of(row), pages) for row in cases}
    assert all(decisions[row["id"]] == row["expected_aggregate"] for row in cases)
    assert list(decisions.values()).count("supported") == 3
    assert list(decisions.values()).count("unsupported") == 3
    assert all(row["kind"] == "derived_control_not_actual_transcript" for row in cases)


def test_control_sources_match_frozen_original_pages():
    artifact = json.loads(CONTROLS.read_text(encoding="utf-8"))
    _, pages = records()
    assert {
        source_id: hashlib.sha256(pages[source_id].encode()).hexdigest()
        for source_id in artifact["source_page_sha256"]
    } == artifact["source_page_sha256"]


def test_unsupported_central_claim_cannot_be_hidden_by_supported_explanation():
    cases, pages = records()
    row = cases[0]
    claims = review_of(row)
    assert claims[0].verdict == "supported"
    assert claims[-1].central and claims[-1].verdict == "unsupported"
    assert aggregate(row, claims, pages) == "unsupported"


def test_unknown_never_authorizes_and_reject_everything_fails_positive_controls():
    cases, pages = records()
    positive = next(row for row in cases if row["id"] == "B-conditioned-correction")
    claims = review_of(positive)
    uncertain = claims[:-1] + (replace(claims[-1], verdict="unknown", rationale="Fuente insuficiente"),)
    assert aggregate(positive, uncertain, pages) == "unknown"
    reject_all = tuple(
        (
            replace(claim, verdict="unsupported", rationale="rechazo automático")
            if claim.kind != "fiction"
            else claim
        )
        for claim in claims
    )
    assert aggregate(positive, reject_all, pages) != positive["expected_aggregate"]


@pytest.mark.parametrize("mutation", ["span", "source", "premise", "coverage"])
def test_ledger_rejects_untraceable_or_omitted_claims(mutation):
    cases, pages = records()
    row = next(item for item in cases if item["id"] == "B-conditioned-correction")
    claims = review_of(row)
    if mutation == "span":
        claims = claims[:-1] + (replace(claims[-1], start=0),)
    elif mutation == "source":
        claims = claims[:-1] + (replace(claims[-1], source_passage="pasaje inventado"),)
    elif mutation == "premise":
        claims = claims[:-1] + (replace(claims[-1], premise_quotes=("premisa inventada",)),)
    else:
        claims = claims[:-1]
    with pytest.raises(ValueError):
        aggregate(row, claims, pages)


@pytest.mark.parametrize(
    "mutation",
    [
        {"end": "beyond_answer"},
        {"premise_quotes": ("",)},
        {"premise_quotes": ("   ",)},
        {"premise_quotes": (None,)},
        {"premise_quotes": "duplicate_real_premise"},
        {"quote": ""},
        {"source_passage": ""},
    ],
)
def test_ledger_rejects_malformed_claim_fields(mutation):
    cases, pages = records()
    row = next(item for item in cases if item["id"] == "B-conditioned-correction")
    claims = review_of(row)
    if mutation.get("end") == "beyond_answer":
        changed = replace(claims[-1], end=len(row["answer"]) + 100)
    elif mutation.get("premise_quotes") == "duplicate_real_premise":
        premise = claims[-1].premise_quotes[0]
        changed = replace(claims[-1], premise_quotes=(premise, premise))
    else:
        changed = replace(claims[-1], **mutation)
    with pytest.raises(ValueError):
        aggregate(row, claims[:-1] + (changed,), pages)
