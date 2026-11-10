"""CPU doubles: identity, bounded cache and local-only loader contract."""

import sys
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace

import pytest

from oralia.infrastructure.embeddings.sentence_transformer_adapter import (
    SentenceTransformerEmbeddingAdapter as Adapter,
)


@pytest.fixture
def loader(monkeypatch):
    calls = []

    def load(name, **kwargs):
        calls.append((name, kwargs))
        if name == "missing":
            assert kwargs.get("local_files_only") is True
            raise OSError("local resource absent")
        return SimpleNamespace(name=name, revision=kwargs.get("revision"))

    monkeypatch.setattr(Adapter, "_model", None)
    monkeypatch.setattr(Adapter, "_model_identity", None, raising=False)
    monkeypatch.setitem(sys.modules, "sentence_transformers", SimpleNamespace(SentenceTransformer=load))
    return calls


def test_a_b_a_identity_with_bounded_single_resident(loader):
    a, b = Adapter("A"), Adapter("B")
    assert [a._get_model().name, b._get_model().name, a._get_model().name] == ["A", "B", "A"]
    assert len(loader) == 3


def test_concurrent_same_identity_loads_once(loader):
    with ThreadPoolExecutor(max_workers=8) as pool:
        models = list(pool.map(lambda _: Adapter("A")._get_model(), range(32)))
    assert all(model is models[0] for model in models)
    assert len(loader) == 1


def test_concurrent_different_identities_never_mix(loader):
    names = ["A", "B"] * 16
    with ThreadPoolExecutor(max_workers=8) as pool:
        assert list(pool.map(lambda name: Adapter(name)._get_model().name, names)) == names


@pytest.mark.parametrize("env", [None, "0", "1"])
def test_explicit_local_loading_preserves_environment(loader, monkeypatch, env):
    import os

    keys = ("HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE")
    for key in keys:
        if env is None:
            monkeypatch.delenv(key, raising=False)
        else:
            monkeypatch.setenv(key, env)
    Adapter("A")._get_model()
    assert loader[0][1]["local_files_only"] is True
    assert [os.environ.get(key) for key in keys] == [env, env]


def test_missing_local_resource_fails_without_remote_fallback(loader):
    with pytest.raises(OSError, match="local resource absent"):
        Adapter("missing")._get_model()
    assert len(loader) == 1


def test_revision_is_part_of_identity(loader):
    assert Adapter("A", revision="v1")._get_model().revision == "v1"
    assert Adapter("A", revision="v2")._get_model().revision == "v2"
    assert len(loader) == 2
