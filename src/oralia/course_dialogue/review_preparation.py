"""Prepare pending teacher drafts through normal APIs in a separate owned database.

No model inference, participant session, publication or reviewed=True operation.
Run in a new Python process so the habitual database engine cannot be reused.
"""

import hashlib
import io
import json
import logging
import os
import re
import secrets
import sqlite3
import sys
from pathlib import Path


def save(path, value):
    temporary = path.with_suffix(".new")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf8")
    temporary.replace(path)


def packet_fingerprint(packet, *, semantic_policy=False):
    """A different policy gets a different owned environment; legacy identity stays exact."""
    value = packet
    if semantic_policy:
        from oralia.domain.dialogue.semantic_templates import SEMANTIC_POLICY_ID

        value = {"packet": packet, "policy_profile": SEMANTIC_POLICY_ID}
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def reuse_selected_materials(destination, source, catalog, selection, source_root):
    """Copy verified existing bytes only; never create a new PDF selection here."""
    from oralia.course_study.__main__ import _no_alias

    for path in [source, destination, source / "provenance.json"]:
        _no_alias(path)
    if not source.is_dir() or not (source / "provenance.json").is_file():
        raise ValueError("prepare the ordinary review materials first; no PDF is regenerated")
    for key in selection:
        _no_alias(source / f"012-{key}-selected.pdf")
        if destination.exists():
            _no_alias(destination / f"012-{key}-selected.pdf")
    if destination.exists():
        _no_alias(destination / "provenance.json")
    stored = selected_materials(source, catalog, selection, source_root)
    names = [row["derived_name"] for row in stored.values()] + ["provenance.json"]
    for name in names:
        _no_alias(source / name)
    if destination.exists():
        existing = selected_materials(destination, catalog, selection, source_root)
        if existing != stored:
            raise ValueError("existing selected material provenance differs; no replacement performed")
        return existing
    payload = {name: (source / name).read_bytes() for name in names}
    # Revalidate bytes captured for copying, rather than trusting an earlier read.
    for row in stored.values():
        if hashlib.sha256(payload[row["derived_name"]]).hexdigest() != row["derived_sha256"]:
            raise ValueError("selected material changed before copying")
    if json.loads(payload["provenance.json"]) != stored:
        raise ValueError("selected material provenance changed before copying")
    destination.mkdir()
    for name, data in payload.items():
        (destination / name).write_bytes(data)
    return selected_materials(destination, catalog, selection, source_root)


def review_root(lab, fingerprint):
    from oralia.course_study.__main__ import _no_alias

    if not re.fullmatch("[a-f0-9]{64}", fingerprint):
        raise ValueError("invalid review packet fingerprint")
    root = lab / ("review-" + fingerprint[:12])
    _no_alias(root)
    marker = {
        "kind": "oralia-course-dialogue-review",
        "version": 1,
        "packet_fingerprint": fingerprint,
        "workspace": str(lab.parent.resolve()),
    }
    path = root / "environment.json"
    if root.exists():
        _no_alias(path)
        if not path.is_file() or json.loads(path.read_text(encoding="utf8")) != marker:
            raise ValueError("review environment marker missing or mismatched; no data modified")
    else:
        root.mkdir()
        save(path, marker)
    return root


def selected_materials(folder, catalog, selection, source_root):
    """Create exactly three mechanical PDF selections, or verify existing bytes."""
    import pypdfium2 as pdfium

    manifest = folder / "provenance.json"
    originals = {
        key: hashlib.sha256((source_root / name).read_bytes()).hexdigest()
        for key, (name, pages) in selection.items()
    }
    if manifest.exists():
        stored = json.loads(manifest.read_text(encoding="utf8"))
        if set(stored) != set(selection):
            raise ValueError("derived selection metadata changed")
        for key, row in stored.items():
            if (
                row.get("derived_name") != f"012-{key}-selected.pdf"
                or row.get("original_name") != selection[key][0]
                or row.get("pages") != {str(i + 1): p for i, p in enumerate(selection[key][1])}
            ):
                raise ValueError("derived selection metadata is outside expected source scope")
            if (
                row["original_sha256"] != originals[key]
                or hashlib.sha256((folder / row["derived_name"]).read_bytes()).hexdigest()
                != row["derived_sha256"]
            ):
                raise ValueError("prepared review material changed; no replacement performed")
        return stored
    if folder.exists():
        raise ValueError("incomplete material preparation preserved; inspect before retry")
    folder.mkdir()
    expected = {r["id"]: r for r in catalog}
    result = {}
    for key, (name, pages) in selection.items():
        if any(expected[f"{key}:{page}"]["original_sha256"] != originals[key] for page in pages):
            raise ValueError("original source changed before PDF selection")
        source = pdfium.PdfDocument((source_root / name).read_bytes())
        writer = pdfium.PdfDocument.new()
        try:
            writer.import_pages(source, [p - 1 for p in pages])
            stream = io.BytesIO()
            writer.save(stream)
            data = stream.getvalue()
            derived_name = f"012-{key}-selected.pdf"
            with pdfium.PdfDocument(data) as derived:
                if len(derived) != len(pages):
                    raise ValueError("derived PDF page count mismatch")
                for index, original in enumerate(pages):
                    before = source[original - 1].render(scale=1).to_pil()
                    after = derived[index].render(scale=1).to_pil()
                    if before.size != after.size or before.tobytes() != after.tobytes():
                        raise ValueError("derived PDF rendering differs from authorized original page")
            (folder / derived_name).write_bytes(data)
            result[key] = {
                "original_name": name,
                "original_sha256": originals[key],
                "derived_name": derived_name,
                "derived_sha256": hashlib.sha256(data).hexdigest(),
                "pages": {str(i + 1): p for i, p in enumerate(pages)},
                "pixel_comparison": "all selected pages equal at scale1",
                "transformation": "mechanical selection only; no teacher approval inferred",
            }
        finally:
            writer.close()
            source.close()
    save(manifest, result)
    return result


