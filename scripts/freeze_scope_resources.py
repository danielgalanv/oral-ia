"""Freeze resource-only revision; preserve original semantic artifacts and budget."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
OUTPUT = EVIDENCE / "scope-resource-revision-v2-final"


def main():
    OUTPUT.mkdir(exist_ok=False)
    original = EVIDENCE / "scope-classifier-frozen-v1/manifest.json"
    files = [
        ROOT / name
        for name in [
            "scripts/trial_course_scope.py",
            "scripts/freeze_scope_resources.py",
            "src/oralia/course_dialogue/gpu_resource_policy.py",
            "tests/course_dialogue/test_gpu_resource_policy.py",
        ]
    ]
    files.append(original)
    for path in list(files):
        copy = OUTPUT / "code" / path.relative_to(ROOT)
        copy.parent.mkdir(parents=True, exist_ok=True)
        copy.write_bytes(path.read_bytes())
        files.append(copy)
    (OUTPUT / "manifest.json").write_text(
        json.dumps(
            {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUTPUT / "policy.json").write_text(
        json.dumps(
            {
                "revision": "resources_only_no_prompt_bank_or_oracle_change",
                "preflight": (
                    "five_samples_two_seconds_apart_utilization_le_5_free_mib_ge_10000_used_range_le_256"
                ),
                "foreign_resident_context_does_not_imply_active_load": True,
                "during": (
                    "two_second_telemetry_and_per_case_samples_memory_headroom_2048_mib_above_own_footprint"
                ),
                "resident_or_unknown_period_latency": "resource-inconclusive",
                "unattributed_pressure": "stop_own_worker_no_blame_to_named_process",
                "total_call_limit_unchanged": 20,
                "calls_consumed_before_revision": 0,
                "exclusive_gpu_claimed": False,
                "publication_allowed": False,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("Resource revision frozen; original semantic artifacts unchanged.")


if __name__ == "__main__":
    main()
