"""Offline runner safety, receipts, frozen bank and independent dispatch accounting."""

import json
from types import SimpleNamespace

import pytest
from frozen_scope_fixture import archived_root

from oralia.infrastructure.generation.generation_port import GenerationOutcome, GenerationRequest
from scripts import trial_scope_finite as runner


def frozen_inputs(tmp_path):
    return runner.frozen_inputs(root=archived_root(runner.PACKAGE, runner.ROOT, tmp_path))


def test_live_tree_replay_is_still_rejected():
    with pytest.raises(ValueError, match="frozen artifact changed"):
        runner.frozen_inputs()


def test_frozen_manifest_and_counts(tmp_path):
    bank, oracle, protocol, _ = frozen_inputs(tmp_path)
    assert len(bank) == len(oracle) == 18
    assert protocol["new_call_limit"] == 72
    assert set(c["id"] for c in bank) == set(oracle)
    assert len({oracle[c["id"]]["included_block"] for c in bank[:9]}) == 9


def test_changed_manifest_is_rejected(tmp_path):
    target = tmp_path / "input.txt"
    target.write_text("original", encoding="utf-8")
    (tmp_path / "manifest.json").write_text(
        json.dumps({"input.txt": runner.digest(target)}), encoding="utf-8"
    )
    target.write_text("changed", encoding="utf-8")
    with pytest.raises(ValueError, match="artifact changed"):
        runner.frozen_inputs(tmp_path, tmp_path)


class Port:
    def __init__(self, answers, budget_path=None):
        self.answers = iter(answers)
        self.requests = []
        self.last_exchange = None
        self.budget_path = budget_path

    async def generate(self, request):
        if self.budget_path is not None:
            assert json.loads(self.budget_path.read_text(encoding="utf-8"))["used"] == len(self.requests) + 1
        self.requests.append(request)
        text = json.dumps(next(self.answers))
        self.last_exchange = {
            "raw_worker_response": json.dumps(
                {"finite_decoder": True, "text": text, "message_profile": "scope-control-finite/v1"}
            )
        }
        return GenerationOutcome(
            ok=True,
            text=text,
            adapter="deterministic",
            finish_reason="stop",
            parameters={"finite_decoder": True},
        )


@pytest.mark.asyncio
async def test_dispatch_accounting_partial_receipts_and_stop_do_not_touch_old_budget(tmp_path):
    bank, oracle, protocol, _ = frozen_inputs(tmp_path)
    policy_path = runner.EVIDENCE / "course-scope-policy-v1.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    metadata_value = json.loads(
        (runner.EVIDENCE / "course-block-descriptions-v1.json").read_text(encoding="utf-8")
    )
    binding = SimpleNamespace(
        policy_sha256=runner.digest(policy_path),
        revalidate=lambda *_: policy,
        assert_decision=lambda *_: None,
    )
    metadata = SimpleNamespace(sha256="fixture", revalidate=lambda *_: metadata_value)
    old = tmp_path / "old.json"
    old.write_text('{"used":2}', encoding="utf-8")
    previous = old.read_bytes()
    budget = tmp_path / "finite.json"
    provider = Port(
        [
            {"intent": "included", "block": "introduccion_ingenieria_software"},
            {"intent": "excluded_standalone", "block": "seguridad"},
        ],
        budget,
    )

    async def resources():
        return True

    records, rows, reason = await runner.run_questions(
        bank,
        oracle,
        protocol,
        provider=provider,
        binding=binding,
        db=None,
        metadata=metadata,
        output=tmp_path,
        budget_path=budget,
        proposal_hash="finite-only",
        resource_check=resources,
    )
    assert len(provider.requests) == 2 and reason == "first_critical_failure"
    assert old.read_bytes() == previous
    assert json.loads(budget.read_text())["used"] == 2
    assert records[1]["steps"][0]["outcome"] is not None
    assert (tmp_path / "F02.partial.json").exists()
    assert records[1]["attempts"][0]["outcome"]["text"] == json.dumps(
        {"intent": "excluded_standalone", "block": "seguridad"}
    )
    payload = json.loads(provider.requests[0].student_input)
    assert "oracle" not in payload and "expected" not in payload and "witnesses" not in payload
    assert len(payload["blocks"]["blocks"]) == 21
    summary = runner.summarize(bank, oracle, rows)
    assert summary["not_executed"] == 16 and summary["false_exclusion"] == 1
    assert summary["finite_enforced"] == summary["finite_completed"] == 2
    assert summary["positive_blocks"]["modelos_sistema"] is None


@pytest.mark.asyncio
async def test_question_and_step_limits_are_joint_before_send(tmp_path):
    _, _, protocol, _ = frozen_inputs(tmp_path)
    now = [0.0]
    provider = Port([{"a": 1}] * 4)
    record = {"id": "fixture"}
    budget = tmp_path / "budget.json"
    port = runner.QuestionPort(provider, record, tmp_path, budget, "trial", protocol, clock=lambda: now[0])
    req = GenerationRequest(purpose="explicacion", instruction="fixture")
    req = req.model_copy(update={"constraints": req.constraints.model_copy(update={"max_tokens": 128})})
    for step in ["target", "referent", "included_part", "excluded_standalone_part"]:
        cap = 32 if step == "referent" else 128
        port.receipt_sink(({"step": step},))
        await port.generate(
            req.model_copy(update={"constraints": req.constraints.model_copy(update={"max_tokens": cap})})
        )
        now[0] += 1
    assert len(provider.requests) == 4
    port.receipt_sink(({"step": "supporting_mention"},))
    with pytest.raises(ValueError, match="limit exceeded"):
        await port.generate(req)
    assert len(provider.requests) == 4
    deadlines = [r.constraints.deadline_ms for r in provider.requests]
    assert deadlines == sorted(deadlines, reverse=True)
    assert json.loads(budget.read_text())["used"] == 4
    now[0] = 29.5
    with pytest.raises(TimeoutError):
        await port.generate(req)
    assert len(provider.requests) == 4


@pytest.mark.asyncio
async def test_total_tokens_global_calls_and_pressure_block_before_send(tmp_path):
    _, _, protocol, _ = frozen_inputs(tmp_path)
    provider = Port([{"a": 1}] * 3)
    budget = tmp_path / "budget.json"
    port = runner.QuestionPort(provider, {"id": "fixture"}, tmp_path, budget, "trial", protocol)
    req = GenerationRequest(purpose="explicacion", instruction="fixture")
    for name, cap in [("target", 128), ("included_part", 176), ("supporting_mention", 176)]:
        port.receipt_sink(({"step": name},))
        await port.generate(
            req.model_copy(update={"constraints": req.constraints.model_copy(update={"max_tokens": cap})})
        )
    port.receipt_sink(({"step": "excluded_standalone_part"},))
    with pytest.raises(ValueError, match="token limit"):
        await port.generate(
            req.model_copy(update={"constraints": req.constraints.model_copy(update={"max_tokens": 176})})
        )
    assert len(provider.requests) == 3
    runner.save(budget, {"proposal_sha256": "trial", "limit": 72, "used": 72, "questions": {}})
    with pytest.raises(ValueError, match="call limit"):
        await port.generate(
            req.model_copy(update={"constraints": req.constraints.model_copy(update={"max_tokens": 128})})
        )
    port.stop_requested = lambda: True
    with pytest.raises(runner.ResourcePressureStop):
        await port.generate(req)
    assert len(provider.requests) == 3
