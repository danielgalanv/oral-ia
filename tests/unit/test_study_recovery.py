"""CPU-only operational recovery. Does not evaluate academic sufficiency."""

import uuid

import pytest

from oralia.documentary.study_errors import StudyFailure
from tests.unit.test_retrieval_increment import query_double
from tests.unit.test_study_lab import setup


@pytest.mark.parametrize(
    "question,history,code",
    [
        ("x" * 140, [], "question_too_long"),
        ("requisito", ["h" * 125], "search_context_too_long"),
    ],
)
def test_capacity_failures_are_distinct_and_precede_embedding(question, history, code):
    retrieval = query_double()
    retrieval.adapter.embed = lambda _: pytest.fail("oversized input must never be embedded")
    before = history.copy()
    with pytest.raises(StudyFailure) as error:
        retrieval.query(question, "dense", history=history)
    assert error.value.code == code
    assert history == before


def test_explicit_focus_change_can_use_short_question_without_truncating_previous_context():
    retrieval = query_double()
    history = ["h" * 125]
    result = retrieval.query("requisito", "dense", history=history, focus_change=True)
    assert result["passages"] == [] and result["sufficiency"] == "not_assessed"
    assert history == ["h" * 125]


@pytest.mark.parametrize("code", ["question_too_long", "search_context_too_long", "no_passages"])
async def test_recoverable_limit_preserves_history_and_quota_then_allows_continuation(code):
    lab, retrieval, provider = setup()
    first = await lab.turn("¿Qué es un requisito?", str(uuid.uuid4()))
    lab.acknowledge(first["id"])
    history = list(lab.history)
    original = retrieval.query

    def limited(question, *args, **kwargs):
        if question == "consulta de prueba con límite":
            if code == "no_passages":
                return {
                    "identity": retrieval.fingerprint["revision"],
                    "strategy": "dense",
                    "passages": [],
                    "sufficiency": "not_assessed",
                }
            raise StudyFailure(code)
        return original(question, *args, **kwargs)

    retrieval.query = limited
    failed_id = str(uuid.uuid4())
    failed = await lab.turn("consulta de prueba con límite", failed_id)
    assert failed["failure_code"] == code
    assert lab.history == history and not lab.closed and lab.pending is None
    assert lab.budget.used == 1 and len(provider.requests) == 1
    assert lab.receipt(failed_id)["diagnostic_preview"] is None
    with pytest.raises(ValueError, match="duplicada"):
        await lab.turn("consulta de prueba con límite", failed_id)
    last = await lab.turn("¿Puedes darme un ejemplo breve?", str(uuid.uuid4()))
    assert last["status"] == "prepared_unverified"
    assert lab.budget.used == 2 and len(provider.requests) == 2
    assert [m.content for m in provider.requests[-1].conversation_history] == [
        history[0]["question"],
        history[0]["text"],
    ]
    lab.acknowledge(last["id"])
    assert len(lab.history) == 2
    lab.close()
