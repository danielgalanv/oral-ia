"""Synthetic port tests for bounded staging; these are not real model evidence."""

import json
import uuid

import pytest

from oralia.course_dialogue.semantic_planner import LocalSemanticPlanner
from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.infrastructure.generation.generation_port import GenerationOutcome


class Port:
    def __init__(self, answers):
        self.answers = iter(answers)
        self.requests = []

    async def generate(self, request):
        self.requests.append(request)
        return GenerationOutcome(
            ok=True, text=json.dumps(next(self.answers)), adapter="deterministic", finish_reason="stop"
        )


def request(options):
    return AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        deadline_ms=30000,
        input={
            "semantic_planning_version": 2,
            "text": "Esto es solo probar el programa",
            "goals": [
                {"id": "requisitos", "description": "Validación de requisitos"},
                {"id": "otro", "description": "Otro objetivo"},
            ],
            "correction_options": options,
            "context": {"current_goal": "requisitos"},
        },
    )


@pytest.mark.asyncio
async def test_noncorrection_uses_one_call_without_all_contrast_texts():
    port = Port([{"act": "explain", "goal_ref": "requisitos"}])
    planner = LocalSemanticPlanner(port)
    result = await planner.plan(
        request([{"id": str(uuid.uuid4()), "goal_ref": "otro", "contrast": "FOREIGN CONTRAST"}]),
        CancellationToken(),
    )
    assert result.schema_version == 2 and result.act == "explain"
    assert len(port.requests) == 1
    assert "FOREIGN CONTRAST" not in port.requests[0].student_input
    assert len(planner.last_trace["phases"]) == 1


@pytest.mark.asyncio
async def test_correction_second_call_has_only_selected_goal_and_remaining_budget():
    key = str(uuid.uuid4())
    foreign = str(uuid.uuid4())
    options = [
        {"id": key, "goal_ref": "requisitos", "contrast": "No equivale a probar el programa"},
        {"id": foreign, "goal_ref": "otro", "contrast": "FOREIGN CONTRAST"},
    ]
    port = Port(
        [
            {"act": "correct", "goal_ref": "requisitos"},
            {
                "contrast_index": 0,
            },
        ]
    )
    planner = LocalSemanticPlanner(port)
    result = await planner.plan(request(options), CancellationToken())
    assert str(result.correction_ref) == key and len(port.requests) == 2
    assert result.claim_quote == "Esto es solo probar el programa"
    assert "FOREIGN CONTRAST" not in port.requests[1].student_input
    assert 0 < port.requests[1].constraints.deadline_ms <= 30000
    assert len(planner.last_trace["phases"]) == 2


@pytest.mark.asyncio
async def test_binding_call_cannot_change_the_classified_goal():
    key = str(uuid.uuid4())
    options = [{"id": key, "goal_ref": "requisitos", "contrast": "Contraste"}]
    port = Port(
        [
            {"act": "correct", "goal_ref": "requisitos"},
            {"schema_version": 2, "act": "explain", "goal_ref": "otro"},
        ]
    )
    with pytest.raises(ValueError):
        await LocalSemanticPlanner(port).plan(request(options), CancellationToken())


@pytest.mark.asyncio
async def test_exhausted_total_budget_does_not_start_second_call(monkeypatch):
    from types import SimpleNamespace

    from oralia.infrastructure.generation.generation_port import GenerationError

    ticks = iter([0, 31, 31])
    monkeypatch.setattr(
        "oralia.course_dialogue.semantic_planner.time", SimpleNamespace(monotonic=lambda: next(ticks))
    )
    port = Port([{"act": "correct", "goal_ref": "requisitos"}])
    with pytest.raises(GenerationError, match="presupuesto"):
        await LocalSemanticPlanner(port).plan(request([]), CancellationToken())
    assert len(port.requests) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("index", [-1, 1, True, "0", None])
async def test_contrast_index_must_be_an_integer_inside_proposed_goal(index):
    key = str(uuid.uuid4())
    port = Port([{"act": "correct", "goal_ref": "requisitos"}, {"contrast_index": index}])
    options = [{"id": key, "goal_ref": "requisitos", "contrast": "Contraste técnico pendiente"}]
    with pytest.raises(ValueError, match="outside"):
        await LocalSemanticPlanner(port).plan(request(options), CancellationToken())


@pytest.mark.asyncio
async def test_answer_intent_binds_only_actual_pending_question_without_grading():
    question = str(uuid.uuid4())
    port = Port([{"act": "respond", "goal_ref": "requisitos"}])
    original = request([])
    bound = original.model_copy(
        update={
            "input": {
                **original.input,
                "context": {
                    "current_goal": "requisitos",
                    "pending_question_id": question,
                    "pending_question_text": "Pregunta ficticia",
                },
            }
        }
    )
    result = await LocalSemanticPlanner(port).plan(bound, CancellationToken())
    assert str(result.reply_to_question_id) == question and result.act == "respond"
    assert len(port.requests) == 1 and result.claim_quote is None
    with pytest.raises(ValueError, match="pending"):
        await LocalSemanticPlanner(Port([{"act": "respond", "goal_ref": "requisitos"}])).plan(
            original, CancellationToken()
        )


@pytest.mark.asyncio
async def test_model_pair_resolves_only_declared_relation_and_never_free_teaching_text():
    definition = str(uuid.uuid4())
    original = request([])
    data = {
        **original.input,
        "goals": [{"id": "no_ambiguedad"}, {"id": "calidad_individual"}],
        "relations": [
            {
                "id": "quality_relation",
                "primary_goal": "calidad_individual",
                "secondary_goal": "no_ambiguedad",
                "definition_ref": definition,
                "description": "Distintos criterios de calidad",
            }
        ],
    }
    port = Port(
        [{"act": "comparison", "goal_ref": "no_ambiguedad", "comparison_goal_ref": "calidad_individual"}]
    )
    result = await LocalSemanticPlanner(port).plan(
        original.model_copy(update={"input": data}), CancellationToken()
    )
    assert result.goal_ref == "calidad_individual" and result.comparison_goal_ref == "no_ambiguedad"
    assert len(port.requests) == 1 and definition not in port.requests[0].student_input
    bad = Port([{"act": "comparison", "goal_ref": "no_ambiguedad", "comparison_goal_ref": "foreign_goal"}])
    with pytest.raises(ValueError, match="outside"):
        await LocalSemanticPlanner(bad).plan(original.model_copy(update={"input": data}), CancellationToken())
