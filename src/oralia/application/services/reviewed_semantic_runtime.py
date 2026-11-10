"""Explicit local semantic proposal dependency; publication remains in guided T090.

No provider startup, teacher publication, session creation or raw-model trace
persistence happens here. Instances are scoped to one application engine/activity.
"""

import time
from dataclasses import dataclass
from uuid import UUID, uuid4

from oralia.application.orchestration.cancellation import run_with_deadline
from oralia.application.services.reviewed_semantic_catalog import ReviewedSelection, ReviewedSemanticCatalog
from oralia.domain.agents.agent_contract import AgentRequest
from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent
from oralia.domain.dialogue.contracts import DialogueContext


@dataclass(frozen=True)
class SemanticSelectionResult:
    selection: ReviewedSelection
    act: str
    greet: bool
    contract_version: str


class ReviewedSemanticRuntime:
    turn_budget_ms = 32000

    def __init__(self, *, engine, activity_id, generation_port, goal_titles=None):
        self.engine = engine
        self.activity_id = str(activity_id)
        self.port = generation_port
        self.goal_titles = dict(goal_titles or {})

    def applies(self, session):
        return session.activity_configuration_id == self.activity_id

    def assert_engine(self, db):
        if db.get_bind().engine is not self.engine:
            raise ValueError("semantic runtime is bound to another database engine")

    def revalidate(self, db, session, selection):
        self.assert_engine(db)
        if not self.applies(session):
            raise ValueError("semantic runtime is bound to another activity")
        catalog = ReviewedSemanticCatalog.for_session(db, session, goal_titles=self.goal_titles)
        if any(ref not in catalog.units for ref in selection.unit_ids):
            raise ValueError("semantic selected unit is no longer available")
        if selection.goal_ref is not None and selection.goal_ref not in catalog.bindings:
            raise ValueError("semantic selected goal is no longer current")
        if selection.comparison_goal_ref is not None and not any(
            relation["primary_goal"] == selection.goal_ref
            and relation["secondary_goal"] == selection.comparison_goal_ref
            for relation in catalog.relations
        ):
            raise ValueError("semantic selected pair is no longer current")

    async def propose(self, db, session, text, context, *, deadline_ms):
        from oralia.application.services.dialogue_context_service import _validate_turn_reference
        from oralia.course_dialogue.semantic_planner import LocalSemanticPlanner
        from oralia.infrastructure.db import models

        started = time.monotonic()
        self.assert_engine(db)
        if not self.applies(session):
            raise ValueError("semantic runtime is bound to another activity")
        context = DialogueContext.model_validate(context)
        catalog = ReviewedSemanticCatalog.for_session(db, session, goal_titles=self.goal_titles)
        pending = str(context.pending_question_unit_id) if context.pending_question_unit_id else None
        pending_text = None
        if pending is not None:
            if pending not in catalog.units or context.pending_question_turn_id is None:
                raise ValueError("semantic pending question has no current approved turn")
            turn_id = str(context.pending_question_turn_id)
            _validate_turn_reference(db, session.id, turn_id)
            turn = db.get(models.Turn, turn_id)
            pending_text = catalog.units[pending].reviewed_content
            if pending_text not in turn.output_text:
                raise ValueError("semantic pending question was not emitted by its approved turn")
        last_text = None
        if context.last_approved_turn_id is not None:
            turn_id = str(context.last_approved_turn_id)
            _validate_turn_reference(db, session.id, turn_id)
            last_text = db.get(models.Turn, turn_id).output_text
        secondary = None
        if (
            len(context.relevant_concepts) == 2
            and context.current_subgoal_ref == context.relevant_concepts[0]
        ):
            secondary = context.relevant_concepts[1]
            if not any(
                relation["primary_goal"] == context.current_subgoal_ref
                and relation["secondary_goal"] == secondary
                for relation in catalog.relations
            ):
                raise ValueError("semantic current pair is no longer registered")
        planner = LocalSemanticPlanner(self.port)
        agent = StudyIntentInterpreterAgent(semantic_planner=planner, semantic_version=7)
        remaining = min(deadline_ms, self.turn_budget_ms) - int((time.monotonic() - started) * 1000)
        if remaining <= 0:
            raise ValueError("No queda presupuesto para la planificación semántica.")
        result = await run_with_deadline(
            agent,
            AgentRequest(
                session_id=UUID(session.id),
                turn_id=uuid4(),
                deadline_ms=min(remaining, agent.contract.timeout_ms),
                input={
                    "semantic_planning_version": 7,
                    "text": text,
                    "goals": catalog.goals,
                    "relations": catalog.relations,
                    "correction_options": catalog.corrections,
                    "context": {
                        "current_goal": context.current_subgoal_ref,
                        "comparison_goal_ref": secondary,
                        "pending_question_id": pending,
                        "pending_question_text": pending_text,
                        "last_actual_preview": last_text,
                        "support_step": context.support_step,
                    },
                },
            ),
        )
        if result.status != "ok":
            raise ValueError("Planificación semántica no disponible; no se confirma un turno nuevo.")
        plan = result.output["semantic_plan"]
        selection = catalog.select(
            plan,
            current_goal=context.current_subgoal_ref,
            current_pair=secondary,
            pending_question=pending,
            support_step=context.support_step,
            current_input=text,
        )
        # Return reference facts only. Raw outcomes, prompts and claim_quote are
        # deliberately not returned to the persistence/orchestration layer.
        return SemanticSelectionResult(
            selection=selection, act=plan["act"], greet=plan["greet"], contract_version=agent.contract.version
        )
