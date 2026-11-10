"""Contract tests with synthetic tokenizers/vectors; real retrieval measured separately."""

from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from oralia.documentary.__main__ import PACKAGES, create_app, load_package
from oralia.documentary.retrieval import Retrieval, split_text
from oralia.infrastructure.embeddings.sentence_transformer_adapter import (
    SentenceTransformerEmbeddingAdapter as Adapter,
)


class CharacterTokenizer:
    def encode(self, text, **kwargs):
        assert kwargs == {"add_special_tokens": True, "truncation": False}
        return [0] + list(text) + [1]


@pytest.mark.parametrize(
    "text", ["x" * 97 + "IMPORTANT END", "Heading\nA | B\nrow1 | value\nrow2 | other", "áé漢字" * 40]
)
def test_token_partition_covers_end_offsets_and_tables(text):
    chunks = list(split_text(text, CharacterTokenizer(), 25))
    assert "".join(c[2] for c in chunks) == text
    assert chunks[-1][1] == len(text)
    for start, end, chunk in chunks:
        assert text[start:end] == chunk
        assert len(CharacterTokenizer().encode(chunk, add_special_tokens=True, truncation=False)) <= 25


def test_cpu_cache_identity_is_explicit(monkeypatch):
    import sys

    calls = []

    def load(name, **kwargs):
        calls.append(kwargs)
        return object()

    monkeypatch.setitem(sys.modules, "sentence_transformers", SimpleNamespace(SentenceTransformer=load))
    monkeypatch.setattr(Adapter, "_model", None)
    monkeypatch.setattr(Adapter, "_model_identity", None)
    a = Adapter("same")._get_model()
    b = Adapter("same", device="cpu")._get_model()
    assert a is not b
    assert calls[-1] == {"local_files_only": True, "device": "cpu"}
    with pytest.raises(ValueError):
        Adapter("same", device="cuda")


def test_revalidation_blocks_changed_or_withdrawn_file(tmp_path):
    from oralia.documentary.retrieval import digest

    (tmp_path / "source").write_bytes(b"original")
    r = object.__new__(Retrieval)
    r.package = tmp_path
    r.sources = {"source": digest(b"original")}
    r.revalidate()
    (tmp_path / "source").write_bytes(b"changed")
    with pytest.raises(ValueError, match="changed"):
        r.revalidate()
    (tmp_path / "source").unlink()
    with pytest.raises(ValueError):
        r.revalidate()


def test_v2_only_available_pages_and_exact_oracle():
    import json

    from oralia.documentary.retrieval import ROOT

    _, pages = load_package(PACKAGES["v2"][0], "manifest-v2.json")
    allowed = {r["id"]: r for group in pages.values() for r in group if r["status"] == "disponible"}
    assert len(allowed) == 117
    bank = json.loads(
        (ROOT / "docs/audits/2026-10-27-retrieval-increment/bank-v1.json").read_text(encoding="utf8")
    )
    assert len(bank) == 30
    assert len({c["subtopic"] for c in bank if c["id"].startswith("Q")}) == 12
    for c in bank:
        for ref in c["oracle"]:
            assert ref["text"] == allowed[ref["id"]]["text"]


def test_api_opt_in_access_close_reentry_and_no_generation():
    class Stub:
        def query(self, *args, **kwargs):
            return {"passages": [], "sufficiency": "not_assessed"}

    package = PACKAGES["v2"][0]
    with TestClient(
        create_app(package, manifest_name="manifest-v2.json", retrieval=Stub()), base_url="http://127.0.0.1"
    ) as c:
        assert c.get("/api/v1/retrieval?question=test").status_code == 401
        c.post("/documentary/enter")
        assert c.get("/api/v1/documentary").json()["retrieval"] is True
        assert c.get("/api/v1/retrieval?question=test").json()["sufficiency"] == "not_assessed"
        c.post("/documentary/leave")
        assert c.get("/api/v1/retrieval?question=test").status_code == 401
        c.post("/documentary/enter")
        assert c.get("/api/v1/retrieval?question=test").status_code == 200
    with TestClient(create_app(package, manifest_name="manifest-v2.json"), base_url="http://127.0.0.1") as c:
        c.post("/documentary/enter")
        assert c.get("/api/v1/retrieval?question=test").status_code == 404


def query_double():
    r = object.__new__(Retrieval)
    r.config = {
        "strategies": ["lexical", "dense", "rrf"],
        "candidates": 20,
        "context_chars": 6000,
        "context_units": 5,
        "rrf_k": 60,
    }
    r.manifest = {"package_id": "isolated"}
    r.tokenizer = CharacterTokenizer()
    r.limit = 128
    r.fragments = []
    r.by_id = {}
    r.pages = {}
    r.fingerprint = {"revision": "synthetic"}
    r.revalidate = lambda: None
    r.adapter = SimpleNamespace(embed=lambda _: [[1, 0]])
    r.store = SimpleNamespace(query=lambda *args: [])
    return r


def test_foreign_fragment_rejected_even_with_course_metadata():
    r = query_double()
    r.store = SimpleNamespace(query=lambda *args: [SimpleNamespace(fragment_id="foreign", relevance_score=1)])
    with pytest.raises(ValueError, match="foreign"):
        r.query("test", "dense")


def test_withdrawal_after_embedding_blocks_delivery():
    r = query_double()
    checks = []

    def validate():
        checks.append(True)
        if len(checks) == 2:
            raise ValueError("withdrawn while waiting")

    r.revalidate = validate
    with pytest.raises(ValueError, match="withdrawn"):
        r.query("test", "dense")


def test_oversized_query_is_rejected_before_encoding():
    from oralia.documentary.study_errors import StudyFailure

    r = query_double()
    r.adapter = SimpleNamespace(embed=lambda _: pytest.fail("must not encode truncated query"))
    with pytest.raises(StudyFailure) as error:
        r.query("x" * 200, "dense")
    assert error.value.code == "question_too_long"


def test_close_during_query_blocks_late_delivery():
    class Closing:
        def query(self, *args, **kwargs):
            client.post("/documentary/leave")
            return {"passages": [{"text": "late"}]}

    with TestClient(
        create_app(PACKAGES["v2"][0], manifest_name="manifest-v2.json", retrieval=Closing()),
        base_url="http://127.0.0.1",
    ) as client:
        client.post("/documentary/enter")
        response = client.get("/api/v1/retrieval?question=test")
        assert response.status_code == 401
        assert "late" not in response.text
