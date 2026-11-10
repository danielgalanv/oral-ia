"""Unit matrix for T090 snapshot, proposal construction, and pure verification."""

import asyncio
import inspect
import unicodedata
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from oralia.application.orchestration.output_authorization_context import (
    AuthorizationReferenceInput,
    InvalidAuthorizationContext,
    build_authorization_snapshot,
)
from oralia.application.orchestration.output_proposal_builder import (
    BoundTemplateSlot,
    ProposalConstructionError,
    build_output_proposal,
)
from oralia.domain.agents.agent_contract import (
    AgentError,
    AgentRequest,
    AgentResult,
    CancellationToken,
)
from oralia.domain.policies.constitutional_control import (
    ConstitutionalControl,
    constitutional_result_or_block,
    evaluate,
)
from oralia.domain.policies.output_authorization_contract import (
    AuthorizationReason,
    AuthorizationSnapshot,
    AuthorizationVerdict,
    OutputProposal,
    ScopeReference,
)
from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
    canonical_policy_sha256,
)
from oralia.domain.policies.output_authorization_verifier import (
    verify_output_authorization,
)
from oralia.domain.policies.output_template_catalog import (
    OutputTemplateCatalog,
    OutputTemplateEntry,
    output_text_sha256,
)
from tests.t090_authorization_contract_helpers import trusted_snapshot_from_dict

_SESSION_ID = "00000000-0000-0000-0000-000000000112"
_RECIPIENT = "participant-a"
_TEXT = "Allowed response."


def _scope() -> dict[str, str]:
    return {
        "topic_ref": "activity",
        "purpose_ref": "inform",
        "action_ref": "continue",
    }


def _policy(*, general_knowledge: bool = False) -> dict:
    return {
        "schema_version": 1,
        "policy_id": "policy-1",
        "policy_version": 1,
        "allowed_recipients": [_RECIPIENT],
        "allowed_disclosures": [
            {
                "category": "public",
                "provenance": "teacher",
                "recipient": _RECIPIENT,
            }
        ],
        "allowed_scopes": {
            "topics": ["activity"],
            "purposes": ["inform"],
            "actions": ["continue"],
        },
        "general_knowledge_allowed": general_knowledge,
        "allowed_templates": [["template-1", 1]],
        "allowed_operational_messages": [["operation-1", 1]],
    }


def _template(text: str = _TEXT, *, operational: bool = False) -> dict:
    return {
        "template_id": "operation-1" if operational else "template-1",
        "template_version": 1,
        "message_type": "operational" if operational else "normal",
        "text": text,
        "sha256": output_text_sha256(text),
        "scope": _scope(),
    }


def _snapshot(
    text: str = _TEXT,
    *,
    general_policy: bool = False,
    general_configuration: bool = False,
) -> dict:
    policy = _policy(general_knowledge=general_policy)
    return {
        "configuration": {
            "session_id": _SESSION_ID,
            "activity_configuration_id": "activity-1",
            "activity_version": 1,
            "policy_id": policy["policy_id"],
            "policy_version": policy["policy_version"],
            "schema_version": policy["schema_version"],
            "policy_sha256": "0" * 64,
            "general_knowledge_allowed": general_configuration,
        },
        "recipient": _RECIPIENT,
        "policy": policy,
        "configuration_general_knowledge_allowed": general_configuration,
        "templates": {"template-1": _template(text)},
        "data_references": {},
    }


def _segment(text: str, start: int, end: int, **changes: object) -> dict:
    segment = {
        "start": start,
        "end": end,
        "expected_text": text[start:end],
        "kind": "fixed",
        "data_ref": None,
        **_scope(),
    }
    segment.update(changes)
    return segment


def _proposal(text: str = _TEXT, segments: list[dict] | None = None) -> dict:
    return {
        "text": text,
        "message_type": "normal",
        "template_id": "template-1",
        "template_version": 1,
        "template_sha256": output_text_sha256(text),
        "segments": segments or [_segment(text, 0, len(text))],
    }


