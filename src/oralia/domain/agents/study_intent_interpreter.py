"""StudyIntentInterpreterAgent (research.md §6 of Feature 003) — deterministic, keyword
heuristic. Detects the 5 canonical self-study modes, plus (T038, FR-009) the 5 remaining
sub-intentions that do not themselves switch `CognitiveState.mode` (the 6th FR-009
request, "pregunta de práctica", already resolves to `requested_mode=practice_questions`
via `_MODE_KEYWORDS`): `simpler_explanation`, `example`, `comparison`, `topic_change`,
`finish`."""

from __future__ import annotations

from oralia.domain.agents.agent import AgentContractSchema
from oralia.domain.agents.agent_contract import AgentError, AgentRequest, AgentResult, CancellationToken

CONTRACT = AgentContractSchema(
    agent_id="study-intent-interpreter",
    version="1.0.0",
    purpose=("Interpretación determinista de la intención del estudiante en autoestudio " "(FR-006, FR-009)"),
    input_schema_ref="contracts/self-study-agents.md#StudyIntentInterpreterAgent.input",
    output_schema_ref="contracts/self-study-agents.md#StudyIntentInterpreterAgent.output",
    timeout_ms=2000,
    confidence_semantics=("heurística determinista — 1.0 en coincidencia directa, 0.5 en fallback genérico"),
    success_criteria=["produce intent_hypotheses y requested_mode a partir de input.text"],
    trace_fields=["primary_intent", "requested_mode"],
)

CANONICAL_MODES = (
    "doubt_resolution",
    "guided_explanation",
    "practice_questions",
    "presentation_preparation",
    "concept_review",
)

_MODE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "practice_questions": (
        "pregunta de práctica",
        "preguntas de práctica",
        "ponme una pregunta",
        "practicar",
    ),
    "guided_explanation": (
        "paso a paso",
        "explicación guiada",
        "explicacion guiada",
        "guíame",
        "guiame",
    ),
    "presentation_preparation": (
        "preparar una exposición",
        "preparar exposicion",
        "exposición",
        "ensayar",
    ),
    "concept_review": ("repasar", "repaso", "revisión de conceptos", "revision de conceptos"),
}

# FR-009 sub-intentions that do not themselves switch `CognitiveState.mode` — checked
# before `_MODE_KEYWORDS` so a more specific sub-intent phrase (e.g. "un ejemplo más
# sencillo") is not shadowed by a generic mode keyword.
_SUB_INTENT_KEYWORDS: dict[str, tuple[str, ...]] = {
    "simpler_explanation": (
        "más sencillo",
        "mas sencillo",
        "más simple",
        "mas simple",
        "no lo entiendo",
        "más fácil",
        "mas facil",
    ),
    "example": ("un ejemplo", "dame un ejemplo", "pon un ejemplo", "ejemplo de esto"),
    "comparison": ("compara", "comparación", "comparacion", "diferencia entre", "en qué se diferencia"),
    "topic_change": ("cambiar de tema", "cambiemos de tema", "otro tema", "hablemos de otra cosa"),
    "finish": (
        "terminar la sesión",
        "terminar la sesion",
        "finalizar la sesión",
        "finalizar la sesion",
        "quiero acabar",
        "hemos terminado",
    ),
}


def _detect_sub_intent(text_lower: str) -> str | None:
    for intent, keywords in _SUB_INTENT_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            return intent
    return None


def _detect_mode(text_lower: str) -> str | None:
    for mode, keywords in _MODE_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            return mode
    return None


