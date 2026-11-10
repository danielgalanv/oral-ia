"""Frozen 3x4 baseline/one-profile study diagnostic on one owned local worker."""

import argparse
import asyncio
import hashlib
import json
import sqlite3
import time
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from oralia.course_dialogue.cached_transformers import CACHED_MODEL_7B, cached_provider
from oralia.course_dialogue.context import plan_context
from oralia.course_dialogue.corpus import SOURCE_ROOT
from oralia.course_dialogue.document_evidence import load_authorized_units
from oralia.course_dialogue.full_corpus import DECISIONS, load_full_teacher_catalog
from oralia.course_dialogue.gpu_resource_policy import preflight
from oralia.course_dialogue.local_expansion import retrieve_with_local_expansion
from oralia.course_dialogue.rag_lab import ActivityScopeBinding, ScopeAssessment
from oralia.course_dialogue.reference_presentation import consulted_sources
from oralia.infrastructure.generation.generation_port import (
    EvidenceItem,
    GenerationConstraints,
    GenerationRequest,
)
from scripts.run_cpu_conversation_lab import serializable
from scripts.run_readable_reference_probe import RecordingWriter
from scripts.trial_course_scope import save, snapshot

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
PROPOSAL = EVIDENCE / "pedagogical-comparison-proposal-v1"
OUTPUT = EVIDENCE / "pedagogical-comparison-run-v1"


class ResourceGuard:
    def __init__(self, tolerated_misses=0):
        self.tolerated_misses = tolerated_misses
        self.misses = 0
        self.low = 0

    def stop_required(self, gpu):
        if gpu is None:
            self.misses += 1
            return self.misses > self.tolerated_misses
        self.misses = 0
        free = float(gpu.splitlines()[0].split(",")[2])
        self.low = self.low + 1 if free < 2048 else 0
        return self.low >= 2


def verify_ready(ready):
    state = ready["generation_state"]
    quant = state["quantization_config"]
    if (
        ready["effective_model_class"] != "Qwen2ForCausalLM"
        or ready["quantization"] != "nf4"
        or not quant["load_in_4bit"]
        or quant["bnb_4bit_quant_type"] != "nf4"
        or quant["bnb_4bit_compute_dtype"] != "bfloat16"
        or state["model_training"]
    ):
        raise ValueError("effective model configuration does not allow the frozen comparison")
    return {
        "allowed": True,
        "model_class": ready["effective_model_class"],
        "quantization": quant,
        "same_worker_for_24_requests": True,
        "semantic_quality_not_inferred": True,
    }


