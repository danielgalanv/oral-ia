"""Verify immutable archived packages after an explicit live transport revision."""

import hashlib
import json
from pathlib import Path

from oralia.course_dialogue.corpus import SOURCE_ROOT

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
OUTPUT = EVIDENCE / "scope-control-profile-preservation-v1.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if OUTPUT.exists():
        raise ValueError("preserve preservation receipt")
    results = []
    for name in (
        "scope-classifier-frozen-v1",
        "scope-resource-revision-v2-final",
        "scope-v2-described-proposal-v1-final",
        "scope-finite-capacity-v1",
    ):
        package = EVIDENCE / name
        manifest = json.loads((package / "manifest.json").read_text(encoding="utf-8"))
        archived = []
        for path, expected in manifest.items():
            live = ROOT / path
            if live.is_file() and digest(live) == expected:
                continue
            copies = [package / "artifacts" / path, package / "code" / path]
            if not any(copy.is_file() and digest(copy) == expected for copy in copies):
                raise ValueError("archived evidence mismatch: " + path)
            archived.append(path)
        results.append(
            {
                "package": name,
                "entries_verified": len(manifest),
                "intentional_live_revision_original_kept_in_archive": archived,
            }
        )
    audit = json.loads((EVIDENCE / "scope-effective-request-audit-v1.json").read_text(encoding="utf-8"))
    old_adapter = (
        EVIDENCE / "scope-finite-capacity-v1/artifacts/src/oralia/course_dialogue/cached_transformers.py"
    )
    assert digest(old_adapter) == audit["frozen_adapter_sha256"]
    policy = json.loads((EVIDENCE / "course-scope-policy-v1.json").read_text(encoding="utf-8"))
    for source in [
        policy["source_scope"]["presentation"],
        *policy["source_scope"]["authorized_lab_documents"],
    ]:
        assert digest(SOURCE_ROOT / source["file"]) == source["sha256"]
    budgets = {
        name: json.loads((EVIDENCE / name).read_text(encoding="utf-8"))["used"]
        for name in (
            "scope-classifier-call-budget.json",
            "scope-v2-described-budget.json",
            "scope-finite-capacity-budget.json",
        )
    }
    assert list(budgets.values()) == [2, 1, 1]
    OUTPUT.write_text(
        json.dumps(
            {
                "packages": results,
                "historical_reconstruction_still_original": True,
                "teacher_sources_unchanged": 4,
                "budgets": budgets,
                "new_model_inferences": 0,
                "historical_3279_hash_audit_claimed": False,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("Archived packages and four teacher sources intact; budgets remain 2/1/1.")


if __name__ == "__main__":
    main()
