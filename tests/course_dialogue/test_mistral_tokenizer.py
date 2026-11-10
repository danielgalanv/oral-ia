"""The Mistral tokenization correction is opt-in and in-memory only."""

import json
from types import SimpleNamespace

import pytest
from tokenizers import Regex, Tokenizer, models, pre_tokenizers

from oralia.course_dialogue.gpu_worker import patch_mistral_regex


def _tokenizer():
    backend = Tokenizer(models.BPE())
    backend.pre_tokenizer = pre_tokenizers.Sequence(
        [
            pre_tokenizers.Split(Regex(r"old-pattern"), behavior="isolated"),
            pre_tokenizers.ByteLevel(add_prefix_space=False, trim_offsets=True, use_regex=False),
        ]
    )
    return SimpleNamespace(backend_tokenizer=backend)


def test_local_mistral_regex_replaces_only_expected_in_memory_shape():
    tokenizer = _tokenizer()
    original = json.loads(tokenizer.backend_tokenizer.pre_tokenizer.__getstate__())
    patch_mistral_regex(tokenizer)
    actual = json.loads(tokenizer.backend_tokenizer.pre_tokenizer.__getstate__())
    assert original["pretokenizers"][0]["pattern"] == {"Regex": "old-pattern"}
    assert actual["pretokenizers"][0]["pattern"]["Regex"].startswith(r"[^\r\n\p{L}\p{N}]")
    assert actual["pretokenizers"][1] == original["pretokenizers"][1]


def test_local_mistral_regex_rejects_an_unexpected_shape():
    tokenizer = _tokenizer()
    tokenizer.backend_tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel()
    with pytest.raises(ValueError, match="shape changed"):
        patch_mistral_regex(tokenizer)
