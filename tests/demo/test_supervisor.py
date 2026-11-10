import os
import secrets
import socket
import subprocess
import sys
import time

import psutil
import pytest

from oralia.demo.launcher import _json_at, start, stop
from oralia.demo.resources import SOURCE_ROOT, DemoError, DemoPaths, check_ports


def free_ports():
    with socket.socket() as first, socket.socket() as second:
        first.bind(("127.0.0.1", 0))
        second.bind(("127.0.0.1", 0))
        return first.getsockname()[1], second.getsockname()[1]


def test_real_supervisor_starts_stops_only_owned_processes_and_keeps_environment(tmp_path):
    paths = DemoPaths(tmp_path)
    sentinel = tmp_path / "oralia.db"
    sentinel.write_bytes(b"habitual fixture remains unchanged")
    foreign = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(90)"])
    secret = secrets.token_urlsafe(32)
    api, web = free_ports()
    env = dict(os.environ, ORALIA_DEMO_ADMIN_SECRET=secret, ORALIA_DB_URL="sqlite:///habitual.db")
    with (tmp_path / "supervisor.log").open("w", encoding="utf-8") as log:
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "oralia.demo",
                "start",
                "--workspace",
                str(tmp_path),
                "--api-port",
                str(api),
                "--web-port",
                str(web),
                "--text-only",
                "--no-browser",
            ],
            cwd=SOURCE_ROOT,
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT,
        )
        try:
            deadline = time.monotonic() + 45
            while _json_at(f"http://127.0.0.1:{web}/demo-ready.json") is None:
                assert process.poll() is None, (tmp_path / "supervisor.log").read_text(encoding="utf-8")
                assert time.monotonic() < deadline
                time.sleep(0.15)
            # Frontend environment and command lines contain no secret.
            for child in psutil.Process(process.pid).children(recursive=True):
                assert secret not in " ".join(child.cmdline())
                if any("vite.js" in part for part in child.cmdline()):
                    assert "ORALIA_ADMIN_SECRET" not in child.environ()
            with pytest.raises(DemoError, match="activa|curso"):
                from oralia.demo.launcher import reset

                reset(paths, confirmation="BORRAR DEMO")
            stop(paths)
            assert process.wait(timeout=20) == 0
            check_ports(api, web)
            assert foreign.poll() is None
            assert sentinel.read_bytes() == b"habitual fixture remains unchanged"
            assert "ORALIA_DB_URL" not in (tmp_path / "supervisor.log").read_text(encoding="utf-8")
            for file in paths.root.rglob("*.log"):
                assert secret not in file.read_text(encoding="utf-8")
        finally:
            if process.poll() is None:
                stop(paths)
                process.wait(timeout=20)
            foreign.terminate()
            foreign.wait(timeout=10)


def test_partial_start_timeout_cleans_children_and_releases_ports(tmp_path):
    api, web = free_ports()
    paths = DemoPaths(tmp_path)
    with pytest.raises(DemoError, match="Timeout"):
        start(
            paths,
            secret=secrets.token_urlsafe(32),
            api_port=api,
            web_port=web,
            text_only=True,
            no_browser=True,
            readiness_timeout=0,
        )
    check_ports(api, web)
    assert not (paths.root / "run.json").exists()


def test_preparation_timeout_cleans_only_its_child(tmp_path):
    api, web = free_ports()
    paths = DemoPaths(tmp_path)
    with pytest.raises(DemoError, match="Preparación interrumpida"):
        start(
            paths,
            secret=secrets.token_urlsafe(32),
            api_port=api,
            web_port=web,
            text_only=True,
            no_browser=True,
            preparation_timeout=0,
        )
    check_ports(api, web)
    assert not (paths.root / "run.json").exists()
