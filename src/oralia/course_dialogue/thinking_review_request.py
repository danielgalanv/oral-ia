"""Explicit review-only capacity for Qwen3 reasoning; ordinary budgets unchanged."""

from typing import Literal

from pydantic import Field

from oralia.course_dialogue.lab_request import RepairGenerationConstraints
from oralia.course_dialogue.web_review_rounds import WebRoundRequest


class ThinkingReviewConstraints(RepairGenerationConstraints):
    max_tokens: int = Field(default=8192, ge=1, le=8192)


class ThinkingReviewRequest(WebRoundRequest):
    model_profile: Literal["qwen3-8b-thinking"] = "qwen3-8b-thinking"
    prompt_task: Literal["review"] = "review"
    constraints: ThinkingReviewConstraints = Field(default_factory=ThinkingReviewConstraints)


def thinking_review_request(request, max_tokens=8192):
    if request.prompt_task != "review":
        raise ValueError("Thinking capacity is review-only")
    data = request.model_dump()
    data["model_profile"] = "qwen3-8b-thinking"
    data["constraints"]["max_tokens"] = max_tokens
    return ThinkingReviewRequest.model_validate(data)
