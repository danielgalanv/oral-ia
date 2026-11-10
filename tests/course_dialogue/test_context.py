"""Compositional support requests preserve an actual input referent, never permission."""

import json
from pathlib import Path

import pytest

from oralia.course_dialogue.context import plan_context


def test_rephrase_then_example_are_compatible_not_a_menu():
    history = [
        {"input": "Qué significa validar requisitos", "academic_query": "Qué significa validar requisitos"}
    ]
    result = plan_context(
        "No lo entiendo todavía. ¿Puedes explicarlo de otra manera y con un ejemplo hipotético?", history
    )
    assert result.academic_query == history[0]["input"]
    assert set(result.requested_support) >= {"rephrase", "example"}


def test_explicit_new_content_question_changes_the_retrieval_anchor():
    q = "¿Y si dos requisitos se contradicen? ¿Cómo se trata ese conflicto?"
    result = plan_context(q, [{"input": "Validar requisitos", "academic_query": "Validar requisitos"}])
    assert result.academic_query == q


def test_foreign_content_is_not_replaced_by_previous_topic():
    q = "¿Cuánto cuesta el petróleo?"
    result = plan_context(q, [{"input": "Validar requisitos", "academic_query": "Validar requisitos"}])
    assert result.academic_query == q


def test_actual_pending_answer_keeps_academic_referent_until_explicit_switch():
    history = [
        {
            "input": "¿Qué es validar requisitos?",
            "academic_query": "validar requisitos",
            "displayed_text": "Se contrasta con necesidades. ¿Qué necesidad se atiende?",
            "display_kind": "candidate",
            "parsed_candidate": {"question": "¿Qué necesidad se atiende?"},
        }
    ]
    answer = plan_context("Las necesidades del cliente", history)
    assert answer.academic_query == "validar requisitos"
    assert answer.pending_question == "¿Qué necesidad se atiende?"
    switch = plan_context("Cambio de tema: ¿qué es un caso de prueba?", history)
    assert switch.academic_query == "qué es un caso de prueba?"


def test_echoed_question_does_not_become_pending_state():
    prompt = "¿Qué es validar requisitos?"
    history = [
        {
            "input": prompt,
            "academic_query": "validar requisitos",
            "displayed_text": "Respuesta. " + prompt,
            "display_kind": "candidate",
            "parsed_candidate": {"question": prompt},
        }
    ]
    result = plan_context("Una necesidad del cliente", history)
    assert result.pending_question is None
    assert result.academic_query == "Una necesidad del cliente"


def test_explicit_switch_discards_previous_output_quoted_in_user_preamble():
    history = [
        {
            "input": "Validar requisitos",
            "academic_query": "validar requisitos",
            "displayed_text": "Validar requisitos es otra actividad.",
            "display_kind": "candidate",
        }
    ]
    text = "Sobre «validar requisitos»: Cambio de tema: ¿qué es un caso de prueba?"
    plan = plan_context(text, history)
    assert plan.academic_query == "qué es un caso de prueba?"


def test_example_after_repeat_and_operational_error_uses_clean_topic_not_old_instruction():
    topic = "¿Qué diferencia hay entre revisar la calidad de los requisitos y validarlos con el cliente?"
    history = [
        {
            "input": topic,
            "academic_query": topic,
            "academic_topic": topic,
            "display_kind": "candidate",
            "displayed_text": "Dos objetivos.",
        },
        {
            "input": (
                "Sobre lo que acabas de mostrar («Dos objetivos»): "
                "Sigo confundido; di qué se comprueba en cada actividad."
            ),
            "academic_query": topic,
            "academic_topic": topic,
            "display_kind": "candidate",
            "displayed_text": "Se comprueban cosas distintas.",
        },
        {
            "input": "Pon un ejemplo",
            "display_kind": "operational",
            "displayed_text": "No se obtuvo una respuesta completa.",
        },
    ]
    current = (
        "Sobre lo que acabas de mostrar («Se comprueban cosas distintas»): "
        "Pon un ejemplo ficticio concreto; declara los supuestos."
    )
    plan = plan_context(current, history)
    assert plan.academic_query == topic
    assert plan.academic_topic == topic
    assert plan.current_request == "Pon un ejemplo ficticio concreto; declara los supuestos."
    assert "example" in plan.requested_support
    assert "Sigo confundido" not in plan.academic_query


def test_explicit_new_example_topic_overrides_referent_without_course_dictionary():
    history = [
        {
            "input": "¿Qué es validar requisitos?",
            "academic_topic": "validar requisitos",
            "displayed_text": "Se contrastan necesidades.",
            "display_kind": "candidate",
        }
    ]
    plan = plan_context("Ahora, sobre pruebas de defectos, pon un ejemplo.", history)
    assert plan.academic_query == "pruebas de defectos"
    assert plan.academic_topic == "pruebas de defectos"
    assert "example" in plan.requested_support
    direct = plan_context("Pon un ejemplo de pruebas de defectos.", history)
    assert direct.academic_query == "pruebas de defectos"
    deictic = plan_context("Pon un ejemplo de eso.", history)
    assert deictic.academic_query == "validar requisitos"


def test_rectification_uses_current_content_and_switch_discards_quoted_preamble():
    history = [
        {
            "input": "Sigo confundido; di qué se comprueba.",
            "academic_topic": "validar requisitos",
            "displayed_text": "Calidad y necesidades.",
            "display_kind": "candidate",
        }
    ]
    correction = plan_context(
        "Sobre lo que acabas de mostrar («Calidad y necesidades»): "
        "Retiro esa idea. ¿Cómo se comprueba que un requisito no admite dos interpretaciones?",
        history,
    )
    assert correction.academic_query.startswith("Retiro esa idea.")
    assert "Sobre lo que acabas" not in correction.academic_query
    switch = plan_context(
        "Sobre lo que acabas de mostrar («Calidad y necesidades»): "
        "Cambio de tema: ¿qué diferencia hay entre pruebas de defectos y de validación?",
        history,
    )
    assert switch.academic_query == "qué diferencia hay entre pruebas de defectos y de validación?"


@pytest.mark.parametrize("variant", ["documental", "pedagogica"])
def test_preserved_capture_example_retrieval_does_not_reuse_repeat_instruction(variant):
    packet = (
        Path(__file__).resolve().parents[2]
        / "specs/012-conversational-course-study/evidence/chat-comparison-v2-final-capture-first"
    )
    saved = json.loads(
        (packet / f"quality-versus-needs-final-capture-0-{variant}.json").read_text(encoding="utf-8")
    )
    turns = saved["turns"]
    plan = plan_context(turns[3]["input"], turns[:3])
    assert plan.academic_query == turns[0]["academic_query"]
    assert plan.current_request.startswith("Pon un ejemplo ficticio concreto")
    assert "Sigo confundido" not in plan.academic_query
