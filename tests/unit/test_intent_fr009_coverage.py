"""Parametrized/consolidated test: `StudyIntentInterpreterAgent` mapea correctamente las
6 solicitudes de FR-009 a la intención/modo esperado, sin ninguna intención adicional no
listada en spec.md — [Remediación E4/MEDIUM — FR-009]."""

from __future__ import annotations

import uuid

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.study_intent_interpreter import CANONICAL_MODES, StudyIntentInterpreterAgent

_FR009_PRIMARY_INTENTS = {
    "simpler_explanation",
    "example",
    "comparison",
    "topic_change",
    "finish",
    *CANONICAL_MODES,
    "doubt_resolution",  # fallback for unmatched free text
}


def _request(text: str):
    return AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        input={"text": text, "enabled_modes": list(CANONICAL_MODES), "current_mode": None, "concepts_addressed": []},
    )


@pytest.mark.parametrize(
    ("text", "expected_primary_intent", "expected_requested_mode"),
    [
        ("Explícamelo de forma más sencilla, no lo entiendo", "simpler_explanation", None),
        ("Dame un ejemplo de esto", "example", None),
        ("Compara los dos conceptos", "comparison", None),
        ("Ponme una pregunta de práctica", "practice_questions", "practice_questions"),
        ("Cambiemos de tema, hablemos de otra cosa", "topic_change", None),
        ("Quiero terminar la sesión", "finish", None),
    ],
)
async def test_fr009_six_requests_map_to_expected_intent(
    text: str, expected_primary_intent: str, expected_requested_mode: str | None
):
    agent = StudyIntentInterpreterAgent()
    result = await agent.execute(_request(text), CancellationToken())
    assert result.output["primary_intent"] == expected_primary_intent
    assert result.output["requested_mode"] == expected_requested_mode
    assert result.output["primary_intent"] in _FR009_PRIMARY_INTENTS, (
        "primary_intent MUST be one of the intents explicitly listed in spec.md (FR-009) "
        "or a canonical mode — never an invented intention"
    )
