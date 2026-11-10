"""Ordinary PowerShell + offline local resources, only an owned scratch demo.

No Reset, personal demo restart, package installation or foreign process stopping.
Secrets are random, process-local and excluded from commands/logs/results.
"""

import hashlib
import json
import os
import queue
import secrets
import shutil
import sqlite3
import subprocess
import sys
import threading
import time
from pathlib import Path

import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tests.dialogue.api_fixture import checked, prepare_guided  # noqa: E402

WORKSPACE = ROOT / ".claude-scratch/feature010-normal-shell"
OUT = Path(__file__).resolve().parent / "operational-rehearsal"
API = "http://127.0.0.1:8026"
WEB = "http://127.0.0.1:5196"
PYTHON = ROOT / ".venv/Scripts/python.exe"
PWSH = shutil.which("pwsh.exe") or shutil.which("pwsh")
assert PWSH and PYTHON.is_file()
assert WORKSPACE.resolve().is_relative_to((ROOT / ".claude-scratch").resolve())
WORKSPACE.mkdir(parents=True, exist_ok=True)
OUT.mkdir(exist_ok=True)
assert not (OUT / "result.json").exists(), "Preserve prior operational evidence; use a new report directory."


def quoted(value):
    return "'" + str(value).replace("'", "''") + "'"


normal_path = (
    "$env:PATH=[Environment]::GetEnvironmentVariable('Path','Mach"
    "ine')+';'+[Environment]::GetEnvironmentVariable('Path','User"
    "');"
)
node_fallback = Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe"
node_setup = (
    "if (-not (Get-Command node.exe -ErrorAction SilentlyContinue)) { "
    f"if (Test-Path -LiteralPath {quoted(node_fallback)}) {{ "
    f"$env:PATH={quoted(node_fallback.parent)}+';'+$env:PATH }} }};"
)
secret = secrets.token_urlsafe(32)
guard = WORKSPACE / "offline-guard"
guard.mkdir(exist_ok=True)
(guard / "sitecustomize.py").write_text(
    """import socket
original=socket.socket.connect
original_ex=socket.socket.connect_ex
def permitted(address):
    return not isinstance(address,tuple) or address[0] in {"127.0.0.1","localhost","::1"}
def connect(sock,address):
    if not permitted(address):raise OSError("offline rehearsal: external connection denied")
    return original(sock,address)
def connect_ex(sock,address):
    if not permitted(address):return 10013
    return original_ex(sock,address)
socket.socket.connect=connect
socket.socket.connect_ex=connect_ex
""",
    encoding="utf-8",
)
env = dict(
    os.environ,
    ORALIA_DEMO_ADMIN_SECRET=secret,
    HF_HUB_OFFLINE="1",
    TRANSFORMERS_OFFLINE="1",
    PYTHONIOENCODING="utf-8",
    PYTHONPATH=str(guard) + os.pathsep + str(ROOT),
)
stable = [ROOT / "oralia.db", ROOT / ".oralia-demo/demo.db", ROOT / ".oralia-demo/fixtures.json"]
before = {
    p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in stable if p.is_file()
}
sentinel = subprocess.Popen(
    [
        str(PYTHON),
        "-u",
        "-c",
        (
            "import socket,time;s=socket.socket();s.bind(('127.0.0.1',0))"
            ";s.listen();print(s.getsockname()[1],flush=True);time.sleep("
            "600)"
        ),
    ],
    cwd=ROOT,
    stdout=subprocess.PIPE,
    text=True,
)
foreign_port = int(sentinel.stdout.readline())
active = None
records = []


def command(action):
    return [
        PWSH,
        "-NoProfile",
        "-NonInteractive",
        "-Command",
        normal_path
        + node_setup
        + f" & {quoted(PYTHON)} -X utf8 -m oralia.demo {action} --workspace {quoted(WORKSPACE)} "
        "--api-port 8026 --web-port 5196 --no-browser; exit $LASTEXITCODE",
    ]


def stop():
    result = subprocess.run(
        command("stop"), cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", timeout=30
    )
    assert secret not in result.stdout + result.stderr
    assert result.returncode == 0, result.stderr


