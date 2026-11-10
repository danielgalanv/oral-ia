"""GenerationPort: the interface `ResponseGeneratorAgent`/`PracticeQuestionAgent` depend
on (contracts/self-study-agents.md). Existing participant defaults remain Ollama and
Deterministic. Feature012 adds an explicit candidate-only cached-CUDA adapter on
this same port; no new agent or approval authority is introduced.
"""

from __future__ import annotations

from typing import Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field

GenerationPurpose = Literal[
    "explicacion",
    "explicacion_progresiva",
    "ejemplo",
    "comparacion",
    "estructura_exposicion",
    "pregunta_practica",
    "resumen",
    "repregunta",
]


class GenerationConstraints(BaseModel):
    deadline_ms: int = Field(default=6000, ge=1, le=30000)
    material_excerpt_version: Literal[1, 2] = 1
    max_tokens: int = 256
    reveal_solution: bool = False


class EvidenceItem(BaseModel):
    fragment_id: str
    text: str
    document_id: str
    document_version: int


class GenerationMessage(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class GenerationRequest(BaseModel):
    purpose: GenerationPurpose
    instruction: str
    student_input: str = ""
    evidence: list[EvidenceItem] = Field(default_factory=list)
    concepts_addressed: list[str] = Field(default_factory=list)
    conversation_history: list[GenerationMessage] = Field(default_factory=list, max_length=8)
    output_schema: dict | None = None
    general_knowledge_allowed: bool = False
    constraints: GenerationConstraints = Field(default_factory=GenerationConstraints)


class GenerationOutcome(BaseModel):
    ok: bool
    text: str
    internal_expected_answer: str | None = None
    adapter: Literal["ollama", "deterministic", "transformers_local", "llama_server"]
    finish_reason: Literal["stop", "length", "deadline"] | None = None
    model: str | None = None
    parameters: dict[str, float | int] = Field(default_factory=dict)
    latency_ms: int = 0


class GenerationError(RuntimeError):
    """Raised by an adapter on an unrecoverable generation failure (research.md §1)."""


class GenerationPort(Protocol):
    async def generate(self, request: GenerationRequest) -> GenerationOutcome: ...
