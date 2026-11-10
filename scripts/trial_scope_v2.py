"""Execute exactly the frozen v2+descriptions trial; no retry or public output."""

import asyncio
import hashlib
import json
import sqlite3
import sys
from dataclasses import asdict
from pathlib import Path

import psutil
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from oralia.course_dialogue.cached_transformers import CACHED_MODEL_7B, cached_provider
from oralia.course_dialogue.corpus import SOURCE_ROOT
from oralia.course_dialogue.gpu_resource_policy import gpu_values, preflight, resource_period
from oralia.course_dialogue.rag_lab import ActivityScopeBinding
from oralia.course_dialogue.scope_block_metadata import BlockMetadata
from oralia.course_dialogue.scope_classifier_v2 import INTENTS, classify_scope_v2
from scripts.trial_course_scope import compute_pids, save, snapshot

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
PACKAGE = EVIDENCE / "scope-v2-described-proposal-v1-final"
OUTPUT = EVIDENCE / "scope-v2-described-first"
BUDGET = EVIDENCE / "scope-v2-described-budget.json"
RUNNER_FREEZE = EVIDENCE / "scope-v2-runner-freeze.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def freeze_runner():
    load_frozen()
    if RUNNER_FREEZE.exists():
        raise ValueError("preserve frozen runner")
    paths = [
        Path(__file__).resolve(),
        ROOT / "tests/course_dialogue/test_scope_v2_runner.py",
        ROOT / "scripts/trial_course_scope.py",
        PACKAGE / "manifest.json",
    ]
    archive = EVIDENCE / "scope-v2-runner-code"
    archive.mkdir(exist_ok=False)
    for path in list(paths):
        copy = archive / path.relative_to(ROOT)
        copy.parent.mkdir(parents=True, exist_ok=True)
        copy.write_bytes(path.read_bytes())
        paths.append(copy)
    save(RUNNER_FREEZE, {p.relative_to(ROOT).as_posix(): digest(p) for p in paths})


