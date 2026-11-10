"""Controlled draft preview. This deliberately cannot publish to participants."""

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

from oralia.domain.dialogue.contracts import SemanticStudyPlan, SemanticStudyPlanV2

PACKET = Path(__file__).resolve().parents[3] / "materiales/docente/feature012-course-drafts/curriculum.json"


@dataclass
class DraftState:
    current_goal: str | None = None
    pending_question_id: str | None = None
    last_unit_ids: list[str] = field(default_factory=list)
    support_step: int = 0
    deferred_questions: list[str] = field(default_factory=list)
    assessment: str = "not_assessed"
    last_response_question_id: str | None = None
    comparison_goal_ref: str | None = None


class DraftCurriculum:
    def __init__(self, path=PACKET, *, catalog=None):
        data = path.read_bytes()
        manifest = json.loads(path.with_name("manifest.json").read_text())
        if hashlib.sha256(data).hexdigest() != manifest["curriculum_sha256"]:
            raise ValueError("draft packet changed; review source before reuse")
        self.packet = json.loads(data)
        if self.packet["human_review"] != "pending" or self.packet["participant_publication"] is not False:
            raise ValueError("inspection packet cannot self-approve")
        self.units = self.packet["units"]
        if catalog is None:
            from oralia.course_dialogue.corpus import load_catalog

            catalog = load_catalog()
        sources = {r["id"]: r for r in catalog}
        for unit in self.units:
            for ref in unit["source_refs"]:
                current = sources.get(ref["source_id"])
                if (
                    current is None
                    or current["original_sha256"] != ref["original_sha256"]
                    or current["page"] != ref["page"]
                ):
                    raise ValueError("draft source missing or changed")
        self.goals = [
            {
                **g,
                "description": next(
                    u["draft_content"]
                    for u in self.units
                    if u["goal"] == g["id"] and u["role"] == "definition"
                ),
            }
            for g in self.packet["goals"]
        ]
        self.corrections = [
            {"id": u["id"], "goal_ref": u["goal"], "contrast": u["draft_content"]}
            for u in self.units
            if u["role"] in {"correction", "comparison"}
        ]
        self.relations = self.packet.get("relations", [])
        by_id = {u["id"]: u for u in self.units}
        goals = {g["id"] for g in self.goals}
        pairs = set()
        for relation in self.relations:
            pair = frozenset([relation["primary_goal"], relation["secondary_goal"]])
            if len(pair) != 2 or not pair <= goals or pair in pairs or relation["review_status"] != "pending":
                raise ValueError("invalid or duplicated draft relation")
            pairs.add(pair)
            for name, kind in [
                ("definition_ref", "comparison"),
                ("rephrase_ref", "explanation"),
                ("example_ref", "example"),
                ("question_ref", "question"),
            ]:
                unit = by_id.get(relation[name])
                if unit is None or unit["goal"] != relation["primary_goal"] or unit["kind"] != kind:
                    raise ValueError("relation unit missing or outside primary goal")

    def render_preview(self, plan, state, *, for_participant=False, current_input=None):
        if for_participant:
            raise ValueError("Teacher review and normal T090 binding required; drafts cannot be published")
        value = plan.model_dump(mode="json") if hasattr(plan, "model_dump") else plan
        plan_type = SemanticStudyPlanV2 if value.get("schema_version") == 2 else SemanticStudyPlan
        plan = plan_type.model_validate(value)
        if getattr(plan, "comparison_goal_ref", None) is not None:
            return self._render_relation(plan, state, current_input)
        claim_binding = None
        chosen_correction = None
        response_question = None
        response_feedback = None
        if isinstance(plan, SemanticStudyPlanV2):
            if (
                plan.reply_to_question_id is not None
                and str(plan.reply_to_question_id) != state.pending_question_id
            ):
                raise ValueError("question reference is not pending")
            if plan.act == "respond":
                response_question = next(
                    (u for u in self.units if u["id"] == state.pending_question_id), None
                )
                if (
                    response_question is None
                    or response_question["role"] != "question"
                    or response_question["goal"] != plan.goal_ref
                    or state.current_goal != plan.goal_ref
                ):
                    raise ValueError("response question outside current goal")
                if not isinstance(current_input, str) or not current_input.strip():
                    raise ValueError("response input missing")
                response_feedback = next(
                    (u for u in self.units if u["id"] == response_question.get("feedback_ref")), None
                )
                if (
                    response_feedback is None
                    or response_feedback["goal"] != plan.goal_ref
                    or response_feedback["role"] not in {"comparison", "correction"}
                ):
                    raise ValueError("question feedback missing or outside current goal")
            if plan.act == "correct":
                if not isinstance(current_input, str) or plan.claim_quote not in current_input:
                    raise ValueError("claim quote is not in actual input")
                unit = next((u for u in self.units if u["id"] == str(plan.correction_ref)), None)
                if (
                    unit is None
                    or unit["goal"] != plan.goal_ref
                    or unit["role"] not in {"correction", "comparison"}
                ):
                    raise ValueError("correction reference outside proposed goal")
                chosen_correction = unit
                claim_binding = {
                    "quote": plan.claim_quote,
                    "correction_ref": str(plan.correction_ref),
                    "semantic_approval": False,
                    "basis": "exact substring of actual current input; not an entailment verdict",
                }
        if plan.act == "finish":
            return {
                "candidate_text": "¿Quieres terminar la inspección? /salir la cierra sin afectar "
                "sesiones de participante.",
                "publication_allowed": False,
                "profile": "controlled_draft_preview",
            }, state
        if plan.act == "clarify":
            if getattr(plan, "scope_limit", False):
                question = (
                    "Esta consulta queda fuera del catálogo de borradores disponible. "
                    "Podemos concretar una duda sobre los requisitos o las técnicas de prueba "
                    "incluidas en las fuentes; no dispongo aquí de una explicación respaldada "
                    "para la consulta actual."
                )
            elif plan.goal_ref is None:
                question = "¿Sobre qué concepto o fragmento concreto quieres que trabajemos?"
            else:
                goal = next((g for g in self.goals if g["id"] == plan.goal_ref), None)
                if goal is None:
                    raise ValueError("unknown goal")
                question = f"Sobre {goal['title']}, ¿qué parte de la distinción quieres aclarar?"
            return {
                "candidate_text": question,
                "publication_allowed": False,
                "profile": "controlled_draft_preview",
            }, state
        if plan.goal_ref not in {g["id"] for g in self.goals}:
            raise ValueError("unknown goal")
        if plan.act == "rephrase" and state.current_goal and plan.goal_ref != state.current_goal:
            raise ValueError("rephrase must preserve current referent")
        if plan.act == "rephrase" and state.support_step >= 3:
            return {
                "candidate_text": "No dispongo de otra estrategia en estos borradores. Podemos "
                "volver a la fuente o concretar una duda distinta; no se acredita "
                "comprensión.",
                "publication_allowed": False,
                "profile": "controlled_draft_preview",
                "reason": "support_limit",
            }, state
        roles = {
            "explain": ["definition", "cause", "process"],
            "rephrase": ["rephrase", "example", "question"],
            "example": ["definition", "example", "question"],
            "comparison": ["comparison", "example", "question"],
            "ask": ["question"],
            "correct": ["correction", "rephrase", "question"],
            "respond": ["comparison"],
        }[plan.act]
        if plan.act == "rephrase" and state.support_step >= 1:
            roles = ["comparison", "example", "question"]
        if plan.act == "rephrase" and state.support_step >= 2:
            roles = ["process", "question"]
        selected = [
            next(u for u in self.units if u["goal"] == plan.goal_ref and u["role"] == role) for role in roles
        ]
        if chosen_correction is not None:
            selected[0] = chosen_correction
        if response_feedback is not None:
            selected[0] = response_feedback
        if any(u["review_status"] != "pending" for u in selected):
            raise ValueError("draft status changed; this is not participant authority")
        text = ("Hola. " if plan.greet else "") + " ".join(u["draft_content"] for u in selected)
        if plan.act == "respond":
            text = (
                "Retomo tu respuesta a la pregunta pendiente. Para revisarla, contrasta esta distinción: "
                + text
            )
        if state.current_goal and state.current_goal != plan.goal_ref:
            text = (
                "Pasamos a " + next(g["title"] for g in self.goals if g["id"] == plan.goal_ref) + ". " + text
            )
        deferred = list(state.deferred_questions)
        if state.pending_question_id and state.current_goal != plan.goal_ref:
            deferred.append(state.pending_question_id)
        question = next((u["id"] for u in selected if u["role"] == "question"), None)
        if question is None and state.current_goal == plan.goal_ref and plan.act != "respond":
            question = state.pending_question_id
        sources = []
        for unit in selected:
            for ref in unit["source_refs"]:
                if ref not in sources:
                    sources.append(ref)
        next_state = DraftState(
            plan.goal_ref,
            question,
            [u["id"] for u in selected],
            (
                min(3, state.support_step + 1)
                if plan.act == "rephrase"
                else state.support_step if state.current_goal == plan.goal_ref else 0
            ),
            deferred[-10:],
            last_response_question_id=(
                state.pending_question_id if plan.act == "respond" else state.last_response_question_id
            ),
            comparison_goal_ref=(
                state.comparison_goal_ref
                if plan.act == "respond" and state.current_goal == plan.goal_ref
                else None
            ),
        )
        return {
            "candidate_text": text,
            "unit_ids": [u["id"] for u in selected],
            "source_refs": sources,
            "publication_allowed": False,
            "human_review": "pending",
            "profile": "controlled_draft_preview",
            "provider": "technically_authored_draft_renderer; semantic plan proposed separately",
            "claim_binding": claim_binding,
            "response_binding": (
                {
                    "question_id": state.pending_question_id,
                    "semantic_assessment": "not_assessed",
                    "feedback_unit_id": response_feedback["id"],
                }
                if response_question is not None
                else None
            ),
        }, next_state

    def _render_relation(self, plan, state, current_input):
        pair = frozenset([plan.goal_ref, plan.comparison_goal_ref])
        relation = next(
            (r for r in self.relations if frozenset([r["primary_goal"], r["secondary_goal"]]) == pair), None
        )
        if relation is None:
            raise ValueError("no authored relation for proposed goals")
        prior = {g for g in [state.current_goal, state.comparison_goal_ref] if g is not None}
        if plan.act == "rephrase" and prior and (not prior <= pair or len(prior) == 2 and prior != pair):
            raise ValueError("relation rephrase must preserve referents")
        if plan.act == "rephrase" and state.support_step >= 3:
            return {
                "candidate_text": (
                    "No hay otra estrategia preparada para esta relación. "
                    "Podemos revisar la fuente o concretar otra duda."
                ),
                "publication_allowed": False,
                "profile": "controlled_draft_preview",
                "reason": "support_limit",
            }, state
        if plan.act == "correct":
            if plan.correction_ref is None or str(plan.correction_ref) != relation["definition_ref"]:
                raise ValueError("correction must bind the authored relation")
            if not isinstance(current_input, str) or plan.claim_quote not in current_input:
                raise ValueError("relation claim is not in actual input")
        if plan.act == "ask":
            keys = ["question_ref"]
        elif plan.act == "rephrase":
            keys = (
                ["rephrase_ref", "example_ref", "question_ref"]
                if state.support_step == 0
                else (
                    ["definition_ref", "example_ref", "question_ref"]
                    if state.support_step == 1
                    else ["rephrase_ref", "question_ref"]
                )
            )
        else:
            keys = ["definition_ref", "example_ref", "question_ref"]
        selected = [next(u for u in self.units if u["id"] == relation[key]) for key in keys]
        if any(u["review_status"] != "pending" for u in selected):
            raise ValueError("relation unit status changed")
        title = {g["id"]: g["title"] for g in self.goals}
        text = (
            ("Hola. " if plan.greet else "")
            + "Contraste entre "
            + title[relation["primary_goal"]]
            + " y "
            + title[relation["secondary_goal"]]
            + ". "
        )
        text += " ".join(u["draft_content"] for u in selected)
        sources = []
        for u in selected:
            for ref in u["source_refs"]:
                if ref not in sources:
                    sources.append(ref)
        deferred = list(state.deferred_questions)
        if state.pending_question_id and prior != pair:
            deferred.append(state.pending_question_id)
        after = DraftState(
            current_goal=relation["primary_goal"],
            comparison_goal_ref=relation["secondary_goal"],
            pending_question_id=relation["question_ref"],
            last_unit_ids=[u["id"] for u in selected],
            support_step=(
                min(3, state.support_step + 1)
                if plan.act == "rephrase"
                else state.support_step if prior == pair else 0
            ),
            deferred_questions=deferred[-10:],
            last_response_question_id=state.last_response_question_id,
        )
        return {
            "candidate_text": text,
            "unit_ids": after.last_unit_ids,
            "source_refs": sources,
            "relation_ref": relation["id"],
            "active_goal_refs": [relation["primary_goal"], relation["secondary_goal"]],
            "publication_allowed": False,
            "human_review": "pending",
            "profile": "controlled_draft_preview",
            "provider": "technically_authored_relation_renderer; semantic plan proposed separately",
        }, after
