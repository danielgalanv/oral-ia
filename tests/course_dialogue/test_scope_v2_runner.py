"""Offline runner checks: frozen inputs, v2 dispatch, receipts and distinct budget."""

import json
from types import SimpleNamespace

import pytest
from frozen_scope_fixture import archived_root

from oralia.infrastructure.generation.generation_port import GenerationOutcome
from scripts import trial_scope_v2 as runner


def load_frozen(tmp_path):
    return runner.load_frozen(root=archived_root(runner.PACKAGE, runner.ROOT, tmp_path))


def test_live_tree_replay_is_still_rejected():
    with pytest.raises(ValueError, match="frozen artifact changed"):
        runner.load_frozen()


def test_final_package_counts_and_manifest(tmp_path):
    bank, oracle, protocol, _ = load_frozen(tmp_path)
    assert len(bank) == 28 and len(oracle) == 28
    assert {c["id"] for c in bank} == set(oracle)
    assert len({oracle[c["id"]]["included_block"] for c in bank[:9]}) == 9
    assert sum(r["primary_intent"] == "unclear_request" for r in oracle.values()) == 3
    assert protocol["continuation_threshold"]["decidable_cases"] == 25
    assert runner.BUDGET != runner.EVIDENCE / "scope-classifier-call-budget.json"


def test_manifest_change_is_rejected_before_model(tmp_path):
    package = tmp_path / "package"
    package.mkdir()
    target = tmp_path / "frozen.txt"
    target.write_text("original", encoding="utf-8")
    (package / "manifest.json").write_text(
        json.dumps({"frozen.txt": runner.digest(target)}), encoding="utf-8"
    )
    target.write_text("changed", encoding="utf-8")
    with pytest.raises(ValueError, match="artifact changed"):
        runner.load_frozen(package, tmp_path)


@pytest.mark.asyncio
async def test_v2_early_stop_preserves_full_receipts_and_old_budget(tmp_path):
    bank, oracle, protocol, _ = load_frozen(tmp_path)
    policy_path = runner.EVIDENCE / "course-scope-policy-v1.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    descriptors = json.loads(
        (runner.EVIDENCE / "course-block-descriptions-v1.json").read_text(encoding="utf-8")
    )
    binding = SimpleNamespace(
        revalidate=lambda *_: policy,
        policy_sha256=runner.digest(policy_path),
        assert_decision=lambda *_: None,
    )
    metadata = SimpleNamespace(revalidate=lambda *_: descriptors, sha256="fixture")
    previous = tmp_path / "old-budget.json"
    previous.write_text('{"used":2}', encoding="utf-8")
    original = previous.read_bytes()
    requests = []

    class Port:
        last_exchange = {"test": "full_exchange_fixture"}

        async def generate(self, request):
            requests.append(request)
            value = dict(
                primary_intent="included_request",
                included_block="introduccion_ingenieria_software",
                excluded_block=None,
                included=None,
                excluded=None,
                supporting_mention=None,
                referent_turn=None,
            )
            if len(requests) == 2:
                value["standalone"] = False  # rejected v1 field, not repaired
            return GenerationOutcome(
                ok=True, text=json.dumps(value), adapter="deterministic", finish_reason="stop"
            )

    async def enough_resources():
        return True

    new_budget = tmp_path / "new-budget.json"
    records, rows, reason = await runner.run_cases(
        bank,
        oracle,
        protocol,
        provider=Port(),
        binding=binding,
        db=None,
        metadata=metadata,
        output=tmp_path,
        budget_path=new_budget,
        proposal_hash="new-trial",
        resource_check=enough_resources,
    )
    assert len(requests) == 2 and reason == "first_critical_failure"
    assert json.loads(new_budget.read_text())["used"] == 2
    assert previous.read_bytes() == original
    assert all("primary_intent" in r.output_schema["properties"] for r in requests)
    assert all("status" not in r.output_schema["properties"] for r in requests)
    payload = json.loads(requests[0].student_input)
    assert len(payload["block_descriptions"]["blocks"]) == 21
    assert "oracle" not in payload and "expected" not in payload
    assert records[1]["outcome"] == json.loads((tmp_path / "N02.outcome.json").read_text())
    assert records[1]["request"] == json.loads((tmp_path / "N02.request.json").read_text(encoding="utf-8"))
    assert records[1]["exchange"] == {"test": "full_exchange_fixture"}
    summary = runner.summarize(bank, oracle, rows, protocol)
    assert summary["not_executed"] == 26 and summary["not_executed_ids"][0] == "N03"
    assert summary["contract_errors"] == 1 and summary["semantic_incorrect"] == 0
    assert summary["passed"] is False
    with pytest.raises(ValueError, match="duplicate"):
        await runner.RecordedPort(Port(), {"id": "N01"}, tmp_path, new_budget, "new-trial").generate(
            requests[0]
        )
    assert len(requests) == 2 and json.loads(new_budget.read_text())["used"] == 2