def _verify(proposal: dict | None, snapshot: dict | None, **kwargs: object) -> AuthorizationVerdict:
    trusted_snapshot = snapshot
    if snapshot is not None and snapshot.get("policy"):
        configuration = snapshot["configuration"]
        policy = snapshot["policy"]
        identity_matches = (
            configuration.get("policy_id", policy.get("policy_id")) == policy.get("policy_id")
            and configuration.get("policy_version", policy.get("policy_version"))
            == policy.get("policy_version")
        )
        if identity_matches:
            try:
                trusted_snapshot = trusted_snapshot_from_dict(
                    snapshot,
                    session_id=_SESSION_ID,
                )
            except (TypeError, ValueError, ValidationError):
                trusted_snapshot = snapshot
    return verify_output_authorization(
        proposal,
        trusted_snapshot,
        actual_session_id=kwargs.pop("actual_session_id", _SESSION_ID),
        actual_activity_configuration_id=kwargs.pop(
            "actual_activity_configuration_id", "activity-1"
        ),
        actual_recipient=kwargs.pop("actual_recipient", _RECIPIENT),
        h02_evaluator=evaluate,
        **kwargs,
    )


def _reasons(verdict: AuthorizationVerdict) -> list[str]:
    return [reason.value for reason in verdict.reason_codes]


def test_contract_models_are_closed_frozen_and_use_tuple_collections() -> None:
    verdict = _verify(_proposal(), _snapshot())
    assert verdict.verdict == "approved"
    assert verdict.reason_codes == ()
    with pytest.raises(ValidationError):
        verdict.verdict = "block"
    with pytest.raises(ValidationError):
        AuthorizationVerdict(
            verdict="block",
            reason_codes=(AuthorizationReason.INVALID_CONTEXT,),
            unexpected=True,
        )
    parsed = OutputProposal.model_validate(_proposal())
    assert isinstance(parsed.segments, tuple)


def test_exact_policy_configuration_catalog_and_session_identity_is_approved() -> None:
    verdict = _verify(_proposal(), _snapshot())
    assert verdict.verdict == "approved"
    assert verdict.activity_configuration_id == "activity-1"
    assert verdict.template_sha256 == output_text_sha256(_TEXT)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("actual_session_id", None),
        ("actual_session_id", "foreign-session"),
        ("actual_activity_configuration_id", None),
        ("actual_activity_configuration_id", "foreign-activity"),
        ("actual_recipient", None),
        ("actual_recipient", "participant-b"),
    ],
)
def test_each_real_execution_identity_is_required_and_must_match(field, value) -> None:
    assert _reasons(_verify(_proposal(), _snapshot(), **{field: value})) == [
        "invalid_context"
    ]


@pytest.mark.parametrize(
    "mutation",
    [
        lambda proposal: proposal.update(unexpected=True),
        lambda proposal: proposal.update(template_version=True),
        lambda proposal: proposal["segments"][0].update(unexpected=True),
        lambda proposal: proposal["segments"][0].pop("action_ref"),
    ],
    ids=["proposal-extra", "boolean-version", "segment-extra", "partial-segment"],
)
def test_proposal_and_segments_are_validated_by_closed_contracts(mutation) -> None:
    proposal = _proposal()
    mutation(proposal)
    assert _reasons(_verify(proposal, _snapshot())) == ["invalid_proposal"]


def test_template_resolution_uses_complete_identity_with_two_versions() -> None:
    first_text = "First version."
    second_text = "Second version."
    raw = _snapshot(second_text)
    raw["policy"]["allowed_templates"] = [["template-1", 1], ["template-1", 2]]
    raw["templates"] = [
        {
            **_template(first_text),
            "template_version": 1,
        },
        {
            **_template(second_text),
            "template_version": 2,
        },
    ]
    trusted = trusted_snapshot_from_dict(raw, session_id=_SESSION_ID)
    proposal = _proposal(second_text)
    proposal["template_version"] = 2
    proposal["template_sha256"] = output_text_sha256(second_text)
    approved = verify_output_authorization(
        proposal,
        trusted,
        actual_session_id=_SESSION_ID,
        actual_activity_configuration_id="activity-1",
        actual_recipient=_RECIPIENT,
        h02_evaluator=evaluate,
    )
    assert approved.verdict == "approved"

    proposal["template_sha256"] = output_text_sha256(first_text)
    assert _reasons(
        verify_output_authorization(
            proposal,
            trusted,
            actual_session_id=_SESSION_ID,
            actual_activity_configuration_id="activity-1",
            actual_recipient=_RECIPIENT,
            h02_evaluator=evaluate,
        )
    ) == ["invalid_context"]


