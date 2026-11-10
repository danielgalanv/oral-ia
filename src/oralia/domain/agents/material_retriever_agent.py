"""MaterialRetrieverAgent (Executable/AgentContract) — contracts/material-retriever-agent.md.

FR-017, FR-018: returns fragments with full provenance for an authorized query,
respecting ``max_fragments``/``time_budget_ms``, in a reproducible order (FR-020).

This module is extended additively by later user stories in this same feature: US4 adds
authorization/vigencia filtering and blocked-attempt logging (``_is_retrievable``,
``_authorized``), US6 adds conflict detection — see the Dependencies section of
tasks.md for why US2/US4/US6 all touch this one file in sequence.

T085 (H08, research.md §14.1/§14.2): replaces the single fixed-window candidate query
with deterministic progressive widening (``_run_widening_search``) that stops on the
first applicable condition (max_fragments reached, time_budget_ms exhausted, corpus
exhausted, or two consecutive widenings with no new candidate ids) and applies a
relevance floor (``_DEFAULT_RELEVANCE_THRESHOLD``) so an authorized, current fragment
that is not actually relevant to the query is no longer returned as if it were. The
``time_budget_ms`` checks in this task remain cooperative (checked between rounds),
never preemptive — unchanged by T086 below.

T086 (H10, research.md §12/§12.1, T091 reproduction): ``self._embedder.embed(...)``
and ``self._store.query(...)`` now run off the event loop thread via
``BoundedBlockingWorker`` (``infrastructure/concurrency/blocking_retrieval_worker.py``)
— a capacity-bounded worker shared across every ``MaterialRetrieverAgent`` instance,
never a private per-agent primitive, since production constructs a new instance per
request. This gives ``run_with_deadline``'s ``asyncio.wait_for`` (Feature 001,
unchanged) an actual suspension point to preempt at. ``execute()`` MUST NOT catch the
resulting ``asyncio.CancelledError`` to fabricate a ``status = "ok"`` partial result —
that is `run_with_deadline`'s job, exactly as for any other agent. All SQLAlchemy
access, conflict detection/recording, trace logging, and result construction remain
synchronous on the event loop thread, never inside the worker.
"""

from __future__ import annotations

import math
import time
from collections.abc import Callable

from sqlalchemy.orm import Session as SASession

