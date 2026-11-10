"""Own Ollama process only; no pull, no shared listeners, no unrelated process kill."""

import json
import os
import shutil
import socket
import subprocess
import time
from contextlib import contextmanager
from pathlib import Path

import httpx
import psutil


@contextmanager
def owned_provider(
    output: Path, port=11436, *, local_source=None, model_name="qwen2.5:0.5b", model_store=None
):
    executable = shutil.which("ollama")
    if executable is None:
        raise ValueError("Falta Ollama local; no se descargará ningún recurso.")
    with socket.socket() as check:
        if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
            check.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        check.bind(("127.0.0.1", port))
    env = {
        key: value
        for key, value in os.environ.items()
        if key.upper()
        in {
            "SYSTEMROOT",
            "PATH",
            "TEMP",
            "TMP",
            "USERPROFILE",
            "HOME",
            "LOCALAPPDATA",
            "APPDATA",
            "PROGRAMFILES",
            "NUMBER_OF_PROCESSORS",
            "PROCESSOR_ARCHITECTURE",
        }
    }
    env.update(
        {
            "OLLAMA_HOST": f"127.0.0.1:{port}",
            "OLLAMA_NO_CLOUD": "1",
            "OLLAMA_CONTEXT_LENGTH": "8192",
            "OLLAMA_NOPRUNE": "1",
            "HTTP_PROXY": "http://127.0.0.1:9",
            "HTTPS_PROXY": "http://127.0.0.1:9",
            "NO_PROXY": "127.0.0.1,localhost",
        }
    )
    if local_source is not None:
        local_source = Path(local_source).resolve(strict=True)
        if model_store is None:
            raise ValueError("La conversión local requiere almacén propio explícito.")
        model_store = Path(model_store)
        model_store.mkdir(exist_ok=True)
        temporary = model_store.parent / "temporary"
        temporary.mkdir(exist_ok=True)
        home = model_store.parent / "provider-home"
        home.mkdir(exist_ok=True)
        env.update(
            {
                "OLLAMA_MODELS": str(model_store.resolve()),
                "HOME": str(home.resolve()),
                "USERPROFILE": str(home.resolve()),
                "TEMP": str(temporary.resolve()),
                "TMP": str(temporary.resolve()),
            }
        )
    started = time.monotonic()
    with (
        (output / "provider-stdout.log").open("wb") as stdout,
        (output / "provider-stderr.log").open("wb") as stderr,
    ):
        process = subprocess.Popen(
            [executable, "serve"],
            env=env,
            stdout=stdout,
            stderr=stderr,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        root = psutil.Process(process.pid)
        creation = root.create_time()
        (output / "ownership.json").write_text(
            json.dumps({"pid": process.pid, "creation_time": creation, "port": port}), encoding="utf-8"
        )
        try:
            while time.monotonic() - started < 30:
                if process.poll() is not None:
                    raise RuntimeError("El proceso propio de Ollama terminó; revise el log local.")
                listeners = [
                    c
                    for c in psutil.net_connections(kind="tcp")
                    if c.status == "LISTEN" and c.laddr.port == port
                ]
                if listeners:
                    if any(c.pid != process.pid or c.laddr.ip != "127.0.0.1" for c in listeners):
                        raise RuntimeError("El puerto no pertenece exclusivamente al proceso propio.")
                    try:
                        with httpx.Client(trust_env=False, timeout=2) as client:
                            response = client.get(f"http://127.0.0.1:{port}/api/tags")
                            response.raise_for_status()
                            data = response.json()
                    except (httpx.TimeoutException, httpx.ConnectError):
                        time.sleep(0.25)
                        continue
                    models = [m for m in data.get("models", []) if m["name"] == model_name]
                    if not models and local_source is not None:
                        modelfile = output / "Modelfile"
                        modelfile.write_text("FROM " + local_source.as_posix() + "\n", encoding="utf-8")
                        converting = time.monotonic()
                        print(
                            "Convirtiendo pesos locales preparados al almacén propio; sin "
                            "descargas. Puede tardar.",
                            flush=True,
                        )
                        with (output / "model-import.log").open("wb") as import_log:
                            completed = subprocess.run(
                                [executable, "create", model_name, "-f", str(modelfile.resolve())],
                                env=env,
                                stdout=import_log,
                                stderr=subprocess.STDOUT,
                                timeout=600,
                                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                            )
                        (output / "model-import.json").write_text(
                            json.dumps(
                                {
                                    "source": str(local_source),
                                    "elapsed_seconds": time.monotonic() - converting,
                                    "exit_code": completed.returncode,
                                    "no_download_requested": True,
                                }
                            ),
                            encoding="utf-8",
                        )
                        if completed.returncode:
                            raise RuntimeError(
                                "La conversión local falló; se conserva el diagnóstico, sin "
                                "descargar otro modelo."
                            )
                        with httpx.Client(trust_env=False, timeout=5) as client:
                            data = client.get(f"http://127.0.0.1:{port}/api/tags").json()
                        models = [m for m in data.get("models", []) if m["name"] == model_name]
                    if not models:
                        raise ValueError("Falta el modelo local elegido; no se descargó ni cambió por otro.")
                    (output / "provider.json").write_text(
                        json.dumps(
                            {
                                "model": models[0],
                                "pid": process.pid,
                                "creation_time": creation,
                                "port": port,
                                "ready_seconds": time.monotonic() - started,
                                "cloud": False,
                            },
                            indent=2,
                        ),
                        encoding="utf-8",
                    )
                    loading = time.monotonic()
                    with httpx.Client(trust_env=False, timeout=60) as client:
                        prepared = client.post(
                            f"http://127.0.0.1:{port}/api/generate",
                            json={"model": model_name, "prompt": "", "stream": False, "keep_alive": "5m"},
                        )
                        prepared.raise_for_status()
                    (output / "model-preparation.json").write_text(
                        json.dumps(
                            {
                                "empty_preload": True,
                                "elapsed_seconds": time.monotonic() - loading,
                                "response": prepared.json(),
                            }
                        ),
                        encoding="utf-8",
                    )
                    probing = time.monotonic()
                    with httpx.Client(trust_env=False, timeout=60) as client:
                        probe = client.post(
                            f"http://127.0.0.1:{port}/api/generate",
                            json={
                                "model": model_name,
                                "prompt": "Responde únicamente: listo.",
                                "stream": False,
                                "options": {"num_predict": 8},
                                "keep_alive": "5m",
                            },
                        )
                        probe.raise_for_status()
                    (output / "technical-probe.json").write_text(
                        json.dumps(
                            {
                                "academic_conversation": False,
                                "elapsed_seconds": time.monotonic() - probing,
                                "response": probe.json(),
                            }
                        ),
                        encoding="utf-8",
                    )
                    yield f"http://127.0.0.1:{port}"
                    break
                time.sleep(0.25)
            else:
                raise TimeoutError("Ollama propio no estuvo disponible en30s.")
        finally:
            # Capture descendants before stopping our parent; verify each birth time.
            owned = []
            if process.poll() is None and root.create_time() == creation:
                owned = [(p, p.create_time()) for p in root.children(recursive=True)]
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
            for child, born in owned:
                try:
                    if child.create_time() == born and child.is_running():
                        child.terminate()
                        try:
                            child.wait(timeout=10)
                        except psutil.TimeoutExpired:
                            child.kill()
                            child.wait(timeout=5)
                except psutil.NoSuchProcess:
                    pass
