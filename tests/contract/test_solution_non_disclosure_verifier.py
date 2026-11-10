"""Contract test for SolutionNonDisclosureVerifierAgent (approved/block), umbral y
configuración independientes de GroundingVerifierAgent (research.md §4)."""

from __future__ import annotations

import uuid

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.solution_non_disclosure_verifier_agent import SolutionNonDisclosureVerifierAgent


def _request(question_text: str, internal_expected_answer: str, attempt_number: int = 1):
    return AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        input={
            "question_text": question_text,
            "internal_expected_answer": internal_expected_answer,
            "reveals_solution": False,
            "attempt_number": attempt_number,
        },
    )


@pytest.mark.contract
async def test_output_shape_is_complete():
    agent = SolutionNonDisclosureVerifierAgent()
    result = await agent.execute(
        _request("¿Qué es la fotosíntesis?", "conversión de luz en energía"), CancellationToken()
    )
    assert result.status == "ok"
    assert "verdict" in result.output
    assert "overlap_score" in result.output
    assert result.output["verdict"] in ("approved", "block")


@pytest.mark.contract
async def test_low_overlap_is_approved():
    agent = SolutionNonDisclosureVerifierAgent()
    result = await agent.execute(
        _request("¿Qué proceso permite a las plantas crecer?", "conversión de luz solar en energía química"),
        CancellationToken(),
    )
    assert result.output["verdict"] == "approved"


@pytest.mark.contract
async def test_high_overlap_with_expected_answer_is_blocked():
    agent = SolutionNonDisclosureVerifierAgent()
    expected_answer = "conversión fotosíntesis energía química clorofila luz solar plantas"
    result = await agent.execute(
        _request(
            "Explica la conversión fotosíntesis energía química clorofila luz solar plantas.",
            expected_answer,
        ),
        CancellationToken(),
    )
    assert result.output["verdict"] == "block"


@pytest.mark.contract
async def test_threshold_is_independent_from_grounding_verifier(monkeypatch: pytest.MonkeyPatch):
    from oralia.infrastructure.generation import config

    monkeypatch.setenv("ORALIA_DISCLOSURE_OVERLAP_THRESHOLD", "0.9")
    assert config.get_disclosure_overlap_threshold() == pytest.approx(0.9)

    agent = SolutionNonDisclosureVerifierAgent()
    # Enough overlap to block at the default 0.3 threshold, not at 0.9.
    result = await agent.execute(
        _request("fotosíntesis energía luz", "fotosíntesis energía luz clorofila plantas"),
        CancellationToken(),
    )
    assert result.output["verdict"] == "approved"


@pytest.mark.contract
@pytest.mark.parametrize(
    ("question_text", "expected_answer", "expected_verdict"),
    [
        ("¿Cuál es el resultado? La respuesta es 4.", "4", "block"),
        ("¿Cuánto vale la constante de gravitación?", "9.8", "approved"),
        ("Resuelve la ecuación x=3 para la variable dada.", "x=3", "block"),
        (
            "Un grupo tiene 4 asignaturas optativas; ¿cuántas ha aprobado el estudiante medio?",
            "4",
            "block",
        ),
        (
            "Explica por qué la presión atmosférica es menor a mayor altitud.",
            "porque la presión atmosférica es menor",
            "block",
        ),
        (
            "¿Es correcto que la presión atmosférica NO es menor a mayor altitud?",
            "porque la presión atmosférica es menor",
            "block",
        ),
        ("¿Qué fracción de 12 es 4?", "4", "block"),
    ],
    ids=("N1", "N2", "N3", "N4", "T1", "C1", "V1"),
)
async def test_short_solution_acceptance_matrix(
    question_text: str,
    expected_answer: str,
    expected_verdict: str,
) -> None:
    agent = SolutionNonDisclosureVerifierAgent()
    result = await agent.execute(_request(question_text, expected_answer), CancellationToken())
    assert result.output["verdict"] == expected_verdict
