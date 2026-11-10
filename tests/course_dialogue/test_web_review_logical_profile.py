"""CPU protocol checks only; they do not prove the review model's judgement."""

import copy

import pytest

from oralia.course_dialogue.thinking_review_request import ThinkingReviewRequest
from oralia.course_dialogue.web_control_request import SOURCE_SYNTHESIS, WebControlRequest
from oralia.course_dialogue.web_review_frame import validate_web_review_frame
from oralia.course_dialogue.web_review_prompts import REVIEW_V7, role_policy
from oralia.course_dialogue.web_review_references import SourceLocation
from oralia.course_dialogue.web_review_rounds import parse_web_review
from oralia.infrastructure.generation.generation_port import EvidenceItem


def frame(request):
    return dict(
        model_prompt_profile="qwen3-8b-thinking",
        prompt_task="review",
        web_review_prompt_version=request.prompt_version,
        web_review_format_reminder=request.format_reminder,
        messages=request.effective_messages(),
    )


def test_control_retry_reconstructs_exactly_and_confirms_reminder():
    request = WebControlRequest(
        purpose="explicacion",
        instruction="control",
        question="Pregunta",
        control="gap",
        prompt_version="web-control/v2",
        format_reminder=True,
        evidence=[],
    )
    value = frame(request)
    validate_web_review_frame(value, "qwen3-8b-thinking")
    assert SOURCE_SYNTHESIS in value["messages"][0]["content"]
    altered = copy.deepcopy(value)
    altered["web_review_format_reminder"] = False
    with pytest.raises(ValueError):
        validate_web_review_frame(altered, "qwen3-8b-thinking")


def test_new_control_policy_is_opt_in():
    request = WebControlRequest(
        purpose="explicacion", instruction="control", question="Pregunta", control="gap", evidence=[]
    )
    assert SOURCE_SYNTHESIS not in request.effective_messages()[0]["content"]


def test_logical_review_profile_preserves_legacy_and_minimal_contract():
    request = ThinkingReviewRequest(
        purpose="explicacion",
        instruction="review",
        question="Pregunta",
        draft="Candidata ficticia de prueba",
        prompt_version="web-review/v8",
        evidence=[
            EvidenceItem(fragment_id="e", document_id="d", document_version=1, text="Fuente de prueba")
        ],
        source_locations={
            "e": SourceLocation(document_id="d", document_version=1, document_title="Documento", page=1)
        },
    )
    validate_web_review_frame(frame(request), "qwen3-8b-thinking")
    assert (
        parse_web_review('{"status":"no_issues_found","issues":[]}', request, request.draft).status
        == "no_issues_found"
    )
    assert role_policy("review", "web-review/v7") == REVIEW_V7
    assert role_policy("review", "web-review/v8").startswith(REVIEW_V7)
    assert role_policy("repair", "web-review/v8") == role_policy("repair", "web-review/v7")
