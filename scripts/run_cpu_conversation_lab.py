"""Executable CPU wiring demonstration: real read-only policy/PDFs, simulated ports.

No model imports, weights, embeddings, network, participant or publication.
"""

import argparse
import asyncio
import hashlib
import json
import sqlite3
from dataclasses import asdict, is_dataclass
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from oralia.course_dialogue.conversation_lab import LaboratoryConversation, PostReview
from oralia.course_dialogue.corpus import SOURCE_ROOT
from oralia.course_dialogue.document_evidence import load_authorized_units
from oralia.course_dialogue.full_corpus import DECISIONS, load_full_teacher_catalog
from oralia.course_dialogue.rag_lab import ActivityScopeBinding, ScopeAssessment, SufficiencyAssessment
from oralia.infrastructure.generation.generation_port import GenerationOutcome

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
POLICY = EVIDENCE / "course-scope-policy-v1.json"
PACKET = EVIDENCE / "cpu-rag-progress-v1"
DATABASE = ROOT / ".oralia-course-study/course.db"


def serializable(value):
    if is_dataclass(value):
        return serializable(asdict(value))
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if isinstance(value, dict):
        return {key: serializable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [serializable(item) for item in value]
    return value


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="conversation")
    name = parser.parse_args().name
    if not name or any(character not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for character in name):
        raise ValueError("local evidence name required")
    output = PACKET / f"{name}.json"
    if output.exists():
        raise ValueError("preserve prior demonstration")
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    engine = create_engine(
        "sqlite://", creator=lambda: sqlite3.connect("file:" + DATABASE.as_posix() + "?mode=ro", uri=True)
    )
    db = Session(engine)
    binding = ActivityScopeBinding(
        engine,
        policy["activity_id"],
        policy["activity_version"],
        policy["course_id"],
        POLICY,
        hashlib.sha256(POLICY.read_bytes()).hexdigest(),
        SOURCE_ROOT,
        "full",
        hashlib.sha256(DECISIONS.read_bytes()).hexdigest(),
    )
    scenarios = [
        (
            "¿Cómo compruebo que un requisito es realizable con la tecnología y el presupuesto disponibles?",
            ["sufficient"],
            "supported",
        ),
        ("¿Por qué?", ["insufficient", "sufficient"], "unknown"),
        ("¿Y eso?", ["sufficient"], "supported"),
        ("¿Cómo valido las necesidades reales de usuarios?", ["insufficient", "insufficient"], "unknown"),
        ("¿Son compatibles estos requisitos?", ["conflict"], "unknown"),
        ("Cambiemos de tema: pruebas de validación y pruebas de defectos", ["sufficient"], "supported"),
    ]
    current = {}

    async def scope(*_):
        return ScopeAssessment(
            "in_scope",
            authority_ref=binding.policy_sha256,
            block_id="verificacion_validacion_pruebas" if current["testing"] else "ingenieria_requisitos",
            reason="SIMULADO: bloque inyectado, no clasificación semántica medida",
        )

    async def assess(*_):
        return SufficiencyAssessment(
            next(current["statuses"]), "simulated-pre-review", "SIMULADO: prueba de cableado"
        )

    async def review(*_):
        return PostReview(
            current["review"], "simulated-post-review", "SIMULADO: no evaluación semántica", simulated=True
        )

    class SimulatedProvider:
        async def generate(self, request):
            return GenerationOutcome(
                ok=True,
                adapter="deterministic",
                finish_reason="stop",
                text=(
                    "SALIDA SIMULADA de cableado, sin explicación académica. "
                    f"[{request.evidence[0].fragment_id}]"
                ),
            )

    try:
        binding.revalidate(db)
        pages, units = load_authorized_units(SOURCE_ROOT, catalog_loader=load_full_teacher_catalog)
        lab = LaboratoryConversation(
            pages,
            units,
            binding=binding,
            db=db,
            scope_assessor=scope,
            assessor=assess,
            provider=SimulatedProvider(),
            post_reviewer=review,
            interfaces_are_simulated=True,
        )
        for index, (question, statuses, verdict) in enumerate(scenarios):
            current.update(statuses=iter(statuses), review=verdict, testing=index == 5)
            row = await lab.turn(question)
            shown = lab.prepare_display(row["turn_id"])
            print(f"Turno {row['turn_id']}: {shown}")
            lab.acknowledge_display(row["turn_id"])
        result = {
            "real_policy_sha256": binding.policy_sha256,
            "page_decisions_sha256": binding.decisions_sha256,
            "read_only_database": True,
            "original_sources_revalidated": True,
            "interfaces_are_simulated": True,
            "model_or_embedding_loads": 0,
            "inference_calls": 0,
            "independent_semantics": False,
            "publication_allowed": False,
            "catalog_pages": len(pages),
            "evidence_units": len(units),
            "history": lab.history,
            "turns": serializable(lab.receipts),
        }
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        (PACKET / f"{name}-transcript.md").write_text(lab.transcript(), encoding="utf-8")
        print(
            json.dumps(
                {"turns": len(lab.receipts), "actual_model_calls": 0, "full_catalog_pages": len(pages)}
            )
        )
    finally:
        db.close()
        engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
