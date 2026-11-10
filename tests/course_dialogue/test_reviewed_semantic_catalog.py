"""Pure reference graph tests with fictional rows, not teacher/model evidence."""

import uuid
from types import SimpleNamespace

import pytest

from oralia.application.services.reviewed_semantic_catalog import ReviewedSemanticCatalog
from oralia.domain.dialogue.contracts import SemanticStudyPlanV2


def identity(key):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "synthetic-reviewed-binding/" + key))


def units():
    rows = []
    for goal in ["a", "b"]:
        for role, kind in [
            ("cause", "explanation"),
            ("process", "explanation"),
            ("rephrase", "explanation"),
            ("example", "example"),
            ("comparison", "comparison"),
            ("question", "question"),
            ("root", "explanation"),
        ]:
            relations = {}
            if role == "root":
                relations = {
                    name: [identity(goal + "-" + ref)]
                    for name, ref in {
                        "didactic_cause": "cause",
                        "didactic_process": "process",
                        "rephrases": "rephrase",
                        "examples": "example",
                        "comparisons": "comparison",
                        "next": "question",
                    }.items()
                }
            if role == "question":
                relations = {"comparisons": [identity(goal + "-comparison")]}
            rows.append(
                SimpleNamespace(
                    id=identity(goal + "-" + role),
                    status="published",
                    course_id="fiction-course",
                    activity_refs=["fiction-activity"],
                    subgoal_ref=goal,
                    topic_ref=goal,
                    kind=kind,
                    reviewed_content=f"Explicitly fictional {goal} {role}.",
                    relations=relations,
                )
            )
    return rows


def catalog(rows=None):
    return ReviewedSemanticCatalog(
        rows if rows is not None else units(), course_id="fiction-course", activity_id="fiction-activity"
    )


def test_selection_returns_references_only_and_correct_causal_order():
    selected = catalog().select(SemanticStudyPlanV2(act="explain", goal_ref="a"))
    assert selected.unit_ids == tuple(identity("a-" + role) for role in ["root", "cause", "process"])
    assert selected.question_ref is None
    assert not hasattr(selected, "text") and not hasattr(selected, "approved")


def test_draft_foreign_or_missing_relation_rows_are_refused():
    for attribute, value in [("status", "draft"), ("course_id", "foreign"), ("activity_refs", ["foreign"])]:
        rows = units()
        setattr(rows[0], attribute, value)
        with pytest.raises(ValueError, match="foreign"):
            catalog(rows)
    rows = units()
    rows.pop(0)
    with pytest.raises(ValueError, match="relation"):
        catalog(rows)


def test_actual_pending_question_and_correction_quote_are_required():
    compiled = catalog()
    question = identity("a-question")
    plan = SemanticStudyPlanV2(act="respond", goal_ref="a", reply_to_question_id=question)
    with pytest.raises(ValueError, match="pending"):
        compiled.select(plan, current_goal="a", pending_question=identity("b-question"))
    result = compiled.select(plan, current_goal="a", pending_question=question)
    assert result.response_question_ref == question and result.unit_ids == (identity("a-comparison"),)
    correction = SemanticStudyPlanV2(
        act="correct", goal_ref="a", correction_ref=identity("a-comparison"), claim_quote="actual"
    )
    with pytest.raises(ValueError, match="binding"):
        compiled.select(correction, current_input="unrelated input")
    result = compiled.select(correction, current_input="actual")
    assert result.unit_ids == (identity("a-comparison"), question)


def test_rephrase_cannot_change_the_current_goal():
    with pytest.raises(ValueError, match="referent"):
        catalog().select(SemanticStudyPlanV2(act="rephrase", goal_ref="a"), current_goal="b")
