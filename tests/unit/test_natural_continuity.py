"""Clause/context controls independent of output publication and scripted transcript strings."""

import json
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest

from oralia.domain.dialogue.continuity import act_for, interpret
from oralia.domain.dialogue.contracts import DialogueAct, DialogueContext


def units(domain):
    data = json.loads(
        Path(f"materiales/docente/integracion-controlada-20261020-v6/{domain}-units.json").read_text(
            encoding="utf-8"
        )
    )
    return [
        SimpleNamespace(**{**u, "relations": u["relations_by_key"], "id": u["key"]}) for u in data["units"]
    ]


@pytest.mark.parametrize(
    "text",
    [
        "¿Para qué revisar la cantidad antes de escribirla?",
        "Vale, ¿por qué no guardarlo primero y comprobarlo después?",
    ],
)
def test_precondition_keeps_validating_as_object_not_subordinate_storage(text):
    r = interpret(text, DialogueContext(current_topic_ref="validacion"), units("programa"))
    assert (r.topic, r.purpose) == ("validacion", "causal_order")


@pytest.mark.parametrize(
    "text",
    [
        "Saludos. ¿Por qué una tela húmeda pierde líquido?",
        "Buenas, ¿cómo sale el vapor de una tela sin hervir?",
    ],
)
def test_compound_greeting_retains_academic_clause(text):
    r = interpret(text, DialogueContext(), units("agua"))
    assert r.greeting and r.topic == "evaporacion" and r.purpose in {"cause", "process", "possibility"}


def test_context_does_not_supply_an_unrelated_subject():
    r = interpret(
        "¿Cómo se hace una predicción del precio del oro?",
        DialogueContext(current_topic_ref="media"),
        units("datos"),
    )
    assert r.topic is None


def test_last_numeric_referent_requires_anchor_and_respects_order():
    q = "¿Qué regla se aplica a ese último valor?"
    assert interpret(q, DialogueContext(current_topic_ref="validacion"), units("programa")).topic is None
    for previous, purpose in [("007 y después mil", "possibility"), ("mil y después 007", "conditions")]:
        context = DialogueContext(
            current_topic_ref="validacion", content_query=previous, last_approved_unit_ids=(uuid4(),)
        )
        assert interpret(q, context, units("programa")).purpose == purpose


def test_student_assertion_is_not_reinterpreted_as_truth_or_new_goal():
    context = DialogueContext(current_topic_ref="evaporacion", pending_question_unit_id=uuid4())
    act = DialogueAct(primary_act="content_answer", reason_code="content_input")
    changed = act_for("Me rectifico: las moléculas no se rompen.", act, context, units("agua"))
    assert changed == act


@pytest.mark.parametrize("permission", ["greeting", "exhaustion"])
def test_continuity_policy_requires_the_additive_greeting_permission(permission):
    from oralia.application.services.screenless_navigation_service import continuity_enabled
    from oralia.domain.dialogue.catalog import guided_policy
    from oralia.domain.policies.output_authorization_policy import (
        canonical_policy_json,
        canonical_policy_sha256,
    )
    from oralia.domain.policies.output_template_catalog import (
        CONTINUITY_NAVIGATION_TEMPLATES,
        GREETED_REVIEWED_RESPONSE,
    )

    policy = guided_policy("owned-test", screenless=True, pedagogy=True, advanced=True, continuity=True)

    def activity(value):
        raw = canonical_policy_json(value)
        return SimpleNamespace(
            output_authorization_policy_json=raw,
            output_authorization_policy_sha256=canonical_policy_sha256(raw),
        )

    assert continuity_enabled(activity(policy), "owned-test")
    required = (
        GREETED_REVIEWED_RESPONSE
        if permission == "greeting"
        else CONTINUITY_NAVIGATION_TEMPLATES["followups_exhausted"]
    )
    modified = policy.model_copy(
        update={
            "allowed_templates": tuple(
                e for e in policy.allowed_templates if e.template_id != required.template_id
            )
        }
    )
    assert not continuity_enabled(activity(modified), "owned-test")


@pytest.mark.parametrize("text", ["¿En qué consiste validar?", "¿Qué se entiende por validar?"])
def test_definition_asks_meaning_not_a_new_operation(text):
    result = interpret(text, DialogueContext(), units("programa"))
    assert (result.topic, result.purpose) == ("validacion", "definition")


