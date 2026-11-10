"""One frozen local advisory review/repair experiment. Explicit execution only."""

import argparse
import asyncio
import copy
import hashlib
import json
import subprocess
import time
from pathlib import Path

from oralia.course_dialogue.lab_request import LabGenerationRequest
from oralia.course_dialogue.review_repair import (
    REPAIR_INSTRUCTION,
    REVIEW_INSTRUCTION,
    CallBudget,
    ReviewRepairGenerationAdapter,
)
from oralia.documentary.study_lab import INSTRUCTION, DiagnosticStudy, TrialBudget
from oralia.infrastructure.generation.generation_port import GenerationOutcome

ROOT = Path(__file__).resolve().parents[1]
DOSSIER = ROOT / "docs/audits/2026-10-28-review-repair"


def write_new(path, value):
    with path.open("x", encoding="utf8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def gpu():
    result = subprocess.run(
        [
            "nvidia-smi",
            "--query-gpu=memory.used,memory.total,utilization.gpu",
            "--format=csv,noheader,nounits",
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=5,
    )
    lines = result.stdout.strip().splitlines()
    if len(lines) != 1:
        raise ValueError("GPU availability ambiguous")
    used, total, utilization = map(int, lines[0].split(","))
    return {
        "monotonic": time.monotonic(),
        "used_mib": used,
        "total_mib": total,
        "utilization_percent": utilization,
    }


def verify_freeze(protocol):
    for name, text in [
        ("draft", INSTRUCTION),
        ("review", REVIEW_INSTRUCTION),
        ("repair", REPAIR_INSTRUCTION),
    ]:
        if hashlib.sha256(text.encode()).hexdigest() != protocol["instruction_sha256"][name]:
            raise ValueError("Instruction changed after freeze: " + name)
    for path, expected in protocol["implementation_sha256"].items():
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != expected:
            raise ValueError("Implementation changed after freeze: " + path)


async def trial(output, protocol_path=None):
    from oralia.course_dialogue.cached_transformers import CACHED_MODEL_14B, cached_provider
    from oralia.documentary.retrieval import Retrieval

    protocol = json.loads((protocol_path or DOSSIER / "protocol-v1.json").read_text(encoding="utf8"))
    verify_freeze(protocol)
    output.mkdir(parents=True, exist_ok=False)
    write_new(output / "protocol.json", protocol)
    budget = CallBudget(maximum=28, seconds=1200)
    before = gpu()
    write_new(output / "gpu-before.json", before)
    if before["used_mib"] > 2000 or before["utilization_percent"] > 5:
        raise ValueError("GPU competition or uncertainty; no load")
    print(
        "REVIEW/REPAIR: one14B NF4, CPU encoder,28calls+1warmup,768tokens/50s per call,20min global.",
        flush=True,
    )
    samples = [before]
    stop = asyncio.Event()

    async def sample():
        while not stop.is_set():
            try:
                samples.append(await asyncio.to_thread(gpu))
            except Exception as error:
                samples.append({"error_type": type(error).__name__})
            try:
                await asyncio.wait_for(stop.wait(), timeout=2)
            except TimeoutError:
                pass

    sampler = asyncio.create_task(sample())
    completed = []
    try:
        async with asyncio.timeout(1200):
            retrieval = await asyncio.to_thread(Retrieval)
            async with cached_provider(
                output, source=CACHED_MODEL_14B, quantization="nf4", preparation_seconds=180
            ) as provider:
                for case in protocol["cases"]:
                    if not provider.usable or budget.remaining() <= 0:
                        write_new(
                            output / (case["id"] + "-not-run.json"),
                            {"case": case, "status": "not_run_budget_or_worker"},
                        )
                        continue
                    case_dir = output / case["id"]
                    case_dir.mkdir(exist_ok=False)

                    def record(event, row, destination=case_dir):
                        write_new(
                            destination / (row["stage"] + "-" + row["attempt_id"] + "-" + event + ".json"),
                            row,
                        )

                    port = ReviewRepairGenerationAdapter(
                        provider, budget=budget, revalidate=retrieval.revalidate, record=record
                    )
                    lab = None
                    capture = {"case": case, "semantic_support": "unverified", "publication_allowed": False}
                    try:
                        if case["kind"] == "exposed_replay":
                            archived_path = ROOT / case["receipt"]
                            if hashlib.sha256(archived_path.read_bytes()).hexdigest() != case["sha256"]:
                                raise ValueError("Archived receipt changed")
                            archived = json.loads(archived_path.read_text(encoding="utf8"))
                            lab = DiagnosticStudy(
                                retrieval,
                                None,
                                authority=lambda: True,
                                budget=TrialBudget(),
                                course="ingenieria-software",
                                activity="requirements-teacher-diagnostic-v2",
                            )
                            lab.validate()
                            lab.checked_passages(archived["retrieval"])
                            req = LabGenerationRequest.model_validate(archived["request"])
                            capture["retrieval"] = archived["retrieval"]
                            capture["request"] = req.model_dump()
                            final = await port.process(
                                req, GenerationOutcome.model_validate(archived["outcome"])
                            )
                            capture["final_outcome"] = final.model_dump()
                            capture["review_repair"] = copy.deepcopy(port.last_review_trace)
                        else:
                            lab = DiagnosticStudy(
                                retrieval,
                                port,
                                authority=lambda: True,
                                budget=TrialBudget(),
                                course="ingenieria-software",
                                activity="requirements-teacher-diagnostic-v2",
                            )
                            result = await lab.turn(case["question"], case["id"], focus_change=True)
                            receipt = lab.receipt(result["id"])
                            capture["diagnostic_receipt"] = receipt
                            capture["review_repair"] = receipt.get("review_repair")
                            capture["retrieval"] = receipt.get("retrieval")
                            capture["request"] = receipt.get("request")
                            if receipt.get("outcome"):
                                capture["final_outcome"] = receipt["outcome"]
                        print("DIAGNÓSTICO UNVERIFIED — " + case["id"], flush=True)
                        print(
                            capture.get("final_outcome", {}).get("text", "(sin candidata final completa)"),
                            flush=True,
                        )
                        completed.append(case["id"])
                    except (Exception, asyncio.CancelledError) as error:
                        capture["error_type"] = type(error).__name__
                        capture["review_repair"] = copy.deepcopy(port.last_review_trace)
                        if isinstance(error, asyncio.CancelledError):
                            raise
                    finally:
                        write_new(case_dir / "capture.json", capture)
                        port.clear_diagnostic()
                        if lab:
                            lab.close()
    finally:
        stop.set()
        await sampler
        samples.append(gpu())
        write_new(output / "gpu-samples.json", samples)
        write_new(
            output / "count.json",
            {
                "llm_calls": budget.used,
                "completed": completed,
                "publication_allowed": False,
                "human_session": False,
            },
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute-authorized-trial", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--protocol", type=Path)
    args = parser.parse_args()
    if not args.execute_authorized_trial:
        parser.error("Default refuses inference; explicit authorized execution required")
    asyncio.run(trial(args.output, args.protocol))
