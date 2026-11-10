"""Read-only laboratory check of the confirmed course scope policy; no model."""

import asyncio
import hashlib
import json
import sqlite3
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from oralia.course_dialogue.corpus import SOURCE_ROOT
from oralia.course_dialogue.document_evidence import load_authorized_units
from oralia.course_dialogue.rag_lab import (
    ActivityScopeBinding,
    ScopeAssessment,
    SufficiencyAssessment,
    diagnostic_rag_turn,
)
from oralia.infrastructure.generation.generation_port import GenerationOutcome

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "specs/012-conversational-course-study/evidence/course-scope-policy-v1.json"
OUTPUT = ROOT / "specs/012-conversational-course-study/evidence/course-scope-policy-validation-v3.json"
DATABASE = ROOT / ".oralia-course-study/course.db"


class FixtureProvider:
    calls = 0

    async def generate(self, _request):
        self.calls += 1
        return GenerationOutcome(
            ok=True, text="Preview ficticio de cableado.", adapter="deterministic", finish_reason="stop"
        )


async def main():
    if OUTPUT.exists():
        raise ValueError("validation evidence already exists")
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    engine = create_engine(
        "sqlite://",
        creator=lambda: sqlite3.connect("file:" + DATABASE.as_posix() + "?mode=ro", uri=True),
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
    )
    provider = FixtureProvider()
    try:
        binding.revalidate(db)

        def unused_assessor(*_):
            raise AssertionError("academic sufficiency should not run")

        outside = await diagnostic_rag_turn(
            [],
            [],
            "¿Debo estudiar gestión de calidad como bloque propio?",
            [],
            scope_assessor=lambda *_: ScopeAssessment(
                "out_of_scope",
                authority_ref=binding.policy_sha256,
                excluded_block_id="gestion_calidad",
                standalone_excluded_block=True,
                reason="bloque extra excluido para esta actividad",
            ),
            assessor=unused_assessor,
            provider=provider,
            binding=binding,
            db=db,
        )
        uncertain = await diagnostic_rag_turn(
            [],
            [],
            "Tema no delimitado",
            [],
            scope_assessor=lambda *_: ScopeAssessment("uncertain_scope", reason="frontera no enumerada"),
            assessor=unused_assessor,
            provider=provider,
            binding=binding,
            db=db,
        )
        catalog, units = load_authorized_units()
        mixed = await diagnostic_rag_turn(
            catalog,
            units,
            "Explica consistencia de requisitos y gestión de calidad como bloque propio",
            [],
            scope_assessor=lambda *_: ScopeAssessment(
                "mixed",
                authority_ref=binding.policy_sha256,
                block_id="ingenieria_requisitos",
                excluded_block_id="gestion_calidad",
                standalone_excluded_block=True,
                reason="dos bloques delimitados",
                in_scope_question="Explica consistencia de requisitos",
                excluded_part="gestión de calidad como bloque propio",
            ),
            assessor=lambda *_: SufficiencyAssessment("sufficient", "fixture", "solo cableado"),
            provider=provider,
            binding=binding,
            db=db,
        )
        result = {
            "policy_sha256": binding.policy_sha256,
            "source_hashes_revalidated": True,
            "activity_id": policy["activity_id"],
            "activity_version": policy["activity_version"],
            "fixture_semantic_decisions": True,
            "cases": [
                {
                    "id": "extra_block",
                    "scope_result": outside["scope_result"],
                    "model_called": False,
                    "participant_display": outside["participant_display"],
                },
                {
                    "id": "unlisted",
                    "scope_result": uncertain["scope_result"],
                    "model_called": False,
                    "participant_display": uncertain["participant_display"],
                },
                {
                    "id": "mixed",
                    "scope_result": mixed["scope_result"],
                    "model_called": bool(mixed["outcome"]),
                    "student_input": mixed["generation_request"].student_input,
                    "participant_display": mixed["participant_display"],
                },
            ],
            "fixture_provider_calls": provider.calls,
            "publication_allowed": False,
        }
        OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(
            json.dumps({"validated": True, "cases": len(result["cases"]), "provider_calls": provider.calls})
        )
    finally:
        db.close()
        engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
