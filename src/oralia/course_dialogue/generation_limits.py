"""Pure pipe-budget validation shared by host and standalone worker."""

REPAIR_PROFILE = "repair-expanded/v1"
REPAIR_TEXT_LIMIT = 16000


def validate_budget_frame(frame, *, repair_enabled=False, thinking_review_enabled=False):
    profile = frame.get("budget_profile", "historical/v1")
    if frame.get("model_prompt_profile") == "qwen3-8b-thinking" and profile != "review-thinking/v1":
        raise ValueError("Thinking checkpoint requires its review-only budget")
    if profile == "review-thinking/v1" and thinking_review_enabled:
        if (
            frame.get("construction_profile") != "structured/v1"
            or frame.get("prompt_task") != "review"
            or frame.get("model_prompt_profile") != "qwen3-8b-thinking"
            or (
                frame.get("finite_outputs") is not None
                and not (
                    frame.get("web_review_prompt_version")
                    in {"web-control/v3", "web-control/v4", "web-control/v5"}
                    and frame.get("finite_after_thinking") is True
                )
            )
        ):
            raise ValueError("Thinking budget is restricted to the registered free review")
        tokens, milliseconds = 8192, 180000
    elif profile == REPAIR_PROFILE and repair_enabled:
        tokens, milliseconds = 2048, 180000
        if frame.get("finite_outputs") is not None:
            raise ValueError("Expanded repair is free text only")
    elif profile == "historical/v1":
        tokens, milliseconds = 768, 50000
    else:
        raise ValueError("Unknown or disabled budget profile")
    if (
        type(frame.get("max_tokens")) is not int
        or type(frame.get("deadline_ms")) is not int
        or not 1 <= frame["max_tokens"] <= tokens
        or not 1 <= frame["deadline_ms"] <= milliseconds
    ):
        raise ValueError("Generation budget outside explicit profile capacity")
    return profile
