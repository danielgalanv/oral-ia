"""Finite syntax cannot certify the meaning of a model-selected alternative."""

import json

import pytest

from oralia.course_dialogue.finite_schema import allowed_next_tokens, finite_json_outputs


def test_only_closed_single_enum_schema_is_enumerated():
    schema = {
        "type": "object",
        "properties": {"scope": {"type": "string", "enum": ["a", "b"]}},
        "required": ["scope"],
        "additionalProperties": False,
    }
    assert [json.loads(text) for text in finite_json_outputs(schema)] == [{"scope": "a"}, {"scope": "b"}]
    assert finite_json_outputs({**schema, "additionalProperties": True}) is None
    assert finite_json_outputs({**schema, "required": []}) is None
    assert finite_json_outputs(None) is None
    assert finite_json_outputs({**schema, "properties": []}) is None
    assert finite_json_outputs({**schema, "properties": {"scope": None}}) is None


def test_finite_decoder_preserves_both_choices_and_allows_eos_only_at_end():
    sequences = [[1, 2, 3], [1, 4, 5]]
    assert allowed_next_tokens(sequences, [], 9) == [1]
    assert allowed_next_tokens(sequences, [1], 9) == [2, 4]
    assert allowed_next_tokens(sequences, [1, 2, 3], 9) == [9]
    with pytest.raises(ValueError, match="outside"):
        allowed_next_tokens(sequences, [1, 8], 9)


def test_explicit_finite_object_outputs_are_bounded_and_never_silently_ignored():
    schema = {"type": "object", "x-oralia-finite-outputs": ['{"act":"ask"}']}
    assert finite_json_outputs(schema) == schema["x-oralia-finite-outputs"]
    for outputs in [[], ["[]"], ["not-json"], ["{}"] * 257]:
        with pytest.raises(ValueError):
            finite_json_outputs({**schema, "x-oralia-finite-outputs": outputs})


def test_large_or_unsafe_enum_is_not_treated_as_a_finite_protocol():
    for values in [[], list(range(33)), [True], [{}], ["x" * 129]]:
        assert (
            finite_json_outputs(
                {
                    "type": "object",
                    "properties": {"x": {"enum": values}},
                    "required": ["x"],
                    "additionalProperties": False,
                }
            )
            is None
        )