def launch(number):
    global active
    tick = time.monotonic()
    active = subprocess.Popen(
        command("start"),
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        bufsize=1,
    )
    lines = []
    events = queue.Queue()

    def read():
        for line in active.stdout:
            lines.append(line)
            events.put(line)

    reader = threading.Thread(target=read, daemon=True)
    reader.start()
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        try:
            line = events.get(timeout=2)
        except queue.Empty:
            assert active.poll() is None, "owned launcher exited before readiness"
            continue
        if "DEMO LISTA:" in line:
            break
    else:
        raise TimeoutError("owned rehearsal did not become ready in 120s")
    elapsed = round(time.monotonic() - tick, 3)
    with httpx.Client(trust_env=False, timeout=5) as client:
        api = client.get(API + "/demo-ready")
        web = client.get(WEB + "/demo-ready.json")
        assert api.status_code == web.status_code == 200 and api.json() == web.json()
    assert sentinel.poll() is None
    return (
        {
            "run": number,
            "seconds_to_ready": elapsed,
            "readiness_both_verified": True,
            "kind": "first observed owned workspace" if number == 1 else "subsequent prepared workspace",
        },
        lines,
        reader,
    )


try:
    check_command = [
        PWSH,
        "-NoProfile",
        "-NonInteractive",
        "-Command",
        normal_path + f" & {quoted(ROOT/'scripts/demo.ps1')} -Action Check -ApiPort {foreign_port} "
        "-WebPort 5196 -TextOnly; exit $LASTEXITCODE",
    ]
    busy = subprocess.run(
        check_command, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", timeout=45
    )
    assert busy.returncode != 0 and "ocupado" in busy.stdout + busy.stderr
    assert secret not in busy.stdout + busy.stderr and sentinel.poll() is None
    (OUT / "occupied-normal-shell.log").write_text(busy.stdout + busy.stderr, encoding="utf-8")
    record, lines, reader = launch(1)
    db_path = WORKSPACE / ".oralia-demo/demo.db"
    engine = create_engine(
        "sqlite://",
        creator=lambda: sqlite3.connect(f"{db_path.as_uri()}?mode=ro", uri=True, check_same_thread=False),
    )
    with httpx.Client(base_url=API, trust_env=False, timeout=30) as client:
        checked(client.post("/api/v1/auth/login", json={"secret": secret}))
        client.__db_sessionmaker__ = sessionmaker(bind=engine)
        for mode in ["self_study", "oral_defense"]:
            fixture = prepare_guided(client, mode=mode)
            sid = fixture["session"]["session_id"]
            route = (
                f"/api/v1/sessions/{sid}/study-turns"
                if mode == "self_study"
                else f"/api/v1/defense-sessions/{sid}/defense-turns"
            )
            texts = (
                ["¿A qué temperatura hierve el agua?", "dimelo", "dame un ejemplo"]
                if mode == "self_study"
                else ["", "no sé justificarlo", "puedes repetir?"]
            )
            for text in texts:
                response = checked(client.post(route, json={"text": text}))
                assert response["output_text"] and response["dialogue_status"]["rendered_unit_ids"]
            end = (
                f"/api/v1/sessions/{sid}/study-end"
                if mode == "self_study"
                else f"/api/v1/defense-sessions/{sid}/defense-end"
            )
            choice = {"retain": True, "scope": ["transcript", "summary"]}
            checked(client.post(end, json=choice))
            checked(client.get(f"/api/v1/governance/sessions/{sid}"))
            exported = client.post(
                "/api/v1/governance/exports", json={"session_ids": [sid], "format": "json"}
            )
            assert exported.status_code == 200 and secret not in exported.text
            checked(client.request("DELETE", f"/api/v1/sessions/{sid}/content", json={"confirm": True}))
            assert client.get(f"/api/v1/governance/sessions/{sid}").status_code == 404
    engine.dispose()
    stop()
    assert active.wait(timeout=20) == 0
    reader.join(timeout=5)
    assert secret not in "".join(lines)
    (OUT / "first-start.log").write_text("".join(lines), encoding="utf-8")
    records.append(record)
    record, lines, reader = launch(2)
    stop()
    assert active.wait(timeout=20) == 0
    reader.join(timeout=5)
    assert secret not in "".join(lines)
    (OUT / "subsequent-start.log").write_text("".join(lines), encoding="utf-8")
    records.append(record)
    after = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in before}
    assert before == after, "personal stable resources changed; investigate without restoring fabricated data"
    assert sentinel.poll() is None
    result = {
        "passed": True,
        "runs": records,
        "workspace": str(WORKSPACE),
        "normal_shell_path_reconstructed": True,
        "external_socket_connections_blocked_in_owned_python_processes": True,
        "physical_disconnect_claimed": False,
        "foreign_sentinel_survived": True,
        "personal_resources_unchanged": before,
        "personal_demo_restarted": False,
        "reset_performed": False,
        "credential_found": False,
        "owned_demo_left": "prepared; stopped",
        "limitation": "synthetic API dialogue/review/export/delete; no human or real voice validation",
    }
    (OUT / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result), flush=True)
finally:
    if active is not None and active.poll() is None:
        stop()
        active.wait(timeout=20)
    if sentinel.poll() is None:
        sentinel.terminate()
    sentinel.wait(timeout=10)
