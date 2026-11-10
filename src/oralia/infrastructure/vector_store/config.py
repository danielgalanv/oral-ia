"""Local persistent ChromaDB directory location (research.md §2)."""

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_VECTOR_STORE_PATH = "./.oralia_data/vector_store"


def get_vector_store_path() -> str:
    return os.environ.get("ORALIA_VECTOR_STORE_PATH", DEFAULT_VECTOR_STORE_PATH)


def ensure_vector_store_dir(path: str | None = None) -> str:
    resolved = path or get_vector_store_path()
    Path(resolved).mkdir(parents=True, exist_ok=True)
    return resolved
