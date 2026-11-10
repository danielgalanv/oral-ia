"""One bounded offline claim-review trial; diagnostic only, never publication."""

import argparse
import asyncio
import hashlib
import json
import time
import zipfile
from pathlib import Path

from oralia.course_dialogue.__main__ import lab_root
from oralia.course_dialogue.cached_transformers import CACHED_MODEL_14B, cached_provider
from oralia.course_dialogue.claim_review import ClaimReview, validate_review
from oralia.course_dialogue.corpus import load_catalog
from oralia.course_study.__main__ import owned_lock
from oralia.infrastructure.generation.generation_port import (
    EvidenceItem,
    GenerationConstraints,
    GenerationError,
    GenerationRequest,
)

ROOT = Path(__file__).resolve().parents[1]
INSTRUCTION = (
    "Eres un revisor técnico de laboratorio. Evalúa SOLO la afirmación marcada, en el "
    "contexto de la pregunta y respuesta completas. Distingue supuesto ficticio, afirmación "
    "general y conclusión. Devuelve supported solo si el pasaje original y, para una conclusión, "
    "las premisas explícitas de la respuesta justifican realmente la afirmación; citar una página "
    "relacionada no basta. Devuelve unsupported cuando una propiedad o conclusión central no se "
    "sigue de lo dicho, aunque el resto de la respuesta sea correcto. Devuelve unknown si faltan "
    "datos para decidir. No presupongas que la frase marcada es válida. Copia pasaje y premisas "
    "literalmente; usa null para fuente y pasaje cuando no exista apoyo, y explica brevemente. "
    "No eres docente ni autorizas publicación. Devuelve solamente el JSON del esquema."
)
SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["kind", "verdict", "source_id", "source_passage", "premise_quotes", "rationale"],
    "properties": {
        "kind": {"type": "string", "enum": ["fiction", "general", "conclusion"]},
        "verdict": {"type": "string", "enum": ["supported", "unsupported", "unknown"]},
        "source_id": {"type": ["string", "null"]},
        "source_passage": {"type": ["string", "null"]},
        "premise_quotes": {"type": "array", "items": {"type": "string"}},
        "rationale": {"type": "string"},
    },
}


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
            data, _ = await asyncio.wait_for(process.communicate(), timeout=5)
            result[key] = data.decode(errors="replace").strip() if process.returncode == 0 else None
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


