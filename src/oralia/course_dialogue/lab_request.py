"""Larger bounds exist only in the owned course-dialogue laboratory worker."""

from typing import Literal

from pydantic import Field

from oralia.course_dialogue.generation_limits import REPAIR_TEXT_LIMIT
from oralia.infrastructure.generation.generation_port import (
    GenerationConstraints,
    GenerationMessage,
    GenerationRequest,
)


class LabGenerationConstraints(GenerationConstraints):
    deadline_ms: int = Field(default=50000, ge=1, le=50000)
    max_tokens: int = Field(default=768, ge=1, le=768)


class LabGenerationRequest(GenerationRequest):
    constraints: LabGenerationConstraints = Field(default_factory=LabGenerationConstraints)


class RepairGenerationConstraints(LabGenerationConstraints):
    deadline_ms: int = Field(default=180000, ge=1, le=180000)
    max_tokens: int = Field(default=2048, ge=1, le=2048)


class RepairGenerationMessage(GenerationMessage):
    content: str = Field(min_length=1, max_length=REPAIR_TEXT_LIMIT)


class RepairGenerationRequest(LabGenerationRequest):
    """Opt-in offline assistant-reviewed repair; never ordinary study turn."""

    generation_profile: Literal["repair-expanded/v1"] = "repair-expanded/v1"
    constraints: RepairGenerationConstraints = Field(default_factory=RepairGenerationConstraints)
    conversation_history: list[RepairGenerationMessage] = Field(default_factory=list, max_length=8)
    output_schema: None = None
    # Probability (reranker) that the best retrieved page answers the question; None when the retriever has none.
    retrieval_relevance: float | None = Field(default=None, ge=0, le=1)
