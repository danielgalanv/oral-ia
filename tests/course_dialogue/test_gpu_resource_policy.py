"""Resource policy distinguishes residence, observed load and uncertainty."""

import pytest

from oralia.course_dialogue.gpu_resource_policy import preflight, resource_period


def samples(gpu="1, 624, 31564"):
    return [{"gpu": gpu, "apps": "91212, N/A"} for _ in range(5)]


def test_idle_resident_process_does_not_block():
    result = preflight(samples())
    assert result["ready"] and not result["exclusive_gpu_claimed"]


@pytest.mark.parametrize("gpu", ["60, 624, 31564", "1, 28000, 4000"])
def test_observed_load_or_low_memory_blocks(gpu):
    assert not preflight(samples(gpu))["ready"]


def test_insufficient_or_unstable_samples_do_not_start():
    assert not preflight(samples()[:1])["ready"]
    changed = samples()
    changed[-1] = {"gpu": "1, 1024, 31164"}
    assert not preflight(changed)["ready"]


def test_unknown_or_resident_period_does_not_blame_model_deadline():
    assert resource_period(samples(), 624, 6000, True) == "resource-inconclusive"
    assert resource_period([{"error": "telemetry"}], 624, 6000) == "resource-inconclusive"
    assert resource_period(samples("100, 14000, 18000"), 624, 6000) == "resource-pressure-observed"
    assert resource_period(samples("100, 7000, 25000"), 624, 6000) == "no_competition_observed"
