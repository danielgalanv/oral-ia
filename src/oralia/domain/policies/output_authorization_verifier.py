"""Pure deterministic verifier for T090 output authorization."""

import hashlib
import re
from collections.abc import Callable, Mapping, Sequence
from string import Formatter
from typing import Any

from pydantic import BaseModel, ValidationError

from oralia.domain.policies.output_authorization_contract import (
    REASON_PRECEDENCE,
    AuthorizationReason,
    AuthorizationSnapshot,
    AuthorizationVerdict,
    OutputProposal,
)

H02Evaluator = Callable[[str], tuple[str, list[str]]]


def _plain(value: object) -> object:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    return value


def _mapping(value: object) -> Mapping[str, Any] | None:
    value = _plain(value)
    return value if isinstance(value, Mapping) else None


def _strict_positive_int(value: object) -> bool:
    return type(value) is int and value > 0


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _reason_order(reasons: Sequence[str], attempt: int) -> tuple[AuthorizationReason, ...]:
    known = {reason.value: reason for reason in REASON_PRECEDENCE}
    selected = {known[reason] for reason in reasons if reason in known}
    if attempt == 1 and selected:
        selected.add(AuthorizationReason.UNSAFE_FALLBACK)
    return tuple(reason for reason in REASON_PRECEDENCE if reason in selected)


def _optional_string(value: object) -> str | None:
    return value if isinstance(value, str) and bool(value.strip()) else None


def _optional_positive_int(value: object) -> int | None:
    return value if _strict_positive_int(value) else None


def _optional_sha256(value: object) -> str | None:
    return (
        value
        if isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
        else None
    )


def _blocked(
    reasons: Sequence[str],
    attempt: int,
    *,
    configuration: Mapping[str, Any] | None = None,
    policy: Mapping[str, Any] | None = None,
    proposal: Mapping[str, Any] | None = None,
) -> AuthorizationVerdict:
    ordered = _reason_order(reasons, attempt)
    return AuthorizationVerdict(
        verdict="block",
        reason_codes=ordered,
        activity_configuration_id=_optional_string(
            (configuration or {}).get("activity_configuration_id")
        ),
        activity_version=_optional_positive_int((configuration or {}).get("activity_version")),
        policy_id=_optional_string((policy or {}).get("policy_id")),
        policy_version=_optional_positive_int((policy or {}).get("policy_version")),
        schema_version=_optional_positive_int((policy or {}).get("schema_version")),
        policy_sha256=_optional_sha256((configuration or {}).get("policy_sha256")),
        template_id=_optional_string((proposal or {}).get("template_id")),
        template_version=_optional_positive_int((proposal or {}).get("template_version")),
        template_sha256=_optional_sha256((proposal or {}).get("template_sha256")),
        fallback_attempt=attempt,
        message_type=(
            (proposal or {}).get("message_type")
            if (proposal or {}).get("message_type") in {"normal", "operational"}
            else None
        ),
    )


def _approved(
    attempt: int,
    configuration: Mapping[str, Any],
    policy: Mapping[str, Any],
    proposal: Mapping[str, Any],
) -> AuthorizationVerdict:
    return AuthorizationVerdict(
        verdict="approved",
        reason_codes=(),
        activity_configuration_id=configuration.get("activity_configuration_id"),
        activity_version=configuration.get("activity_version"),
        policy_id=policy.get("policy_id"),
        policy_version=policy.get("policy_version"),
        schema_version=policy.get("schema_version"),
        policy_sha256=configuration.get("policy_sha256"),
        template_id=proposal.get("template_id"),
        template_version=proposal.get("template_version"),
        template_sha256=proposal.get("template_sha256"),
        fallback_attempt=attempt,
        message_type=proposal.get("message_type"),
    )


def _template_from_snapshot(
    snapshot: Mapping[str, Any],
    template_id: str,
    template_version: int,
    template_sha256: str,
) -> Mapping[str, Any] | None:
    templates = _plain(snapshot.get("templates"))
    if isinstance(templates, Mapping):
        candidate = _mapping(templates.get(template_id))
        if candidate and (
            candidate.get("template_id") == template_id
            and candidate.get("template_version", candidate.get("version")) == template_version
            and candidate.get("sha256") == template_sha256
        ):
            return candidate
        return None
    if isinstance(templates, Sequence) and not isinstance(templates, (str, bytes)):
        for value in templates:
            template = _mapping(value)
            if template and (
                template.get("template_id") == template_id
                and template.get("template_version", template.get("version")) == template_version
                and template.get("sha256") == template_sha256
            ):
                return template
    return None


