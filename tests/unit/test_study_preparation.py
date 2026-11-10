"""Reusable preparation rejects changed inputs/artifacts without starting any model."""

import json

import pytest

from oralia.documentary import study_preparation as preparation


def setup(monkeypatch, tmp_path):
    monkeypatch.setattr(preparation, "ROOT", tmp_path)
    inputs = {"sources": {"fixture": "original"}}
    monkeypatch.setattr(preparation, "current_inputs", lambda: inputs.copy())
    monkeypatch.setattr(preparation, "prepare_teacher_concepts", lambda root: None)
    root = tmp_path / ".claude-scratch/study-chat-fixture"
    for name in (
        "web-dist/index.html",
        "retrieval-index/identity.json",
        "retrieval-index/fragments.json",
        "retrieval-index/chroma/index_version.json",
        "concept-catalogue/manifest.json",
    ):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture", encoding="utf8")
    preparation.prepare_receipt(root)
    return root, inputs


def test_reuse_is_read_only_and_rejects_source_changes(monkeypatch, tmp_path):
    root, inputs = setup(monkeypatch, tmp_path)
    before = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}
    assert preparation.validate_preparation(root) == root
    assert before == {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}
    inputs["sources"] = {"fixture": "changed"}
    with pytest.raises(ValueError, match="Sources"):
        preparation.validate_preparation(root)
    with pytest.raises(FileExistsError):
        preparation.prepare_receipt(root)


@pytest.mark.parametrize("change", ["modified", "deleted", "extra", "schema"])
def test_reuse_rejects_changed_build_index_or_receipt(monkeypatch, tmp_path, change):
    root, _ = setup(monkeypatch, tmp_path)
    if change == "modified":
        (root / "retrieval-index/fragments.json").write_text("changed", encoding="utf8")
    elif change == "deleted":
        (root / "web-dist/index.html").unlink()
    elif change == "extra":
        (root / "web-dist/injected.js").write_text("unexpected", encoding="utf8")
    else:
        (root / preparation.RECEIPT).write_text(json.dumps({"schema": "foreign"}), encoding="utf8")
    with pytest.raises(ValueError):
        preparation.validate_preparation(root)


def test_unknown_roots_are_not_adopted(monkeypatch, tmp_path):
    monkeypatch.setattr(preparation, "ROOT", tmp_path)
    with pytest.raises(ValueError, match="owned"):
        preparation.prepare_receipt(tmp_path / "demo")


def test_working_copy_keeps_template_reusable_after_runtime_writes(monkeypatch, tmp_path):
    root, _ = setup(monkeypatch, tmp_path)
    destination = root / "launches/fixture/retrieval-index"
    assert preparation.materialize_index(root, destination) == destination
    (destination / "fragments.json").write_text("runtime changes", encoding="utf8")
    assert preparation.validate_preparation(root) == root
    with pytest.raises(FileExistsError):
        preparation.materialize_index(root, destination)
    with pytest.raises(ValueError, match="owned"):
        preparation.materialize_index(root, tmp_path / "foreign")
