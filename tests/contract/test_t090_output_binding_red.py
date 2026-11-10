"""T093: reproduce missing structural output binding through today's agent API.

All policy, template, reference, scope, proposal, and segment structures are local
dictionaries. They describe the future contract without importing future types.
"""

import asyncio
import hashlib
import unicodedata
from copy import deepcopy
from uuid import UUID

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.policies.constitutional_control import ConstitutionalControl
from tests.t090_authorization_contract_helpers import trusted_snapshot_from_dict

_SESSION_ID = UUID("00000000-0000-0000-0000-000000000093")
_TURN_ID = UUID("00000000-0000-0000-0000-000000000094")
_ASCII_TEXT = "The session starts tomorrow."
_ASCII_TEMPLATE_TEXT = "The session starts {schedule}."
_UNICODE_TEXT = "Tutoría ágil 🙂 𝄞."
_NFC_TEXT = "Tutoría ágil."


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _segment(
    text: str,
    start: int,
    end: int,
    *,
    kind: str = "fixed",
    data_ref: str | None = None,
    topic_ref: str = "activity-logistics",
    purpose_ref: str = "inform-participant",
    action_ref: str = "continue-activity",
) -> dict:
    return {
        "start": start,
        "end": end,
        "expected_text": text[start:end],
        "kind": kind,
        "data_ref": data_ref,
        "topic_ref": topic_ref,
        "purpose_ref": purpose_ref,
        "action_ref": action_ref,
    }


def _ascii_segments(text: str = _ASCII_TEXT) -> list[dict]:
    slot_start = text.index("tomorrow")
    slot_end = slot_start + len("tomorrow")
    return [
        _segment(text, 0, slot_start),
        _segment(text, slot_start, slot_end, kind="slot", data_ref="schedule-1"),
        _segment(text, slot_end, len(text)),
    ]


def _template(*, unicode_text: bool = False) -> dict:
    text = _UNICODE_TEXT if unicode_text else _ASCII_TEMPLATE_TEXT
    template_id = "unicode-confirmation" if unicode_text else "schedule-confirmation"
    return {
        "template_id": template_id,
        "template_version": 1,
        "text": text,
        "sha256": _sha256(text),
        "trusted_scope": {
            "topic_ref": "activity-logistics",
            "purpose_ref": "inform-participant",
            "action_ref": "continue-activity",
        },
    }


def _snapshot(*, unicode_text: bool = False) -> dict:
    template = _template(unicode_text=unicode_text)
    return {
        "configuration": {
            "activity_configuration_id": "activity-config-1",
            "activity_version": 3,
        },
        "policy": {
            "policy_id": "output-policy-1",
            "policy_version": 2,
            "schema_version": 1,
            "allowed_templates": [
                [template["template_id"], template["template_version"]]
            ],
            "allowed_scopes": {
                "topics": ["activity-logistics", "activity-content"],
                "purposes": ["inform-participant"],
                "actions": ["continue-activity"],
            },
            "allowed_disclosures": [
                {
                    "category": "activity_schedule",
                    "provenance": "teacher_activity",
                    "recipient": "participant-a",
                }
            ],
        },
        "recipient": "participant-a",
        "templates": {template["template_id"]: template},
        "data_references": {
            "schedule-1": {
                "category": "activity_schedule",
                "provenance": "teacher_activity",
                "recipient": "participant-a",
                "value": "tomorrow",
                "sha256": _sha256("tomorrow"),
                "scope": template["trusted_scope"],
            }
        },
    }


def _proposal(text: str, segments: list[dict], *, unicode_text: bool = False) -> dict:
    template = _template(unicode_text=unicode_text)
    return {
        "text": text,
        "message_type": "normal",
        "template_id": template["template_id"],
        "template_version": template["template_version"],
        "template_sha256": template["sha256"],
        "segments": segments,
    }


def _positive_ascii() -> tuple[dict, dict]:
    return _proposal(_ASCII_TEXT, _ascii_segments()), _snapshot()


def _positive_unicode() -> tuple[dict, dict]:
    text = _UNICODE_TEXT
    boundaries = [0, text.index("á"), text.index("🙂"), text.index("𝄞"), len(text)]
    segments = [
        _segment(text, start, end)
        for start, end in zip(boundaries, boundaries[1:], strict=False)
    ]
    return _proposal(text, segments, unicode_text=True), _snapshot(unicode_text=True)