def _reference_from_snapshot(
    snapshot: Mapping[str, Any],
    data_ref: str,
) -> Mapping[str, Any] | None:
    references = _plain(snapshot.get("data_references"))
    if isinstance(references, Mapping):
        return _mapping(references.get(data_ref))
    if isinstance(references, Sequence) and not isinstance(references, (str, bytes)):
        for value in references:
            reference = _mapping(value)
            if reference and reference.get("data_ref") == data_ref:
                return reference
    return None


def _scope(value: Mapping[str, Any]) -> Mapping[str, Any] | None:
    return _mapping(value.get("scope") or value.get("trusted_scope"))


def _template_reconstructs(
    template_text: str,
    proposal_text: str,
    segments: Sequence[Mapping[str, Any]],
) -> bool:
    if template_text == proposal_text:
        return True
    placeholders = [
        field_name
        for _, field_name, _, _ in Formatter().parse(template_text)
        if field_name is not None
    ]
    variable_segments = [
        segment
        for segment in segments
        if segment.get("kind") in {"slot", "general_knowledge"}
    ]
    if len(placeholders) != len(variable_segments):
        return False
    iterator = iter(variable_segments)

    def replacement(_: re.Match[str]) -> str:
        return str(next(iterator).get("expected_text", ""))

    pattern = re.compile(r"\{[^{}]+\}")
    return pattern.sub(replacement, template_text) == proposal_text


