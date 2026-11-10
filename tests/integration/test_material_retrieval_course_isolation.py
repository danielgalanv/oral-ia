"""T098 (Feature 002, follow-up to T085/T099) — `MaterialRetrieverAgent` sends
`filters={"course_id": course_id}` to the `VectorStore` as a coarse pre-filter, but
never re-validated `MaterialFragment.course_id`/`MaterialDocument.course_id` against
SQL afterwards. A `VectorStore` that ignores the filter (or whose metadata has
drifted from SQL) could return a fragment from a DIFFERENT course whenever it shares
`activity_configuration_id` with the requested one — the only check actually
performed (`_authorized`) never looked at course_id at all.

Every assertion below states the CORRECT required behavior — a fragment/document
belonging to another course MUST NEVER be returned, regardless of what the store or
its metadata claims. Run against the pre-T098 code, tests 1/2/3/8 MUST fail; the
exact same assertions MUST hold, unchanged, once T098 is implemented.
"""

from __future__ import annotations

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


@pytest.mark.integration
async def test_vector_store_ignoring_course_filter_never_leaks_other_course_fragment(db_session):
    """The store returns the WRONG-course fragment first, with relevance 0.9 (well
    above the 0.35 floor) — it MUST NOT be returned for a query scoped to the correct
    course, even though it shares `activity_configuration_id` with it."""
    wrong_course, wrong_document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    right_course, right_document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])

    wrong_fragment = _make_fragment(
        db_session, document=wrong_document, course_id=wrong_course.id, activity_configuration_ids=["act-1"]
    )
    right_fragment = _make_fragment(
        db_session, document=right_document, course_id=right_course.id, activity_configuration_ids=["act-1"]
    )

    # `_OrderedCandidateVectorStore` ignores `filters` entirely — exactly the "store
    # that ignores the course_id filter" scenario this reproduction requires.
    store = _OrderedCandidateVectorStore(
        [VectorMatch(wrong_fragment.id, {}, 0.90), VectorMatch(right_fragment.id, {}, 0.80)]
    )
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(right_course.id, "act-1", max_fragments=5), CancellationToken())

    returned_ids = [f["fragment_id"] for f in result.output["fragments"]]
    assert wrong_fragment.id not in returned_ids, "a fragment from a different course leaked into fragments"
    assert returned_ids == [right_fragment.id]


@pytest.mark.integration
async def test_fragment_course_id_mismatch_is_rejected_even_if_document_course_id_matches(db_session):
    """`fragment.course_id` disagrees with the requested course, even though its
    OWN document's `course_id` matches — the discrepancy itself MUST cause
    rejection, not just an outright wrong document."""
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    other_course, _other_document = _make_course_and_document(
        db_session, activity_configuration_ids=["act-1"]
    )

    mismatched_fragment = _make_fragment(
        db_session, document=document, course_id=other_course.id, activity_configuration_ids=["act-1"]
    )

    store = _OrderedCandidateVectorStore([VectorMatch(mismatched_fragment.id, {}, 0.90)])
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(course.id, "act-1", max_fragments=5), CancellationToken())

    assert result.output["fragments"] == []


@pytest.mark.integration
async def test_document_course_id_mismatch_is_rejected_even_if_fragment_course_id_matches(db_session):
    """`document.course_id` disagrees with the requested course, even though the
    fragment's OWN `course_id` matches — SQL metadata drift between the two rows
    MUST also cause rejection."""
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    other_course, _other_document = _make_course_and_document(
        db_session, activity_configuration_ids=["act-1"]
    )
    document.course_id = other_course.id
    db_session.add(document)
    db_session.flush()

    fragment = _make_fragment(
        db_session, document=document, course_id=course.id, activity_configuration_ids=["act-1"]
    )

    store = _OrderedCandidateVectorStore([VectorMatch(fragment.id, {}, 0.90)])
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(course.id, "act-1", max_fragments=5), CancellationToken())

    assert result.output["fragments"] == []


@pytest.mark.integration
async def test_fragment_and_document_of_the_correct_course_are_accepted(db_session):
    """Positive contrast — both `fragment.course_id` and `document.course_id` match
    the requested course: MUST be accepted, same as before this round."""
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    fragment = _make_fragment(
        db_session, document=document, course_id=course.id, activity_configuration_ids=["act-1"]
    )
    store = _OrderedCandidateVectorStore([VectorMatch(fragment.id, {}, 0.90)])
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(course.id, "act-1", max_fragments=5), CancellationToken())

    assert [f["fragment_id"] for f in result.output["fragments"]] == [fragment.id]


