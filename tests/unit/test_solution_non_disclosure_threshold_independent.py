"""Unit test: el umbral/configuración de SolutionNonDisclosureVerifierAgent es
independiente del de GroundingVerifierAgent (valores y variables de entorno distintos,
research.md §4)."""

from __future__ import annotations

import pytest

from oralia.domain.agents import grounding_verifier_agent
from oralia.infrastructure.generation import config


def test_default_threshold_values_are_distinct():
    assert grounding_verifier_agent._SUPPORT_OVERLAP_THRESHOLD == 0.4
    assert config.get_disclosure_overlap_threshold() == pytest.approx(0.3)
    assert grounding_verifier_agent._SUPPORT_OVERLAP_THRESHOLD != config.get_disclosure_overlap_threshold()


def test_env_var_names_are_distinct_and_independently_configurable(monkeypatch: pytest.MonkeyPatch):
    # GroundingVerifierAgent's threshold is fixed in code (Feature 002 does not expose
    # it via env var, research.md §4) — only SolutionNonDisclosureVerifierAgent's is.
    monkeypatch.setenv("ORALIA_DISCLOSURE_OVERLAP_THRESHOLD", "0.75")
    assert config.get_disclosure_overlap_threshold() == pytest.approx(0.75)
    assert grounding_verifier_agent._SUPPORT_OVERLAP_THRESHOLD == 0.4, (
        "changing ORALIA_DISCLOSURE_OVERLAP_THRESHOLD MUST NOT affect GroundingVerifierAgent"
    )


def test_tokenization_functions_are_separate_implementations():
    from oralia.domain.agents import solution_non_disclosure_verifier_agent as nd_module

    assert nd_module._significant_words is not grounding_verifier_agent._significant_words
