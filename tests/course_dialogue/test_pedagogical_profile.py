"""Optional pedagogical prompting is wiring, not a semantic quality guarantee."""

import pytest
from test_rag_lab import AssessorFixture, ProviderFixture, ScopeAssessorFixture, page

from oralia.course_dialogue.document_evidence import build_units
from oralia.course_dialogue.rag_lab import RAG_INSTRUCTION, diagnostic_rag_turn


@pytest.mark.asyncio
async def test_general_profile_is_opt_in_and_changes_only_instruction():
    pages = [page("req", "Requisitos\nLa consistencia evita contradicciones.\n")]
    ports = [ProviderFixture(), ProviderFixture()]
    for profile, port in zip(("baseline", "pedagogy-v1"), ports, strict=True):
        await diagnostic_rag_turn(
            pages,
            build_units(pages),
            "consistencia requisitos",
            [],
            scope_assessor=ScopeAssessorFixture(),
            assessor=AssessorFixture("sufficient"),
            provider=port,
            pedagogical_profile=profile,
        )
    before, after = [p.requests[0].model_dump() for p in ports]
    assert before["instruction"] == RAG_INSTRUCTION
    assert after["instruction"].startswith(RAG_INSTRUCTION)
    assert "supuestos" in after["instruction"]
    assert "estrategia" in after["instruction"]
    assert "registro" not in after["instruction"]
    assert {k: v for k, v in before.items() if k != "instruction"} == {
        k: v for k, v in after.items() if k != "instruction"
    }
