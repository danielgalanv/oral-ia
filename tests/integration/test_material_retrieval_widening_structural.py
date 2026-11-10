"""T085 (H08, research.md §14.1/§14.2) — structural tests for the progressive
widening search, the relevance floor, and their side-effect boundaries
(`MaterialRetrieverAgent._run_widening_search`). Complements, without duplicating,
`tests/integration/test_material_retrieval_h08_reproduction.py` (T090's frozen
outcome-only reproductions) — these tests instead pin down internal mechanics that
T090 deliberately does not couple to: round count, dedup, order, stop-condition
identity, and side-effect cardinality.

Reuses the harness (`_OrderedCandidateVectorStore`, `_FixedEmbeddingAdapter`,
`_make_course_and_document`, `_make_fragment`, `_request`) from the T090 module
instead of duplicating it.
"""

from __future__ import annotations

import math
import uuid

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.material_retriever_agent import MaterialRetrieverAgent
from oralia.infrastructure.vector_store.chroma_store import VectorMatch
from tests.integration.test_material_retrieval_h08_reproduction import (
    _FixedEmbeddingAdapter,
    _make_course_and_document,
    _make_fragment,
    _OrderedCandidateVectorStore,
    _request,
)


class _CyclingVectorStore:
    """Double for the "two consecutive stale rounds" stop condition: for `k` beyond
    the underlying candidate count, keeps returning exactly `k` items (never fewer —
    `len(matches) < k` MUST NOT be what stops this loop) by cycling through the same
    ids, so every round beyond the first contributes zero NEW fragment ids. Confirms
    the stop condition is a genuine consecutive-round counter, not a size or set-only
    comparison."""

    def __init__(self, candidates: list[VectorMatch]) -> None:
        self._candidates = candidates
        self.queried_k: list[int] = []

    def query(self, embedding, filters, k):  # noqa: ANN001
        self.queried_k.append(k)
        n = len(self._candidates)
        return [self._candidates[i % n] for i in range(k)]

    def add(self, *a, **kw):
        raise NotImplementedError

    def delete(self, *a, **kw):
        raise NotImplementedError

    def rebuild(self, *a, **kw):
        raise NotImplementedError

    def get_index_version(self) -> str:
        return "test-version"


class _SpyVectorStore:
    """Wraps a real double, recording every `k` requested — used to assert a store
    was (or was not) queried at all, e.g. for `max_fragments <= 0`."""

    def __init__(self, delegate) -> None:
        self._delegate = delegate
        self.query_calls = 0

    def query(self, embedding, filters, k):  # noqa: ANN001
        self.query_calls += 1
        return self._delegate.query(embedding, filters, k)

    def add(self, *a, **kw):
        raise NotImplementedError

    def delete(self, *a, **kw):
        raise NotImplementedError

    def rebuild(self, *a, **kw):
        raise NotImplementedError

    def get_index_version(self) -> str:
        return "test-version"


class _FakeClock:
    """Deterministic, injectable monotonic clock (seconds) — returns the next value
    from a fixed sequence on each call, repeating the last one if called more times
    than provided (defensive, never raises)."""

    def __init__(self, values: list[float]) -> None:
        self._values = values
        self._i = 0

    def __call__(self) -> float:
        value = self._values[min(self._i, len(self._values) - 1)]
        self._i += 1
        return value