@pytest.mark.parametrize(
    "mutation",
    [
        lambda snapshot: snapshot["configuration"].update(session_id="foreign-session"),
        lambda snapshot: snapshot["configuration"].update(policy_id="foreign-policy"),
        lambda snapshot: snapshot["configuration"].update(policy_version=2),
        lambda snapshot: snapshot.update(recipient="participant-b"),
        lambda snapshot: snapshot["templates"]["template-1"].update(sha256="f" * 64),
    ],
    ids=["foreign-session", "foreign-policy", "foreign-version", "false-recipient", "catalog-hash"],
)
def test_foreign_or_forged_context_blocks_before_proposal_checks(mutation) -> None:
    snapshot = _snapshot()
    mutation(snapshot)
    proposal = _proposal(segments=[])
    assert _reasons(_verify(proposal, snapshot)) == ["invalid_context"]


@pytest.mark.parametrize("defect", ["invented", "missing-data-ref", "orphaned-scope"])
def test_invented_absent_or_incompatible_references_are_unverified(defect: str) -> None:
    text = "secret"
    snapshot = _snapshot(text)
    snapshot["data_references"] = {
        "known": {
            "category": "public",
            "provenance": "teacher",
            "recipient": _RECIPIENT,
            "value": text,
            "sha256": output_text_sha256(text),
            "scope": _scope(),
        }
    }
    data_ref = "invented" if defect == "invented" else "known"
    changes: dict[str, object] = {"kind": "slot", "data_ref": data_ref}
    if defect == "missing-data-ref":
        changes["data_ref"] = None
    if defect == "orphaned-scope":
        changes["topic_ref"] = "other"
    proposal = _proposal(text, [_segment(text, 0, len(text), **changes)])
    assert _reasons(_verify(proposal, snapshot)) == ["unverified_binding"]


class _DeniedReference(dict):
    def get(self, key, default=None):
        if key in {"value", "value_sha256", "sha256"}:
            raise AssertionError("denied reference value was read")
        return super().get(key, default)


def test_denied_reference_reaches_verifier_without_value_or_hash() -> None:
    text = "private"
    snapshot = _snapshot(text)
    denied = _DeniedReference(
        category="private",
        provenance="record",
        recipient=_RECIPIENT,
        scope=_scope(),
        feature_002_retrievable=True,
    )
    snapshot["data_references"] = {"denied": denied}
    proposal = _proposal(
        text,
        [_segment(text, 0, len(text), kind="slot", data_ref="denied")],
    )
    assert _reasons(_verify(proposal, snapshot)) == ["unauthorized_data"]


def test_untrusted_snapshot_dictionary_cannot_create_authority() -> None:
    raw = _snapshot()
    verdict = verify_output_authorization(
        _proposal(),
        raw,
        actual_session_id=_SESSION_ID,
        actual_activity_configuration_id="activity-1",
        actual_recipient=_RECIPIENT,
        h02_evaluator=evaluate,
    )
    assert _reasons(verdict) == ["invalid_context"]


def test_every_python_unicode_boundary_can_be_covered_exactly() -> None:
    text = "A á 🙂 𝄞."
    boundaries = list(range(len(text) + 1))
    segments = [
        _segment(text, start, end)
        for start, end in zip(boundaries, boundaries[1:], strict=False)
    ]
    assert _verify(_proposal(text, segments), _snapshot(text)).verdict == "approved"


@pytest.mark.parametrize("defect", ["space-gap", "punctuation-gap", "overlap", "reversed", "out-of-range"])
def test_invalid_ranges_and_complete_coverage_fail_structurally(defect: str) -> None:
    text = "A value."
    if defect == "space-gap":
        point = text.index(" ")
        segments = [_segment(text, 0, point), _segment(text, point + 1, len(text))]
    elif defect == "punctuation-gap":
        segments = [_segment(text, 0, len(text) - 1)]
    elif defect == "overlap":
        segments = [_segment(text, 0, 3), _segment(text, 2, len(text))]
    elif defect == "reversed":
        segments = [_segment(text, 0, 2), _segment(text, 4, 3)]
    else:
        segments = [_segment(text, 0, len(text) + 1)]
    assert _reasons(_verify(_proposal(text, segments), _snapshot(text))) == ["invalid_proposal"]


