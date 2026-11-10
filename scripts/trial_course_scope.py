"""One frozen local scope trial, independent of academic answer verification."""

import asyncio
import hashlib
import json
import re
import sqlite3
import sys
import time
from dataclasses import asdict
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from oralia.course_dialogue.cached_transformers import CACHED_MODEL_7B, cached_provider
from oralia.course_dialogue.corpus import SOURCE_ROOT
from oralia.course_dialogue.gpu_resource_policy import gpu_values, preflight, resource_period
from oralia.course_dialogue.rag_lab import ActivityScopeBinding
from oralia.course_dialogue.scope_classifier import classify_scope

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
INPUT = EVIDENCE / "scope-classifier-frozen-v1"
OUTPUT = EVIDENCE / "scope-classifier-resource-v2"
REVISION = EVIDENCE / "scope-resource-revision-v2-final"
BUDGET = EVIDENCE / "scope-classifier-call-budget.json"


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


class RecordingProvider:
    def __init__(self, provider, record):
        self.provider = provider
        self.record = record

    async def generate(self, request):
        # Persist before dispatch, so crashes never reset the shared trial budget.
        budget = json.loads(BUDGET.read_text(encoding="utf-8")) if BUDGET.exists() else {"used": 0}
        if budget["used"] >= 20:
            raise ValueError("twenty-call total budget exhausted")
        budget["used"] += 1
        save(BUDGET, budget)
        self.record["request"] = request.model_dump(mode="json")
        return await self.provider.generate(request)


