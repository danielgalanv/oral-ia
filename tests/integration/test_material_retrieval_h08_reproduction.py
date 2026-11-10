"""T090 — baseline reproduction for T085 (H08), before any fix is implemented.

Two independent, deterministic reproductions against the REAL `MaterialRetrieverAgent`,
each controlling only its input boundaries (a double `VectorStore` and/or a double
`EmbeddingAdapter`) — never a copy of the agent's own logic, and `MaterialRetrieverAgent`
itself is NOT modified by this task:

- H08.A: the fixed candidate window (`over_fetch = max(max_fragments * 4, max_fragments)`,
  a single `store.query(...)` call) can lose authorized, current evidence that simply
  ranks behind enough unauthorized/expired candidates — `research.md` §14.1.
- H08.B: no relevance floor is applied to `relevance_score` — an authorized, current
  fragment with a very low relevance score is still returned as if it answered the
  query — `research.md` §14.2.

Every assertion below states the CORRECT final behavior (per FR-019/FR-019a and the
corrected design in `research.md` §14.1/§14.2) — never the current buggy behavior. Run
against the current (pre-T085) code, the H08.A and the negative half of H08.B are
EXPECTED TO FAIL; the positive contrast of H08.B is expected to already pass. The exact
same assertions MUST still hold, unchanged, once T085 is implemented.
"""

from __future__ import annotations

import uuid

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.material_retriever_agent import MaterialRetrieverAgent
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from oralia.infrastructure.vector_store.chroma_store import VectorMatch


class _FixedEmbeddingAdapter:
    """Controls only the embedding boundary — the vector's actual content is
    irrelevant to either reproduction below, since the double `VectorStore` returns a
    pre-ordered candidate list regardless of the query vector (exactly mirroring what
    `MaterialRetrieverAgent` itself observes from `ChromaVectorStore.query`: a
    relevance-ranked list truncated to `k`)."""

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] for _ in texts]


class _OrderedCandidateVectorStore:
    """Deterministic double: returns the first `k` items of a fixed, pre-ordered
    candidate list — never re-ranks, never inspects `filters`/`embedding`. Records
    every `k` it was asked for (`queried_k`) purely as a diagnostic for the
    T090 evidence report; the tests below MUST NOT assert on its exact values (per
    this round's instruction: the contract under test is "valid evidence behind
    invalid candidates is not lost", not "the store was called with a specific k")."""

    def __init__(self, candidates: list[VectorMatch]) -> None:
        self._candidates = candidates
        self.queried_k: list[int] = []

    def query(self, embedding, filters, k):  # noqa: ANN001 - matches VectorStore Protocol
        self.queried_k.append(k)
        return self._candidates[: max(k, 0)]

    def add(self, *args, **kwargs):
        raise NotImplementedError("not used by this reproduction")

    def delete(self, *args, **kwargs):
        raise NotImplementedError("not used by this reproduction")

    def rebuild(self, *args, **kwargs):
        raise NotImplementedError("not used by this reproduction")

    def get_index_version(self) -> str:
        return "test-version"


def _make_course_and_document(db, *, activity_configuration_ids: list[str], status: str = "active"):
    course = models.Course(name="Curso H08", subject_code="H08")
    db.add(course)
    db.flush()
    document = models.MaterialDocument(
        course_id=course.id,
        filename="h08.pdf",
        content_hash=uuid.uuid4().hex,
        mime_type="application/pdf",
        size_bytes=1,
        status=status,
        activity_configuration_ids=activity_configuration_ids,
    )
    db.add(document)
    db.flush()
    return course, document


def _make_fragment(
    db,
    *,
    document: models.MaterialDocument,
    course_id: str,
    activity_configuration_ids: list[str],
    valid_until=None,
    indexing_status: str = "indexed",
) -> models.MaterialFragment:
    fragment = models.MaterialFragment(
        document_id=document.id,
        document_version=document.version,
        text=f"Fragmento {uuid.uuid4().hex[:8]} sobre el tema del curso.",
        location_ref="p1",
        sequence_index=0,
        embedding_ref=uuid.uuid4().hex,
        course_id=course_id,
        activity_configuration_ids=activity_configuration_ids,
        valid_until=valid_until,
        indexing_status=indexing_status,
    )
    db.add(fragment)
    db.flush()
    return fragment


def _request(course_id: str, activity_configuration_id: str, max_fragments: int) -> AgentRequest:
    return AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        input={
            "query_text": "consulta de prueba sobre el tema del curso",
            "course_id": course_id,
            "activity_configuration_id": activity_configuration_id,
            "max_fragments": max_fragments,
            "time_budget_ms": 5000,
        },
    )


