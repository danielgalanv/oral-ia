"""Premises are literal data; a probe cannot become an authoritative criticism."""

import asyncio

from oralia.course_dialogue.example_probe import literal_requirements, probe_request
from oralia.course_dialogue.review_repair import CallBudget
from oralia.course_dialogue.web_review_frame import validate_web_review_frame
from oralia.course_dialogue.web_review_references import SourceLocation
from oralia.course_dialogue.web_review_rounds import WebReviewRounds
from tests.course_dialogue.test_web_review_rounds import Provider, request


def test_extract_literal_premises_without_authors_conclusion():
    draft = (
        "**Requisito 1:** El sistema cifra los mensajes.\n\n"
        "**Requisito 2:** Permite acceso sin registro.\n\nPor tanto, son incompatibles."
    )
    rows = literal_requirements(draft)
    assert len(rows) == 2 and all(draft[p["start"] : p["end"]] == p["text"] for p in rows)
    probe = probe_request(request(), draft)
    messages = probe.effective_messages()
    assert "Por tanto" not in messages[-1]["content"]
    validate_web_review_frame(
        dict(
            model_prompt_profile="qwen3-8b-thinking",
            prompt_task="review",
            web_review_prompt_version="example-probe/v1",
            web_review_format_reminder=False,
            messages=messages,
        ),
        "qwen3-8b-thinking",
    )


def test_no_invented_premises_for_unstructured_answer():
    assert probe_request(request(), "Una explicación sin pares numerados.") is None


def test_probe_is_advisory_and_cannot_create_an_issue_or_replace_answer():
    draft = "**Requisito 1:** Conserva datos.\n**Requisito 2:** Permite consulta."
    critic = Provider(
        "Un escenario hipotético podría cumplir ambos.", '{"status":"no_issues_found","issues":[]}'
    )
    loop = WebReviewRounds(
        Provider(draft),
        critic,
        budget=CallBudget(),
        revalidate=lambda: None,
        generator_profile="qwen25-14b",
        critic_profile="qwen3-8b-thinking",
        repair_with_generator=True,
        prompt_version="web-review/v8",
        example_probe_enabled=True,
        source_locations={
            "E": SourceLocation(
                document_id="internet/original",
                document_version=1,
                document_title="NASA",
                url="https://www.nasa.gov/test",
            ),
            "T": SourceLocation(
                document_id="teacher/current", document_version=1, document_title="Docente", page=1
            ),
        },
    )
    trace = asyncio.run(loop.process(request()))
    assert [c["stage"] for c in trace["calls"]] == ["generate", "review", "review"]
    assert trace["calls"][1]["review_kind"] == "example_probe"
    assert trace["diagnostic_preview"] == draft
    assert critic.requests[1].observations[0]["not_automatic_issue"] is True
