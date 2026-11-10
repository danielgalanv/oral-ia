"""Contract test for StudyIntentInterpreterAgent (Feature 003, remediación D1) —
contrato de entrada, formato de intent_hypotheses, requested_mode por modo canónico,
confidence, forma estructurada de salida, y entrada inválida/vacía."""

from __future__ import annotations

import re
import uuid

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.study_intent_interpreter import CANONICAL_MODES, StudyIntentInterpreterAgent

_HYPOTHESIS_RE = re.compile(r"^[a-z_]+:\d\.\d{2}$")


def _request(text: str, enabled_modes: list[str] | None = None, current_mode: str | None = None):
    return AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        input={
            "text": text,
            "enabled_modes": enabled_modes or list(CANONICAL_MODES),
            "current_mode": current_mode,
            "concepts_addressed": [],
        },
    )


@pytest.mark.contract
async def test_output_shape_is_complete():
    agent = StudyIntentInterpreterAgent()
    result = await agent.execute(_request("¿Qué es la fotosíntesis?"), CancellationToken())
    assert result.status == "ok"
    output = result.output
    for key in ("intent_hypotheses", "primary_intent", "primary_confidence", "requested_mode"):
        assert key in output


@pytest.mark.contract
async def test_intent_hypotheses_format():
    agent = StudyIntentInterpreterAgent()
    result = await agent.execute(_request("¿Qué es la fotosíntesis?"), CancellationToken())
    hypotheses = result.output["intent_hypotheses"]
    assert hypotheses, "intent_hypotheses MUST NOT be empty"
    for hypothesis in hypotheses:
        assert _HYPOTHESIS_RE.match(hypothesis), f"{hypothesis!r} does not match '{{intent}}:{{confidence:.2f}}'"


@pytest.mark.contract
async def test_primary_confidence_in_unit_interval():
    agent = StudyIntentInterpreterAgent()
    result = await agent.execute(_request("¿Qué es la fotosíntesis?"), CancellationToken())
    assert 0.0 <= result.output["primary_confidence"] <= 1.0


@pytest.mark.contract
@pytest.mark.parametrize(
    ("text", "expected_mode"),
    [
        ("¿Qué es la fotosíntesis?", "doubt_resolution"),
        ("Explícame paso a paso la fotosíntesis", "guided_explanation"),
        ("Ponme una pregunta de práctica", "practice_questions"),
        ("Quiero preparar una exposición sobre el tema", "presentation_preparation"),
        ("Quiero repasar los conceptos vistos", "concept_review"),
    ],
)
async def test_requested_mode_per_canonical_mode(text: str, expected_mode: str):
    agent = StudyIntentInterpreterAgent()
    result = await agent.execute(_request(text), CancellationToken())
    assert result.output["requested_mode"] == expected_mode
    assert result.output["primary_intent"] == expected_mode


@pytest.mark.contract
async def test_empty_text_is_recognized_without_exception():
    agent = StudyIntentInterpreterAgent()
    result = await agent.execute(_request(""), CancellationToken())
    assert result.status == "ok"
    assert result.output["primary_intent"] == "missing_input"
    assert result.output["requested_mode"] is None
