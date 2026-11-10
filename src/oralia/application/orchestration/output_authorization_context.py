"""Build the minimal trusted authorization snapshot for one real session."""

from collections.abc import Iterable

from pydantic import BaseModel, ConfigDict

from oralia.domain.policies.output_authorization_contract import (
    AuthorizationConfigurationIdentity,
    AuthorizationSnapshot,
    ScopeReference,
    TrustedDataReference,
    TrustedTemplate,
)
from oralia.domain.policies.output_authorization_policy import (
    DisclosureRule,
    load_output_authorization_policy,
)
from oralia.domain.policies.output_template_catalog import (
    DEFAULT_OUTPUT_TEMPLATE_CATALOG,
    OutputTemplateCatalog,
    output_text_sha256,
)
from oralia.infrastructure.db import models


class InvalidAuthorizationContext(ValueError):
    """The supplied session/configuration cannot produce a trusted snapshot."""


class AuthorizationReferenceInput(BaseModel):
    """Trusted reference metadata supplied by the orchestration layer."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    data_ref: str
    category: str
    provenance: str
    recipient: str
    scope: ScopeReference
    value: str | None = None
    value_sha256: str | None = None


def _catalog_template(
    catalog: OutputTemplateCatalog,
    template_id: str,
    version: int,
) -> TrustedTemplate:
    matches = [
        entry
        for entry in catalog.entries
        if entry.template_id == template_id and entry.version == version
    ]
    if len(matches) != 1:
        raise InvalidAuthorizationContext("policy template version is absent from the catalog")
    entry = catalog.resolve(template_id, version, matches[0].sha256)
    return TrustedTemplate(
        template_id=entry.template_id,
        template_version=entry.version,
        message_type=entry.message_type,
        text=entry.text,
        sha256=entry.sha256,
        scope=ScopeReference(
            topic_ref=entry.topic_ref,
            purpose_ref=entry.purpose_ref,
            action_ref=entry.action_ref,
        ),
    )


def build_authorization_snapshot(
    session: models.Session,
    activity: models.ActivityConfiguration,
    *,
    data_references: Iterable[AuthorizationReferenceInput] = (),
    catalog: OutputTemplateCatalog = DEFAULT_OUTPUT_TEMPLATE_CATALOG,
) -> AuthorizationSnapshot:
    """Build a snapshot only from the supplied real session and configuration.

    This function performs no database query and has no global session dependency.
    """

    if session.activity_configuration_id != activity.id:
        raise InvalidAuthorizationContext("session and activity configuration do not match")
    if (
        activity.output_authorization_policy_json is None
        or activity.output_authorization_policy_sha256 is None
    ):
        raise InvalidAuthorizationContext("activity configuration has no complete policy")

    try:
        policy = load_output_authorization_policy(
            activity.output_authorization_policy_json,
            activity.output_authorization_policy_sha256,
        )
    except (TypeError, ValueError) as exc:
        raise InvalidAuthorizationContext("activity policy is invalid") from exc

    if policy.general_knowledge_allowed != activity.general_knowledge_allowed:
        raise InvalidAuthorizationContext("configuration and policy knowledge flags differ")

    templates = tuple(
        _catalog_template(catalog, reference.template_id, reference.version)
        for reference in policy.allowed_templates
    ) + tuple(
        _catalog_template(
            catalog,
            reference.operational_message_id,
            reference.version,
        )
        for reference in policy.allowed_operational_messages
    )

    real_recipient = session.participant_code
    trusted_references: list[TrustedDataReference] = []
    for reference in data_references:
        rule = DisclosureRule(
            category=reference.category,
            provenance=reference.provenance,
            recipient=real_recipient,
        )
        authorized = reference.recipient == real_recipient and rule in policy.allowed_disclosures
        digest = None
        if authorized:
            if reference.value is None:
                raise InvalidAuthorizationContext(
                    "authorized references require their exact value"
                )
            digest = reference.value_sha256 or output_text_sha256(reference.value)
            if reference.value_sha256 is not None and digest != output_text_sha256(reference.value):
                raise InvalidAuthorizationContext("trusted reference hash does not match its value")
        elif reference.value is not None or reference.value_sha256 is not None:
            raise InvalidAuthorizationContext(
                "denied references must contain metadata only"
            )
        trusted_references.append(
            TrustedDataReference(
                data_ref=reference.data_ref,
                category=reference.category,
                provenance=reference.provenance,
                recipient=reference.recipient,
                scope=reference.scope,
                authorized=authorized,
                value=reference.value if authorized else None,
                value_sha256=digest if authorized else None,
            )
        )

    return AuthorizationSnapshot(
        configuration=AuthorizationConfigurationIdentity(
            session_id=session.id,
            activity_configuration_id=activity.id,
            activity_version=activity.version,
            policy_id=policy.policy_id,
            policy_version=policy.policy_version,
            schema_version=policy.schema_version,
            policy_sha256=activity.output_authorization_policy_sha256,
        ),
        recipient=real_recipient,
        policy=policy,
        configuration_general_knowledge_allowed=activity.general_knowledge_allowed,
        templates=templates,
        data_references=tuple(trusted_references),
    )


__all__ = [
    "AuthorizationReferenceInput",
    "InvalidAuthorizationContext",
    "build_authorization_snapshot",
]
