"""Opt-in scope contract v2; v1 and participant routes are unchanged."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

from oralia.course_dialogue.context import plan_context
from oralia.course_dialogue.scope_classifier import ScopeSelection, Span, bind_selection, shown_history
from oralia.infrastructure.generation.generation_port import GenerationConstraints, GenerationRequest

PROMPT = Path(__file__).with_name("scope_classifier_v2_prompt.txt")
INTENTS = {
    "included_request": ("in_scope", False),
    "included_with_supporting_mention": ("in_scope", False),
    "excluded_standalone_request": ("out_of_scope", True),
    "included_and_excluded_standalone_requests": ("mixed", True),
    "unclear_request": ("uncertain_scope", False),
    "session_operation": ("operational", False),
}


class ScopeSelectionV2(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    primary_intent: Literal[
        "included_request",
        "included_with_supporting_mention",
        "excluded_standalone_request",
        "included_and_excluded_standalone_requests",
        "unclear_request",
        "session_operation",
    ]
    included_block: str | None
    excluded_block: str | None
    included: Span | None
    excluded: Span | None
    supporting_mention: Span | None
    referent_turn: int | None


@dataclass(frozen=True)
class BoundScopeV2:
    selection: ScopeSelectionV2
    assessment: object
    rag_question: str | None
    referent_turn: int | None
    publication_allowed: bool = False


def bind_v2(selection, text, history, policy, policy_hash):
    if selection.referent_turn is not None and (
        selection.referent_turn < 0 or selection.referent_turn >= len(history)
    ):
        raise ValueError("v2 referent must be shown")
    auxiliary = selection.primary_intent == "included_with_supporting_mention"
    if auxiliary:
        if selection.included_block not in policy["included_blocks"] or selection.supporting_mention is None:
            raise ValueError("supporting mention needs an included anchor and literal witness")
        selection.supporting_mention.extract(text)
    elif selection.supporting_mention is not None:
        raise ValueError("unexpected supporting mention")
    status, standalone = INTENTS[selection.primary_intent]
    if status != "mixed" and (selection.included is not None or selection.excluded is not None):
        raise ValueError("literal question parts are reserved for mixed requests")
    derived = ScopeSelection(
        status=status,
        standalone=standalone,
        included_block=selection.included_block,
        excluded_block=selection.excluded_block,
        included=selection.included,
        excluded=selection.excluded,
        referent_turn=selection.referent_turn,
    )
    assessment, question = bind_selection(derived, text, history, policy, policy_hash)
    return BoundScopeV2(selection, assessment, question, selection.referent_turn)


async def classify_scope_v2(text, history, *, provider, binding, db, metadata=None):
    """Metadata is separate and optional for contract-only offline evaluation."""
    if not isinstance(text, str) or not text.strip() or len(text) > 4000:
        raise ValueError("v2 question limit")
    history = shown_history(history)
    policy = binding.revalidate(db)
    descriptions = metadata.revalidate(binding, policy) if metadata is not None else None
    payload = {
        "contract_version": 2,
        "policy_sha256": binding.policy_sha256,
        "included_blocks": policy["included_blocks"],
        "excluded_blocks": policy["excluded_as_standalone_blocks_for_this_activity"],
        "boundary_rules": policy.get("boundary_rules", {}),
        "question": text,
        "shown_history": history,
        "resolved_query_hint_not_authority": plan_context(text, history).academic_query,
        "block_descriptions": descriptions,
        "block_metadata_sha256": metadata.sha256 if metadata is not None else None,
    }
    request = GenerationRequest(
        purpose="explicacion",
        instruction=PROMPT.read_text(encoding="utf-8"),
        student_input=json.dumps(payload, ensure_ascii=False),
        general_knowledge_allowed=False,
        output_schema=ScopeSelectionV2.model_json_schema(),
        constraints=GenerationConstraints(max_tokens=256, deadline_ms=30000),
    )
    policy = binding.revalidate(db)
    if metadata is not None:
        metadata.revalidate(binding, policy)
    outcome = await provider.generate(request)
    policy = binding.revalidate(db)
    if metadata is not None:
        metadata.revalidate(binding, policy)
    if not outcome.ok or outcome.finish_reason != "stop":
        raise ValueError("v2 generation incomplete")
    result = bind_v2(
        ScopeSelectionV2.model_validate_json(outcome.text), text, history, policy, binding.policy_sha256
    )
    binding.assert_decision(result.assessment, policy)
    return result, request, outcome
