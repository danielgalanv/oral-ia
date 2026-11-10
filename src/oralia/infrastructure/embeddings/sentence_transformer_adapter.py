"""``sentence-transformers`` EmbeddingAdapter (research.md §3).

Resources must already exist locally. The loader receives ``local_files_only=True``;
missing resources fail without a remote fallback or mutation of process environment.
"""

from __future__ import annotations

import threading
from typing import Protocol

DEFAULT_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


class EmbeddingAdapter(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]: ...


class SentenceTransformerEmbeddingAdapter:
    """One cached resident, keyed by model and revision, serialized during loading.

    Switching identity replaces the cache reference. In-flight callers may retain
    their own reference until encode finishes; no unbounded model registry is kept.
    """

    _model = None
    _model_identity: tuple[str, str | None] | None = None
    _lock = threading.Lock()

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL_NAME,
        *,
        revision: str | None = None,
        device: str | None = None,
        normalize: bool = False,
    ) -> None:
        self._model_name = model_name
        self._revision = revision
        if device not in {None, "cpu"}:
            raise ValueError("only explicit CPU is supported by this option")
        self._device = device
        self._normalize = normalize

    def _get_model(self):
        identity = (self._model_name, self._revision, self._device)
        cls = SentenceTransformerEmbeddingAdapter
        with cls._lock:
            if cls._model is None or cls._model_identity != identity:
                from sentence_transformers import SentenceTransformer

                options = {"local_files_only": True}
                if self._device is not None:
                    options["device"] = self._device
                if self._revision is not None:
                    options["revision"] = self._revision
                model = SentenceTransformer(self._model_name, **options)
                # Publish only a successfully loaded identity. Failed loads leave
                # the prior cache intact and never return it for another request.
                cls._model = model
                cls._model_identity = identity
            return cls._model

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        options = {"convert_to_numpy": True}
        if self._normalize:
            options["normalize_embeddings"] = True
        vectors = self._get_model().encode(texts, **options)
        return [vector.tolist() for vector in vectors]
