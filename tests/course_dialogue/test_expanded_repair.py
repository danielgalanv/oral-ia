"""Opt-in repair boundary contracts; no model or GPU."""

import asyncio
import json

import pytest
from pydantic import ValidationError

from oralia.course_dialogue.cached_transformers import CachedTransformersGenerationAdapter
from oralia.course_dialogue.generation_limits import REPAIR_PROFILE, validate_budget_frame
from oralia.course_dialogue.lab_request import (
    LabGenerationConstraints,
    RepairGenerationConstraints,
    RepairGenerationMessage,
    RepairGenerationRequest,
)
from oralia.course_dialogue.review_repair import CallBudget, ReviewRepairGenerationAdapter
from oralia.infrastructure.generation.generation_port import GenerationError, GenerationMessage
from tests.course_dialogue.test_cached_adapter import Process


class RepairPipe(Process):
    def __init__(self, text="respuesta", reason="stop"):
        super().__init__(reason)
        self.text = text

    async def readline(self):
        row = json.loads(await super().readline())
        row.update(text=self.text, budget_profile=REPAIR_PROFILE)
        return json.dumps(row).encode()


def request(**kwargs):
    return RepairGenerationRequest(purpose="explicacion", instruction="synthetic", **kwargs)


def test_types_preserve_defaults_and_bound_exact_expanded_capacity():
    assert LabGenerationConstraints().model_dump()["max_tokens"] == 768
    assert LabGenerationConstraints().deadline_ms == 50000
    assert RepairGenerationConstraints().max_tokens == 2048
    assert RepairGenerationConstraints().deadline_ms == 180000
    for values in ({"max_tokens": 2049}, {"deadline_ms": 180001}):
        with pytest.raises(ValidationError):
            RepairGenerationConstraints(**values)
    with pytest.raises(ValidationError):
        LabGenerationConstraints(max_tokens=2048)
    assert len(RepairGenerationMessage(role="assistant", content="x" * 16000).content) == 16000
    with pytest.raises(ValidationError):
        RepairGenerationMessage(role="assistant", content="x" * 16001)
    with pytest.raises(ValidationError):
        GenerationMessage(role="assistant", content="x" * 4001)
    with pytest.raises(ValidationError):
        request(output_schema={"type": "object"})


def test_expanded_builder_supplies_exact_source_index_without_changing_evidence():
    from oralia.course_dialogue.review_repair import AdvisoryReview

    evidence = [
        {
            "fragment_id": "source:1",
            "document_id": "document",
            "document_version": 2,
            "text": "actual evidence",
        }
    ]
    req = request(evidence=evidence)
    built = ReviewRepairGenerationAdapter.repair_request(
        req, "candidate", AdvisoryReview(status="no_issues_found", issues=[])
    )
    assert built.evidence == req.evidence
    assert json.loads(built.student_input)["source_index"] == [
        {"fragment_id": "source:1", "document_id": "document", "document_version": 2}
    ]
    assert "marcador literal" in built.instruction


@pytest.mark.parametrize(
    "frame,enabled",
    [
        ({"max_tokens": 2049, "deadline_ms": 180000, "budget_profile": REPAIR_PROFILE}, True),
        ({"max_tokens": 2048, "deadline_ms": 180001, "budget_profile": REPAIR_PROFILE}, True),
        ({"max_tokens": 2048, "deadline_ms": 180000, "budget_profile": REPAIR_PROFILE}, False),
        ({"max_tokens": 769, "deadline_ms": 50000}, True),
        ({"max_tokens": 768, "deadline_ms": 50001}, True),
        ({"max_tokens": 1, "deadline_ms": 1, "budget_profile": "unknown"}, True),
        (
            {
                "max_tokens": 2048,
                "deadline_ms": 180000,
                "budget_profile": REPAIR_PROFILE,
                "finite_outputs": ["a"],
            },
            True,
        ),
    ],
)
def test_shared_worker_validation_rejects_invalid_or_disabled_profiles(frame, enabled):
    with pytest.raises(ValueError):
        validate_budget_frame(frame, repair_enabled=enabled)


