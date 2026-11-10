"""One bounded closed-reference local claim trial; no participant authority."""

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


def source_options(case, pages):
    """Enumerate every nonempty original page line, without oracle selection."""
    options = {}
    for page_id in case["source_ids"]:
        for line in pages[page_id]["text"].splitlines():
            if line.strip():
                key = f"S{len(options) + 1:02d}"
                options[key] = {"source_id": page_id, "source_passage": line}
    if not 1 <= len(options) <= 32:
        raise ValueError("source menu outside finite decoder bounds")
    return options


def premise_options(case, quote):
    """Enumerate answer sentences without selecting an oracle premise."""
    sentences = [part.strip() + "." for part in case["answer"].split(". ")]
    options = {}
    for sentence in sentences:
        if sentence and sentence != quote and sentence in case["answer"]:
            options[f"P{len(options) + 1:02d}"] = sentence
    if not 1 <= len(options) <= 32:
        raise ValueError("premise menu outside finite decoder bounds")
    return options


def finite_request(case, quote, pages, field, options, instruction, menu):
    return GenerationRequest(
        purpose="resumen",
        instruction=instruction,
        student_input=json.dumps(
            {
                "question": case["question"],
                "answer": case["answer"],
                "claim_to_review": quote,
                "fixed_kind": case["kinds"][quote],
                "options": menu,
            },
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
            "required": [field],
            "properties": {field: {"type": "string", "enum": options}},
        },
        constraints=GenerationConstraints(max_tokens=64, deadline_ms=30000),
    )


async def choose(provider, request, field):
    outcome = await provider.generate(request)
    if not outcome.ok or outcome.finish_reason not in (None, "stop"):
        raise ValueError("incomplete finite choice")
    parsed = json.loads(outcome.text)
    if not isinstance(parsed, dict) or set(parsed) != {field}:
        raise ValueError("invalid finite choice")
    chosen = parsed[field]
    if chosen not in request.output_schema["properties"][field]["enum"]:
        raise ValueError("choice outside frozen menu")
    return chosen, outcome.model_dump(mode="json")


