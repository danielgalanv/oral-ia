"""Literal editing safety, not semantic validation of the replacement."""

import pytest

from oralia.course_dialogue.web_local_patch import apply_patch, first_anchored_target


def test_automatic_critique_selects_whole_sentence_and_preserves_all_other_text():
    draft = "Un ejemplo. Es realizable por ser medible, y se prueba. Falta analizar el contexto."
    issues = [{"claim": '"Es realizable por ser medible"', "kind": "contradiction"}]
    target, issue = first_anchored_target(draft, issues)
    assert target == "Es realizable por ser medible, y se prueba."
    assert issue == issues[0]
    changed = apply_patch(draft, target, "Se puede comprobar, pero falta acreditar su viabilidad.")
    assert changed == (
        "Un ejemplo. Se puede comprobar, pero falta acreditar su viabilidad. " "Falta analizar el contexto."
    )


def test_unanchored_or_ambiguous_critic_cannot_choose_an_edit():
    with pytest.raises(ValueError):
        first_anchored_target("Una frase.", [{"claim": "", "kind": "coverage"}])
    with pytest.raises(ValueError):
        first_anchored_target("Una frase. Una frase.", [{"claim": "Una frase."}])
    with pytest.raises(ValueError):
        first_anchored_target("Una frase.", [{"claim": "Otra frase."}])


def test_a_closing_quote_does_not_merge_the_example_with_the_defective_sentence():
    draft = 'Ejemplo: "Reinicia en 5 segundos." Es realizable por ser medible. Falta contexto.'
    target, _ = first_anchored_target(draft, [{"claim": "Es realizable por ser medible"}])
    assert target == "Es realizable por ser medible."


@pytest.mark.parametrize(
    "old,new", [("Otra frase.", "Cambio."), ("Una frase.", ""), ("Una frase.", "Una frase.")]
)
def test_missing_empty_or_noop_edit_is_rejected(old, new):
    with pytest.raises(ValueError):
        apply_patch("Una frase.", old, new)
