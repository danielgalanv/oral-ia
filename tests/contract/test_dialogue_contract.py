"""Versioned dialogue contracts; no output authorization is implied by intent."""

from uuid import uuid4

import pytest
from pydantic import ValidationError

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent
from oralia.domain.dialogue.contracts import DialogueAct, DialogueContext, ProposalPlan


@pytest.mark.parametrize(
    ("text", "act"),
    [
        ("hola", "greeting"),
        ("puedes repetir?", "repeat"),
        ("no entiendo, dilo de otra forma", "rephrase"),
        ("no sé justificarlo", "help"),
        ("y ahora?", "continue"),
        ("No repitas; dame otro ejemplo", "example"),
        ("compara las opciones", "comparison"),
        ("quiero terminar la sesión", "finish"),
        ("repite y no repitas", "ambiguous"),
    ],
)
async def test_v2_act_is_separate_from_active_mode(text, act):
    request = AgentRequest(
        session_id=uuid4(),
        turn_id=uuid4(),
        input={"text": text, "dialogue_schema_version": 2, "current_mode": "guided_explanation"},
    )
    result = await StudyIntentInterpreterAgent().execute(request, CancellationToken())
    assert result.status == "ok"
    output = DialogueAct.model_validate(result.output["dialogue_act"])
    assert output.primary_act == act
    assert output.confidence_kind == "heuristic"
    assert result.output["requested_mode"] is None
    if text.startswith("No repitas"):
        assert "repeat" in output.negated_acts


async def test_cancelled_v2_does_not_produce_a_plan():
    token = CancellationToken()
    token.cancel()
    result = await StudyIntentInterpreterAgent().execute(
        AgentRequest(
            session_id=uuid4(), turn_id=uuid4(), input={"text": "hola", "dialogue_schema_version": 2}
        ),
        token,
    )
    assert result.status == "cancelled"
    assert result.output is None


def test_context_is_bounded_and_rejects_unknown_fields():
    assert DialogueContext.model_validate({}).schema_version == 1
    for payload in [{"support_step": 4}, {"content_query": "x" * 501}, {"secret": "x"}]:
        with pytest.raises(ValidationError):
            DialogueContext.model_validate(payload)


def test_plan_cannot_authorize_candidate_text_or_arbitrary_transform():
    base = {
        "template_id": "reviewed-unit",
        "template_version": "1",
        "unit_refs": [str(uuid4())],
        "template_sha256": "a" * 64,
        "action": "example",
    }
    assert ProposalPlan.model_validate(base).action == "example"
    for extra in [{"candidate_text": "inventado"}, {"transformation": "free_paraphrase"}]:
        with pytest.raises(ValidationError):
            ProposalPlan.model_validate(base | extra)


@pytest.mark.parametrize(
    "text,expected",
    [
        ("No me des un ejemplo; repite", "repeat"),
        ("Sin ayuda, vuelve a repetir", "repeat"),
        ("No termines; continúa", "continue"),
        ("No repitas; no me des un ejemplo; continúa", "continue"),
        ("No entiendo, necesito una pista", "ambiguous"),
    ],
)
async def test_negation_with_polite_auxiliary_and_inability_are_distinct(text, expected):
    result = await StudyIntentInterpreterAgent().execute(
        AgentRequest(session_id=uuid4(), turn_id=uuid4(), input={"text": text, "dialogue_schema_version": 2}),
        CancellationToken(),
    )
    assert result.output["dialogue_act"]["primary_act"] == expected


@pytest.mark.parametrize(
    "text,expected",
    [
        ("Repite la comparación", "repeat"),
        ("Repite el ejemplo", "repeat"),
        ("Repite la pista", "repeat"),
        ("Repite y compara", "ambiguous"),
        ("Repite y dame un ejemplo", "ambiguous"),
        ("No repitas la comparación; continúa", "continue"),
        ("¿Puedes releer la pregunta?", "repeat"),
        ("¿Puedes ayudarme?", "help"),
        ("Hola, buenas tardes", "greeting"),
    ],
)
async def test_requested_operation_is_distinct_from_its_content_object(text, expected):
    result = await StudyIntentInterpreterAgent().execute(
        AgentRequest(session_id=uuid4(), turn_id=uuid4(), input={"text": text, "dialogue_schema_version": 2}),
        CancellationToken(),
    )
    assert result.output["dialogue_act"]["primary_act"] == expected


async def test_repeat_target_is_the_object_before_its_complement():
    result = await StudyIntentInterpreterAgent().execute(
        AgentRequest(
            session_id=uuid4(),
            turn_id=uuid4(),
            input={"text": "repite la pista de la pregunta", "dialogue_schema_version": 2},
        ),
        CancellationToken(),
    )
    assert result.output["dialogue_act"]["repeat_target"] == "hint"


def test_repeat_target_cannot_be_attached_to_a_different_action():
    with pytest.raises(ValidationError):
        DialogueAct(primary_act="help", reason_code="explicit_control", repeat_target="hint")


@pytest.mark.parametrize(
    "text", ["Esto, por favor", "Por favor, dímelo", "Dímelo ahora", "Ahora, aclara eso"]
)
@pytest.mark.parametrize("references", [0, 1, 2, 4])
async def test_polite_reference_still_requires_one_authorized_referent(text, references):
    from oralia.domain.dialogue.contracts import Referent

    context = DialogueContext(
        candidate_referents=tuple(Referent(kind="topic", ref=f"synthetic-{i}") for i in range(references))
    )
    result = await StudyIntentInterpreterAgent().execute(
        AgentRequest(
            session_id=uuid4(),
            turn_id=uuid4(),
            input={
                "text": text,
                "dialogue_schema_version": 2,
                "dialogue_context": context.model_dump(mode="json"),
            },
        ),
        CancellationToken(),
    )
    act = result.output["dialogue_act"]
    assert act["primary_act"] == ("repeat" if references == 1 else "ambiguous")
    assert act["needs_clarification"] == (references != 1)


@pytest.mark.parametrize(
    "text,expected",
    [
        ("¿Qué viene después de la comparación?", "continue"),
        ("Continúa tras el ejemplo", "continue"),
        ("¿Qué paso sigue después de la pista?", "continue"),
        ("Continúa y dame un ejemplo", "ambiguous"),
        ("Continúa y compara", "ambiguous"),
    ],
)
async def test_continuation_complement_is_not_a_second_operation(text, expected):
    result = await StudyIntentInterpreterAgent().execute(
        AgentRequest(session_id=uuid4(), turn_id=uuid4(), input={"text": text, "dialogue_schema_version": 2}),
        CancellationToken(),
    )
    assert result.output["dialogue_act"]["primary_act"] == expected


@pytest.mark.parametrize(
    "text,expected",
    [
        ("¿Podrías comparar los dos recorridos?", "comparison"),
        ("Necesito contrastar ambos procesos", "comparison"),
        ("Quiero relacionar los dos conceptos", "comparison"),
        ("¿Puedes repetirme la explicación?", "repeat"),
        ("¿Puedes repetírmelo?", "repeat"),
    ],
)
async def test_infinitive_operations_keep_their_action_and_clitics(text, expected):
    result = await StudyIntentInterpreterAgent().execute(
        AgentRequest(session_id=uuid4(), turn_id=uuid4(), input={"text": text, "dialogue_schema_version": 2}),
        CancellationToken(),
    )
    assert result.output["dialogue_act"]["primary_act"] == expected
