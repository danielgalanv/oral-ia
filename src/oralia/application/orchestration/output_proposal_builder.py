"""Construct output proposals from trusted catalog templates and snapshot values."""

from string import Formatter

from pydantic import BaseModel, ConfigDict

from oralia.domain.policies.output_authorization_contract import (
    AuthorizationSnapshot,
    OutputProposal,
    OutputSegment,
)
from oralia.domain.policies.output_template_catalog import (
    DEFAULT_OUTPUT_TEMPLATE_CATALOG,
    OutputTemplateCatalog,
)


class ProposalConstructionError(ValueError):
    """A trusted template cannot be bound to the supplied snapshot."""


class BoundTemplateSlot(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    placeholder: str
    data_ref: str


def build_output_proposal(
    snapshot: AuthorizationSnapshot,
    *,
    template_id: str,
    template_version: int,
    template_sha256: str,
    slots: tuple[BoundTemplateSlot, ...] = (),
    catalog: OutputTemplateCatalog = DEFAULT_OUTPUT_TEMPLATE_CATALOG,
    require_policy_permission: bool = True,
) -> OutputProposal:
    """Build a proposal without accepting generator-supplied free output text."""

    try:
        entry = catalog.resolve(template_id, template_version, template_sha256)
    except (KeyError, ValueError) as exc:
        raise ProposalConstructionError("template identity is not in the trusted catalog") from exc

    trusted = next(
        (
            item
            for item in snapshot.templates
            if (
                item.template_id,
                item.template_version,
                item.sha256,
            )
            == entry.identity
        ),
        None,
    )
    if trusted is None:
        raise ProposalConstructionError("template identity is not trusted by the snapshot")

    allowed_pairs = (
        {(item.template_id, item.version) for item in snapshot.policy.allowed_templates}
        if entry.message_type == "normal"
        else {
            (item.operational_message_id, item.version)
            for item in snapshot.policy.allowed_operational_messages
        }
    )
    if require_policy_permission and (template_id, template_version) not in allowed_pairs:
        raise ProposalConstructionError("template version is not allowed by the policy")

    slots_by_name = {slot.placeholder: slot for slot in slots}
    if len(slots_by_name) != len(slots):
        raise ProposalConstructionError("slot placeholders must be unique")
    references = {item.data_ref: item for item in snapshot.data_references}

    text_parts: list[str] = []
    segments: list[OutputSegment] = []
    cursor = 0
    used_slots: set[str] = set()
    for literal, field_name, format_spec, conversion in Formatter().parse(entry.text):
        if literal:
            text_parts.append(literal)
            end = cursor + len(literal)
            segments.append(
                OutputSegment(
                    start=cursor,
                    end=end,
                    expected_text=literal,
                    kind="fixed",
                    data_ref=None,
                    topic_ref=entry.topic_ref,
                    purpose_ref=entry.purpose_ref,
                    action_ref=entry.action_ref,
                )
            )
            cursor = end
        if field_name is None:
            continue
        if format_spec or conversion:
            raise ProposalConstructionError("format specifications and conversions are forbidden")
        slot = slots_by_name.get(field_name)
        if slot is None:
            raise ProposalConstructionError("every template placeholder requires a bound slot")
        reference = references.get(slot.data_ref)
        if reference is None or not reference.authorized or reference.value is None:
            raise ProposalConstructionError("slot must use an authorized snapshot reference")
        used_slots.add(field_name)
        text_parts.append(reference.value)
        end = cursor + len(reference.value)
        if end == cursor:
            raise ProposalConstructionError("empty slot values cannot form visible segments")
        segments.append(
            OutputSegment(
                start=cursor,
                end=end,
                expected_text=reference.value,
                kind="slot",
                data_ref=reference.data_ref,
                topic_ref=reference.scope.topic_ref,
                purpose_ref=reference.scope.purpose_ref,
                action_ref=reference.scope.action_ref,
                value_sha256=reference.value_sha256,
            )
        )
        cursor = end

    if used_slots != set(slots_by_name):
        raise ProposalConstructionError("unused slot bindings are forbidden")
    text = "".join(text_parts)
    if not text or not segments:
        raise ProposalConstructionError("an output proposal must contain visible text")
    return OutputProposal(
        text=text,
        message_type=entry.message_type,
        template_id=entry.template_id,
        template_version=entry.version,
        template_sha256=entry.sha256,
        segments=tuple(segments),
    )


__all__ = [
    "BoundTemplateSlot",
    "ProposalConstructionError",
    "build_output_proposal",
]
