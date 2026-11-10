"""Minimal comparison structure, not tests of model capability."""

import ast
import json
from pathlib import Path

from oralia.course_dialogue.finite_schema import finite_json_outputs
from scripts.prepare_minimal_capacity_probe import build_probe, execution_budget


def test_exactly_three_tasks_five_calls_and_bounded_total_tokens():
    frames, oracle = build_probe()
    assert len(frames) == 5 and len(oracle) == 3
    assert sum(frame["max_tokens"] for frame in frames) == 576
    assert all(frame["deadline_ms"] == 30000 for frame in frames)
    assert frames[-1]["finite_outputs"] is None


def test_comparisons_change_only_decoder_restriction_not_model_messages():
    frames, _ = build_probe()
    for free, finite in ((frames[0], frames[1]), (frames[2], frames[3])):
        assert {k: v for k, v in free.items() if k not in {"id", "finite_outputs"}} == {
            k: v for k, v in finite.items() if k not in {"id", "finite_outputs"}
        }
        assert free["finite_outputs"] is None
        assert finite_json_outputs({"type": "object", "x-oralia-finite-outputs": finite["finite_outputs"]})


def test_finite_decoder_does_not_force_the_correct_answer():
    frames, oracle = build_probe()
    for finite, key in ((frames[1], "instruction"), (frames[3], "scope")):
        alternatives = [json.loads(value) for value in finite["finite_outputs"]]
        assert oracle[key]["expected_json"] in alternatives
        assert any(value != oracle[key]["expected_json"] for value in alternatives)
    assert oracle["explanation"]["no_predefined_answer"] is True


def test_oracles_not_embedded_in_model_input():
    frames, _ = build_probe()
    assert all("expected_json" not in json.dumps(frame["messages"]) for frame in frames)
    assert all("required_claims" not in json.dumps(frame["messages"]) for frame in frames)


def test_prepared_inputs_did_not_change_during_code_formatting():
    root = (
        Path(__file__).resolve().parents[2]
        / "specs/012-conversational-course-study/evidence/minimal-capacity-probe-v1"
    )
    frames, oracle = build_probe()
    assert json.loads((root / "frames.json").read_text(encoding="utf-8")) == frames
    assert json.loads((root / "oracle.json").read_text(encoding="utf-8")) == oracle


def test_budget_includes_the_existing_worker_warmup_not_just_pipe_requests():
    source = Path(__file__).resolve().parents[2] / "src/oralia/course_dialogue/gpu_worker.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    calls = [
        n
        for n in ast.walk(tree)
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and n.func.attr == "generate"
        and isinstance(n.func.value, ast.Name)
        and n.func.value.id == "model"
    ]
    assert len(calls) == 2
    assert (
        sum(
            any(
                k.arg == "max_new_tokens" and isinstance(k.value, ast.Constant) and k.value.value == 1
                for k in call.keywords
            )
            for call in calls
        )
        == 1
    )
    budget = execution_budget()
    assert budget["diagnostic_pipe_requests_maximum"] == 5
    assert budget["total_model_generate_invocations_maximum"] == 6
    assert budget["total_new_tokens_maximum"] == 577
