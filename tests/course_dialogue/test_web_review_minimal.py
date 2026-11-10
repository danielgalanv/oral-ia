"""Single-decision laboratory contract: no academic endorsement from host derivation."""

import json

import pytest

from oralia.course_dialogue.model_prompt_profiles import validate_structured_frame
from oralia.course_dialogue.web_review_rounds import WebReviewRounds, parse_web_review
from tests.course_dialogue.test_web_review_references import base, issue, locations


def request(task="review"):
    return WebReviewRounds.request(
        base(),
        task,
        draft=None if task == "generate" else "A measurable requirement is feasible.",
        prompt_version="web-review/v7",
        source_locations=locations(),
    )


@pytest.mark.parametrize(
    "status,action",
    [("no_issues_found", "explanation"), ("insufficient_evidence", "limit"), ("issues_found", "repair")],
)
def test_host_derives_only_action_not_support(status, action):
    row = dict(status=status, issues=[issue()] if status == "issues_found" else [])
    parsed = parse_web_review(json.dumps(row), request(), request().draft)
    assert parsed.response_action == action
    assert parsed.external_support == parsed.teacher_compatibility == "unknown"
    assert parsed.status == status


@pytest.mark.parametrize(
    "patch",
    [
        dict(response_action="repair"),
        dict(external_support="supported"),
        dict(teacher_compatibility="compatible"),
        dict(extra=True),
    ],
)
def test_redundant_or_extra_model_decisions_are_rejected(patch):
    row = dict(status="no_issues_found", issues=[], **patch)
    with pytest.raises(ValueError):
        parse_web_review(json.dumps(row), request(), request().draft)


@pytest.mark.parametrize(
    "row",
    [
        dict(status="issues_found", issues=[]),
        dict(status="no_issues_found", issues=[issue()]),
        dict(status="insufficient_evidence", issues=[issue()]),
    ],
)
def test_status_and_issues_must_agree(row):
    with pytest.raises(ValueError):
        parse_web_review(json.dumps(row), request(), request().draft)


@pytest.mark.parametrize("change", ["foreign", "duplicated", "missing", "quote"])
def test_source_guards_are_preserved(change):
    entry = issue()
    if change == "foreign":
        entry["evidence"] = [dict(source_id="alien")]
    if change == "duplicated":
        entry["evidence"] *= 2
    if change == "missing":
        entry.update(kind="contradiction", evidence=[])
    if change == "quote":
        entry["evidence"][0]["quote"] = "literal"
    with pytest.raises(ValueError):
        parse_web_review(json.dumps(dict(status="issues_found", issues=[entry])), request(), request().draft)


@pytest.mark.parametrize("task", ["review", "repair", "generate"])
def test_actual_worker_renderer_reconstructs_v7(task):
    req = request(task)
    frame = dict(
        model_prompt_profile=req.model_profile,
        prompt_task=task,
        messages=req.effective_messages(),
        web_review_prompt_version="web-review/v7",
        web_review_format_reminder=False,
    )
    validate_structured_frame(frame, req.model_profile)


def test_defaults_and_v6_remain_separate():
    req = WebReviewRounds.request(base(), "review", draft="Answer")
    assert req.prompt_version == "web-review/v1"
    old = WebReviewRounds.request(
        base(), "review", draft="Answer", prompt_version="web-review/v6", source_locations=locations()
    )
    with pytest.raises(ValueError):
        parse_web_review('{"status":"no_issues_found","issues":[]}', old, old.draft)


@pytest.mark.asyncio
async def test_minimal_review_repair_recheck_keeps_semantics_unknown_and_unpublished():
    from oralia.course_dialogue.review_repair import CallBudget
    from tests.course_dialogue.test_web_review_references import Provider

    generator = Provider("A measurable requirement is feasible.")
    critic = Provider(
        json.dumps(dict(status="issues_found", issues=[issue()])),
        "Measurability does not establish feasibility.",
        json.dumps(dict(status="no_issues_found", issues=[])),
    )
    revalidations = []
    loop = WebReviewRounds(
        generator,
        critic,
        budget=CallBudget(maximum=4),
        revalidate=lambda: revalidations.append(True),
        prompt_version="web-review/v7",
        source_locations=locations(),
    )
    trace = await loop.process(base())
    assert trace["accepted_by_critic"] and len(trace["versions"]) == 2
    assert len(trace["calls"]) == 4 and revalidations
    assert all(
        row["external_support"] == row["teacher_compatibility"] == "unknown" for row in trace["reviews"]
    )
    assert trace["publication_allowed"] is False and trace["participant_display"] is None
    assert trace["independent_semantics"] is False
