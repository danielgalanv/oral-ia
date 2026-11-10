"""Synthetic bounded target/action routing; never pedagogical acceptance."""

import json
import uuid

import pytest

from oralia.course_dialogue.semantic_planner import LocalSemanticPlanner
from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.infrastructure.generation.generation_port import GenerationOutcome


@pytest.mark.asyncio
async def test_joint_intent_proposal_contains_only_registered_tuples_and_actual_greeting():
    data = request()
    data.input["semantic_planning_version"] = 6
    data.input["text"] = "Hola. Consulta sintética."
    port = Port([{"act": "comparison", "goal_ref": "a", "comparison_goal_ref": "b", "greet": True}])
    result = await LocalSemanticPlanner(port).plan(data, CancellationToken())
    assert result.act == "comparison" and result.greet is True and len(port.requests) == 1
    alternatives = [json.loads(text) for text in port.requests[0].output_schema["x-oralia-finite-outputs"]]
    assert all(candidate["greet"] is True for candidate in alternatives)
    assert not any(candidate["act"] == "respond" for candidate in alternatives)


@pytest.mark.asyncio
async def test_joint_intent_rejects_undeclared_reverse_relation_despite_real_goal_ids():
    data = request()
    data.input["semantic_planning_version"] = 6
    port = Port([{"act": "comparison", "goal_ref": "b", "comparison_goal_ref": "a"}])
    with pytest.raises(ValueError, match="tuple"):
        await LocalSemanticPlanner(port).plan(data, CancellationToken())


@pytest.mark.asyncio
async def test_joint_intent_correction_reuses_real_claim_and_goal_scoped_binding():
    data = request()
    data.input["semantic_planning_version"] = 6
    port = Port([{"act": "correct", "goal_ref": "a"}, {"contrast_index": 0}])
    result = await LocalSemanticPlanner(port).plan(data, CancellationToken())
    assert result.claim_quote == data.input["text"]
    assert str(result.correction_ref) == data.input["correction_options"][0]["id"]
    assert len(port.requests) == 2


class Port:
    def __init__(self, answers):
        self.answers = iter(answers)
        self.requests = []

    async def generate(self, request):
        self.requests.append(request)
        return GenerationOutcome(
            ok=True, text=json.dumps(next(self.answers)), adapter="deterministic", finish_reason="stop"
        )


@pytest.mark.asyncio
async def test_readable_goal_projection_is_reversible_and_does_not_change_input_or_unit_ids():
    data = request()
    data.input["semantic_planning_version"] = 7
    data.input["goals"][0]["title"] = "Ámbito A"
    data.input["goals"][1]["title"] = "Ámbito B"
    question = str(uuid.uuid4())
    data.input["context"] = {"current_goal": "a", "pending_question_id": question}
    port = Port([{"act": "respond", "goal_ref": "ambito_a"}])
    planner = LocalSemanticPlanner(port)
    result = await planner.plan(data, CancellationToken())
    assert result.goal_ref == "a" and str(result.reply_to_question_id) == question
    payload = json.loads(port.requests[0].student_input)
    assert payload["current_input"] == data.input["text"]
    assert payload["actual_context"]["pending_question_id"] == question
    assert planner.last_trace["goal_reference_resolution"]["ambito_a"] == "a"


@pytest.mark.asyncio
async def test_readable_projection_refuses_colliding_titles_before_inference():
    data = request()
    data.input["semantic_planning_version"] = 7
    for goal in data.input["goals"]:
        goal["title"] = "Mismo título"
    port = Port([])
    with pytest.raises(ValueError, match="reference"):
        await LocalSemanticPlanner(port).plan(data, CancellationToken())
    assert port.requests == []


@pytest.mark.asyncio
async def test_v8_single_focus_drops_inherited_pair_for_a_question():
    data = request()
    data.input["semantic_planning_version"] = 8
    data.input["goals"][0]["title"] = "Focus A"
    data.input["goals"][1]["title"] = "Focus B"
    data.input["context"] = {"current_goal": "a", "comparison_goal_ref": "b"}
    port = Port([{"target_ref": "focus_a"}, {"act": "ask"}])
    planner = LocalSemanticPlanner(port)
    result = await planner.plan(data, CancellationToken())
    assert (result.act, result.goal_ref, result.comparison_goal_ref) == ("ask", "a", None)
    assert planner.last_trace["protocol"] == "semantic-planning/v8-readable-focus-then-act"
    assert json.loads(port.requests[0].student_input)["actual_context"]["comparison_goal_ref"] == "focus_b"


