"""Teacher-side reading and marking of the notice log (`notice_log.py`); shared by the CLI and the web page."""

import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

VERDICTS = ("acierto", "falsa_alarma", "dudoso")
DEFAULT_DIR = Path(__file__).resolve().parents[3] / "registro-avisos"


def log_dir():
    return Path(os.environ.get("ORALIA_REGISTRO_AVISOS") or DEFAULT_DIR)


def read_lines(path):
    if not path.exists():
        return []
    entries = []
    for line in path.read_text(encoding="utf8").splitlines():
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue  # a half-written line never hides the others
    return entries


def marks(directory=None):
    """id -> last mark of that notice."""
    return {m["id"]: m for m in read_lines((directory or log_dir()) / "etiquetas.jsonl")}


def notices(directory=None):
    """Every logged notice, newest first, with its mark (or None)."""
    directory = directory or log_dir()
    labelled = marks(directory)
    rows = [dict(e, mark=labelled.get(e["id"])) for e in read_lines(directory / "avisos.jsonl")]
    return sorted(rows, key=lambda e: e["at"], reverse=True)


def mark(identifier, verdict, note="", directory=None):
    directory = directory or log_dir()
    if verdict not in VERDICTS:
        raise ValueError("unknown verdict")
    if identifier not in {e["id"] for e in read_lines(directory / "avisos.jsonl")}:
        raise KeyError(identifier)
    entry = dict(
        id=identifier,
        veredicto=verdict,
        nota=str(note)[:1000],
        at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "etiquetas.jsonl").open("a", encoding="utf8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def purge(older_than_days=0, directory=None, now=None):
    """Delete notices (and their marks) older than `older_than_days`; 0 deletes everything. Returns how many were removed."""
    directory = directory or log_dir()
    now = now or datetime.now(timezone.utc)
    notices_path, marks_path = directory / "avisos.jsonl", directory / "etiquetas.jsonl"
    entries = read_lines(notices_path)
    keep = [
        e
        for e in entries
        if older_than_days > 0 and (now - datetime.fromisoformat(e["at"])).days < older_than_days
    ]
    kept_ids = {e["id"] for e in keep}

    def write(path, rows):
        path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf8")

    if notices_path.exists():
        write(notices_path, keep)
    if marks_path.exists():
        write(marks_path, [m for m in read_lines(marks_path) if m["id"] in kept_ids])
    return len(entries) - len(keep)


def summary(directory=None):
    rows = notices(directory)
    labelled = [r for r in rows if r["mark"]]
    by_kind = Counter((k, r["mark"]["veredicto"]) for r in labelled for k in r["notice_kinds"])
    return dict(
        total=len(rows),
        evaluados=len(labelled),
        por_veredicto=dict(Counter(r["mark"]["veredicto"] for r in labelled)),
        por_tipo=[dict(tipo=k, veredicto=v, n=n) for (k, v), n in sorted(by_kind.items())],
    )
