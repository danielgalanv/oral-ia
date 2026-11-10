"""Semantic plans never grant review, disclosure or a grade."""

import asyncio
import json
import uuid
from dataclasses import asdict
from pathlib import Path

import pytest
from pydantic import ValidationError

from oralia.course_dialogue.draft_dialogue import DraftCurriculum, DraftState
from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent
from oralia.domain.dialogue.contracts import SemanticStudyPlan


def curriculum():
    sources = json.loads(
        Path("specs/012-conversational-course-study/evidence/source-catalog.json").read_text(encoding="utf-8")
    )
    return DraftCurriculum(catalog=sources)


@pytest.mark.parametrize("field", ["reviewed", "text", "score", "publication_allowed"])
def test_plan_rejects_authority_or_free_text(field):
    with pytest.raises(ValidationError):
        SemanticStudyPlan.model_validate({"act": "explain", "goal_ref": "validacion_requisitos", field: True})


def test_drafts_cannot_be_promoted_by_calling_renderer():
    c = curriculum()
    state = DraftState()
    with pytest.raises(ValueError, match="Teacher review"):
        c.render_preview(
            SemanticStudyPlan(act="explain", goal_ref="validacion_requisitos"), state, for_participant=True
        )
    assert state == DraftState()


def test_rephrase_preserves_referent_and_general_before_example():
    c = curriculum()
    state = DraftState(current_goal="validacion_requisitos")
    row, next_state = c.render_preview(
        SemanticStudyPlan(act="rephrase", goal_ref="validacion_requisitos"), state
    )
    assert row["candidate_text"].index("dos preguntas") < row["candidate_text"].index("Ejemplo hipotético")
    assert "¿qué tendrías" in row["candidate_text"]
    assert next_state.pending_question_id and next_state.assessment == "not_assessed"
    assert not row["publication_allowed"]
    with pytest.raises(ValueError, match="referent"):
        c.render_preview(SemanticStudyPlan(act="rephrase", goal_ref="conflictos_requisitos"), state)


def test_source_change_or_foreign_goal_does_not_advance_state():
    sources = json.loads(
        Path("specs/012-conversational-course-study/evidence/source-catalog.json").read_text(encoding="utf-8")
    )
    sources[0]["original_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="source"):
        DraftCurriculum(catalog=sources)
    state = DraftState()
    before = asdict(state)
    with pytest.raises(ValueError, match="unknown goal"):
        curriculum().render_preview(SemanticStudyPlan(act="explain", goal_ref="foreign_course"), state)
    assert asdict(state) == before


def test_new_focus_keeps_deferred_question_without_marking_mastery():
    c = curriculum()
    _, state = c.render_preview(SemanticStudyPlan(act="ask", goal_ref="validacion_requisitos"), DraftState())
    old = state.pending_question_id
    row, next_state = c.render_preview(
        SemanticStudyPlan(act="explain", goal_ref="conflictos_requisitos"), state
    )
    assert old in next_state.deferred_questions
    assert next_state.assessment == "not_assessed" and "Pasamos" in row["candidate_text"]


@pytest.mark.asyncio
async def test_existing_interpreter_opt_in_cancels_without_a_plan():
    class Planner:
        async def plan(self, request, cancellation):
            await asyncio.sleep(60)

    agent = StudyIntentInterpreterAgent(semantic_planner=Planner())
    token = CancellationToken()
    request = AgentRequest(
        session_id=uuid.uuid4(), turn_id=uuid.uuid4(), input={"semantic_planning_version": 1}
    )
    task = asyncio.create_task(agent.execute(request, token))
    await asyncio.sleep(0)
    token.cancel()
    result = await task
    assert result.status == "cancelled" and result.output is None
    assert StudyIntentInterpreterAgent().contract.timeout_ms == 2000
    assert agent.contract.timeout_ms == 32000


def test_clarification_uses_actual_goal_without_inventing_another_topic():
    c = curriculum()
    state = DraftState(current_goal="validacion_requisitos")
    row, after = c.render_preview(SemanticStudyPlan(act="clarify", goal_ref="conflictos_requisitos"), state)
    title = next(g["title"] for g in c.goals if g["id"] == "conflictos_requisitos")
    assert title in row["candidate_text"]
    assert "cliente" not in row["candidate_text"]
    assert after is state
    unknown, _ = c.render_preview(SemanticStudyPlan(act="clarify"), DraftState())
    assert "concepto" in unknown["candidate_text"]
    assert "cliente" not in unknown["candidate_text"]


def test_explanation_does_not_silently_answer_or_drop_pending_question():
    c = curriculum()
    _, state = c.render_preview(SemanticStudyPlan(act="ask", goal_ref="validacion_requisitos"), DraftState())
    _, after = c.render_preview(SemanticStudyPlan(act="explain", goal_ref="validacion_requisitos"), state)
    assert after.pending_question_id == state.pending_question_id
    assert after.assessment == "not_assessed"


def test_sources_are_union_of_all_emitted_units():
    c = curriculum()
    units = [
        u
        for u in c.units
        if u["goal"] == "validacion_requisitos" and u["role"] in {"definition", "cause", "process"}
    ]
    units[0]["source_refs"] = units[0]["source_refs"][:1]
    expected = {json.dumps(ref, sort_keys=True) for unit in units for ref in unit["source_refs"]}
    row, _ = c.render_preview(
        SemanticStudyPlan(act="explain", goal_ref="validacion_requisitos"), DraftState()
    )
    assert {json.dumps(ref, sort_keys=True) for ref in row["source_refs"]} == expected
