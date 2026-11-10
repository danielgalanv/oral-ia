"""Strict demo resource boundary, process environment and exclusive lifecycle lock."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import socket
import stat
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[3]


class DemoError(RuntimeError):
    pass


def write_json(path: Path, value):
    temporary = path.with_suffix(".new")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _no_links(path: Path):
    junction = path.is_junction() if hasattr(path, "is_junction") else False
    if path.is_symlink() or junction:
        raise DemoError("Ruta demo con enlace: se rechaza por seguridad.")
    if path.exists() and getattr(path.lstat(), "st_file_attributes", 0) & getattr(
        stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0
    ):
        raise DemoError("Ruta demo con reparse point: se rechaza por seguridad.")


@dataclass(frozen=True)
class DemoPaths:
    workspace: Path

    def __post_init__(self):
        object.__setattr__(self, "workspace", self.workspace.resolve())

    @property
    def root(self):
        return self.workspace / ".oralia-demo"

    @property
    def db(self):
        return self.root / "demo.db"

    @property
    def db_url(self):
        return f"sqlite:///{self.db.as_posix()}"

    @property
    def marker(self):
        return {"kind": "oralia-demo", "schema": 1, "workspace": str(self.workspace)}

    def validate(self, *, required=True, tree=False):
        # Resolve and compare before any recursive deletion or resource mutation.
        _no_links(self.root)
        if self.root.resolve() != self.workspace / ".oralia-demo":
            raise DemoError("La ruta demo no está dentro del workspace esperado.")
        if self.root.exists():
            marker = self.root / "marker.json"
            _no_links(marker)
            try:
                actual = json.loads(marker.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                raise DemoError(
                    "Directorio demo sin marcador válido; no se altera. Revise la ruta."
                ) from None
            if actual != self.marker:
                raise DemoError("Marcador demo no corresponde a este workspace; no se altera.")
            for directory, dirs, files in os.walk(self.root, followlinks=False):
                for name in [*dirs, *files]:
                    _no_links(Path(directory) / name)
                if not tree:
                    # Validate the complete tree anyway: no aliases into habitual data.
                    continue
        elif required:
            raise DemoError("Demo no preparada. Ejecute .\\scripts\\demo.ps1 primero.")

    def initialize(self):
        self.validate(required=False)
        if not self.root.exists():
            self.root.mkdir()
            write_json(self.root / "marker.json", self.marker)
        for name in ("files", "vector_store", "tmp", "vite-cache", "logs", "public", "config"):
            (self.root / name).mkdir(exist_ok=True)


@contextmanager
def lifecycle_lock(paths: DemoPaths):
    import msvcrt

    paths.workspace.mkdir(parents=True, exist_ok=True)
    lock_path = paths.workspace / ".oralia-demo.lock"
    _no_links(lock_path)
    with lock_path.open("a+b") as stream:
        try:
            if os.fstat(stream.fileno()).st_size == 0:
                stream.write(b"0")
                stream.flush()
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            raise DemoError(
                "Demo activa u otra operación en curso. Use -Action Stop y vuelva a intentar."
            ) from None
        try:
            yield
        finally:
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)


def child_environment(paths: DemoPaths, web_port: int, *, secret: str | None = None):
    env = {k: v for k, v in os.environ.items() if not k.startswith(("ORALIA_", "VITE_"))}
    env.update(
        {
            "ORALIA_DB_URL": paths.db_url,
            "ORALIA_VECTOR_STORE_PATH": str(paths.root / "vector_store"),
            "ORALIA_LOCAL_UI_ORIGIN": f"http://127.0.0.1:{web_port}",
            "ORALIA_ALLOW_LAN": "0",
            "ORALIA_COOKIE_NAMESPACE": "oralia_demo",
            "ORALIA_DEMO_CONFIG_DIR": str(paths.root / "config"),
            "ORALIA_DEMO_CACHE_DIR": str(paths.root / "vite-cache"),
            "ORALIA_DEMO_PUBLIC_DIR": str(paths.root / "public"),
            "HF_HUB_OFFLINE": "1",
            "TRANSFORMERS_OFFLINE": "1",
            "HF_HUB_DISABLE_TELEMETRY": "1",
            "ANONYMIZED_TELEMETRY": "False",
            "PYTHONIOENCODING": "utf-8",
            "TEMP": str(paths.root / "tmp"),
            "TMP": str(paths.root / "tmp"),
        }
    )
    if secret is not None:
        env["ORALIA_ADMIN_SECRET"] = secret
    return env


def check_ports(api_port, web_port):
    if not 1024 <= api_port <= 65535 or not 1024 <= web_port <= 65535 or api_port == web_port:
        raise DemoError("Use dos puertos distintos entre 1024 y 65535.")
    for port in (api_port, web_port):
        with socket.socket() as sock:
            try:
                sock.bind(("127.0.0.1", port))
            except OSError:
                raise DemoError(
                    f"Puerto {port} ocupado. Elija -ApiPort/-WebPort explícitos o libérelo usted."
                ) from None


def dependencies():
    missing = [
        name
        for name in (
            "fastapi",
            "uvicorn",
            "sqlalchemy",
            "alembic",
            "psutil",
            "docx",
            "chromadb",
            "sentence_transformers",
        )
        if importlib.util.find_spec(name) is None
    ]
    if missing:
        raise DemoError("Faltan dependencias Python. Prepare uv sync --extra dev antes de iniciar.")
    node = shutil.which("node.exe") or shutil.which("node")
    vite = SOURCE_ROOT / "apps/web/node_modules/vite/bin/vite.js"
    if not node or not vite.is_file():
        raise DemoError("Falta Node/Vite. Prepare Node y pnpm --dir apps/web install antes de iniciar.")
    return node, vite


def check_embeddings():
    # This process is a dedicated offline preflight/preparation process.
    os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", HF_HUB_DISABLE_TELEMETRY="1")
    from oralia.infrastructure.embeddings.sentence_transformer_adapter import (
        SentenceTransformerEmbeddingAdapter,
    )

    try:
        SentenceTransformerEmbeddingAdapter().embed(["El agua hierve a 100 grados."])
    except Exception:
        raise DemoError(
            "Faltan embeddings locales utilizables. Prepárelos con conexión o use -TextOnly "
            "(sin fuentes). No se descargó ningún modelo."
        ) from None
