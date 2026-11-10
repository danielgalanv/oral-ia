"""Fictitious fixtures via existing material/publication services, no cognitive bypass."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from unittest.mock import patch

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from docx import Document
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from oralia.application.commands.activate_material import activate_material
from oralia.application.commands.create_activity import ActivityConfigurationInput
from oralia.application.commands.ingest_material import ingest_material
from oralia.application.services.activity_governance_service import create_managed_activity, publish_activity
from oralia.demo.resources import DemoError, DemoPaths, child_environment, write_json
from oralia.domain.policies.output_authorization_policy import (
    AllowedScope,
    DisclosureRule,
    OutputAuthorizationPolicy,
    TemplateReference,
)
from oralia.domain.policies.output_template_catalog import DEFAULT_OUTPUT_TEMPLATE_CATALOG
from oralia.infrastructure.db import models
from oralia.infrastructure.db.base import Base
from oralia.infrastructure.db.engine import build_engine

PARTICIPANT = "demo-007"
COURSE = "70000000-0000-0000-0000-000000000001"
RETENTION = "70000000-0000-0000-0000-000000000002"
MATERIAL = "El agua hierve a 100 grados. El agua líquida puede pasar a vapor al calentarse."


def migration_config(paths):
    config = Config()
    config.set_main_option(
        "script_location", str(Path(__file__).resolve().parents[1] / "infrastructure/db/migrations")
    )
    config.set_main_option("sqlalchemy.url", paths.db_url)
    return config


def verify_schema(paths):
    engine = build_engine(paths.db_url)
    try:
        with engine.connect() as connection:
            current = MigrationContext.configure(connection).get_current_revision()
        if current != ScriptDirectory.from_config(migration_config(paths)).get_current_head():
            raise DemoError(
                "Esquema demo no está actualizado. Vuelva a arrancar para aplicar migraciones solo a demo."
            )
        inspector = inspect(engine)
        if set(Base.metadata.tables) - set(inspector.get_table_names()):
            raise DemoError(
                "Esquema demo incompleto; faltan tablas. Revise migraciones o use Reset confirmado."
            )
        for name, table in Base.metadata.tables.items():
            if set(table.columns.keys()) - {column["name"] for column in inspector.get_columns(name)}:
                raise DemoError(
                    "Esquema demo incompleto; faltan columnas. Use Reset confirmado tras revisar datos demo."
                )
    finally:
        engine.dispose()


def output_policy(mode):
    # Manual, versioned fixture authorization; does not grant participant consent.
    entries = [
        e
        for e in DEFAULT_OUTPUT_TEMPLATE_CATALOG.entries
        if e.message_type == "normal" and e.template_id.startswith("defense-") == (mode == "oral_defense")
    ]
    disclosures = [("generated_defense", "defense-agency"), ("defense_summary", "persisted_session_facts")]
    if mode != "oral_defense":
        disclosures = [("texto", "activity_material")]
    return OutputAuthorizationPolicy(
        schema_version=1,
        policy_id=f"demo007-{mode}",
        policy_version=1,
        allowed_recipients=(PARTICIPANT,),
        allowed_disclosures=tuple(
            DisclosureRule(category=c, provenance=p, recipient=PARTICIPANT) for c, p in disclosures
        ),
        allowed_scopes=AllowedScope(
            topics=tuple(dict.fromkeys(e.topic_ref for e in entries)),
            purposes=tuple(dict.fromkeys(e.purpose_ref for e in entries)),
            actions=tuple(dict.fromkeys(e.action_ref for e in entries)),
        ),
        general_knowledge_allowed=False,
        allowed_templates=tuple(TemplateReference(e.template_id, e.version) for e in entries),
        allowed_operational_messages=(("safe-technical-fallback", 1),),
    )


def prepare(paths: DemoPaths, *, text_only=False):
    paths.initialize()
    profile = {"schema": 1, "revision": 1, "profile": "text_only" if text_only else "full"}
    state = paths.root / "seed-state.json"
    if state.exists() and json.loads(state.read_text(encoding="utf-8")) != profile:
        raise DemoError("El perfil demo ha cambiado. Use -Action Reset con confirmación antes de cambiarlo.")
    write_json(state, profile)
    # Dedicated preparation subprocess in normal use; scoped environment also isolates unit tests.
    with patch.dict("os.environ", child_environment(paths, 5180), clear=True):
        command.upgrade(migration_config(paths), "head")
        verify_schema(paths)
        engine = build_engine(paths.db_url)
        try:
            with Session(engine, expire_on_commit=False) as db:
                manifest_path = paths.root / "fixtures.json"
                if manifest_path.exists():
                    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                    for activity in manifest["activities"]:
                        meta = db.get(models.ActivityGovernance, activity["id"])
                        if meta is None or meta.status != "active":
                            raise DemoError(
                                "Actividad demo modificada. Revise en Gobierno o use Reset explícito."
                            )
                    return manifest
                if db.get(models.Course, COURSE) is None:
                    db.add(
                        models.Course(
                            id=COURSE, name="Curso ficticio: cambios del agua", subject_code="DEMO007"
                        )
                    )
                    db.flush()
                if db.get(models.RetentionPolicy, RETENTION) is None:
                    db.add(
                        models.RetentionPolicy(
                            id=RETENTION,
                            version=1,
                            content_scope="transcript,summary",
                            retention_days=1,
                            access_scope="local_teacher",
                            purge_rule="manual",
                        )
                    )
                    db.flush()
                material_file = paths.root / "files/agua-demo.docx"
                if not material_file.exists():
                    document = Document()
                    document.add_paragraph(MATERIAL)
                    document.save(material_file)
                content = material_file.read_bytes()
                document = (
                    db.query(models.MaterialDocument)
                    .filter_by(course_id=COURSE, filename=material_file.name)
                    .one_or_none()
                )
                if document is None:
                    if text_only:
                        document = models.MaterialDocument(
                            course_id=COURSE,
                            filename=material_file.name,
                            content_hash=hashlib.sha256(content).hexdigest(),
                            mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            size_bytes=len(content),
                            status="pending",
                            error_detail="demo text_only: embeddings no preparados",
                        )
                        db.add(document)
                        db.flush()
                    else:
                        document = ingest_material(
                            db, course_id=COURSE, filename=material_file.name, content=content
                        )
                        activate_material(db, document.id)
                refs = [] if text_only else [{"document_id": document.id, "version": document.version}]
                activities = []
                for mode, name in [
                    ("self_study", "Demo: autoestudio del agua"),
                    ("oral_defense", "Demo: defensa del agua"),
                ]:
                    activity = (
                        db.query(models.ActivityConfiguration)
                        .filter_by(course_id=COURSE, name=name)
                        .one_or_none()
                    )
                    if activity is None:
                        mode_config = (
                            {
                                "initial_questions": [
                                    "¿A qué temperatura hierve el agua?",
                                    "¿Cómo pasa el agua líquida a vapor?",
                                ],
                                "topics": ["agua"],
                                "summary_authorized": True,
                                "transcript_retention_authorized": True,
                            }
                            if mode == "oral_defense"
                            else {
                                "enabled_modes": ["doubt_resolution", "guided_explanation"],
                                "summary_authorized": True,
                                "retention_authorized": True,
                            }
                        )
                        activity = create_managed_activity(
                            db,
                            ActivityConfigurationInput(
                                course_id=COURSE,
                                name=name,
                                subject="Cambios del agua",
                                objective="Explicar cambios del agua usando el material ficticio",
                                mode=mode,
                                language="es",
                                max_turns=8,
                                max_duration_seconds=600,
                                retention_policy_id=RETENTION,
                                output_authorization_policy=output_policy(mode),
                            ),
                            model_id="deterministic",
                            material_versions=refs,
                            mode_config=mode_config,
                        )
                        publish_activity(db, activity.id)
                    activities.append({"id": activity.id, "name": activity.name, "mode": mode})
                db.commit()
                manifest = {
                    **profile,
                    "course_id": COURSE,
                    "material_id": document.id,
                    "material_sha256": hashlib.sha256(content).hexdigest(),
                    "activities": activities,
                    "participant_code": PARTICIPANT,
                    "generation": "deterministic",
                    "voice_validated": False,
                }
                write_json(manifest_path, manifest)
                return manifest
        finally:
            engine.dispose()
