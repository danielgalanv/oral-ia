"""Synthetic protocol tests; scope selection is not an authorization verdict."""

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


def request():
    return AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        deadline_ms=30000,
        input={
            "semantic_planning_version": 3,
            "text": "Consulta ficticia sobre técnicas y necesidades",
            "context": {},
            "goals": [
                {"id": "validacion_requisitos", "source_ids": ["procedure:12"]},
                {"id": "inspeccion_pruebas", "source_ids": ["testing:11"]},
                {"id": "verificacion_validacion_software", "source_ids": ["testing:9"]},
            ],
            "relations": [
                {
                    "id": "techniques",
                    "primary_goal": "verificacion_validacion_software",
                    "secondary_goal": "inspeccion_pruebas",
                    "definition_ref": str(uuid.uuid4()),
                    "description": "Técnicas y referencias",
                }
            ],
        },
    )


@pytest.mark.asyncio
async def test_scope_narrows_goals_but_preserves_real_context():
    port = Port(
        [
            {"scope": "software_product"},
            {
                "act": "comparison",
                "goal_ref": "inspeccion_pruebas",
                "comparison_goal_ref": "verificacion_validacion_software",
            },
        ]
    )
    planner = LocalSemanticPlanner(port)
    result = await planner.plan(request(), CancellationToken())
    assert result.goal_ref == "verificacion_validacion_software"
    assert len(port.requests) == 2
    data = json.loads(port.requests[1].student_input)
    assert {g["id"] for g in data["allowed_goals"]} == {
        "inspeccion_pruebas",
        "verificacion_validacion_software",
    }
    assert planner.last_trace["scope_not_authorization"] is True
    assert planner.last_trace["max_calls"] == 3


@pytest.mark.asyncio
async def test_outside_catalog_does_not_generate_a_lesson_or_select_a_random_goal():
    port = Port([{"scope": "outside_catalog"}])
    result = await LocalSemanticPlanner(port).plan(request(), CancellationToken())
    assert result.scope_limit is True and result.goal_ref is None and result.act == "clarify"
    assert len(port.requests) == 1


@pytest.mark.asyncio
async def test_a_later_goal_cannot_escape_the_scoped_set():
    port = Port([{"scope": "software_product"}, {"act": "explain", "goal_ref": "validacion_requisitos"}])
    with pytest.raises(ValueError, match="outside"):
        await LocalSemanticPlanner(port).plan(request(), CancellationToken())


@pytest.mark.asyncio
async def test_scoped_agent_is_opt_in_and_never_authorizes_publication():
    from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent

    port = Port([{"scope": "outside_catalog"}])
    agent = StudyIntentInterpreterAgent(semantic_planner=LocalSemanticPlanner(port), semantic_version=3)
    result = await agent.execute(request(), CancellationToken())
    assert result.status == "ok"
    assert result.trace["contract_version"] == "4.0.0"
    assert result.output["publication_authority"] is False
    assert result.output["semantic_plan"]["scope_limit"] is True


@pytest.mark.asyncio
async def test_unknown_source_metadata_fails_before_inference():
    data = request()
    data.input["goals"][0]["source_ids"] = ["foreign:1"]
    port = Port([])
    with pytest.raises(ValueError, match="source scope"):
        await LocalSemanticPlanner(port).plan(data, CancellationToken())
    assert not port.requests


@pytest.mark.asyncio
async def test_cancelled_agent_starts_no_scope_inference():
    from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent

    token = CancellationToken()
    token.cancel()
    port = Port([])
    agent = StudyIntentInterpreterAgent(semantic_planner=LocalSemanticPlanner(port), semantic_version=3)
    result = await agent.execute(request(), token)
    assert result.status == "cancelled" and not port.requests
