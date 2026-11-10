"""Closed technical values, not just closed dictionary keys."""

import json

from oralia.application.services.session_privacy_service import technical_payload


def test_nested_allowed_keys_cannot_carry_free_text():
    sentinel = "PRIVATE_SENTINEL_academic_response"
    payload = {
        "model": sentinel,
        "scope": [sentinel],
        "reasons": [sentinel],
        "reason_codes": ["invalid_context", sentinel],
        "authorization_context": {"status": sentinel, "reasons": [sentinel]},
        "activated_steps": [{"step_id": sentinel, "agent_id": sentinel}],
        "status": "ok",
        "attempt": 1,
    }
    projected = technical_payload(payload)
    assert sentinel not in json.dumps(projected)
    assert projected["status"] == "ok"
    assert projected["attempt"] == 1
    assert projected["reason_codes"] == ["invalid_context"]


def test_wrong_types_are_not_technical_metadata():
    projected = technical_payload({"attempt": "private", "blocked": "private", "model": {"status": "ok"}})
    assert projected == {}
    assert technical_payload({"attempt": 10**400, "latency_ms": float("nan")}) == {}


def test_valid_identifiers_and_codes_survive_and_projection_is_idempotent():
    payload = {
        "verification_result_id": "01000000-0000-0000-0000-000000000001",
        "policy_sha256": "a" * 64,
        "scope": ["transcript", "summary"],
        "reason_codes": ["out_of_scope"],
        "latency_ms": 5,
        "blocked": True,
    }
    assert technical_payload(payload) == payload
    assert technical_payload(technical_payload(payload)) == payload


def test_real_producer_grounding_and_coherence_codes_are_preserved():
    payload = {
        "grounding_verdict": "no_fundamentada",
        "coherence_verdict": "reformulate",
        "incident_types": ["repeticion"],
        "recovery_action": "pedir_aclaracion",
        "activated_steps": [
            {"step_id": "generate-question", "agent_id": "practice-question-agent", "role": "generator"}
        ],
    }
    assert technical_payload(payload) == payload
