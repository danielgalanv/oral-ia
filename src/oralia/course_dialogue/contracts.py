"""Closed candidate contract; deliberately distinct from T090 OutputProposal."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Closed(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Segment(Closed):
    kind: Literal["literal", "paraphrase", "illustrative_example", "comprehension_question"]
    text: str = Field(min_length=1, max_length=3000)
    source_id: str = Field(min_length=1, max_length=100)
    source_quote: str = Field(min_length=1, max_length=1500)
    assumptions: list[str] = Field(default_factory=list, max_length=6)

    @model_validator(mode="after")
    def example_assumptions(self):
        if self.kind == "illustrative_example" and not self.assumptions:
            raise ValueError("A hypothetical example requires explicit assumptions")
        if self.kind != "illustrative_example" and self.assumptions:
            raise ValueError("Assumptions belong only to hypothetical examples")
        return self


class Context(Closed):
    topic: str = Field(min_length=1, max_length=150)
    objective: str = Field(min_length=1, max_length=300)
    strategy: str = Field(min_length=1, max_length=150)
    pending_question: str | None = Field(max_length=500)


class Candidate(Closed):
    schema_version: Literal[1] = 1
    segments: list[Segment] = Field(min_length=1, max_length=8)
    context: Context

    def render_for_inspection(self):
        return "\n\n".join(f"[{s.kind}] {s.text}" for s in self.segments)


class CandidateV2(Closed):
    """Compact lab-only answer. References are claims to inspect, not approval."""

    schema_version: Literal[2] = 2
    answer: str = Field(min_length=1, max_length=3000)
    source_ids: list[str] = Field(default_factory=list, max_length=4)
    example: str | None = Field(default=None, max_length=1200)
    assumptions: list[str] = Field(default_factory=list, max_length=4)
    question: str | None = Field(default=None, max_length=500)
    limitation: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def evidence_or_limit(self):
        if not self.source_ids and not self.limitation:
            raise ValueError("An answer without references must state its evidence limit")
        if self.example and not self.assumptions:
            raise ValueError("A hypothetical example requires explicit assumptions")
        return self

    def render_for_inspection(self):
        parts = [self.answer]
        if self.example:
            parts.append("Ejemplo hipotético: " + self.example)
            parts.append("Supuestos del ejemplo: " + "; ".join(self.assumptions))
        if self.limitation:
            parts.append("Límite: " + self.limitation)
        if self.question:
            parts.append(self.question)
        return "\n\n".join(parts)


class CandidateV3(CandidateV2):
    """Compact laboratory output; a strict bound, never a truncation rule."""

    schema_version: Literal[3] = 3
    answer: str = Field(min_length=1, max_length=400)
    example: str | None = Field(default=None, max_length=200)
    assumptions: list[Annotated[str, Field(min_length=1, max_length=70)]] = Field(
        default_factory=list, max_length=2
    )
    question: str | None = Field(default=None, max_length=100)
    limitation: str | None = Field(default=None, max_length=120)


class CandidateV4(Closed):
    """One coherent lab reply plus references and explicit fictional assumptions."""

    schema_version: Literal[4] = 4
    body: str = Field(min_length=1, max_length=3500)
    source_ids: list[str] = Field(default_factory=list, max_length=6)
    modes: list[Literal["documentary", "inference", "fictional_example"]] = Field(min_length=1, max_length=3)
    fictional_assumptions: list[str] = Field(default_factory=list, max_length=4)

    @model_validator(mode="after")
    def explicit_scope(self):
        if len(set(self.modes)) != len(self.modes):
            raise ValueError("Duplicate response mode")
        if "documentary" in self.modes and not self.source_ids:
            raise ValueError("Documentary body requires source ids")
        if "fictional_example" in self.modes:
            if not self.fictional_assumptions or "ejemplo hipotético" not in self.body.casefold():
                raise ValueError("Fictional example and assumptions must be explicit")
        elif self.fictional_assumptions:
            raise ValueError("Assumptions require a fictional example")
        if "inference" in self.modes and "inferencia" not in self.body.casefold():
            raise ValueError("Inference must be labelled in the displayed body")
        if not self.source_ids and "límite de fuentes" not in self.body.casefold():
            raise ValueError("Uncited body must state its source limit")
        return self

    def render_for_inspection(self):
        if "fictional_example" in self.modes:
            return self.body + "\n\nSupuestos ficticios: " + "; ".join(self.fictional_assumptions)
        return self.body
