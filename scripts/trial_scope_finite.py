"""One frozen finite-scope capacity run with per-dispatch accounting and partial receipts."""

import asyncio
import hashlib
import json
import sqlite3
import sys
import time
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
from oralia.course_dialogue.scope_finite import classify_finite_scope, literal_span
from scripts.trial_course_scope import compute_pids, save, snapshot

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
PACKAGE = EVIDENCE / "scope-finite-capacity-v1"
OUTPUT = EVIDENCE / "scope-finite-capacity-first"
BUDGET = EVIDENCE / "scope-finite-capacity-budget.json"
RUNNER_MANIFEST = EVIDENCE / "scope-finite-runner-manifest.json"


class ResourcePressureStop(RuntimeError):
    pass


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_inputs(package=PACKAGE, root=ROOT):
    manifest = json.loads((package / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest.items():
        if digest(root / name) != expected:
            raise ValueError("frozen artifact changed: " + name)
    bank = json.loads((package / "bank.json").read_text(encoding="utf-8"))
    oracle = json.loads((package / "oracle.json").read_text(encoding="utf-8"))
    protocol = json.loads((package / "protocol.json").read_text(encoding="utf-8"))
    ids = [case["id"] for case in bank]
    if ids != [f"F{i:02}" for i in range(1, 19)] or set(oracle) != set(ids):
        raise ValueError("expected exactly the frozen eighteen IDs and separate oracle")
    if len({oracle[key]["included_block"] for key in ids[:9]}) != 9 or (
        protocol["new_call_limit"] != 72
        or protocol["maximum_calls_per_question"] != 4
        or protocol["shared_tokens_per_question"] != 512
        or protocol["shared_deadline_per_question_ms"] != 30000
    ):
        raise ValueError("frozen counts or budgets inconsistent")
    return bank, oracle, protocol, manifest


class QuestionPort:
    def __init__(
        self,
        provider,
        record,
        output,
        budget_path,
        proposal_hash,
        protocol,
        clock=time.monotonic,
        stop_requested=lambda: False,
    ):
        self.provider, self.record, self.output = provider, record, output
        self.budget_path, self.proposal_hash, self.protocol = budget_path, proposal_hash, protocol
        self.clock, self.started = clock, clock()
        self.receipts = ()
        self.stop_requested = stop_requested

    @property
    def last_exchange(self):
        return getattr(self.provider, "last_exchange", None)

    def receipt_sink(self, receipts):
        self.receipts = receipts
        self.record["steps"] = receipts
        save(self.output / f"{self.record['id']}.partial.json", self.record)

    async def generate(self, request):
        if self.stop_requested():
            raise ResourcePressureStop("resource pressure observed before next step; no dispatch")
        step = self.receipts[-1]["step"]
        caps = {
            "target": 128,
            "referent": 32,
            "included_part": 176,
            "excluded_standalone_part": 176,
            "supporting_mention": 176,
        }
        remaining = int(30000 - (self.clock() - self.started) * 1000)
        if remaining < 1000:
            raise TimeoutError("shared question deadline before dispatch")
        if step not in caps or request.constraints.max_tokens > caps[step]:
            raise ValueError("step token limit exceeded")
        budget = (
            json.loads(self.budget_path.read_text(encoding="utf-8"))
            if self.budget_path.exists()
            else {
                "proposal_sha256": self.proposal_hash,
                "used": 0,
                "limit": self.protocol["new_call_limit"],
                "questions": {},
            }
        )
        if (
            budget["proposal_sha256"] != self.proposal_hash
            or budget["limit"] != self.protocol["new_call_limit"]
        ):
            raise ValueError("foreign budget; old trials are not reusable")
        question = budget["questions"].setdefault(
            self.record["id"], {"calls": 0, "tokens_reserved": 0, "steps": []}
        )
        if (
            budget["used"] >= self.protocol["new_call_limit"]
            or question["calls"] >= 4
            or step in question["steps"]
        ):
            raise ValueError("total/question/duplicate-step call limit exceeded")
        if question["tokens_reserved"] + request.constraints.max_tokens > 512:
            raise ValueError("shared question token limit exceeded")
        question["calls"] += 1
        question["tokens_reserved"] += request.constraints.max_tokens
        question["steps"].append(step)
        budget["used"] += 1
        save(self.budget_path, budget)  # reserve before the provider can receive the request
        constrained = request.model_copy(
            update={
                "constraints": request.constraints.model_copy(
                    update={"deadline_ms": min(request.constraints.deadline_ms, remaining)}
                )
            }
        )
        attempt = {"step": step, "request": constrained.model_dump(mode="json"), "outcome": None}
        self.record.setdefault("attempts", []).append(attempt)
        self.receipt_sink(self.receipts)
        try:
            outcome = await asyncio.wait_for(self.provider.generate(constrained), timeout=remaining / 1000)
            attempt["outcome"] = outcome.model_dump(mode="json")
            return outcome
        except BaseException as error:
            attempt["error_type"] = type(error).__name__
            raise
        finally:
            attempt["exchange"] = self.last_exchange
            self.receipt_sink(self.receipts)


def evaluate(case, expected, result):
    actual = result.assessment
    literal_steps = [
        step
        for step in result.receipts
        if step["step"] in {"supporting_mention", "included_part", "excluded_standalone_part"}
    ]
    witness_texts = [(step.get("outcome") or {}).get("text") for step in literal_steps]
    scope_correct = (
        actual.status == expected["status"]
        and actual.block_id == expected["included_block"]
        and actual.excluded_block_id == expected["excluded_block"]
    )
    witness_correct = witness_texts == expected["witnesses"]
    reference_correct = result.referent_turn == expected["referent_turn"]
    false_exclusion = actual.status in {"out_of_scope", "mixed"} and (
        expected["status"] not in {"out_of_scope", "mixed"}
        or actual.excluded_block_id != expected["excluded_block"]
        or (actual.status == "out_of_scope" and expected["status"] == "mixed")
    )
    mixed_leak = (
        expected["status"] == "mixed"
        and result.rag_question is not None
        and (
            actual.status != "mixed"
            or result.rag_question != expected["witnesses"][0]
            or result.rag_history != ()
        )
    )
    finite = [s for s in result.receipts if s["request"]["output_schema"] is not None]
    enforced = sum(
        json.loads((s.get("exchange") or {}).get("raw_worker_response") or "{}").get("finite_decoder") is True
        for s in finite
    )
    completed = sum((s.get("outcome") or {}).get("finish_reason") == "stop" for s in finite)
    resource_abstention = result.reason == "shared_deadline_at_final_validation" or any(
        s.get("rejected") == "shared_deadline" or (s.get("outcome") or {}).get("finish_reason") == "deadline"
        for s in result.receipts
    )
    return {
        "id": case["id"],
        "expected": expected["status"],
        "actual": actual.status,
        "scope_correct": scope_correct,
        "reference_correct": reference_correct,
        "witness_correct": witness_correct,
        "correct": bool(finite)
        and completed == len(finite)
        and scope_correct
        and witness_correct
        and reference_correct,
        "false_exclusion": false_exclusion,
        "mixed_leak": mixed_leak,
        "false_abstention": actual.status == "uncertain_scope" and expected["status"] != "uncertain_scope",
        "literal_unique_matches": sum(
            literal_span(case["text"], quote) is not None for quote in witness_texts
        ),
        "literal_steps": len(literal_steps),
        "finite_steps": len(finite),
        "finite_enforced": enforced,
        "finite_completed": completed,
        "resource_abstention": resource_abstention,
        "critical": false_exclusion or mixed_leak or enforced != len(finite),
        "error_kind": None,
    }


def summarize(bank, oracle, rows):
    executed = {row["id"] for row in rows}
    matrix = {}
    for row in rows:
        key = row["expected"] + " -> " + row["actual"]
        matrix[key] = matrix.get(key, 0) + 1
    by_id = {row["id"]: row for row in rows}
    result = {
        "executed": len(rows),
        "not_executed": len(bank) - len(rows),
        "not_executed_ids": [c["id"] for c in bank if c["id"] not in executed],
        "matrix": matrix,
        "correct": sum(r["correct"] for r in rows),
        "positive_blocks": {
            oracle[c["id"]]["included_block"]: by_id.get(c["id"], {}).get("correct") for c in bank[:9]
        },
    }
    for name in (
        "false_exclusion",
        "mixed_leak",
        "false_abstention",
        "finite_steps",
        "finite_enforced",
        "literal_steps",
        "literal_unique_matches",
        "finite_completed",
        "resource_abstention",
    ):
        result[name] = sum(r.get(name, 0) for r in rows)
    result["protocol_errors"] = sum(r["error_kind"] == "protocol" for r in rows)
    result["resource_errors"] = sum(r["error_kind"] == "resource" for r in rows)
    result["passed"] = (
        len(rows) == 18
        and result["correct"] >= 15
        and all(result["positive_blocks"].values())
        and result["false_exclusion"] == result["mixed_leak"] == result["protocol_errors"] == 0
        and result["resource_errors"] == 0
        and result["resource_abstention"] == 0
        and result["finite_steps"] == result["finite_enforced"] == result["finite_completed"]
    )
    return result


async def run_questions(
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
    stop_requested=lambda: False,
    evaluate_fn=evaluate,
    summarize_fn=summarize,
):
    records, rows = [], []
    reason = "completed"
    for case in bank:
        if not await resource_check():
            reason = "observed_resource_pressure_before_question"
            break
        record = {"id": case["id"], "input": case, "participant_display": None}
        port = QuestionPort(
            provider, record, output, budget_path, proposal_hash, protocol, stop_requested=stop_requested
        )
        try:
            result = await classify_finite_scope(
                case["text"],
                case["history"],
                provider=port,
                binding=binding,
                db=db,
                metadata=metadata,
                receipt_sink=port.receipt_sink,
            )
            record["result"] = asdict(result)
            row = evaluate_fn(case, oracle[case["id"]], result)
        except Exception as error:
            record.update(error_type=type(error).__name__, error=str(error))
            if not record.get("attempts"):
                records.append({**record, "not_executed": True})
                reason = "pre_dispatch_failure"
                break
            resource_error = isinstance(error, (TimeoutError, ResourcePressureStop)) or (
                getattr(provider, "last_exchange", None) or {}
            ).get("failure_type") in {"read_timeout", "eof", "worker_unavailable"}
            row = {
                "id": case["id"],
                "expected": oracle[case["id"]]["status"],
                "actual": "resource-inconclusive" if resource_error else "error",
                "correct": False,
                "critical": True,
                "error_kind": "resource" if resource_error else "protocol",
            }
        records.append(record)
        rows.append(row)
        save(output / "records.json", records)
        save(output / "evaluations.json", rows)
        save(output / "metrics.json", summarize_fn(bank, oracle, rows))
        print(json.dumps(row), flush=True)
        if row["critical"]:
            reason = "first_critical_failure"
            break
    save(output / "records.json", records)
    return records, rows, reason


def freeze_runner():
    frozen_inputs()
    if RUNNER_MANIFEST.exists():
        raise ValueError("preserve runner freeze")
    paths = [
        Path(__file__).resolve(),
        ROOT / "tests/course_dialogue/test_scope_finite_runner.py",
        ROOT / "scripts/trial_course_scope.py",
        ROOT / "src/oralia/course_dialogue/gpu_resource_policy.py",
        PACKAGE / "manifest.json",
    ]
    archive = EVIDENCE / "scope-finite-runner-code"
    archive.mkdir(exist_ok=False)
    for path in list(paths):
        copy = archive / path.relative_to(ROOT)
        copy.parent.mkdir(parents=True, exist_ok=True)
        copy.write_bytes(path.read_bytes())
        paths.append(copy)
    save(RUNNER_MANIFEST, {path.relative_to(ROOT).as_posix(): digest(path) for path in paths})


async def main():
    bank, oracle, protocol, manifest = frozen_inputs()
    for name, expected in json.loads(RUNNER_MANIFEST.read_text(encoding="utf-8")).items():
        if digest(ROOT / name) != expected:
            raise ValueError("runner changed: " + name)
    OUTPUT.mkdir(exist_ok=False)
    samples, rows = [], []
    for _ in range(5):
        samples.append({"phase": "before", **await snapshot()})
        await asyncio.sleep(2)
    ready = preflight(samples)
    save(OUTPUT / "preflight.json", ready)
    if not ready["ready"]:
        samples.append({"phase": "after_not_run", **await snapshot()})
        save(OUTPUT / "gpu-telemetry.json", samples)
        save(OUTPUT / "not-run.json", {"reason": "observed_load_or_memory"})
        save(OUTPUT / "metrics.json", summarize(bank, oracle, rows))
        return
    baseline = gpu_values(samples[-1])[1]
    database = ROOT / ".oralia-course-study/course.db"
    engine = create_engine(
        "sqlite://", creator=lambda: sqlite3.connect("file:" + database.as_posix() + "?mode=ro", uri=True)
    )
    db = Session(engine)
    policy_path = EVIDENCE / "course-scope-policy-v1.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    binding = ActivityScopeBinding(
        engine,
        policy["activity_id"],
        policy["activity_version"],
        policy["course_id"],
        policy_path,
        digest(policy_path),
        SOURCE_ROOT,
    )
    metadata_path = EVIDENCE / "course-block-descriptions-v1.json"
    metadata = BlockMetadata(metadata_path, manifest[metadata_path.relative_to(ROOT).as_posix()])
    metadata.revalidate(binding, binding.revalidate(db))
    stop, pressure = asyncio.Event(), asyncio.Event()
    own_mib = None
    reason = "preparation_incomplete"

    async def monitor():
        while not stop.is_set():
            try:
                sample = await snapshot()
                samples.append(sample)
                if (
                    own_mib is not None
                    and resource_period([sample], baseline, own_mib) == "resource-pressure-observed"
                ):
                    pressure.set()
            except Exception as error:
                samples.append({"error": type(error).__name__})
            save(OUTPUT / "gpu-telemetry.json", samples)
            try:
                await asyncio.wait_for(stop.wait(), 2)
            except TimeoutError:
                pass

    monitor_task = asyncio.create_task(monitor())
    try:
        async with cached_provider(OUTPUT, source=CACHED_MODEL_7B, quantization="nf4") as provider:
            worker = json.loads((OUTPUT / "worker.json").read_text(encoding="utf-8"))
            own_mib = worker["memory_footprint_bytes"] / 1024**2
            root_process = psutil.Process(provider.process.pid)
            own_pids = {root_process.pid, *(p.pid for p in root_process.children(recursive=True))}

            async def resource_check():
                sample = await snapshot()
                samples.append({"phase": "between_questions", **sample})
                return (
                    not pressure.is_set()
                    and resource_period([sample], baseline, own_mib) != "resource-pressure-observed"
                )

            _, rows, reason = await run_questions(
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
                stop_requested=pressure.is_set,
            )
            save(
                OUTPUT / "resource-review.json",
                {
                    "own_pids": sorted(own_pids),
                    "pressure_observed": pressure.is_set(),
                    "foreign_compute_pids_observed": sorted(
                        {
                            pid
                            for sample in samples
                            if "process_table" in sample
                            for pid in compute_pids(sample)
                        }
                        - own_pids
                    ),
                    "exclusive_gpu_claimed": False,
                    "memory_peak_proves_foreign_activity": False,
                    "performance_status": "resource-inconclusive",
                },
            )
    finally:
        stop.set()
        await monitor_task
        samples.append({"phase": "after", **await snapshot()})
        save(OUTPUT / "gpu-telemetry.json", samples)
        save(OUTPUT / "metrics.json", summarize(bank, oracle, rows))
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
