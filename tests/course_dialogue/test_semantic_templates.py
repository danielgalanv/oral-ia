"""Candidate templates require explicit policy/catalog; defaults stay unchanged."""

import pytest

from oralia.domain.dialogue.catalog import guided_policy
from oralia.domain.dialogue.semantic_templates import (
    SEMANTIC_GREETED_3,
    SEMANTIC_RECEIPT,
    SEMANTIC_TEMPLATE_CATALOG,
    semantic_guided_policy,
)
from oralia.domain.policies.output_template_catalog import DEFAULT_OUTPUT_TEMPLATE_CATALOG


def test_candidate_templates_do_not_enter_the_ordinary_default_catalog():
    for entry in [SEMANTIC_GREETED_3, SEMANTIC_RECEIPT]:
        with pytest.raises(KeyError):
            DEFAULT_OUTPUT_TEMPLATE_CATALOG.resolve(*entry.identity)
        assert SEMANTIC_TEMPLATE_CATALOG.resolve(*entry.identity) == entry


def test_candidate_policy_does_not_expand_recipients_or_data_provenance():
    base = guided_policy("fiction", screenless=True, pedagogy=True, advanced=True, continuity=True)
    policy = semantic_guided_policy("fiction")
    assert policy.allowed_recipients == base.allowed_recipients
    assert policy.allowed_disclosures == base.allowed_disclosures
    assert policy.allowed_scopes == base.allowed_scopes
    assert policy.general_knowledge_allowed is False
    assert len(policy.allowed_templates) == len(base.allowed_templates) + 3
