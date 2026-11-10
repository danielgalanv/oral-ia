"""Pure Qwen3 mode binding and final-answer separation; no model imports."""

import hashlib
import json

THINKING_MODEL = "qwen3-8b-thinking"
THINKING_BUDGET = "review-thinking/v1"


def thinking_selection(runtime, requested, enabled):
    if type(enabled) is not bool or (requested is not None and type(requested) is not bool):
        raise ValueError("Thinking flags must be explicit booleans")
    if runtime is not None and runtime["model_profile"] == THINKING_MODEL:
        if not enabled or requested is False:
            raise ValueError("Thinking reviewer requires explicit capability and matching mode")
        return True
    if enabled or requested is True:
        raise ValueError("Thinking is allowed only for the registered review checkpoint")
    if runtime is not None:
        expected = runtime["chat_options"].get("enable_thinking")
        if requested is False and expected is None:
            raise ValueError("Thinking flag incompatible with checkpoint family")
        return expected
    return requested


def split_thinking_output(ids, tokenizer):
    """Decode only the final channel; reasoning is represented by counts and digest."""
    opening = tokenizer.convert_tokens_to_ids("<think>")
    closing = tokenizer.convert_tokens_to_ids("</think>")
    if (opening, closing) != (151667, 151668):
        raise ValueError("Pinned Qwen3 reasoning markers changed")
    digest = hashlib.sha256(json.dumps(ids).encode("ascii")).hexdigest()
    closes = [i for i, value in enumerate(ids) if value == closing]
    opens = [i for i, value in enumerate(ids) if value == opening]
    valid = len(closes) == 1 and (not opens or opens == [0])
    boundary = closes[0] + 1 if valid else len(ids)
    final_ids = ids[boundary:] if valid else []
    text = tokenizer.decode(final_ids, skip_special_tokens=True) if valid else ""
    if "<think>" in text or "</think>" in text:
        valid, text = False, ""
    status = (
        "separated" if valid and text.strip() else "empty_final" if valid else "missing_or_invalid_end_marker"
    )
    return text, dict(
        status=status,
        reasoning_tokens=boundary,
        final_tokens=len(final_ids),
        total_tokens=len(ids),
        output_ids_sha256=digest,
    )


def validate_thinking_result(result):
    meta = result.get("thinking_output")
    observed = (result.get("generation_state") or {}).get("explicit_generate_kwargs", {})
    if (
        result.get("enable_thinking") is not True
        or result.get("sampling_profile") != "qwen3-thinking-sampling/v1"
    ):
        raise ValueError("Thinking mode not confirmed")
    if any(
        observed.get(k) != v
        for k, v in dict(do_sample=True, temperature=0.6, top_p=0.95, top_k=20, min_p=0.0).items()
    ):
        raise ValueError("Thinking sampling not confirmed")
    if not isinstance(meta, dict) or set(meta) != {
        "status",
        "reasoning_tokens",
        "final_tokens",
        "total_tokens",
        "output_ids_sha256",
    }:
        raise ValueError("Thinking separation receipt missing or malformed")
    if meta["status"] not in {"separated", "empty_final", "missing_or_invalid_end_marker"}:
        raise ValueError("Unknown thinking separation status")
    for key in ("reasoning_tokens", "final_tokens", "total_tokens"):
        if type(meta[key]) is not int or meta[key] < 0:
            raise ValueError("Invalid thinking token count")
    digest = meta["output_ids_sha256"]
    if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise ValueError("Invalid output token digest")
    if meta["reasoning_tokens"] + meta["final_tokens"] != meta["total_tokens"] or meta[
        "total_tokens"
    ] != result.get("output_tokens"):
        raise ValueError("Thinking token counts inconsistent")
    if "<think>" in result["text"] or "</think>" in result["text"]:
        raise ValueError("Reasoning markers leaked into final text")
    if (meta["status"] == "separated") != bool(result["text"].strip()):
        raise ValueError("Final text and separation status disagree")
    return meta
