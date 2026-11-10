"""Future explicitly authorized trial only. Default invocation does not load models.

Not executed by the CPU increment. This is an offline experimental inspection,
not a participant session or a claim that a human used the tutor.
"""

import argparse
import asyncio
import hashlib
import json
import subprocess
import time
import uuid
from pathlib import Path

from oralia.documentary.study_lab import INSTRUCTION, DiagnosticStudy, TrialBudget

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs/audits/2026-10-27-generated-study-cpu/protocol-v2-50s.json"


def gpu():
    result = subprocess.run(
        [
            "nvidia-smi",
            "--query-gpu=memory.used,memory.total,utilization.gpu",
            "--format=csv,noheader,nounits",
        ],
        capture_output=True,
        text=True,
        timeout=5,
        check=True,
    )
    rows = [list(map(int, line.split(","))) for line in result.stdout.strip().splitlines()]
    if len(rows) != 1:
        raise ValueError("Disponibilidad GPU ambigua; se aplaza")
    return {
        "monotonic": time.monotonic(),
        "used_mib": rows[0][0],
        "total_mib": rows[0][1],
        "utilization_percent": rows[0][2],
    }


def mechanical_recovery_start(prior):
    count = json.loads((prior / "count.json").read_text(encoding="utf8"))
    cleanup = json.loads((prior / "worker-cleanup.json").read_text(encoding="utf8"))
    log = (prior / "worker-stderr.log").read_text(encoding="utf8")
    if (
        count["academic_requests"] != 0
        or (prior / "worker.json").exists()
        or not cleanup["owned_tree_stopped"]
        or '"stage": "weights_loaded"' in log
    ):
        raise ValueError("No recovery: prior academic use/warmup uncertain or worker not stopped")
    return json.loads((prior / "gpu-before.json").read_text(encoding="utf8"))[0]["monotonic"]


async def trial(output, mechanical_recovery_from=None):
    # Imports/load exclusively after the explicit CLI switch, never app startup.
    from oralia.course_dialogue.cached_transformers import CACHED_MODEL_14B, cached_provider
    from oralia.documentary.retrieval import Retrieval

    output.mkdir(parents=True, exist_ok=False)
    protocol = json.loads(PROTOCOL.read_text(encoding="utf8"))
    if protocol["instruction_sha256"] != hashlib.sha256(INSTRUCTION.encode()).hexdigest():
        raise ValueError("Instrucción distinta de la congelada; no inferir")
    if CACHED_MODEL_14B.name != protocol["snapshot"]:
        raise ValueError("Snapshot distinto del protocolizado; no cambiar de modelo")
    (output / "protocol.json").write_text(json.dumps(protocol, ensure_ascii=False, indent=2), encoding="utf8")
    print(
        "ENSAYO FUTURO AUTORIZADO: Qwen2.5-14B NF4 local; CPU encoder; "
        "8 peticiones + calentamiento interno1token;768tokens/50s;20min globales.",
        flush=True,
    )
    samples = [gpu()]
    (output / "gpu-before.json").write_text(json.dumps(samples), encoding="utf8")
    if samples[0]["used_mib"] > 2000 or samples[0]["utilization_percent"] > 5:
        raise ValueError("Competencia GPU o disponibilidad incierta: no cargar el modelo")
    stop = asyncio.Event()

    async def sample():
        while not stop.is_set():
            try:
                samples.append(await asyncio.to_thread(gpu))
            except Exception as error:
                samples.append({"measurement_error": type(error).__name__})
            try:
                await asyncio.wait_for(stop.wait(), timeout=2)
            except TimeoutError:
                pass

    sampler = asyncio.create_task(sample())
    budget = TrialBudget(
        started=(
            mechanical_recovery_start(mechanical_recovery_from)
            if mechanical_recovery_from
            else time.monotonic()
        )
    )
    preparation_seconds = 180 if mechanical_recovery_from else 90
    (output / "preparation-budget.json").write_text(
        json.dumps(
            {
                "preparation_seconds": preparation_seconds,
                "mechanical_recovery_from": (
                    str(mechanical_recovery_from) if mechanical_recovery_from else None
                ),
                "global_started_monotonic": budget.started,
                "remaining_global_seconds": budget.remaining(),
                "academic_request_ms_unchanged": 50000,
            },
            indent=2,
        ),
        encoding="utf8",
    )
    complete = set()
    lab = None
    try:
        async with asyncio.timeout(max(0, budget.remaining())):
            retrieval = await asyncio.to_thread(Retrieval)  # existing CPU-only profile, build=False
            async with cached_provider(
                output, source=CACHED_MODEL_14B, quantization="nf4", preparation_seconds=preparation_seconds
            ) as provider:
                for scenario in protocol["scenarios"]:
                    if scenario["depends_on"] and scenario["depends_on"] not in complete:
                        row = {"status": "not_run_dependency_not_shown", "scenario": scenario}
                    elif not provider.usable:
                        row = {"status": "not_run_worker_unusable", "scenario": scenario}
                    else:
                        if scenario["depends_on"] is None:
                            if lab:
                                lab.close()
                            lab = DiagnosticStudy(
                                retrieval,
                                provider,
                                authority=lambda: True,
                                budget=budget,
                                course="ingenieria-software",
                                activity="requirements-teacher-diagnostic-v2",
                            )
                        result = await lab.turn(
                            scenario["question"],
                            str(uuid.uuid4()),
                            focus_change=scenario.get("focus_change", False),
                        )
                        row = lab.receipt(result["id"])
                        row["scenario"] = scenario
                        if result["status"] == "prepared_unverified":
                            shown = lab.display(result["id"])
                            # Console text is the offline diagnostic surface. Never
                            # acknowledge a missing/truncated/blocked candidate.
                            print("CANDIDATA DIAGNÓSTICA UNVERIFIED — " + scenario["id"], flush=True)
                            print(shown["diagnostic_preview"], flush=True)
                            print(json.dumps(shown["retrieval"]["passages"], ensure_ascii=False), flush=True)
                            lab.acknowledge(result["id"])
                            row = lab.receipt(result["id"])
                            row["scenario"] = scenario
                            complete.add(scenario["id"])
                    with (output / (scenario["id"] + "-" + uuid.uuid4().hex + ".json")).open(
                        "x", encoding="utf8"
                    ) as f:
                        json.dump(row, f, ensure_ascii=False, indent=2)
    finally:
        if lab:
            lab.close()
        stop.set()
        await sampler
        try:
            samples.append(gpu())
        except Exception as error:
            samples.append({"measurement_error": type(error).__name__})
        (output / "gpu-samples.json").write_text(json.dumps(samples, indent=2), encoding="utf8")
        (output / "count.json").write_text(
            json.dumps(
                {
                    "academic_requests": budget.used,
                    "complete_console_diagnostics": sorted(complete),
                    "human_session": False,
                    "publication_allowed": False,
                }
            ),
            encoding="utf8",
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute-future-authorized-trial", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--mechanical-recovery-from", type=Path)
    args = parser.parse_args()
    if not args.execute_future_authorized_trial or args.output is None:
        parser.error(
            "No inference. Requires future explicit authorization, execution switch and exclusive output."
        )
    asyncio.run(trial(args.output, args.mechanical_recovery_from))