@pytest.mark.parametrize(
    "text",
    [
        "Quería decir que cambia el estado y sigue siendo agua.",
        "Sigo hablando del estado: el agua continúa siendo la misma sustancia.",
    ],
)
def test_continue_verb_inside_a_rectification_is_not_a_control(text):
    context = DialogueContext(current_topic_ref="evaporacion", pending_question_unit_id=uuid4())
    act = DialogueAct(primary_act="continue", reason_code="explicit_control")
    assert act_for(text, act, context, units("agua")).primary_act == "content_answer"


def test_relative_clause_does_not_turn_alternative_request_into_a_question():
    context = DialogueContext(current_topic_ref="evaporacion")
    result = interpret("Necesito que lo expliques de otra manera.", context, units("agua"))
    assert result.alternate


@pytest.mark.parametrize(
    "text",
    [
        "¿Y cómo pasa, en orden?",
        "¿Cómo ocurre ese proceso, paso a paso?",
        "¿Cuál es el procedimiento de eso?",
    ],
)
def test_process_deixis_does_not_retrieve_a_foreign_topic(text):
    context = DialogueContext(current_topic_ref="evaporacion", last_approved_unit_ids=(uuid4(),))
    request = interpret(text, context, units("agua"))
    assert request.topic == "evaporacion"
    assert request.purpose == "process"


@pytest.mark.parametrize(
    "text", ["La cantidad 7,25 es menor que mil.", "Tres coma cinco pasa porque es menor que 1000."]
)
def test_decimal_object_is_not_the_incidental_comparison_number(text):
    context = DialogueContext(current_topic_ref="validacion", last_approved_unit_ids=(uuid4(),))
    request = interpret(text, context, units("programa"))
    assert (request.topic, request.purpose) == ("validacion", "decimal_fact")


def test_failed_response_cannot_lend_its_stale_approved_numeric_referent():
    context = DialogueContext(
        current_topic_ref="validacion",
        content_query="¿Y mil?",
        last_notice="verification_failed",
        last_approved_unit_ids=(uuid4(),),
    )
    request = interpret("Dime los pasos con ese último número.", context, units("programa"))
    assert request.purpose == "clarify_numeric"


@pytest.mark.parametrize("prefix", ["Sí. ", "De acuerdo. ", "Vale, "])
def test_affirmative_prefix_preserves_an_explicit_new_close_request(prefix):
    from oralia.domain.dialogue.continuity import is_close_request

    assert is_close_request(prefix + "Termina sin conservar nada.")
    assert not is_close_request(prefix + "No termines todavía.")


@pytest.mark.parametrize(
    "text",
    [
        "La aceptación describe la entrada; guardado describe lo ocurrido después.",
        "Distingo el registro válido de la confirmación del guardado.",
    ],
)
def test_describing_an_outcome_is_not_typing_an_input(text):
    result = interpret(text, DialogueContext(current_topic_ref="validacion"), units("programa"))
    assert result.purpose == "storage_boundary"


@pytest.mark.parametrize(
    "text",
    [
        "Hola, ¿basta teclear el texto para admitirlo?",
        "Buenas. Poder escribir una cantidad significa que la acepta el programa?",
    ],
)
def test_compound_acceptance_question_keeps_its_academic_clause(text):
    result = interpret(text, DialogueContext(), units("programa"))
    assert result.greeting
    assert (result.topic, result.purpose) == ("validacion", "acceptance_boundary")


def test_missing_object_does_not_authorize_an_unrelated_process():
    rows = units("datos")
    anchor = next(u for u in rows if u.id == "datos-media-causal-count")
    anchor.id = str(uuid4())
    context = DialogueContext(current_topic_ref="media", last_approved_unit_ids=(anchor.id,))
    request = interpret("¿Cómo se calcula el precio del oro?", context, rows)
    assert request.purpose != "object_process" and request.topic is None


@pytest.mark.parametrize(
    "text,topic",
    [
        ("Saludos. ¿Una tela húmeda puede secarse sin llevar agua a ebullición?", "evaporacion"),
        ("¿La condensación puede ocurrir sin hervir?", "condensacion"),
        ("¿Puede congelarse el agua sin llegar a ebullición?", "congelacion"),
        ("¿El agua sin hervir puede evaporarse?", "evaporacion"),
    ],
)
def test_negated_process_modifier_does_not_replace_the_main_process(text, topic):
    result = interpret(text, DialogueContext(), units("agua"))
    assert result.topic == topic


def test_negated_known_process_does_not_authorize_an_unknown_main_subject():
    result = interpret("¿Puede calcularse el precio del oro sin hervir?", DialogueContext(), units("agua"))
    assert result.topic is None and result.purpose == "clarify_object"


