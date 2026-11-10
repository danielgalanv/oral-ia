"""Explicit local snapshots: shown answers and descriptive counts, never grading or raw drafts."""

import copy
import json
import re
from collections import Counter
from datetime import UTC, datetime


def session_report(session):
    session.validate()
    turns = []
    for number, row in enumerate(session.receipts.values(), 1):
        shown = bool(row["shown"])
        turns.append(
            {
                "number": number,
                "question": row["question"],
                "status": row["status"],
                "shown": shown,
                "answer": row.get("diagnostic_preview") if shown else None,
                "failure_code": row.get("failure_code"),
                "local_sources": (
                    [
                        {k: p[k] for k in ("filename", "page", "original_url")}
                        for p in row.get("retrieval", {}).get("passages", [])
                    ]
                    if shown
                    else []
                ),
                "internet_sources": copy.deepcopy(row.get("web_sources", [])) if shown else [],
            }
        )
    questions = Counter(" ".join(t["question"].split()).casefold() for t in turns)
    return {
        "format": "oralia-study-report/v1",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "session_code": session.report_id,
        "provider_kind": getattr(session.provider, "diagnostic_label", "disconnected"),
        "semantic_support": "unverified",
        "publication_allowed": False,
        "course": session.binding[2],
        "activity": session.binding[3],
        "package": session.binding[0],
        "retrieval_revision": session.binding[1],
        "counts": {
            "completed_attempts": len(turns),
            "shown_answers": sum(t["shown"] for t in turns),
            "shown_answers_with_internet": sum(bool(t["internet_sources"]) for t in turns),
            "unshown_attempts": sum(not t["shown"] for t in turns),
        },
        "repeated_questions": [{"question_normalized": q, "count": n} for q, n in questions.items() if n > 1],
        "limitations": [
            "Descriptive observations, not learning outcomes or student assessment.",
            "No semantic topic classification; repeated questions use case/whitespace normalization only.",
            "Only explicitly shown answers; no raw drafts, reasoning traces or audio.",
            "Downloaded copies are not deleted when the application session closes.",
        ],
        "turns": turns,
    }


def fenced(text):
    longest = max((len(m[0]) for m in re.finditer(r"`+", text)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}text\n{text}\n{fence}"


def markdown_report(report):
    lines = [
        "# ORALIA — registro descriptivo de autoestudio",
        f"Sesión: {report['session_code']}",
        f"Generado: {report['generated_at_utc']}",
        "Proveedor registrado (no es una acreditación de calidad):",
        fenced(report["provider_kind"]),
        "Sin calificación, rúbrica, inferencia de aprendizaje o audio.",
        "La copia descargada no se borra al finalizar la sesión.",
        fenced(json.dumps(report["counts"], ensure_ascii=False, indent=2)),
    ]
    for turn in report["turns"]:
        lines.extend(
            [
                f"## Intercambio {turn['number']}",
                "Pregunta",
                fenced(turn["question"]),
                "Respuesta mostrada" if turn["shown"] else "Sin respuesta confirmada como mostrada",
                fenced(turn["answer"] or ""),
                "Fuentes consultadas",
                fenced(
                    json.dumps(
                        {"locales": turn["local_sources"], "internet": turn["internet_sources"]},
                        ensure_ascii=False,
                        indent=2,
                    )
                ),
            ]
        )
    return "\n\n".join(lines) + "\n"