@pytest.mark.integration
async def test_widening_continues_past_other_course_candidates_to_find_valid_ones(db_session):
    """Several other-course candidates ranked ahead of a correct one MUST NOT stop
    the search — widening continues, mirroring H08.A's original guarantee, now for
    the course-isolation defect specifically."""
    right_course, right_document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    wrong_course, wrong_document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])

    candidates: list[VectorMatch] = []
    for i in range(16):
        frag = _make_fragment(
            db_session,
            document=wrong_document,
            course_id=wrong_course.id,
            activity_configuration_ids=["act-1"],
        )
        candidates.append(VectorMatch(frag.id, {}, 0.95 - i * 0.01))
    right_fragment = _make_fragment(
        db_session, document=right_document, course_id=right_course.id, activity_configuration_ids=["act-1"]
    )
    candidates.append(VectorMatch(right_fragment.id, {}, 0.80))

    store = _OrderedCandidateVectorStore(candidates)
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(right_course.id, "act-1", max_fragments=1), CancellationToken())

    assert [f["fragment_id"] for f in result.output["fragments"]] == [right_fragment.id]
    assert len(store.queried_k) >= 2, "expected multiple widening rounds past the other-course candidates"


@pytest.mark.integration
async def test_other_course_block_is_logged_once_across_several_widenings(db_session, monkeypatch):
    """An other-course candidate appearing across MULTIPLE widening rounds MUST
    still produce exactly one blocked-attempt log call per `execute()` — the same
    `blocked_out_of_scope` bucket as an activity mismatch."""
    from oralia.application.services import trace_service

    calls: list[dict] = []

    def _spy(db, **kwargs):
        calls.append(kwargs)

    monkeypatch.setattr(trace_service, "record_event", _spy)

    right_course, _right_document = _make_course_and_document(
        db_session, activity_configuration_ids=["act-1"]
    )
    wrong_course, wrong_document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    candidates = [
        VectorMatch(
            _make_fragment(
                db_session,
                document=wrong_document,
                course_id=wrong_course.id,
                activity_configuration_ids=["act-1"],
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
            "course_id": right_course.id,
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
async def test_other_course_candidates_never_reach_conflict_detection(db_session, monkeypatch):
    """Other-course candidates MUST NOT be passed to `detect_conflicts` — only the
    final selected (same-course) fragments."""
    from oralia.domain.agents import material_retriever_agent as module

    seen_candidates: list[list] = []
    original = module.detect_conflicts

    def _spy(candidates):
        seen_candidates.append(list(candidates))
        return original(candidates)

    monkeypatch.setattr(module, "detect_conflicts", _spy)

    right_course, right_document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    wrong_course, wrong_document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    kept = _make_fragment(
        db_session, document=right_document, course_id=right_course.id, activity_configuration_ids=["act-1"]
    )
    other_course_fragment = _make_fragment(
        db_session, document=wrong_document, course_id=wrong_course.id, activity_configuration_ids=["act-1"]
    )

    candidates = [VectorMatch(other_course_fragment.id, {}, 0.95), VectorMatch(kept.id, {}, 0.80)]
    store = _OrderedCandidateVectorStore(candidates)
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(right_course.id, "act-1", max_fragments=5), CancellationToken())

    assert [f["fragment_id"] for f in result.output["fragments"]] == [kept.id]
    assert len(seen_candidates) == 1
    assert [c.fragment_id for c in seen_candidates[0]] == [kept.id]


@pytest.mark.integration
async def test_vector_match_metadata_claiming_correct_course_cannot_override_sql(db_session):
    """The `VectorMatch.metadata` dict claims the correct course, but SQL says
    otherwise — SQL MUST prevail; the agent MUST NOT trust the store's metadata for
    authorization."""
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    other_course, other_document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    fragment = _make_fragment(
        db_session, document=other_document, course_id=other_course.id, activity_configuration_ids=["act-1"]
    )

    # Metadata dishonestly claims the CORRECT course — MUST be ignored.
    store = _OrderedCandidateVectorStore([VectorMatch(fragment.id, {"course_id": course.id}, 0.90)])
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(course.id, "act-1", max_fragments=5), CancellationToken())

    assert result.output["fragments"] == []
