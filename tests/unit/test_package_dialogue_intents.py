"""Independent finite intent controls, including goals absent from published sources."""

import pytest

from oralia.domain.dialogue.package_dialogue import navigation_text, request_for, topic_for


@pytest.mark.parametrize(
    "text,purpose",
    [
        ("¿Qué significa condiciones y comparación de fuentes?", "definition"),
        ("¿Por qué es así en condiciones y comparación de fuentes?", "cause"),
        ("Explícame paso a paso condiciones y comparación de fuentes.", "process"),
        ("¿Qué es posible y qué no en condiciones y comparación de fuentes?", "possibility"),
    ],
)
def test_purpose_precedes_a_noun_in_the_topic_title(text, purpose):
    result = request_for(text, {"presion", "ebullicion"})
    assert result.purpose == purpose
    assert result.topic == "presion"


def test_unknown_content_never_inherits_the_current_academic_topic():
    assert topic_for("¿Puedes predecir el precio del oro?", {"media"}, "media") is None
    assert topic_for("¿Por qué ocurre?", {"media"}, "media") == "media"


def test_provenance_alias_only_canonicalizes_an_explicit_source_request():
    assert navigation_text("¿De dónde procede esa explicación?") == "de donde sale eso"
    assert navigation_text("El precio procede de otra fuente") == "El precio procede de otra fuente"
