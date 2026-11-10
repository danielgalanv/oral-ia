"""Explicit reasoning mode, review-only capacity and final-channel transport."""

import json

import pytest

from oralia.course_dialogue.cached_transformers import CachedTransformersGenerationAdapter
from oralia.course_dialogue.generation_limits import validate_budget_frame
from oralia.course_dialogue.model_prompt_profiles import resolve_runtime, snapshot_path
from oralia.course_dialogue.qwen_thinking import split_thinking_output, thinking_selection
from oralia.course_dialogue.thinking_review_request import thinking_review_request
from oralia.infrastructure.generation.generation_port import GenerationError
from tests.course_dialogue.test_web_review_gpu_frames import ReviewPipe
from tests.course_dialogue.test_web_review_minimal import request


def test_mode_is_pinned_to_checkpoint_sampler_and_capability():
    profile = resolve_runtime(
        snapshot_path("qwen3-8b-thinking"), "qwen3-8b-thinking", "qwen3-thinking-sampling/v1"
    )
    assert profile["chat_options"] == {"enable_thinking": True}
    assert profile["generate_kwargs"] == dict(
        do_sample=True, temperature=0.6, top_p=0.95, top_k=20, min_p=0.0
    )
    assert thinking_selection(profile, None, True) is True
    for sampling in ["greedy/v1", "qwen3-nonthinking-sampling/v1"]:
        with pytest.raises(ValueError):
            resolve_runtime(snapshot_path("qwen3-8b-thinking"), "qwen3-8b-thinking", sampling)
    for requested, enabled in [(False, True), (None, False), (1, True), (True, 1)]:
        with pytest.raises(ValueError):
            thinking_selection(profile, requested, enabled)
    with pytest.raises(ValueError):
        thinking_selection(None, True, True)


class Tokenizer:
    def convert_tokens_to_ids(self, value):
        return {"<think>": 151667, "</think>": 151668}[value]

    def decode(self, ids, **kwargs):
        assert 99 not in ids, "Reasoning must never be decoded for display"
        return "{}" if 42 in ids else ""


@pytest.mark.parametrize("ids", [[99, 151668, 42], [151667, 99, 151668, 42]])
def test_only_final_ids_are_decoded(ids):
    text, meta = split_thinking_output(ids, Tokenizer())
    assert text == "{}" and meta["status"] == "separated"
    assert meta["reasoning_tokens"] + meta["final_tokens"] == len(ids)
    assert len(meta["output_ids_sha256"]) == 64 and "reasoning_content" not in meta


@pytest.mark.parametrize("ids", [[99], [99, 151668], [99, 151668, 42, 151668], [99, 151667, 151668, 42]])
def test_incomplete_or_malformed_thinking_never_becomes_a_verdict(ids):
    text, meta = split_thinking_output(ids, Tokenizer())
    assert not text and meta["status"] != "separated"


def test_large_budget_requires_exact_profile_task_and_capability():
    req = thinking_review_request(request())
    assert req.constraints.max_tokens == 8192
    frame = dict(
        budget_profile="review-thinking/v1",
        max_tokens=8192,
        deadline_ms=180000,
        construction_profile="structured/v1",
        prompt_task="review",
        model_prompt_profile="qwen3-8b-thinking",
    )
    assert validate_budget_frame(frame, thinking_review_enabled=True) == "review-thinking/v1"
    for patch in [
        dict(prompt_task="repair"),
        dict(model_prompt_profile="qwen3-8b-nonthinking"),
        dict(max_tokens=8193),
        dict(finite_outputs=["{}"]),
    ]:
        with pytest.raises(ValueError):
            validate_budget_frame({**frame, **patch}, thinking_review_enabled=True)
    with pytest.raises(ValueError):
        validate_budget_frame(frame, repair_enabled=True)
    with pytest.raises(ValueError):
        thinking_review_request(request("repair"))


