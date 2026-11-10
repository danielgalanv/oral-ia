"""One bounded RAG candidate conversation; no simulated semantic verdicts."""

import asyncio
import hashlib
import json
import re
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
from oralia.infrastructure.generation.generation_port import (
    EvidenceItem,
    GenerationConstraints,
    GenerationRequest,
)
from scripts.run_cpu_conversation_lab import serializable
from scripts.trial_course_scope import save, snapshot

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
PACKET = EVIDENCE / "study-review-preparation-v1"
OUTPUT = EVIDENCE / "study-review-run-2026-10-27"


def persist_citation_check(record, expected_ids, records, output):
    cited = set(re.findall(r"\[([^\[\]]+)\]", record["outcome"]["text"]))
    record["citation_check"] = {
        "missing": not cited,
        "foreign": sorted(cited - expected_ids),
        "semantic_support": "unverified",
    }
    save(output, records)
    if not cited or cited - expected_ids:
        raise ValueError("invalid citations; candidate retained but not shown")


async def main():
    OUTPUT.mkdir(exist_ok=False)
    raw = (PACKET / "review.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == (PACKET / "review.sha256").read_text()
    packet = json.loads(raw)
    save(
        OUTPUT / "protocol.json",
        {
            "review_sha256": hashlib.sha256(raw).hexdigest(),
            "diagnostic_requests_maximum": 4,
            "warmup_maximum": 1,
            "model_generate_maximum": 5,
            "new_tokens_maximum": 2049,
            "per_request_tokens": 512,
            "per_request_deadline_ms": 30000,
            "load_deadline_seconds": 90,
            "retries": 0,
            "prompt_or_oracle_adaptation": False,
            "stop": "first_incomplete_or_invalid_citation_or_protocol_or_source_failure",
            "scope": "prepared_question_metadata_bound_to_real_policy_not_semantic_classifier_validation",
            "retrieval": "bilingual-v1_one_planned_expansion_not_a_sufficiency_verdict",
            "pre_and_post_semantic_review": "unavailable_not_simulated_as_supported",
            "display": "unverified_technical_candidate_console_only_never_participant",
            "publication_allowed": False,
            "reserve_used": False,
            "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        },
    )
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
    resources, records, history = [], [], []
    budget = {
        "diagnostic_requests_reserved": 0,
        "tokens_reserved": 0,
        "warmup_maximum": 1,
        "warmup_confirmed": 0,
    }

    async def sample(stage):
        resources.append({**await snapshot(), "stage": stage})
        save(OUTPUT / "resources.json", resources)

    done = asyncio.Event()

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
            budget["warmup_confirmed"] = 1
            save(OUTPUT / "budget.json", budget)
            for case in packet["questions"]:
                policy = binding.revalidate(db)
                binding.assert_catalog(pages, units, policy)
                scope = ScopeAssessment(
                    "in_scope",
                    authority_ref=binding.policy_sha256,
                    block_id=(
                        "verificacion_validacion_pruebas" if case["id"] == "ST04" else "ingenieria_requisitos"
                    ),
                    reason="prepared control question, not an automatic scope decision",
                )
                binding.assert_decision(scope, policy)
                plan = plan_context(case["question"], history)
                attempts = retrieve_with_local_expansion(
                    units,
                    pages,
                    plan.academic_query,
                    displayed_history=tuple(r["displayed_text"] for r in history),
                    focus_change=case["act"] == "topic_switch",
                    insufficient=True,
                    lexical_profile="bilingual-v1",
                )
                if not attempts.delivered.units:
                    raise ValueError("no retrieved source units; no generation")
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
                    instruction=(
                        "Diagnóstico de estudio local, sin publicación. "
                        "Responde en español a la pregunta actual "
                        "usando solo los pasajes recuperados. El historial resuelve referentes, "
                        "no es fuente académica. "
                        "No añadas hechos de memoria. Explica o reformula según la petición; "
                        "los ejemplos deben ser "
                        "hipotéticos, con datos inventados identificados y principio "
                        "respaldado en los pasajes. "
                        "Expresa límites si falta apoyo. Cita cada afirmación documental con el id exacto "
                        "de <pasaje id=...> entre corchetes [id]. "
                        "No sustituyas la explicación por una pregunta."
                    ),
                    student_input=case["question"],
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
                    "id": case["id"],
                    "question": case["question"],
                    "resolved_query": plan.academic_query,
                    "scope_control": serializable(scope),
                    "evidence_attempts": serializable(attempts),
                    "generation_request": request.model_dump(mode="json"),
                    "semantic_support": "unverified",
                    "publication_allowed": False,
                    "displayed_text": None,
                }
                records.append(record)
                budget["diagnostic_requests_reserved"] += 1
                budget["tokens_reserved"] += 512
                save(OUTPUT / "budget.json", budget)
                save(OUTPUT / "records.json", records)
                binding.revalidate(db)
                binding.assert_catalog(pages, units, policy)
                outcome = await provider.generate(request)
                record.update(outcome=outcome.model_dump(mode="json"), exchange=provider.last_exchange)
                save(OUTPUT / "records.json", records)
                binding.revalidate(db)
                binding.assert_catalog(pages, units, policy)
                if not outcome.ok or outcome.finish_reason != "stop":
                    raise ValueError("incomplete generation; remaining turns not executed")
                expected_ids = {u.id for u in attempts.delivered.units}
                persist_citation_check(record, expected_ids, records, OUTPUT / "records.json")
                print(f"\n[UNVERIFIED LAB CANDIDATE {case['id']}]\n{outcome.text}\n", flush=True)
                record["displayed_text"] = outcome.text
                history.append(
                    {
                        "input": case["question"],
                        "displayed_text": outcome.text,
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
            [c["id"] for c in packet["questions"] if not any(r["id"] == c["id"] for r in records)],
        )
        db.close()
        engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
