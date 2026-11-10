"""Append-only log of the review notices shown to students, for later teacher evaluation.

One JSON line per notice (or failed review). It holds the student's question and the model's answer, so it
stays local; the teacher marks each entry with `scripts/avisos_docente.py`. Logging never breaks a turn.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

LOG_VERSION = "notice-log/v1"


def record_notice(path, request, answer, trace, notice, *, model=""):
    """Append one entry; returns its id, or None if nothing was written (no notice, or the disk refused)."""
    if not notice or path is None:
        return None
    units = {u["id"]: u["text"] for u in trace.get("answer_units", [])}
    flagged = [
        dict(
            use_id=c["use_id"],
            kind=c["kind"],
            verdict=c["verdict"],
            reason=c.get("reason", ""),
            unit_text=units.get(c["use_id"], ""),
        )
        for c in trace.get("checks", [])
        if c.get("verdict") == "incorrect"
    ]
    entry = dict(
        version=LOG_VERSION,
        id=uuid.uuid4().hex[:12],
        at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        question=getattr(request, "student_input", ""),
        answer=answer,
        sources=[e.fragment_id for e in request.evidence],
        status=trace.get("status"),
        notice_kinds=[i["kind"] for i in notice["items"]],
        reviewer_findings=flagged,
        reviewer_model=model,
    )
    try:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        return None
    return entry["id"]


def record_rejection(path, question, code, message, previous=None):
    """Append a refusal or clarification the filter gave instead of an answer, so the teacher can judge it.

    It uses the same file and shape as a notice (`kind: "rechazo"`); the teacher marks whether refusing was right.
    """
    if path is None:
        return None
    entry = dict(
        version=LOG_VERSION,
        id=uuid.uuid4().hex[:12],
        kind="rechazo",
        at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        question=question,
        previous_question=previous,
        answer=message,
        sources=[],
        status=code,
        notice_kinds=[code],
        reviewer_findings=[],
        reviewer_model="",
    )
    try:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        return None
    return entry["id"]
