"""T092: reproduce the missing contextual disclosure check through today's agent API.

The local dictionaries describe test authority only. They do not grant authority to
generator-supplied labels; the future verifier must compare them with trusted context.
"""

import asyncio
import hashlib
from uuid import UUID

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.policies.constitutional_control import ConstitutionalControl
from tests.t090_authorization_contract_helpers import trusted_snapshot_from_dict

_TEXT = "La tutoría se celebrará en el aula norte."
_SESSION_ID = UUID("00000000-0000-0000-0000-000000000092")
_TURN_ID = UUID("00000000-0000-0000-0000-000000000093")


def _policy() -> dict:
    return {
        "policy_id": "t090-disclosure-policy",
        "policy_version": 1,
        "schema_version": 1,
        "allowed_disclosures": [
            {
                "category": "activity_schedule",
                "provenance": "teacher_activity",
                "recipient": "participant-a",
            }
        ],
        "allowed_recipients": ["participant-a"],
        "allowed_scopes": {
            "topics": ["activity-logistics"],
            "purposes": ["inform-participant"],
            "actions": ["continue-activity"],
        },
        "general_knowledge_allowed": False,
        "allowed_templates": [["schedule-confirmation", 1]],
        "allowed_operational_messages": [],
    }


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _request(
    *,
    category: str = "activity_schedule",
    provenance: str = "teacher_activity",
    recipient: str = "participant-a",
    policy: dict | None,
) -> AgentRequest:
    data_reference = {
        "data_ref": "schedule-1",
        "category": category,
        "provenance": provenance,
        "recipient": recipient,
        "scope": {
            "topic_ref": "activity-logistics",
            "purpose_ref": "inform-participant",
            "action_ref": "continue-activity",
        },
    }
    if (category, provenance, recipient) == (
        "activity_schedule",
        "teacher_activity",
        "participant-a",
    ):
        data_reference.update(value=_TEXT, sha256=_sha256(_TEXT))
    proposal = {
        "text": _TEXT,
        "message_type": "normal",
        "template_id": "schedule-confirmation",
        "template_version": 1,
        "template_sha256": _sha256(_TEXT),
        "segments": [
            {
                "start": 0,
                "end": len(_TEXT),
                "expected_text": _TEXT,
                "kind": "slot",
                "data_ref": "schedule-1",
                "topic_ref": "activity-logistics",
                "purpose_ref": "inform-participant",
                "action_ref": "continue-activity",
            }
        ],
    }
    snapshot = {
        "configuration": {
            "session_id": str(_SESSION_ID),
            "activity_configuration_id": "activity-1",
            "activity_version": 1,
            "policy_id": "t090-disclosure-policy",
            "policy_version": 1,
        },
        "recipient": "participant-a",
        "policy": policy,
        "templates": {
            "schedule-confirmation": {
                "template_id": "schedule-confirmation",
                "template_version": 1,
                "text": _TEXT,
                "sha256": _sha256(_TEXT),
                "scope": data_reference["scope"],
            }
        },
        "data_references": {"schedule-1": data_reference},
    }
    trusted_snapshot = (
        trusted_snapshot_from_dict(snapshot, session_id=str(_SESSION_ID))
        if policy is not None and policy.get("schema_version") == 1
        else snapshot
    )
    return AgentRequest(
        session_id=_SESSION_ID,
        turn_id=_TURN_ID,
        input={"proposal_text": _TEXT, "proposal": proposal},
        context={
            "activity_configuration_id": (
                trusted_snapshot.configuration.activity_configuration_id
                if hasattr(trusted_snapshot, "configuration")
                else snapshot["configuration"]["activity_configuration_id"]
            ),
            "actual_recipient": "participant-a",
            "authorization_snapshot": trusted_snapshot,
        },
    )


@pytest.mark.contract
@pytest.mark.parametrize(
    "case_id,category,provenance,recipient,policy_kind,expected_verdict,expected_reason",
    [
        (
            "allowed_triple",
            "activity_schedule",
            "teacher_activity",
            "participant-a",
            "valid",
            "approved",
            None,
        ),
        (
            "denied_category",
            "private_profile",
            "teacher_activity",
            "participant-a",
            "valid",
            "block",
            "unauthorized_data",
        ),
        (
            "denied_provenance",
            "activity_schedule",
            "internal_record",
            "participant-a",
            "valid",
            "block",
            "unauthorized_data",
        ),
        (
            "denied_recipient",
            "activity_schedule",
            "teacher_activity",
            "participant-b",
            "valid",
            "block",
            "unauthorized_data",
        ),
        (
            "unknown_category",
            "unlisted_category",
            "teacher_activity",
            "participant-a",
            "valid",
            "block",
            "unauthorized_data",
        ),
        (
            "missing_policy",
            "activity_schedule",
            "teacher_activity",
            "participant-a",
            "missing",
            "block",
            "missing_policy",
        ),
        (
            "invalid_policy_version",
            "activity_schedule",
            "teacher_activity",
            "participant-a",
            "invalid",
            "block",
            "invalid_context",
        ),
    ],
    ids=lambda value: value if value in {
        "allowed_triple",
        "denied_category",
        "denied_provenance",
        "denied_recipient",
        "unknown_category",
        "missing_policy",
        "invalid_policy_version",
    } else None,
)
def test_contextual_disclosure_requires_explicit_policy(
    case_id: str,
    category: str,
    provenance: str,
    recipient: str,
    policy_kind: str,
    expected_verdict: str,
    expected_reason: str | None,
) -> None:
    policy = None if policy_kind == "missing" else _policy()
    if policy_kind == "invalid":
        assert policy is not None
        policy["schema_version"] = 999

    result = asyncio.run(
        ConstitutionalControl().execute(
            _request(category=category, provenance=provenance, recipient=recipient, policy=policy),
            CancellationToken(),
        )
    )

    assert result.status == "ok", case_id
    assert result.output is not None, case_id
    assert result.output["verdict"] == expected_verdict, case_id
    reasons = result.output["reasons"]
    if expected_reason is None:
        assert reasons == [], case_id
    else:
        assert expected_reason in reasons, case_id
