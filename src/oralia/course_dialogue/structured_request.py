"""Opt-in typed task data; existing laboratory request remains unchanged."""

from typing import Literal

from pydantic import Field, model_validator

from oralia.course_dialogue.lab_request import RepairGenerationRequest
from oralia.course_dialogue.model_prompt_profiles import PROFILES, render_messages


class StructuredGenerationRequest(RepairGenerationRequest):
    model_profile: str
    prompt_task: Literal["generate", "review", "repair"]
    didactic_profile: (
        Literal["study-dialogue/v1", "study-dialogue/v2", "study-dialogue/v3", "study-dialogue/v4"] | None
    ) = None
    question: str = Field(min_length=1, max_length=2000)
    draft: str | None = Field(default=None, max_length=16000)
    observations: list[dict] = Field(default_factory=list, max_length=5)
    obligations: list[str] = Field(default_factory=list, max_length=10)

    @model_validator(mode="after")
    def validate_renderer(self):
        if self.model_profile not in PROFILES:
            raise ValueError("Unknown checkpoint profile")
        self.effective_messages()
        return self

    def effective_messages(self):
        return render_messages(
            self.model_profile,
            self.prompt_task,
            self.question,
            [e.model_dump() for e in self.evidence],
            self.draft,
            self.observations,
            self.obligations,
            [m.model_dump() for m in self.conversation_history],
            didactic_profile=self.didactic_profile,
        )


def structured_request(
    base,
    *,
    model_profile,
    task,
    question=None,
    draft=None,
    observations=None,
    obligations=None,
    didactic_profile=None,
):
    return StructuredGenerationRequest(
        purpose=base.purpose,
        instruction="Host renderer structured/v1",
        student_input="",
        model_profile=model_profile,
        prompt_task=task,
        didactic_profile=didactic_profile,
        question=question or base.student_input,
        evidence=base.evidence,
        conversation_history=[m.model_dump() for m in base.conversation_history],
        constraints=base.constraints.model_dump(),
        draft=draft,
        observations=observations or [],
        obligations=obligations or [],
        general_knowledge_allowed=False,
    )
