"""Repair exposed candidates from explicit agent-supplied critiques, not self-review.

This isolates the corrector when a critic has actually identified the error.
The current assistant performs post-review outside this local-model runner.
"""

import argparse
import asyncio
import copy
import hashlib
import json
from pathlib import Path

from run_review_repair_trial import gpu, write_new

from oralia.course_dialogue.lab_request import LabGenerationRequest
from oralia.course_dialogue.review_repair import CallBudget, ReviewRepairGenerationAdapter
from oralia.documentary.study_lab import DiagnosticStudy, TrialBudget
from oralia.infrastructure.generation.generation_port import GenerationOutcome

ROOT = Path(__file__).resolve().parents[1]
DOSSIER = ROOT / "docs/audits/2026-10-28-agent-assisted-repair"


async def trial(output):
    from oralia.course_dialogue.cached_transformers import CACHED_MODEL_14B, cached_provider
    from oralia.documentary.retrieval import Retrieval

    protocol = json.loads((DOSSIER / "protocol-v1.json").read_text(encoding="utf8"))
    for path, expected in protocol["sha256"].items():
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != expected:
            raise ValueError("Frozen artifact changed: " + path)
    cards = json.loads((DOSSIER / "supplied-critiques-v1.json").read_text(encoding="utf8"))
    output.mkdir(parents=True, exist_ok=False)
    write_new(output / "protocol.json", protocol)
    budget = CallBudget(maximum=4, seconds=600)
    before = gpu()
    write_new(output / "gpu-before.json", before)
    if before["used_mib"] > 2000 or before["utilization_percent"] > 5:
        raise ValueError("GPU competition; do not load")
    print("AGENT-ASSISTED REPAIR:4exposed cases,4calls+1warmup,768tokens/50s,10min global.", flush=True)
    samples = [before]
    stop = asyncio.Event()

    async def sample():
        while not stop.is_set():
            samples.append(await asyncio.to_thread(gpu))
            try:
                await asyncio.wait_for(stop.wait(), timeout=2)
            except TimeoutError:
                pass

    sampler = asyncio.create_task(sample())
    try:
        async with asyncio.timeout(600):
            retrieval = await asyncio.to_thread(Retrieval)
            async with cached_provider(
                output, source=CACHED_MODEL_14B, quantization="nf4", preparation_seconds=180
            ) as provider:
                for card in cards["cases"]:
                    destination = output / card["id"]
                    destination.mkdir(exist_ok=False)
                    if not provider.usable or budget.remaining() <= 0:
                        write_new(destination / "not-run.json", {"status": "not_run_worker_or_budget"})
                        continue
                    path = ROOT / card["receipt"]
                    if hashlib.sha256(path.read_bytes()).hexdigest() != card["sha256"]:
                        raise ValueError("Archived candidate changed")
                    archived = json.loads(path.read_text(encoding="utf8"))
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

                    def record(event, row, folder=destination):
                        write_new(folder / (row["attempt_id"] + "-" + event + ".json"), row)

                    port = ReviewRepairGenerationAdapter(
                        provider, budget=budget, revalidate=lab.validate, record=record
                    )
                    capture = {
                        "card": card,
                        "retrieval": archived["retrieval"],
                        "request": archived["request"],
                        "semantic_support": "unverified",
                        "publication_allowed": False,
                        "post_review": "pending_current_assistant",
                    }
                    try:
                        final = await port.repair_with_supplied_review(
                            LabGenerationRequest.model_validate(archived["request"]),
                            GenerationOutcome.model_validate(archived["outcome"]),
                            card["review"],
                        )
                        capture["final_outcome"] = final.model_dump()
                        print("CANDIDATA UNVERIFIED — " + card["id"], flush=True)
                        print(final.text, flush=True)
                    except Exception as error:
                        capture["error_type"] = type(error).__name__
                    finally:
                        capture["review_repair"] = copy.deepcopy(port.last_review_trace)
                        write_new(destination / "capture.json", capture)
                        port.clear_diagnostic()
                        lab.close()
    finally:
        stop.set()
        await sampler
        samples.append(gpu())
        write_new(output / "gpu-samples.json", samples)
        write_new(
            output / "count.json",
            {"repair_llm_calls": budget.used, "publication_allowed": False, "autonomous_verifier": False},
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute-authorized-trial", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.execute_authorized_trial:
        parser.error("Explicit authorized execution required")
    asyncio.run(trial(args.output))
