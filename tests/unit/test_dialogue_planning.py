"""Development regressions on references, independent of authorization gates."""

from types import SimpleNamespace
from uuid import uuid4

from oralia.domain.dialogue.contracts import DialogueAct, DialogueContext
from oralia.domain.dialogue.policy import choose


def unit(kind, topic="cambio"):
    return SimpleNamespace(
        id=str(uuid4()),
        kind=kind,
        topic_ref=topic,
        subgoal_ref=topic,
        reviewed_content="Texto revisado de " + kind,
        relations={},
        version=1,
        reveal_policy="study_only",
    )


def test_mode_request_preserves_explicit_named_topic():
    units = [unit("explanation")]
    choice = choose(
        units,
        DialogueAct(
            primary_act="mode_switch", requested_mode="guided_explanation", reason_code="mode_request"
        ),
        DialogueContext(),
        "Explicación guiada sobre cambio",
        protected=False,
        study_mode="guided_explanation",
    )
    assert choice.unit_id == units[0].id


def test_repeat_keeps_all_parts_of_approved_composition():
    units = [unit(kind) for kind in ["explanation", "example", "comparison"]]
    context = DialogueContext(current_topic_ref="cambio", last_approved_unit_ids=tuple(u.id for u in units))
    result = choose(
        units,
        DialogueAct(primary_act="repeat", reason_code="explicit_control"),
        context,
        "repite",
        protected=False,
    )
    assert [result.unit_id, *result.additional_unit_ids] == [u.id for u in units]


def test_requested_guided_mode_can_start_from_first_published_objective():
    units = [unit(kind) for kind in ["explanation", "example", "comparison"]]
    act = DialogueAct(
        primary_act="mode_switch", requested_mode="presentation_preparation", reason_code="mode_request"
    )
    choice = choose(
        units,
        act,
        DialogueContext(),
        "Quiero preparar una exposición",
        protected=False,
        study_mode="presentation_preparation",
    )
    assert [choice.unit_id, *choice.additional_unit_ids] == [u.id for u in units]
