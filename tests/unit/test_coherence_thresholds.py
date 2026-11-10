"""Unit test: las ventanas de ausencia-de-progreso/repetición son configurables por
variable de entorno, por defecto 3/1."""

from __future__ import annotations

import pytest

from oralia.infrastructure.generation import config


def test_default_thresholds_are_3_and_1():
    assert config.get_coherence_no_progress_window() == 3
    assert config.get_coherence_repetition_window() == 1


def test_thresholds_are_configurable_via_env_vars(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("ORALIA_COHERENCE_NO_PROGRESS_WINDOW", "5")
    monkeypatch.setenv("ORALIA_COHERENCE_REPETITION_WINDOW", "2")
    assert config.get_coherence_no_progress_window() == 5
    assert config.get_coherence_repetition_window() == 2
