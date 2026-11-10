"""Corrected-transport diagnostic runner with a fresh 48-call ledger and frozen inputs."""

import json
from types import SimpleNamespace

import pytest

from oralia.course_dialogue.cached_transformers import CachedTransformersGenerationAdapter
from oralia.course_dialogue.scope_message_profiles import validate_frame_profile
from scripts import diagnose_scope_control as diagnostic
from scripts.trial_scope_finite import QuestionPort


def test_new_bank_and_explicit_budget_are_bounded():
    bank, oracle, protocol = diagnostic.build_inputs()
    assert len(bank) == len(oracle) == 12
    assert set(c["id"] for c in bank) == set(oracle)
    assert protocol["new_call_limit"] == 48 and protocol["shared_tokens_per_question"] == 512
    assert protocol["message_profile"] == "scope-control/v1"
    assert sum(e["status"] == "mixed" for e in oracle.values()) == 2
    assert any(e["referent_turn"] == 0 for e in oracle.values())


def test_resident_or_high_own_memory_peak_is_not_a_resource_stop():
    assert not diagnostic.unsafe_resources({"gpu": "100, 15500, 17000"})
    assert diagnostic.unsafe_resources({"gpu": "100, 31500, 1000"})


def test_diagnostic_low_load_policy_preserves_raw_observations():
    samples = [{"gpu": f"{value}, 1644, 30544"} for value in (5, 9, 5, 9, 5)]
    assert diagnostic.diagnostic_preflight(samples)["ready"]
    assert diagnostic.diagnostic_preflight(samples)["max_utilization_percent"] == 9
    assert not diagnostic.diagnostic_preflight(samples[:2])["ready"]
    assert not diagnostic.diagnostic_preflight([{"gpu": "30, 1644, 30544"}] * 5)["ready"]
    assert not diagnostic.diagnostic_preflight([{"gpu": "5, 30000, 2000"}] * 5)["ready"]


def test_resource_summary_uses_all_samples_even_when_monitor_finishes_late():
    samples = [{"gpu": "1, 20000, 12000"}, {"gpu": "30, 31500, 512"}]
    review = diagnostic.final_resource_review(samples, 20000, 5200, set())
    assert review["pressure_observed"] and review["minimum_free_mib"] == 512
    assert review["memory_peak_proves_foreign_activity"] is False


def test_hash_mismatch_prevents_loading(tmp_path):
    path = tmp_path / "file.txt"
    path.write_text("old", encoding="utf-8")
    (tmp_path / "manifest.json").write_text(
        json.dumps({"file.txt": diagnostic.digest(path)}), encoding="utf-8"
    )
    path.write_text("new", encoding="utf-8")
    with pytest.raises(ValueError, match="artifact changed"):
        diagnostic.load(tmp_path, tmp_path)


class Pipe:
    returncode = None

    def __init__(self, budget, confirm=True):
        self.budget, self.confirm = budget, confirm
        self.frames = []
        self.stdin = SimpleNamespace(write=self.write, drain=self.drain)
        self.stdout = SimpleNamespace(readline=self.readline)

    def write(self, data):
        ledger = json.loads(self.budget.read_text(encoding="utf-8"))
        assert ledger["limit"] == 48 and ledger["used"] == len(self.frames) + 1
        self.frames.append(json.loads(data))

    async def drain(self):
        pass

    async def readline(self):
        frame = self.frames[-1]
        profile = validate_frame_profile(frame)
        value = (
            {"intent": "included", "block": "introduccion_ingenieria_software"}
            if len(self.frames) == 1
            else {"intent": "excluded_standalone", "block": "seguridad"}
        )
        result = {
            "id": frame["id"],
            "type": "result",
            "text": json.dumps(value),
            "finish_reason": "stop",
            "finite_decoder": True,
            "input_tokens": 1,
            "output_tokens": 5,
            "latency_ms": 1,
        }
        if self.confirm:
            result["message_profile"] = profile
        return json.dumps(result).encode()

    def terminate(self):
        self.returncode = 0


@pytest.mark.asyncio
@pytest.mark.parametrize("confirm", [True, False])
async def test_profile_enforcement_partial_receipts_and_independent_ledger(tmp_path, confirm):
    bank, oracle, protocol = diagnostic.build_inputs()
    policy_path = diagnostic.EVIDENCE / "course-scope-policy-v1.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    metadata_value = json.loads(
        (diagnostic.EVIDENCE / "course-block-descriptions-v1.json").read_text(encoding="utf-8")
    )
    binding = SimpleNamespace(
        policy_sha256=diagnostic.digest(policy_path),
        revalidate=lambda *_: policy,
        assert_decision=lambda *_: None,
    )
    metadata = SimpleNamespace(sha256="fixture", revalidate=lambda *_: metadata_value)
    old = tmp_path / "old.json"
    old.write_text('{"used":1,"limit":72}', encoding="utf-8")
    old_contents = old.read_bytes()
    ledger = tmp_path / "diagnostic.json"
    pipe = Pipe(ledger, confirm=confirm)
    adapter = CachedTransformersGenerationAdapter(pipe, message_profile="scope-control/v1")

    async def resources():
        return True

    records, rows, reason = await diagnostic.run_questions(
        bank,
        oracle,
        protocol,
        provider=adapter,
        binding=binding,
        db=None,
        metadata=metadata,
        output=tmp_path,
        budget_path=ledger,
        proposal_hash="diagnostic",
        resource_check=resources,
        evaluate_fn=diagnostic.evaluate,
        summarize_fn=diagnostic.summarize,
    )
    expected_count = 2 if confirm else 1
    assert len(pipe.frames) == expected_count and reason == "first_critical_failure"
    assert old.read_bytes() == old_contents
    assert json.loads(ledger.read_text())["used"] == expected_count
    assert json.loads(ledger.read_text())["limit"] == 48
    assert (tmp_path / f"C{expected_count:02}.partial.json").exists()
    assert records[-1]["attempts"][-1]["exchange"]["raw_worker_response"]
    payload = json.loads(
        pipe.frames[0]["messages"][1]["content"]
        .removeprefix("<scope_control_data>")
        .removesuffix("</scope_control_data>")
    )
    assert "witness_terms" not in payload and "oracle" not in payload and "author" not in payload
    summary = diagnostic.summarize(bank, oracle, rows)
    assert summary["not_executed"] == 12 - expected_count
    if confirm:
        assert summary["false_exclusion"] == 1 and summary["finite_enforced"] == 2
        assert summary["profiles_confirmed"] == 2
    else:
        assert summary["protocol_errors"] == 1 and not summary["passed_diagnostic_only"]


@pytest.mark.asyncio
async def test_48_calls_is_a_hard_pre_send_limit(tmp_path):
    _, _, protocol = diagnostic.build_inputs()
    budget = tmp_path / "budget.json"
    diagnostic.save(budget, {"proposal_sha256": "diag", "used": 48, "limit": 48, "questions": {}})
    port = QuestionPort(SimpleNamespace(), {"id": "C01"}, tmp_path, budget, "diag", protocol)
    port.receipt_sink(({"step": "target"},))
    from oralia.infrastructure.generation.generation_port import GenerationRequest

    req = GenerationRequest(purpose="explicacion", instruction="fixture")
    req = req.model_copy(update={"constraints": req.constraints.model_copy(update={"max_tokens": 128})})
    with pytest.raises(ValueError, match="call limit"):
        await port.generate(req)
    assert json.loads(budget.read_text())["used"] == 48
