"""Foreground Windows supervisor: owned children only, localhost and explicit reset."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
import webbrowser
from pathlib import Path

import psutil

from oralia.demo.progress import Progress
from oralia.demo.resources import (
    SOURCE_ROOT,
    DemoError,
    DemoPaths,
    check_embeddings,
    check_ports,
    child_environment,
    dependencies,
    lifecycle_lock,
    write_json,
)


def check(paths, api_port=8010, web_port=5180, *, text_only=False, progress=None):
    progress = progress or Progress(paths=paths)
    with progress.stage("dependencias"):
        paths.validate(required=False)
        dependencies()
        check_ports(api_port, web_port)
    if not text_only:
        with progress.stage("embeddings"):
            check_embeddings()
    with progress.stage("esquema"):
        if paths.db.exists():
            from alembic.runtime.migration import MigrationContext
            from alembic.script import ScriptDirectory

            from oralia.demo.fixtures import migration_config
            from oralia.infrastructure.db.engine import build_engine

            engine = build_engine(paths.db_url)
            try:
                with engine.connect() as connection:
                    current = MigrationContext.configure(connection).get_current_revision()
                script = ScriptDirectory.from_config(migration_config(paths))
                if current is not None and current not in {r.revision for r in script.walk_revisions()}:
                    raise DemoError(
                        "Revisión demo desconocida. No se altera; revise su origen antes de Reset."
                    )
            finally:
                engine.dispose()
    return {
        "api": f"http://127.0.0.1:{api_port}",
        "web": f"http://127.0.0.1:{web_port}",
        "data": str(paths.root),
        "profile": "text_only: sin fuentes" if text_only else "full: embeddings locales",
        "generation": "deterministic; no es una validación de LLM/voz/utilidad humana",
    }


def _identity(process):
    try:
        return process.pid, psutil.Process(process.pid).create_time()
    except psutil.NoSuchProcess:
        return None


def _stop_owned(children):
    # IDs come from live Popen objects created by this invocation, never from a receipt/port scan.
    owned = []
    for _child, identity in children:
        if identity is None:
            continue
        try:
            root = psutil.Process(identity[0])
            if root.create_time() != identity[1]:
                continue
            owned += [*root.children(recursive=True), root]
        except psutil.NoSuchProcess:
            continue
    for process in owned:
        try:
            process.terminate()  # psutil Process guards PID reuse.
        except psutil.NoSuchProcess:
            pass
    _, remaining = psutil.wait_procs(owned, timeout=5)
    for process in remaining:
        try:
            process.kill()
        except psutil.NoSuchProcess:
            pass
    psutil.wait_procs(remaining, timeout=5)
    for child, _ in children:
        try:
            child.wait(timeout=2)
        except subprocess.TimeoutExpired:
            pass


def _json_at(url):
    # Ignore ambient HTTP proxies, including on offline demonstrations.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(url, timeout=0.7) as response:
            return json.loads(response.read(4096))
    except (OSError, ValueError, urllib.error.URLError):
        return None


def start(
    paths: DemoPaths,
    *,
    secret: str | None = None,
    secret_factory=None,
    progress=None,
    api_port=8010,
    web_port=5180,
    text_only=False,
    no_browser=False,
    readiness_timeout=90,
    preparation_timeout=120,
):
    progress = progress or Progress(paths=paths)
    progress.protect(secret)
    with lifecycle_lock(paths):
        details = check(paths, api_port, web_port, text_only=text_only, progress=progress)
        secret = secret if secret is not None else secret_factory()
        progress.protect(secret)
        if len(secret) < 24:
            raise DemoError("La credencial demo debe tener al menos 24 caracteres; no se ha guardado.")
        paths.initialize()
        receipt_path = paths.root / "run.json"
        if receipt_path.exists() and _live_supervisor(paths, strict=False):
            raise DemoError("Ya hay una demo activa. Use -Action Stop.")
        paths.validate()
        prep_env = child_environment(paths, web_port)
        log_paths = [paths.root / f"logs/{name}.log" for name in ("prepare", "api", "web")]
        with progress.stage("texto" if text_only else "preparacion"):
            with log_paths[0].open("w", encoding="utf-8") as log:
                preparation = subprocess.Popen(
                    [
                        sys.executable,
                        "-m",
                        "oralia.demo",
                        "prepare",
                        "--workspace",
                        str(paths.workspace),
                        *(["--text-only"] if text_only else []),
                    ],
                    cwd=SOURCE_ROOT,
                    env=prep_env,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                )
                identity = _identity(preparation)
                try:
                    preparation.wait(timeout=preparation_timeout)
                except subprocess.TimeoutExpired:
                    _stop_owned([(preparation, identity)])
                    raise DemoError(
                        "Preparación interrumpida o lenta. Se detuvo su proceso; revise logs/prepare.log."
                    ) from None
                except KeyboardInterrupt:
                    _stop_owned([(preparation, identity)])
                    raise
            if preparation.returncode:
                raise DemoError(
                    "Preparación demo falló. Revise .oralia-demo/logs/prepare.log; "
                    "no se arrancaron servidores."
                )
        run_id = uuid.uuid4().hex
        write_json(
            receipt_path,
            {
                "run_id": run_id,
                "pid": os.getpid(),
                "created": psutil.Process().create_time(),
                "workspace": str(paths.workspace),
                "api_port": api_port,
                "web_port": web_port,
            },
        )
        write_json(paths.root / "public/demo-ready.json", {"run_id": run_id})
        stop_path = paths.root / "stop.json"
        stop_path.unlink(missing_ok=True)
        node, vite = dependencies()
        env_api = child_environment(paths, web_port, secret=secret)
        env_web = child_environment(paths, web_port)
        env_web.update(
            ORALIA_E2E_WEB_PORT=str(web_port),
            ORALIA_E2E_API_URL=details["api"],
            VITE_ORALIA_DEMO_PROFILE="text_only" if text_only else "full",
        )
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        children = []
        logs = []
        readiness = None
        try:
            for stage, command, env, log_path in [
                (
                    "api",
                    [
                        sys.executable,
                        "-m",
                        "oralia.demo",
                        "serve-api",
                        "--workspace",
                        str(paths.workspace),
                        "--api-port",
                        str(api_port),
                        "--run-id",
                        run_id,
                    ],
                    env_api,
                    log_paths[1],
                ),
                (
                    "interfaz",
                    [node, str(vite), "--host", "127.0.0.1", "--port", str(web_port), "--strictPort"],
                    env_web,
                    log_paths[2],
                ),
            ]:
                with progress.stage(stage, completion="Proceso iniciado; disponibilidad pendiente."):
                    log = log_path.open("w", encoding="utf-8")
                    logs.append(log)
                    child = subprocess.Popen(
                        command,
                        cwd=SOURCE_ROOT / "apps/web" if env is env_web else SOURCE_ROOT,
                        env=env,
                        stdout=log,
                        stderr=subprocess.STDOUT,
                        creationflags=flags,
                    )
                    children.append((child, _identity(child)))
            deadline = time.monotonic() + readiness_timeout
            ready = False
            readiness = progress.stage(
                "espera",
                note=(
                    "La API también carga sus embeddings locales antes de estar disponible."
                    if not text_only
                    else "Esperando respuesta de API e interfaz."
                ),
            )
            readiness.__enter__()
            while True:
                if any(child.poll() is not None for child, _ in children):
                    raise DemoError(
                        "Un servidor terminó. Revise logs/api.log y logs/web.log; sus hijos se detuvieron."
                    )
                if stop_path.exists():
                    try:
                        if json.loads(stop_path.read_text(encoding="utf-8")) == {"run_id": run_id}:
                            break
                    except ValueError:
                        pass
                if not ready:
                    if _json_at(details["api"] + "/demo-ready") == {"run_id": run_id} and _json_at(
                        details["web"] + "/demo-ready.json"
                    ) == {"run_id": run_id}:
                        ready = True
                        readiness.__exit__(None, None, None)
                        readiness = None
                        print("DEMO LISTA: " + details["web"], flush=True)
                        print(
                            "Datos ficticios; código demo-007; generación determinista. "
                            + details["profile"],
                            flush=True,
                        )
                        print(
                            "Ctrl+C o .\\scripts\\demo.ps1 -Action Stop. La credencial no se guarda.",
                            flush=True,
                        )
                        if not no_browser:
                            webbrowser.open(details["web"])
                    elif time.monotonic() >= deadline:
                        raise DemoError("Timeout de arranque. Revise logs demo; no se cambió ningún puerto.")
                time.sleep(0.15)
        except KeyboardInterrupt:
            if readiness is not None:
                readiness.__exit__(KeyboardInterrupt, KeyboardInterrupt(), None)
                readiness = None
            print("Parando únicamente los procesos de esta demo…", flush=True)
        except Exception:
            if readiness is not None:
                readiness.__exit__(*sys.exc_info())
                readiness = None
            raise
        finally:
            if readiness is not None:
                readiness.__exit__(KeyboardInterrupt, KeyboardInterrupt(), None)
            _stop_owned(children)
            for log in logs:
                log.close()
            receipt_path.unlink(missing_ok=True)
            stop_path.unlink(missing_ok=True)
            (paths.root / "public/demo-ready.json").unlink(missing_ok=True)
            print("Demo detenida; datos conservados.", flush=True)


def _live_supervisor(paths, *, strict=True):
    try:
        receipt = json.loads((paths.root / "run.json").read_text(encoding="utf-8"))
        process = psutil.Process(receipt["pid"])
        valid = (
            receipt["workspace"] == str(paths.workspace)
            and process.create_time() == receipt["created"]
            and "oralia.demo" in process.cmdline()
            and "start" in process.cmdline()
            and Path(process.cwd()).resolve() == SOURCE_ROOT
        )
        if not valid:
            raise DemoError("Recibo de proceso no corresponde al supervisor; no se detiene ningún PID.")
        return receipt
    except (FileNotFoundError, psutil.NoSuchProcess):
        return None
    except (ValueError, KeyError, psutil.AccessDenied):
        if strict:
            raise DemoError("No se puede verificar el supervisor; no se detiene ningún proceso.") from None
        return None


def stop(paths: DemoPaths, *, timeout=20):
    paths.validate()
    receipt = _live_supervisor(paths)
    if receipt is None:
        print("No hay supervisor demo activo; no se detuvo ningún proceso.")
        return
    write_json(paths.root / "stop.json", {"run_id": receipt["run_id"]})
    deadline = time.monotonic() + timeout
    while (paths.root / "run.json").exists():
        if time.monotonic() >= deadline:
            raise DemoError(
                "Supervisor no confirmó parada. Use Ctrl+C en su terminal; no se mató ningún PID ajeno."
            )
        time.sleep(0.1)
    print("Parada confirmada; solo hijos del lanzador.")


def reset(paths: DemoPaths, *, confirmation: str):
    with lifecycle_lock(paths):
        paths.validate(tree=True)
        if _live_supervisor(paths):
            raise DemoError("Demo activa. Use -Action Stop antes de reiniciar datos.")
        if confirmation != "BORRAR DEMO":
            raise DemoError("Reinicio cancelado. No se borró ningún dato.")
        paths.validate(tree=True)  # Verify absolute target and links again immediately before deletion.
        shutil.rmtree(paths.root)
        print("Solo se eliminaron los datos demo: " + str(paths.root))
