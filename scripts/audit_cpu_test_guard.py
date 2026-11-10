"""Opt-in pytest plugin: prove remediation tests never load embedding/model weights.

Run with ``-p scripts.audit_cpu_test_guard``. Tokenizer-only local checks are allowed.
No global installation or user environment changes.
"""

import sys
from types import SimpleNamespace

import pytest


@pytest.fixture(autouse=True)
def prohibit_real_embedding_load(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("remediation CPU validation must not load real embedding weights")

    monkeypatch.setitem(sys.modules, "sentence_transformers", SimpleNamespace(SentenceTransformer=forbidden))
