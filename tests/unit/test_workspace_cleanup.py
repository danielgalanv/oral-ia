import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "workspace_cleanup", Path(__file__).resolve().parents[2] / "scripts/clean_workspace.py"
)
cleanup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cleanup)


def test_preview_and_apply_preserve_sources_data_and_historical_caches(tmp_path):
    cache = tmp_path / "src/oralia/__pycache__/sample.pyc"
    cache.parent.mkdir(parents=True)
    cache.write_bytes(b"generated")
    protected = [
        "oralia.db",
        "src/oralia/source.py",
        "docs/audits/__pycache__/evidence.pyc",
        ".claude-scratch/receipt.json",
        ".venv/keep.pyc",
        "materiales/original.pdf",
    ]
    for name in protected:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"preserve")
    preview = cleanup.clean(tmp_path)
    assert preview["candidates"] and cache.exists()
    result = cleanup.clean(tmp_path, apply=True)
    assert not result["errors"] and not cache.exists()
    assert all((tmp_path / name).read_bytes() == b"preserve" for name in protected)


def test_cache_link_is_not_followed_or_deleted(tmp_path):
    outside = tmp_path / "protected"
    outside.mkdir()
    (outside / "sentinel").write_text("keep")
    try:
        (tmp_path / ".pytest_cache").symlink_to(outside, target_is_directory=True)
    except OSError:
        if os.name != "nt":
            pytest.skip("symlink privilege unavailable")
        # A directory junction needs no symbolic-link privilege on Windows.
        subprocess.run(
            ["cmd.exe", "/c", "mklink", "/J", str(tmp_path / ".pytest_cache"), str(outside)],
            check=True,
            capture_output=True,
        )
    assert not cleanup.clean(tmp_path, apply=True)["removed"]
    assert (outside / "sentinel").read_text() == "keep"


def test_report_cannot_overwrite_existing_material_before_cleaning(tmp_path, monkeypatch):
    cache = tmp_path / ".pytest_cache"
    cache.mkdir()
    protected = tmp_path / "manifest.json"
    protected.write_text("preserve")
    monkeypatch.setattr(cleanup, "__file__", str(tmp_path / "scripts/clean_workspace.py"))
    monkeypatch.setattr(sys, "argv", ["clean_workspace.py", "--apply", "--output", str(protected)])
    with pytest.raises(ValueError, match="new JSON"):
        cleanup.main()
    assert protected.read_text() == "preserve" and cache.exists()