async def main():
    global PROPOSAL, OUTPUT
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposal-name", default=PROPOSAL.name)
    parser.add_argument("--output-name", default=OUTPUT.name)
    args = parser.parse_args()
    for name in (args.proposal_name, args.output_name):
        if not name or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for c in name):
            raise ValueError("local experiment directory name required")
    PROPOSAL, OUTPUT = EVIDENCE / args.proposal_name, EVIDENCE / args.output_name
    raw = (PROPOSAL / "protocol.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == (PROPOSAL / "protocol.sha256").read_text()
    clarification = (PROPOSAL / "example-clarification.json").read_bytes()
    assert (
        hashlib.sha256(clarification).hexdigest() == (PROPOSAL / "example-clarification.sha256").read_text()
    )
    protocol = json.loads(raw)
    OUTPUT.mkdir(exist_ok=False)
    save(OUTPUT / "protocol.json", protocol)
    save(OUTPUT / "example-clarification.json", json.loads(clarification))
    (OUTPUT / "executed-runner.py").write_bytes(Path(__file__).read_bytes())
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
        "full",
        hashlib.sha256(DECISIONS.read_bytes()).hexdigest(),
    )
    resources, records, frames = [], [], []
    ledger = {
        "requests_reserved": 0,
        "tokens_reserved": 0,
        "warmup_confirmed": 0,
        "requests_maximum": 24,
        "generate_maximum": 25,
        "new_tokens_maximum": 12289,
    }
    finished, unsafe = asyncio.Event(), asyncio.Event()
    live = {"provider": None}
    ids = [f"{case}-{profile}-{turn}" for case, profile in protocol["order"] for turn in range(1, 5)]

    async def sample(stage):
        value = {**await snapshot(), "stage": stage}
        resources.append(value)
        save(OUTPUT / "resources.json", resources)
        return value

    async def monitor():
        guard = ResourceGuard(protocol.get("telemetry_transient_misses_tolerated", 0))
        while not finished.is_set():
            try:
                value = await sample("during")
                if guard.stop_required(value["gpu"]) or (OUTPUT / "STOP").exists():
                    unsafe.set()
            except Exception as error:
                resources.append({"stage": "during", "error": type(error).__name__})
                save(OUTPUT / "resources.json", resources)
                if guard.stop_required(None):
                    unsafe.set()
            if unsafe.is_set() and live["provider"] is not None:
                live["provider"].terminate_owned()
                return
            try:
                await asyncio.wait_for(finished.wait(), timeout=1)
            except TimeoutError:
                pass

    task = None
    started = time.monotonic()
    try:
        binding.revalidate(db)
        pages, units = load_authorized_units(SOURCE_ROOT, catalog_loader=load_full_teacher_catalog)
        for _ in range(5):
            await sample("before")
            await asyncio.sleep(1)
        decision = preflight(resources)
        save(OUTPUT / "preflight.json", decision)
        if not decision["ready"]:
            print("Preflight refused; no model loaded and no comparison responses", flush=True)
            return
        task = asyncio.create_task(monitor())
        async with asyncio.timeout(protocol["total_wall_deadline_seconds"]):
            async with cached_provider(OUTPUT, source=CACHED_MODEL_7B, quantization="nf4") as provider:
                live["provider"] = provider
                ready = json.loads((OUTPUT / "worker.json").read_text())
                save(OUTPUT / "effective-configuration-check.json", verify_ready(ready))
                print(
                    (
                        "Effective Qwen2.5-7B NF4/BF16 configuration confirmed; starting "
                        "bounded 24-response comparison"
                    ),
                    flush=True,
                )
                ledger["warmup_confirmed"] = 1
                save(OUTPUT / "budget.json", ledger)
                provider.process.stdin = RecordingWriter(
                    provider.process.stdin, frames, OUTPUT / "sent-frames.json"
                )
                cases = {case["id"]: case for case in protocol["cases"]}
                for case_id, profile in protocol["order"]:
                    history = []
                    case = cases[case_id]
                    for index, turn in enumerate(case["turns"], 1):
                        if (
                            unsafe.is_set()
                            or time.monotonic() - started > protocol["total_wall_deadline_seconds"]
                        ):
                            raise RuntimeError("resource/privacy or total wall limit stop")
                        key = f"{case_id}-{profile}-{index}"
                        policy = binding.revalidate(db)
                        binding.assert_catalog(pages, units, policy)
                        scope = ScopeAssessment(
                            "in_scope",
                            authority_ref=binding.policy_sha256,
                            block_id=turn.get("block", case["block"]),
                            reason="frozen control metadata, not automatic scope validation",
                        )
                        binding.assert_decision(scope, policy)
                        plan = plan_context(turn["question"], history)
                        retrieval_started = time.monotonic()
                        attempts = retrieve_with_local_expansion(
                            units,
                            pages,
                            plan.academic_query,
                            displayed_history=tuple(r["displayed_text"] for r in history),
                            focus_change=turn["act"] == "topic_switch",
                            insufficient=True,
                            lexical_profile="bilingual-v1",
                        )
                        retrieval_ms = (time.monotonic() - retrieval_started) * 1000
                        if not attempts.delivered.units:
                            raise ValueError("no retrieved units; no generation or fabricated followup")
                        context = []
                        for shown in history:
                            context.extend(
                                [
                                    {"role": "user", "content": shown["input"]},
                                    {"role": "assistant", "content": shown["displayed_text"]},
                                ]
                            )
                        request = GenerationRequest(
                            purpose="explicacion",
                            instruction=protocol["profiles"][profile],
                            student_input=turn["question"],
                            conversation_history=context,
                            evidence=[
                                EvidenceItem(
                                    fragment_id=u.id,
                                    document_id=u.document_id,
                                    document_version=u.version,
                                    text=f'<pasaje id="{u.id}">\n{u.text}\n</pasaje>',
                                )
                                for u in attempts.delivered.units
                            ],
                            general_knowledge_allowed=False,
                            constraints=GenerationConstraints(max_tokens=512, deadline_ms=30000),
                        )
                        record = {
                            "id": key,
                            "case": case_id,
                            "profile": profile,
                            "turn": index,
                            "question": turn["question"],
                            "act": turn["act"],
                            "references": turn["references"],
                            "resolved_query": plan.academic_query,
                            "retrieval_ms": retrieval_ms,
                            "evidence_attempts": serializable(attempts),
                            "generation_request": request.model_dump(mode="json"),
                            "displayed_text": None,
                            "semantic_support": "unverified",
                            "publication_allowed": False,
                        }
                        records.append(record)
                        ledger["requests_reserved"] += 1
                        ledger["tokens_reserved"] += 512
                        assert ledger["requests_reserved"] <= 24 and ledger["tokens_reserved"] <= 12288
                        save(OUTPUT / "budget.json", ledger)
                        save(OUTPUT / "records.json", records)
                        policy = binding.revalidate(db)
                        binding.assert_catalog(pages, units, policy)
                        record["generation_started_monotonic"] = time.monotonic()
                        outcome = await provider.generate(request)
                        record["generation_finished_monotonic"] = time.monotonic()
                        record.update(
                            outcome=outcome.model_dump(mode="json"), exchange=provider.last_exchange
                        )
                        save(OUTPUT / "records.json", records)
                        policy = binding.revalidate(db)
                        binding.assert_catalog(pages, units, policy)
                        binding.assert_decision(scope, policy)
                        if not outcome.ok or outcome.finish_reason != "stop" or not outcome.text.strip():
                            raise ValueError(
                                "incomplete/empty/protocol response; unshown candidate cannot enter history"
                            )
                        state = json.loads(provider.last_exchange["raw_worker_response"])["generation_state"]
                        assert state["effective_config_after_explicit_overrides"]["do_sample"] is False
                        assert state["effective_config_after_explicit_overrides"]["max_new_tokens"] == 512
                        assert state["finite_prefix_constraint"] is False
                        sources = consulted_sources(attempts.delivered.units)
                        shown = outcome.text + "\n\n" + sources["display_text"]
                        print(f"\n[UNVERIFIED TECHNICAL PREVIEW {key}]\n{shown}\n", flush=True)
                        record.update(displayed_text=shown, source_presentation=sources)
                        history.append(
                            {
                                "input": turn["question"],
                                "displayed_text": shown,
                                "displayed_kind": "laboratory_preview",
                                "display_kind": "candidate",
                                "academic_topic": plan.academic_query,
                            }
                        )
                        save(OUTPUT / "records.json", records)
                        save(OUTPUT / f"history-{case_id}-{profile}.json", history)
    except Exception as error:
        save(OUTPUT / "failure.json", {"type": type(error).__name__, "detail": str(error)})
        raise
    finally:
        finished.set()
        if task is not None:
            await task
        await sample("after")
        save(OUTPUT / "unexecuted.json", [key for key in ids if not any(r["id"] == key for r in records)])
        db.close()
        engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
