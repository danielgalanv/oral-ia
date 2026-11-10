"""Immutable domain model for output authorization policy values."""

import hashlib
import hmac
import json
from typing import Annotated, Any, NamedTuple, Self

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StringConstraints,
    model_validator,
)


def _reject_blank_string(value: str) -> str:
    if not value.strip():
        raise ValueError("string must contain at least one non-whitespace character")
    return value


NonEmptyString = Annotated[
    str,
    StringConstraints(strict=True, min_length=1),
    AfterValidator(_reject_blank_string),
]
PositiveStrictInt = Annotated[int, Field(strict=True, gt=0)]
SupportedSchemaVersion = Annotated[int, Field(strict=True, ge=1, le=1)]


class DisclosureRule(BaseModel):
    """An explicitly authorized category/provenance/recipient combination."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    category: NonEmptyString
    provenance: NonEmptyString
    recipient: NonEmptyString


class AllowedScope(BaseModel):
    """The topics, purposes, and actions authorized by a policy."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    topics: tuple[NonEmptyString, ...]
    purposes: tuple[NonEmptyString, ...]
    actions: tuple[NonEmptyString, ...]


class TemplateReference(NamedTuple):
    """Versioned normal-template reference represented as a JSON pair."""

    template_id: NonEmptyString
    version: PositiveStrictInt


class OperationalMessageReference(NamedTuple):
    """Versioned operational-message reference represented as a JSON pair."""

    operational_message_id: NonEmptyString
    version: PositiveStrictInt


class OutputAuthorizationPolicy(BaseModel):
    """Closed, immutable permissions attached to an activity configuration."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: SupportedSchemaVersion
    policy_id: NonEmptyString
    policy_version: PositiveStrictInt
    allowed_recipients: tuple[NonEmptyString, ...]
    allowed_disclosures: tuple[DisclosureRule, ...]
    allowed_scopes: AllowedScope
    general_knowledge_allowed: StrictBool
    allowed_templates: tuple[TemplateReference, ...]
    allowed_operational_messages: tuple[OperationalMessageReference, ...]

    @model_validator(mode="after")
    def reject_duplicate_permissions(self) -> Self:
        collections = (
            self.allowed_recipients,
            self.allowed_disclosures,
            self.allowed_scopes.topics,
            self.allowed_scopes.purposes,
            self.allowed_scopes.actions,
            self.allowed_templates,
            self.allowed_operational_messages,
        )
        if any(len(values) != len(set(values)) for values in collections):
            raise ValueError("policy collections must not contain duplicates")
        return self


def canonical_policy_json(policy: OutputAuthorizationPolicy) -> str:
    """Serialize a policy with stable keys and deterministically ordered permissions."""

    if not isinstance(policy, OutputAuthorizationPolicy):
        raise TypeError("policy must be an OutputAuthorizationPolicy")

    payload = policy.model_dump(mode="json")
    payload["allowed_recipients"] = sorted(payload["allowed_recipients"])
    payload["allowed_disclosures"] = sorted(
        payload["allowed_disclosures"],
        key=lambda rule: (rule["category"], rule["provenance"], rule["recipient"]),
    )
    scopes = payload["allowed_scopes"]
    scopes["topics"] = sorted(scopes["topics"])
    scopes["purposes"] = sorted(scopes["purposes"])
    scopes["actions"] = sorted(scopes["actions"])
    payload["allowed_templates"] = sorted(
        payload["allowed_templates"],
        key=lambda reference: (reference[0], reference[1]),
    )
    payload["allowed_operational_messages"] = sorted(
        payload["allowed_operational_messages"],
        key=lambda reference: (reference[0], reference[1]),
    )
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def canonical_policy_sha256(canonical_json: str) -> str:
    """Return the SHA-256 hex digest of the canonical JSON's exact UTF-8 bytes."""

    if not isinstance(canonical_json, str):
        raise TypeError("canonical_json must be a string")
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def _reject_non_json_number(value: str) -> None:
    raise ValueError(f"non-finite JSON number is forbidden: {value}")


def _reject_duplicate_object_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def load_output_authorization_policy(
    policy_json: str,
    expected_sha256: str,
) -> OutputAuthorizationPolicy:
    """Verify and load one immutable policy from its canonical persisted form."""

    if not isinstance(policy_json, str):
        raise TypeError("policy_json must be a string")
    if not isinstance(expected_sha256, str):
        raise TypeError("expected_sha256 must be a string")

    actual_sha256 = canonical_policy_sha256(policy_json)
    if not hmac.compare_digest(actual_sha256, expected_sha256):
        raise ValueError("policy SHA-256 does not match its stored JSON")

    raw_policy = json.loads(
        policy_json,
        parse_constant=_reject_non_json_number,
        object_pairs_hook=_reject_duplicate_object_keys,
    )
    policy = OutputAuthorizationPolicy.model_validate(raw_policy)
    if canonical_policy_json(policy) != policy_json:
        raise ValueError("policy JSON is not canonical")
    return policy


__all__ = [
    "AllowedScope",
    "DisclosureRule",
    "OperationalMessageReference",
    "OutputAuthorizationPolicy",
    "TemplateReference",
    "canonical_policy_json",
    "canonical_policy_sha256",
    "load_output_authorization_policy",
]
