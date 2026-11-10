"""One bounded offline RAG plumbing diagnosis; fixture gates are not semantic review."""

import asyncio
import json
from dataclasses import asdict
from pathlib import Path

from oralia.course_dialogue.cached_transformers import CACHED_MODEL, cached_provider
from oralia.course_dialogue.document_evidence import load_authorized_units
from oralia.course_dialogue.rag_lab import ScopeAssessment, SufficiencyAssessment, diagnostic_rag_turn

OUTPUT = Path("specs/012-conversational-course-study/evidence/rag-local-first")


class FixtureAssessor:
    def __init__(self, *statuses):
        self.statuses = iter(statuses)

    def __call__(self, question, retrieval):
        return SufficiencyAssessment(
            next(self.statuses), "fixture-not-semantic-review", "estado inyectado para probar cableado"
        )


def fixture_scope(_question, _resolved_query, _history):
    return ScopeAssessment("in_scope", reason="alcance inyectado, no decisión docente")


def serializable(row):
    attempts = row["evidence_attempts"]
    return {
        "input": row["input"],
        "academic_query": row["academic_query"],
        "focus_change": row["focus_change"],
        "assessments": [asdict(value) for value in row["assessments"]],
        "initial_ids": [unit.id for unit in attempts.initial.units],
        "expanded_ids": [unit.id for unit in attempts.expanded.units] if attempts.expanded else None,
        "delivered_ids": [unit.id for unit in attempts.delivered.units],
        "delivered_trace": attempts.delivered.trace,
        "generation_request": (
            row["generation_request"].model_dump(mode="json") if row["generation_request"] else None
        ),
        "outcome": row["outcome"].model_dump(mode="json") if row["outcome"] else None,
        "displayed_text": row["displayed_text"],
        "displayed_kind": row["displayed_kind"],
        "raw_candidate": row["raw_candidate"],
        "laboratory_preview": row["laboratory_preview"],
        "participant_display": row["participant_display"],
        "citation_check": row["citation_check"],
        "history_omissions": row["history_omissions"],
        "publication_allowed": row["publication_allowed"],
        "semantic_support": row["semantic_support"],
    }


async def main():
    OUTPUT.mkdir(parents=True, exist_ok=False)
    catalog, units = load_authorized_units()
    records = []
    async with cached_provider(OUTPUT, source=CACHED_MODEL) as provider:
        first = await diagnostic_rag_turn(
            catalog,
            units,
            "¿Qué puede y qué no puede demostrar una prueba que pasa?",
            [],
            scope_assessor=fixture_scope,
            assessor=FixtureAssessor("sufficient"),
            provider=provider,
        )
        records.append(serializable(first))
        followup = await diagnostic_rag_turn(
            catalog,
            units,
            "¿Por qué?",
            [first],
            scope_assessor=fixture_scope,
            assessor=FixtureAssessor("insufficient", "sufficient"),
            provider=provider,
        )
        records.append(serializable(followup))
        insufficient = await diagnostic_rag_turn(
            catalog,
            units,
            "Pregunta sin respaldo en los PDF autorizados",
            [],
            scope_assessor=fixture_scope,
            assessor=FixtureAssessor("insufficient", "insufficient"),
            provider=provider,
        )
        records.append(serializable(insufficient))
        conflict = await diagnostic_rag_turn(
            catalog,
            units,
            "¿Son compatibles estas dos reglas?",
            [],
            scope_assessor=fixture_scope,
            assessor=FixtureAssessor("conflict"),
            provider=provider,
        )
        records.append(serializable(conflict))
    (OUTPUT / "conversation.json").write_text(
        json.dumps(
            {"fixture_assessments_not_semantic_evidence": True, "turns": records},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(json.dumps({"turns": len(records), "generated": sum(bool(r["outcome"]) for r in records)}))


if __name__ == "__main__":
    asyncio.run(main())
