"""One frozen, fixed-source local generator diagnosis; never a participant route."""

import argparse
import asyncio
import hashlib
import json
import re
import time
import zipfile
from pathlib import Path

from oralia.course_dialogue.__main__ import lab_root
from oralia.course_dialogue.cached_transformers import (
    CACHED_MODEL_14B,
    CACHED_MODEL_MISTRAL_24B,
    cached_provider,
)
from oralia.course_dialogue.document_evidence import build_units
from oralia.course_dialogue.full_corpus import load_full_teacher_catalog
from oralia.course_dialogue.lab_request import LabGenerationRequest
from oralia.course_study.__main__ import owned_lock
from oralia.infrastructure.generation.generation_port import EvidenceItem, GenerationMessage

if __package__:
    from scripts.compare_course_chat import gpu_snapshot, monitor_gpu, save
else:
    from compare_course_chat import gpu_snapshot, monitor_gpu, save

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
PROTOCOL = EVIDENCE / "chat-fixed-source-14b-protocol.json"
UNITS = EVIDENCE / "chat-fixed-source-14b-units.json"
RUBRIC = EVIDENCE / "chat-fixed-source-14b-rubric.md"
INSTRUCTION = (
    "Diagnóstico local de explicación académica en español. Responde la pregunta actual y "
    "atiende al historial realmente mostrado. Cita entre corchetes el id exacto de cada "
    "unidad que sostenga un principio académico. No atribuyas hechos ficticios a las fuentes. "
    "Si inventas un escenario, usa 'Ejemplo hipotético:' y 'Supuestos ficticios:' y cita "
    "la fuente del principio que ilustra, no la existencia del escenario. Si una afirmación "
    "no está apoyada, usa 'Límite de fuentes:' o declara 'Inferencia:'. Conserva matices y "
    "límites, especialmente la diferencia entre lo deseable y lo garantizado. "
    "Solo texto final; no JSON ni aprobación docente."
)


def local_model_profile(name):
    if name == "qwen14b":
        return CACHED_MODEL_14B, None
    if name == "mistral24b":
        return CACHED_MODEL_MISTRAL_24B, "mistral_regex_local"
    raise ValueError("Unknown local laboratory model")


def load_frozen(protocol_path=PROTOCOL, units_path=UNITS):
    protocol_bytes = protocol_path.read_bytes()
    unit_bytes = units_path.read_bytes()
    protocol = json.loads(protocol_bytes)
    frozen = json.loads(unit_bytes)
    if frozen["protocol_sha256"] != hashlib.sha256(protocol_bytes).hexdigest():
        raise ValueError("Frozen protocol hash changed")
    actual = {unit.id: unit for unit in build_units(load_full_teacher_catalog())}
    for identifier, row in frozen["units"].items():
        unit = actual.get(identifier)
        if (
            unit is None
            or unit.text != row["text"]
            or unit.text_sha256 != row["text_sha256"]
            or unit.original_sha256 != row["original_sha256"]
        ):
            raise ValueError("Original teacher unit changed: " + identifier)
    for stage in protocol["stages"]:
        if not set(protocol["source_ids"][stage]) <= set(frozen["units"]):
            raise ValueError("Protocol names an unfrozen source")
    return protocol, frozen


def display_decision(outcome, source_ids, stage):
    if not outcome.ok or outcome.finish_reason != "stop":
        return None, "incomplete_generation"
    candidate = outcome.text.strip()
    ids = re.findall(r"\[([^\[\]]+)\]", candidate)
    if not candidate or not ids or not set(ids) <= set(source_ids):
        return None, "missing_or_foreign_source_reference"
    if stage == "example" and (
        "Ejemplo hipotético:" not in candidate or "Supuestos ficticios:" not in candidate
    ):
        return None, "missing_fiction_label"
    return candidate, None