@pytest.mark.integration
async def test_h08a_authorized_fragment_beyond_fixed_window_is_not_lost(db_session):
    """H08.A reproduction (research.md §14.1). `max_fragments=2` — the current fixed
    window is `over_fetch = max(2*4, 2) = 8`. The first 8 candidates the store would
    return (highest relevance) are ALL excluded by authorization or vigencia; three
    further candidates, ranked 9th-11th, ARE authorized/active/indexed/current, with
    relevance clearly high enough not to be confused with a future relevance floor.

    Correct required behavior (asserted here, unchanged before and after T085): the
    two most relevant AUTHORIZED fragments (positions 9 and 10) MUST appear in
    `fragments`, in relevance order — evidence must never be lost merely for ranking
    behind invalid candidates within a fixed window. Against the current agent this
    MUST fail (`fragments` comes back empty): the single `store.query(..., k=8)` call
    never even retrieves positions 9-11."""
    course, wrong_activity_document = _make_course_and_document(
        db_session, activity_configuration_ids=["act-other"]
    )
    _, valid_document = _make_course_and_document(
        db_session, activity_configuration_ids=["act-1"]
    )
    # (Both documents share the same course — the reproduction is scoped to a single
    # course_id, isolating the window/filter defect from any course-isolation concern.)
    valid_document.course_id = course.id
    db_session.add(valid_document)
    db_session.flush()

    candidates: list[VectorMatch] = []
    # Positions 1-4: wrong activity_configuration_id (excluded by _authorized).
    for i in range(4):
        frag = _make_fragment(
            db_session,
            document=wrong_activity_document,
            course_id=course.id,
            activity_configuration_ids=["act-other"],
        )
        candidates.append(VectorMatch(frag.id, {}, 0.95 - i * 0.01))
    # Positions 5-8: right activity, but expired (excluded by _is_retrievable/FR-019a).
    for i in range(4):
        frag = _make_fragment(
            db_session,
            document=valid_document,
            course_id=course.id,
            activity_configuration_ids=["act-1"],
            valid_until=utcnow().replace(year=2000),
        )
        candidates.append(VectorMatch(frag.id, {}, 0.91 - i * 0.01))
    # Positions 9-11: authorized, active, indexed, current — must be recovered.
    valid_fragment_ids: list[str] = []
    for i in range(3):
        frag = _make_fragment(
            db_session,
            document=valid_document,
            course_id=course.id,
            activity_configuration_ids=["act-1"],
        )
        valid_fragment_ids.append(frag.id)
        candidates.append(VectorMatch(frag.id, {}, 0.80 - i * 0.01))

    store = _OrderedCandidateVectorStore(candidates)
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(course.id, "act-1", max_fragments=2), CancellationToken())

    returned_ids = [f["fragment_id"] for f in result.output["fragments"]]
    assert returned_ids == valid_fragment_ids[:2], (
        f"expected the two most relevant authorized/current fragments {valid_fragment_ids[:2]!r} "
        f"(positions 9-10, beyond the fixed window), got {returned_ids!r} - "
        f"store was queried with k={store.queried_k!r}"
    )


@pytest.mark.integration
async def test_h08b_irrelevant_query_over_nonempty_authorized_corpus_yields_no_fragments(db_session):
    """H08.B reproduction, negative half (research.md §14.2, Escenario C.1). A
    non-empty, fully authorized/current corpus is queried by something unrelated to
    it — every candidate's `relevance_score` is far below the conservative threshold
    this round measured and proposes (0.35; see T090 evidence — measured negatives
    0.058-0.216, measured positives 0.621-0.813 with the real project embedding
    model). Correct required behavior: `fragments = []`, with a warning distinguishing
    this from budget/corpus exhaustion. Against the current agent this MUST fail:
    today every authorized/current candidate is returned regardless of relevance."""
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    candidates = []
    for score in (0.22, 0.15, 0.12, 0.06):
        frag = _make_fragment(
            db_session,
            document=document,
            course_id=course.id,
            activity_configuration_ids=["act-1"],
        )
        candidates.append(VectorMatch(frag.id, {}, score))

    store = _OrderedCandidateVectorStore(candidates)
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(course.id, "act-1", max_fragments=5), CancellationToken())

    assert result.output["fragments"] == []
    assert any(
        "pertinente" in w or "relevan" in w for w in result.output["warnings"]
    ), f"expected a relevance-specific warning, got {result.output['warnings']!r}"
    assert not any("presupuesto" in w for w in result.output["warnings"])
    assert not any("agotado para esta consulta" in w for w in result.output["warnings"])


@pytest.mark.integration
async def test_h08b_relevant_fragment_above_threshold_is_kept(db_session):
    """H08.B positive contrast — a candidate clearly above the proposed threshold
    (0.70, within the measured positive range 0.621-0.813) MUST be kept alongside
    clearly irrelevant noise below it. This is the correct behavior already, both
    before and after T085 — included here (not just relying on pre-existing tests)
    because it shares the exact same controlled setup as the negative case above,
    making the contrast direct and self-contained."""
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    relevant = _make_fragment(
        db_session, document=document, course_id=course.id, activity_configuration_ids=["act-1"]
    )
    candidates = [VectorMatch(relevant.id, {}, 0.70)]
    for score in (0.20, 0.10):
        frag = _make_fragment(
            db_session, document=document, course_id=course.id, activity_configuration_ids=["act-1"]
        )
        candidates.append(VectorMatch(frag.id, {}, score))

    store = _OrderedCandidateVectorStore(candidates)
    agent = MaterialRetrieverAgent(db_session, vector_store=store, embedding_adapter=_FixedEmbeddingAdapter())
    result = await agent.execute(_request(course.id, "act-1", max_fragments=5), CancellationToken())

    returned_ids = [f["fragment_id"] for f in result.output["fragments"]]
    assert relevant.id in returned_ids
