"""Contract tests for the immutable T090 output-template catalog."""

import hashlib
from dataclasses import dataclass

import pytest
from pydantic import ValidationError

from oralia.domain.agents.fallback_agent import SAFE_FALLBACK_TEXT
from oralia.domain.policies.output_template_catalog import (
    DEFAULT_OUTPUT_TEMPLATE_CATALOG,
    SAFE_TECHNICAL_FALLBACK,
    SC007_ACKNOWLEDGEMENT,
    OutputTemplateCatalog,
    OutputTemplateEntry,
    output_text_sha256,
)


@dataclass(frozen=True)
class HistoricalTemplateReference:
    template_id: str
    version: int
    sha256: str


def _entry(*, version: int, text: str, template_id: str = "synthetic-template") -> OutputTemplateEntry:
    return OutputTemplateEntry.from_text(
        template_id=template_id,
        version=version,
        message_type="normal",
        text=text,
        topic_ref="synthetic-topic",
        purpose_ref="synthetic-purpose",
        action_ref="synthetic-action",
    )


def _resolve_reference(
    catalog: OutputTemplateCatalog,
    reference: HistoricalTemplateReference,
) -> OutputTemplateEntry:
    return catalog.resolve(reference.template_id, reference.version, reference.sha256)


def test_default_catalog_resolves_normal_and_operational_entries_exactly() -> None:
    normal = DEFAULT_OUTPUT_TEMPLATE_CATALOG.resolve(*SC007_ACKNOWLEDGEMENT.identity)
    operational = DEFAULT_OUTPUT_TEMPLATE_CATALOG.resolve(*SAFE_TECHNICAL_FALLBACK.identity)

    assert normal == SC007_ACKNOWLEDGEMENT
    assert normal.message_type == "normal"
    assert normal.topic_ref == "activity"
    assert normal.purpose_ref == "acknowledge_turn"
    assert normal.action_ref == "continue"
    assert normal.sha256 == hashlib.sha256(normal.text.encode("utf-8")).hexdigest()

    assert operational == SAFE_TECHNICAL_FALLBACK
    assert operational.message_type == "operational"
    assert operational.text == SAFE_FALLBACK_TEXT
    assert operational.topic_ref == "activity"
    assert operational.purpose_ref == "technical_recovery"
    assert operational.action_ref == "clarify"
    assert operational.sha256 == hashlib.sha256(operational.text.encode("utf-8")).hexdigest()


def test_two_versions_coexist_and_resolve_only_by_complete_identity() -> None:
    version_1 = _entry(version=1, text="Synthetic version one")
    version_2 = _entry(version=2, text="Synthetic version two")
    catalog = OutputTemplateCatalog(entries=(version_1, version_2))

    resolved_1 = catalog.resolve(*version_1.identity)
    resolved_2 = catalog.resolve(*version_2.identity)

    assert resolved_1.version == 1
    assert resolved_1.text == "Synthetic version one"
    assert resolved_1.sha256 != resolved_2.sha256
    assert resolved_2.version == 2
    assert resolved_2.text == "Synthetic version two"
    with pytest.raises(KeyError):
        catalog.resolve(version_1.template_id, version_1.version, version_2.sha256)


def test_extended_returns_new_catalog_without_mutating_original() -> None:
    version_1 = _entry(version=1, text="Original text")
    version_2 = _entry(version=2, text="New text")
    original = OutputTemplateCatalog(entries=(version_1,))

    extended = original.extended((version_2,))

    assert original.resolve(*version_1.identity) == version_1
    with pytest.raises(KeyError):
        original.resolve(*version_2.identity)
    assert extended.resolve(*version_1.identity) == version_1
    assert extended.resolve(*version_2.identity) == version_2


def test_historical_configuration_and_trace_keep_resolving_original_version() -> None:
    version_1 = _entry(version=1, text="Historical text")
    version_2 = _entry(version=2, text="Replacement text")
    original = OutputTemplateCatalog(entries=(version_1,))
    configuration_reference = HistoricalTemplateReference(*version_1.identity)
    trace_reference = HistoricalTemplateReference(*version_1.identity)

    extended = original.extended((version_2,))

    for reference in (configuration_reference, trace_reference):
        resolved = _resolve_reference(extended, reference)
        assert resolved.version == 1
        assert resolved.sha256 == version_1.sha256
        assert resolved.text == "Historical text"
        assert resolved.text != version_2.text


def test_missing_or_retired_version_fails_closed_without_substitution() -> None:
    version_1 = _entry(version=1, text="Historical text")
    version_2 = _entry(version=2, text="Current text")
    version_2_only = OutputTemplateCatalog(entries=(version_2,))
    historical_reference = HistoricalTemplateReference(*version_1.identity)

    with pytest.raises(KeyError):
        _resolve_reference(version_2_only, historical_reference)
    with pytest.raises(KeyError):
        version_2_only.resolve(version_2.template_id, 99, version_2.sha256)


def test_mismatched_hash_never_resolves_an_approximate_entry() -> None:
    version_1 = _entry(version=1, text="Version one")
    version_2 = _entry(version=2, text="Version two")
    catalog = OutputTemplateCatalog(entries=(version_1, version_2))

    with pytest.raises(KeyError):
        catalog.resolve(version_1.template_id, version_1.version, "0" * 64)
    with pytest.raises(KeyError):
        catalog.resolve(version_1.template_id, version_1.version, version_2.sha256)


def test_duplicate_id_and_version_are_rejected_on_creation_and_extension() -> None:
    original = _entry(version=1, text="Original text")
    identical = _entry(version=1, text="Original text")
    conflicting = OutputTemplateEntry.from_text(
        template_id=original.template_id,
        version=original.version,
        message_type="operational",
        text="Different text",
        topic_ref="different-topic",
        purpose_ref="different-purpose",
        action_ref="different-action",
    )

    for collision in (identical, conflicting):
        with pytest.raises(ValidationError):
            OutputTemplateCatalog(entries=(original, collision))

    catalog = OutputTemplateCatalog(entries=(original,))
    for collision in (identical, conflicting):
        with pytest.raises(ValidationError):
            catalog.extended((collision,))


def test_published_entries_catalog_and_collections_are_immutable() -> None:
    version_1 = _entry(version=1, text="Published version")
    version_2 = _entry(version=2, text="Later version")
    original = OutputTemplateCatalog(entries=(version_1,))

    with pytest.raises(ValidationError):
        version_1.text = "Mutated"
    with pytest.raises(ValidationError):
        original.entries = (version_2,)
    assert isinstance(original.entries, tuple)

    extended = original.extended((version_2,))
    resolved_original = original.resolve(*version_1.identity)
    resolved_extended = extended.resolve(*version_1.identity)
    assert resolved_original.model_dump() == resolved_extended.model_dump()
    assert resolved_original.text == "Published version"


def test_unicode_forms_remain_distinct_without_silent_normalization() -> None:
    composed_text = "Café"
    decomposed_text = "Cafe\u0301"
    composed = _entry(version=1, text=composed_text, template_id="unicode-template")
    decomposed = _entry(version=2, text=decomposed_text, template_id="unicode-template")
    catalog = OutputTemplateCatalog(entries=(composed, decomposed))

    assert composed_text != decomposed_text
    assert output_text_sha256(composed_text) != output_text_sha256(decomposed_text)
    assert catalog.resolve(*composed.identity).text == composed_text
    assert catalog.resolve(*decomposed.identity).text == decomposed_text