from oralia.domain.agents.agent import AgentContractSchema
from oralia.domain.agents.agent_contract import AgentRequest, AgentResult, CancellationToken
from oralia.domain.materials.conflict_detector import ConflictCandidate, detect_conflicts
from oralia.infrastructure.concurrency.blocking_retrieval_worker import (
    BoundedBlockingWorker,
    default_blocking_retrieval_worker,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from oralia.infrastructure.embeddings.sentence_transformer_adapter import (
    EmbeddingAdapter,
    SentenceTransformerEmbeddingAdapter,
)
from oralia.infrastructure.vector_store.chroma_store import ChromaVectorStore, VectorStore

CONTRACT = AgentContractSchema(
    agent_id="material-retriever",
    version="1.0.0",
    purpose="Recuperación de fragmentos autorizados con procedencia trazable (research.md §1)",
    input_schema_ref="contracts/material-retriever-agent.md#MaterialRetrieverAgent.input",
    output_schema_ref="contracts/material-retriever-agent.md#MaterialRetrieverAgent.output",
    timeout_ms=5000,
    confidence_semantics="no aplica — este agente no emite un veredicto, solo evidencia",
    success_criteria=[
        "fragments devueltos incluyen procedencia completa " "(document_id, document_version, location_ref)"
    ],
    trace_fields=["index_version", "fragment_count"],
)

_DEFAULT_MAX_FRAGMENTS = 5

# T085/research.md §14.1: initial candidate window — same multiplier as the retracted
# fixed-window design, but now only the FIRST round's size, not the final answer;
# widening (below) takes over from here instead of stopping after one query.
_INITIAL_OVERFETCH_MULTIPLIER = 4
# Geometric widening factor between rounds ("por ejemplo duplicando k" — this round's
# instruction; not fixed by research.md to any specific multiplier).
_WIDENING_FACTOR = 2
# research.md §14.1, condition (d): two consecutive rounds contributing no new
# candidate id are treated as "the index has nothing further to offer", independent of
# condition (c) (`len(matches) < k`) — a consecutive-round counter, not a size or set
# comparison, per this round's explicit instruction.
_STALE_ROUNDS_LIMIT = 2

# T085/research.md §14.2: relevance floor on `relevance_score` (Chroma cosine
# similarity, `1 - distance`) — measured in T090 against the project's real embedding
# model/store (paraphrase-multilingual-MiniLM-L12-v2 + ChromaVectorStore): positives
# 0.6212-0.8130, negatives 0.0583-0.2162, clean gap of 0.4050. 0.35 sits closer to the
# negative side (margin 0.134 above the worst negative vs. 0.271 below the weakest
# positive) — deliberately biased against rejecting genuinely relevant evidence.
# Single named default; configurable only at construction (never via
# `MaterialQueryInput`/the HTTP contract — this is an internal retrieval-quality knob,
# not a per-query user setting).
_DEFAULT_RELEVANCE_THRESHOLD = 0.35

_BUDGET_EXHAUSTED_WARNING = "presupuesto temporal agotado, resultado parcial"
_CORPUS_EXHAUSTED_WARNING = "corpus agotado para esta consulta"
_INSUFFICIENT_RELEVANCE_WARNING = "sin evidencia suficientemente pertinente"


def _meets_relevance_threshold(score: float, threshold: float) -> bool:
    """Non-finite scores (``NaN``, ``+inf``, ``-inf``) MUST NOT be treated as a match —
    ``float("nan") >= threshold`` is already always `False` in Python, but `+inf` would
    otherwise compare as "above any threshold"; ``math.isfinite`` rejects all three
    explicitly rather than relying on that comparison quirk. The boundary is inclusive:
    a score exactly equal to `threshold` MUST be accepted."""
    return math.isfinite(score) and score >= threshold


def _fragment_authorized_for_scope(
    fragment: models.MaterialFragment,
    document: models.MaterialDocument | None,
    *,
    course_id: str | None,
    activity_configuration_id: str | None,
) -> bool:
    """FR-019: course + activity scope — pure predicate over already-fetched SQL
    rows (no queries here). Shared, single source of truth for both
    `MaterialRetrieverAgent`'s own widening loop (T098) and Feature 003's
    `concepts_pending` queue-reuse (`get_currently_valid_fragment`, T099) — never
    duplicated, so the two call sites cannot silently diverge.

    T098 (H08/research.md §14.1a — course_id was never revalidated against SQL,
    relying solely on the `VectorStore`'s own metadata filter as a coarse
    pre-filter): when `course_id` is given, it MUST match **both**
    `fragment.course_id` and `document.course_id` — a discrepancy between the two
    denormalized copies is itself untrusted and MUST be rejected, not just an
    outright wrong course on one of them. `VectorMatch.metadata` is never consulted
    here — SQL is the only source of authorization, regardless of what the store or
    its metadata claims."""
    if course_id is not None:
        if fragment.course_id != course_id:
            return False
        if document is None or document.course_id != course_id:
            return False
    if activity_configuration_id is not None:
        if activity_configuration_id not in (fragment.activity_configuration_ids or []):
            return False
    return True


def _fragment_currently_retrievable(
    fragment: models.MaterialFragment, document: models.MaterialDocument | None
) -> bool:
    """FR-019/FR-019a: lifecycle — indexed, active document, non-retired, non-expired.
    Pure predicate over already-fetched SQL rows; shared with
    `get_currently_valid_fragment` (T099) for the same reason as
    `_fragment_authorized_for_scope`."""
    if fragment.indexing_status != "indexed":
        return False
    if document is None or document.status != "active" or document.retired_at is not None:
        return False
    if fragment.valid_until is not None and fragment.valid_until < utcnow():
        return False
    return True


def _matches_governed_material_version(db, fragment, activity_id):
    if activity_id is None:
        return True
    governance = db.get(models.ActivityGovernance, activity_id)
    if governance is None:
        return True
    return any(
        ref.get("document_id") == fragment.document_id and ref.get("version") == fragment.document_version
        for ref in governance.material_versions
    )


class MaterialRetrieverAgent:
    contract = CONTRACT

    def __init__(
        self,
        db: SASession,
        *,
        vector_store: VectorStore | None = None,
        embedding_adapter: EmbeddingAdapter | None = None,
        relevance_threshold: float = _DEFAULT_RELEVANCE_THRESHOLD,
        clock: Callable[[], float] = time.monotonic,
        blocking_retrieval_worker: BoundedBlockingWorker | None = None,
    ) -> None:
        self._db = db
        self._store = vector_store or ChromaVectorStore()
        self._embedder = embedding_adapter or SentenceTransformerEmbeddingAdapter()
        self._relevance_threshold = relevance_threshold
        # Injectable monotonic clock (defaults to `time.monotonic`) — lets tests
        # control elapsed-time-between-rounds deterministically (no real sleeps,
        # no global monkeypatch of the `time` module) per this round's instruction.
        self._clock = clock
        # T086 (research.md §12.1): defaults to the process-wide singleton — MUST be
        # shared across every `MaterialRetrieverAgent` instance (production
        # constructs a new one per request), never a private per-agent primitive.
        # Tests inject a smaller, isolated `BoundedBlockingWorker` via this
        # parameter so a burst in one test cannot affect another's capacity
        # accounting — never exposed through `MaterialQueryInput`/the HTTP contract.
        self._worker = blocking_retrieval_worker or default_blocking_retrieval_worker()

    async def execute(self, request: AgentRequest, cancellation: CancellationToken) -> AgentResult:
        started = self._clock()
        data = request.input
        query_text = str(data.get("query_text", ""))
        course_id = data.get("course_id")
        activity_configuration_id = data.get("activity_configuration_id")
        session_id = data.get("session_id")
        max_fragments = int(data.get("max_fragments", _DEFAULT_MAX_FRAGMENTS))
        time_budget_ms = int(data.get("time_budget_ms", request.deadline_ms))

        if max_fragments <= 0:
            # Defensive guard (T085, documented fissure from T090): with the previous
            # single fixed-window query, `max_fragments <= 0` still reached the store
            # (Chroma floors `n_results` to 1 regardless of the requested `k`) and the
            # post-append break check let up to one fragment through — never the
            # `fragments = []` a non-positive limit implies. Returning immediately,
            # before ever calling `self._store.query(...)`, closes that gap without
            # touching the HTTP schema (still not validated/rejected there — see the
            # follow-up task registered in tasks.md, out of scope for T085).
            return AgentResult(
                status="ok",
                output={
                    "fragments": [],
                    "index_version": self._store.get_index_version(),
                    "warnings": [],
                    "conflicts": [],
                },
                confidence=None,
                trace={"index_version": self._store.get_index_version(), "fragment_count": 0},
            )

        # T086: off the event loop thread via the shared, capacity-bounded worker —
        # `execute()` MUST NOT catch the `asyncio.CancelledError` this `await` can
        # raise (run_with_deadline, Feature 001, turns that into `status = "timeout"`
        # exactly as for any other agent — research.md §12).
        vector = (await self._worker.run(self._embedder.embed, [query_text]))[0] if query_text else []

        warnings: list[str] = []
        if vector:
            selected, blocked_out_of_scope, budget_exhausted, corpus_exhausted, relevance_rejected = (
                await self._run_widening_search(
                    vector=vector,
                    course_id=course_id,
                    activity_configuration_id=activity_configuration_id,
                    max_fragments=max_fragments,
                    time_budget_ms=time_budget_ms,
                    started=started,
                )
            )
        else:
            selected, blocked_out_of_scope = [], False
            budget_exhausted = corpus_exhausted = relevance_rejected = False

        # Priority order (§5 of this round): an empty result caused exclusively by
        # candidates that were structurally valid (authorized/current) but below the
        # relevance floor MUST report that specific cause, never the generic
        # corpus-exhaustion warning — and a budget warning MUST NOT describe a corpus
        # that was, in fact, examined completely.
        if not selected and relevance_rejected:
            warnings.append(_INSUFFICIENT_RELEVANCE_WARNING)
        elif corpus_exhausted and len(selected) < max_fragments:
            warnings.append(_CORPUS_EXHAUSTED_WARNING)
        if budget_exhausted:
            warnings.append(_BUDGET_EXHAUSTED_WARNING)

        if blocked_out_of_scope and session_id is not None:
            # No real Session row exists for a direct/technical query (session_id is
            # null there per contract) — TraceEvent.session_id has an enforced FK, so
            # tracing only applies to genuine participant sessions (Feature 003's
            # conversational flow always supplies one).
            self._log_blocked_attempt(
                session_id=session_id,
                course_id=course_id,
                activity_configuration_id=activity_configuration_id,
                query_text=query_text,
            )

        fragments_out = [
            {
                "fragment_id": fragment.id,
                "document_id": fragment.document_id,
                "document_version": fragment.document_version,
                "location_ref": fragment.location_ref,
                "text": fragment.text,
                "relevance_score": relevance_score,
            }
            for fragment, relevance_score in selected
        ]

        conflicts_out = self._detect_and_record_conflicts(selected, query_text)

        output = {
            "fragments": fragments_out,
            "index_version": self._store.get_index_version(),
            "warnings": warnings,
            "conflicts": conflicts_out,
        }
        return AgentResult(
            status="ok",
            output=output,
            confidence=None,
            trace={"index_version": output["index_version"], "fragment_count": len(fragments_out)},
        )

    async def _run_widening_search(
        self,
        *,
        vector: list[float],
        course_id: str | None,
        activity_configuration_id: str | None,
        max_fragments: int,
        time_budget_ms: int,
        started: float,
    ) -> tuple[list[tuple[models.MaterialFragment, float]], bool, bool, bool, bool]:
        """T085/research.md §14.1: deterministic progressive widening — replaces the
        single fixed-window `store.query(...)` call. Returns
        `(selected, blocked_out_of_scope, budget_exhausted, corpus_exhausted, relevance_rejected)`.

        Each round re-queries the store from scratch with a larger `k` (geometric
        widening, `_WIDENING_FACTOR`) — the returned list is the store's own current
        top-`k` by relevance, not an increment to append to a prior round's list. The
        selection is therefore rebuilt fresh from THIS round's order every round
        (`selected = [...]` below, never `selected.extend(...)`) so an earlier, smaller
        round's ordering can never take precedence over the store's most recent
        ranking, and duplicates across rounds cannot occur (a single query never
        repeats an id, and a later round's full re-ranking supersedes, rather than
        follows, the previous one).

        SQL is queried only for fragment ids not already in `fragment_rows_cache`
        (`seen_ids` accumulates every id ever seen, purely to drive the SQL cache and
        the two-consecutive-stale-rounds counter below — it does not gate the rebuilt
        `selected` list, which is derived directly from each round's `matches`).

        Stop conditions, checked in this order once a round's query+SQL+filtering has
        completed (`time_budget_ms` is additionally checked *before* each round's
        query, so a budget already exhausted before starting a round never issues it):
        (1) `len(selected) >= max_fragments` — enough authorized, current, relevant
        candidates. (2) elapsed time exceeds `time_budget_ms` — whatever this round
        already produced is kept, cooperative only (T086, not this task, is what would
        make this preemptive). (3) `len(matches) < k` — the store returned fewer
        candidates than requested: the corpus has nothing further to offer for this
        query/filter. (4) `_STALE_ROUNDS_LIMIT` consecutive rounds contributed no new
        candidate id at all — a consecutive-round counter (reset the moment a round
        does contribute a new id), independent of (3), for the edge case where `k`
        stays below `collection.count()` yet widening stops surfacing anything new."""
        seen_ids: set[str] = set()
        fragment_rows_cache: dict[str, models.MaterialFragment] = {}
        # T098: batched alongside `fragment_rows_cache` so `MaterialDocument` is
        # fetched at most once per distinct `document_id` for the whole search (not
        # once per candidate per round) — needed now that authorization itself
        # (course_id) depends on the document row too, not just lifecycle.
        document_rows_cache: dict[str, models.MaterialDocument] = {}
        selected: list[tuple[models.MaterialFragment, float]] = []
        blocked_out_of_scope = False
        relevance_rejected = False
        budget_exhausted = False
        corpus_exhausted = False
        stale_rounds = 0
        k = max(max_fragments * _INITIAL_OVERFETCH_MULTIPLIER, max_fragments)

        while True:
            if self._elapsed_ms(started) >= time_budget_ms:
                budget_exhausted = True
                break

            # T086: off the event loop thread via the same shared, capacity-bounded
            # worker as `embed` above — every round's `query()` is its own genuine
            # cancellation point now, not just the first.
            matches = await self._worker.run(self._store.query, vector, {"course_id": course_id}, k)

            new_ids = [m.fragment_id for m in matches if m.fragment_id not in seen_ids]
            stale_rounds = 0 if new_ids else stale_rounds + 1
            seen_ids.update(m.fragment_id for m in matches)

            rows_to_fetch = [fid for fid in new_ids if fid not in fragment_rows_cache]
            if rows_to_fetch:
                rows = (
                    self._db.query(models.MaterialFragment)
                    .filter(models.MaterialFragment.id.in_(rows_to_fetch))
                    .all()
                )
                for row in rows:
                    fragment_rows_cache[row.id] = row

            doc_ids_to_fetch = {
                fragment_rows_cache[fid].document_id
                for fid in new_ids
                if fid in fragment_rows_cache
                and fragment_rows_cache[fid].document_id not in document_rows_cache
            }
            if doc_ids_to_fetch:
                doc_rows = (
                    self._db.query(models.MaterialDocument)
                    .filter(models.MaterialDocument.id.in_(doc_ids_to_fetch))
                    .all()
                )
                for doc_row in doc_rows:
                    document_rows_cache[doc_row.id] = doc_row

            selected = []
            used_ids: set[str] = set()
            round_blocked = False
            round_relevance_rejected = False
            for match in matches:
                if match.fragment_id in used_ids:
                    # Defensive: a single store query never repeats an id in
                    # practice, but the contract ("eliminando duplicados por
                    # fragment_id, conservando la primera aparición") MUST hold even
                    # against a malformed/duplicated candidate list — first
                    # occurrence wins, later ones are skipped outright.
                    continue
                used_ids.add(match.fragment_id)
                fragment = fragment_rows_cache.get(match.fragment_id)
                if fragment is None:
                    continue
                # T098: `VectorMatch.metadata` is intentionally never read here — only
                # already-fetched SQL rows decide authorization (`_authorized` below).
                document = document_rows_cache.get(fragment.document_id)
                if not self._authorized(fragment, document, activity_configuration_id, course_id):
                    round_blocked = True
                    continue
                if not self._is_retrievable(fragment, document):
                    continue
                if not _meets_relevance_threshold(match.relevance_score, self._relevance_threshold):
                    round_relevance_rejected = True
                    continue
                selected.append((fragment, match.relevance_score))
                if len(selected) >= max_fragments:
                    break
            blocked_out_of_scope = blocked_out_of_scope or round_blocked
            relevance_rejected = relevance_rejected or round_relevance_rejected

            if self._elapsed_ms(started) >= time_budget_ms:
                budget_exhausted = True
                break
            if len(selected) >= max_fragments:
                break
            if len(matches) < k:
                corpus_exhausted = True
                break
            if stale_rounds >= _STALE_ROUNDS_LIMIT:
                corpus_exhausted = True
                break

            k *= _WIDENING_FACTOR

        return selected, blocked_out_of_scope, budget_exhausted, corpus_exhausted, relevance_rejected

    def _elapsed_ms(self, started: float) -> float:
        return (self._clock() - started) * 1000

    def _authorized(
        self,
        fragment: models.MaterialFragment,
        document: models.MaterialDocument | None,
        activity_configuration_id: str | None,
        course_id: str | None,
    ) -> bool:
        """FR-019: course + activity scope. Thin delegate to the shared,
        module-level `_fragment_authorized_for_scope` (T098) so this agent's own
        loop and Feature 003's queue-reuse (`get_currently_valid_fragment`, T099)
        can never apply diverging policies. A fragment with no activity assignments
        yet is not authorized for any activity-scoped query."""

        return _matches_governed_material_version(
            self._db, fragment, activity_configuration_id
        ) and _fragment_authorized_for_scope(
            fragment, document, course_id=course_id, activity_configuration_id=activity_configuration_id
        )

    def _is_retrievable(
        self, fragment: models.MaterialFragment, document: models.MaterialDocument | None
    ) -> bool:
        """FR-019/FR-019a: active, indexed, non-retired, non-expired. Thin delegate
        to the shared `_fragment_currently_retrievable` (T098) — see `_authorized`."""

        return _fragment_currently_retrievable(fragment, document)

    def _detect_and_record_conflicts(
        self, selected: list[tuple[models.MaterialFragment, float]], query_text: str
    ) -> list[dict]:
        """FR-022/FR-022a: flag conflicting evidence and persist a MaterialConflictRecord
        (deduplicated against any still-unreviewed record for the same fragment pair —
        FR-022b)."""

        candidates = [
            ConflictCandidate(fragment_id=fragment.id, document_id=fragment.document_id, text=fragment.text)
            for fragment, _ in selected
        ]
        conflicts_out: list[dict] = []
        for a, b in detect_conflicts(candidates):
            record = self._get_or_create_conflict_record(a, b, query_text)
            conflicts_out.append(
                {
                    "conflict_record_id": record.id,
                    "document_ids": record.document_ids,
                    "conflicting_claims": record.conflicting_claims,
                }
            )
        return conflicts_out

    def _get_or_create_conflict_record(
        self, a: ConflictCandidate, b: ConflictCandidate, query_text: str
    ) -> models.MaterialConflictRecord:
        fragment_ids = sorted([a.fragment_id, b.fragment_id])
        pending = (
            self._db.query(models.MaterialConflictRecord)
            .filter(models.MaterialConflictRecord.review_status == "pending_review")
            .all()
        )
        for record in pending:
            if sorted(record.fragment_ids or []) == fragment_ids:
                return record

        record = models.MaterialConflictRecord(
            document_ids=sorted({a.document_id, b.document_id}),
            fragment_ids=fragment_ids,
            conflicting_claims=[a.text, b.text],
            detected_by_query=query_text,
            review_status="pending_review",
        )
        self._db.add(record)
        self._db.flush()
        return record

    def _log_blocked_attempt(
        self,
        *,
        session_id: str,
        course_id: str | None,
        activity_configuration_id: str | None,
        query_text: str,
    ) -> None:
        """FR-026: an out-of-scope retrieval attempt is blocked and traced — never
        silently dropped."""

        from oralia.application.services import trace_service

        trace_service.record_event(
            self._db,
            session_id=session_id,
            event_type="material_retrieval_blocked_out_of_scope",
            payload={"course_id": course_id, "activity_configuration_id": activity_configuration_id},
            memory_category="metacognitive",
        )


def get_currently_valid_fragment(
    db: SASession,
    fragment_id: str,
    *,
    course_id: str | None,
    activity_configuration_id: str | None,
) -> models.MaterialFragment | None:
    """T099 (Feature 002, follow-up to T085): shared, additive revalidation policy —
    used by callers that reuse a *previously* retrieved/enqueued fragment id (e.g.
    `self_study_agency_composer.py`'s `concepts_pending` queue-continuity mechanism)
    and MUST NOT presume that authorization/vigencia granted at some earlier point
    still holds now. Deliberately NOT wired into `MaterialRetrieverAgent._authorized`/
    `_is_retrievable` or its own widening loop — those own `blocked_out_of_scope`/
    FR-026 trace-logging side effects, and adding `course_id` there is T098's
    still-unimplemented scope, not this one. This function has no side effects; it
    only reads.

    T098 note: this now delegates to the exact same shared predicates
    (`_fragment_authorized_for_scope`/`_fragment_currently_retrievable`) that
    `MaterialRetrieverAgent`'s own widening loop uses — including course_id, which
    this function already checked before T098 wired the same check into the
    agent's own loop. The two call sites cannot diverge because they share one
    implementation, not two copies of the same rules.

    Returns the fragment row if and only if it currently passes every check below,
    else `None` (including when the row no longer exists at all):
    - `fragment.course_id == course_id` and `document.course_id == course_id`
      (`course_id=None` skips this check — mirrors `_authorized`'s treatment of a
      `None` scope filter as "no restriction requested");
    - `activity_configuration_id in fragment.activity_configuration_ids`
      (`activity_configuration_id=None` skips this check, same rationale);
    - `fragment.indexing_status == "indexed"`;
    - `document.status == "active"` and `document.retired_at is None`;
    - `fragment.valid_until` is `None` or still in the future.
    """
    fragment = db.get(models.MaterialFragment, fragment_id)
    if fragment is None:
        return None
    document = db.get(models.MaterialDocument, fragment.document_id)
    if not _matches_governed_material_version(db, fragment, activity_configuration_id):
        return None
    if not _fragment_authorized_for_scope(
        fragment, document, course_id=course_id, activity_configuration_id=activity_configuration_id
    ):
        return None
    if not _fragment_currently_retrievable(fragment, document):
        return None
    return fragment
