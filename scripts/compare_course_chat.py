"""Frozen, bounded A/B/C laboratory comparison; never a participant endpoint."""

import argparse
import asyncio
import hashlib
import json
import re
import time
import zipfile
from pathlib import Path

from oralia.course_dialogue.__main__ import inspect_drafts, lab_root
from oralia.course_dialogue.cached_transformers import CACHED_MODEL_QWEN3_8B, cached_provider
from oralia.course_dialogue.corpus import SemanticCatalog, load_catalog
from oralia.course_dialogue.document_evidence import load_authorized_units
from oralia.course_dialogue.draft_dialogue import DraftCurriculum
from oralia.course_dialogue.full_corpus import load_full_teacher_catalog
from oralia.course_dialogue.runtime import propose
from oralia.course_study.__main__ import owned_lock

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = ROOT / "specs/012-conversational-course-study/evidence/chat-comparison-protocol.json"


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


async def gpu_snapshot():
    result = {"monotonic": time.monotonic()}
    for label, arguments in (
        (
            "gpu",
            (
                "--query-gpu=timestamp,utilization.gpu,memory.used,memory.free,power.draw,clocks.sm,temperature.gpu",
                "--format=csv,noheader,nounits",
            ),
        ),
        ("compute_apps", ("--query-compute-apps=pid,used_gpu_memory", "--format=csv,noheader,nounits")),
    ):
        try:
            process = await asyncio.create_subprocess_exec(
                "nvidia-smi",
                *arguments,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.DEVNULL,
            )
            output, _ = await asyncio.wait_for(process.communicate(), timeout=5)
            result[label] = output.decode(errors="replace").strip() if process.returncode == 0 else None
        except (OSError, TimeoutError):
            result[label] = None
    return result


async def monitor_gpu(samples, stop):
    while not stop.is_set():
        samples.append(await gpu_snapshot())
        try:
            await asyncio.wait_for(stop.wait(), timeout=2)
        except TimeoutError:
            pass


def next_input(case, previous, stage):
    """Continuation depends on actual displayed text, never an expected answer."""
    if not previous:
        return "No recibí una respuesta completa. " + case[stage]
    questions = re.findall(r"¿[^?]{5,160}\?", previous)
    referent = questions[-1] if questions else previous[:120]
    return f"Sobre lo que acabas de mostrar («{referent}»): {case[stage]}"


def observe(row):
    text = row.get("displayed_text") or ""
    refs = row.get("retrieved_source_ids", [])
    parsed = row.get("parsed_candidate") or {}
    proposed_refs = parsed.get("source_ids", [])
    if "segments" in parsed:
        proposed_refs = [s["source_id"] for s in parsed["segments"]]
    return {
        "structure_complete": bool(text) and not row.get("error"),
        "provenance_declared": bool(proposed_refs),
        "provenance_in_retrieval": bool(proposed_refs) and set(proposed_refs) <= set(refs),
        "content_semantics": "pending_independent_review",
        "relevance_and_coverage": "pending_independent_review",
        "continuity": "pending_independent_review",
        "publication_authorized": False,
    }


async def run_bc(
    case,
    variant,
    catalog,
    provider,
    document_units=None,
    compact_output=False,
    conversational_output=False,
    plain_text_lab=False,
):
    turns = []
    for stage in case.get("stages", ("first", "followup", "switch")):
        previous = turns[-1].get("displayed_text") if turns else None
        question = case[stage] if stage == "first" else next_input(case, previous, stage)
        captured = {}
        started = time.perf_counter()
        started_monotonic = time.monotonic()
        try:
            row = await propose(
                catalog,
                question,
                turns,
                provider,
                variant=variant,
                inference_deadline_ms=30000,
                trace=captured.update,
                document_units=document_units,
                compact_output=compact_output,
                conversational_output=conversational_output,
                plain_text_lab=plain_text_lab,
                structured=not plain_text_lab,
            )
        except Exception as exc:
            row = {
                "input": question,
                "displayed_text": "No se obtuvo una respuesta completa. Puedes reformular la pregunta.",
                "display_kind": "operational",
                "raw_candidate": None,
                "error": type(exc).__name__,
                "diagnostic": str(exc),
                "publication_allowed": False,
            }
        row.update(
            stage=stage,
            request_snapshot=captured,
            elapsed_seconds=time.perf_counter() - started,
            started_monotonic=started_monotonic,
            ended_monotonic=time.monotonic(),
        )
        row["observation"] = observe(row)
        turns.append(row)
        print(
            case["id"],
            variant,
            stage,
            row.get("error", "candidate"),
            round(row["elapsed_seconds"], 2),
            flush=True,
        )
        if (
            len(turns) == 1
            and case.get("stop_if_first_undisplayed")
            and row.get("display_kind") != "candidate"
        ):
            for skipped in case.get("stages", ("first", "followup", "switch"))[1:]:
                turns.append(
                    {"stage": skipped, "executed": False, "reason": "first_academic_answer_undisplayed"}
                )
            break
        if not provider.usable:
            for skipped in case.get("stages", ("first", "followup", "switch"))[len(turns) :]:
                turns.append({"stage": skipped, "executed": False, "reason": "owned_worker_unavailable"})
            break
    return turns


