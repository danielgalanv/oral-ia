"""Closed source-block selection, independent of the real course corpus."""

from hashlib import sha256
from types import SimpleNamespace

import pytest

from oralia.domain.materials.query_excerpt import select_query_excerpts


def evidence(text, key="one"):
    return SimpleNamespace(fragment_id=key, text=text)


@pytest.mark.parametrize(
    "query,label",
    [
        ("Qué significa validar requisitos", "Objetivo"),
        ("Qué riesgos hay si no validar", "Riesgos"),
        ("Qué tareas hay para validar", "Tareas"),
    ],
)
def test_selection_is_literal_bounded_and_footer_free(query, label):
    source = (
        "Validar requisitos\n• Objetivo: contrastar necesidades.\n"
        "• Riesgos: producto inadecuado.\n• Tareas: reuniones.\n30/10/2014 Chapter 4 12"
    )
    plan = select_query_excerpts([evidence(source)], query)
    assert len(plan) == 1
    span = plan[0]
    assert source[span.start : span.end] == span.text
    assert span.source_sha256 == sha256(source.encode()).hexdigest()
    assert label in span.text
    assert "2014" not in span.text


def test_unavailable_example_is_not_generated():
    assert not select_query_excerpts(
        [evidence("• Objetivo: contrastar necesidades.")], "Inventa un ejemplo de mi proyecto"
    )


def test_foreign_object_does_not_receive_an_arbitrary_source():
    assert not select_query_excerpts(
        [evidence("• Comprobable: pruebas razonables.")], "Calcula el precio del petróleo"
    )


def test_matching_content_label_precedes_generic_question_verb():
    source = "Verificar calidad\n• Comprobable. Se pueden definir pruebas.\n• Tareas: reunión."
    span = select_query_excerpts([evidence(source)], "Cómo se define comprobable")[0]
    assert "Comprobable" in span.text and "reunión" not in span.text


def test_full_labels_distinguish_comprehension_from_checkability():
    source = (
        "Calidad\n• Comprensible. Se entiende sin dificultad.\n"
        "• Comprobable. Se pueden definir pruebas razonables."
    )
    span = select_query_excerpts([evidence(source)], "Qué significa comprobable")[0]
    assert "Comprobable" in span.text and "Comprensible" not in span.text


@pytest.mark.parametrize("object_name,expected", [("cliente", True), ("petróleo", False)])
def test_structural_task_uses_only_object_present_in_same_source(object_name, expected):
    source = (
        "Validar requisitos\n• Objetivo: aprobación de los clientes.\n"
        "• Riesgos: producto inadecuado.\n• Tareas: reuniones y prototipado."
    )
    spans = select_query_excerpts([evidence(source)], f"¿Cómo lo haríamos con el {object_name}?")
    assert bool(spans) is expected
    if expected:
        assert spans[0].text == "• Tareas: reuniones y prototipado."
