"""Freeze prepared CPU evidence and future test inputs; never starts inference."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
PACKAGE = EVIDENCE / "minimal-capacity-probe-v1"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    output = PACKAGE / "manifest.json"
    if output.exists():
        raise ValueError("preserve frozen proposal")
    files = [
        ROOT / name
        for name in (
            "scripts/audit_local_scope_resource.py",
            "scripts/reconstruct_scope_cpu_traces.py",
            "scripts/check_scope_cpu_trace_tokenizers.py",
            "scripts/prepare_minimal_capacity_probe.py",
            "scripts/check_minimal_probe_cpu.py",
            "scripts/freeze_minimal_cpu_probe.py",
            "tests/course_dialogue/test_minimal_capacity_probe.py",
            "tests/course_dialogue/test_generation_observability.py",
            "src/oralia/course_dialogue/generation_observability.py",
            "src/oralia/course_dialogue/gpu_worker.py",
            "src/oralia/course_dialogue/finite_schema.py",
            "src/oralia/course_dialogue/scope_message_profiles.py",
        )
    ]
    files += [
        PACKAGE / name
        for name in (
            "frames.json",
            "oracle.json",
            "protocol.json",
            "source.json",
            "execution-budget.json",
            "cpu-tokenizer-check.json",
        )
    ]
    files += [
        EVIDENCE / name
        for name in (
            "cpu-local-scope-resource-audit-v1.json",
            "cpu-effective-scope-traces-v1.json",
            "cpu-scope-trace-tokenizer-audit-v1.json",
        )
    ]
    for path in list(files):
        copy = PACKAGE / "artifacts" / path.relative_to(ROOT)
        copy.parent.mkdir(parents=True, exist_ok=True)
        copy.write_bytes(path.read_bytes())
        files.append(copy)
    resource = json.loads((EVIDENCE / "cpu-local-scope-resource-audit-v1.json").read_text(encoding="utf-8"))
    source = Path(resource["source"])
    metadata = [
        "config.json",
        "generation_config.json",
        "model.safetensors.index.json",
        "tokenizer_config.json",
        "tokenizer.json",
        "vocab.json",
        "merges.txt",
    ]
    result = {
        "workspace_files": {path.relative_to(ROOT).as_posix(): digest(path) for path in files},
        "external_metadata": {str(source / name): digest(source / name) for name in metadata},
        "weight_headers_only": resource["shards"],
        "weight_values_or_upstream_hash_authenticated": False,
        "state": "GPU_not_authorized_pending_user_availability_confirmation",
    }
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("Minimal proposal and CPU evidence frozen. GPU not started.")


if __name__ == "__main__":
    main()