async def run_a(case, curriculum, provider):
    events = []
    writes = []
    answers = []
    stage = 0
    inputs = []

    def on_event(event):
        events.append(event)
        if event.get("event") == "actual_preview":
            answers.append(event["preview"]["candidate_text"])

    def read(_prompt):
        nonlocal stage
        names = case.get("stages", ("first", "followup", "switch"))
        if stage >= len(names):
            return "/salir"
        name = names[stage]
        value = case[name] if stage == 0 else next_input(case, answers[-1] if answers else None, name)
        stage += 1
        inputs.append(value)
        return value

    await inspect_drafts(
        curriculum, provider, read=read, write=writes.append, semantic_version=7, on_event=on_event
    )
    turns = []
    actual_by_turn = []
    for event in events:
        if event.get("event") == "input" and event.get("text") != "/salir":
            actual_by_turn.append({})
        elif event.get("event") == "actual_preview" and actual_by_turn:
            actual_by_turn[-1] = event["preview"]
    names = case.get("stages", ("first", "followup", "switch"))
    for index, question in enumerate(inputs):
        actual = actual_by_turn[index] if index < len(actual_by_turn) else {}
        row = {
            "input": question,
            "stage": names[index],
            "displayed_text": actual.get("candidate_text"),
            "raw_candidate": None,
            "retrieved_source_ids": [r["source_id"] for r in actual.get("source_refs", [])],
            "parsed_candidate": {"source_ids": [r["source_id"] for r in actual.get("source_refs", [])]},
            "publication_allowed": False,
            "actual_preview": actual,
        }
        row["observation"] = observe(row)
        turns.append(row)
    return {"turns": turns, "events": events, "console": writes}


def prepare_catalog(whole_units=False, full_teacher_pdfs=False):
    pages = load_full_teacher_catalog() if full_teacher_pdfs else load_catalog()
    if whole_units:
        authorized_pages, document_units = load_authorized_units(
            catalog_loader=load_full_teacher_catalog if full_teacher_pdfs else load_catalog
        )
        if [(p["id"], p["text_sha256"]) for p in pages] != [
            (p["id"], p["text_sha256"]) for p in authorized_pages
        ]:
            raise ValueError("whole-unit extraction changed the authorized catalog")
        # Table units must be checked against the extracted boxes in this same catalog.
        pages = authorized_pages
    else:
        document_units = None
    catalog = pages if whole_units else SemanticCatalog(pages)
    return pages, catalog, document_units


async def run(
    protocol,
    output,
    partition,
    repetitions,
    whole_units=False,
    bc_only=False,
    full_teacher_pdfs=False,
    compact_output=False,
    conversational_output=False,
    plain_text_lab=False,
):
    pages, catalog, document_units = prepare_catalog(whole_units, full_teacher_pdfs)
    curriculum = DraftCurriculum(catalog=pages)
    samples = []
    stop = asyncio.Event()
    sampler = asyncio.create_task(monitor_gpu(samples, stop))
    try:
        async with cached_provider(
            output, source=CACHED_MODEL_QWEN3_8B, quantization="nf4", enable_thinking=False
        ) as provider:
            for case in protocol[partition]:
                for repetition in range(repetitions):
                    orders = (
                        ("A", "documental", "pedagogica"),
                        ("documental", "pedagogica", "A"),
                        ("pedagogica", "A", "documental"),
                    )
                    variants = tuple(v for v in orders[repetition % len(orders)] if not bc_only or v != "A")
                    for variant in variants:
                        started = time.perf_counter()
                        started_monotonic = time.monotonic()
                        result = (
                            (await run_a(case, curriculum, provider))
                            if variant == "A"
                            else {
                                "turns": await run_bc(
                                    case,
                                    variant,
                                    catalog,
                                    provider,
                                    document_units,
                                    compact_output,
                                    conversational_output,
                                    plain_text_lab,
                                )
                            }
                        )
                        result.update(
                            case=case["id"],
                            variant=variant,
                            repetition=repetition,
                            actual_local_model=True,
                            participant_publication=False,
                            human_review="pending",
                            elapsed_seconds=time.perf_counter() - started,
                            started_monotonic=started_monotonic,
                            ended_monotonic=time.monotonic(),
                        )
                        save(output / f"{case['id']}-{repetition}-{variant}.json", result)
                        if not provider.usable:
                            return
    finally:
        stop.set()
        await sampler
        save(output / "gpu-telemetry.json", samples)
        save(output / "gpu-after.json", await gpu_snapshot())