@pytest.mark.integration
async def test_multiple_widenings_recover_the_two_valid_fragments_beyond_them(db_session):
    """max_fragments=2 -> initial k=8. Requires THREE rounds (k=8,16,32) before the
    two valid fragments (positions 17-18 of 18) are ever fetched — confirms genuine
    multi-round widening, not just a single larger window."""
    course, invalid_document = _make_course_and_document(db_session, activity_configuration_ids=["act-other"])
    _, valid_document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    valid_document.course_id = course.id
    db_session.add(valid_document)
    db_session.flush()

    candidates: list[VectorMatch] = []
    for i in range(16):
        frag = _make_fragment(
            db_session,
            document=invalid_document,
            course_id=course.id,
            activity_configuration_ids=["act-other"],
        )
        candidates.append(VectorMatch(frag.id, {}, 0.95 - i * 0.01))
    valid_ids = []
    for i in range(2):
        frag = _make_fragment(
            db_session, document=valid_document, course_id=course.id, activity_configuration_ids=["act-1"]
        )
        valid_ids.append(frag.id)
        candidates.append(VectorMatch(frag.id, {}, 0.80 - i * 0.01))

    store = _OrderedCandidateVectorStore(candidates)
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(course.id, "act-1", max_fragments=2), CancellationToken())

    returned_ids = [f["fragment_id"] for f in result.output["fragments"]]
    assert returned_ids == valid_ids
    assert store.queried_k == [8, 16, 32], f"expected three widening rounds, got {store.queried_k!r}"


@pytest.mark.integration
async def test_final_order_matches_relevance_order_of_the_last_useful_query(db_session):
    """The output order MUST match the relevance order of the round that actually
    produced the final selection — not, e.g., insertion/document order."""
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    frag_low = _make_fragment(
        db_session, document=document, course_id=course.id, activity_configuration_ids=["act-1"]
    )
    frag_high = _make_fragment(
        db_session, document=document, course_id=course.id, activity_configuration_ids=["act-1"]
    )
    # Store returns the higher-relevance fragment first, deliberately created second —
    # if the agent leaked creation/insertion order instead of the store's order, this
    # would catch it.
    candidates = [VectorMatch(frag_high.id, {}, 0.9), VectorMatch(frag_low.id, {}, 0.6)]
    store = _OrderedCandidateVectorStore(candidates)
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(course.id, "act-1", max_fragments=5), CancellationToken())

    returned_ids = [f["fragment_id"] for f in result.output["fragments"]]
    assert returned_ids == [frag_high.id, frag_low.id]


@pytest.mark.integration
async def test_duplicate_id_within_a_round_appears_once_keeping_first_occurrence(db_session):
    """A malformed/duplicated candidate list (same fragment_id twice in one round)
    MUST NOT produce a duplicate in the output — first occurrence wins."""
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    frag = _make_fragment(
        db_session, document=document, course_id=course.id, activity_configuration_ids=["act-1"]
    )
    candidates = [VectorMatch(frag.id, {}, 0.9), VectorMatch(frag.id, {}, 0.5)]
    store = _OrderedCandidateVectorStore(candidates)
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(course.id, "act-1", max_fragments=5), CancellationToken())

    fragments = result.output["fragments"]
    assert [f["fragment_id"] for f in fragments] == [frag.id]
    assert fragments[0]["relevance_score"] == 0.9  # first occurrence's score, not the second's


@pytest.mark.integration
async def test_two_consecutive_stale_rounds_terminate_the_search(db_session):
    """A store that keeps returning `len(matches) == k` (never triggering the
    corpus-exhausted condition) but recycles the same 3 ids forever MUST still
    terminate — via the consecutive-stale-round counter, not `len(matches) < k`."""
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-other"])
    candidates = [
        VectorMatch(
            _make_fragment(
                db_session,
                document=document,
                course_id=course.id,
                activity_configuration_ids=["act-other"],
            ).id,
            {},
            0.9 - i * 0.1,
        )
        for i in range(3)
    ]
    store = _CyclingVectorStore(candidates)
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(course.id, "act-1", max_fragments=1), CancellationToken())

    assert result.output["fragments"] == []
    assert store.queried_k == [4, 8, 16], (
        f"expected a bounded search that stops after two consecutive stale rounds, got {store.queried_k!r}"
    )
    assert any(w == "corpus agotado para esta consulta" for w in result.output["warnings"])


