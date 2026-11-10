"""Owned, offline replay of two frozen synthetic requests with GPU telemetry."""

import argparse
import asyncio
import hashlib
import json
import time
import zipfile
from pathlib import Path

from oralia.course_dialogue.__main__ import lab_root
from oralia.course_dialogue.cached_transformers import CACHED_MODEL_QWEN3_8B, cached_provider
from oralia.course_study.__main__ import owned_lock
from oralia.infrastructure.generation.generation_port import GenerationRequest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "specs/012-conversational-course-study/evidence/chat-comparison-extended-first"


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


async def sample_gpu(rows, stop):
    while not stop.is_set():
        entry = {"elapsed_monotonic": time.monotonic()}
        for label, arguments in [
            (
                "gpu",
                [
                    "--query-gpu=timestamp,utilization.gpu,memory.used,memory.free,power.draw,clocks.sm,temperature.gpu",
                    "--format=csv,noheader,nounits",
                ],
            ),
            ("compute_apps", ["--query-compute-apps=pid,used_gpu_memory", "--format=csv,noheader,nounits"]),
        ]:
            try:
                proc = await asyncio.create_subprocess_exec(
                    "nvidia-smi",
                    *arguments,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.DEVNULL,
                )
                output, _ = await asyncio.wait_for(proc.communicate(), timeout=5)
                entry[label] = output.decode(errors="replace").strip() if proc.returncode == 0 else None
            except (OSError, TimeoutError):
                entry[label] = None
        rows.append(entry)
        try:
            await asyncio.wait_for(stop.wait(), timeout=2)
        except TimeoutError:
            pass


async def run(output, requests):
    stop = asyncio.Event()
    telemetry = []
    sampler = asyncio.create_task(sample_gpu(telemetry, stop))
    results = []
    try:
        async with cached_provider(
            output, source=CACHED_MODEL_QWEN3_8B, quantization="nf4", enable_thinking=False
        ) as provider:
            for label in (
                "short-first",
                "first",
                "repeat",
                "short-first-after",
                "first-after",
                "repeat-after",
            ):
                base = requests["repeat" if "repeat" in label else "first"]
                request = base.model_copy(deep=True)
                if label.startswith("short"):
                    request.constraints.max_tokens = 1
                before = time.monotonic()
                try:
                    outcome = await provider.generate(request)
                    record = {
                        "label": label,
                        "outcome": outcome.model_dump(),
                        "raw_worker_response": provider.last_exchange.get("raw_worker_response"),
                    }
                except Exception as exc:
                    record = {
                        "label": label,
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                        "last_exchange": provider.last_exchange,
                    }
                record["wall_seconds"] = time.monotonic() - before
                results.append(record)
                save(output / "requests-results.json", results)
                print(
                    label,
                    record.get("error_type", record.get("outcome", {}).get("finish_reason")),
                    round(record["wall_seconds"], 2),
                    flush=True,
                )
    finally:
        stop.set()
        await sampler
        save(output / "gpu-telemetry.json", telemetry)


def main():
    parser = argparse.ArgumentParser(description="Bounded diagnostic, synthetic requests only")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT) or output.exists():
        parser.error("Output must be a new path inside the workspace")
    transcript = json.loads(
        (SOURCE / "validation-to-test-case-complete-pedagogica.json").read_text(encoding="utf-8")
    )
    requests = {
        "first": GenerationRequest.model_validate(transcript["turns"][0]["request_snapshot"]),
        "repeat": GenerationRequest.model_validate(transcript["turns"][2]["request_snapshot"]),
    }
    output.mkdir(parents=True)
    script = Path(__file__).read_bytes()
    protocol = {
        "source": str(SOURCE.relative_to(ROOT)),
        "source_transcript_sha256": hashlib.sha256(
            (SOURCE / "validation-to-test-case-complete-pedagogica.json").read_bytes()
        ).hexdigest(),
        "script_sha256": hashlib.sha256(script).hexdigest(),
        "request_sha256": {
            name: hashlib.sha256(
                json.dumps(request.model_dump(mode="json"), ensure_ascii=False, sort_keys=True).encode()
            ).hexdigest()
            for name, request in requests.items()
        },
        "sequence": ["short-first", "first", "repeat", "short-first-after", "first-after", "repeat-after"],
        "short_control": "max_tokens=1 probes combined prefill/first-token cost, not a direct phase split",
        "deadline_ms": 30000,
        "model": str(CACHED_MODEL_QWEN3_8B),
        "quantization": "nf4",
        "enable_thinking": False,
        "publication_allowed": False,
    }
    save(output / "protocol-before.json", protocol)
    with zipfile.ZipFile(output / "source-before.zip", "x", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("scripts/diagnose_chat_timeout.py", script)
        archive.writestr("protocol-before.json", (output / "protocol-before.json").read_bytes())
        for name in (
            "src/oralia/course_dialogue/gpu_worker.py",
            "src/oralia/course_dialogue/cached_transformers.py",
        ):
            archive.writestr(name, (ROOT / name).read_bytes())
    with owned_lock(lab_root(ROOT)):
        asyncio.run(run(output, requests))


if __name__ == "__main__":
    main()
