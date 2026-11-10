"""Bounded transient telemetry handling, independent of academic outputs."""

from scripts.run_pedagogical_comparison import ResourceGuard


def test_single_miss_does_not_kill_safe_worker_but_two_consecutive_misses_stop():
    guard = ResourceGuard(tolerated_misses=1)
    assert guard.stop_required(None) is False
    assert guard.stop_required("0, 7600, 24000") is False
    assert guard.stop_required(None) is False
    assert guard.stop_required(None) is True


def test_critical_memory_and_original_strict_behavior_remain():
    guard = ResourceGuard(tolerated_misses=1)
    assert guard.stop_required("80, 31000, 1000") is False
    assert guard.stop_required("80, 31000, 1000") is True
    assert ResourceGuard(tolerated_misses=0).stop_required(None) is True