@pytest.mark.integration
async def test_fewer_matches_than_k_terminates_without_further_queries(db_session):
    """`len(matches) < k` MUST stop the search after a single round — no further
    widening once the store itself reports fewer candidates than requested."""
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-other"])
    candidates = [
        VectorMatch(
            _make_fragment(
                db_session,
                document=document,
                course_id=course.id,
                activity_configuration_ids=["act-other"],
            ).id,
            {},
            0.9,
        )
        for _ in range(3)
    ]
    store = _OrderedCandidateVectorStore(candidates)
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(course.id, "act-1", max_fragments=5), CancellationToken())

    assert result.output["fragments"] == []
    assert store.queried_k == [20], (
        f"expected exactly one query (k=5*4=20 > 3 candidates), got {store.queried_k!r}"
    )
    assert any(w == "corpus agotado para esta consulta" for w in result.output["warnings"])


@pytest.mark.integration
async def test_budget_exhausted_between_rounds_keeps_partial_results_single_warning(db_session):
    """Budget exhaustion detected BEFORE a second round MUST keep whatever the first
    round already found, and emit exactly the budget warning — never the
    corpus-exhausted one, since the search did not actually run out of corpus."""
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    frag_valid = _make_fragment(
        db_session, document=document, course_id=course.id, activity_configuration_ids=["act-1"]
    )
    invalid_document = _make_course_and_document(db_session, activity_configuration_ids=["act-other"])[1]
    invalid_document.course_id = course.id
    db_session.add(invalid_document)
    db_session.flush()
    invalid_frags = [
        _make_fragment(
            db_session,
            document=invalid_document,
            course_id=course.id,
            activity_configuration_ids=["act-other"],
        )
        for _ in range(4)
    ]
    candidates = [VectorMatch(f.id, {}, 0.9 - i * 0.01) for i, f in enumerate(invalid_frags)]
    candidates.append(VectorMatch(frag_valid.id, {}, 0.85))
    # pad round 1 (k=8)
    candidates += [VectorMatch(f.id, {}, 0.5 - i * 0.01) for i, f in enumerate(invalid_frags)]

    store = _OrderedCandidateVectorStore(candidates)
    # `_request()` uses time_budget_ms=5000. started=0.0; pre-round-1 check=0.01s
    # (10ms, within budget); post-round-1 check=0.02s (20ms, within budget) -> loop
    # continues; pre-round-2 check=6.0s (6000ms, exceeds the 5000ms budget) -> stop
    # before round 2's query.
    clock = _FakeClock([0.0, 0.01, 0.02, 6.0])
    agent = MaterialRetrieverAgent(
        db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter(), clock=clock
    )
    result = await agent.execute(_request(course.id, "act-1", max_fragments=2), CancellationToken())

    returned_ids = [f["fragment_id"] for f in result.output["fragments"]]
    assert returned_ids == [frag_valid.id]
    assert store.queried_k == [8], (
        f"expected a single round before the budget check stopped it, got {store.queried_k!r}"
    )
    assert result.output["warnings"] == ["presupuesto temporal agotado, resultado parcial"]


@pytest.mark.integration
async def test_blocked_out_of_scope_attempt_is_logged_once_across_several_widenings(db_session, monkeypatch):
    """An unauthorized candidate appearing across MULTIPLE widening rounds MUST still
    produce exactly one blocked-attempt log call per `execute()`."""
    from oralia.application.services import trace_service

    calls: list[dict] = []

    def _spy(db, **kwargs):
        calls.append(kwargs)

    monkeypatch.setattr(trace_service, "record_event", _spy)

    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-other"])
    candidates = [
        VectorMatch(
            _make_fragment(
                db_session, document=document, course_id=course.id, activity_configuration_ids=["act-other"]
            ).id,
            {},
            0.9 - i * 0.01,
        )
        for i in range(20)
    ]
    store = _OrderedCandidateVectorStore(candidates)
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    request = AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        input={
            "query_text": "consulta de prueba",
            "course_id": course.id,
            "activity_configuration_id": "act-1",
            "session_id": str(uuid.uuid4()),
            "max_fragments": 1,
            "time_budget_ms": 5000,
        },
    )
    result = await agent.execute(request, CancellationToken())

    assert result.output["fragments"] == []
    assert len(store.queried_k) >= 2, "this reproduction requires multiple widening rounds to be meaningful"
    assert len(calls) == 1, f"expected exactly one blocked-attempt log call, got {len(calls)}"


