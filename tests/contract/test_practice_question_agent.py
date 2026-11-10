"""Contract test for PracticeQuestionAgent (question_type/internal_expected_answer/
reveals_solution) — MUST incluir cobertura paramétrica de los 5 valores de
question_type; nunca evalúa la calidad académica ni la corrección pedagógica de la
pregunta generada — [Remediación F8/LOW — FR-012]."""

from __future__ import annotations

import uuid

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.practice_question_agent import QUESTION_TYPES, PracticeQuestionAgent

_EVIDENCE = [
    {"fragment_id": "f1", "text": "La fotosíntesis convierte luz en energía química.", "document_id": "d1", "document_version": 1}
]


def _request(previous_questions: list[dict] | None = None, reveals_solution: bool = False):
    return AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        input={
            "evidence": _EVIDENCE,
            "objective_ref": "obj-1",
            "concepts": ["fotosíntesis"],
            "previous_questions": previous_questions or [],
            "reveals_solution": reveals_solution,
        },
    )


@pytest.mark.contract
async def test_output_shape_is_complete():
    agent = PracticeQuestionAgent()
    result = await agent.execute(_request(), CancellationToken())
    assert result.status == "ok"
    for key in (
        "question_type",
        "question_text",
        "internal_expected_answer",
        "difficulty_hint",
        "reveals_solution",
        "generation_trace",
    ):
        assert key in result.output


@pytest.mark.contract
@pytest.mark.parametrize("previous_count", list(range(len(QUESTION_TYPES))))
async def test_question_type_covers_all_five_canonical_values(previous_count: int):
    agent = PracticeQuestionAgent()
    previous = [{"question_type": "explicacion", "concepts": []} for _ in range(previous_count)]
    result = await agent.execute(_request(previous_questions=previous), CancellationToken())
    assert result.output["question_type"] == QUESTION_TYPES[previous_count]
    assert result.output["question_type"] in QUESTION_TYPES


@pytest.mark.contract
async def test_internal_expected_answer_populated_when_reveals_solution_false():
    agent = PracticeQuestionAgent()
    result = await agent.execute(_request(reveals_solution=False), CancellationToken())
    assert result.output["internal_expected_answer"] is not None
    assert result.output["reveals_solution"] is False


@pytest.mark.contract
async def test_internal_expected_answer_null_when_reveals_solution_true():
    agent = PracticeQuestionAgent()
    result = await agent.execute(_request(reveals_solution=True), CancellationToken())
    assert result.output["internal_expected_answer"] is None
    assert result.output["reveals_solution"] is True
