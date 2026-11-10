"""V2 checks individual solution clauses; V1 overlap contract remains unchanged."""

from uuid import uuid4

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.solution_non_disclosure_verifier_agent import SolutionNonDisclosureVerifierAgent


@pytest.mark.parametrize(
    "candidate",
    [
        "La respuesta documentada es 100 grados Celsius.",
        "A presión atmosférica, el agua hierve aproximadamente a 100 grados Celsius.",
    ],
)
async def test_solution_is_not_diluted_by_other_reviewed_answers(candidate):
    result = await SolutionNonDisclosureVerifierAgent().execute(
        AgentRequest(
            session_id=uuid4(),
            turn_id=uuid4(),
            input={
                "dialogue_schema_version": 2,
                "question_text": candidate,
                "internal_expected_answers": [
                    "A presión atmosférica, el agua hierve aproximadamente a 100 grados Celsius.",
                    "La condición del entorno acompaña a la magnitud.",
                    "El material desarrolla un ejemplo y un contraste distintos.",
                ],
            },
        ),
        CancellationToken(),
    )
    assert result.status == "ok" and result.output["verdict"] == "block"


@pytest.mark.parametrize("answers", [None, [], [""], [False]])
async def test_no_valid_solution_set_does_not_approve_hint(answers):
    result = await SolutionNonDisclosureVerifierAgent().execute(
        AgentRequest(
            session_id=uuid4(),
            turn_id=uuid4(),
            input={
                "dialogue_schema_version": 2,
                "question_text": "una pista",
                "internal_expected_answers": answers,
            },
        ),
        CancellationToken(),
    )
    assert result.status != "ok"


@pytest.mark.parametrize(
    "question,verdict",
    [
        ("¿Qué condiciones necesitas declarar para justificar una temperatura de ebullición?", "approved"),
        ("¿La temperatura de ebullición depende de la presión?", "block"),
    ],
)
async def test_shared_topic_is_distinct_from_echoing_documented_predicate(question, verdict):
    result = await SolutionNonDisclosureVerifierAgent().execute(
        AgentRequest(
            session_id=uuid4(),
            turn_id=uuid4(),
            input={
                "dialogue_schema_version": 2,
                "question_text": question,
                "internal_expected_answers": ["La temperatura de ebullición depende de la presión."],
            },
        ),
        CancellationToken(),
    )
    assert result.status == "ok" and result.output["verdict"] == verdict
