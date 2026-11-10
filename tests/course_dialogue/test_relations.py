"""Two-topic proposals resolve only through explicitly authored relations."""

import json
from pathlib import Path

import pytest

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


def test_relation_contains_both_concepts_and_keeps_separate_sources():
    c = curriculum()
    plan = SemanticStudyPlanV2(
        act="comparison", goal_ref="no_ambiguedad", comparison_goal_ref="calidad_individual"
    )
    row, state = c.render_preview(plan, DraftState())
    assert all(word in row["candidate_text"].lower() for word in ["interpret", "comprob", "realiz"])
    assert row["relation_ref"] and row["publication_allowed"] is False
    assert {state.current_goal, state.comparison_goal_ref} == {"calidad_individual", "no_ambiguedad"}
    assert state.assessment == "not_assessed"


def test_unprepared_pair_is_rejected_without_changing_state():
    c = curriculum()
    state = DraftState(current_goal="validacion_requisitos")
    plan = SemanticStudyPlanV2(
        act="comparison", goal_ref="validacion_requisitos", comparison_goal_ref="inspeccion_pruebas"
    )
    with pytest.raises(ValueError, match="relation"):
        c.render_preview(plan, state)
    assert state == DraftState(current_goal="validacion_requisitos")


def test_relation_rephrase_preserves_pair_and_general_before_example():
    c = curriculum()
    plan = SemanticStudyPlanV2(
        act="comparison", goal_ref="calidad_individual", comparison_goal_ref="no_ambiguedad"
    )
    _, state = c.render_preview(plan, DraftState())
    row, after = c.render_preview(plan.model_copy(update={"act": "rephrase"}), state)
    assert row["candidate_text"].find("Ejemplo hipotético") > 30
    assert {after.current_goal, after.comparison_goal_ref} == {state.current_goal, state.comparison_goal_ref}
    with pytest.raises(ValueError, match="Teacher review"):
        c.render_preview(plan, state, for_participant=True)
