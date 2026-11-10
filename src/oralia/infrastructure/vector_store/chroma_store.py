"""ChromaDB-backed VectorStore (research.md §2).

Chroma metadata carries only ``course_id`` — a coarse, cheap pre-filter, not an
authorization decision. Authorization (course/activity/session scope), lifecycle
state (active/inactive/retired) and vigencia (``valid_until``) are never duplicated
into Chroma metadata: SQL (``MaterialDocument``/``MaterialFragment``) stays the
single source of truth for those, so deactivating or retiring a document never
requires a second write into the vector index. Callers over-fetch by ``course_id``
and MUST revalidate ``course_id`` itself — not just "the remaining filters" — against
SQL afterwards (T098, research.md §14.1a/§14.1c): a store that ignores this filter,
or whose metadata has drifted from SQL, MUST NOT be trusted to have already enforced
it. ``VectorMatch.metadata`` in particular MUST NOT be read for authorization by any
caller — it is index information only, never a substitute for the SQL row.

Rebuild uses a blue-green collection swap (``material_fragments_v{N}``): the new
collection is fully populated before the version pointer moves, so concurrent reads are
always served from the last *complete* index (Edge Case, research.md §9) — never a
partially-rebuilt one.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Protocol

import chromadb
from chromadb.errors import NotFoundError

from oralia.infrastructure.vector_store.config import ensure_vector_store_dir

COLLECTION_PREFIX = "material_fragments_v"
_VERSION_FILE = "index_version.json"
_QUERY_MAX_ATTEMPTS = 2
_FINGERPRINT_KEY = "oralia:vector-space:v1"
_FINGERPRINT_FIELDS = {
    "encoder",
    "revision",
    "dimension",
    "normalization",
    "representation",
    "extraction",
    "chunking",
}


class VectorMatch:
    def __init__(self, fragment_id: str, metadata: dict[str, Any], relevance_score: float) -> None:
        self.fragment_id = fragment_id
        self.metadata = metadata
        self.relevance_score = relevance_score


class VectorStore(Protocol):
    def add(self, fragment_id: str, embedding: list[float], metadata: dict[str, Any]) -> None: ...

    def query(self, embedding: list[float], filters: dict[str, Any], k: int) -> list[VectorMatch]: ...

    def delete(self, fragment_id: str) -> None: ...

    def rebuild(self, items: list[tuple[str, list[float], dict[str, Any]]]) -> str: ...

    def get_index_version(self) -> str: ...


class ChromaVectorStore:
    def __init__(self, path: str | None = None, *, fingerprint: dict[str, Any] | None = None) -> None:
        # None is the historical interface, never accreditation for a new experiment.
        self._fingerprint = None
        self._dimension = None
        if fingerprint is not None:
            if set(fingerprint) != _FINGERPRINT_FIELDS:
                raise ValueError("incomplete vector-space fingerprint")
            dimension = fingerprint["dimension"]
            if type(dimension) is not int or dimension < 1:
                raise ValueError("invalid fingerprint dimension")
            if any(
                not isinstance(fingerprint[k], str) or not fingerprint[k].strip()
                for k in _FINGERPRINT_FIELDS - {"dimension"}
            ):
                raise ValueError("fingerprint fields must identify explicit versions and policies")
            self._dimension = dimension
            self._fingerprint = json.dumps(fingerprint, sort_keys=True, separators=(",", ":"))
        self._path = ensure_vector_store_dir(path)
        self._client = chromadb.PersistentClient(path=self._path)
        self._version = self._load_version()

    def _version_file(self) -> Path:
        return Path(self._path) / _VERSION_FILE

    def _load_version(self) -> int:
        vf = self._version_file()
        if vf.exists():
            return int(json.loads(vf.read_text(encoding="utf-8"))["version"])
        self._write_version_atomic(1)
        return 1

    def _write_version_atomic(self, version: int) -> None:
        version_file = self._version_file()
        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=version_file.parent,
                prefix=f".{version_file.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary:
                json.dump({"version": version}, temporary)
                temporary.flush()
                os.fsync(temporary.fileno())
                temporary_path = Path(temporary.name)
            os.replace(temporary_path, version_file)
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()

    def _collection_name(self, version: int | None = None) -> str:
        return f"{COLLECTION_PREFIX}{version if version is not None else self._version}"

    def _collection(self):
        collection = self._client.get_collection(self._collection_name())
        self._check_fingerprint(collection)
        return collection

    def _metadata(self):
        metadata = {"hnsw:space": "cosine"}
        if self._fingerprint is not None:
            metadata[_FINGERPRINT_KEY] = self._fingerprint
        return metadata

    def _check_fingerprint(self, collection):
        actual = (collection.metadata or {}).get(_FINGERPRINT_KEY)
        if self._fingerprint is None:
            if actual is not None:
                raise ValueError("fingerprinted index requires explicit vector-space identity")
            return
        if actual is None:
            raise ValueError("unaccredited legacy index; preserve it and build a separate version explicitly")
        if actual != self._fingerprint:
            raise ValueError("vector-space fingerprint mismatch; separate index required")

    def _check_dimension(self, embedding):
        if self._dimension is not None and len(embedding) != self._dimension:
            raise ValueError("embedding dimension disagrees with vector-space fingerprint")

    def _writable_collection(self):
        collection = self._client.get_or_create_collection(self._collection_name(), metadata=self._metadata())
        self._check_fingerprint(collection)
        return collection

    def get_index_version(self) -> str:
        return str(self._version)

    def add(self, fragment_id: str, embedding: list[float], metadata: dict[str, Any]) -> None:
        self._check_dimension(embedding)
        self._writable_collection().upsert(ids=[fragment_id], embeddings=[embedding], metadatas=[metadata])

    def delete(self, fragment_id: str) -> None:
        self._collection().delete(ids=[fragment_id])

    def query(self, embedding: list[float], filters: dict[str, Any], k: int) -> list[VectorMatch]:
        self._check_dimension(embedding)
        for attempt in range(_QUERY_MAX_ATTEMPTS):
            try:
                collection = self._collection()
                count = collection.count()
                if count == 0:
                    return []
                result = collection.query(
                    query_embeddings=[embedding],
                    n_results=min(max(k, 1), count),
                    where=filters or None,
                )
                matches: list[VectorMatch] = []
                ids = result.get("ids", [[]])[0]
                metadatas = result.get("metadatas", [[]])[0]
                distances = result.get("distances", [[]])[0]
                for fid, meta, dist in zip(ids, metadatas, distances, strict=True):
                    matches.append(VectorMatch(fragment_id=fid, metadata=meta, relevance_score=1.0 - dist))
                return matches
            except NotFoundError:
                if attempt + 1 >= _QUERY_MAX_ATTEMPTS:
                    raise
                self._version = self._load_version()

        raise AssertionError("unreachable bounded query loop")

    def rebuild(self, items: list[tuple[str, list[float], dict[str, Any]]]) -> str:
        for _, embedding, _ in items:
            self._check_dimension(embedding)
        # Writers are serialized by the application's index rebuild lock. A store
        # may predate the preceding writer: refresh the committed pointer before
        # choosing a candidate, or deleting N+1 could delete the active index.
        self._version = self._load_version()
        new_version = self._version + 1
        new_name = self._collection_name(new_version)
        try:
            self._client.delete_collection(new_name)
        except NotFoundError:
            pass
        new_collection = self._client.create_collection(new_name, metadata=self._metadata())
        if items:
            new_collection.upsert(
                ids=[item[0] for item in items],
                embeddings=[item[1] for item in items],
                metadatas=[item[2] for item in items],
            )
        # Swap the pointer only after the new collection is fully populated — readers
        # resolve "current" via this file, so an in-progress rebuild never affects them.
        self._write_version_atomic(new_version)
        self._version = new_version
        retired_version = new_version - 2
        if retired_version >= 1:
            try:
                self._client.delete_collection(self._collection_name(retired_version))
            except NotFoundError:
                pass
        return str(new_version)