def main():
    parser = argparse.ArgumentParser(description="Frozen candidate-only chat comparison")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--partition", choices=("development", "reserved"), default="development")
    parser.add_argument("--repetitions", type=int, choices=(1, 3), default=1)
    parser.add_argument(
        "--whole-units", action="store_true", help="Opt-in B/C lab context from authorized complete units"
    )
    parser.add_argument("--bc-only", action="store_true", help="Diagnostic B/C only; skip A")
    parser.add_argument(
        "--full-teacher-pdfs", action="store_true", help="Use reviewed 139-page text lab catalog"
    )
    parser.add_argument("--compact-output", action="store_true", help="Opt-in bounded B/C JSON response")
    parser.add_argument("--conversational-output", action="store_true", help="Opt-in unified B/C body")
    parser.add_argument(
        "--plain-text-lab", action="store_true", help="Opt-in cited text with 768/50 lab bounds"
    )
    args = parser.parse_args()
    if args.full_teacher_pdfs and not args.whole_units:
        parser.error("--full-teacher-pdfs requires --whole-units")
    if sum((args.compact_output, args.conversational_output, args.plain_text_lab)) > 1:
        parser.error("Select one B/C output contract")
    if args.plain_text_lab and (not args.bc_only or not args.whole_units):
        parser.error("--plain-text-lab requires --bc-only and --whole-units")
    output = args.output.resolve()
    protocol_path = args.protocol.resolve()
    if not output.is_relative_to(ROOT) or output.exists():
        parser.error("Output must be a new path inside the workspace")
    if not protocol_path.is_relative_to(ROOT):
        parser.error("Protocol must be inside the workspace")
    protocol_bytes = protocol_path.read_bytes()
    protocol = json.loads(protocol_bytes)
    if args.partition not in protocol or not isinstance(protocol[args.partition], list):
        parser.error("Partition is not a frozen case list")
    output.mkdir(parents=True)
    before = []

    async def preflight():
        for _ in range(3):
            before.append(await gpu_snapshot())
            await asyncio.sleep(1)

    asyncio.run(preflight())
    save(output / "gpu-before.json", before)
    source_names = [
        "scripts/compare_course_chat.py",
        "src/oralia/course_dialogue/__main__.py",
        "src/oralia/course_dialogue/cached_transformers.py",
        "src/oralia/course_dialogue/gpu_worker.py",
        "src/oralia/course_dialogue/runtime.py",
        "src/oralia/course_dialogue/context.py",
        "src/oralia/course_dialogue/corpus.py",
        "src/oralia/course_dialogue/document_evidence.py",
        "src/oralia/course_dialogue/full_corpus.py",
        "src/oralia/course_dialogue/lab_request.py",
        "specs/012-conversational-course-study/evidence/teacher-pdf-decisions.json",
        "specs/012-conversational-course-study/evidence/teacher-pdf-inventory.json",
        "src/oralia/course_dialogue/contracts.py",
        "src/oralia/course_dialogue/draft_dialogue.py",
        "src/oralia/course_dialogue/semantic_planner.py",
        "src/oralia/domain/dialogue/interpretation.py",
        "src/oralia/infrastructure/generation/generation_port.py",
        "src/oralia/infrastructure/generation/ollama_adapter.py",
        "src/oralia/course_study/__main__.py",
    ]
    sources = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in source_names}
    with zipfile.ZipFile(output / "source-before.zip", "x", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("protocol.json", protocol_bytes)
        for name in source_names:
            archive.writestr(name, (ROOT / name).read_bytes())
    save(
        output / "frozen-run.json",
        {
            "protocol_sha256": hashlib.sha256(protocol_bytes).hexdigest(),
            "source_sha256": sources,
            "model": str(CACHED_MODEL_QWEN3_8B),
            "quantization": "nf4",
            "enable_thinking": False,
            "partition": args.partition,
            "repetitions": args.repetitions,
            "final_g2": False,
            "whole_units": args.whole_units,
            "bc_only": args.bc_only,
            "full_teacher_pdfs": args.full_teacher_pdfs,
            "compact_output": args.compact_output,
            "conversational_output": args.conversational_output,
            "plain_text_lab": args.plain_text_lab,
        },
    )
    root = lab_root(ROOT)
    with owned_lock(root):
        asyncio.run(
            run(
                protocol,
                output,
                args.partition,
                args.repetitions,
                args.whole_units,
                args.bc_only,
                args.full_teacher_pdfs,
                args.compact_output,
                args.conversational_output,
                args.plain_text_lab,
            )
        )


if __name__ == "__main__":
    main()
