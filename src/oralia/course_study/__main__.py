"""Local terminal using the normal authenticated ASGI API; no network listener."""

import argparse
import hashlib
import json
import logging
import os
import secrets
import stat
import sys
from contextlib import contextmanager
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[3]


def _no_alias(path):
    if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
        raise ValueError("Ruta con enlace; no se modifica.")
    if path.exists():
        info = path.lstat()
        if getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
            raise ValueError("Ruta con enlace o reparse point; no se modifica.")
        if stat.S_ISREG(info.st_mode) and info.st_nlink > 1:
            raise ValueError("Archivo con enlace duro; no se modifica.")


def root_for(workspace):
    workspace = Path(workspace)
    _no_alias(workspace)
    workspace = workspace.resolve()
    root = workspace / ".oralia-course-study"
    _no_alias(root)
    marker = {"kind": "oralia-real-course-study", "version": 1, "workspace": str(workspace)}
    if root.exists():
        _no_alias(root / "marker.json")
        if json.loads((root / "marker.json").read_text(encoding="utf-8")) != marker:
            raise ValueError("El entorno no tiene el marcador esperado; no se modifica.")
        for directory, directories, files in os.walk(root, followlinks=False):
            for name in directories + files:
                _no_alias(Path(directory) / name)
    else:
        root.mkdir()
        (root / "marker.json").write_text(json.dumps(marker), encoding="utf-8")
    for name in ["vector_store", "tmp", "config"]:
        (root / name).mkdir(exist_ok=True)
    return root


@contextmanager
def owned_lock(root):
    import msvcrt

    with (root / "operation.lock").open("a+b") as stream:
        if stream.seek(0, 2) == 0:
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        try:
            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            raise ValueError("Ya hay un autoestudio en este entorno. Cierre esa terminal.") from None
        try:
            yield
        finally:
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)