def test_utf16_width_for_an_emoji_is_not_a_python_codepoint_offset() -> None:
    text = "A🙂B"
    start = text.index("🙂")
    wrong_end = start + len("🙂".encode("utf-16-le")) // 2
    segments = [
        _segment(text, 0, start),
        _segment(text, start, wrong_end, expected_text="🙂"),
        _segment(text, wrong_end, len(text)),
    ]
    assert _reasons(_verify(_proposal(text, segments), _snapshot(text))) == ["invalid_proposal"]


def test_unicode_normalization_is_never_silent() -> None:
    nfc = "Tutoría ágil."
    nfd = unicodedata.normalize("NFD", nfc)
    proposal = _proposal(nfd, [_segment(nfd, 0, len(nfd))])
    proposal["template_sha256"] = output_text_sha256(nfc)
    assert _reasons(_verify(proposal, _snapshot(nfc))) == ["unverified_binding"]


@pytest.mark.parametrize("field", ["category", "provenance", "recipient"])
def test_each_disclosure_dimension_is_required(field: str) -> None:
    text = "private"
    snapshot = _snapshot(text)
    reference = {
        "category": "public",
        "provenance": "teacher",
        "recipient": _RECIPIENT,
        "scope": _scope(),
    }
    reference[field] = "denied"
    snapshot["data_references"] = {"ref": reference}
    proposal = _proposal(
        text,
        [_segment(text, 0, len(text), kind="slot", data_ref="ref")],
    )
    assert _reasons(_verify(proposal, snapshot)) == ["unauthorized_data"]


@pytest.mark.parametrize("field", ["topic_ref", "purpose_ref", "action_ref"])
def test_each_scope_dimension_is_required(field: str) -> None:
    proposal = _proposal()
    proposal["segments"][0][field] = "outside"
    snapshot = _snapshot()
    snapshot["templates"]["template-1"]["scope"][field] = "outside"
    assert _reasons(_verify(proposal, snapshot)) == ["out_of_scope"]


@pytest.mark.parametrize(
    "policy_flag,configuration_flag,approved",
    [(False, False, False), (False, True, False), (True, False, False), (True, True, True)],
)
def test_general_knowledge_requires_policy_and_configuration_conjunction(
    policy_flag: bool,
    configuration_flag: bool,
    approved: bool,
) -> None:
    proposal = _proposal()
    proposal["segments"][0]["kind"] = "general_knowledge"
    snapshot = _snapshot(
        general_policy=policy_flag,
        general_configuration=configuration_flag,
    )
    verdict = _verify(proposal, snapshot)
    assert (verdict.verdict == "approved") is approved
    if not approved:
        assert _reasons(verdict) == ["unauthorized_data"]


def test_multiple_late_causes_are_complete_ordered_and_deduplicated() -> None:
    text = "Tu nota es 9."
    snapshot = _snapshot(text)
    snapshot["data_references"] = {
        "denied": {
            "category": "private",
            "provenance": "record",
            "recipient": _RECIPIENT,
            "scope": {**_scope(), "topic_ref": "outside"},
        }
    }
    proposal = _proposal(
        text,
        [
            _segment(
                text,
                0,
                len(text),
                kind="slot",
                data_ref="denied",
                topic_ref="outside",
            )
        ],
    )
    assert _reasons(_verify(proposal, snapshot)) == [
        "unauthorized_data",
        "out_of_scope",
        "assigns_grade",
    ]


def test_blocked_operational_attempt_appends_unsafe_fallback_last() -> None:
    text = "Tu nota es 9."
    snapshot = _snapshot(text)
    snapshot["templates"] = {"operation-1": _template(text, operational=True)}
    proposal = _proposal(text)
    proposal.update(
        message_type="operational",
        template_id="operation-1",
        template_sha256=output_text_sha256(text),
    )
    assert _reasons(_verify(proposal, snapshot, fallback_attempt=1)) == [
        "assigns_grade",
        "unsafe_fallback",
    ]


def test_verifier_has_no_database_or_global_session_dependency() -> None:
    signature = inspect.signature(verify_output_authorization)
    source = inspect.getsource(inspect.getmodule(verify_output_authorization))
    assert "db" not in signature.parameters
    assert "Session" not in signature.parameters
    assert "oralia.infrastructure" not in source


