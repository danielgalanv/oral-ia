"""FR-017: basic CPU/memory monitor smoke test."""

from oralia.infrastructure.telemetry.resources import as_dict, snapshot


def test_snapshot_returns_plausible_values():
    s = snapshot()
    assert s.memory_rss_mb > 0
    assert s.cpu_percent >= 0
    assert s.timestamp > 0


def test_as_dict_has_expected_keys():
    d = as_dict()
    assert set(d.keys()) == {"cpu_percent", "memory_rss_mb"}
    assert isinstance(d["memory_rss_mb"], float)
