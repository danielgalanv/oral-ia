"""Independent positive and negative controls for the bounded opt-in verifier."""

from uuid import uuid4

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.coherence_propositions import compare, repeated
from oralia.domain.agents.coherence_verifier_agent import CoherenceVerifierAgent


@pytest.mark.parametrize(
    "proposal,source",
    [
        ("El agua no contiene moléculas.", "El agua contiene moléculas."),
        ("La media de la serie A es 9.", "La media de la serie A es 6."),
        ("La mediana de la serie A es seis.", "La mediana de la serie A es tres."),
        (
            "El agua no hierve a presión atmosférica.",
            "El agua hierve a presión atmosférica.",
        ),
    ],
)
def test_same_property_and_scope_rejects_real_conflict(proposal, source):
    conflicts, uncertain = compare(proposal, [source])
    assert conflicts
    assert not uncertain


@pytest.mark.parametrize(
    "proposal,source",
    [
        ("La mediana de la serie B es 6.", "La mediana de la serie A es 3."),
        (
            "El agua no hierve a menor presión.",
            "El agua hierve a presión atmosférica.",
        ),
        ("El agua no cambia de identidad.", "El agua contiene moléculas."),
        ("La validación no guarda registros.", "La validación comprueba registros."),
    ],
)
def test_other_scope_or_predicate_is_not_a_contradiction(proposal, source):
    assert compare(proposal, [source]) == ([], [])


def test_missing_condition_requests_clarification_instead_of_inventing_conflict():
    conflicts, uncertain = compare("La mediana es 6.", ["La mediana de la serie A es 3."])
    assert not conflicts
    assert uncertain


def test_repetition_compares_actual_clauses_not_shared_topic_words():
    source = "El agua contiene moléculas. El agua cambia de estado."
    assert repeated(source, [source])
    assert not repeated("El agua contiene moléculas. El agua hierve.", [source])
    assert not repeated(source, [])


@pytest.mark.parametrize(
    "text",
    [
        "El agua puede hervir a otra temperatura. Este texto no permite asignar una temperatura concreta.",
        "La serie B es cinco, cinco, seis, seis y ocho; su rango es tres segundos.",
    ],
)
def test_modal_complements_and_observation_lists_do_not_contradict_themselves(text):
    assert compare(text, [text]) == ([], [])


def test_nominal_object_is_not_a_second_grounding_assertion():
    from oralia.domain.agents.grounding_verifier_agent import _split_into_clauses

    assert _split_into_clauses("La densidad relaciona masa y volumen.") == [
        "La densidad relaciona masa y volumen."
    ]
    assert len(_split_into_clauses("La validación comprueba y no guarda.")) == 2
    assert _split_into_clauses("A y B tienen cinco duraciones.") == ["A y B tienen cinco duraciones."]
    assert len(_split_into_clauses("A dura 20 minutos y B dura 100 minutos.")) == 2


@pytest.mark.parametrize("intentional_repeat", [False, True])
async def test_actual_verifier_never_exempts_a_conflicting_candidate_copy(intentional_repeat):
    text = "La media de la serie A es 9."
    result = await CoherenceVerifierAgent().execute(
        AgentRequest(
            session_id=uuid4(),
            turn_id=uuid4(),
            input={
                "proposal_text": text,
                "prior_statements": [text],
                "active_sources": [text, "La media de la serie A es 6."],
                "dialogue_schema_version": 3,
                "structural_progress": True,
                "intentional_repeat": intentional_repeat,
            },
        ),
        CancellationToken(),
    )
    assert result.output["verdict"] == "block"
    assert "contradiccion" in result.output["incident_types"]


async def test_actual_verifier_missing_condition_cannot_be_approved():
    result = await CoherenceVerifierAgent().execute(
        AgentRequest(
            session_id=uuid4(),
            turn_id=uuid4(),
            input={
                "proposal_text": "La mediana es 6.",
                "active_sources": ["La mediana de la serie A es 3."],
                "dialogue_schema_version": 3,
                "structural_progress": True,
            },
        ),
        CancellationToken(),
    )
    assert result.output["verdict"] == "reformulate"
    assert result.output["incident_types"] == ["condiciones_no_comparables"]