class ThinkingPipe(ReviewPipe):
    def __init__(self, change=None):
        super().__init__()
        self.change = change

    async def readline(self):
        row = json.loads(await super().readline())
        row.update(
            budget_profile="review-thinking/v1",
            text='{"status":"no_issues_found","issues":[]}',
            enable_thinking=True,
            sampling_profile="qwen3-thinking-sampling/v1",
            output_tokens=3,
            generation_state=dict(
                explicit_generate_kwargs=dict(
                    do_sample=True, temperature=0.6, top_p=0.95, top_k=20, min_p=0.0
                )
            ),
            thinking_output=dict(
                status="separated",
                reasoning_tokens=1,
                final_tokens=2,
                total_tokens=3,
                output_ids_sha256="a" * 64,
            ),
        )
        if self.change == "mode":
            row["enable_thinking"] = False
        if self.change == "sampling":
            row["generation_state"]["explicit_generate_kwargs"]["temperature"] = 0.7
        if self.change == "counts":
            row["thinking_output"]["final_tokens"] = 99
        if self.change == "missing":
            del row["thinking_output"]
        if self.change == "leak":
            row["text"] = "<think>hidden</think>{}"
        if self.change == "partial":
            row.update(text="", finish_reason="length")
            row["thinking_output"].update(
                status="missing_or_invalid_end_marker", reasoning_tokens=3, final_tokens=0
            )
        return json.dumps(row).encode()


@pytest.mark.asyncio
@pytest.mark.parametrize("change", [None, "partial"])
async def test_actual_adapter_keeps_reasoning_separate_and_incomplete_unusable(change):
    pipe = ThinkingPipe(change)
    port = CachedTransformersGenerationAdapter(
        pipe,
        repair_profile_enabled=True,
        model_prompt_profile="qwen3-8b-thinking",
        thinking_review_enabled=True,
    )
    result = await port.generate(thinking_review_request(request()))
    assert result.ok == (change is None)
    assert (
        result.parameters["thinking_enabled"] == 1 and pipe.payload["budget_profile"] == "review-thinking/v1"
    )
    assert "hidden" not in result.text


@pytest.mark.asyncio
@pytest.mark.parametrize("change", ["mode", "sampling", "counts", "missing", "leak"])
async def test_wrong_or_missing_thinking_confirmation_stops_owned_worker(change):
    port = CachedTransformersGenerationAdapter(
        ThinkingPipe(change),
        repair_profile_enabled=True,
        model_prompt_profile="qwen3-8b-thinking",
        thinking_review_enabled=True,
    )
    with pytest.raises(GenerationError):
        await port.generate(thinking_review_request(request()))
    assert not port.usable


@pytest.mark.asyncio
async def test_loop_constructs_explicit_thinking_request_without_publishing():
    from oralia.course_dialogue.review_repair import CallBudget
    from oralia.course_dialogue.thinking_review_request import ThinkingReviewRequest
    from oralia.course_dialogue.web_review_rounds import WebReviewRounds
    from tests.course_dialogue.test_web_review_references import Provider, base, locations

    critic = Provider('{"status":"no_issues_found","issues":[]}')
    loop = WebReviewRounds(
        Provider("A generated answer."),
        critic,
        budget=CallBudget(maximum=2),
        revalidate=lambda: None,
        generator_profile="qwen25-14b",
        critic_profile="qwen3-8b-thinking",
        repair_with_generator=True,
        prompt_version="web-review/v7",
        source_locations=locations(),
    )
    result = await loop.process(base())
    assert (
        isinstance(critic.requests[0], ThinkingReviewRequest)
        and critic.requests[0].constraints.max_tokens == 8192
    )
    assert result["accepted_by_critic"] and not result["publication_allowed"]


@pytest.mark.asyncio
async def test_regular_request_cannot_use_thinking_checkpoint_even_with_optin():
    req = request()
    req.model_profile = "qwen3-8b-thinking"
    port = CachedTransformersGenerationAdapter(
        ThinkingPipe(),
        repair_profile_enabled=True,
        model_prompt_profile="qwen3-8b-thinking",
        thinking_review_enabled=True,
    )
    with pytest.raises(GenerationError):
        await port.generate(req)
    assert port.process.payload is None


def test_repair_budget_cannot_bypass_review_only_thinking_guard():
    with pytest.raises(ValueError):
        validate_budget_frame(
            dict(
                budget_profile="repair-expanded/v1",
                max_tokens=2048,
                deadline_ms=180000,
                model_prompt_profile="qwen3-8b-thinking",
                prompt_task="repair",
            ),
            repair_enabled=True,
            thinking_review_enabled=True,
        )