async def evaluate_claim(provider, case, quote, pages):
    trace = []
    preamble = (
        "Eres un revisor técnico de laboratorio, no docente. Evalúa solo la afirmación marcada "
        "en la pregunta y respuesta completas. La clase del tramo se ha fijado por separado y "
        "no debes evaluarla. Elige supported si el texto original y las premisas declaradas "
        "justifican realmente la afirmación; unsupported si una propiedad o conclusión no se "
        "sigue; unknown si no puedes decidir. Una explicación principal correcta no justifica "
        "cualquier conclusión añadida. Elige solo una opción del esquema; no autorizas publicación."
    )
    request = finite_request(
        case,
        quote,
        pages,
        "verdict",
        ["supported", "unsupported", "unknown"],
        preamble,
        [],
    )
    verdict, outcome = await choose(provider, request, "verdict")
    trace.append({"step": "verdict", "request": request.model_dump(mode="json"), "outcome": outcome})
    source_id = source_passage = None
    premises = ()
    rationale = ""
    if verdict == "supported":
        sources = source_options(case, pages)
        request = finite_request(
            case,
            quote,
            pages,
            "source_ref",
            list(sources),
            "Elige el pasaje original que mejor respalda la afirmación marcada. "
            "La existencia de un pasaje relacionado no demuestra por sí sola apoyo; "
            "selecciona solo una referencia de la lista cerrada.",
            sources,
        )
        chosen, outcome = await choose(provider, request, "source_ref")
        trace.append({"step": "source_ref", "request": request.model_dump(mode="json"), "outcome": outcome})
        source_id, source_passage = sources[chosen].values()
        if case["kinds"][quote] == "conclusion":
            options = premise_options(case, quote)
            request = finite_request(
                case,
                quote,
                pages,
                "premise_ref",
                list(options),
                "Elige una premisa declarada en la respuesta que sea necesaria para la "
                "conclusión marcada. Solo puedes escoger una frase real de la lista; "
                "no copies la página ni la propia conclusión como premisa.",
                options,
            )
            chosen, outcome = await choose(provider, request, "premise_ref")
            trace.append(
                {"step": "premise_ref", "request": request.model_dump(mode="json"), "outcome": outcome}
            )
            premises = (options[chosen],)
    else:
        reasons = {
            "missing_conditions": "model_reason:missing_conditions",
            "invalid_inference": "model_reason:invalid_inference",
            "source_absent": "model_reason:source_absent",
            "uncertain": "model_reason:uncertain",
        }
        request = finite_request(
            case,
            quote,
            pages,
            "reason_ref",
            list(reasons),
            "Elige una razón breve para tu etiqueta. La selección registra tu juicio, "
            "no prueba su verdad. Devuelve solo una opción del esquema.",
            reasons,
        )
        chosen, outcome = await choose(provider, request, "reason_ref")
        trace.append({"step": "reason_ref", "request": request.model_dump(mode="json"), "outcome": outcome})
        rationale = reasons[chosen]
    start = case["answer"].index(quote)
    claim = ClaimReview(
        start=start,
        end=start + len(quote),
        quote=quote,
        kind=case["kinds"][quote],
        central=True,
        verdict=verdict,
        premise_quotes=premises,
        source_id=source_id,
        source_passage=source_passage,
        rationale=rationale,
    )
    validate_review(case["answer"], (claim,), {key: value["text"] for key, value in pages.items()}, (quote,))
    return claim, trace


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
                    row = {"case_id": case["id"], "quote": quote, "publication_allowed": False}
                    started = time.perf_counter()
                    try:
                        claim, trace = await evaluate_claim(provider, case, quote, pages)
                        row["trace"] = trace
                        row["claim"] = {
                            "kind_fixed_before_inference": claim.kind,
                            "verdict": claim.verdict,
                            "source_id": claim.source_id,
                            "source_passage": claim.source_passage,
                            "premise_quotes": claim.premise_quotes,
                            "rationale": claim.rationale,
                        }
                        expected = oracle[case["id"]][quote]
                        row["expected_after_inference"] = expected
                        if claim.verdict != expected["verdict"]:
                            if claim.verdict == "supported" and expected["verdict"] == "unsupported":
                                row["failure"] = "false_permission"
                            elif claim.verdict == "unsupported" and expected["verdict"] == "supported":
                                row["failure"] = "false_rejection"
                            else:
                                row["failure"] = "unknown_mismatch"
                        elif claim.verdict == "supported":
                            row["witness_needs_manual_review"] = True
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
                        return
                summary["cases_completed"] += 1
    finally:
        stop.set()
        await watcher
        save(output / "gpu-telemetry.json", samples)
        save(output / "gpu-after.json", await gpu_snapshot())
        save(output / "summary.json", summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--oracle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    inputs_path, oracle_path, output = (path.resolve() for path in (args.inputs, args.oracle, args.output))
    if any(not path.is_relative_to(ROOT) for path in (inputs_path, oracle_path, output)) or output.exists():
        parser.error("Inputs, oracle and new output must be inside workspace")
    input_bytes, oracle_bytes = inputs_path.read_bytes(), oracle_path.read_bytes()
    inputs, oracle = json.loads(input_bytes), json.loads(oracle_bytes)
    output.mkdir(parents=True)
    sources = [
        "scripts/closed_reference_claim_trial.py",
        "src/oralia/course_dialogue/claim_review.py",
        "src/oralia/course_dialogue/cached_transformers.py",
        "src/oralia/course_dialogue/gpu_worker.py",
        "src/oralia/course_dialogue/corpus.py",
        "src/oralia/infrastructure/generation/generation_port.py",
        "src/oralia/course_dialogue/finite_schema.py",
    ]
    with zipfile.ZipFile(output / "source-before.zip", "x", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("inputs.json", input_bytes)
        archive.writestr("oracle.json", oracle_bytes)
        for name in sources:
            archive.writestr(name, (ROOT / name).read_bytes())
    save(
        output / "frozen-run.json",
        {
            "inputs_sha256": hashlib.sha256(input_bytes).hexdigest(),
            "oracle_sha256": hashlib.sha256(oracle_bytes).hexdigest(),
            "source_sha256": {
                name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources
            },
            "model": str(CACHED_MODEL_14B),
            "quantization": "nf4",
            "scope": (
                "fixed central spans and kinds; model selects verdict and "
                "closed source/premise/reason refs"
            ),
            "stop_condition": (
                "first false permission, false rejection, abstention mismatch or invalid output"
            ),
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