def prepare(root, packet, catalog, selection, source_root, *, semantic_policy=False):
    if semantic_policy:
        marker = root / "environment.json"
        if not marker.is_file() or json.loads(marker.read_text(encoding="utf8")).get(
            "packet_fingerprint"
        ) != packet_fingerprint(packet, semantic_policy=True):
            raise ValueError(
                "semantic policy requires its separate marked environment before database access"
            )
    import structlog
    from alembic import command
    from alembic.config import Config
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    from oralia.course_dialogue.authoring import draft_graph, next_draft_input
    from oralia.course_study.preparation import checked
    from oralia.domain.dialogue.catalog import guided_policy
    from oralia.domain.dialogue.semantic_templates import semantic_guided_policy
    from oralia.infrastructure.db import models
    from oralia.interfaces.api.app import create_app

    workspace = Path(__file__).resolve().parents[3]
    command.upgrade(Config(str(workspace / "alembic.ini")), "head")
    structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.WARNING))
    material = selected_materials(root / "materials", catalog, selection, source_root)
    fingerprint = packet_fingerprint(packet, semantic_policy=semantic_policy)
    journal = root / "preparation.json"
    state = (
        json.loads(journal.read_text(encoding="utf8"))
        if journal.exists()
        else {
            "packet_fingerprint": fingerprint,
            "course": None,
            "retention": None,
            "activity": None,
            "documents": {},
            "units": {},
            "pending_operation": None,
        }
    )
    if state["packet_fingerprint"] != fingerprint:
        raise ValueError("packet changed; existing review preserved")
    if state["pending_operation"]:
        raise ValueError("previous API operation unconfirmed; review journal before retry")
    save(journal, state)

    def recorded(label, call, store):
        state["pending_operation"] = label
        save(journal, state)
        value = call()
        store(value)
        state["pending_operation"] = None
        save(journal, state)
        return value

    app = create_app()
    with TestClient(app, base_url="http://127.0.0.1") as teacher:
        checked(teacher.post("/api/v1/auth/login", json={"secret": os.environ["ORALIA_ADMIN_SECRET"]}))
        try:
            if state["course"] is None:
                recorded(
                    "create-course",
                    lambda: checked(
                        teacher.post(
                            "/api/v1/governance/courses",
                            json={
                                "name": "Ingeniería del Software012 — revisión docente pendiente",
                                "subject_code": "IS-REVIEW-012",
                            },
                        ),
                        201,
                    ),
                    lambda v: state.update(course=v),
                )
            if state["retention"] is None:
                recorded(
                    "create-retention",
                    lambda: checked(
                        teacher.post("/api/v1/governance/retention-policies", json={"retention_days": 1}), 201
                    ),
                    lambda v: state.update(retention=v),
                )
            for key, row in material.items():
                if key not in state["documents"]:
                    recorded(
                        "upload-" + key,
                        lambda row=row: checked(
                            teacher.post(
                                "/api/v1/materials/documents",
                                data={"course_id": state["course"]["id"]},
                                files={
                                    "file": (
                                        row["derived_name"],
                                        (root / "materials" / row["derived_name"]).read_bytes(),
                                        "application/pdf",
                                    )
                                },
                            ),
                            201,
                        ),
                        lambda v, key=key: state["documents"].update({key: v}),
                    )
                document = checked(
                    teacher.get("/api/v1/materials/documents/" + state["documents"][key]["id"])
                )
                if document["content_hash"] != row["derived_sha256"]:
                    raise ValueError("review document hash mismatch")
                if document["status"] != "active":
                    if state.get("prepared"):
                        raise ValueError(
                            "prepared review material no longer active; no automatic reactivation"
                        )
                    recorded(
                        "activate-material-" + key,
                        lambda document=document: checked(
                            teacher.post("/api/v1/materials/documents/" + document["id"] + "/activate")
                        ),
                        lambda v, key=key: state["documents"].update({key: v}),
                    )
            if state["activity"] is None:
                recorded(
                    "create-draft-activity",
                    lambda: checked(
                        teacher.post(
                            "/api/v1/governance/activities",
                            json={
                                "activity": {
                                    "course_id": state["course"]["id"],
                                    "name": "012 borradores — no disponible a participantes",
                                    "subject": "Ingeniería del Software",
                                    "objective": (
                                        "Revisión pendiente de contenido y enlace semántico; "
                                        "no tutor activado"
                                    ),
                                    "mode": "self_study",
                                    "language": "es",
                                    "max_turns": 30,
                                    "max_duration_seconds": 900,
                                    "retention_policy_id": state["retention"]["id"],
                                    "output_authorization_policy": (
                                        semantic_guided_policy("oralia-is-012")
                                        if semantic_policy
                                        else guided_policy("oralia-is-012")
                                    ).model_dump(mode="json"),
                                },
                                "model_id": "guided_controlled",
                                "material_versions": [
                                    {"document_id": d["id"], "version": d["version"]}
                                    for d in state["documents"].values()
                                ],
                                "mode_config": {
                                    "enabled_modes": (
                                        ["doubt_resolution", "guided_explanation"]
                                        if semantic_policy
                                        else [
                                            "doubt_resolution",
                                            "guided_explanation",
                                            "practice_questions",
                                            "concept_review",
                                        ]
                                    ),
                                    "summary_authorized": False,
                                    "retention_authorized": False,
                                    "practice_reveals_solution": False,
                                },
                            },
                        ),
                        201,
                    ),
                    lambda v: state.update(activity=v),
                )
            dbpath = root / "review.db"
            reader = create_engine(
                "sqlite://",
                creator=lambda: sqlite3.connect(
                    f"file:{dbpath.as_posix()}?mode=ro", uri=True, check_same_thread=False
                ),
            )
            bindings = {}
            try:
                with Session(reader) as db:
                    for key, document in state["documents"].items():
                        for derived_page, original_page in material[key]["pages"].items():
                            fragments = (
                                db.query(models.MaterialFragment)
                                .filter_by(
                                    document_id=document["id"],
                                    document_version=document["version"],
                                    location_ref="página " + derived_page,
                                    indexing_status="indexed",
                                )
                                .all()
                            )
                            if len(fragments) != 1:
                                raise ValueError("review source page needs an explicit fragment binding")
                            bindings[f"{key}:{original_page}"] = {
                                "document_id": document["id"],
                                "document_version": document["version"],
                                "fragment_id": fragments[0].id,
                            }
            finally:
                reader.dispose()
            graph = draft_graph(packet)
            existing = {
                u["id"]: u
                for u in checked(
                    teacher.get(
                        "/api/v1/governance/teaching-units", params={"course_id": state["course"]["id"]}
                    )
                )
            }
            for key, identifier in state["units"].items():
                current = existing.get(identifier)
                if (
                    current is None
                    or current["status"] != "draft"
                    or current["reviewed_content"] != graph[key]["unit"]["draft_content"]
                ):
                    raise ValueError("prepared draft changed; no overwrite or automatic publication")
                _, expected = next_draft_input(
                    graph,
                    {k: v for k, v in state["units"].items() if k != key},
                    state["course"]["id"],
                    state["activity"]["id"],
                    bindings,
                )
                values = expected.model_dump(mode="json")
                if any(current.get(name) != value for name, value in values.items()):
                    raise ValueError("prepared draft binding changed; no overwrite")
            while True:
                item = next_draft_input(
                    graph, state["units"], state["course"]["id"], state["activity"]["id"], bindings
                )
                if item is None:
                    break
                key, payload = item

                def store(value, key=key):
                    if value["status"] != "draft":
                        raise ValueError("API returned non-draft teaching unit")
                    state["units"][key] = value["id"]

                recorded(
                    "create-unit-" + key,
                    lambda payload=payload: checked(
                        teacher.post(
                            "/api/v1/governance/teaching-units", json=payload.model_dump(mode="json")
                        ),
                        201,
                    ),
                    store,
                )
            activities = checked(teacher.get("/api/v1/governance/activities"))
            current = next(a for a in activities if a["id"] == state["activity"]["id"])
            if current["status"] != "draft":
                raise ValueError("review activity must remain draft")
            sample = next(iter(state["units"].values()))
            denied = teacher.post(
                "/api/v1/governance/teaching-units/" + sample + "/publish", json={"reviewed": False}
            )
            if denied.status_code != 409:
                raise ValueError("explicit-review gate did not reject publication")
            guest = TestClient(app, base_url="http://127.0.0.1")
            try:
                anonymous = guest.get(
                    "/api/v1/governance/teaching-units", params={"course_id": state["course"]["id"]}
                )
                if anonymous.status_code not in {401, 403}:
                    raise ValueError("teacher area allowed anonymous access")
                entry = guest.post(
                    "/api/v1/sessions",
                    json={
                        "participant_code": "oralia-is-012",
                        "activity_configuration_id": state["activity"]["id"],
                    },
                )
                if entry.status_code not in {401, 403, 409}:
                    raise ValueError("draft review activity accepted participant entry")
            finally:
                guest.close()
            state.update(
                {
                    "prepared": True,
                    "unit_count": len(state["units"]),
                    "participant_available": False,
                    "human_review": "pending",
                    "gate_checks": {
                        "publication_without_review": denied.status_code,
                        "anonymous_teacher_read": anonymous.status_code,
                        "participant_entry": entry.status_code,
                    },
                }
            )
            save(journal, state)
        finally:
            checked(teacher.post("/api/v1/auth/logout"))
    return {
        "root": str(root),
        "course_id": state["course"]["id"],
        "activity_id": state["activity"]["id"],
        "documents": len(state["documents"]),
        "units": len(state["units"]),
        "activity_status": "draft",
        "unit_status": "draft",
        "teacher_review": "pending",
        "participant_available": False,
    }


