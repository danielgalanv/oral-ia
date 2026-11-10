"""Scope check of follow-up questions: the question alone first, previous question only when it needs context."""

import types

import pytest

from oralia.documentary.study_web_flow import StudyWebFlow


class Message:
    def __init__(self, role, content):
        self.role, self.content = role, content


class Base:
    def __init__(self, question, history):
        self.student_input, self.conversation_history = question, history

    def model_copy(self, update):
        copy = Base(self.student_input, self.conversation_history)
        for key, value in update.items():
            setattr(copy, key, value)
        return copy


def flow(answers, seen):
    instance = StudyWebFlow.__new__(StudyWebFlow)
    instance.web = types.SimpleNamespace(policy=types.SimpleNamespace(concepts=["c"]))

    async def judge(control, base, evidence, concepts=()):
        seen.append((base.student_input, len(base.conversation_history)))
        return types.SimpleNamespace(status=answers[len(seen) - 1])

    instance.judge = judge
    return instance


HISTORY = [Message("user", "¿Qué es la elicitación?"), Message("assistant", "Es un proceso…")]


@pytest.mark.asyncio
async def test_a_question_that_needs_context_is_judged_again_with_the_previous_question_and_no_history():
    seen = []
    verdict = await flow(["unknown", "in_scope"], seen).judge_scope(Base("¿Qué técnicas incluye?", HISTORY))
    assert verdict.status == "in_scope"
    assert seen == [("¿Qué técnicas incluye?", 0), ("¿Qué es la elicitación? ¿Qué técnicas incluye?", 0)]


@pytest.mark.asyncio
@pytest.mark.parametrize("first", ["in_scope", "outside"])
async def test_a_clear_verdict_on_the_question_alone_is_final_even_after_a_valid_turn(first):
    seen = []
    verdict = await flow([first, "in_scope"], seen).judge_scope(Base("Cambiando de tema: ¿qué es SQL?", HISTORY))
    assert verdict.status == first and len(seen) == 1


@pytest.mark.asyncio
async def test_without_a_previous_question_unknown_stays_unknown():
    seen = []
    verdict = await flow(["unknown"], seen).judge_scope(Base("¿Qué significa eso?", []))
    assert verdict.status == "unknown" and len(seen) == 1


def test_question_parts_splits_mixed_requests():
    from oralia.documentary.study_web_flow import question_parts

    parts = question_parts("¿Qué es un requisito? Y de paso, ¿puedes recomendarme un libro de novelas?")
    assert parts == ["Qué es un requisito", "puedes recomendarme un libro de novelas"]
    assert question_parts("¿Qué es la trazabilidad de requisitos?") == ["Qué es la trazabilidad de requisitos"]