def _cases() -> list[tuple[str, dict, dict, str, str | None]]:
    ascii_proposal, ascii_snapshot = _positive_ascii()
    unicode_proposal, unicode_snapshot = _positive_unicode()

    invented = deepcopy(ascii_proposal)
    invented["segments"][1]["data_ref"] = "schedule-invented"

    forged_scope = deepcopy(ascii_proposal)
    forged_scope["segments"][1]["topic_ref"] = "activity-content"

    gap = deepcopy(ascii_proposal)
    gap_at = 5
    gap["segments"] = [
        _segment(_ASCII_TEXT, 0, gap_at),
        _segment(_ASCII_TEXT, gap_at + 1, len(_ASCII_TEXT)),
    ]

    overlap = deepcopy(ascii_proposal)
    overlap_at = 10
    overlap["segments"] = [
        _segment(_ASCII_TEXT, 0, overlap_at + 1),
        _segment(_ASCII_TEXT, overlap_at, len(_ASCII_TEXT)),
    ]

    uncovered_space = deepcopy(ascii_proposal)
    space_at = _ASCII_TEXT.index(" ")
    uncovered_space["segments"] = [
        _segment(_ASCII_TEXT, 0, space_at),
        _segment(_ASCII_TEXT, space_at + 1, len(_ASCII_TEXT)),
    ]

    uncovered_punctuation = deepcopy(ascii_proposal)
    uncovered_punctuation["segments"] = [_segment(_ASCII_TEXT, 0, len(_ASCII_TEXT) - 1)]

    wrong_offset = deepcopy(unicode_proposal)
    emoji_start = _UNICODE_TEXT.index("🙂")
    utf16_width = len("🙂".encode("utf-16-le")) // 2
    wrong_end = emoji_start + utf16_width
    wrong_segments = [
        _segment(_UNICODE_TEXT, 0, emoji_start),
        {
            **_segment(_UNICODE_TEXT, emoji_start, wrong_end),
            "expected_text": "🙂",
        },
        _segment(_UNICODE_TEXT, wrong_end, len(_UNICODE_TEXT)),
    ]
    assert wrong_segments[0]["start"] == 0
    assert all(
        left["end"] == right["start"]
        for left, right in zip(wrong_segments, wrong_segments[1:], strict=False)
    )
    assert wrong_segments[-1]["end"] == len(_UNICODE_TEXT)
    assert all(0 <= segment["start"] < segment["end"] <= len(_UNICODE_TEXT) for segment in wrong_segments)
    covered_indices = [
        index
        for segment in wrong_segments
        for index in range(segment["start"], segment["end"])
    ]
    assert covered_indices == list(range(len(_UNICODE_TEXT)))
    assert _UNICODE_TEXT[emoji_start:wrong_end] != "🙂"
    assert utf16_width != len("🙂")
    wrong_offset["segments"] = wrong_segments

    nfd_text = unicodedata.normalize("NFD", _NFC_TEXT)
    normalization_mismatch = {
        "text": nfd_text,
        "message_type": "normal",
        "template_id": "normalization-confirmation",
        "template_version": 1,
        "template_sha256": _sha256(_NFC_TEXT),
        "segments": [_segment(nfd_text, 0, len(nfd_text))],
    }
    normalization_snapshot = _snapshot()
    normalization_snapshot["policy"]["allowed_templates"] = [
        ["normalization-confirmation", 1]
    ]
    normalization_snapshot["templates"] = {
        "normalization-confirmation": {
            "template_id": "normalization-confirmation",
            "template_version": 1,
            "text": _NFC_TEXT,
            "sha256": _sha256(_NFC_TEXT),
            "trusted_scope": _template()["trusted_scope"],
        }
    }

    return [
        ("exact_ascii_binding", ascii_proposal, ascii_snapshot, "approved", None),
        ("exact_unicode_codepoint_binding", unicode_proposal, unicode_snapshot, "approved", None),
        ("invented_data_reference", invented, ascii_snapshot, "block", "unverified_binding"),
        ("forged_scope_label", forged_scope, ascii_snapshot, "block", "unverified_binding"),
        ("one_character_gap", gap, ascii_snapshot, "block", "invalid_proposal"),
        ("overlapping_segments", overlap, ascii_snapshot, "block", "invalid_proposal"),
        ("uncovered_space", uncovered_space, ascii_snapshot, "block", "invalid_proposal"),
        (
            "uncovered_punctuation",
            uncovered_punctuation,
            ascii_snapshot,
            "block",
            "invalid_proposal",
        ),
        (
            "wrong_utf16_or_byte_offset",
            wrong_offset,
            unicode_snapshot,
            "block",
            "invalid_proposal",
        ),
        (
            "unicode_normalization_mismatch",
            normalization_mismatch,
            normalization_snapshot,
            "block",
            "unverified_binding",
        ),
    ]


_CASES = _cases()


@pytest.mark.contract
@pytest.mark.parametrize(
    "case_id,proposal,snapshot,expected_verdict,expected_reason",
    _CASES,
    ids=[case[0] for case in _CASES],
)
def test_final_text_requires_complete_verified_binding(
    case_id: str,
    proposal: dict,
    snapshot: dict,
    expected_verdict: str,
    expected_reason: str | None,
) -> None:
    trusted_snapshot = trusted_snapshot_from_dict(snapshot, session_id=str(_SESSION_ID))
    result = asyncio.run(
        ConstitutionalControl().execute(
            AgentRequest(
                session_id=_SESSION_ID,
                turn_id=_TURN_ID,
                input={"proposal_text": proposal["text"], "proposal": proposal},
                context={
                    "activity_configuration_id": (
                        trusted_snapshot.configuration.activity_configuration_id
                    ),
                    "actual_recipient": "participant-a",
                    "authorization_snapshot": trusted_snapshot,
                },
            ),
            CancellationToken(),
        )
    )

    assert result.status == "ok", case_id
    assert result.output is not None, case_id
    assert result.output["verdict"] == expected_verdict, case_id
    reasons = result.output["reasons"]
    assert isinstance(reasons, list), case_id
    if expected_reason is None:
        assert reasons == [], case_id
    else:
        assert expected_reason in reasons, case_id
