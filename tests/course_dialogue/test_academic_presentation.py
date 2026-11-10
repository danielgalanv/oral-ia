"""Observed wrapper regressions: presentation is not semantic correction."""

import json
from pathlib import Path

import pytest

from oralia.course_dialogue.review_repair import CallBudget
from oralia.course_dialogue.web_review_rounds import WebReviewRounds
from tests.course_dialogue.test_web_review_rounds import Provider, request, review
from tests.unit.test_study_lab import ProviderFixture, identifier, setup


@pytest.mark.asyncio
async def test_review_and_history_use_visible_body_while_raw_generation_is_preserved():
    body = "Primera línea.\n\nSegunda línea con 0,3 segundos."
    raw = json.dumps({"mensaje_mostrado": body}, ensure_ascii=False)
    critic = Provider(review())
    loop = WebReviewRounds(Provider(raw), critic, budget=CallBudget(maximum=3), revalidate=lambda: None)
    trace = await loop.process(request())
    assert trace["diagnostic_preview"] == body
    assert trace["versions"][0]["text"] == raw
    assert trace["calls"][0]["outcome"]["text"] == raw
    assert critic.requests[0].draft == body


@pytest.mark.asyncio
async def test_interactive_delivery_keeps_raw_and_acknowledges_only_displayed_body():
    body = "Una explicación completa, con tildes y sin envoltura."
    raw = json.dumps({"mensaje_mostrado": body}, ensure_ascii=False)
    lab, _, _ = setup(ProviderFixture(text=raw))
    ident = identifier()
    await lab.turn("Explica el concepto", ident)
    receipt = lab.display(ident)
    assert receipt["diagnostic_preview"] == body
    assert receipt["raw_candidate"] == receipt["outcome"]["text"] == raw
    lab.acknowledge(ident)
    assert lab.history[-1]["text"] == body


@pytest.mark.parametrize(
    "text",
    [
        "Texto normal intacto.",
        'Ejemplo: {"mensaje_mostrado":"dato"}',
        '```json\n{"mensaje_mostrado":"dato"}\n```',
    ],
)
def test_academic_examples_and_plain_text_are_not_rewritten(text):
    from oralia.course_dialogue.academic_presentation import present_academic_answer

    assert present_academic_answer(text)["text"] == text


@pytest.mark.parametrize(
    "raw",
    [
        '{"mensaje_mostrado":"a","mensaje_mostrado":"b"}',
        '{"mensaje_mostrado":"a","extra":"no descartar"}',
        '{"mensaje_mostrado":null}',
        '{"mensaje_mostrado":"  "}',
        '{"mensaje_mostrado":"incompleto"',
        '{"mensaje_mostrado":"a"} trailing',
    ],
)
def test_ambiguous_or_incomplete_wrappers_are_never_silently_repaired(raw):
    from oralia.course_dialogue.academic_presentation import present_academic_answer

    with pytest.raises(ValueError):
        present_academic_answer(raw)


@pytest.mark.asyncio
async def test_invalid_wrapper_cannot_enter_interactive_history_and_retains_evidence():
    raw = '{"mensaje_mostrado":"texto", "extra":"no perder"}'
    lab, _, _ = setup(ProviderFixture(text=raw))
    ident = identifier()
    await lab.turn("Explica el concepto", ident)
    receipt = lab.receipt(ident)
    assert receipt["diagnostic_preview"] is None
    assert receipt["raw_candidate"] == raw
    assert not lab.history


def test_v2_is_explicit_and_v1_remains_unchanged():
    from oralia.course_dialogue.model_prompt_profiles import render_messages

    v1 = render_messages("qwen25-14b", "generate", "q", [], didactic_profile="study-dialogue/v1")
    v2 = render_messages("qwen25-14b", "generate", "q", [], didactic_profile="study-dialogue/v2")
    assert v2[0]["content"].startswith(v1[0]["content"])
    assert "sin envolver" in v2[0]["content"]
    assert "término original" in v2[0]["content"]
    assert "completeness" not in v2[0]["content"].lower()


def test_exact_recorded_B3_is_unwrapped_without_altering_its_academic_content():
    from oralia.course_dialogue.academic_presentation import present_academic_answer

    root = Path(__file__).resolve().parents[2]
    receipt = root / "docs/audits/2026-11-01-autostudy-approval/run-20261101-214928/B3/result.json"
    raw = json.loads(receipt.read_text(encoding="utf8"))["trace"]["diagnostic_preview"]
    result = present_academic_answer(raw)
    assert result["text"] == json.loads(raw)["mensaje_mostrado"]
    assert result["format"] == "mensaje_mostrado_json"
    assert present_academic_answer("Complejidad y completitud.")["text"] == "Complejidad y completitud."


@pytest.mark.asyncio
async def test_v2_reaches_native_frame_and_rejects_profile_downgrade():
    from oralia.course_dialogue.cached_transformers import CachedTransformersGenerationAdapter
    from oralia.course_dialogue.lab_request import LabGenerationRequest
    from oralia.course_dialogue.model_prompt_profiles import validate_structured_frame
    from oralia.course_dialogue.structured_request import structured_request
    from tests.course_dialogue.test_structured_prompts import Pipe

    request = structured_request(
        LabGenerationRequest(purpose="explicacion", instruction="not copied", student_input="Explica"),
        model_profile="qwen25-14b",
        task="generate",
        didactic_profile="study-dialogue/v2",
    )
    pipe = Pipe()
    await CachedTransformersGenerationAdapter(
        pipe, repair_profile_enabled=True, model_prompt_profile="qwen25-14b"
    ).generate(request)
    validate_structured_frame(pipe.payload, "qwen25-14b")
    pipe.payload["didactic_profile"] = "study-dialogue/v1"
    with pytest.raises(ValueError):
        validate_structured_frame(pipe.payload, "qwen25-14b")
