"""Synthetic review/repair contract tests; no semantic capability implied."""

import asyncio
import json

import pytest

from oralia.course_dialogue.lab_request import LabGenerationRequest
from oralia.course_dialogue.review_repair import (
    CallBudget,
    ReviewRepairGenerationAdapter,
    parse_review,
)
from oralia.infrastructure.generation.generation_port import GenerationOutcome


def request():
    return LabGenerationRequest(
        purpose="explicacion",
        instruction="fixture original",
        student_input="fixture question",
        evidence=[
            {
                "fragment_id": "fixture:1",
                "document_id": "fixture-document",
                "document_version": 2,
                "text": "Fixture evidence\nalpha is allowed; beta is constrained.",
            }
        ],
    )


def outcome(text, reason="stop"):
    return GenerationOutcome(ok=reason == "stop", text=text, adapter="deterministic", finish_reason=reason)


def review(status="issues_found", **overrides):
    issue = {
        "kind": "contradiction",
        "claim": "alpha is forbidden",
        "explanation": "fixture mismatch",
        "evidence": [{"source_id": "fixture:1", "quote": "alpha is allowed"}],
    }
    issue.update(overrides)
    return json.dumps({"status": status, "issues": [issue] if status == "issues_found" else []})


class ProviderFixture:
    def __init__(self, results):
        self.results = iter(results)
        self.requests = []
        self.last_exchange = None

    async def generate(self, req):
        self.requests.append(req)
        self.last_exchange = {"raw_worker_response": "fixture wire"}
        return next(self.results)


@pytest.mark.asyncio
async def test_one_round_exact_context_and_budgets_without_promotion():
    provider = ProviderFixture(
        [
            outcome("alpha is forbidden"),
            outcome(review()),
            outcome("alpha is allowed"),
            outcome(review("no_issues_found")),
        ]
    )
    checks = []
    port = ReviewRepairGenerationAdapter(
        provider, budget=CallBudget(), revalidate=lambda: checks.append(True)
    )
    final = await port.generate(request())
    trace = port.last_review_trace
    assert final.text == "alpha is allowed"
    assert [c["stage"] for c in trace["calls"]] == ["draft", "review", "repair", "post_review"]
    assert trace["initial"]["text"] == "alpha is forbidden"
    assert trace["semantic_support"] == "unverified" and not trace["publication_allowed"]
    assert not trace["independent_semantics"]
    assert all(r.evidence == request().evidence for r in provider.requests)
    assert all(
        r.constraints.deadline_ms == 50000 and r.constraints.max_tokens == 768 for r in provider.requests
    )
    assert len(checks) == 8 and provider.last_exchange is None
    port.clear_diagnostic()
    assert port.last_review_trace is None


@pytest.mark.asyncio
async def test_no_findings_never_trigger_repair_or_become_supported():
    p = ProviderFixture([outcome(review("no_issues_found"))])
    port = ReviewRepairGenerationAdapter(p, budget=CallBudget(), revalidate=lambda: None)
    final = await port.process(request(), outcome("alpha is allowed"))
    assert final.text == "alpha is allowed" and len(p.requests) == 1
    assert not port.last_review_trace["repair_attempted"]
    assert port.last_review_trace["semantic_support"] == "unverified"


@pytest.mark.parametrize(
    "payload",
    [
        review(evidence=[{"source_id": "foreign", "quote": "alpha is allowed"}]),
        review(evidence=[{"source_id": "fixture:1", "quote": "alpha is not allowed"}]),
        review(claim="not in candidate"),
        review(evidence=[]),
        '{"status":"supported","issues":[]}',
        "```json\n{}\n```",
    ],
)
def test_fabricated_witness_invalid_claim_and_positive_authority_rejected(payload):
    with pytest.raises(ValueError):
        parse_review(payload, request(), "alpha is forbidden")


