"""Closed immutable contracts for T090 output authorization."""

from enum import StrEnum
from typing import Annotated, Literal, Self

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StringConstraints,
    model_validator,
)

from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
    canonical_policy_sha256,
)
from oralia.domain.policies.output_template_catalog import output_text_sha256


def _non_blank(value: str) -> str:
    if not value.strip():
        raise ValueError("string must contain a non-whitespace character")
    return value


NonBlankString = Annotated[
    str,
    StringConstraints(strict=True, min_length=1),
    AfterValidator(_non_blank),
]
PositiveStrictInt = Annotated[int, Field(strict=True, gt=0)]
NonNegativeStrictInt = Annotated[int, Field(strict=True, ge=0)]
Sha256Hex = Annotated[
    str,
    StringConstraints(strict=True, min_length=64, max_length=64, pattern=r"^[0-9a-f]{64}$"),
]
MessageType = Literal["normal", "operational"]
SegmentKind = Literal["fixed", "slot", "general_knowledge"]


class AuthorizationReason(StrEnum):
    MISSING_POLICY = "missing_policy"
    INVALID_CONTEXT = "invalid_context"
    INVALID_PROPOSAL = "invalid_proposal"
    UNVERIFIED_BINDING = "unverified_binding"
    UNAUTHORIZED_DATA = "unauthorized_data"
    OUT_OF_SCOPE = "out_of_scope"
    ASSIGNS_GRADE = "assigns_grade"
    ASSIGNS_SCORE_FRACTION = "assigns_score_fraction"
    ACADEMIC_DECISION = "academic_decision"
    IMPERSONATES_PROFESSOR = "impersonates_professor"
    UNSAFE_FALLBACK = "unsafe_fallback"


REASON_PRECEDENCE: tuple[AuthorizationReason, ...] = (
    AuthorizationReason.MISSING_POLICY,
    AuthorizationReason.INVALID_CONTEXT,
    AuthorizationReason.INVALID_PROPOSAL,
    AuthorizationReason.UNVERIFIED_BINDING,
    AuthorizationReason.UNAUTHORIZED_DATA,
    AuthorizationReason.OUT_OF_SCOPE,
    AuthorizationReason.ASSIGNS_GRADE,
    AuthorizationReason.ASSIGNS_SCORE_FRACTION,
    AuthorizationReason.ACADEMIC_DECISION,
    AuthorizationReason.IMPERSONATES_PROFESSOR,
    AuthorizationReason.UNSAFE_FALLBACK,
)