def request_for(case, quote, pages):
    return GenerationRequest(
        purpose="resumen",
        instruction=INSTRUCTION,
        student_input=json.dumps(
            {"question": case["question"], "answer": case["answer"], "claim_to_review": quote},
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
        output_schema=SCHEMA,
        constraints=GenerationConstraints(max_tokens=320, deadline_ms=30000),
    )


def adjudicate_structure(case, quote, parsed, pages):
    if not isinstance(parsed, dict) or set(parsed) != set(SCHEMA["required"]):
        raise ValueError("invalid response fields")
    if not isinstance(parsed["premise_quotes"], list):
        raise ValueError("premise_quotes must be an array")
    start = case["answer"].index(quote)
    claim = ClaimReview(
        start=start,
        end=start + len(quote),
        quote=quote,
        kind=parsed["kind"],
        central=True,
        verdict=parsed["verdict"],
        premise_quotes=tuple(parsed["premise_quotes"]),
        source_id=parsed["source_id"],
        source_passage=parsed["source_passage"],
        rationale=parsed["rationale"],
    )
    validate_review(case["answer"], (claim,), pages, (quote,))
    return claim


def classify_mismatch(kind, verdict, expected):
    """Keep semantic label errors distinct from class and abstention mismatches."""
    if verdict != expected["verdict"]:
        if verdict == "supported" and expected["verdict"] == "unsupported":
            return "false_permission"
        if verdict == "unsupported" and expected["verdict"] == "supported":
            return "false_rejection"
        return "unknown_mismatch"
    if kind != expected["kind"]:
        return "classification_mismatch"
    return None


async def run(output, inputs, oracle, pages):
    samples = []
    stop = asyncio.Event()
    watcher = asyncio.create_task(monitor(samples, stop))
    summary = {
        "claims_attempted": 0,
        "cases_completed": 0,
        "stopped_at": None,
        "reason": None,
        "publication_allowed": False,
    }
    try:
        async with cached_provider(
            output, source=CACHED_MODEL_14B, quantization="nf4", enable_thinking=False
        ) as provider:
            for case in inputs["cases"]:
                for quote in case["central_quotes"]:
                    request = request_for(case, quote, pages)
                    row = {
                        "case_id": case["id"],
                        "quote": quote,
                        "request": request.model_dump(mode="json"),
                        "publication_allowed": False,
                    }
                    started = time.perf_counter()
                    try:
                        outcome = await provider.generate(request)
                        row["outcome"] = outcome.model_dump(mode="json")
                        if not outcome.ok or outcome.finish_reason not in (None, "stop"):
                            raise ValueError("incomplete response")
                        parsed = json.loads(outcome.text)
                        claim = adjudicate_structure(case, quote, parsed, pages)
                        row["claim"] = {
                            "kind": claim.kind,
                            "verdict": claim.verdict,
                            "source_id": claim.source_id,
                            "source_passage": claim.source_passage,
                            "premise_quotes": claim.premise_quotes,
                            "rationale": claim.rationale,
                        }
                        expected = oracle[case["id"]][quote]
                        row["expected_after_inference"] = expected
                        row["failure"] = classify_mismatch(claim.kind, claim.verdict, expected)
                        row["match"] = row["failure"] is None
                    except (ValueError, TypeError, KeyError, GenerationError) as exc:
                        row["failure"] = "invalid_output"
                        row["diagnostic"] = f"{type(exc).__name__}: {exc}"
                    row["elapsed_seconds"] = time.perf_counter() - started
                    summary["claims_attempted"] += 1
                    save(output / f"{case['id']}-{summary['claims_attempted']:02d}.json", row)
                    print(case["id"], row.get("claim", {}).get("verdict", row.get("failure")), flush=True)
                    if row.get("failure") or not provider.usable:
                        summary["stopped_at"] = {"case_id": case["id"], "quote": quote}
                        summary["reason"] = row.get("failure", "worker_unavailable")
                        return summary
                summary["cases_completed"] += 1
    finally:
        stop.set()
        await watcher
        save(output / "gpu-telemetry.json", samples)
        save(output / "gpu-after.json", await gpu_snapshot())
        save(output / "summary.json", summary)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--oracle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    inputs_path, oracle_path, output = (p.resolve() for p in (args.inputs, args.oracle, args.output))
    if any(not p.is_relative_to(ROOT) for p in (inputs_path, oracle_path, output)) or output.exists():
        parser.error("Input, oracle and new output must be inside workspace")
    inputs_bytes, oracle_bytes = inputs_path.read_bytes(), oracle_path.read_bytes()
    inputs, oracle = json.loads(inputs_bytes), json.loads(oracle_bytes)
    output.mkdir(parents=True)
    sources = [
        "scripts/trial_chat_claim_reviewer.py",
        "src/oralia/course_dialogue/claim_review.py",
        "src/oralia/course_dialogue/cached_transformers.py",
        "src/oralia/course_dialogue/gpu_worker.py",
        "src/oralia/course_dialogue/corpus.py",
        "src/oralia/infrastructure/generation/generation_port.py",
    ]
    with zipfile.ZipFile(output / "source-before.zip", "x", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("inputs.json", inputs_bytes)
        archive.writestr("oracle.json", oracle_bytes)
        for name in sources:
            archive.writestr(name, (ROOT / name).read_bytes())
    save(
        output / "frozen-run.json",
        {
            "inputs_sha256": hashlib.sha256(inputs_bytes).hexdigest(),
            "oracle_sha256": hashlib.sha256(oracle_bytes).hexdigest(),
            "source_sha256": {
                name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources
            },
            "model": str(CACHED_MODEL_14B),
            "quantization": "nf4",
            "instruction": INSTRUCTION,
            "schema": SCHEMA,
            "stop_condition": "first wrong kind/verdict, malformed/omitted output or unusable worker",
            "participant_publication": False,
        },
    )
    pages = {page["id"]: page for page in load_catalog()}
    save(
        output / "page-hashes.json",
        {
            page_id: pages[page_id]["text_sha256"]
            for case in inputs["cases"]
            for page_id in case["source_ids"]
        },
    )

    async def preflight():
        before = []
        for _ in range(3):
            before.append(await gpu_snapshot())
            await asyncio.sleep(1)
        save(output / "gpu-before.json", before)
        return before

    before = asyncio.run(preflight())
    if any(sample["gpu"] is None for sample in before):
        save(output / "not-run.json", {"reason": "gpu_telemetry_unavailable"})
        return
    if any(
        int(sample["gpu"].split(",")[1].strip()) > 10 or int(sample["gpu"].split(",")[3].strip()) < 16000
        for sample in before
    ):
        save(output / "not-run.json", {"reason": "gpu_busy_or_insufficient_free_memory"})
        return
    with owned_lock(lab_root(ROOT)):
        asyncio.run(run(output, inputs, oracle, pages))


if __name__ == "__main__":
    main()
