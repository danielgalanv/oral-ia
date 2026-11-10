"""One frozen local calibration of a separate semantic reviewer; never a publication gate."""

import argparse
import asyncio
import hashlib
import json
import time
import zipfile
from pathlib import Path

from oralia.course_dialogue.__main__ import lab_root
from oralia.course_dialogue.cached_transformers import CACHED_MODEL_14B, cached_provider
from oralia.course_dialogue.corpus import load_catalog
from oralia.course_study.__main__ import owned_lock
from oralia.infrastructure.generation.generation_port import (
    EvidenceItem,
    GenerationConstraints,
    GenerationRequest,
)

ROOT = Path(__file__).resolve().parents[1]


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


async def gpu_snapshot():
    result = {"monotonic": time.monotonic()}
    for key, args in (
        (
            "gpu",
            (
                "--query-gpu=timestamp,utilization.gpu,memory.used,memory.free,power.draw",
                "--format=csv,noheader,nounits",
            ),
        ),
        ("compute_apps", ("--query-compute-apps=pid,used_gpu_memory", "--format=csv,noheader,nounits")),
    ):
        try:
            process = await asyncio.create_subprocess_exec(
                "nvidia-smi", *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL
            )
            output, _ = await asyncio.wait_for(process.communicate(), timeout=5)
            result[key] = output.decode(errors="replace").strip() if process.returncode == 0 else None
        except (OSError, TimeoutError):
            result[key] = None
    return result


async def monitor(samples, stop):
    while not stop.is_set():
        samples.append(await gpu_snapshot())
        try:
            await asyncio.wait_for(stop.wait(), timeout=2)
        except TimeoutError:
            pass


async def run(output, protocol, pages):
    samples = []
    stop = asyncio.Event()
    watcher = asyncio.create_task(monitor(samples, stop))
    summary = {"cases_attempted": 0, "matches": 0, "stopped_at": None, "publication_allowed": False}
    try:
        async with cached_provider(
            output, source=CACHED_MODEL_14B, quantization="nf4", enable_thinking=False
        ) as provider:
            for case in protocol["cases"]:
                request = GenerationRequest(
                    purpose="resumen",
                    instruction=(
                        "Eres un revisor técnico independiente del generador, no docente. "
                        "Decide si la RESPUESTA mostrada atiende exactamente la PREGUNTA y si todas "
                        "sus afirmaciones generales centrales están respaldadas por las PÁGINAS. "
                        "En un ejemplo ficticio, los datos inventados no necesitan aparecer en las páginas, "
                        "pero las propiedades atribuidas al requisito y la conclusión sí deben deducirse "
                        "de esos datos y de los criterios del curso. Si falta definir un término decisivo, "
                        "si una conclusión no se sigue, si se arrastra otro tema o se confirma una "
                        "idea falsa, "
                        "rechaza. Acepta una inferencia válida y pertinente aunque no sea cita literal. "
                        "La referencia de página por sí sola no prueba apoyo. "
                        "Devuelve solo el JSON solicitado."
                    ),
                    student_input=json.dumps(
                        {"pregunta_actual": case["question"], "respuesta_mostrada": case["answer"]},
                        ensure_ascii=False,
                    ),
                    evidence=[
                        EvidenceItem(
                            fragment_id=page_id,
                            document_id=pages[page_id]["filename"],
                            document_version=1,
                            text=pages[page_id]["text"],
                        )
                        for page_id in case["source_ids"]
                    ],
                    output_schema={
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["decision"],
                        "properties": {"decision": {"type": "string", "enum": ["accept", "reject"]}},
                    },
                    constraints=GenerationConstraints(max_tokens=48, deadline_ms=30000),
                )
                started = time.perf_counter()
                row = {
                    "id": case["id"],
                    "expected_frozen": case["expected"],
                    "request": request.model_dump(mode="json"),
                    "publication_allowed": False,
                }
                try:
                    outcome = await provider.generate(request)
                    row["outcome"] = outcome.model_dump(mode="json")
                    parsed = json.loads(outcome.text)
                    if not outcome.ok or outcome.finish_reason not in (None, "stop"):
                        raise ValueError("incomplete verifier outcome")
                    if set(parsed) != {"decision"} or parsed["decision"] not in {"accept", "reject"}:
                        raise ValueError("invalid verifier decision")
                    row["decision"] = parsed["decision"]
                    row["match"] = parsed["decision"] == case["expected"]
                except (ValueError, TypeError) as exc:
                    row["error"] = type(exc).__name__
                    row["diagnostic"] = str(exc)
                row["elapsed_seconds"] = time.perf_counter() - started
                summary["cases_attempted"] += 1
                summary["matches"] += int(row.get("match", False))
                save(output / f"{case['id']}.json", row)
                print(case["id"], row.get("decision", row.get("error")), row.get("match"), flush=True)
                if not row.get("match") or not provider.usable:
                    summary["stopped_at"] = case["id"]
                    break
    finally:
        stop.set()
        await watcher
        save(output / "gpu-telemetry.json", samples)
        save(output / "gpu-after.json", await gpu_snapshot())
        save(output / "summary.json", summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    protocol_path = args.protocol.resolve()
    output = args.output.resolve()
    if not protocol_path.is_relative_to(ROOT) or not output.is_relative_to(ROOT) or output.exists():
        parser.error("Protocol and new output must be inside the workspace")
    protocol_bytes = protocol_path.read_bytes()
    protocol = json.loads(protocol_bytes)
    output.mkdir(parents=True)
    source_names = [
        "scripts/calibrate_chat_semantic_verifier.py",
        "src/oralia/course_dialogue/cached_transformers.py",
        "src/oralia/course_dialogue/gpu_worker.py",
        "src/oralia/course_dialogue/corpus.py",
        "src/oralia/infrastructure/generation/generation_port.py",
        "src/oralia/infrastructure/generation/ollama_adapter.py",
    ]
    with zipfile.ZipFile(output / "source-before.zip", "x", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("protocol.json", protocol_bytes)
        for name in source_names:
            archive.writestr(name, (ROOT / name).read_bytes())
    save(
        output / "frozen-run.json",
        {
            "protocol_sha256": hashlib.sha256(protocol_bytes).hexdigest(),
            "source_sha256": {
                name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in source_names
            },
            "model": str(CACHED_MODEL_14B),
            "quantization": "nf4",
            "participant_publication": False,
        },
    )
    pages = {page["id"]: page for page in load_catalog()}
    save(
        output / "page-hashes.json",
        {
            page_id: pages[page_id]["text_sha256"]
            for case in protocol["cases"]
            for page_id in case["source_ids"]
        },
    )

    async def preflight():
        before = []
        for _ in range(3):
            before.append(await gpu_snapshot())
            await asyncio.sleep(1)
        save(output / "gpu-before.json", before)

    asyncio.run(preflight())
    with owned_lock(lab_root(ROOT)):
        asyncio.run(run(output, protocol, pages))


if __name__ == "__main__":
    main()
