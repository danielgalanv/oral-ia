import os
import subprocess
import sys

import psutil
import pytest

from oralia.demo.launcher import reset, stop
from oralia.demo.resources import DemoError, DemoPaths, write_json


def test_reset_confirms_exact_scope_and_keeps_habitual_sentinel(tmp_path):
    sentinel = tmp_path / "oralia.db"
    sentinel.write_bytes(b"habitual unchanged")
    paths = DemoPaths(tmp_path)
    paths.initialize()
    (paths.root / "demo.db").write_bytes(b"only demo")
    with pytest.raises(DemoError, match="cancelado"):
        reset(paths, confirmation="no")
    assert (paths.root / "demo.db").exists()
    reset(paths, confirmation="BORRAR DEMO")
    assert not paths.root.exists()
    assert sentinel.read_bytes() == b"habitual unchanged"


def test_stop_rejects_tampered_receipt_and_does_not_terminate_foreign_process(tmp_path):
    foreign = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    try:
        paths = DemoPaths(tmp_path)
        paths.initialize()
        write_json(
            paths.root / "run.json",
            {
                "pid": foreign.pid,
                "created": psutil.Process(foreign.pid).create_time(),
                "workspace": str(paths.workspace),
                "run_id": "forged",
            },
        )
        with pytest.raises(DemoError, match="no corresponde"):
            stop(paths, timeout=0.1)
        assert foreign.poll() is None
        assert not (paths.root / "stop.json").exists()
    finally:
        foreign.terminate()
        foreign.wait(timeout=10)


def test_nested_junction_prevents_reset_without_touching_target(tmp_path):
    paths = DemoPaths(tmp_path)
    paths.initialize()
    target = tmp_path / "habitual"
    target.mkdir()
    (target / "keep").write_text("kept")
    link = paths.root / "nested"
    command = f'New-Item -ItemType Junction -Path "{link}" -Target "{target}" | Out-Null'
    result = subprocess.run(["pwsh", "-NoProfile", "-Command", command], capture_output=True)
    assert result.returncode == 0
    try:
        with pytest.raises(DemoError, match="enlace|reparse"):
            reset(paths, confirmation="BORRAR DEMO")
        assert (target / "keep").read_text() == "kept"
    finally:
        os.rmdir(link)  # Remove link itself, never recurse into its target.
