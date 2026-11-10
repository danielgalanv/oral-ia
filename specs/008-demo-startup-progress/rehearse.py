"""Repeatable prepared-demo rehearsal: no reset, no credential literals or foreign kills."""

import hashlib
import json
import os
import queue
import secrets
import subprocess
import sys
import threading
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
DEMO = ROOT / ".oralia-demo"
assert (DEMO / "fixtures.json").is_file(), "Prepared demo required; do not reset"
BASE = json.loads((OUT / "baseline.json").read_text(encoding="utf-8"))
secret = secrets.token_urlsafe(32)
env = dict(os.environ, ORALIA_DEMO_ADMIN_SECRET=secret, PYTHONIOENCODING="utf-8")
command = ["pwsh", "-NoProfile", "-File", str(ROOT / "scripts/demo.ps1")]
foreign = subprocess.Popen(
    [
        sys.executable,
        "-u",
        "-c",
        "import socket,time; s=socket.socket(); s.bind(('127.0.0.1',0)); s.listen(); "
        "print(s.getsockname()[1],flush=True); time.sleep(300)",
    ],
    stdout=subprocess.PIPE,
    text=True,
)
foreign_port = int(foreign.stdout.readline())
active = None
records = []


def invoke(*args):
    result = subprocess.run(
        [*command, *args], cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", timeout=60
    )
    assert secret not in result.stdout + result.stderr
    return result


def launch():
    global active
    number = len(records)
    started = time.monotonic()
    active = subprocess.Popen(
        [*command, "-NoBrowser"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        bufsize=1,
    )
    events = queue.Queue()
    output = []
    timed = []

    def read():
        for line in active.stdout:
            output.append(line)
            timed.append({"seconds": round(time.monotonic() - started, 3), "message": line.strip()})
            events.put(line)

    reader = threading.Thread(target=read)
    reader.start()
    try:
        deadline = time.monotonic() + 100
        while True:
            assert time.monotonic() < deadline, "readiness timeout"
            line = events.get(timeout=10)
            if "DEMO LISTA:" in line:
                break
            assert active.poll() is None, "launcher exited early"
        startup_seconds = round(time.monotonic() - started, 3)
        with httpx.Client(trust_env=False, timeout=2) as client:
            api = client.get("http://127.0.0.1:8010/demo-ready")
            web = client.get("http://127.0.0.1:5180/demo-ready.json")
            assert api.status_code == web.status_code == 200 and api.json() == web.json()
            assert client.get("http://127.0.0.1:5180/api/v1/governance/activities").status_code == 401
        assert foreign.poll() is None
        stopped = invoke("-Action", "Stop")
        assert stopped.returncode == 0
        assert active.wait(timeout=20) == 0
        reader.join(timeout=5)
        text = "".join(output)
        assert secret not in text
        labels = [
            "dependencias y puertos",
            "embeddings locales",
            "Preparación de datos e índice demo",
            "Inicio de API",
            "Inicio de interfaz",
            "Espera de disponibilidad",
        ]
        positions = [text.index(label) for label in labels]
        assert positions == sorted(positions)
        assert text.count("[INICIO] Comprobación de dependencias") == 1
        assert text.count("[INICIO] Comprobación o carga de embeddings") == 1
        assert "[ESPERA]" in text
        assert "Ctrl+C" in text and "-Action Stop" in text
        (OUT / f"rehearsal-start-{number}.log").write_text(text, encoding="utf-8")
        (OUT / f"rehearsal-start-{number}-events.json").write_text(
            json.dumps(timed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        records.append(
            {
                "run": number + 1,
                "kind": "first observed prepared" if number == 0 else "subsequent prepared",
                "startup_to_ready_seconds": startup_seconds,
                "cycle_seconds": round(time.monotonic() - started, 3),
                "readiness_both_verified": True,
                "preflight_once": True,
                "foreign_alive": True,
            }
        )
    finally:
        if active.poll() is None:
            invoke("-Action", "Stop")
            active.wait(timeout=20)
        reader.join(timeout=5)
        active = None


try:
    busy = invoke("-Action", "Check", "-ApiPort", str(foreign_port), "-TextOnly")
    assert busy.returncode != 0 and "[FALLO] Comprobación de dependencias" in busy.stderr + busy.stdout
    assert "ocupado" in busy.stderr + busy.stdout and foreign.poll() is None
    (OUT / "rehearsal-busy.log").write_text(busy.stdout + busy.stderr, encoding="utf-8")
    check = invoke("-Action", "Check")
    assert check.returncode == 0
    assert json.loads(check.stdout)["profile"] == "full: embeddings locales"
    (OUT / "rehearsal-check.log").write_text(check.stderr + check.stdout, encoding="utf-8")
    launch()
    launch()
    after = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in BASE["stable_resources"]
    }
    assert after == BASE["stable_resources"], "Prepared or habitual stable data changed"
    for path in DEMO.rglob("*.log"):
        assert secret not in path.read_text(encoding="utf-8")
    report = {
        "passed": True,
        "command": ".\\scripts\\demo.ps1 -NoBrowser",
        "runs": records,
        "busy_rejected": True,
        "check_json_preserved": True,
        "credential_found": False,
        "stable_files_unchanged": len(after),
        "foreign_survived": foreign.poll() is None,
        "reset_performed": False,
        "demo_left": "prepared full; stopped",
        "timing_limit": "first observed prepared, not cold cache; no causal performance improvement claim",
    }
    (OUT / "validation-demo.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report), flush=True)
finally:
    if active is not None and active.poll() is None:
        invoke("-Action", "Stop")
        active.wait(timeout=20)
    foreign.terminate()
    foreign.wait(timeout=10)