async def snapshot():
    result = {"monotonic": time.monotonic()}
    for key, args in (
        ("gpu", ["--query-gpu=utilization.gpu,memory.used,memory.free", "--format=csv,noheader,nounits"]),
        ("apps", ["--query-compute-apps=pid,used_gpu_memory", "--format=csv,noheader,nounits"]),
        ("process_table", []),
    ):
        proc = await asyncio.create_subprocess_exec(
            "nvidia-smi", *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        out, _ = await asyncio.wait_for(proc.communicate(), 5)
        if proc.returncode:
            raise ValueError("GPU telemetry unavailable")
        result[key] = out.decode().strip()
    return result


def compute_pids(sample):
    """WDDM compute-apps includes desktop C+G clients; identify explicit C rows."""
    return [int(pid) for pid in re.findall(r"\|\s+\d+\s+N/A\s+N/A\s+(\d+)\s+C\s+", sample["process_table"])]


def evaluate(case, expected, result):
    actual = result.selection
    correct = actual.status == expected["status"]
    for key in ("included_block", "excluded_block", "referent_turn"):
        correct = correct and getattr(actual, key) == expected.get(key)
    critical = actual.status in {"out_of_scope", "mixed"} and (
        expected["status"] not in {"out_of_scope", "mixed"}
        or actual.excluded_block != expected.get("excluded_block")
    )
    if expected["status"] == "mixed":
        # Exact permitted fragment is checked against a frozen independent oracle.
        isolated = actual.status == "mixed" and result.rag_question == expected["included_quote"]
        correct = correct and isolated and actual.excluded.quote == expected["excluded_quote"]
        critical = critical or not isolated
    return {
        "id": case["id"],
        "expected": expected["status"],
        "actual": actual.status,
        "correct": correct,
        "critical": critical,
    }


def metrics(rows, total=20):
    matrix = {}
    for row in rows:
        key = row["expected"] + " -> " + row["actual"]
        matrix[key] = matrix.get(key, 0) + 1
    decidable = [r for r in rows if r["expected"] != "uncertain_scope"]
    return {
        "executed": len(rows),
        "not_executed": total - len(rows),
        "correct": sum(r["correct"] for r in rows),
        "incorrect_executed": sum(not r["correct"] for r in rows),
        "matrix": matrix,
        "decidable_executed": len(decidable),
        "decidable_correct": sum(r["correct"] for r in decidable),
        "decidable_non_uncertain": sum(r["actual"] != "uncertain_scope" for r in decidable),
        "false_exclusions": sum(
            r["actual"] in {"out_of_scope", "mixed"} and r["expected"] not in {"out_of_scope", "mixed"}
            for r in rows
        ),
        "false_inclusions": sum(r["expected"] == "out_of_scope" and r["actual"] == "in_scope" for r in rows),
        "resource_inconclusive_errors": sum(
            r["actual"] == "error" and r.get("resource_status") == "resource-inconclusive" for r in rows
        ),
        "semantic_evaluated": sum(r["actual"] != "error" for r in rows),
        "semantic_incorrect": sum(not r["correct"] and r["actual"] != "error" for r in rows),
    }


async def main():
    OUTPUT.mkdir(exist_ok=False)
    manifest = json.loads((INPUT / "manifest.json").read_text(encoding="utf-8"))
    for name, digest in manifest.items():
        if name == "scripts/trial_course_scope.py":
            name = (INPUT / "code/scripts/trial_course_scope.py").relative_to(ROOT).as_posix()
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest:
            raise ValueError("frozen artifact changed: " + name)
    revision = json.loads((REVISION / "manifest.json").read_text(encoding="utf-8"))
    for name, digest in revision.items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest:
            raise ValueError("resource revision changed: " + name)
    cases = json.loads((INPUT / "bank.json").read_text(encoding="utf-8"))
    oracle = json.loads((INPUT / "oracle.json").read_text(encoding="utf-8"))
    if len(cases) != 20 or len(oracle) != 20:
        raise ValueError("expected twenty frozen cases")
    samples, records, rows = [], [], []
    stop = asyncio.Event()

    async def monitor():
        while not stop.is_set():
            try:
                samples.append(await snapshot())
            except Exception as error:
                samples.append({"error": type(error).__name__})
            save(OUTPUT / "gpu-telemetry.json", samples)
            try:
                await asyncio.wait_for(stop.wait(), 2)
            except TimeoutError:
                pass

    for _ in range(5):
        samples.append({"phase": "before", **await snapshot()})
        await asyncio.sleep(2)
    before = samples[-1]
    readiness = preflight(samples)
    save(OUTPUT / "preflight.json", readiness)
    if not readiness["ready"]:
        save(OUTPUT / "not-run.json", {"reason": "gpu_busy_or_insufficient", "snapshot": before})
        save(OUTPUT / "gpu-telemetry.json", samples)
        save(OUTPUT / "metrics.json", metrics(rows))
        samples.append({"phase": "after_not_run", **await snapshot()})
        save(OUTPUT / "gpu-telemetry.json", samples)
        return
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
        hashlib.sha256(policy_path.read_bytes()).hexdigest(),
        SOURCE_ROOT,
    )
    binding.revalidate(db)
    sampler = asyncio.create_task(monitor())
    reason = "completed"
    try:
        async with cached_provider(OUTPUT, source=CACHED_MODEL_7B, quantization="nf4") as provider:
            ready = json.loads((OUTPUT / "worker.json").read_text(encoding="utf-8"))
            own_mib = ready["memory_footprint_bytes"] / 1024**2
            for case in cases:
                current = await snapshot()
                samples.append({"phase": "before_case", "id": case["id"], **current})
                if resource_period([current], gpu_values(before)[1], own_mib) == "resource-pressure-observed":
                    reason = "unattributed_resource_pressure"
                    break
                record = {"id": case["id"], "input": case, "participant_display": None}
                sample_start = len(samples) - 1

                try:
                    result = await classify_scope(
                        case["text"],
                        case["history"],
                        provider=RecordingProvider(provider, record),
                        binding=binding,
                        db=db,
                    )
                    record.update(
                        selection=result.selection.model_dump(),
                        rag_question=result.rag_question,
                        assessment=asdict(result.assessment),
                        request=result.request.model_dump(mode="json"),
                        outcome=result.outcome.model_dump(mode="json"),
                    )
                    row = evaluate(case, oracle[case["id"]], result)
                except Exception as error:
                    record.update(error_type=type(error).__name__, error=str(error))
                    if "request" not in record:
                        records.append({**record, "not_executed": True})
                        save(OUTPUT / "records.json", records)
                        reason = "pre_dispatch_revalidation_failure"
                        break
                    row = {
                        "id": case["id"],
                        "expected": oracle[case["id"]]["status"],
                        "actual": "error",
                        "correct": False,
                        "critical": True,
                    }
                record["exchange"] = provider.last_exchange
                after_case = await snapshot()
                samples.append({"phase": "after_case", "id": case["id"], **after_case})
                resident = bool(set(compute_pids(current)) - {provider.process.pid})
                record["resource_status"] = resource_period(
                    samples[sample_start:], gpu_values(before)[1], own_mib, resident
                )
                row["resource_status"] = record["resource_status"]
                records.append(record)
                rows.append(row)
                save(OUTPUT / "records.json", records)
                save(OUTPUT / "evaluations.json", rows)
                save(OUTPUT / "metrics.json", metrics(rows))
                print(json.dumps(row), flush=True)
                if row["critical"]:
                    reason = "first_critical_failure"
                    break
                if record["resource_status"] == "resource-pressure-observed":
                    reason = "unattributed_resource_pressure"
                    break
    finally:
        stop.set()
        await sampler
        samples.append({"phase": "after", **await snapshot()})
        save(OUTPUT / "gpu-telemetry.json", samples)
        save(
            OUTPUT / "termination.json",
            {
                "reason": reason,
                "publication_allowed": False,
                "metrics": metrics(rows),
                "latencies_inconclusive_if_foreign_compute_present": True,
            },
        )
        db.close()
        engine.dispose()


if __name__ == "__main__":
    if sys.argv[1:]:
        raise ValueError("no trial overrides")
    asyncio.run(main())