class AuthorizationConfigurationIdentity(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    session_id: NonBlankString
    activity_configuration_id: NonBlankString
    activity_version: PositiveStrictInt
    policy_id: NonBlankString
    policy_version: PositiveStrictInt
    schema_version: Annotated[int, Field(strict=True, ge=1, le=1)]
    policy_sha256: Sha256Hex


class ScopeReference(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    topic_ref: NonBlankString
    purpose_ref: NonBlankString
    action_ref: NonBlankString


class TrustedTemplate(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    template_id: NonBlankString
    template_version: PositiveStrictInt
    message_type: MessageType
    text: NonBlankString
    sha256: Sha256Hex
    scope: ScopeReference

    @model_validator(mode="after")
    def verify_exact_text_hash(self) -> Self:
        if self.sha256 != output_text_sha256(self.text):
            raise ValueError("trusted template hash must match its exact UTF-8 text")
        return self


class TrustedDataReference(BaseModel):
    """Filtered reference; denied references deliberately omit value and value hash."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    data_ref: NonBlankString
    category: NonBlankString
    provenance: NonBlankString
    recipient: NonBlankString
    scope: ScopeReference
    authorized: StrictBool
    value: str | None = None
    value_sha256: Sha256Hex | None = None

    @model_validator(mode="after")
    def protect_denied_values(self) -> Self:
        if not self.authorized and (self.value is not None or self.value_sha256 is not None):
            raise ValueError("denied references must not contain values or value hashes")
        if self.authorized and self.value is None:
            raise ValueError("authorized references require their exact value")
        if self.authorized:
            expected = output_text_sha256(self.value)
            if self.value_sha256 != expected:
                raise ValueError("authorized reference hash must match its exact value")
        return self


class AuthorizationSnapshot(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    configuration: AuthorizationConfigurationIdentity
    recipient: NonBlankString
    policy: OutputAuthorizationPolicy
    configuration_general_knowledge_allowed: StrictBool
    templates: tuple[TrustedTemplate, ...]
    data_references: tuple[TrustedDataReference, ...]

    @model_validator(mode="after")
    def validate_identity(self) -> Self:
        identity = self.configuration
        if (
            identity.policy_id != self.policy.policy_id
            or identity.policy_version != self.policy.policy_version
            or identity.schema_version != self.policy.schema_version
        ):
            raise ValueError("configuration identity must match the embedded policy")
        canonical = canonical_policy_json(self.policy)
        if identity.policy_sha256 != canonical_policy_sha256(canonical):
            raise ValueError("configuration policy hash must match the canonical policy")
        template_ids = [(item.template_id, item.template_version) for item in self.templates]
        if len(template_ids) != len(set(template_ids)):
            raise ValueError("trusted template identities must be unique")
        reference_ids = [item.data_ref for item in self.data_references]
        if len(reference_ids) != len(set(reference_ids)):
            raise ValueError("trusted data reference identities must be unique")
        allowed_disclosures = {
            (rule.category, rule.provenance, rule.recipient)
            for rule in self.policy.allowed_disclosures
        }
        for reference in self.data_references:
            triple = (reference.category, reference.provenance, self.recipient)
            should_be_authorized = (
                reference.recipient == self.recipient and triple in allowed_disclosures
            )
            if reference.authorized is not should_be_authorized:
                raise ValueError("reference authorization must match policy and real recipient")
        return self


class OutputSegment(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    start: NonNegativeStrictInt
    end: PositiveStrictInt
    expected_text: str
    kind: SegmentKind
    data_ref: NonBlankString | None = None
    topic_ref: NonBlankString
    purpose_ref: NonBlankString
    action_ref: NonBlankString
    value_sha256: Sha256Hex | None = None


class OutputProposal(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    text: NonBlankString
    message_type: MessageType
    template_id: NonBlankString
    template_version: PositiveStrictInt
    template_sha256: Sha256Hex
    segments: tuple[OutputSegment, ...]


class AuthorizationVerdict(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    verdict: Literal["approved", "block"]
    reason_codes: tuple[AuthorizationReason, ...]
    activity_configuration_id: NonBlankString | None = None
    activity_version: PositiveStrictInt | None = None
    policy_id: NonBlankString | None = None
    policy_version: PositiveStrictInt | None = None
    schema_version: PositiveStrictInt | None = None
    policy_sha256: Sha256Hex | None = None
    template_id: NonBlankString | None = None
    template_version: PositiveStrictInt | None = None
    template_sha256: Sha256Hex | None = None
    fallback_attempt: Literal[0, 1] = 0
    message_type: MessageType | None = None

    @model_validator(mode="after")
    def validate_verdict_reasons(self) -> Self:
        if self.verdict == "approved" and self.reason_codes:
            raise ValueError("approved verdicts cannot contain reasons")
        if self.verdict == "block" and not self.reason_codes:
            raise ValueError("blocked verdicts require at least one reason")
        if tuple(dict.fromkeys(self.reason_codes)) != self.reason_codes:
            raise ValueError("reason codes must be unique")
        expected = tuple(reason for reason in REASON_PRECEDENCE if reason in self.reason_codes)
        if expected != self.reason_codes:
            raise ValueError("reason codes must follow contractual precedence")
        return self


__all__ = [
    "AuthorizationConfigurationIdentity",
    "AuthorizationReason",
    "AuthorizationSnapshot",
    "AuthorizationVerdict",
    "MessageType",
    "OutputProposal",
    "OutputSegment",
    "REASON_PRECEDENCE",
    "ScopeReference",
    "SegmentKind",
    "TrustedDataReference",
    "TrustedTemplate",
]
