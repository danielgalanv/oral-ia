"""Open, ephemeral exports built from consent-checked projections, never ORM dumps."""

from __future__ import annotations

import html
import json
import re
from copy import deepcopy

from sqlalchemy.orm import Session

from oralia.application.services.session_privacy_service import review_session
from oralia.infrastructure.db import models


def export_sessions(
    db: Session, session_ids: list[str], *, include_free_text=False, reviewed_free_text=False
):
    if not 1 <= len(session_ids) <= 100 or len(session_ids) != len(set(session_ids)):
        raise ValueError("export requires 1 to 100 distinct sessions")
    if include_free_text and not reviewed_free_text:
        raise ValueError("human review of free text is required")
    # Validate the complete selection first; no streaming of a permitted prefix.
    reviews = [review_session(db, session_id) for session_id in session_ids]
    aliases: dict[str, str] = {}
    counters: dict[str, int] = {}

    def alias(kind, value):
        if value is None:
            return None
        if value not in aliases:
            counters[kind] = counters.get(kind, 0) + 1
            aliases[value] = f"{kind}-{counters[kind]}"
        return aliases[value]

    def replace_ids(value):
        if isinstance(value, dict):
            result = {}
            for key, item in value.items():
                if key in {"id", "session_id", "turn_id", "transcript_id", "document_id", "family_id"}:
                    result[key] = alias(key.removesuffix("_id"), item)
                elif key == "participant_code":
                    continue
                else:
                    result[key] = replace_ids(item)
            return result
        if isinstance(value, list):
            return [replace_ids(item) for item in value]
        return value

    for session_id in session_ids:
        alias("participant", db.get(models.Session, session_id).participant_code)

    free_text_fields = {
        "input_text",
        "output_text",
        "raw_text",
        "corrections",
        "questions_asked",
        "topics_covered",
        "concepts_mentioned",
        "concepts_addressed",
        "location_ref",
    }

    def redact_known_identifiers(value, field=None):
        if isinstance(value, dict):
            return {key: redact_known_identifiers(item, key) for key, item in value.items()}
        if isinstance(value, list):
            return [redact_known_identifiers(item, field) for item in value]
        if isinstance(value, str) and field in free_text_fields:
            for original, replacement in sorted(aliases.items(), key=lambda item: -len(item[0])):
                value = re.sub(r"(?<!\w)" + re.escape(original) + r"(?!\w)", replacement, value)
        return value

    sessions = []
    for review in reviews:
        projection = deepcopy(review)
        projection["trace"] = [
            {"event_type": e["event_type"], "agent_id": e["agent_id"], "latency_ms": e["latency_ms"]}
            for e in projection["trace"]
        ]
        if not include_free_text:
            projection["turns"] = [{"turn_id": t["turn_id"]} for t in projection["turns"]]
            projection["transcripts"] = [
                {
                    "transcript_id": t["transcript_id"],
                    "turn_id": t["turn_id"],
                    "corrections_count": len(t["corrections"]),
                }
                for t in projection["transcripts"]
            ]
            summary = projection["summary"]
            projection["summary"] = {
                key: value
                for key, value in (summary or {}).items()
                if key in {"turn_count", "duration_seconds", "clarifications_count", "close_reason"}
            } or None
            projection["sources"] = [
                {"document_id": source["document_id"], "document_version": source["document_version"]}
                for source in projection["sources"]
            ]
        projection = replace_ids(projection)
        sessions.append(projection)
    sessions = redact_known_identifiers(sessions)
    bundle = {
        "schema_version": 1,
        "free_text_included": bool(include_free_text),
        "free_text_human_reviewed": bool(include_free_text and reviewed_free_text),
        "privacy_warning": (
            "Alias del lote; el texto libre puede contener información personal. "
            "No se garantiza anonimización."
        ),
        "sessions": sessions,
    }
    lines = ["# ORAL-IA — Exportación autorizada", "", bundle["privacy_warning"], ""]
    for session in sessions:
        lines += [
            f"## {session['session_id']}",
            "",
            f"Estado: {session['status']}. Scopes: {', '.join(session['scopes'])}.",
            "",
        ]
        for title, key in [
            ("Configuración y versiones", "configuration"),
            ("Transcripción", "turns"),
            ("Originales y correcciones de voz", "transcripts"),
            ("Resumen", "summary"),
            ("Fuentes", "sources"),
            ("Agentes", "agents"),
            ("Verificaciones", "verifications"),
            ("Trazabilidad e incidencias", "trace"),
        ]:
            rendered = html.escape(json.dumps(session[key], ensure_ascii=False, indent=2)).replace(
                "```", "\\u0060\\u0060\\u0060"
            )
            lines += [f"### {title}", "", "```text", rendered, "```", ""]
    return bundle, "\n".join(lines)
