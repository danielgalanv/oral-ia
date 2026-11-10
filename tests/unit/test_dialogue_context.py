"""Pure reference and stagnation decisions do not infer participant competence."""

from oralia.domain.dialogue.contracts import DialogueContext, Referent


def test_reference_must_be_unique_or_explicitly_selected():
    from oralia.domain.dialogue.context import resolve_referent

    first = Referent(kind="topic", ref="first")
    second = Referent(kind="topic", ref="second")
    assert resolve_referent(DialogueContext()) is None
    assert resolve_referent(DialogueContext(candidate_referents=(first,))) == first
    assert resolve_referent(DialogueContext(candidate_referents=(first, second))) is None
    assert (
        resolve_referent(DialogueContext(candidate_referents=(first, second), selected_referent=second))
        == second
    )
    assert resolve_referent(DialogueContext(candidate_referents=(first,), selected_referent=second)) is None


def test_stagnation_is_bounded_and_explicit_repeat_does_not_count():
    from oralia.domain.dialogue.context import after_output

    original = DialogueContext(content_query="consulta sintética")
    first = after_output(
        original, action="help", approved_text="Límite explícito", evidence_ids=(), progressed=False
    )
    assert first.stalled_count == 1 and first.offered_actions == ("rephrase", "topic_switch")
    second = after_output(
        first, action="help", approved_text="Otra estrategia", evidence_ids=(), progressed=False
    )
    assert second.stalled_count == 2
    assert second.offered_actions == ("help", "topic_switch", "finish")
    third = after_output(second, action="help", approved_text="Límite", evidence_ids=(), progressed=False)
    assert third.stalled_count == 2
    repeated = after_output(
        second, action="repeat", approved_text="Límite", evidence_ids=(), progressed=False
    )
    assert repeated.stalled_count == second.stalled_count
    recovered = after_output(
        second,
        action="content_question",
        approved_text="Contenido revisado",
        evidence_ids=("a",),
        progressed=True,
    )
    assert recovered.stalled_count == 0 and recovered.offered_actions == ()