@pytest.mark.integration
async def test_discarded_candidates_never_reach_conflict_detection(db_session, monkeypatch):
    """Unauthorized, expired, and below-threshold candidates MUST NOT be passed to
    `detect_conflicts` — only the final selected fragments."""
    from oralia.domain.agents import material_retriever_agent as module

    seen_candidates: list[list] = []
    original = module.detect_conflicts

    def _spy(candidates):
        seen_candidates.append(list(candidates))
        return original(candidates)

    monkeypatch.setattr(module, "detect_conflicts", _spy)

    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    kept = _make_fragment(
        db_session, document=document, course_id=course.id, activity_configuration_ids=["act-1"]
    )
    wrong_activity_doc = _make_course_and_document(db_session, activity_configuration_ids=["act-other"])[1]
    wrong_activity_doc.course_id = course.id
    db_session.add(wrong_activity_doc)
    db_session.flush()
    unauthorized = _make_fragment(
        db_session, document=wrong_activity_doc, course_id=course.id, activity_configuration_ids=["act-other"]
    )
    low_relevance = _make_fragment(
        db_session, document=document, course_id=course.id, activity_configuration_ids=["act-1"]
    )

    candidates = [
        VectorMatch(unauthorized.id, {}, 0.95),
        VectorMatch(kept.id, {}, 0.80),
        VectorMatch(low_relevance.id, {}, 0.10),
    ]
    store = _OrderedCandidateVectorStore(candidates)
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(course.id, "act-1", max_fragments=5), CancellationToken())

    assert [f["fragment_id"] for f in result.output["fragments"]] == [kept.id]
    assert len(seen_candidates) == 1
    assert [c.fragment_id for c in seen_candidates[0]] == [kept.id]


@pytest.mark.integration
async def test_relevance_score_exactly_at_threshold_is_accepted(db_session):
    """The boundary is inclusive: `relevance_score == 0.35` MUST be accepted."""
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    frag = _make_fragment(
        db_session, document=document, course_id=course.id, activity_configuration_ids=["act-1"]
    )
    store = _OrderedCandidateVectorStore([VectorMatch(frag.id, {}, 0.35)])
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(course.id, "act-1", max_fragments=5), CancellationToken())

    assert [f["fragment_id"] for f in result.output["fragments"]] == [frag.id]


@pytest.mark.integration
async def test_relevance_score_immediately_below_threshold_is_rejected(db_session):
    """A score infinitesimally below the threshold MUST be rejected — confirms the
    comparison, not just widely-separated measured values."""
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    frag = _make_fragment(
        db_session, document=document, course_id=course.id, activity_configuration_ids=["act-1"]
    )
    store = _OrderedCandidateVectorStore([VectorMatch(frag.id, {}, 0.349999)])
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(course.id, "act-1", max_fragments=5), CancellationToken())

    assert result.output["fragments"] == []
    assert any(w == "sin evidencia suficientemente pertinente" for w in result.output["warnings"])


@pytest.mark.integration
async def test_non_finite_relevance_scores_are_never_returned(db_session):
    """NaN/+inf/-inf MUST all be discarded safely — none of them count as "meeting"
    the threshold, even though a naive `score >= threshold` comparison would let
    `float("inf")` through."""
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    frags = [
        _make_fragment(
            db_session, document=document, course_id=course.id, activity_configuration_ids=["act-1"]
        )
        for _ in range(3)
    ]
    candidates = [
        VectorMatch(frags[0].id, {}, math.nan),
        VectorMatch(frags[1].id, {}, math.inf),
        VectorMatch(frags[2].id, {}, -math.inf),
    ]
    store = _OrderedCandidateVectorStore(candidates)
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(course.id, "act-1", max_fragments=5), CancellationToken())

    assert result.output["fragments"] == []
    assert any(w == "sin evidencia suficientemente pertinente" for w in result.output["warnings"])