def test_snapshot_builder_binds_real_session_and_omits_denied_values() -> None:
    entry = OutputTemplateEntry.from_text(
        template_id="template-1",
        version=1,
        message_type="normal",
        text="Value: {value}.",
        topic_ref="activity",
        purpose_ref="inform",
        action_ref="continue",
    )
    catalog = OutputTemplateCatalog(entries=(entry,))
    policy_payload = _policy()
    policy_payload["allowed_operational_messages"] = []
    policy = OutputAuthorizationPolicy.model_validate(policy_payload)
    raw = canonical_policy_json(policy)
    activity = SimpleNamespace(
        id="activity-1",
        version=1,
        general_knowledge_allowed=False,
        output_authorization_policy_json=raw,
        output_authorization_policy_sha256=canonical_policy_sha256(raw),
    )
    session = SimpleNamespace(
        id=_SESSION_ID,
        activity_configuration_id="activity-1",
        participant_code=_RECIPIENT,
    )
    references = (
        AuthorizationReferenceInput(
            data_ref="allowed",
            category="public",
            provenance="teacher",
            recipient=_RECIPIENT,
            scope=ScopeReference.model_validate(_scope()),
            value="public value",
        ),
        AuthorizationReferenceInput(
            data_ref="denied",
            category="private",
            provenance="record",
            recipient=_RECIPIENT,
            scope=ScopeReference.model_validate(_scope()),
        ),
    )
    snapshot = build_authorization_snapshot(
        session,
        activity,
        data_references=references,
        catalog=catalog,
    )
    assert snapshot.configuration.session_id == _SESSION_ID
    assert snapshot.recipient == _RECIPIENT
    denied = next(item for item in snapshot.data_references if item.data_ref == "denied")
    assert denied.authorized is False
    assert denied.value is None
    assert denied.value_sha256 is None

    poisoned = (
        AuthorizationReferenceInput(
            data_ref="denied",
            category="private",
            provenance="record",
            recipient=_RECIPIENT,
            scope=ScopeReference.model_validate(_scope()),
            value="must be rejected",
        ),
    )
    with pytest.raises(InvalidAuthorizationContext):
        build_authorization_snapshot(
            session,
            activity,
            data_references=poisoned,
            catalog=catalog,
        )

    foreign = SimpleNamespace(**{**session.__dict__, "activity_configuration_id": "foreign"})
    with pytest.raises(InvalidAuthorizationContext):
        build_authorization_snapshot(foreign, activity, catalog=catalog)


def test_proposal_builder_uses_only_catalog_template_and_authorized_snapshot_slot() -> None:
    entry = OutputTemplateEntry.from_text(
        template_id="template-1",
        version=1,
        message_type="normal",
        text="Value: {value}.",
        topic_ref="activity",
        purpose_ref="inform",
        action_ref="continue",
    )
    catalog = OutputTemplateCatalog(entries=(entry,))
    policy_payload = _policy()
    policy_payload["allowed_operational_messages"] = []
    policy = OutputAuthorizationPolicy.model_validate(policy_payload)
    raw = canonical_policy_json(policy)
    activity = SimpleNamespace(
        id="activity-1",
        version=1,
        general_knowledge_allowed=False,
        output_authorization_policy_json=raw,
        output_authorization_policy_sha256=canonical_policy_sha256(raw),
    )
    session = SimpleNamespace(
        id=_SESSION_ID,
        activity_configuration_id="activity-1",
        participant_code=_RECIPIENT,
    )
    snapshot = build_authorization_snapshot(
        session,
        activity,
        data_references=(
            AuthorizationReferenceInput(
                data_ref="allowed",
                category="public",
                provenance="teacher",
                recipient=_RECIPIENT,
                scope=ScopeReference.model_validate(_scope()),
                value="public value",
            ),
        ),
        catalog=catalog,
    )
    proposal = build_output_proposal(
        snapshot,
        template_id=entry.template_id,
        template_version=entry.version,
        template_sha256=entry.sha256,
        slots=(BoundTemplateSlot(placeholder="value", data_ref="allowed"),),
        catalog=catalog,
    )
    assert proposal.text == "Value: public value."
    assert proposal.template_sha256 == entry.sha256
    assert inspect.signature(build_output_proposal).parameters.get("text") is None
    with pytest.raises(ProposalConstructionError):
        build_output_proposal(
            snapshot,
            template_id=entry.template_id,
            template_version=entry.version,
            template_sha256="f" * 64,
            catalog=catalog,
        )


