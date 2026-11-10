"""Safe fallback agent (FR-018): always succeeds, never touches CognitiveState directly —
used by agency_composer when a primary step times out or errors."""

from __future__ import annotations

from oralia.domain.agents.agent import AgentContractSchema
from oralia.domain.agents.agent_contract import AgentRequest, AgentResult, CancellationToken

CONTRACT = AgentContractSchema(
    agent_id="safe-fallback",
    version="1.0.0",
    purpose="Respuesta segura y determinista cuando un paso previo falla o excede su timeout",
    input_schema_ref="AgentRequest",
    output_schema_ref="AgentResult{output.text: str}",
    timeout_ms=500,
    confidence_semantics="1.0 — respuesta fija, no una estimación",
    success_criteria=["siempre produce una salida válida, incluso sin datos del paso previo"],
    trace_fields=[],
)

SAFE_FALLBACK_TEXT = (
    "Ha ocurrido un problema técnico al procesar tu mensaje. Puedes intentarlo de nuevo "
    "o finalizar la sesión cuando quieras."
)


class SafeFallbackAgent:
    contract = CONTRACT

    async def execute(self, request: AgentRequest, cancellation: CancellationToken) -> AgentResult:
        return AgentResult(status="ok", output={"text": SAFE_FALLBACK_TEXT}, confidence=1.0, trace={})