def main():
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--semantic-policy", action="store_true", help="Prepare a separate draft policy profile"
    )
    args = parser.parse_args()
    from oralia.course_dialogue.__main__ import lab_root
    from oralia.course_study.__main__ import WORKSPACE, owned_lock

    if "oralia.infrastructure.db.engine" in sys.modules:
        raise RuntimeError("review preparation requires a new Python process")
    from oralia.course_dialogue.corpus import SELECTION, SOURCE_ROOT, load_catalog
    from oralia.course_dialogue.draft_dialogue import DraftCurriculum

    catalog = load_catalog()
    curriculum = DraftCurriculum(catalog=catalog)
    fingerprint = packet_fingerprint(curriculum.packet, semantic_policy=args.semantic_policy)
    lab = lab_root(WORKSPACE)
    with owned_lock(lab):
        root = review_root(lab, fingerprint)
        if args.semantic_policy:
            original = lab / ("review-" + packet_fingerprint(curriculum.packet)[:12])
            if not original.is_dir():
                raise ValueError("prepare the ordinary review first; its verified PDF bytes are required")
            review_root(lab, packet_fingerprint(curriculum.packet))
            reuse_selected_materials(
                root / "materials", original / "materials", catalog, SELECTION, SOURCE_ROOT
            )
        for name in ["tmp", "vector_store"]:
            (root / name).mkdir(exist_ok=True)
        for key in list(os.environ):
            if key.startswith(("ORALIA_", "VITE_")):
                del os.environ[key]
        os.environ.update(
            {
                "ORALIA_DB_URL": f"sqlite:///{(root/'review.db').as_posix()}",
                "ORALIA_VECTOR_STORE_PATH": str(root / "vector_store"),
                "ORALIA_ADMIN_SECRET": secrets.token_urlsafe(32),
                "ORALIA_ALLOW_LAN": "0",
                "HF_HUB_OFFLINE": "1",
                "TRANSFORMERS_OFFLINE": "1",
                "HF_HUB_DISABLE_TELEMETRY": "1",
                "ANONYMIZED_TELEMETRY": "False",
                "TEMP": str(root / "tmp"),
                "TMP": str(root / "tmp"),
                "HTTP_PROXY": "http://127.0.0.1:9",
                "HTTPS_PROXY": "http://127.0.0.1:9",
                "NO_PROXY": "127.0.0.1,localhost",
            }
        )
        import tempfile

        tempfile.tempdir = str(root / "tmp")
        print(
            "Preparando revisión propia por APIs normales; no se publican unidades ni se crean sesiones.",
            flush=True,
        )
        result = prepare(
            root, curriculum.packet, catalog, SELECTION, SOURCE_ROOT, semantic_policy=args.semantic_policy
        )
        print(json.dumps(result, ensure_ascii=False))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
