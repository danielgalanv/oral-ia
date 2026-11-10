"""T107 reproduction: the current turn text must cross the generation data boundary."""

from __future__ import annotations

import asyncio
import uuid

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.response_generator_agent import ResponseGeneratorAgent
from oralia.infrastructure.generation.generation_port import GenerationOutcome, GenerationRequest
from oralia.infrastructure.generation.ollama_adapter import _build_user_content

_EVIDENCE = [
    {
        "fragment_id": "fragment-1",
        "text": "La fotosíntesis transforma energía luminosa.",
        "document_id": "document-1",
        "document_version": 1,
    }
]


class _CapturingGenerationPort:
    def __init__(self) -> None:
        self.requests = []

    async def generate(self, request):
        self.requests.append(request)
        return GenerationOutcome(ok=True, text="respuesta", adapter="deterministic")


def test_distinct_turn_input_reaches_generation_request_as_distinct_data() -> None:
    capture = _CapturingGenerationPort()
    agent = ResponseGeneratorAgent(primary=capture)
    inputs = ("¿Qué transforma la luz?", "¿Dónde ocurre la fotosíntesis?")

    for current_input in inputs:
        request = AgentRequest(
            session_id=uuid.uuid4(),
            turn_id=uuid.uuid4(),
            input={
                "purpose": "explicacion",
                "input_text": current_input,
                "evidence": _EVIDENCE,
                "concepts_addressed": [],
                "general_knowledge_allowed": False,
            },
        )
        asyncio.run(agent.execute(request, CancellationToken()))

    assert len(capture.requests) == 2
    if "student_input" not in capture.requests[0].__class__.model_fields:
        assert capture.requests[0] == capture.requests[1]
    assert [request.student_input for request in capture.requests] == list(inputs)


def test_student_input_is_delimited_only_in_ollama_user_content() -> None:
    first = GenerationRequest(
        purpose="explicacion",
        instruction="Instrucción fija",
        student_input="¿Qué transforma la luz?",
    )
    second = first.model_copy(update={"student_input": "¿Dónde ocurre?"})

    first_content = _build_user_content(first)
    second_content = _build_user_content(second)

    assert first.instruction == second.instruction == "Instrucción fija"
    assert "<pregunta_actual>¿Qué transforma la luz?</pregunta_actual>" in first_content
    assert "<pregunta_actual>¿Dónde ocurre?</pregunta_actual>" in second_content
    assert first_content != second_content

