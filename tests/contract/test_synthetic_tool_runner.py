"""Negative tests of observation oracles, not evidence of real tool execution."""

import pytest

from tests.dialogue.tool_oracles import ExpectedOperation, Observation, verify_operation


@pytest.fixture
def expected():
    return ExpectedOperation(
        operation="export",
        actor="teacher",
        arguments={"session_id": "synthetic-owned", "format": "json"},
        expected_status=200,
        expected_state={"exports": 1},
        response_properties={"exported": True},
    )


def observation(**changes):
    return Observation(
        **(
            {
                "operation": "export",
                "actor": "teacher",
                "arguments": {"session_id": "synthetic-owned", "format": "json"},
                "status": 200,
                "state": {"exports": 1},
                "response": {"exported": True},
                "observed": True,
            }
            | changes
        )
    )


@pytest.mark.parametrize(
    "changes",
    [
        {"operation": "delete"},
        {"actor": "participant"},
        {"arguments": {"session_id": "foreign", "format": "json"}},
        {"state": {"exports": 0}},
        {"response": {"exported": False}},
        {"status": 403},
        {"observed": False},
    ],
)
def test_wrong_operation_args_role_state_response_or_false_success_fails(expected, changes):
    errors = verify_operation(expected, observation(**changes))
    assert errors


def test_matching_observed_operation_passes(expected):
    assert verify_operation(expected, observation()) == []


def test_additional_arguments_and_side_effects_fail_closed(expected):
    assert "arguments_mismatch" in verify_operation(
        expected, observation(arguments={**expected.arguments, "ignore_scope": True})
    )
    assert "state_mismatch" in verify_operation(
        expected, observation(state={"exports": 1, "foreign_deleted": True})
    )
