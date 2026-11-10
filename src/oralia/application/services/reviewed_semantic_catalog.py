"""Reference planning over currently authorized published units, never approval.

Participant callers must use for_session; the pure compiler is independently
testable but supplies neither authorization snapshots nor trusted output text.
"""

from dataclasses import dataclass

from oralia.domain.dialogue.contracts import SemanticStudyPlanV2


@dataclass(frozen=True)
class GoalBindings:
    goal_ref: str
    root: str
    cause: str
    process: str
    rephrase: str
    example: str
    comparison: str
    question: str


@dataclass(frozen=True)
class ReviewedSelection:
    unit_ids: tuple[str, ...] = ()
    goal_ref: str | None = None
    comparison_goal_ref: str | None = None
    question_ref: str | None = None
    response_question_ref: str | None = None
    support_step: int = 0
    notice: str | None = None


class ReviewedSemanticCatalog:
    def __init__(self, units, *, course_id, activity_id, goal_titles=None):
        self.units = {unit.id: unit for unit in units}
        if len(self.units) != len(units) or any(
            unit.status != "published" or unit.course_id != course_id or activity_id not in unit.activity_refs
            for unit in units
        ):
            raise ValueError("semantic catalog contains unavailable or foreign units")
        self.bindings = {}
        self.goals = []
        self.relations = []
        self.corrections = []
        goal_titles = goal_titles or {}

        def reference(unit, name, kind, *, same_goal=True):
            refs = unit.relations.get(name, [])
            if len(refs) != 1 or refs[0] not in self.units:
                raise ValueError("semantic teaching relation missing or unavailable")
            target = self.units[refs[0]]
            if target.kind != kind or same_goal and target.subgoal_ref != unit.subgoal_ref:
                raise ValueError("semantic teaching relation has an incompatible role or goal")
            return target

        for unit in units:
            if unit.kind != "explanation" or not {"didactic_cause", "didactic_process"} <= set(
                unit.relations
            ):
                continue
            if unit.subgoal_ref in self.bindings:
                raise ValueError("semantic goal has more than one current root")
            values = {
                name: reference(unit, relation, kind).id
                for name, relation, kind in [
                    ("cause", "didactic_cause", "explanation"),
                    ("process", "didactic_process", "explanation"),
                    ("rephrase", "rephrases", "explanation"),
                    ("example", "examples", "example"),
                    ("comparison", "comparisons", "comparison"),
                    ("question", "next", "question"),
                ]
            }
            question = self.units[values["question"]]
            reference(question, "comparisons", "comparison")
            binding = GoalBindings(goal_ref=unit.subgoal_ref, root=unit.id, **values)
            self.bindings[unit.subgoal_ref] = binding
            self.goals.append(
                {
                    "id": unit.subgoal_ref,
                    "title": goal_titles.get(unit.subgoal_ref, unit.subgoal_ref),
                    "description": unit.reviewed_content,
                }
            )
        if not self.bindings:
            raise ValueError("no complete authorized semantic teaching goals")
        pairs = set()
        bridge_ids = set()
        for unit in units:
            if unit.kind != "comparison" or not unit.relations.get("comparisons"):
                continue
            secondary = reference(unit, "comparisons", "explanation", same_goal=False)
            if secondary.subgoal_ref == unit.subgoal_ref:
                continue
            primary = self.bindings.get(unit.subgoal_ref)
            other = self.bindings.get(secondary.subgoal_ref)
            pair = frozenset([unit.subgoal_ref, secondary.subgoal_ref])
            if primary is None or other is None or secondary.id != other.root or pair in pairs:
                raise ValueError("semantic cross-goal relation has no unique current roots")
            pairs.add(pair)
            bridge_ids.add(unit.id)
            self.relations.append(
                {
                    "id": unit.id,
                    "primary_goal": unit.subgoal_ref,
                    "secondary_goal": secondary.subgoal_ref,
                    "definition_ref": unit.id,
                    "rephrase_ref": reference(unit, "rephrases", "explanation").id,
                    "example_ref": reference(unit, "examples", "example").id,
                    "question_ref": primary.question,
                    "description": unit.reviewed_content,
                }
            )
        self.corrections = [
            {"id": unit.id, "goal_ref": unit.subgoal_ref, "contrast": unit.reviewed_content}
            for unit in units
            if unit.kind == "comparison" and unit.id not in bridge_ids and unit.subgoal_ref in self.bindings
        ]

    @classmethod
    def for_session(cls, db, session, *, goal_titles=None):
        from oralia.application.services.dialogue_retrieval_service import authorized_unit
        from oralia.application.services.guided_dialogue_service import (
            current_units,
            validate_guided_configuration,
        )
        from oralia.domain.policies.output_authorization_contract import ScopeReference
        from oralia.domain.policies.output_template_catalog import MATERIAL_FRAGMENT_RESPONSE
        from oralia.infrastructure.db import models

        db.refresh(session)
        activity = db.get(
            models.ActivityConfiguration, session.activity_configuration_id, populate_existing=True
        )
        state = db.get(models.CognitiveState, session.id, populate_existing=True)
        governance = (
            db.get(models.ActivityGovernance, activity.id, populate_existing=True) if activity else None
        )
        if (
            session.status != "active"
            or activity is None
            or activity.mode != "self_study"
            or governance is None
            or governance.status != "active"
            or governance.model_id != "guided_controlled"
            or state is None
            or state.mode not in {"doubt_resolution", "guided_explanation"}
        ):
            raise ValueError("semantic catalog requires an active non-protected self-study session")
        validate_guided_configuration(db, activity)
        entry = MATERIAL_FRAGMENT_RESPONSE
        scope = ScopeReference(
            topic_ref=entry.topic_ref, purpose_ref=entry.purpose_ref, action_ref=entry.action_ref
        )
        rows = [
            authorized_unit(db, session, unit.id, scope, allow_solution=True)
            for unit in current_units(db, activity)
        ]
        return cls(rows, course_id=activity.course_id, activity_id=activity.id, goal_titles=goal_titles)

    def select(
        self,
        plan,
        *,
        current_goal=None,
        current_pair=None,
        pending_question=None,
        support_step=0,
        current_input=None,
    ):
        plan = SemanticStudyPlanV2.model_validate(plan)
        if plan.act in {"finish", "clarify"}:
            return ReviewedSelection(notice=plan.act)
        binding = self.bindings.get(plan.goal_ref)
        if binding is None:
            raise ValueError("semantic goal outside current reviewed catalog")
        if current_pair is not None and not any(
            item["primary_goal"] == current_goal and item["secondary_goal"] == current_pair
            for item in self.relations
        ):
            raise ValueError("semantic comparative context is not current")
        relation = None
        if plan.comparison_goal_ref is not None:
            relation = next(
                (
                    item
                    for item in self.relations
                    if item["primary_goal"] == plan.goal_ref
                    and item["secondary_goal"] == plan.comparison_goal_ref
                ),
                None,
            )
            if relation is None:
                raise ValueError("semantic pair outside current reviewed catalog")
        if plan.act == "respond":
            if (
                not pending_question
                or str(plan.reply_to_question_id) != pending_question
                or current_goal != plan.goal_ref
                or pending_question not in self.units
                or self.units[pending_question].kind != "question"
                or self.units[pending_question].subgoal_ref != plan.goal_ref
            ):
                raise ValueError("semantic response is not bound to the actual pending question")
            feedback = self.units[pending_question].relations.get("comparisons", [])
            if len(feedback) != 1 or feedback[0] not in self.units:
                raise ValueError("semantic question feedback unavailable")
            return ReviewedSelection(
                unit_ids=(feedback[0],),
                goal_ref=plan.goal_ref,
                comparison_goal_ref=current_pair,
                response_question_ref=pending_question,
                support_step=support_step,
            )
        if plan.act == "rephrase" and (
            current_goal != plan.goal_ref or current_pair != plan.comparison_goal_ref
        ):
            raise ValueError("semantic rephrase changes the actual referent")
        if plan.act == "rephrase" and support_step >= 3:
            return ReviewedSelection(notice="followups_exhausted")
        question = None
        if plan.act == "correct":
            allowed = {item["id"] for item in self.corrections if item["goal_ref"] == plan.goal_ref}
            if relation:
                allowed = {relation["definition_ref"]}
            if (
                str(plan.correction_ref) not in allowed
                or not current_input
                or plan.claim_quote not in current_input
            ):
                raise ValueError("semantic correction lacks current claim/contrast binding")
            refs = (str(plan.correction_ref), binding.question)
            question = binding.question
        elif relation:
            refs = (
                relation["rephrase_ref"] if plan.act == "rephrase" else relation["definition_ref"],
                relation["example_ref"],
                relation["question_ref"],
            )
            question = relation["question_ref"]
        elif plan.act == "explain":
            refs = (binding.root, binding.cause, binding.process)
        elif plan.act == "ask":
            refs = (binding.question,)
            question = binding.question
        else:
            first = (
                binding.rephrase
                if plan.act == "rephrase"
                else binding.comparison if plan.act == "comparison" else binding.root
            )
            refs = (first, binding.example, binding.question)
            question = binding.question
        if len(set(refs)) != len(refs) or any(ref not in self.units for ref in refs):
            raise ValueError("semantic composition has unavailable or duplicate references")
        return ReviewedSelection(
            unit_ids=refs,
            goal_ref=plan.goal_ref,
            comparison_goal_ref=plan.comparison_goal_ref,
            question_ref=question,
            support_step=(
                min(support_step + 1, 3)
                if plan.act == "rephrase"
                else support_step if current_goal == plan.goal_ref else 0
            ),
        )