@pytest.mark.asyncio
async def test_v8_can_keep_a_registered_relation_when_selected():
    data = request()
    data.input["semantic_planning_version"] = 8
    data.input["goals"][0]["title"] = "Focus A"
    data.input["goals"][1]["title"] = "Focus B"
    port = Port([{"target_ref": "relation:ab"}, {"act": "comparison"}])
    result = await LocalSemanticPlanner(port).plan(data, CancellationToken())
    assert (result.act, result.goal_ref, result.comparison_goal_ref) == (
        "comparison",
        "a",
        "b",
    )


@pytest.mark.asyncio
async def test_v9_new_request_cannot_become_pending_question_response():
    data = request()
    data.input["semantic_planning_version"] = 9
    data.input["goals"][0]["title"] = "Focus A"
    data.input["goals"][1]["title"] = "Focus B"
    question = str(uuid.uuid4())
    data.input["context"] = {
        "current_goal": "a",
        "pending_question_id": question,
        "pending_question_text": "Pregunta sintética efectiva",
    }
    port = Port(
        [
            {"target_ref": "relation:ab"},
            {"turn_role": "new_request"},
            {"act": "comparison"},
        ]
    )
    planner = LocalSemanticPlanner(port)
    result = await planner.plan(data, CancellationToken())
    assert (result.act, result.goal_ref, result.comparison_goal_ref) == ("comparison", "a", "b")
    actions = {c["act"] for c in json.loads(port.requests[2].student_input)["choices"]}
    assert "respond" not in actions
    assert planner.last_trace["protocol"] == "semantic-planning/v9-readable-focus-then-act"


@pytest.mark.asyncio
async def test_v9_actual_answer_attempt_can_bind_pending_question():
    data = request()
    data.input["semantic_planning_version"] = 9
    data.input["goals"][0]["title"] = "Focus A"
    data.input["goals"][1]["title"] = "Focus B"
    question = str(uuid.uuid4())
    data.input["context"] = {
        "current_goal": "a",
        "pending_question_id": question,
        "pending_question_text": "Pregunta sintética efectiva",
    }
    port = Port([{"target_ref": "focus_a"}, {"turn_role": "answer_attempt"}, {"act": "respond"}])
    result = await LocalSemanticPlanner(port).plan(data, CancellationToken())
    assert result.act == "respond" and str(result.reply_to_question_id) == question


@pytest.mark.asyncio
async def test_v9_requires_effective_question_text_for_response_gate():
    data = request()
    data.input["semantic_planning_version"] = 9
    data.input["goals"][0]["title"] = "Focus A"
    data.input["goals"][1]["title"] = "Focus B"
    data.input["context"] = {"current_goal": "a", "pending_question_id": str(uuid.uuid4())}
    port = Port([{"target_ref": "focus_a"}])
    with pytest.raises(ValueError, match="pending question text"):
        await LocalSemanticPlanner(port).plan(data, CancellationToken())


@pytest.mark.asyncio
async def test_v10_can_reduce_a_proposed_relation_to_sufficient_single_goal():
    data = request()
    data.input["semantic_planning_version"] = 10
    data.input["goals"][0]["title"] = "Focus A"
    data.input["goals"][1]["title"] = "Focus B"
    port = Port(
        [
            {"target_ref": "relation:ab"},
            {"focus_scope": "secondary_only"},
            {"act": "explain"},
        ]
    )
    planner = LocalSemanticPlanner(port)
    result = await planner.plan(data, CancellationToken())
    assert (result.act, result.goal_ref, result.comparison_goal_ref) == ("explain", "b", None)
    details = json.loads(port.requests[1].student_input)["focus_details"]
    assert [item["role"] for item in details] == ["primary", "secondary"]
    assert planner.last_trace["protocol"] == "semantic-planning/v10-readable-focus-then-act"


@pytest.mark.asyncio
async def test_v10_retains_registered_relation_when_both_goals_needed():
    data = request()
    data.input["semantic_planning_version"] = 10
    data.input["goals"][0]["title"] = "Focus A"
    data.input["goals"][1]["title"] = "Focus B"
    port = Port(
        [
            {"target_ref": "relation:ab"},
            {"focus_scope": "keep_relation"},
            {"act": "comparison"},
        ]
    )
    result = await LocalSemanticPlanner(port).plan(data, CancellationToken())
    assert (result.act, result.goal_ref, result.comparison_goal_ref) == ("comparison", "a", "b")


def request():
    return AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        deadline_ms=30000,
        input={
            "semantic_planning_version": 4,
            "text": "Entrada sintética real del turno",
            "context": {},
            "goals": [{"id": "a", "description": "concept A"}, {"id": "b", "description": "concept B"}],
            "relations": [
                {
                    "id": "ab",
                    "primary_goal": "a",
                    "secondary_goal": "b",
                    "description": "relation",
                    "definition_ref": str(uuid.uuid4()),
                }
            ],
            "correction_options": [
                {"id": str(uuid.uuid4()), "goal_ref": "a", "contrast": "first"},
                {"id": str(uuid.uuid4()), "goal_ref": "a", "contrast": "second"},
            ],
        },
    )