async def run(output, protocol, frozen, *, model_source=CACHED_MODEL_14B, tokenizer_fix=None):
    samples = []
    stop = asyncio.Event()
    sampler = asyncio.create_task(monitor_gpu(samples, stop))
    history = []
    turns = []
    try:
        async with cached_provider(
            output,
            source=model_source,
            quantization="nf4",
            enable_thinking=False,
            tokenizer_fix=tokenizer_fix,
        ) as provider:
            for stage in protocol["stages"]:
                question = protocol["questions"][stage]
                if history:
                    question = f"Sobre lo que acabas de mostrar («{history[-1].content[:120]}»): {question}"
                source_ids = protocol["source_ids"][stage]
                evidence = [
                    EvidenceItem(
                        fragment_id=identifier,
                        text=frozen["units"][identifier]["text"],
                        document_id=identifier,
                        document_version=1,
                    )
                    for identifier in source_ids
                ]
                request = LabGenerationRequest(
                    purpose="ejemplo" if stage == "example" else "explicacion",
                    instruction=INSTRUCTION,
                    student_input=question,
                    evidence=evidence,
                    conversation_history=history,
                    output_schema=None,
                    general_knowledge_allowed=False,
                )
                started = time.monotonic()
                try:
                    outcome = await provider.generate(request)
                    displayed, error = display_decision(outcome, source_ids, stage)
                    provider_data = outcome.model_dump()
                except Exception as exc:
                    displayed, error = None, type(exc).__name__
                    provider_data = {"error_type": type(exc).__name__, "detail": str(exc)}
                row = {
                    "stage": stage,
                    "question": question,
                    "request": request.model_dump(),
                    "provider": provider_data,
                    "transport": provider.last_exchange,
                    "displayed_text": displayed
                    or "No se obtuvo una respuesta completa. Puedes reformular la pregunta.",
                    "display_kind": "candidate" if displayed else "operational",
                    "error": error,
                    "elapsed_seconds": time.monotonic() - started,
                    "source_condition": "fixed_complete_original_units_not_retrieval",
                    "publication_allowed": False,
                }
                turns.append(row)
                save(output / "conversation.json", {"turns": turns, "complete": False})
                print(f"[TURN] {stage}: {row['display_kind']} ({row['elapsed_seconds']:.1f}s)", flush=True)
                if displayed:
                    history.extend(
                        [
                            GenerationMessage(role="user", content=question),
                            GenerationMessage(role="assistant", content=displayed),
                        ]
                    )
                elif protocol["stop_if_first_undisplayed"] or protocol["stop_if_any_later_undisplayed"]:
                    break
                if not provider.usable:
                    break
    finally:
        stop.set()
        await sampler
        save(output / "gpu-telemetry.json", samples)
        save(output / "gpu-after.json", await gpu_snapshot())
        save(
            output / "conversation.json",
            {
                "turns": turns,
                "complete": len(turns) == len(protocol["stages"])
                and all(t["display_kind"] == "candidate" for t in turns),
            },
        )


def main():
    parser = argparse.ArgumentParser(description="Frozen local generator capacity diagnosis")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, default=PROTOCOL)
    parser.add_argument("--units", type=Path, default=UNITS)
    parser.add_argument("--rubric", type=Path, default=RUBRIC)
    parser.add_argument("--model", choices=("qwen14b", "mistral24b"), default="qwen14b")
    args = parser.parse_args()
    output = args.output.resolve()
    protocol_path = args.protocol.resolve()
    units_path = args.units.resolve()
    rubric_path = args.rubric.resolve()
    if not output.is_relative_to(ROOT) or output.exists():
        parser.error("Output must be a new path inside workspace")
    if any(not p.is_relative_to(ROOT) or not p.is_file() for p in (protocol_path, units_path, rubric_path)):
        parser.error("Protocol, units and rubric must be existing workspace files")
    protocol, frozen = load_frozen(protocol_path, units_path)
    model_source, tokenizer_fix = local_model_profile(args.model)
    output.mkdir(parents=True)
    sources = [
        Path(__file__),
        protocol_path,
        units_path,
        rubric_path,
        ROOT / "src/oralia/course_dialogue/cached_transformers.py",
        ROOT / "src/oralia/course_dialogue/gpu_worker.py",
        ROOT / "src/oralia/course_dialogue/lab_request.py",
        ROOT / "src/oralia/course_dialogue/full_corpus.py",
        ROOT / "src/oralia/course_dialogue/document_evidence.py",
    ]
    with zipfile.ZipFile(output / "source-before.zip", "x", zipfile.ZIP_DEFLATED) as archive:
        for source in sources:
            archive.writestr(source.relative_to(ROOT).as_posix(), source.read_bytes())
    save(
        output / "frozen-run.json",
        {
            "source_sha256": {
                p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources
            },
            "model": str(model_source),
            "quantization": "nf4",
            "tokenizer_fix": tokenizer_fix,
            "controlled_fixed_sources": True,
            "publication_allowed": False,
        },
    )

    async def preflight():
        samples = []
        for _ in range(3):
            samples.append(await gpu_snapshot())
            await asyncio.sleep(1)
        return samples

    save(output / "gpu-before.json", asyncio.run(preflight()))
    with owned_lock(lab_root(ROOT)):
        asyncio.run(run(output, protocol, frozen, model_source=model_source, tokenizer_fix=tokenizer_fix))


if __name__ == "__main__":
    main()