async def test_exact_budget_serialization_long_text_and_timeout_are_not_clipped(monkeypatch):
    pipe = RepairPipe("x" * 12000)
    adapter = CachedTransformersGenerationAdapter(pipe, repair_profile_enabled=True)
    observed = []
    real_wait = asyncio.wait_for

    async def wait(awaitable, timeout):
        observed.append(timeout)
        return await real_wait(awaitable, timeout)

    monkeypatch.setattr(asyncio, "wait_for", wait)
    result = await adapter.generate(
        request(conversation_history=[{"role": "assistant", "content": "h" * 12000}])
    )
    assert result.text == "x" * 12000 and result.ok
    assert pipe.payload["max_tokens"] == 2048 and pipe.payload["deadline_ms"] == 180000
    assert pipe.payload["budget_profile"] == REPAIR_PROFILE
    assert pipe.payload["finite_outputs"] is None
    assert observed == [182]
    assert result.parameters["max_tokens_capacity"] == 2048
    assert validate_budget_frame(pipe.payload, repair_enabled=True) == REPAIR_PROFILE


async def test_expanded_request_requires_provider_opt_in_before_pipe_write():
    pipe = RepairPipe()
    with pytest.raises(GenerationError, match="opt-in"):
        await CachedTransformersGenerationAdapter(pipe).generate(request())
    assert pipe.payload is None


async def test_expanded_profile_cannot_enter_self_review_or_other_stages():
    port = ReviewRepairGenerationAdapter(None, budget=CallBudget(), revalidate=lambda: None)
    with pytest.raises(ValueError, match="self-review"):
        await port.generate(request())
    with pytest.raises(ValueError, match="self-review"):
        port.review_request(request(), "candidate")
    with pytest.raises(ValueError, match="repair calls only"):
        await port.call("draft", request(), {"calls": []})
    assert port.budget.used == 0


async def test_output_over_capacity_and_unconfirmed_profile_rejected():
    pipe = RepairPipe("x" * 16001)
    with pytest.raises(GenerationError, match="no clipping"):
        await CachedTransformersGenerationAdapter(pipe, repair_profile_enabled=True).generate(request())
    with pytest.raises(GenerationError, match="confirm"):
        await CachedTransformersGenerationAdapter(Process(), repair_profile_enabled=True).generate(request())


async def test_expanded_timeout_and_cancellation_stop_owned_transport():
    for cancel in (False, True):
        pipe = RepairPipe()
        entered = asyncio.Event()

        async def waiting(entered=entered):
            entered.set()
            await asyncio.Event().wait()

        pipe.stdout.readline = waiting
        adapter = CachedTransformersGenerationAdapter(pipe, repair_profile_enabled=True)
        task = asyncio.create_task(adapter.generate(request(constraints={"deadline_ms": 1})))
        await entered.wait()
        if cancel:
            task.cancel()
        with pytest.raises(asyncio.CancelledError if cancel else GenerationError):
            await task
        assert not adapter.usable and pipe.returncode == -15


async def test_outer_call_preserves_180_seconds_budget_and_rejects_late_cancel_suppression(monkeypatch):
    from oralia.infrastructure.generation.generation_port import GenerationOutcome

    seen = []
    real_timeout = asyncio.timeout_at

    def record(deadline):
        seen.append(deadline - asyncio.get_running_loop().time())
        return real_timeout(deadline)

    monkeypatch.setattr(asyncio, "timeout_at", record)

    class Provider:
        async def generate(self, req):
            return GenerationOutcome(ok=True, text="x" * 12000, adapter="deterministic", finish_reason="stop")

    port = ReviewRepairGenerationAdapter(
        Provider(), budget=CallBudget(maximum=1, seconds=300), revalidate=lambda: None
    )
    row = {"calls": []}
    result = await port.call("repair", request(), row)
    assert len(result.text) == 12000 and 179 < seen[0] <= 180
    assert len(row["calls"]) == 1 and port.budget.used == 1

    class Late:
        async def generate(self, req):
            try:
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                pass
            return GenerationOutcome(ok=True, text="late", adapter="deterministic", finish_reason="stop")

    port = ReviewRepairGenerationAdapter(Late(), budget=CallBudget(maximum=1), revalidate=lambda: None)
    with pytest.raises(TimeoutError):
        await port.call("repair", request(constraints={"deadline_ms": 1}), {"calls": []})
