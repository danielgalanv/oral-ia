"""A corrective proposal must identify actual input, not invent a student belief."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from oralia.course_dialogue.draft_dialogue import DraftCurriculum, DraftState
from oralia.domain.dialogue.contracts import SemanticStudyPlanV2


def curriculum():
    sources = json.loads(
        Path("specs/012-conversational-course-study/evidence/source-catalog.json").read_text(encoding="utf8")
    )
    return DraftCurriculum(catalog=sources)


def test_v2_correction_requires_claim_and_explicit_unit():
    with pytest.raises(ValidationError):
        SemanticStudyPlanV2(act="correct", goal_ref="validacion_requisitos")


def test_correction_cannot_attribute_an_unwritten_claim_or_foreign_goal():
    c = curriculum()
    unit = next(u for u in c.units if u["goal"] == "validacion_requisitos" and u["role"] == "correction")
    plan = SemanticStudyPlanV2(
        act="correct", goal_ref=unit["goal"], correction_ref=unit["id"], claim_quote="solo pasar pruebas"
    )
    state = DraftState(current_goal=unit["goal"])
    with pytest.raises(ValueError, match="claim"):
        c.render_preview(plan, state, current_input="¿Qué significa validar?")
    bad = plan.model_copy(update={"goal_ref": "conflictos_requisitos"})
    with pytest.raises(ValueError, match="correction"):
        c.render_preview(bad, state, current_input="¿Validar es solo pasar pruebas?")
    assert state == DraftState(current_goal=unit["goal"])


def test_real_quote_is_traceability_and_never_an_entailment_or_grade_verdict():
    c = curriculum()
    unit = next(u for u in c.units if u["goal"] == "validacion_requisitos" and u["role"] == "correction")
    plan = SemanticStudyPlanV2(
        act="correct", goal_ref=unit["goal"], correction_ref=unit["id"], claim_quote="solo pasar pruebas"
    )
    row, after = c.render_preview(plan, DraftState(), current_input="¿Validar es solo pasar pruebas?")
    assert row["claim_binding"]["quote"] == "solo pasar pruebas"
    assert row["claim_binding"]["semantic_approval"] is False
    assert row["publication_allowed"] is False and after.assessment == "not_assessed"


def test_selected_contrast_is_rendered_instead_of_fixed_correction_for_goal():
    c = curriculum()
    unit = next(u for u in c.units if u["goal"] == "validacion_requisitos" and u["role"] == "comparison")
    text = "Si es coherente, ¿ya responde al cliente?"
    plan = SemanticStudyPlanV2(
        act="correct", goal_ref=unit["goal"], correction_ref=unit["id"], claim_quote="es coherente"
    )
    row, _ = c.render_preview(plan, DraftState(), current_input=text)
    assert row["candidate_text"].startswith(unit["draft_content"])
    assert row["unit_ids"][0] == unit["id"]


@pytest.mark.asyncio
async def test_v2_agent_preserves_version_and_rejects_legacy_or_unknown_request():
    import uuid

    from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
    from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent

    class Planner:
        async def plan(self, request, cancellation):
            return SemanticStudyPlanV2(act="explain", goal_ref="validacion_requisitos")

    agent = StudyIntentInterpreterAgent(semantic_planner=Planner(), semantic_version=2)

    def request(version):
        return AgentRequest(
            session_id=uuid.uuid4(), turn_id=uuid.uuid4(), input={"semantic_planning_version": version}
        )

    assert agent.contract.version == "3.3.0"
    result = await agent.execute(request(2), CancellationToken())
    assert result.status == "ok" and result.output["semantic_plan"]["schema_version"] == 2
    assert result.output["publication_authority"] is False
    for version in (1, 3):
        result = await agent.execute(request(version), CancellationToken())
        assert result.status == "error" and result.output is None