def test_causal_operator_preserves_approved_object_before_lexical_similarity():
    rows = units("agua")
    anchor = next(u for u in rows if u.id == "agua-evaporacion-possibility")
    anchor.id = str(uuid4())
    context = DialogueContext(current_topic_ref="evaporacion", last_approved_unit_ids=(anchor.id,))
    result = interpret("¿Qué causa que salga por la superficie?", context, rows)
    assert (result.topic, result.purpose) == ("evaporacion", "cause")


@pytest.mark.parametrize("marker", ["Qué es", "Qué significa", "En qué consiste", "Qué se entiende por"])
@pytest.mark.parametrize(
    "operation,topic", [("validar", "validacion"), ("almacenar", "almacenamiento"), ("recibir", "entrada")]
)
@pytest.mark.parametrize("argument", ["esa entrada", "ese registro", "una cantidad"])
def test_definition_focus_is_the_operation_not_its_argument(marker, operation, topic, argument):
    result = interpret(f"¿{marker} {operation} {argument}?", DialogueContext(), units("programa"))
    assert (result.topic, result.purpose) == (topic, "definition")


@pytest.mark.parametrize(
    "relation",
    [
        "Por qué difieren",
        "Por qué son distintos",
        "A qué se deben las diferencias entre",
        "Por qué no coinciden",
    ],
)
@pytest.mark.parametrize("subject", ["esos dos resúmenes", "esas medidas", "ambas descripciones"])
def test_comparison_relation_preserves_the_current_object(relation, subject):
    rows = units("datos")
    anchor = next(u for u in rows if u.id == "datos-mediana-definition")
    anchor.id = str(uuid4())
    context = DialogueContext(current_topic_ref="mediana", last_approved_unit_ids=(anchor.id,))
    result = interpret(f"¿{relation} {subject}?", context, rows)
    assert (result.topic, result.purpose) == ("mediana", "comparison")


def test_comparison_does_not_transfer_the_current_object_to_foreign_nouns():
    rows = units("datos")
    anchor = next(u for u in rows if u.id == "datos-mediana-definition")
    anchor.id = str(uuid4())
    context = DialogueContext(current_topic_ref="mediana", last_approved_unit_ids=(anchor.id,))
    result = interpret("¿Por qué difieren esos precios del oro?", context, rows)
    assert result.purpose != "comparison"


@pytest.mark.parametrize(
    "argument",
    ["la entrada recibida", "el registro introducido", "la cantidad ingresada", "el texto escrito"],
)
@pytest.mark.parametrize("marker", ["Qué es", "Qué se entiende por", "En qué consiste", "Definición de"])
def test_definition_focus_precedes_acceptance_boundary(marker, argument):
    result = interpret(f"¿{marker} validar {argument}?", DialogueContext(), units("programa"))
    assert (result.topic, result.purpose) == ("validacion", "definition")


@pytest.mark.parametrize(
    "relation",
    [
        "respuesta de escritura",
        "resultado de escritura",
        "respuesta de la escritura",
        "resultado de la escritura",
    ],
)
@pytest.mark.parametrize(
    "prefix", ["Diferencio la validación del dato de la", "No confundo la validación del registro con la"]
)
def test_explicit_outcome_relation_keeps_published_storage_bridge(relation, prefix):
    result = interpret(
        f"{prefix} {relation}.", DialogueContext(current_topic_ref="validacion"), units("programa")
    )
    assert (result.topic, result.purpose) == ("validacion", "storage_boundary")


@pytest.mark.parametrize(
    "phrase",
    [
        "Se seca una tela sin hervir el agua",
        "La tela se seca sin que el agua hierva",
        "Se secaba la ropa aunque no hirviendo",
    ],
)
def test_negated_competing_process_keeps_inflected_main_process(phrase):
    result = interpret(f"¿{phrase}?", DialogueContext(), units("agua"))
    assert (result.topic, result.purpose) == ("evaporacion", "possibility")


@pytest.mark.parametrize("verb", ["salen", "resultan", "son"])
def test_comparison_result_verbs_do_not_introduce_foreign_objects(verb):
    rows = units("datos")
    anchor = next(u for u in rows if u.id == "datos-mediana-definition")
    anchor.id = str(uuid4())
    context = DialogueContext(current_topic_ref="mediana", last_approved_unit_ids=(anchor.id,))
    result = interpret(f"¿Por qué {verb} diferentes?", context, rows)
    assert (result.topic, result.purpose) == ("mediana", "comparison")
