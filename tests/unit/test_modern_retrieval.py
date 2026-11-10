"""Ranking logic of the bge-m3 + reranker retrieval, with the ranking service simulated."""

import numpy as np
import httpx
import pytest

from oralia.documentary.modern_retrieval import ModernRetrieval
from oralia.documentary.study_errors import StudyFailure


class Tokenizer:
    def encode(self, text, **_):
        return text.split()


class Base:
    pages = {"a": {"text": "alpha"}, "b": {"text": "beta"}, "c": {"text": "gamma"}}
    fragments = [{"id": "a@0:5", "page_id": "a"}, {"id": "b@0:4", "page_id": "b"}, {"id": "c@0:5", "page_id": "c"}]

    def revalidate(self):
        pass

    def assemble(self, ranked, question, history, focus_change, strategy):
        return {"ranked": ranked, "strategy": strategy, "history": list(history)}


def build(scores):
    def handler(request):
        if request.url.path == "/rerank":
            return httpx.Response(200, json={"scores": scores})
        return httpx.Response(200, json={"vectors": [[1.0, 0.0]]})

    retrieval = ModernRetrieval.__new__(ModernRetrieval)
    retrieval.base, retrieval.np = Base(), np
    retrieval.fingerprint = {"revision": "x"}
    retrieval.url, retrieval.tokenizer = "http://ranker", Tokenizer()
    retrieval.client = httpx.Client(transport=httpx.MockTransport(handler))
    retrieval.index = np.array([[0.1, 1.0], [1.0, 0.0], [0.5, 0.5], [0.9, 0.1]], dtype="float32")
    retrieval.owner = ["a", "b", "b", "c"]  # page b has two chunks; the best one counts
    retrieval.first_fragment = {"a": "a@0:5", "b": "b@0:4", "c": "c@0:5"}
    return retrieval


def test_dense_candidates_take_the_best_chunk_per_page_and_the_reranker_decides_the_final_order():
    retrieval = build([0.2, 0.1, 0.9])  # dense order is b, c, a; the reranker prefers the last candidate
    assert retrieval.dense_pages("q") == ["b", "c", "a"]
    result = retrieval.query("pregunta", "dense", history=("antes",))
    assert result["ranked"] == ["a@0:5", "b@0:4", "c@0:5"]
    assert result["strategy"] == "dense" and result["ranking"] == "bge-m3+rerank"


def test_a_search_text_beyond_the_encoder_limit_and_a_stopped_service_fail_closed():
    retrieval = build([0.5, 0.5, 0.5])
    with pytest.raises(StudyFailure):
        retrieval.query(" ".join(["x"] * 600), "dense")
    retrieval.client = httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(503)))
    with pytest.raises(StudyFailure):
        retrieval.query("pregunta", "dense")
