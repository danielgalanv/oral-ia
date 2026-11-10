"""Finite final syntax must not replace the model's reasoning or its decision."""

import json

import pytest

from oralia.course_dialogue.finite_schema import allowed_thinking_tokens
from oralia.course_dialogue.generation_limits import validate_budget_frame
from oralia.course_dialogue.web_control_request import (
    WebControlRequest,
    finite_control_schema,
    parse_finite_control,
)
from oralia.course_dialogue.web_review_frame import validate_web_review_frame


def test_reasoning_unrestricted_but_final_closed():
    choices = [[1, 2], [1, 3]]
    assert list(allowed_thinking_tokens(choices, [8, 7], 9, 12, 10)) == list(range(12))
    assert allowed_thinking_tokens(choices, [8, 7, 10], 9, 12, 10) == [1]
    assert allowed_thinking_tokens(choices, [8, 7, 10, 1], 9, 12, 10) == [2, 3]
    assert allowed_thinking_tokens(choices, [8, 7, 10, 1, 2], 9, 12, 10) == [9]
    with pytest.raises(ValueError):
        allowed_thinking_tokens(choices, [10, 1, 2, 4], 9, 12, 10)
    with pytest.raises(ValueError):
        allowed_thinking_tokens(choices, [10, 10], 9, 12, 10)


@pytest.mark.parametrize("control", ["gap", "support", "compatibility"])
@pytest.mark.parametrize("version", ["web-control/v3", "web-control/v4", "web-control/v5"])
def test_schema_and_frame_bound_to_control(control, version):
    schema = finite_control_schema(control, ["software requirements", "requirements validation"])
    request = WebControlRequest(
        purpose="explicacion",
        instruction="control",
        question="¿La premisa es cierta?",
        prompt_version=version,
        control=control,
        allowed_concepts=["software requirements", "requirements validation"],
        output_schema=schema,
        evidence=[],
    )
    frame = dict(
        model_prompt_profile="qwen3-8b-thinking",
        prompt_task="review",
        web_review_prompt_version=version,
        web_review_format_reminder=False,
        finite_outputs=schema["x-oralia-finite-outputs"],
        finite_after_thinking=True,
        messages=request.effective_messages(),
    )
    validate_web_review_frame(frame, "qwen3-8b-thinking")
    for text in schema["x-oralia-finite-outputs"]:
        verdict = parse_finite_control(text, control, ["software requirements", "requirements validation"])
        assert "reason" not in json.loads(text) and verdict.status == json.loads(text)["status"]
        with pytest.raises(ValueError):
            parse_finite_control(text + "}", control, ["software requirements", "requirements validation"])
    frame["finite_outputs"] = ["{}"]
    with pytest.raises(ValueError):
        validate_web_review_frame(frame, "qwen3-8b-thinking")


def test_no_instruction_only_fallback():
    with pytest.raises(ValueError):
        WebControlRequest(
            purpose="explicacion",
            instruction="control",
            question="Pregunta",
            prompt_version="web-control/v3",
            control="gap",
            evidence=[],
        )


def test_scope_requires_explicit_activity_binding_and_native_schema():
    concepts = ["software requirements"]
    fields = dict(
        purpose="explicacion",
        instruction="Scope",
        question="Pregunta",
        control="scope",
        allowed_concepts=concepts,
        output_schema=finite_control_schema("scope", concepts),
        evidence=[],
    )
    with pytest.raises(ValueError):
        WebControlRequest(**fields, prompt_version="web-control/v5")
    binding = {"activity": "fixture", "version": 1, "concepts": concepts, "exclusive": True}
    request = WebControlRequest(**fields, prompt_version="web-control/v5", scope_binding=binding)
    frame = dict(
        model_prompt_profile="qwen3-8b-thinking",
        prompt_task="review",
        web_review_prompt_version="web-control/v5",
        web_review_format_reminder=False,
        finite_outputs=fields["output_schema"]["x-oralia-finite-outputs"],
        finite_after_thinking=True,
        messages=request.effective_messages(),
    )
    validate_web_review_frame(frame, "qwen3-8b-thinking")
    with pytest.raises(ValueError):
        WebControlRequest(**fields, prompt_version="web-control/v4", scope_binding=binding)
    frame["messages"][1]["content"] = frame["messages"][1]["content"].replace(
        '"exclusive":true', '"exclusive":false'
    )
    with pytest.raises(ValueError):
        validate_web_review_frame(frame, "qwen3-8b-thinking")


@pytest.mark.parametrize("version", ["web-control/v3", "web-control/v4", "web-control/v5"])
def test_finite_thinking_budget_is_specific_to_registered_controls_and_not_larger(version):
    frame = dict(
        model_prompt_profile="qwen3-8b-thinking",
        construction_profile="structured/v1",
        prompt_task="review",
        budget_profile="review-thinking/v1",
        finite_outputs=["{}"],
        finite_after_thinking=True,
        web_review_prompt_version=version,
        max_tokens=8192,
        deadline_ms=180000,
    )
    assert validate_budget_frame(frame, thinking_review_enabled=True) == "review-thinking/v1"
    with pytest.raises(ValueError):
        validate_budget_frame(
            {**frame, "web_review_prompt_version": "web-control/v2"}, thinking_review_enabled=True
        )
    with pytest.raises(ValueError):
        validate_budget_frame({**frame, "max_tokens": 8193}, thinking_review_enabled=True)