def test_closed_snapshot_rejects_extra_authority_fields() -> None:
    with pytest.raises(ValidationError):
        AuthorizationSnapshot.model_validate({"unexpected": "authority"})


def test_input_mutation_does_not_change_parsed_proposal() -> None:
    raw = _proposal()
    proposal = OutputProposal.model_validate(raw)
    raw["segments"][0]["expected_text"] = "changed"
    assert proposal.segments[0].expected_text == _TEXT


def test_text_only_constitutional_call_cannot_approve() -> None:
    assert ConstitutionalControl.contract.version == "2.0.0"
    result = asyncio.run(
        ConstitutionalControl().execute(
            AgentRequest(
                session_id=_SESSION_ID,
                turn_id="00000000-0000-0000-0000-000000000113",
                input={"proposal_text": "Harmless but unbound text."},
            ),
            CancellationToken(),
        )
    )
    assert result.status == "ok"
    assert result.output is not None
    assert result.output["verdict"] == "block"
    assert result.output["reasons"] == ["missing_policy"]


def test_constitutional_control_requires_actual_recipient() -> None:
    snapshot = trusted_snapshot_from_dict(_snapshot(), session_id=_SESSION_ID)
    result = asyncio.run(
        ConstitutionalControl().execute(
            AgentRequest(
                session_id=_SESSION_ID,
                turn_id="00000000-0000-0000-0000-000000000114",
                input={"proposal": _proposal(), "proposal_text": _TEXT},
                context={
                    "activity_configuration_id": "activity-1",
                    "authorization_snapshot": snapshot,
                },
            ),
            CancellationToken(),
        )
    )
    assert result.output["verdict"] == "block"
    assert result.output["reasons"] == ["invalid_context"]


def _valid_authorization_result() -> AgentResult:
    verdict = _verify(_proposal(), _snapshot())
    return AgentResult(
        status="ok",
        output={
            "verdict": "approved",
            "reasons": [],
            "authorization_context": verdict.model_dump(
                mode="json",
                exclude={"verdict", "reason_codes"},
                exclude_none=True,
            ),
        },
    )


@pytest.mark.parametrize(
    "mutation",
    [
        lambda output: output.pop("authorization_context"),
        lambda output: output.update(verdict="block", reasons=["invented_reason"]),
        lambda output: output.update(reasons=["invalid_context", "invalid_context"]),
        lambda output: output.update(
            reasons=["unsafe_fallback", "invalid_context"]
        ),
        lambda output: output.update(reasons=["invalid_context"]),
        lambda output: output.update(verdict="block", reasons=[]),
        lambda output: output["authorization_context"].update(fallback_attempt=1),
        lambda output: output["authorization_context"].pop("policy_sha256"),
        lambda output: output["authorization_context"].update(
            message_type="operational"
        ),
    ],
    ids=[
        "missing-context",
        "unknown-reason",
        "duplicate-reason",
        "wrong-precedence",
        "approved-with-reasons",
        "block-without-reasons",
        "wrong-attempt",
        "incomplete-approved-identity",
        "wrong-message-type",
    ],
)
def test_constitutional_result_never_implicitly_approves_ambiguous_shapes(mutation) -> None:
    result = _valid_authorization_result()
    mutation(result.output)
    assert constitutional_result_or_block(result) == ("block", ["invalid_context"])


@pytest.mark.parametrize(
    "result",
    [
        None,
        AgentResult(status="ok", output=None),
        AgentResult(
            status="error",
            error=AgentError(code="CONTROL_ERROR", message="controlled"),
        ),
        AgentResult(status="timeout", output=None),
        AgentResult(status="cancelled", output=None),
    ],
    ids=["absent", "no-output", "error", "timeout", "cancelled"],
)
def test_missing_error_timeout_or_cancelled_control_result_blocks(result) -> None:
    assert constitutional_result_or_block(result) == ("block", ["invalid_context"])
    assert constitutional_result_or_block(result, fallback_attempt=1) == (
        "block",
        ["invalid_context", "unsafe_fallback"],
    )
