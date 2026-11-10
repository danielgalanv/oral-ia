"""Frozen budget/configuration checks before the real conversation comparison."""

import copy
import hashlib
import json
from pathlib import Path

import pytest

from scripts.run_pedagogical_comparison import verify_ready

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"


def test_frozen_comparison_and_pre_inference_clarification_keep_baseline_and_budget():
    folder = EVIDENCE / "pedagogical-comparison-proposal-v1"
    raw = (folder / "protocol.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == (folder / "protocol.sha256").read_text()
    protocol = json.loads(raw)
    old = json.loads((EVIDENCE / "readable-reference-proposal-v1/protocol.json").read_text(encoding="utf-8"))
    assert protocol["profiles"]["baseline"] == old["instruction"]
    assert len(protocol["cases"]) == 3 and all(len(case["turns"]) == 4 for case in protocol["cases"])
    assert len(protocol["order"]) * 4 == protocol["academic_requests_maximum"] == 24
    assert protocol["new_tokens_maximum"] == 24 * 512 + 1
    assert protocol["model_generate_maximum"] == 25
    clarification = (folder / "example-clarification.json").read_bytes()
    assert hashlib.sha256(clarification).hexdigest() == (folder / "example-clarification.sha256").read_text()
    assert json.loads(clarification)["original_protocol_sha256"] == hashlib.sha256(raw).hexdigest()
    assert json.loads(clarification)["no_comparison_inference_yet"] is True
    assert "0.3" not in protocol["profiles"]["pedagogy-v1"]


def test_effective_config_refuses_invalid_model_before_academic_requests():
    ready = {
        "effective_model_class": "Qwen2ForCausalLM",
        "quantization": "nf4",
        "generation_state": {
            "model_training": False,
            "quantization_config": {
                "load_in_4bit": True,
                "bnb_4bit_quant_type": "nf4",
                "bnb_4bit_compute_dtype": "bfloat16",
            },
        },
    }
    assert verify_ready(ready)["allowed"] is True
    wrong = copy.deepcopy(ready)
    wrong["generation_state"]["model_training"] = True
    with pytest.raises(ValueError, match="effective model configuration"):
        verify_ready(wrong)
    wrong = copy.deepcopy(ready)
    wrong["generation_state"]["quantization_config"]["bnb_4bit_compute_dtype"] = "float32"
    with pytest.raises(ValueError, match="effective model configuration"):
        verify_ready(wrong)
