import pytest

from oralia.course_dialogue.model_prompt_profiles import render_messages
from oralia.course_dialogue.structured_request import StructuredGenerationRequest
from oralia.course_dialogue.web_review_prompts import role_policy


def test_keyword_profile_extends_existing_guidance_without_subject_answers():
    args = ("qwen25-14b", "generate", "Una pregunta", [])
    old = render_messages(*args, didactic_profile="study-dialogue/v3")
    new = render_messages(*args, didactic_profile="study-dialogue/v4")
    assert new[0]["content"].startswith(old[0]["content"])
    assert "Palabras clave:" in new[0]["content"]
    assert new[1:] == old[1:]
    request = StructuredGenerationRequest(
        purpose="explicacion",
        instruction="Prueba",
        model_profile="qwen25-14b",
        prompt_task="generate",
        question="Una pregunta",
        didactic_profile="study-dialogue/v4",
    )
    assert request.effective_messages() == new


def test_concept_reviewer_extends_existing_contract_not_a_term_dictionary():
    old = role_policy("review", "web-review/v8")
    new = role_policy("review", "web-review/v9")
    assert new.startswith(old)
    assert "independientemente" in new
    assert "completitud" not in new[len(old) :].lower()
    assert "complejidad" not in new[len(old) :].lower()
    assert "Palabras clave:" in role_policy("repair", "web-review/v9")


@pytest.mark.parametrize("text", ["Respuesta sin lista", "Respuesta\nPalabras clave:", "Palabras clave: ; ;"])
def test_missing_or_empty_keywords_are_not_invented(text):
    from oralia.course_dialogue.concept_keywords import keyword_terms

    assert keyword_terms(text) == []


def test_only_explicit_terms_are_extracted_without_gating_minor_format():
    from oralia.course_dialogue.concept_keywords import keyword_terms

    assert keyword_terms("Una explicación\n\n**Palabras clave:** atributo; función") == [
        "atributo",
        "función",
    ]
    assert keyword_terms("Palabras clave: atributo; ATRIBUTO") == ["atributo", "ATRIBUTO"]
    assert keyword_terms("Palabras clave: atributo, función") == ["atributo", "función"]
    assert len(keyword_terms("Palabras clave: " + ";".join(["concepto"] * 9))) == 9


def test_normal_pilot_selects_keywords_but_not_unqualified_concept_reviewer(tmp_path):
    from oralia.documentary.real_study_provider import RealStudyProvider

    provider = RealStudyProvider(tmp_path, reviewed=True, local_first=True)
    assert provider.study_dialogue_profile == "study-dialogue/v4"
    assert provider.review_prompt_version == "web-review/v8"


def test_measured_generation_messages_are_identical_with_stable_review_version():
    from oralia.course_dialogue.web_review_rounds import WebRoundRequest

    args = dict(
        purpose="explicacion",
        instruction="Prueba",
        question="Pregunta",
        model_profile="qwen25-14b",
        prompt_task="generate",
        didactic_profile="study-dialogue/v4",
        source_locations={},
    )
    stable = WebRoundRequest(**args, prompt_version="web-review/v8")
    experimental = WebRoundRequest(**args, prompt_version="web-review/v9")
    assert stable.effective_messages() == experimental.effective_messages()


@pytest.mark.asyncio
async def test_missing_keywords_requests_real_repair_even_after_native_acceptance():
    import json

    from oralia.course_dialogue.lab_request import RepairGenerationRequest
    from oralia.course_dialogue.review_repair import CallBudget
    from oralia.course_dialogue.web_review_rounds import WebReviewRounds
    from oralia.infrastructure.generation.generation_port import GenerationOutcome

    class Port:
        def __init__(self, texts):
            self.texts = iter(texts)

        async def generate(self, request):
            return GenerationOutcome(
                ok=True, text=next(self.texts), finish_reason="stop", adapter="deterministic"
            )

    verdict = json.dumps({"status": "no_issues_found", "issues": []})
    loop = WebReviewRounds(
        Port(["Explicación.", "Explicación.\nPalabras clave: atributo"]),
        Port([verdict, verdict]),
        budget=CallBudget(maximum=4),
        revalidate=lambda: None,
        max_rounds=1,
        generator_profile="qwen25-14b",
        critic_profile="qwen3-8b-thinking",
        repair_with_generator=True,
        generation_didactic_profile="study-dialogue/v4",
        prompt_version="web-review/v9",
        source_locations={},
    )
    trace = await loop.process(
        RepairGenerationRequest(purpose="explicacion", instruction="Prueba", student_input="Pregunta")
    )
    assert len(trace["versions"]) == 2, {
        k: v for k, v in trace.items() if k in ("status", "error", "reviews")
    }
    assert all(r["status"] == "no_issues_found" for r in trace["reviews"])
    assert len(trace["host_keyword_reviews"]) == 1
    assert trace["diagnostic_preview"].endswith("Palabras clave: atributo")
    assert not trace["publication_allowed"]


def test_concept_review_native_frame_is_bound_to_registered_policy():
    from oralia.course_dialogue.thinking_review_request import ThinkingReviewRequest
    from oralia.course_dialogue.web_review_frame import validate_web_review_frame

    request = ThinkingReviewRequest(
        purpose="explicacion",
        instruction="Prueba",
        question="Pregunta",
        draft="Respuesta",
        prompt_version="web-review/v9",
        source_locations={},
    )
    frame = dict(
        model_prompt_profile="qwen3-8b-thinking",
        prompt_task="review",
        messages=request.effective_messages(),
        web_review_prompt_version="web-review/v9",
        web_review_format_reminder=False,
    )
    validate_web_review_frame(frame, "qwen3-8b-thinking")
    frame["messages"][0]["content"] += " Alteración"
    with pytest.raises(ValueError):
        validate_web_review_frame(frame, "qwen3-8b-thinking")
