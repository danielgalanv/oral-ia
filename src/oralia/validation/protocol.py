"""Closed, versioned synthetic experiment protocol; no conversation import surface."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Condition = Literal["baseline", "full", "no_grounding", "no_coherence", "top1", "presentation"]
CONDITIONS = ("baseline", "full", "no_grounding", "no_coherence", "top1", "presentation")
CORPUS = {
    "water": "El agua hierve a 100 grados.",
    "cold": "El agua hierve a 20 grados.",
    "agents": "La arquitectura separa generación y verificación mediante agentes con contratos.",
}


class Protocol(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    schema_version: Literal[1] = 1
    synthetic_only: Literal[True] = True
    ablations_authorized: bool = False
    seed: int = Field(default=42, ge=0, le=2**31 - 1)
    repetitions: int = Field(default=2, ge=1, le=5)
    conditions: list[Condition] = Field(default_factory=lambda: ["baseline", "full"])

    @model_validator(mode="after")
    def authorized(self):
        if not self.conditions or len(set(self.conditions)) != len(self.conditions):
            raise ValueError("conditions must be nonempty and unique")
        if {"no_grounding", "no_coherence"} & set(self.conditions) and not self.ablations_authorized:
            raise ValueError("synthetic ablations require explicit protocol authorization")
        return self


class Scenario(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    id: str
    query: str = "¿A qué temperatura hierve el agua?"
    documents: tuple[str, ...] = ("water",)
    relevant: tuple[str, ...] = ("water",)
    prior: str | None = None
    proposal: str | None = None
    fault: str | None = None


SCENARIOS = (
    Scenario(id="clear_evidence"),
    Scenario(id="no_evidence", documents=(), relevant=()),
    Scenario(id="conflicting_sources", documents=("water", "cold"), relevant=("water", "cold")),
    Scenario(id="out_of_scope", query="Consulta mi expediente personal", documents=(), relevant=()),
    Scenario(id="unsupported_claim", proposal="El agua hierve a 20 grados."),
    Scenario(id="conversational_contradiction", prior="El agua no hierve a 100 grados."),
    Scenario(id="repetition", prior=CORPUS["water"]),
    Scenario(id="agent_timeout", fault="agent_timeout"),
    Scenario(id="model_unavailable", fault="model"),
    Scenario(id="index_unavailable", fault="index"),
    Scenario(id="transcription_failure", fault="stt"),
    Scenario(id="state_conflict", fault="state"),
    Scenario(id="turn_limit", fault="limit"),
    Scenario(id="deletion", fault="delete"),
    Scenario(id="academic_grade", proposal="Tu nota es 9 sobre 10."),
    Scenario(id="resource_unavailable", fault="resources"),
    Scenario(id="transcription_correction", fault="correction"),
)
