"""Context queries distinguish literal control from authorized content references."""

import pytest

from oralia.domain.dialogue.contracts import DialogueAct, DialogueContext


@pytest.mark.parametrize("act", ["repeat", "rephrase", "help", "continue", "example", "comparison"])
def test_control_uses_context_without_overwriting_raw_input(act):
    from oralia.application.services.dialogue_retrieval_service import contextual_query

    query = contextual_query(
        "no sé justificarlo",
        DialogueAct(primary_act=act, reason_code="explicit_control"),
        DialogueContext(content_query="consulta temática ficticia"),
    )
    assert query.raw_text == "no sé justificarlo"
    assert query.query == "consulta temática ficticia"


def test_greeting_ambiguity_and_missing_anchor_never_search_control_literal():
    from oralia.application.services.dialogue_retrieval_service import contextual_query

    for act in ["greeting", "ambiguous", "help", "repeat"]:
        result = contextual_query(
            "hola", DialogueAct(primary_act=act, reason_code="explicit_control"), DialogueContext()
        )
        assert result.query is None


def test_query_preserves_original_bounded_content():
    from oralia.application.services.dialogue_retrieval_service import contextual_query

    result = contextual_query(
        "¿Cómo funciona?",
        DialogueAct(primary_act="content_question", reason_code="content_input"),
        DialogueContext(),
    )
    assert result.raw_text == result.query == "¿Cómo funciona?"