def test_only_whitespace_normalization_is_allowed():
    payload = review(evidence=[{"source_id": "fixture:1", "quote": "Fixture evidence alpha is allowed"}])
    assert parse_review(payload, request(), "alpha is forbidden").status == "issues_found"
    with pytest.raises(ValueError):
        parse_review(
            review(evidence=[{"source_id": "fixture:1", "quote": " "}]), request(), "alpha is forbidden"
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("stage", ["review", "repair", "post_review"])
async def test_incomplete_text_is_never_silently_stitched(stage):
    results = [outcome(review()), outcome("alpha is allowed"), outcome(review("no_issues_found"))]
    idx = ["review", "repair", "post_review"].index(stage)
    results[idx] = outcome("partial", "length")
    p = ProviderFixture(results)
    port = ReviewRepairGenerationAdapter(p, budget=CallBudget(), revalidate=lambda: None)
    final = await port.process(request(), outcome("alpha is forbidden"))
    assert final.text == ("alpha is allowed" if stage == "post_review" else "alpha is forbidden")
    assert len(p.requests) == idx + 1
    assert "partial" != final.text


@pytest.mark.asyncio
async def test_invalid_review_blocks_repair_and_preserves_raw():
    p = ProviderFixture([outcome("not JSON")])
    port = ReviewRepairGenerationAdapter(p, budget=CallBudget(), revalidate=lambda: None)
    final = await port.process(request(), outcome("alpha is forbidden"))
    assert final.text == "alpha is forbidden"
    assert port.last_review_trace["status"] == "review_invalid"
    assert port.last_review_trace["calls"][0]["outcome"]["text"] == "not JSON"


@pytest.mark.asyncio
async def test_source_change_after_review_prevents_repair():
    checks = 0

    def validate():
        nonlocal checks
        checks += 1
        if checks == 2:
            raise ValueError("withdrawn during review")

    p = ProviderFixture([outcome(review())])
    port = ReviewRepairGenerationAdapter(p, budget=CallBudget(), revalidate=validate)
    with pytest.raises(ValueError, match="withdrawn"):
        await port.process(request(), outcome("alpha is forbidden"))
    assert len(p.requests) == 1 and p.last_exchange is None


@pytest.mark.asyncio
async def test_budget_counts_every_stage_and_cannot_be_renewed_by_repair():
    p = ProviderFixture([outcome(review())])
    budget = CallBudget(maximum=1)
    port = ReviewRepairGenerationAdapter(p, budget=budget, revalidate=lambda: None)
    with pytest.raises(ValueError, match="budget exhausted"):
        await port.process(request(), outcome("alpha is forbidden"))
    assert budget.used == 1 and len(p.requests) == 1


@pytest.mark.asyncio
async def test_late_provider_ignoring_cancel_does_not_complete_stage():
    class Late:
        last_exchange = None

        async def generate(self, req):
            try:
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                pass
            return outcome(review())

    budget = CallBudget(seconds=0.02)
    port = ReviewRepairGenerationAdapter(Late(), budget=budget, revalidate=lambda: None)
    with pytest.raises(TimeoutError):
        await port.process(request(), outcome("alpha is forbidden"))


@pytest.mark.asyncio
async def test_existing_diagnostic_surface_records_both_versions_and_only_final_history():
    from tests.unit.test_study_lab import setup

    lab, _, _ = setup()
    # The review deliberately has no issue: proves the advisory state is not a
    # fabricated supported verdict and the candidate is acknowledged separately.
    p = ProviderFixture([outcome("fixture candidate"), outcome(review("no_issues_found"))])
    lab.provider = ReviewRepairGenerationAdapter(p, budget=CallBudget(), revalidate=lab.validate)
    result = await lab.turn("fixture question", "fixture-request")
    row = lab.display(result["id"])
    assert row["workflow_deadline_seconds"] == 200
    assert row["review_repair"]["initial"]["text"] == "fixture candidate"
    assert row["semantic_support"] == "unverified" and not row["publication_allowed"]
    assert lab.history == [] and lab.provider.last_review_trace is None
    lab.acknowledge(result["id"])
    assert lab.history == [{"question": "fixture question", "text": "fixture candidate"}]
    lab.close()
    assert lab.receipts == {} and lab.history == []


@pytest.mark.asyncio
async def test_concurrent_diagnostic_sessions_do_not_share_workflow_trace():
    from oralia.course_dialogue.review_repair import REVIEW_INSTRUCTION
    from oralia.documentary.study_lab import DiagnosticStudy, TrialBudget
    from tests.unit.test_study_lab import RetrievalFixture

    class ConcurrentFixture:
        last_exchange = None

        async def generate(self, req):
            await asyncio.sleep(0.01)
            return outcome(
                review("no_issues_found") if req.instruction == REVIEW_INSTRUCTION else req.student_input
            )

    r = RetrievalFixture()
    global_port = ReviewRepairGenerationAdapter(
        ConcurrentFixture(), budget=CallBudget(), revalidate=r.revalidate
    )

    def session():
        return DiagnosticStudy(
            r, global_port, authority=lambda: True, budget=TrialBudget(), course="test", activity="test"
        )

    a, b = session(), session()
    ra, rb = await asyncio.gather(a.turn("session A", "a"), b.turn("session B", "b"))
    assert a.display(ra["id"])["review_repair"]["initial"]["text"] == "session A"
    assert b.display(rb["id"])["review_repair"]["initial"]["text"] == "session B"
    assert a.provider is not b.provider and global_port.last_review_trace is None


@pytest.mark.asyncio
async def test_repaired_text_alone_enters_the_displayed_history():
    from tests.unit.test_study_lab import setup

    issue = {
        "status": "issues_found",
        "issues": [
            {
                "kind": "unsupported",
                "claim": "FIXTURE INITIAL",
                "explanation": "fixture-only critique",
                "evidence": [],
            }
        ],
    }
    p = ProviderFixture(
        [
            outcome("FIXTURE INITIAL"),
            outcome(json.dumps(issue)),
            outcome("FIXTURE REPAIRED"),
            outcome(review("no_issues_found")),
        ]
    )
    lab, _, _ = setup()
    port = ReviewRepairGenerationAdapter(p, budget=CallBudget(), revalidate=lab.validate)
    lab.provider = port.for_session(lab.validate)
    result = await lab.turn("fixture question", "fixture-repair")
    row = lab.display(result["id"])
    assert row["diagnostic_preview"] == "FIXTURE REPAIRED"
    assert row["review_repair"]["initial"]["text"] == "FIXTURE INITIAL"
    assert lab.history == []
    lab.acknowledge(result["id"])
    assert lab.history == [{"question": "fixture question", "text": "FIXTURE REPAIRED"}]


@pytest.mark.asyncio
async def test_supplied_agent_review_uses_only_corrector_and_leaves_post_review_pending():
    p = ProviderFixture([outcome("alpha is allowed")])
    port = ReviewRepairGenerationAdapter(p, budget=CallBudget(), revalidate=lambda: None)
    final = await port.repair_with_supplied_review(
        request(), outcome("alpha is forbidden"), json.loads(review())
    )
    assert final.text == "alpha is allowed" and len(p.requests) == 1
    trace = port.last_review_trace
    assert [c["stage"] for c in trace["calls"]] == ["repair"]
    assert trace["status"] == "repaired_external_post_review_pending"
    assert trace["reviewer"] == "supplied_agent_review_not_autonomous"
    assert "post_review" not in trace and trace["publication_allowed"] is False


@pytest.mark.asyncio
async def test_bad_supplied_witness_never_reaches_corrector():
    p = ProviderFixture([])
    port = ReviewRepairGenerationAdapter(p, budget=CallBudget(), revalidate=lambda: None)
    with pytest.raises(ValueError):
        await port.repair_with_supplied_review(
            request(), outcome("alpha is forbidden"), json.loads(review(claim="invented candidate phrase"))
        )
    assert p.requests == []
