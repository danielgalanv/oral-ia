import pytest
from pydantic import ValidationError

from oralia.validation.protocol import SCENARIOS, Protocol


def test_catalog_and_protocol_are_closed_synthetic_and_bounded():
    assert len(SCENARIOS) == 17
    assert len({s.id for s in SCENARIOS}) == 17
    for change in [
        {"synthetic_only": False},
        {"repetitions": 0},
        {"repetitions": 6},
        {"conditions": ["no_grounding"]},
        {"conditions": ["unknown"]},
        {"conditions": ["full", "full"]},
        {"database": "real.db"},
    ]:
        with pytest.raises((ValidationError, ValueError)):
            Protocol(**change)


def test_ablation_requires_explicit_authorization():
    assert Protocol(ablations_authorized=True, conditions=["no_grounding"]).synthetic_only