def verify_output_authorization(
    proposal: OutputProposal | Mapping[str, Any] | None,
    snapshot: AuthorizationSnapshot | Mapping[str, Any] | None,
    *,
    actual_session_id: str,
    actual_activity_configuration_id: str,
    actual_recipient: str,
    fallback_attempt: int = 0,
    h02_evaluator: H02Evaluator | None = None,
) -> AuthorizationVerdict:
    """Verify one final text without database or global-state access."""

    attempt = fallback_attempt if fallback_attempt in (0, 1) else 1
    if snapshot is None:
        return _blocked(["missing_policy"], attempt)
    if not isinstance(snapshot, AuthorizationSnapshot):
        snapshot_mapping = _mapping(snapshot)
        raw_policy = _mapping(snapshot_mapping.get("policy")) if snapshot_mapping else None
        reason = "missing_policy" if not raw_policy else "invalid_context"
        return _blocked([reason], attempt)
    snapshot_map = _mapping(snapshot)
    policy = _mapping(snapshot_map.get("policy")) if snapshot_map else None
    if not policy:
        return _blocked(["missing_policy"], attempt)

    configuration = _mapping(snapshot_map.get("configuration")) or {}
    recipient = snapshot_map.get("recipient")
    schema_version = policy.get("schema_version")
    policy_version = policy.get("policy_version")
    activity_version = configuration.get("activity_version")
    context_invalid = (
        schema_version != 1
        or not _strict_positive_int(policy_version)
        or not _strict_positive_int(activity_version)
        or not isinstance(configuration.get("activity_configuration_id"), str)
        or not configuration.get("activity_configuration_id")
        or not isinstance(policy.get("policy_id"), str)
        or not policy.get("policy_id")
        or not isinstance(recipient, str)
        or not recipient
    )
    if configuration.get("policy_id") not in (None, policy.get("policy_id")):
        context_invalid = True
    if configuration.get("policy_version") not in (None, policy_version):
        context_invalid = True
    if configuration.get("schema_version") not in (None, schema_version):
        context_invalid = True
    if (
        not isinstance(actual_session_id, str)
        or not actual_session_id
        or configuration.get("session_id") != actual_session_id
    ):
        context_invalid = True
    if (
        not isinstance(actual_activity_configuration_id, str)
        or not actual_activity_configuration_id
        or configuration.get("activity_configuration_id")
        != actual_activity_configuration_id
    ):
        context_invalid = True
    if not isinstance(actual_recipient, str) or not actual_recipient or recipient != actual_recipient:
        context_invalid = True
    allowed_recipients = policy.get("allowed_recipients")
    if allowed_recipients is not None and recipient not in allowed_recipients:
        context_invalid = True
    if context_invalid:
        return _blocked(
            ["invalid_context"],
            attempt,
            configuration=configuration,
            policy=policy,
        )

    try:
        parsed_proposal = OutputProposal.model_validate(proposal)
    except (TypeError, ValidationError):
        return _blocked(
            ["invalid_proposal"],
            attempt,
            configuration=configuration,
            policy=policy,
        )
    proposal_map = parsed_proposal.model_dump(mode="json")
    text = proposal_map.get("text")
    message_type = proposal_map.get("message_type")
    template_id = proposal_map.get("template_id")
    template_version = proposal_map.get("template_version")
    template_sha256 = proposal_map.get("template_sha256")
    segments_raw = proposal_map.get("segments")
    proposal_shape_valid = (
        isinstance(text, str)
        and bool(text)
        and message_type in {"normal", "operational"}
        and isinstance(template_id, str)
        and bool(template_id)
        and _strict_positive_int(template_version)
        and isinstance(template_sha256, str)
        and len(template_sha256) == 64
        and all(character in "0123456789abcdef" for character in template_sha256)
        and isinstance(segments_raw, Sequence)
        and not isinstance(segments_raw, (str, bytes))
        and bool(segments_raw)
    )
    if attempt == 1 and message_type != "operational":
        return _blocked(
            ["invalid_context"],
            attempt,
            configuration=configuration,
            policy=policy,
            proposal=proposal_map,
        )
    if not proposal_shape_valid:
        return _blocked(
            ["invalid_proposal"],
            attempt,
            configuration=configuration,
            policy=policy,
            proposal=proposal_map,
        )

    segments: list[Mapping[str, Any]] = []
    expected_start = 0
    for raw_segment in segments_raw:
        segment = _mapping(raw_segment)
        if segment is None:
            proposal_shape_valid = False
            break
        start = segment.get("start")
        end = segment.get("end")
        expected_text = segment.get("expected_text")
        if (
            type(start) is not int
            or type(end) is not int
            or start != expected_start
            or start < 0
            or end <= start
            or end > len(text)
            or not isinstance(expected_text, str)
            or text[start:end] != expected_text
            or segment.get("kind") not in {"fixed", "slot", "general_knowledge"}
        ):
            proposal_shape_valid = False
            break
        segments.append(segment)
        expected_start = end
    if not proposal_shape_valid or expected_start != len(text):
        return _blocked(
            ["invalid_proposal"],
            attempt,
            configuration=configuration,
            policy=policy,
            proposal=proposal_map,
        )

    template = _template_from_snapshot(
        snapshot_map,
        template_id,
        template_version,
        template_sha256,
    )
    template_text = template.get("text") if template else None
    template_scope = _scope(template) if template else None
    template_context_invalid = (
        template is None
        or template.get("template_id") != template_id
        or template.get("template_version", template.get("version")) != template_version
        or template.get("sha256") != template_sha256
        or not isinstance(template_text, str)
        or _sha256(template_text) != template_sha256
        or template_scope is None
    )
    if template_context_invalid:
        return _blocked(
            ["invalid_context"],
            attempt,
            configuration=configuration,
            policy=policy,
            proposal=proposal_map,
        )

    allowed_key = (
        "allowed_operational_messages" if message_type == "operational" else "allowed_templates"
    )
    allowed_pairs = policy.get(allowed_key, [])
    if [template_id, template_version] not in allowed_pairs and (
        template_id,
        template_version,
    ) not in allowed_pairs:
        return _blocked(
            ["unauthorized_data"],
            attempt,
            configuration=configuration,
            policy=policy,
            proposal=proposal_map,
        )

    if not _template_reconstructs(template_text, text, segments):
        return _blocked(
            ["unverified_binding"],
            attempt,
            configuration=configuration,
            policy=policy,
            proposal=proposal_map,
        )

    allowed_disclosures = {
        (
            rule.get("category"),
            rule.get("provenance"),
            rule.get("recipient"),
        )
        for raw_rule in policy.get("allowed_disclosures", [])
        if (rule := _mapping(raw_rule)) is not None
    }
    scopes = _mapping(policy.get("allowed_scopes")) or {}
    allowed_topics = set(scopes.get("topics", []))
    allowed_purposes = set(scopes.get("purposes", []))
    allowed_actions = set(scopes.get("actions", []))
    unauthorized = False
    out_of_scope = False

    for segment in segments:
        segment_scope = (
            segment.get("topic_ref"),
            segment.get("purpose_ref"),
            segment.get("action_ref"),
        )
        if not (
            segment_scope[0] in allowed_topics
            and segment_scope[1] in allowed_purposes
            and segment_scope[2] in allowed_actions
        ):
            out_of_scope = True

        kind = segment.get("kind")
        data_ref = segment.get("data_ref")
        if kind == "fixed":
            trusted_scope = (
                template_scope.get("topic_ref"),
                template_scope.get("purpose_ref"),
                template_scope.get("action_ref"),
            )
            if data_ref is not None or segment_scope != trusted_scope:
                return _blocked(
                    ["unverified_binding"],
                    attempt,
                    configuration=configuration,
                    policy=policy,
                    proposal=proposal_map,
                )
            continue
        if kind == "general_knowledge":
            if data_ref is not None:
                return _blocked(
                    ["unverified_binding"],
                    attempt,
                    configuration=configuration,
                    policy=policy,
                    proposal=proposal_map,
                )
            configuration_allows = snapshot_map.get(
                "configuration_general_knowledge_allowed",
                configuration.get("general_knowledge_allowed", False),
            )
            if not (
                policy.get("general_knowledge_allowed") is True
                and configuration_allows is True
            ):
                unauthorized = True
            continue
        if not isinstance(data_ref, str) or not data_ref:
            return _blocked(
                ["unverified_binding"],
                attempt,
                configuration=configuration,
                policy=policy,
                proposal=proposal_map,
            )
        reference = _reference_from_snapshot(snapshot_map, data_ref)
        if reference is None:
            return _blocked(
                ["unverified_binding"],
                attempt,
                configuration=configuration,
                policy=policy,
                proposal=proposal_map,
            )
        reference_scope = _scope(reference)
        if reference_scope is None or segment_scope != (
            reference_scope.get("topic_ref"),
            reference_scope.get("purpose_ref"),
            reference_scope.get("action_ref"),
        ):
            return _blocked(
                ["unverified_binding"],
                attempt,
                configuration=configuration,
                policy=policy,
                proposal=proposal_map,
            )

        disclosure = (
            reference.get("category"),
            reference.get("provenance"),
            recipient,
        )
        explicitly_authorized = (
            reference.get("recipient") == recipient
            and disclosure in allowed_disclosures
            and reference.get("authorized", True) is not False
        )
        if not explicitly_authorized:
            unauthorized = True
            continue

        # Values are read only after the complete disclosure triple is authorized.
        value = reference.get("value")
        value_sha256 = reference.get("value_sha256", reference.get("sha256"))
        expected_text = segment.get("expected_text")
        claimed_hash = segment.get("value_sha256")
        if (
            not isinstance(value, str)
            or value != expected_text
            or not isinstance(value_sha256, str)
            or value_sha256 != _sha256(value)
            or (claimed_hash is not None and claimed_hash != value_sha256)
        ):
            return _blocked(
                ["unverified_binding"],
                attempt,
                configuration=configuration,
                policy=policy,
                proposal=proposal_map,
            )

    late_reasons: list[str] = []
    if unauthorized:
        late_reasons.append("unauthorized_data")
    if out_of_scope:
        late_reasons.append("out_of_scope")
    if h02_evaluator is None:
        from oralia.domain.policies.constitutional_control import evaluate

        h02_evaluator = evaluate
    _, h02_reasons = h02_evaluator(text)
    late_reasons.extend(h02_reasons)
    if late_reasons:
        return _blocked(
            late_reasons,
            attempt,
            configuration=configuration,
            policy=policy,
            proposal=proposal_map,
        )
    return _approved(attempt, configuration, policy, proposal_map)


__all__ = ["verify_output_authorization"]
