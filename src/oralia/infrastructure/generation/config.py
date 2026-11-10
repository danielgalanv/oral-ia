"""Generation configuration (research.md §1/§4/§5 of Feature 003) — env-var driven, same
pattern as `infrastructure/vector_store/config.py` (Feature 002)."""

from __future__ import annotations

import os
from contextvars import ContextVar

activity_model: ContextVar[str | None] = ContextVar("oralia_activity_model", default=None)

DEFAULT_OLLAMA_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_OLLAMA_TIMEOUT_MS = 6000
DEFAULT_OLLAMA_TEMPERATURE = 0.2
DEFAULT_OLLAMA_MAX_TOKENS = 256
DEFAULT_PRACTICE_REGEN_MAX_ATTEMPTS = 2
DEFAULT_DISCLOSURE_OVERLAP_THRESHOLD = 0.3
DEFAULT_COHERENCE_NO_PROGRESS_WINDOW = 3
DEFAULT_COHERENCE_REPETITION_WINDOW = 1


def get_ollama_base_url() -> str:
    return os.environ.get("ORALIA_OLLAMA_BASE_URL", DEFAULT_OLLAMA_BASE_URL)


def get_ollama_model() -> str | None:
    """No default — MUST be configured explicitly (research.md §1); `None` means the
    agent MUST NOT invoke `OllamaGenerationAdapter` at all."""
    selected = activity_model.get()
    if selected == "deterministic":
        return None
    if selected and selected.startswith("ollama:"):
        return selected.removeprefix("ollama:")
    return os.environ.get("ORALIA_OLLAMA_MODEL") or None


def get_ollama_timeout_ms() -> int:
    return int(os.environ.get("ORALIA_OLLAMA_TIMEOUT_MS", DEFAULT_OLLAMA_TIMEOUT_MS))


def get_ollama_temperature() -> float:
    value = float(os.environ.get("ORALIA_OLLAMA_TEMPERATURE", DEFAULT_OLLAMA_TEMPERATURE))
    return max(0.0, min(1.0, value))


def get_ollama_max_tokens() -> int:
    value = int(os.environ.get("ORALIA_OLLAMA_MAX_TOKENS", DEFAULT_OLLAMA_MAX_TOKENS))
    if not 64 <= value <= 512:
        raise ValueError("ORALIA_OLLAMA_MAX_TOKENS must be between 64 and 512")
    return value


def get_practice_regen_max_attempts() -> int:
    return int(os.environ.get("ORALIA_PRACTICE_REGEN_MAX_ATTEMPTS", DEFAULT_PRACTICE_REGEN_MAX_ATTEMPTS))


def get_disclosure_overlap_threshold() -> float:
    return float(os.environ.get("ORALIA_DISCLOSURE_OVERLAP_THRESHOLD", DEFAULT_DISCLOSURE_OVERLAP_THRESHOLD))


def get_coherence_no_progress_window() -> int:
    return int(os.environ.get("ORALIA_COHERENCE_NO_PROGRESS_WINDOW", DEFAULT_COHERENCE_NO_PROGRESS_WINDOW))


def get_coherence_repetition_window() -> int:
    return int(os.environ.get("ORALIA_COHERENCE_REPETITION_WINDOW", DEFAULT_COHERENCE_REPETITION_WINDOW))
