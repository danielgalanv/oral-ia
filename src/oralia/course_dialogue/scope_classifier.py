"""Fallible laboratory scope classifier; never authorizes academic output."""

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from oralia.course_dialogue.context import plan_context
from oralia.course_dialogue.rag_lab import ScopeAssessment
from oralia.infrastructure.generation.generation_port import GenerationConstraints, GenerationRequest

PROMPT_PATH = Path(__file__).with_name("scope_classifier_prompt.txt")


class Span(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    start: int = Field(ge=0)
    end: int = Field(gt=0)
    quote: str = Field(min_length=1, max_length=4000)

    def extract(self, text):
        if self.start >= self.end or self.end > len(text) or text[self.start : self.end] != self.quote:
            raise ValueError("scope span does not match literal question")
        return self.quote


class ScopeSelection(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    status: Literal["in_scope", "out_of_scope", "uncertain_scope", "mixed", "operational"]
    included_block: str | None
    excluded_block: str | None
    standalone: bool
    included: Span | None
    excluded: Span | None
    referent_turn: int | None = Field(ge=0)


@dataclass(frozen=True)
class ScopeResult:
    assessment: ScopeAssessment
    rag_question: str | None
    selection: ScopeSelection
    request: GenerationRequest
    outcome: object
    policy_sha256: str
    publication_allowed: bool = False


def shown_history(history):
    """Only explicitly shown rows may supply a referent; reject silent clipping."""
    if len(history) > 4:
        raise ValueError("scope history limit")
    result = []
    for row in history:
        if not row.get("displayed_text") or row.get("displayed_kind") not in {
            "laboratory_preview",
            "candidate",
            "operational",
        }:
            raise ValueError("scope history must be actually shown")
        if any(not isinstance(row.get(k), str) or len(row[k]) > 4000 for k in ("input", "displayed_text")):
            raise ValueError("scope history field limit")
        result.append({k: row[k] for k in ("input", "displayed_text", "displayed_kind")})
    return result


def bind_selection(selection, text, history, policy, policy_hash):
    """Check structure and literal segmentation; semantic accuracy needs evaluation."""
    if selection.referent_turn is not None and selection.referent_turn >= len(history):
        raise ValueError("scope referent not shown")
    if selection.status in {"in_scope", "mixed"}:
        if selection.included_block not in policy["included_blocks"]:
            raise ValueError("scope included block not in policy")
    elif selection.included_block is not None or selection.included is not None:
        raise ValueError("unexpected included block or span")
    if selection.status in {"out_of_scope", "mixed"}:
        if selection.excluded_block not in policy["excluded_as_standalone_blocks_for_this_activity"]:
            raise ValueError("scope excluded block not in policy")
        if not selection.standalone:
            raise ValueError("scope exclusion is not standalone")
    elif selection.excluded_block is not None or selection.excluded is not None or selection.standalone:
        raise ValueError("unexpected exclusion")
    for span in (selection.included, selection.excluded):
        if span is not None:
            span.extract(text)
    if selection.status == "mixed":
        if selection.included is None or selection.excluded is None:
            raise ValueError("mixed scope requires both literal spans")
        a, b = selection.included, selection.excluded
        if not (a.end <= b.start or b.end <= a.start):
            raise ValueError("mixed scope spans overlap")
        # Do not add history/resolved query here: it may contain the excluded part.
        rag_question = a.extract(text)
    elif selection.status == "in_scope":
        rag_question = text
    else:
        rag_question = None
    assessment = ScopeAssessment(
        selection.status,
        authority_ref=policy_hash,
        reason="fallible_local_scope_classifier_not_content_verification",
        in_scope_question=rag_question if selection.status == "mixed" else None,
        excluded_part=selection.excluded.quote if selection.excluded else None,
        block_id=selection.included_block,
        excluded_block_id=selection.excluded_block,
        standalone_excluded_block=selection.standalone,
    )
    assessment.validate()
    return assessment, rag_question


async def classify_scope(text, history, *, provider, binding, db):
    if not isinstance(text, str) or not text.strip() or len(text) > 4000:
        raise ValueError("scope question limit")
    history = shown_history(history)
    policy = binding.revalidate(db)
    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    payload = {
        "policy_sha256": binding.policy_sha256,
        "included_blocks": policy["included_blocks"],
        "excluded_blocks": policy["excluded_as_standalone_blocks_for_this_activity"],
        "boundary_rules": policy.get("boundary_rules", {}),
        "question": text,
        "resolved_query_hint_not_authority": plan_context(text, history).academic_query,
        "shown_history": history,
    }
    request = GenerationRequest(
        purpose="explicacion",
        instruction=prompt,
        student_input=json.dumps(payload, ensure_ascii=False),
        general_knowledge_allowed=False,
        output_schema=ScopeSelection.model_json_schema(),
        constraints=GenerationConstraints(max_tokens=256, deadline_ms=30000),
    )
    binding.revalidate(db)
    outcome = await provider.generate(request)
    policy = binding.revalidate(db)
    if not outcome.ok or outcome.finish_reason != "stop":
        raise ValueError("scope generation incomplete")
    selection = ScopeSelection.model_validate_json(outcome.text)
    assessment, rag_question = bind_selection(selection, text, history, policy, binding.policy_sha256)
    binding.assert_decision(assessment, policy)
    return ScopeResult(assessment, rag_question, selection, request, outcome, binding.policy_sha256)


def prompt_sha256():
    return hashlib.sha256(PROMPT_PATH.read_bytes()).hexdigest()
