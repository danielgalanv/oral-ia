"""Deterministic Interpreter agent (research.md §2) — no LLM in this feature.

Implements the same async Executable protocol a real LLM-backed interpreter will use
later (Constitution Principio II/XI: replaceable behind a stable contract).
"""

from __future__ import annotations

from oralia.domain.agents.agent import AgentContractSchema
from oralia.domain.agents.agent_contract import AgentRequest, AgentResult, CancellationToken

CONTRACT = AgentContractSchema(
    agent_id="interpreter-deterministic",
    version="1.0.0",
    purpose="Interpretación determinista del turno (sin LLM) — research.md §2",
    input_schema_ref="AgentRequest{input.text: str}",
    output_schema_ref="AgentResult{output.intent: str, output.echo: str}",
    timeout_ms=2000,
    confidence_semantics="1.0 siempre — heurística determinista, no una estimación probabilística",
    success_criteria=["produce intent y echo a partir de input.text"],
    trace_fields=["intent"],
)

_CLARIFICATION_MARKERS = ("?", "no entiendo", "no se", "no sé")


class DeterministicInterpreter:
    contract = CONTRACT

    async def execute(self, request: AgentRequest, cancellation: CancellationToken) -> AgentResult:
        text = str(request.input.get("text", "")).strip()
        if not text:
            intent = "acknowledge_missing_info"
        elif any(marker in text.lower() for marker in _CLARIFICATION_MARKERS):
            intent = "clarify"
        else:
            intent = "respond"

        return AgentResult(
            status="ok",
            output={"intent": intent, "echo": text},
            confidence=1.0,
            trace={"intent": intent},
        )
