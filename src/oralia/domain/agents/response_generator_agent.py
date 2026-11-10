"""ResponseGeneratorAgent (research.md §1 of Feature 003) — role `generator`. Delegates
to `GenerationPort`: tries the primary (`OllamaGenerationAdapter`) then the reserve
(`DeterministicGenerationAdapter`) inside this same agent — no third wrapper class
(research.md §1). If the reserve also fails, the exception propagates; `run_with_deadline`
(Feature 001, unchanged) converts it into a failed step, and `execute_agency`'s
`fallback_step` (Feature 001, unchanged) provides the final safety net (research.md §2).
"""

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
    agent_id="response-generator",
    version="1.0.0",
    purpose="Genera una respuesta fundamentada u otro contenido derivado de evidencia (FR-008)",
    input_schema_ref="contracts/self-study-agents.md#ResponseGeneratorAgent.input",
    output_schema_ref="contracts/self-study-agents.md#ResponseGeneratorAgent.output",
    timeout_ms=8000,
    confidence_semantics="no aplica — la fundamentación la evalúa GroundingVerifierAgent por separado",
    success_criteria=["produce proposal_text a partir de evidence y purpose"],
    trace_fields=["adapter", "model", "fallback_used"],
)

_INSTRUCTIONS: dict[str, str] = {
    "explicacion": (
        "Eres un asistente de apoyo docente. Responde a la duda del estudiante usando "
        "únicamente el contenido de las etiquetas <evidencia> como fuente. Si la "
        "evidencia no es suficiente, dilo explícitamente en vez de inventar información. "
        "No asignes notas ni emitas juicios sobre el estudiante. Responde en español, de "
        "forma clara y concisa."
    ),
    "explicacion_progresiva": (
        "Eres un asistente de apoyo docente. Explica el concepto de forma progresiva, en "
        "un paso pequeño y verificable a la vez, usando únicamente el contenido de las "
        "etiquetas <evidencia>. No asignes notas. Responde en español."
    ),
    "ejemplo": (
        "Eres un asistente de apoyo docente. Genera un ejemplo distinto de cualquier "
        "explicación previa, fundamentado únicamente en el contenido de las etiquetas "
        "<evidencia>. No asignes notas. Responde en español."
    ),
    "comparacion": (
        "Eres un asistente de apoyo docente. Compara los elementos solicitados usando "
        "únicamente el contenido de las etiquetas <evidencia>. No asignes notas. "
        "Responde en español."
    ),
    "estructura_exposicion": (
        "Eres un asistente de apoyo docente. Ayuda al estudiante a estructurar una "
        "exposición sobre el tema, usando únicamente el contenido de las etiquetas "
        "<evidencia>. No asignes notas ni evalúes al estudiante. Responde en español."
    ),
    "resumen": (
        "Eres un asistente de apoyo docente. Resume el concepto usando únicamente el "
        "contenido de las etiquetas <evidencia>. No asignes notas. Responde en español."
    ),
}
_DEFAULT_PURPOSE = "explicacion"


class ResponseGeneratorAgent:
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
        purpose = str(data.get("purpose", _DEFAULT_PURPOSE))
        evidence = [EvidenceItem(**item) for item in data.get("evidence", [])]
        gen_request = GenerationRequest(
            purpose=purpose,  # type: ignore[arg-type]
            instruction=_INSTRUCTIONS.get(purpose, _INSTRUCTIONS[_DEFAULT_PURPOSE]),
            student_input=str(data.get("student_input", data.get("input_text", ""))),
            evidence=evidence,
            concepts_addressed=list(data.get("concepts_addressed", [])),
            general_knowledge_allowed=bool(data.get("general_knowledge_allowed", False)),
            constraints=GenerationConstraints(
                material_excerpt_version=data.get("material_excerpt_version", 1)
            ),
        )

        try:
            outcome = await self._primary.generate(gen_request)
            fallback_used = False
        except (GenerationError, TimeoutError, ConnectionError):
            outcome = await self._secondary.generate(gen_request)
            fallback_used = True

        return AgentResult(
            status="ok",
            output={
                "proposal_text": outcome.text,
                "generation_trace": {
                    "adapter": outcome.adapter,
                    "model": outcome.model,
                    "fallback_used": fallback_used,
                },
            },
            confidence=None,
            trace={"adapter": outcome.adapter, "fallback_used": fallback_used},
        )
