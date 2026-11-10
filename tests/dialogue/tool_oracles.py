"""Property oracles consume observations; they never execute or fabricate tools."""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class ExpectedOperation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation: str
    actor: Literal["teacher", "participant", "system"]
    arguments: dict[str, Any]
    expected_status: int
    expected_state: dict[str, Any]
    response_properties: dict[str, Any]


class Observation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation: str
    actor: Literal["teacher", "participant", "system"]
    arguments: dict[str, Any]
    status: int
    state: dict[str, Any]
    response: dict[str, Any]
    observed: bool


def verify_operation(expected: ExpectedOperation, observed: Observation) -> list[str]:
    """Exact role/argument/effect oracles; prose claiming success is insufficient.

    `observed` is evidence provenance from the harness, never an API response field.
    The harness must collect the real response and read persisted effects itself.
    These unit-tested comparisons do not establish that a service was exercised.
    """
    errors = []
    for code, matches in [
        ("unobserved_operation", observed.observed),
        ("operation_mismatch", observed.operation == expected.operation),
        ("role_mismatch", observed.actor == expected.actor),
        ("arguments_mismatch", observed.arguments == expected.arguments),
        ("status_mismatch", observed.status == expected.expected_status),
        ("state_mismatch", observed.state == expected.expected_state),
        (
            "response_mismatch",
            all(
                observed.response.get(key) == value and key in observed.response
                for key, value in expected.response_properties.items()
            ),
        ),
    ]:
        if not matches:
            errors.append(code)
    return errors
