"""Observed resources, not process residency, determine laboratory readiness."""


def gpu_values(sample):
    return tuple(float(value.strip()) for value in sample["gpu"].splitlines()[0].split(","))


def preflight(samples, required_free_mib=10000):
    if len(samples) < 5:
        return {"ready": False, "reason": "insufficient_samples"}
    values = [gpu_values(sample) for sample in samples]
    low_use = all(util <= 5 for util, _, _ in values)
    sufficient = all(free >= required_free_mib for _, _, free in values)
    stable = max(used for _, used, _ in values) - min(used for _, used, _ in values) <= 256
    return {
        "ready": low_use and sufficient and stable,
        "reason": "observed_low_load" if low_use and sufficient and stable else "busy_or_insufficient",
        "exclusive_gpu_claimed": False,
        "resident_context_is_not_active_load": True,
    }


def resource_period(samples, baseline_used_mib, owned_footprint_mib, resident_foreign=False):
    if not samples or any("error" in sample for sample in samples):
        return "resource-inconclusive"
    # This bound allows own KV cache and allocator headroom. It indicates
    # unattributed pressure, not proof that any named process caused it.
    ceiling = baseline_used_mib + owned_footprint_mib + 2048
    if any(gpu_values(sample)[1] > ceiling for sample in samples):
        return "resource-pressure-observed"
    if resident_foreign:
        return "resource-inconclusive"
    return "no_competition_observed"
