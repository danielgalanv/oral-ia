"""Distinct model ports and explicit capacities; no inference or semantic claims."""

import json

import pytest

from oralia.course_dialogue.review_repair import CallBudget
from oralia.course_dialogue.web_review_rounds import WebReviewRounds
from tests.course_dialogue.test_web_review_references import Provider, base, issue, locations


@pytest.mark.asyncio
async def test_real_generator_port_also_receives_repair_and_critic_only_reviews():
    generator = Provider(
        "A measurable requirement is feasible.", "Measurability alone does not demonstrate feasibility."
    )
    critic = Provider(
        json.dumps(dict(status="issues_found", issues=[issue()])),
        json.dumps(dict(status="no_issues_found", issues=[])),
    )
    loop = WebReviewRounds(
        generator,
        critic,
        budget=CallBudget(maximum=4),
        revalidate=lambda: None,
        generator_profile="qwen25-14b",
        critic_profile="qwen3-8b-nonthinking",
        repair_with_generator=True,
        stage_tokens={"generate": 1536, "review": 1024, "repair": 2048},
        prompt_version="web-review/v7",
        source_locations=locations(),
    )
    result = await loop.process(base())
    assert [r.prompt_task for r in generator.requests] == ["generate", "repair"]
    assert all(r.model_profile == "qwen25-14b" for r in generator.requests)
    assert [r.constraints.max_tokens for r in generator.requests] == [1536, 2048]
    assert [r.prompt_task for r in critic.requests] == ["review", "review"]
    assert all(
        r.model_profile == "qwen3-8b-nonthinking" and r.constraints.max_tokens == 1024
        for r in critic.requests
    )
    assert critic.requests[0].draft == result["versions"][0]["text"]
    assert critic.requests[1].draft == result["versions"][1]["text"]
    assert generator.requests[1].observations
    assert result["accepted_by_critic"] and not result["publication_allowed"]
    assert result["participant_display"] is None


@pytest.mark.parametrize(
    "options",
    [
        dict(critic_profile="unknown"),
        dict(generator_profile="unknown"),
        dict(stage_tokens={"generate": 2049, "review": 1, "repair": 1}),
        dict(stage_tokens={"generate": True, "review": 1, "repair": 1}),
        dict(stage_tokens={"generate": 1}),
        dict(stage_tokens={"generate": 1, "review": 1, "repair": 1, "extra": 1}),
        dict(repair_with_generator="yes"),
    ],
)
def test_invalid_explicit_profiles_and_capacities_rejected(options):
    with pytest.raises(ValueError):
        WebReviewRounds(Provider(), Provider(), budget=CallBudget(), revalidate=lambda: None, **options)


@pytest.mark.asyncio
async def test_didactic_generation_profile_reaches_only_generation_and_native_frame():
    from oralia.course_dialogue.cached_transformers import CachedTransformersGenerationAdapter
    from oralia.course_dialogue.model_prompt_profiles import STUDY_DIALOGUE
    from tests.course_dialogue.test_web_review_gpu_frames import ReviewPipe

    generator = Provider("A generated answer.")
    critic = Provider('{"status":"no_issues_found","issues":[]}')
    loop = WebReviewRounds(
        generator,
        critic,
        budget=CallBudget(maximum=2),
        revalidate=lambda: None,
        generator_profile="qwen25-14b",
        generation_didactic_profile="study-dialogue/v1",
        prompt_version="web-review/v7",
        source_locations=locations(),
    )
    await loop.process(base())
    request = generator.requests[0]
    assert (
        request.didactic_profile == "study-dialogue/v1"
        and STUDY_DIALOGUE in request.effective_messages()[0]["content"]
    )
    assert critic.requests[0].didactic_profile is None
    pipe = ReviewPipe()
    await CachedTransformersGenerationAdapter(
        pipe, repair_profile_enabled=True, model_prompt_profile="qwen25-14b"
    ).generate(request)
    assert pipe.payload["didactic_profile"] == "study-dialogue/v1"


def test_unknown_didactic_profile_cannot_be_selected():
    with pytest.raises(ValueError):
        WebReviewRounds(
            Provider(),
            Provider(),
            budget=CallBudget(),
            revalidate=lambda: None,
            generation_didactic_profile="unknown",
        )