def interactive(client, prepared, read=input, write=print, pending=None):
    from oralia.course_study.preparation import RECIPIENT, checked

    session = checked(
        client.post(
            "/api/v1/sessions",
            json={"participant_code": RECIPIENT, "activity_configuration_id": prepared["activity_id"]},
        ),
        201,
    )
    sid = session["session_id"]
    write(session["ai_disclosure"])
    write(session["privacy_notice"])
    if pending is not None:
        pending.write_text(
            json.dumps({"session_id": sid, "activity_id": prepared["activity_id"]}), encoding="utf-8"
        )
    write(
        "ORALIA: asistente de IA; puede equivocarse. Perfil extractivo limitado: citas, "
        "sin elaboración libre. Voz no validada."
    )
    write(
        "Fuente: Procedimiento requisitos, páginas 10–12. /salir cierra sin conservar "
        "contenido; /fuentes muestra la correspondencia."
    )
    try:
        while True:
            try:
                text = read("Tú: ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not text:
                continue
            if text == "/salir":
                break
            if text == "/fuentes":
                write(
                    "Extracto 1 → original 10; extracto 2 → original 11; extracto 3 → original 12. "
                    "Derivación mecánica, sin aprobación docente inferida."
                )
                continue
            response = client.post(f"/api/v1/sessions/{sid}/study-turns", json={"text": text})
            if response.status_code != 200:
                write(
                    f"No se pudo procesar el turno (HTTP {response.status_code}); "
                    "cierre de esta sesión propia."
                )
                break
            actual = response.json()
            write(
                "ORALIA (salida efectiva): "
                + (
                    actual.get("output_text")
                    or "Sin respuesta publicable; revise la preparación antes de reintentar."
                )
            )
            for citation in actual.get("sources", []):
                page = citation["location_ref"].split()[-1]
                original = prepared["provenance"]["pages"].get(page, "no identificada")
                write(
                    f"Fuente: página original {original}, {citation['location_ref']} del extracto; "
                    f"versión {citation['document_version']}."
                )
            if actual.get("session_closed") or actual.get("blocked"):
                write("La API ha detenido la sesión; no se simulan turnos restantes.")
                break
    finally:
        response = client.post(f"/api/v1/sessions/{sid}/study-end", json={"retain": False, "scope": []})
        if response.status_code == 200:
            status = response.json().get("status")
            write(
                f"Sesión finalizada ({status}) sin conservación de contenido; materiales preparados intactos."
            )
            if pending is not None:
                pending.unlink(missing_ok=True)
        else:
            write(
                "No se confirmó el cierre. Vuelva a iniciar el entorno "
                "para recuperar solo su sesión pendiente."
            )
    return sid


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Autoestudio real aislado; terminal/API ASGI local sin puertos."
    )
    parser.add_argument("--workspace", type=Path, default=WORKSPACE, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    for stream in [sys.stdout, sys.stderr]:
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    root = root_for(args.workspace)
    with owned_lock(root):
        if "oralia.infrastructure.db.engine" in sys.modules:
            raise RuntimeError("Use una ejecución nueva del comando para aislar el motor de datos.")
        for key in list(os.environ):
            if key.startswith(("ORALIA_", "VITE_")):
                del os.environ[key]
        secret = secrets.token_urlsafe(32)
        os.environ.update(
            {
                "ORALIA_DB_URL": f"sqlite:///{(root / 'course.db').as_posix()}",
                "ORALIA_VECTOR_STORE_PATH": str(root / "vector_store"),
                "ORALIA_ADMIN_SECRET": secret,
                "ORALIA_ALLOW_LAN": "0",
                "HF_HUB_OFFLINE": "1",
                "TRANSFORMERS_OFFLINE": "1",
                "HF_HUB_DISABLE_TELEMETRY": "1",
                "ANONYMIZED_TELEMETRY": "False",
                "TEMP": str(root / "tmp"),
                "TMP": str(root / "tmp"),
            }
        )
        import tempfile

        tempfile.tempdir = str(root / "tmp")
        import structlog
        from alembic import command
        from alembic.config import Config
        from fastapi.testclient import TestClient

        from oralia.course_study.materials import DEFAULT_SOURCE
        from oralia.course_study.preparation import checked, prepare
        from oralia.interfaces.api.app import create_app

        if not DEFAULT_SOURCE.is_file():
            raise ValueError("Falta el PDF original de Procedimiento requisitos en la ruta proporcionada.")
        print("Comprobando embeddings locales; la primera carga puede tardar. Sin descargas.")
        from oralia.infrastructure.embeddings.sentence_transformer_adapter import (
            SentenceTransformerEmbeddingAdapter,
        )

        try:
            SentenceTransformerEmbeddingAdapter().embed(["Calidad y validación de requisitos"])
        except Exception:
            raise ValueError(
                "Faltan embeddings locales utilizables. Prepare los recursos antes de repetir; "
                "no se descargó ningún modelo."
            ) from None
        print("Preparando esquema y recursos locales propios.")
        config = Config(str(WORKSPACE / "alembic.ini"))
        command.upgrade(config, "head")
        structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.WARNING))
        app = create_app()
        manifest = root / "config" / "activity.json"
        source_hash = hashlib.sha256(DEFAULT_SOURCE.read_bytes()).hexdigest()
        with TestClient(app, base_url="http://127.0.0.1") as teacher:
            checked(teacher.post("/api/v1/auth/login", json={"secret": secret}))
            if manifest.exists():
                prepared = json.loads(manifest.read_text(encoding="utf-8"))
                if (
                    prepared["provenance"]["original_sha256"] != source_hash
                    or prepared["policy"] != "material-self-study/v2"
                ):
                    raise ValueError(
                        "La fuente/perfil cambió; se conserva el entorno. "
                        "Prepare un nuevo workspace propio explícito."
                    )
                rows = checked(teacher.get("/api/v1/governance/activities"))
                current = next((row for row in rows if row["id"] == prepared["activity_id"]), None)
                if (
                    not current
                    or current["course_id"] != prepared["course_id"]
                    or current["status"] != "active"
                    or current["model_id"] != "deterministic"
                    or current["output_authorization_policy"]["policy_id"] != prepared["policy"]
                ):
                    raise ValueError(
                        "La actividad preparada no coincide con el perfil propio; "
                        "no se reutiliza ni se duplica."
                    )
                checked(teacher.get(f"/api/v1/activities/{prepared['activity_id']}"))
                document = checked(teacher.get(f"/api/v1/materials/documents/{prepared['document']['id']}"))
                if (
                    document["status"] != "active"
                    or document["course_id"] != prepared["course_id"]
                    or document["version"] != prepared["document"]["version"]
                    or document["content_hash"] != prepared["document"]["content_hash"]
                ):
                    raise ValueError(
                        "El material preparado cambió o no está activo; no se sustituye silenciosamente."
                    )
            else:
                preparation_pending = root / "config" / "preparation-pending.json"
                if preparation_pending.exists():
                    raise ValueError(
                        "Preparación anterior incompleta; se conservan sus recursos y no se duplican. "
                        "Revise el entorno antes de reintentar."
                    )
                preparation_pending.write_text(json.dumps({"original_sha256": source_hash}), encoding="utf-8")
                prepared = prepare(teacher)
                temporary = manifest.with_suffix(".new")
                temporary.write_text(json.dumps(prepared, ensure_ascii=False, indent=2), encoding="utf-8")
                temporary.replace(manifest)
                preparation_pending.unlink()
            # Recover only an own interrupted session recorded by this environment.
            pending = root / "config" / "pending-session.json"
            if pending.exists():
                prior = json.loads(pending.read_text())
                if prior["activity_id"] != prepared["activity_id"]:
                    raise ValueError("La sesión pendiente no corresponde a la actividad preparada.")
                own_sid = prior["session_id"]
                checked(
                    teacher.post(
                        f"/api/v1/governance/sessions/{own_sid}/close",
                        json={"confirm": True, "reason": "abandoned"},
                    )
                )
                pending.unlink()
            checked(teacher.post("/api/v1/auth/logout"))
        print(
            "Perfil extractive_limited/deterministic; API ASGI en proceso, sin servidor TCP ni demo habitual."
        )
        print("Actividad aislada preparada: " + prepared["activity_id"])
        with TestClient(app, base_url="http://127.0.0.1") as learner:
            interactive(learner, prepared, pending=root / "config" / "pending-session.json")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Cancelado; solo recursos de autoestudio propios.")
        raise SystemExit(130) from None
    except Exception as exc:
        # No environment dump, token, credential or participant content.
        print(f"Autoestudio no disponible ({type(exc).__name__}): {exc}", file=sys.stderr)
        raise SystemExit(2) from None
