"""Contract test for ResponseGeneratorAgent — determinista, sin Ollama (research.md §1)."""

from __future__ import annotations

import uuid

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.response_generator_agent import ResponseGeneratorAgent
from oralia.infrastructure.generation.generation_port import GenerationOutcome


def _request(purpose: str = "explicacion", evidence: list[dict] | None = None):
    return AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        input={
            "purpose": purpose,
            "evidence": evidence
            or [{"fragment_id": "f1", "text": "El sol es una estrella.", "document_id": "d1", "document_version": 1}],
            "concepts_addressed": [],
            "general_knowledge_allowed": False,
        },
    )


class _FakePrimary:
    async def generate(self, request):
        return GenerationOutcome(
            ok=True, text="respuesta del modelo", adapter="ollama", model="fake-model", latency_ms=1
        )


class _FailingAdapter:
    async def generate(self, request):
        raise RuntimeError("boom")


@pytest.mark.contract
async def test_output_shape_is_complete():
    agent = ResponseGeneratorAgent()
    result = await agent.execute(_request(), CancellationToken())
    assert result.status == "ok"
    assert "proposal_text" in result.output
    assert result.output["proposal_text"]
    trace = result.output["generation_trace"]
    for key in ("adapter", "model", "fallback_used"):
        assert key in trace


@pytest.mark.contract
async def test_falls_back_to_deterministic_without_ollama_configured():
    """No ORALIA_OLLAMA_MODEL configured in the test environment — the agent MUST
    still produce a valid answer via DeterministicGenerationAdapter (research.md §1)."""
    agent = ResponseGeneratorAgent()
    result = await agent.execute(_request(), CancellationToken())
    assert result.output["generation_trace"]["adapter"] == "deterministic"
    assert result.output["generation_trace"]["fallback_used"] is True


@pytest.mark.contract
async def test_uses_primary_when_available():
    agent = ResponseGeneratorAgent(primary=_FakePrimary())
    result = await agent.execute(_request(), CancellationToken())
    assert result.output["generation_trace"]["adapter"] == "ollama"
    assert result.output["generation_trace"]["fallback_used"] is False
    assert result.output["proposal_text"] == "respuesta del modelo"


@pytest.mark.contract
async def test_both_adapters_failing_propagates_exception():
    """research.md §2: a secondary failure MUST propagate — the generic execute_agency
    fallback_step is the last resort, not a second try/except inside this agent."""
    agent = ResponseGeneratorAgent(primary=_FailingAdapter(), secondary=_FailingAdapter())
    with pytest.raises(RuntimeError):
        await agent.execute(_request(), CancellationToken())
