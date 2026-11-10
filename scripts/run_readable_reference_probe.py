"""One new bounded RAG diagnostic, with host-owned readable consulted sources."""

import argparse
import asyncio
import hashlib
import json
import sqlite3
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
from scripts.trial_course_scope import save, snapshot

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
PROPOSAL = EVIDENCE / "readable-reference-proposal-v1"
OUTPUT = EVIDENCE / "readable-reference-run-2026-10-27"


class RecordingWriter:
    """Capture actual frames; opt-in audit metadata does not alter model messages."""

    def __init__(self, original, frames, output):
        self.original, self.frames, self.output = original, frames, output

    def write(self, raw):
        frame = json.loads(raw)
        if "messages" in frame:
            frame["audit_config"] = True
            self.frames.append(frame)
            save(self.output, self.frames)
            raw = (json.dumps(frame, ensure_ascii=False) + "\n").encode()
        self.original.write(raw)

    async def drain(self):
        await self.original.drain()


async def main():
    global OUTPUT
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-name", default=OUTPUT.name)
    name = parser.parse_args().output_name
    if not name or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for c in name):
        raise ValueError("new local output name required")
    OUTPUT = EVIDENCE / name
    raw = (PROPOSAL / "protocol.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == (PROPOSAL / "protocol.sha256").read_text()
    protocol = json.loads(raw)
    OUTPUT.mkdir(exist_ok=False)
    save(OUTPUT / "protocol.json", protocol)
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
    records, history, resources, frames = [], [], [], []
    budget = {
        "requests_reserved": 0,
        "tokens_reserved": 0,
        "warmup_confirmed": 0,
        "requests_maximum": 3,
        "generate_invocations_maximum": 4,
        "new_tokens_maximum": 1537,
    }
    done = asyncio.Event()

    async def sample(stage):
        resources.append({**await snapshot(), "stage": stage})
        save(OUTPUT / "resources.json", resources)

    async def monitor():
        while not done.is_set():
            try:
                await sample("during")
            except Exception as error:
                resources.append({"stage": "during", "error": type(error).__name__})
            try:
                await asyncio.wait_for(done.wait(), timeout=1)
            except TimeoutError:
                pass

    task = None
    try:
        binding.revalidate(db)
        pages, units = load_authorized_units(SOURCE_ROOT, catalog_loader=load_full_teacher_catalog)
        for _ in range(5):
            await sample("before")
            await asyncio.sleep(1)
        decision = preflight(resources)
        save(OUTPUT / "preflight.json", decision)
        if not decision["ready"]:
            return
        task = asyncio.create_task(monitor())
        async with cached_provider(OUTPUT, source=CACHED_MODEL_7B, quantization="nf4") as provider:
            provider.process.stdin = RecordingWriter(
                provider.process.stdin, frames, OUTPUT / "sent-frames.json"
            )
            budget["warmup_confirmed"] = 1
            save(OUTPUT / "budget.json", budget)
            for case in protocol["cases"]:
                policy = binding.revalidate(db)
                binding.assert_catalog(pages, units, policy)
                scope = ScopeAssessment(
                    "in_scope",
                    authority_ref=binding.policy_sha256,
                    block_id="ingenieria_requisitos",
                    reason="prepared control metadata, not classifier validation",
                )
                binding.assert_decision(scope, policy)
                plan = plan_context(case["question"], history)
                attempts = retrieve_with_local_expansion(
                    units,
                    pages,
                    plan.academic_query,
                    displayed_history=tuple(r["displayed_text"] for r in history),
                    insufficient=True,
                    lexical_profile="bilingual-v1",
                )
                if not attempts.delivered.units:
                    raise ValueError("no retrieved evidence")
                context = []
                for row in history:
                    context.extend(
                        [
                            {"role": "user", "content": row["input"]},
                            {"role": "assistant", "content": row["displayed_text"]},
                        ]
                    )
                request = GenerationRequest(
                    purpose="explicacion",
                    instruction=protocol["instruction"],
                    student_input=case["question"],
                    conversation_history=context,
                    general_knowledge_allowed=False,
                    constraints=GenerationConstraints(max_tokens=512, deadline_ms=30000),
                    evidence=[
                        EvidenceItem(
                            fragment_id=u.id,
                            document_id=u.document_id,
                            document_version=u.version,
                            text=f'<pasaje id="{u.id}">\n{u.text}\n</pasaje>',
                        )
                        for u in attempts.delivered.units
                    ],
                )
                record = {
                    "id": case["id"],
                    "question": case["question"],
                    "resolved_query": plan.academic_query,
                    "scope_control": serializable(scope),
                    "evidence_attempts": serializable(attempts),
                    "generation_request": request.model_dump(mode="json"),
                    "displayed_text": None,
                    "semantic_support": "unverified",
                    "publication_allowed": False,
                }
                records.append(record)
                budget["requests_reserved"] += 1
                budget["tokens_reserved"] += 512
                assert budget["requests_reserved"] <= 3 and budget["tokens_reserved"] <= 1536
                save(OUTPUT / "budget.json", budget)
                save(OUTPUT / "records.json", records)
                outcome = await provider.generate(request)
                record.update(outcome=outcome.model_dump(mode="json"), exchange=provider.last_exchange)
                save(OUTPUT / "records.json", records)
                policy = binding.revalidate(db)
                binding.assert_catalog(pages, units, policy)
                binding.assert_decision(scope, policy)
                if not outcome.ok or outcome.finish_reason != "stop":
                    raise ValueError("incomplete generation; no followup on unshown output")
                sources = consulted_sources(attempts.delivered.units)
                shown = outcome.text + "\n\n" + sources["display_text"]
                print(f"\n[UNVERIFIED TECHNICAL PREVIEW {case['id']}]\n{shown}\n", flush=True)
                record.update(displayed_text=shown, source_presentation=sources)
                history.append(
                    {
                        "input": case["question"],
                        "displayed_text": shown,
                        "displayed_kind": "laboratory_preview",
                        "display_kind": "candidate",
                        "academic_topic": plan.academic_query,
                    }
                )
                save(OUTPUT / "records.json", records)
                save(OUTPUT / "shown-history.json", history)
    except Exception as error:
        save(OUTPUT / "failure.json", {"type": type(error).__name__, "detail": str(error)})
        raise
    finally:
        done.set()
        if task is not None:
            await task
        await sample("after")
        save(
            OUTPUT / "unexecuted.json",
            [c["id"] for c in protocol["cases"] if not any(r["id"] == c["id"] for r in records)],
        )
        db.close()
        engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