def load_frozen(package=PACKAGE, root=ROOT):
    manifest = json.loads((package / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest.items():
        if digest(root / name) != expected:
            raise ValueError("frozen artifact changed: " + name)
    bank = json.loads((package / "bank.json").read_text(encoding="utf-8"))
    oracle = json.loads((package / "oracle.json").read_text(encoding="utf-8"))
    protocol = json.loads((package / "protocol.json").read_text(encoding="utf-8"))
    ids = [case["id"] for case in bank]
    if ids != [f"N{i:02}" for i in range(1, 29)] or set(ids) != set(oracle):
        raise ValueError("expected the ordered 28 IDs and matching oracle")
    counts = {
        "positive_blocks": sum(oracle[key]["primary_intent"] == "included_request" for key in ids[:9]),
        "unclear": sum(row["primary_intent"] == "unclear_request" for row in oracle.values()),
        "decidable": sum(row["primary_intent"] != "unclear_request" for row in oracle.values()),
    }
    threshold = protocol["continuation_threshold"]
    if counts != {"positive_blocks": 9, "unclear": 3, "decidable": 25} or (
        len({oracle[key]["included_block"] for key in ids[:9]}) != 9
        or protocol["contract_version"] != 2
        or protocol["total_new_call_budget"] != 28
        or threshold["positive_blocks_correct"] != counts["positive_blocks"]
        or threshold["unclear_cases_preserved"] != counts["unclear"]
        or threshold["decidable_cases"] != counts["decidable"]
    ):
        raise ValueError("frozen bank and threshold counts disagree")
    return bank, oracle, protocol, manifest


class RecordedPort:
    def __init__(self, provider, record, output, budget_path, proposal_hash, limit=28):
        self.provider, self.record, self.output = provider, record, output
        self.budget_path, self.proposal_hash, self.limit = budget_path, proposal_hash, limit

    async def generate(self, request):
        budget = (
            json.loads(self.budget_path.read_text(encoding="utf-8"))
            if self.budget_path.exists()
            else {"proposal_sha256": self.proposal_hash, "limit": self.limit, "used": 0, "case_ids": []}
        )
        key = self.record["id"]
        if budget["proposal_sha256"] != self.proposal_hash or budget["limit"] != self.limit:
            raise ValueError("foreign trial budget")
        if budget["used"] >= self.limit or key in budget["case_ids"]:
            raise ValueError("trial budget exhausted or duplicate case")
        budget["used"] += 1
        budget["case_ids"].append(key)
        save(self.budget_path, budget)
        self.record["request"] = request.model_dump(mode="json")
        save(self.output / f"{key}.request.json", self.record["request"])
        outcome = await self.provider.generate(request)
        self.record["outcome"] = outcome.model_dump(mode="json")
        save(self.output / f"{key}.outcome.json", self.record["outcome"])
        return outcome


def evaluate(key, expected, result):
    selection = result.selection
    expected_status = INTENTS[expected["primary_intent"]][0]
    actual = result.assessment.status
    false_exclusion = actual in {"out_of_scope", "mixed"} and (
        expected_status not in {"out_of_scope", "mixed"}
        or selection.excluded_block != expected["excluded_block"]
    )
    correct = all(
        getattr(selection, field) == expected[field]
        for field in ("primary_intent", "included_block", "excluded_block", "referent_turn")
    )
    leak = False
    if expected_status == "mixed":
        leak = actual != "mixed" or result.rag_question != expected["allowed_quote"]
        correct = correct and not leak and selection.excluded.quote == expected["excluded_quote"]
    if expected["supporting_mention"] is not None:
        correct = (
            correct
            and selection.supporting_mention is not None
            and (selection.supporting_mention.quote == expected["supporting_mention"])
        )
    return {
        "id": key,
        "expected": expected_status,
        "actual": actual,
        "correct": correct,
        "false_exclusion": false_exclusion,
        "mixed_leak": leak,
        "critical": false_exclusion or leak,
        "error_kind": None,
    }


def summarize(bank, oracle, rows, protocol):
    matrix = {}
    for row in rows:
        label = row["expected"] + " -> " + row["actual"]
        matrix[label] = matrix.get(label, 0) + 1
    result = {
        "executed": len(rows),
        "not_executed": len(bank) - len(rows),
        "not_executed_ids": [c["id"] for c in bank if c["id"] not in {r["id"] for r in rows}],
        "matrix": matrix,
        "correct": sum(r["correct"] for r in rows),
        "semantic_incorrect": sum(not r["correct"] and r["error_kind"] is None for r in rows),
        "contract_errors": sum(r["error_kind"] == "contract" for r in rows),
        "resource_errors": sum(r["error_kind"] == "resource" for r in rows),
        "false_exclusions": sum(r["false_exclusion"] for r in rows),
        "mixed_leaks": sum(r["mixed_leak"] for r in rows),
        "positives_correct": sum(r["correct"] and r["id"] in {c["id"] for c in bank[:9]} for r in rows),
        "unclear_preserved": sum(r["correct"] and r["expected"] == "uncertain_scope" for r in rows),
        "decidable_correct": sum(r["correct"] and r["expected"] != "uncertain_scope" for r in rows),
    }
    threshold = protocol["continuation_threshold"]
    result["passed"] = (
        len(rows) == 28
        and result["positives_correct"] == threshold["positive_blocks_correct"]
        and result["unclear_preserved"] == threshold["unclear_cases_preserved"]
        and result["decidable_correct"] >= threshold["decidable_correct_minimum"]
        and all(
            result[key] == 0
            for key in ("false_exclusions", "mixed_leaks", "contract_errors", "resource_errors")
        )
    )
    return result


async def run_cases(
    bank,
    oracle,
    protocol,
    *,
    provider,
    binding,
    db,
    metadata,
    output,
    budget_path,
    proposal_hash,
    resource_check,
):
    records, rows = [], []
    reason = "completed"
    for case in bank:
        if not await resource_check():
            reason = "resource_pressure_before_dispatch"
            break
        record = {"id": case["id"], "input": case, "participant_display": None}
        port = RecordedPort(
            provider, record, output, budget_path, proposal_hash, protocol["total_new_call_budget"]
        )
        try:
            result, _, _ = await classify_scope_v2(
                case["text"], case["history"], provider=port, binding=binding, db=db, metadata=metadata
            )
            record.update(
                selection=result.selection.model_dump(),
                assessment=asdict(result.assessment),
                rag_question=result.rag_question,
            )
            row = evaluate(case["id"], oracle[case["id"]], result)
        except Exception as error:
            record.update(error_type=type(error).__name__, error=str(error))
            if "request" not in record:
                records.append({**record, "not_executed": True})
                reason = "pre_dispatch_failure"
                break
            outcome = record.get("outcome", {})
            resource_error = outcome.get("finish_reason") == "deadline" or (
                getattr(provider, "last_exchange", None) or {}
            ).get("failure_type") in {"read_timeout", "eof", "worker_unavailable"}
            row = {
                "id": case["id"],
                "expected": INTENTS[oracle[case["id"]]["primary_intent"]][0],
                "actual": "resource-inconclusive" if resource_error else "error",
                "correct": False,
                "false_exclusion": False,
                "mixed_leak": False,
                "critical": True,
                "error_kind": "resource" if resource_error else "contract",
            }
        record["exchange"] = getattr(provider, "last_exchange", None)
        records.append(record)
        rows.append(row)
        save(output / "records.json", records)
        save(output / "evaluations.json", rows)
        save(output / "metrics.json", summarize(bank, oracle, rows, protocol))
        print(json.dumps(row), flush=True)
        if row["critical"]:
            reason = "first_critical_failure"
            break
    save(output / "records.json", records)
    return records, rows, reason


async def main():
    bank, oracle, protocol, manifest = load_frozen()
    for name, expected in json.loads(RUNNER_FREEZE.read_text(encoding="utf-8")).items():
        if digest(ROOT / name) != expected:
            raise ValueError("runner artifact changed: " + name)
    OUTPUT.mkdir(exist_ok=False)
    samples, rows = [], []
    for _ in range(5):
        samples.append({"phase": "before", **await snapshot()})
        await asyncio.sleep(2)
    save(OUTPUT / "preflight.json", preflight(samples))
    if not preflight(samples)["ready"]:
        save(OUTPUT / "not-run.json", {"reason": "observed_load_or_memory"})
        save(OUTPUT / "gpu-telemetry.json", samples)
        save(OUTPUT / "metrics.json", summarize(bank, oracle, [], protocol))
        return
    baseline = gpu_values(samples[-1])[1]
    policy_path = EVIDENCE / "course-scope-policy-v1.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    database = ROOT / ".oralia-course-study/course.db"
    engine = create_engine(
        "sqlite://", creator=lambda: sqlite3.connect("file:" + database.as_posix() + "?mode=ro", uri=True)
    )
    db = Session(engine)
    binding = ActivityScopeBinding(
        engine,
        policy["activity_id"],
        policy["activity_version"],
        policy["course_id"],
        policy_path,
        digest(policy_path),
        SOURCE_ROOT,
    )
    binding.revalidate(db)
    metadata_path = EVIDENCE / "course-block-descriptions-v1.json"
    metadata = BlockMetadata(metadata_path, manifest[metadata_path.relative_to(ROOT).as_posix()])
    metadata.revalidate(binding, policy)
    stop, pressure = asyncio.Event(), asyncio.Event()
    own_mib = None
    reason = "preparation_incomplete"

    async def monitor():
        while not stop.is_set():
            try:
                current = await snapshot()
                samples.append(current)
                if (
                    own_mib is not None
                    and resource_period([current], baseline, own_mib) == "resource-pressure-observed"
                ):
                    pressure.set()
            except Exception as error:
                samples.append({"error": type(error).__name__})
            save(OUTPUT / "gpu-telemetry.json", samples)
            try:
                await asyncio.wait_for(stop.wait(), 2)
            except TimeoutError:
                pass

    sampler = asyncio.create_task(monitor())
    try:
        async with cached_provider(OUTPUT, source=CACHED_MODEL_7B, quantization="nf4") as provider:
            ready = json.loads((OUTPUT / "worker.json").read_text(encoding="utf-8"))
            own_mib = ready["memory_footprint_bytes"] / 1024**2
            process = psutil.Process(provider.process.pid)
            own_pids = {process.pid, *(p.pid for p in process.children(recursive=True))}

            async def resource_check():
                sample = await snapshot()
                samples.append({"phase": "between_cases", **sample})
                return (
                    not pressure.is_set()
                    and resource_period([sample], baseline, own_mib) != "resource-pressure-observed"
                )

            _, rows, reason = await run_cases(
                bank,
                oracle,
                protocol,
                provider=provider,
                binding=binding,
                db=db,
                metadata=metadata,
                output=OUTPUT,
                budget_path=BUDGET,
                proposal_hash=digest(PACKAGE / "manifest.json"),
                resource_check=resource_check,
            )
            save(
                OUTPUT / "resource-review.json",
                {
                    "own_pids": sorted(own_pids),
                    "foreign_compute_pids_observed": sorted(
                        {p for s in samples if "process_table" in s for p in compute_pids(s)} - own_pids
                    ),
                    "exclusive_gpu_claimed": False,
                    "pressure_observed": pressure.is_set(),
                    "performance_status": "resource-inconclusive",
                },
            )
    finally:
        stop.set()
        await sampler
        samples.append({"phase": "after", **await snapshot()})
        save(OUTPUT / "gpu-telemetry.json", samples)
        save(OUTPUT / "metrics.json", summarize(bank, oracle, rows, protocol))
        save(OUTPUT / "termination.json", {"reason": reason, "publication_allowed": False})
        db.close()
        engine.dispose()


if __name__ == "__main__":
    if sys.argv[1:] == ["--freeze-runner"]:
        freeze_runner()
    elif not sys.argv[1:]:
        asyncio.run(main())
    else:
        raise ValueError("no trial overrides")
