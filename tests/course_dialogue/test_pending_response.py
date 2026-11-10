"""Receiving an answer is different from grading or inferring understanding."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from oralia.course_dialogue.draft_dialogue import DraftCurriculum, DraftState
from oralia.domain.dialogue.contracts import SemanticStudyPlanV2


def curriculum():
    return DraftCurriculum(
        catalog=json.loads(
            Path("specs/012-conversational-course-study/evidence/source-catalog.json").read_text(
                encoding="utf8"
            )
        )
    )


def test_response_requires_actual_pending_question_reference():
    with pytest.raises(ValidationError):
        SemanticStudyPlanV2(act="respond", goal_ref="validacion_requisitos")


def test_receiving_answer_preserves_referent_and_records_no_assessment():
    c = curriculum()
    _, state = c.render_preview({"act": "ask", "goal_ref": "validacion_requisitos"}, DraftState())
    plan = SemanticStudyPlanV2(
        act="respond", goal_ref=state.current_goal, reply_to_question_id=state.pending_question_id
    )
    row, after = c.render_preview(
        plan, state, current_input="Comprobaría si recoge la necesidad de cancelar."
    )
    assert "Retomo tu respuesta" in row["candidate_text"]
    assert after.current_goal == state.current_goal and after.pending_question_id is None
    assert after.last_response_question_id == state.pending_question_id
    assert after.assessment == "not_assessed" and row["publication_allowed"] is False
    assert state.pending_question_id is not None


def test_response_cannot_consume_pending_question_of_another_goal():
    c = curriculum()
    _, state = c.render_preview({"act": "ask", "goal_ref": "validacion_requisitos"}, DraftState())
    plan = SemanticStudyPlanV2(
        act="respond", goal_ref="conflictos_requisitos", reply_to_question_id=state.pending_question_id
    )
    with pytest.raises(ValueError, match="question"):
        c.render_preview(plan, state, current_input="Respuesta ficticia")
    assert state.pending_question_id is not None


def test_feedback_addresses_question_instead_of_another_contrast_of_same_goal():
    c = curriculum()
    _, state = c.render_preview({"act": "ask", "goal_ref": "inspeccion_pruebas"}, DraftState())
    plan = SemanticStudyPlanV2(
        act="respond", goal_ref=state.current_goal, reply_to_question_id=state.pending_question_id
    )
    row, _ = c.render_preview(
        plan, state, current_input="Creo que una inspección sin defectos elimina las pruebas."
    )
    assert "complementarias" in row["candidate_text"]
    assert "necesidades reales del cliente" not in row["candidate_text"]
