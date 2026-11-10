"""FR-013: select the conversational action for a turn — respond, ask, re_ask, clarify,
acknowledge_missing_info, summarize or finish."""

from __future__ import annotations

from typing import Literal

ActionType = Literal["respond", "ask", "re_ask", "clarify", "acknowledge_missing_info", "summarize", "finish"]

_INTENT_TO_ACTION: dict[str, ActionType] = {
    "acknowledge_missing_info": "acknowledge_missing_info",
    "clarify": "clarify",
    "respond": "respond",
}


def select_action(intent: str, *, blocked: bool) -> ActionType:
    """Deterministic selection (research.md §2): no LLM, a documented rule table."""
    if blocked:
        return "clarify"
    return _INTENT_TO_ACTION.get(intent, "respond")