class StudyIntentInterpreterAgent:
    contract = CONTRACT
    semantic_contract = CONTRACT.model_copy(
        update={
            "version": "3.0.0",
            "purpose": "Proponer intención y referente semánticos, sin texto docente ni autoridad",
            "input_schema_ref": "specs/012-conversational-course-study/contracts/semantic-planning.md#input",
            "output_schema_ref": "specs/012-conversational-course-study/contracts/semantic-pla"
            "nning.md#output",
            "timeout_ms": 32000,
            "confidence_semantics": "propuesta no calibrada; no acredita permisos ni comprensión",
        }
    )

    def __init__(self, *, semantic_planner=None, semantic_version=1):
        if semantic_version not in {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}:
            raise ValueError("unknown semantic planning version")
        self._semantic_planner = semantic_planner
        self._semantic_version = semantic_version
        if semantic_planner is not None:
            self.contract = self.semantic_contract
            if semantic_version != 1:
                self.contract = self.semantic_contract.model_copy(
                    update={
                        "version": {
                            2: "3.3.0",
                            3: "4.0.0",
                            4: "5.1.0",
                            5: "6.0.0",
                            6: "7.0.1",
                            7: "8.0.0",
                            8: "8.1.0",
                            9: "8.2.0",
                            10: "8.3.0",
                        }[semantic_version],
                        "input_schema_ref": (
                            "specs/012-conversational-course-study/contracts/"
                            f"semantic-planning.md#input-v{semantic_version}"
                        ),
                        "output_schema_ref": (
                            "specs/012-conversational-course-study/contracts/semantic-planning.md#output-v2"
                        ),
                    }
                )

    async def _execute_semantic(self, request, cancellation):
        import asyncio

        if (
            self._semantic_planner is None
            or request.input.get("semantic_planning_version") != self._semantic_version
        ):
            return AgentResult(
                status="error",
                error=AgentError(
                    code="SEMANTIC_PLANNER_UNAVAILABLE",
                    message="No hay planificador semántico optativo configurado.",
                ),
            )
        if cancellation.is_cancelled():
            return AgentResult(status="cancelled")
        planned = asyncio.create_task(self._semantic_planner.plan(request, cancellation))
        cancelled = asyncio.create_task(cancellation.wait())
        try:
            done, _ = await asyncio.wait({planned, cancelled}, return_when=asyncio.FIRST_COMPLETED)
            if cancelled in done or cancellation.is_cancelled():
                planned.cancel()
                return AgentResult(status="cancelled")
            from oralia.domain.dialogue.contracts import SemanticStudyPlan, SemanticStudyPlanV2

            result = await planned
            plan_type = SemanticStudyPlanV2 if self._semantic_version != 1 else SemanticStudyPlan
            plan = plan_type.model_validate(result)
            return AgentResult(
                status="ok",
                output={"semantic_plan": plan.model_dump(mode="json"), "publication_authority": False},
                confidence=None,
                trace={"contract_version": self.contract.version, "semantic_plan_only": True},
            )
        except (ValueError, RuntimeError) as exc:
            return AgentResult(
                status="error", error=AgentError(code="INVALID_SEMANTIC_PLAN", message=type(exc).__name__)
            )
        finally:
            for task in [planned, cancelled]:
                if not task.done():
                    task.cancel()
            await asyncio.gather(planned, cancelled, return_exceptions=True)

    dialogue_contract = CONTRACT.model_copy(
        update={
            "version": "2.1.2",
            "input_schema_ref": "specs/010-guided-dialogue/contracts/dialogue.md#entrada-de-interpretación",
            "output_schema_ref": "specs/010-guided-dialogue/contracts/dialogue.md#salida",
            "success_criteria": ["produce acto conversacional sin conceder permisos ni modificar modo"],
            "trace_fields": ["schema_version", "primary_act", "reason_code"],
        }
    )

    async def execute(self, request: AgentRequest, cancellation: CancellationToken) -> AgentResult:
        if "semantic_planning_version" in request.input:
            return await self._execute_semantic(request, cancellation)
        if request.input.get("dialogue_schema_version") == 2:
            return self._execute_dialogue(request, cancellation)
        text = str(request.input.get("text", "")).strip()
        # `enabled_modes` (documented in the contract) is intentionally not consulted
        # here — mode validation/rejection against it is the compositor's
        # responsibility (T056), not this stateless interpreter's.
        current_mode = request.input.get("current_mode")

        if not text:
            return AgentResult(
                status="ok",
                output={
                    "intent_hypotheses": ["missing_input:1.00"],
                    "primary_intent": "missing_input",
                    "primary_confidence": 1.0,
                    "requested_mode": None,
                },
                confidence=1.0,
                trace={"primary_intent": "missing_input", "requested_mode": None},
            )

        text_lower = text.lower()
        detected_sub_intent = _detect_sub_intent(text_lower)
        detected_mode = _detect_mode(text_lower) if detected_sub_intent is None else None

        if detected_sub_intent is not None:
            primary_intent = detected_sub_intent
            confidence = 0.85
            requested_mode = None
        elif detected_mode is not None:
            primary_intent = detected_mode
            confidence = 0.85
            requested_mode = detected_mode
        else:
            # No specific-mode/sub-intent keyword matched. If a mode is already active
            # (`current_mode`), a plain follow-up utterance continues it — it MUST NOT
            # silently switch back to doubt_resolution every turn just because the text
            # didn't match a keyword (that would break continuity for
            # guided_explanation/practice_questions/etc., SC-005). Only a session's
            # first, unmatched turn (`current_mode` is null) defaults to
            # doubt_resolution, the most generic mode (research.md §6).
            primary_intent = current_mode if current_mode else "doubt_resolution"
            confidence = 0.6
            requested_mode = None if current_mode else "doubt_resolution"

        intent_hypotheses = [f"{primary_intent}:{confidence:.2f}"]
        if requested_mode is None and current_mode:
            intent_hypotheses.append(f"{current_mode}:{1 - confidence:.2f}")

        return AgentResult(
            status="ok",
            output={
                "intent_hypotheses": intent_hypotheses,
                "primary_intent": primary_intent,
                "primary_confidence": confidence,
                "requested_mode": requested_mode,
            },
            confidence=confidence,
            trace={"primary_intent": primary_intent, "requested_mode": requested_mode},
        )

    def _execute_dialogue(self, request: AgentRequest, cancellation: CancellationToken) -> AgentResult:
        from pydantic import ValidationError

        from oralia.domain.dialogue.contracts import DialogueContext
        from oralia.domain.dialogue.interpretation import interpret

        if cancellation.is_cancelled():
            return AgentResult(status="cancelled")
        try:
            context = DialogueContext.model_validate(request.input.get("dialogue_context") or {})
        except ValidationError:
            return AgentResult(
                status="error",
                error=AgentError(code="invalid_input", message="Contexto de diálogo inválido."),
            )
        act = interpret(
            str(request.input.get("text", "")),
            pending_question=context.pending_question_turn_id is not None,
            referents=context.candidate_referents,
        )
        legacy = {
            "rephrase": "simpler_explanation",
            "topic_switch": "topic_change",
            "example": "example",
            "comparison": "comparison",
            "finish": "finish",
        }.get(act.primary_act, request.input.get("current_mode") or "doubt_resolution")
        if act.requested_mode:
            legacy = act.requested_mode
        return AgentResult(
            status="ok",
            output={
                "dialogue_act": act.model_dump(mode="json"),
                "intent_hypotheses": [f"{legacy}:0.60"],
                "primary_intent": legacy,
                "primary_confidence": 0.6,
                "requested_mode": act.requested_mode,
            },
            confidence=0.6,
            trace={"schema_version": 2, "primary_act": act.primary_act, "reason_code": act.reason_code},
        )
