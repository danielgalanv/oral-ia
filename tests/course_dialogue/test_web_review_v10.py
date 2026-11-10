"""CPU protocol checks for the general review policy; they do not prove the model's judgement."""

import pytest

from oralia.course_dialogue.thinking_review_request import ThinkingReviewRequest
from oralia.course_dialogue.web_review_frame import validate_web_review_frame
from oralia.course_dialogue.web_review_prompts import REVIEW_V7, REVIEW_V10, role_policy
from oralia.course_dialogue.web_review_references import SourceLocation
from oralia.course_dialogue.web_review_rounds import parse_web_review
from oralia.infrastructure.generation.generation_port import EvidenceItem


def request(version="web-review/v10"):
    return ThinkingReviewRequest(
        purpose="explicacion",
        instruction="review",
        question="Pregunta",
        draft="Candidata ficticia de prueba",
        prompt_version=version,
        evidence=[
            EvidenceItem(fragment_id="e", document_id="d", document_version=1, text="Fuente de prueba")
        ],
        source_locations={
            "e": SourceLocation(document_id="d", document_version=1, document_title="Documento", page=1)
        },
    )


def test_v10_keeps_the_v7_contract_and_repair_but_is_opt_in():
    req = request()
    validate_web_review_frame(
        dict(
            model_prompt_profile="qwen3-8b-thinking",
            prompt_task="review",
            web_review_prompt_version=req.prompt_version,
            web_review_format_reminder=req.format_reminder,
            messages=req.effective_messages(),
        ),
        "qwen3-8b-thinking",
    )
    assert (
        parse_web_review('{"status":"no_issues_found","issues":[]}', req, req.draft).status
        == "no_issues_found"
    )
    with pytest.raises(ValueError):
        parse_web_review('{"status":"no_issues_found","issues":[],"extra":1}', req, req.draft)
    assert role_policy("repair", "web-review/v10") == role_policy("repair", "web-review/v8")
    assert role_policy("review", "web-review/v8").startswith(REVIEW_V7)  # frozen versions untouched


def test_v10_is_subject_neutral_and_free_of_case_patches_and_development_notes():
    text = REVIEW_V10.lower()
    for stale in (
        "requisito",
        "mínimo",
        "umbral",
        "enlace",
        "incompatibles",
        "palabras clave",
        "sin endurecer",
        "sin aumentar",
        "autoriza",
        "aprobación",
    ):
        assert stale not in text
    for needed in ("significado", "alcance", "condiciones", "atribución", "hipotétic"):
        assert needed in text