@pytest.mark.asyncio
async def test_catalog_relation_and_actual_greeting_remain_separate():
    data = request()
    data.input["text"] = "Hola. Consulta sintética sobre una relación."
    port = Port([{"target_index": 2}, {"action_index": 3}])
    planner = LocalSemanticPlanner(port)
    result = await planner.plan(data, CancellationToken())
    assert (result.goal_ref, result.comparison_goal_ref, result.act, result.greet) == (
        "a",
        "b",
        "comparison",
        True,
    )
    assert len(port.requests) == 2 and planner.last_trace["max_calls"] == 3
    assert planner.last_trace["publication_authority"] is False


@pytest.mark.asyncio
async def test_catalog_correction_keeps_actual_input_and_bound_contrast():
    data = request()
    port = Port([{"target_index": 0}, {"action_index": 5}, {"contrast_index": 1}])
    result = await LocalSemanticPlanner(port).plan(data, CancellationToken())
    assert str(result.correction_ref) == data.input["correction_options"][1]["id"]
    assert result.claim_quote == data.input["text"] and len(port.requests) == 3


@pytest.mark.asyncio
async def test_answer_to_a_relation_question_binds_the_actual_pending_reference():
    data = request()
    question = str(uuid.uuid4())
    data.input["context"] = {"current_goal": "a", "comparison_goal_ref": "b", "pending_question_id": question}
    port = Port([{"target_index": 2}, {"action_index": 6}])
    result = await LocalSemanticPlanner(port).plan(data, CancellationToken())
    assert result.act == "respond" and str(result.reply_to_question_id) == question
    assert result.comparison_goal_ref is None


@pytest.mark.asyncio
async def test_new_protocol_is_explicit_and_uses_the_existing_agent():
    from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent

    port = Port([{"target_index": 2}, {"action_index": 3}])
    agent = StudyIntentInterpreterAgent(semantic_planner=LocalSemanticPlanner(port), semantic_version=4)
    result = await agent.execute(request(), CancellationToken())
    assert result.status == "ok" and result.trace["contract_version"] == "5.1.0"
    assert result.output["publication_authority"] is False


@pytest.mark.asyncio
async def test_receiving_an_answer_is_not_offered_without_a_pending_question():
    port = Port([{"target_index": 0}, {"action_index": 4}])
    result = await LocalSemanticPlanner(port).plan(request(), CancellationToken())
    choices = json.loads(port.requests[1].student_input)["choices"]
    assert "respond" not in {choice["value"]["act"] for choice in choices}
    assert result.act == "ask" and result.greet is False


@pytest.mark.asyncio
async def test_literal_reference_protocol_avoids_index_translation_and_invalid_state_actions():
    data = request()
    data.input["semantic_planning_version"] = 5
    port = Port([{"target_ref": "a"}, {"act": "explain"}])
    result = await LocalSemanticPlanner(port).plan(data, CancellationToken())
    assert result.goal_ref == "a" and result.act == "explain"
    first = json.loads(port.requests[0].student_input)
    assert {c["target_ref"] for c in first["choices"]} == {
        "a",
        "b",
        "relation:ab",
        "control:clarify",
        "control:outside_catalog",
        "control:finish",
    }
    acts = {c["act"] for c in json.loads(port.requests[1].student_input)["choices"]}
    assert not acts & {"respond", "rephrase", "clarify", "finish"}


@pytest.mark.asyncio
async def test_literal_reference_protocol_rejects_undeclared_or_extra_authority():
    data = request()
    data.input["semantic_planning_version"] = 5
    for answer in [{"target_ref": "unregistered"}, {"target_ref": "a", "approved": True}]:
        with pytest.raises(ValueError):
            await LocalSemanticPlanner(Port([answer])).plan(data, CancellationToken())


@pytest.mark.asyncio
async def test_literal_reference_protocol_cannot_receive_after_question_was_cleared():
    data = request()
    data.input["semantic_planning_version"] = 5
    data.input["context"] = {"current_goal": "a", "pending_question_id": None}
    port = Port([{"target_ref": "a"}, {"act": "respond"}])
    with pytest.raises(ValueError, match="reference"):
        await LocalSemanticPlanner(port).plan(data, CancellationToken())


@pytest.mark.asyncio
@pytest.mark.parametrize("index", [True, -1, 999, "0"])
async def test_catalog_rejects_non_integer_or_unknown_target(index):
    port = Port([{"target_index": index}])
    with pytest.raises(ValueError, match="index"):
        await LocalSemanticPlanner(port).plan(request(), CancellationToken())
    assert len(port.requests) == 1
