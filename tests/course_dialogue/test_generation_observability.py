"""CPU-only observability must not mutate generation configuration or run a model."""

import json
from pathlib import Path
from types import SimpleNamespace

from oralia.course_dialogue.generation_observability import generation_snapshot


class Config:
    def __init__(self, values):
        self.values = values

    def to_dict(self):
        return dict(self.values)

    def update(self, **values):
        self.values.update(values)


def test_actual_config_and_overrides_are_recorded_without_mutation_or_generation():
    config = Config({"do_sample": True, "repetition_penalty": 1.05, "temperature": 0.7})
    model = SimpleNamespace(
        generation_config=config,
        config=SimpleNamespace(quantization_config={"load_in_4bit": True}),
        training=False,
        is_quantized=True,
        parameters=lambda: iter([SimpleNamespace(dtype="bfloat16", device="cpu")]),
    )
    result = generation_snapshot(
        model,
        SimpleNamespace(eos_token_id=151645),
        {"do_sample": False, "max_new_tokens": 64, "pad_token_id": 151645},
        finite=True,
    )
    assert result["model_generation_config"]["repetition_penalty"] == 1.05
    assert result["effective_config_after_explicit_overrides"]["do_sample"] is False
    assert result["effective_config_after_explicit_overrides"]["repetition_penalty"] == 1.05
    assert config.values["do_sample"] is True
    assert result["finite_prefix_constraint"] is True
    assert result["representative_parameter_device"] == "cpu"


def test_historical_gap_is_not_replaced_by_a_later_receipt():
    evidence = Path(__file__).resolve().parents[2] / "specs/012-conversational-course-study/evidence"
    old = json.loads(
        (evidence / "scope-control-diagnostic-resource-run/worker.json").read_text(encoding="utf-8")
    )
    assert "generation_state" not in old
    record = json.loads(
        (evidence / "scope-control-diagnostic-resource-run/records.json").read_text(encoding="utf-8")
    )[0]
    assert "generation_state" not in json.loads(record["attempts"][0]["exchange"]["raw_worker_response"])
