"""CPU-only evidence capture; never loads an encoder, generator or listener."""

import argparse
import hashlib
import json
import subprocess
import uuid
from datetime import UTC, datetime
from pathlib import Path

from pydantic import ValidationError

from oralia.course_dialogue.cached_transformers import CACHED_MODEL_14B, CUDA_PYTHON
from oralia.course_dialogue.lab_request import LabGenerationConstraints

ROOT = Path(__file__).resolve().parents[1]


def write_new(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def budget_receipt():
    requested = {"deadline_ms": 60000, "max_tokens": 768}
    try:
        LabGenerationConstraints(**requested)
    except ValidationError as error:
        return {"requested": requested, "status": "rejected", "errors": error.errors()}
    return {"requested": requested, "status": "accepted"}


def capture(output):
    # Both directory creation and every receipt refuse accidental overwrite.
    output.mkdir(parents=True, exist_ok=False)
    budget = budget_receipt()
    write_new(output / "budget.json", budget)
    files = []
    for path in sorted(CACHED_MODEL_14B.iterdir()):
        if path.is_file():
            row = {"name": path.name, "bytes": path.stat().st_size}
            if path.suffix == ".json" or path.name == "merges.txt":
                row["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            files.append(row)
    index = json.loads((CACHED_MODEL_14B / "model.safetensors.index.json").read_text())
    shards = sorted(set(index["weight_map"].values()))
    write_new(
        output / "local-files.json",
        {
            "snapshot": str(CACHED_MODEL_14B),
            "runtime_path": str(CUDA_PYTHON),
            "runtime_file_exists": CUDA_PYTHON.is_file(),
            "required_shards": shards,
            "all_shards_present": all((CACHED_MODEL_14B / name).is_file() for name in shards),
            "files": files,
            "weights_hashed": False,
            "runtime_loaded": False,
            "effective_runtime_identity": "not_observed",
            "quantization_requested": "nf4",
        },
    )
    gpu = subprocess.run(["nvidia-smi"], capture_output=True, text=True, timeout=15, check=False)
    write_new(
        output / "gpu.json",
        {
            "observed_at_utc": datetime.now(UTC).isoformat(),
            "returncode": gpu.returncode,
            "stdout": gpu.stdout,
            "stderr": gpu.stderr,
            "attribution": "unknown; no foreign processes inspected or stopped",
        },
    )
    write_new(
        output / "status.json",
        {
            "kind": "preflight_only",
            "academic_requests": 0,
            "warmups": 0,
            "worker_started": False,
            "encoder_loaded": False,
            "budget_status": budget["status"],
            "inference_allowed_by_this_helper": False,
            "participant_publication_allowed": False,
            "semantic_support": "unverified",
            "sufficiency": "not_assessed",
        },
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "docs/audits/2026-10-27-first-generated-study" / ("preflight-" + uuid.uuid4().hex),
    )
    args = parser.parse_args()
    capture(args.output)
    print(args.output)
