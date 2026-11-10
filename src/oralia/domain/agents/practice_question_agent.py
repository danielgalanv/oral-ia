"""PracticeQuestionAgent (contracts/self-study-agents.md) — role `generator`. Derives a
practice question from evidence/objective/concepts/session history — never grades the
student's answer (FR-014); delegates to `GenerationPort` with the same primary→reserve
sequence as `ResponseGeneratorAgent` (research.md §1), no third wrapper class."""

from __future__ import annotations

from oralia.domain.agents.agent import AgentContractSchema
from oralia.domain.agents.agent_contract import AgentRequest, AgentResult, CancellationToken
from oralia.infrastructure.generation.deterministic_adapter import DeterministicGenerationAdapter
from oralia.infrastructure.generation.generation_port import (
    EvidenceItem,
    GenerationConstraints,
    GenerationError,
    GenerationPort,
    GenerationRequest,
)
from oralia.infrastructure.generation.ollama_adapter import OllamaGenerationAdapter

CONTRACT = AgentContractSchema(
    agent_id="practice-question-agent",
    version="1.0.0",
    purpose=(
        "Genera una pregunta de práctica derivada de objetivos/conceptos/evidencia/"
        "historial (FR-011, FR-012)"
    ),
    input_schema_ref="contracts/self-study-agents.md#PracticeQuestionAgent.input",
    output_schema_ref="contracts/self-study-agents.md#PracticeQuestionAgent.output",
    timeout_ms=8000,
    confidence_semantics=(
        "no aplica — la no-revelación la evalúa SolutionNonDisclosureVerifierAgent " "por separado"
    ),
    success_criteria=["produce question_text/internal_expected_answer sin calificar al estudiante"],
    trace_fields=["question_type", "adapter", "fallback_used"],
)

# data-model.md / contracts/self-study-agents.md: 5 canonical question_type values.
QUESTION_TYPES = ("explicacion", "aplicacion", "comparacion", "justificacion", "deteccion_errores")

_DIFFICULTY_HINT = "media"


class PracticeQuestionAgent:
    contract = CONTRACT

    def __init__(
        self,
        *,
        primary: GenerationPort | None = None,
        secondary: GenerationPort | None = None,
    ) -> None:
        self._primary = primary or OllamaGenerationAdapter()
        self._secondary = secondary or DeterministicGenerationAdapter()

    async def execute(self, request: AgentRequest, cancellation: CancellationToken) -> AgentResult:
        data = request.input
        evidence = [EvidenceItem(**item) for item in data.get("evidence", [])]
        concepts = list(data.get("concepts", []))
        # FR-011a: previous_questions MUST already be filtered by session_id by the
        # caller — this agent only reads it to avoid repeating the same question_type.
        previous_questions = list(data.get("previous_questions", []))
        reveals_solution = bool(data.get("reveals_solution", False))

        question_type = QUESTION_TYPES[len(previous_questions) % len(QUESTION_TYPES)]

        gen_request = GenerationRequest(
            purpose="pregunta_practica",
            instruction=(
                "Eres un asistente de apoyo docente. Genera una única pregunta de "
                f"práctica de tipo '{question_type}' sobre los conceptos indicados, "
                "usando únicamente el contenido de las etiquetas <evidencia> como "
                "fuente. No asignes notas ni evalúes al estudiante. Responde en "
                "español."
            ),
            evidence=evidence,
            concepts_addressed=concepts,
            general_knowledge_allowed=False,
            constraints=GenerationConstraints(reveal_solution=reveals_solution),
        )

        try:
            outcome = await self._primary.generate(gen_request)
            fallback_used = False
        except (GenerationError, TimeoutError, ConnectionError):
            outcome = await self._secondary.generate(gen_request)
            fallback_used = True

        internal_expected_answer = None if reveals_solution else outcome.internal_expected_answer

        return AgentResult(
            status="ok",
            output={
                "question_type": question_type,
                "question_text": outcome.text,
                "internal_expected_answer": internal_expected_answer,
                "difficulty_hint": _DIFFICULTY_HINT,
                "reveals_solution": reveals_solution,
                "generation_trace": {
                    "adapter": outcome.adapter,
                    "model": outcome.model,
                    "fallback_used": fallback_used,
                },
            },
            confidence=None,
            trace={
                "question_type": question_type,
                "adapter": outcome.adapter,
                "fallback_used": fallback_used,
            },
        )