@pytest.mark.integration
async def test_h08b_mixed_contrast_keeps_relevant_and_excludes_both_irrelevant(db_session):
    """New test for the T090 mixed contrast (0.70 kept, 0.20 and 0.10 excluded) — the
    historical T090 assertion (`test_h08b_relevant_fragment_above_threshold_is_kept`)
    only checks inclusion of the relevant candidate; this test additionally asserts
    the two irrelevant ones are excluded, without touching that historical test."""
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    relevant = _make_fragment(
        db_session, document=document, course_id=course.id, activity_configuration_ids=["act-1"]
    )
    noise = [
        _make_fragment(
            db_session, document=document, course_id=course.id, activity_configuration_ids=["act-1"]
        )
        for _ in range(2)
    ]
    candidates = [
        VectorMatch(relevant.id, {}, 0.70),
        VectorMatch(noise[0].id, {}, 0.20),
        VectorMatch(noise[1].id, {}, 0.10),
    ]
    store = _OrderedCandidateVectorStore(candidates)
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(course.id, "act-1", max_fragments=5), CancellationToken())

    returned_ids = [f["fragment_id"] for f in result.output["fragments"]]
    assert returned_ids == [relevant.id]
    assert noise[0].id not in returned_ids
    assert noise[1].id not in returned_ids


@pytest.mark.integration
async def test_max_fragments_zero_or_negative_returns_empty_without_querying_store(db_session):
    """`max_fragments <= 0` MUST return `fragments = []` without ever calling
    `store.query(...)` — the documented defensive guard (T085; the previous fixed
    window had a fissure here, see T090 evidence)."""
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    frag = _make_fragment(
        db_session, document=document, course_id=course.id, activity_configuration_ids=["act-1"]
    )
    inner = _OrderedCandidateVectorStore([VectorMatch(frag.id, {}, 0.9)])
    store = _SpyVectorStore(inner)

    for max_fragments in (0, -1, -5):
        agent = MaterialRetrieverAgent(
            db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter()
        )
        result = await agent.execute(
            _request(course.id, "act-1", max_fragments=max_fragments), CancellationToken()
        )
        assert result.output["fragments"] == [], f"max_fragments={max_fragments}"

    assert store.query_calls == 0


@pytest.mark.integration
async def test_budget_exactly_at_the_limit_does_not_trigger_an_extra_round(db_session):
    """T099 (follow-up to T085): `elapsed_ms == time_budget_ms` MUST count as budget
    exhausted (`>=`, not `>`) — the contract says the budget "se agota", which
    includes hitting it exactly, not only exceeding it. `max_fragments=1`, no
    candidate in round 1 is authorized, so nothing satisfies condition 1 and the loop
    would otherwise widen to a second round; the post-round-1 check lands exactly on
    the budget."""
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-other"])
    candidates = [
        VectorMatch(
            _make_fragment(
                db_session,
                document=document,
                course_id=course.id,
                activity_configuration_ids=["act-other"],
            ).id,
            {},
            0.9,
        )
        for _ in range(4)
    ]
    store = _OrderedCandidateVectorStore(candidates)
    # time_budget_ms=5000 (via `_request()`). started=0.0; pre-round-1 check=0.1s
    # (100ms, within budget) -> round 1 (k=4) runs; post-round-1 check=5.0s (exactly
    # 5000ms = the budget) -> MUST be treated as exhausted, stopping before round 2.
    clock = _FakeClock([0.0, 0.1, 5.0])
    agent = MaterialRetrieverAgent(
        db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter(), clock=clock
    )
    result = await agent.execute(_request(course.id, "act-1", max_fragments=1), CancellationToken())

    assert result.output["fragments"] == []
    assert store.queried_k == [4], (
        f"expected a single round at the exact budget boundary, got {store.queried_k!r}"
    )
    assert result.output["warnings"] == ["presupuesto temporal agotado, resultado parcial"]
