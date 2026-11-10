"""Trusted test-only adapter from frozen contract dictionaries to T090 models."""

from collections.abc import Mapping
from typing import Any

from oralia.domain.policies.output_authorization_contract import (
    AuthorizationConfigurationIdentity,
    AuthorizationSnapshot,
    ScopeReference,
    TrustedDataReference,
    TrustedTemplate,
)
from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
    canonical_policy_sha256,
)


def trusted_snapshot_from_dict(
    raw: Mapping[str, Any],
    *,
    session_id: str,
) -> AuthorizationSnapshot:
    """Construct trusted authority explicitly; raw dictionaries remain untrusted."""

    recipient = raw["recipient"]
    policy_payload = dict(raw["policy"])
    policy_payload.setdefault("allowed_recipients", [recipient])
    policy_payload.setdefault("allowed_disclosures", [])
    policy_payload.setdefault(
        "allowed_scopes",
        {"topics": [], "purposes": [], "actions": []},
    )
    policy_payload.setdefault("general_knowledge_allowed", False)
    policy_payload.setdefault("allowed_templates", [])
    policy_payload.setdefault("allowed_operational_messages", [])
    policy = OutputAuthorizationPolicy.model_validate(policy_payload)
    policy_json = canonical_policy_json(policy)
    policy_sha256 = canonical_policy_sha256(policy_json)

    configuration = raw["configuration"]
    identity = AuthorizationConfigurationIdentity(
        session_id=configuration.get("session_id", session_id),
        activity_configuration_id=configuration["activity_configuration_id"],
        activity_version=configuration["activity_version"],
        policy_id=policy.policy_id,
        policy_version=policy.policy_version,
        schema_version=policy.schema_version,
        policy_sha256=policy_sha256,
    )
    normal_pairs = {
        (reference.template_id, reference.version) for reference in policy.allowed_templates
    }
    templates_raw = raw.get("templates", {})
    template_values = (
        templates_raw.values()
        if isinstance(templates_raw, Mapping)
        else templates_raw
    )
    templates = []
    for template in template_values:
        scope = template.get("scope") or template.get("trusted_scope")
        pair = (template["template_id"], template["template_version"])
        templates.append(
            TrustedTemplate(
                template_id=template["template_id"],
                template_version=template["template_version"],
                message_type="normal" if pair in normal_pairs else "operational",
                text=template["text"],
                sha256=template["sha256"],
                scope=ScopeReference.model_validate(scope),
            )
        )

    allowed_disclosures = {
        (rule.category, rule.provenance, rule.recipient)
        for rule in policy.allowed_disclosures
    }
    references = []
    for data_ref, reference in raw.get("data_references", {}).items():
        authorized = (
            reference.get("recipient") == recipient
            and (
                reference.get("category"),
                reference.get("provenance"),
                recipient,
            )
            in allowed_disclosures
        )
        references.append(
            TrustedDataReference(
                data_ref=data_ref,
                category=reference["category"],
                provenance=reference["provenance"],
                recipient=reference["recipient"],
                scope=ScopeReference.model_validate(reference["scope"]),
                authorized=authorized,
                value=reference.get("value") if authorized else None,
                value_sha256=(
                    reference.get("value_sha256", reference.get("sha256"))
                    if authorized
                    else None
                ),
            )
        )
    configuration_general = raw.get(
        "configuration_general_knowledge_allowed",
        configuration.get("general_knowledge_allowed", False),
    )
    return AuthorizationSnapshot(
        configuration=identity,
        recipient=recipient,
        policy=policy,
        configuration_general_knowledge_allowed=configuration_general,
        templates=tuple(templates),
        data_references=tuple(references),
    )


__all__ = ["trusted_snapshot_from_dict"]
