"""Persistent unit coverage for the immutable T090 output authorization policy."""

import hashlib
import json
from copy import deepcopy

import pytest
from pydantic import ValidationError

from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
    canonical_policy_sha256,
    load_output_authorization_policy,
)


def _payload() -> dict:
    return {
        "schema_version": 1,
        "policy_id": " política-e\u0301-🙂 ",
        "policy_version": 2,
        "allowed_recipients": ["participant-z", "participant-a"],
        "allowed_disclosures": [
            {"category": "z", "provenance": "b", "recipient": "participant-z"},
            {"category": "a", "provenance": "c", "recipient": "participant-a"},
            {"category": "a", "provenance": "b", "recipient": "participant-z"},
        ],
        "allowed_scopes": {
            "topics": ["z-topic", "a-topic"],
            "purposes": ["study", "answer"],
            "actions": ["respond", "acknowledge"],
        },
        "general_knowledge_allowed": False,
        "allowed_templates": [["z-template", 2], ["a-template", 3], ["a-template", 1]],
        "allowed_operational_messages": [["z-operation", 1], ["a-operation", 2]],
    }


def _canonical_raw(payload: dict) -> str:
    return canonical_policy_json(OutputAuthorizationPolicy.model_validate(payload))


def test_canonical_json_has_exact_format_and_deterministic_collection_order() -> None:
    raw = _canonical_raw(_payload())
    decoded = json.loads(raw)

    assert raw == json.dumps(
        decoded,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    assert decoded["allowed_recipients"] == ["participant-a", "participant-z"]
    assert decoded["allowed_disclosures"] == [
        {"category": "a", "provenance": "b", "recipient": "participant-z"},
        {"category": "a", "provenance": "c", "recipient": "participant-a"},
        {"category": "z", "provenance": "b", "recipient": "participant-z"},
    ]
    assert decoded["allowed_scopes"] == {
        "actions": ["acknowledge", "respond"],
        "purposes": ["answer", "study"],
        "topics": ["a-topic", "z-topic"],
    }
    assert decoded["allowed_templates"] == [
        ["a-template", 1],
        ["a-template", 3],
        ["z-template", 2],
    ]
    assert decoded["allowed_operational_messages"] == [
        ["a-operation", 2],
        ["z-operation", 1],
    ]


def test_small_canonical_json_matches_literal_contract() -> None:
    payload = {
        "schema_version": 1,
        "policy_id": "p",
        "policy_version": 1,
        "allowed_recipients": ["r"],
        "allowed_disclosures": [],
        "allowed_scopes": {"topics": [], "purposes": [], "actions": []},
        "general_knowledge_allowed": False,
        "allowed_templates": [],
        "allowed_operational_messages": [],
    }

    assert _canonical_raw(payload) == (
        '{"allowed_disclosures":[],"allowed_operational_messages":[],'
        '"allowed_recipients":["r"],"allowed_scopes":{"actions":[],'
        '"purposes":[],"topics":[]},"allowed_templates":[],'
        '"general_knowledge_allowed":false,"policy_id":"p",'
        '"policy_version":1,"schema_version":1}'
    )


def test_input_permutations_produce_identical_canonical_json() -> None:
    original = _payload()
    permuted = deepcopy(original)
    for field in (
        "allowed_recipients",
        "allowed_disclosures",
        "allowed_templates",
        "allowed_operational_messages",
    ):
        permuted[field].reverse()
    for values in permuted["allowed_scopes"].values():
        values.reverse()

    assert _canonical_raw(original) == _canonical_raw(permuted)


def test_sha256_uses_exact_utf8_bytes_and_unicode_is_not_normalized() -> None:
    raw = _canonical_raw(_payload())

    assert canonical_policy_sha256(raw) == hashlib.sha256(raw.encode("utf-8")).hexdigest()
    assert " política-e\u0301-🙂 " in raw
    assert "política-é-🙂" not in raw


def test_canonical_round_trip_returns_frozen_tuple_collections() -> None:
    raw = _canonical_raw(_payload())
    loaded = load_output_authorization_policy(raw, canonical_policy_sha256(raw))

    assert canonical_policy_json(loaded) == raw
    assert isinstance(loaded.allowed_recipients, tuple)
    assert isinstance(loaded.allowed_disclosures, tuple)
    assert isinstance(loaded.allowed_scopes.topics, tuple)
    assert isinstance(loaded.allowed_templates, tuple)
    assert isinstance(loaded.allowed_operational_messages, tuple)
    with pytest.raises(ValidationError):
        loaded.policy_id = "changed"
    with pytest.raises(ValidationError):
        loaded.allowed_scopes.topics = ("changed",)


def test_load_rejects_hash_mismatch_and_noncanonical_json() -> None:
    raw = _canonical_raw(_payload())
    pretty = json.dumps(json.loads(raw), ensure_ascii=False, indent=2)

    with pytest.raises(ValueError):
        load_output_authorization_policy(raw, "0" * 64)
    with pytest.raises(ValueError):
        load_output_authorization_policy(pretty, canonical_policy_sha256(pretty))


def test_load_rejects_nan_extra_fields_and_duplicate_object_keys() -> None:
    raw = _canonical_raw(_payload())
    with_nan = raw.replace("{", '{"unexpected":NaN,', 1)
    with_duplicate_key = raw.replace("{", '{"schema_version":1,', 1)
    decoded = json.loads(raw)
    decoded["unexpected"] = "forbidden"
    with_extra = json.dumps(
        decoded,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )

    for invalid in (with_nan, with_duplicate_key, with_extra):
        with pytest.raises((ValueError, ValidationError)):
            load_output_authorization_policy(invalid, canonical_policy_sha256(invalid))


@pytest.mark.parametrize("constant", ["NaN", "Infinity", "-Infinity"])
def test_load_rejects_every_non_finite_json_number(constant: str) -> None:
    raw = _canonical_raw(_payload())
    invalid = raw.replace("{", f'{{"unexpected":{constant},', 1)

    with pytest.raises(ValueError):
        load_output_authorization_policy(invalid, canonical_policy_sha256(invalid))


@pytest.mark.parametrize(
    "container_key",
    ["allowed_scopes", "allowed_disclosures"],
)
def test_nested_extra_fields_are_rejected(container_key: str) -> None:
    payload = _payload()
    if container_key == "allowed_scopes":
        payload[container_key]["unexpected"] = []
    else:
        payload[container_key][0]["unexpected"] = "forbidden"

    with pytest.raises(ValidationError):
        OutputAuthorizationPolicy.model_validate(payload)


@pytest.mark.parametrize(
    "invalid",
    [
        (
            '{"actions":[],"actions":["respond"],"purposes":[],"topics":[]}'
        ),
        (
            '{"category":"public","category":"private",'
            '"provenance":"teacher","recipient":"participant-a"}'
        ),
    ],
)
def test_nested_duplicate_json_keys_are_rejected(invalid: str) -> None:
    raw = _canonical_raw(_payload())
    if '"actions"' in invalid:
        original = json.dumps(
            json.loads(raw)["allowed_scopes"],
            sort_keys=True,
            separators=(",", ":"),
        )
    else:
        original = json.dumps(
            json.loads(raw)["allowed_disclosures"][0],
            sort_keys=True,
            separators=(",", ":"),
        )
    malformed = raw.replace(original, invalid, 1)

    with pytest.raises(ValueError):
        load_output_authorization_policy(malformed, canonical_policy_sha256(malformed))


def test_recalculated_hash_does_not_make_noncanonical_json_valid() -> None:
    raw = _canonical_raw(_payload())
    decoded = json.loads(raw)
    reversed_keys = dict(reversed(list(decoded.items())))
    noncanonical_keys = json.dumps(
        reversed_keys,
        sort_keys=False,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    decoded["allowed_recipients"].reverse()
    noncanonical_collection = json.dumps(
        decoded,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )

    for invalid in (noncanonical_keys, noncanonical_collection):
        assert canonical_policy_sha256(invalid) != canonical_policy_sha256(raw)
        with pytest.raises(ValueError, match="not canonical"):
            load_output_authorization_policy(invalid, canonical_policy_sha256(invalid))


def test_unicode_escaped_json_is_rejected_when_canonical_form_is_literal() -> None:
    raw = _canonical_raw(_payload())
    escaped = raw.replace("🙂", r"\ud83d\ude42")
    assert escaped != raw

    with pytest.raises(ValueError, match="not canonical"):
        load_output_authorization_policy(escaped, canonical_policy_sha256(escaped))


@pytest.mark.parametrize("invalid_hash", ["A" * 64, "0" * 63, "g" * 64])
def test_invalid_hash_forms_are_rejected(invalid_hash: str) -> None:
    raw = _canonical_raw(_payload())

    with pytest.raises(ValueError, match="SHA-256"):
        load_output_authorization_policy(raw, invalid_hash)


def test_unknown_schema_and_boolean_versions_are_rejected() -> None:
    for field, value in (
        ("schema_version", 2),
        ("schema_version", True),
        ("policy_version", True),
    ):
        payload = _payload()
        payload[field] = value
        with pytest.raises(ValidationError):
            OutputAuthorizationPolicy.model_validate(payload)

    for field in ("allowed_templates", "allowed_operational_messages"):
        payload = _payload()
        payload[field] = [["template", True]]
        with pytest.raises(ValidationError):
            OutputAuthorizationPolicy.model_validate(payload)


@pytest.mark.parametrize(
    ("field", "duplicate"),
    [
        ("allowed_recipients", ["participant-a", "participant-a"]),
        (
            "allowed_disclosures",
            [
                {"category": "a", "provenance": "b", "recipient": "participant-a"},
                {"category": "a", "provenance": "b", "recipient": "participant-a"},
            ],
        ),
        ("allowed_templates", [["template", 1], ["template", 1]]),
        ("allowed_operational_messages", [["operation", 1], ["operation", 1]]),
    ],
)
def test_top_level_duplicate_permissions_are_rejected(field: str, duplicate: list) -> None:
    payload = _payload()
    payload[field] = duplicate
    with pytest.raises(ValidationError):
        OutputAuthorizationPolicy.model_validate(payload)


@pytest.mark.parametrize("scope", ["topics", "purposes", "actions"])
def test_scope_duplicates_are_rejected(scope: str) -> None:
    payload = _payload()
    payload["allowed_scopes"][scope] = ["same", "same"]
    with pytest.raises(ValidationError):
        OutputAuthorizationPolicy.model_validate(payload)


def test_loaded_policies_and_exported_dicts_share_no_mutable_state() -> None:
    raw = _canonical_raw(_payload())
    digest = canonical_policy_sha256(raw)
    first = load_output_authorization_policy(raw, digest)
    second = load_output_authorization_policy(raw, digest)
    exported = first.model_dump(mode="json")

    exported["allowed_recipients"].append("intruder")
    exported["allowed_scopes"]["topics"].append("intruder")

    assert "intruder" not in first.allowed_recipients
    assert "intruder" not in first.allowed_scopes.topics
    assert second == first
    assert canonical_policy_json(first) == raw


def test_policy_does_not_share_deeply_mutable_input_state() -> None:
    payload = _payload()
    policy = OutputAuthorizationPolicy.model_validate(payload)
    original = canonical_policy_json(policy)

    payload["allowed_recipients"].append("intruder")
    payload["allowed_disclosures"][0]["category"] = "changed"
    payload["allowed_scopes"]["topics"].append("intruder")
    payload["allowed_templates"][0][0] = "changed"
    payload["allowed_operational_messages"][0][0] = "changed"

    assert canonical_policy_json(policy) == original
    assert "intruder" not in policy.allowed_recipients
    assert "intruder" not in policy.allowed_scopes.topics
