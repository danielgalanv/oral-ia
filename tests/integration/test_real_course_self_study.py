"""Real selected PDF, actual API/provider/verifiers, external corpus opt-in."""

import json
import os
from pathlib import Path

import pytest

from oralia.course_study.preparation import RECIPIENT, checked, prepare
from oralia.infrastructure.db import models
from tests.dialogue.package_fixture import ensure_owned_temporary


@pytest.mark.skipif(
    not os.environ.get("ORALIA_REAL_COURSE_RUN"), reason="explicit real-course source and evidence directory"
)
def test_real_course_conversation(app_client, monkeypatch):
    from oralia.infrastructure.generation.ollama_adapter import OllamaGenerationAdapter

    async def forbidden(*args, **kwargs):
        raise AssertionError("The deterministic course profile must not call a generative model")

    monkeypatch.setattr(OllamaGenerationAdapter, "generate", forbidden)
    ensure_owned_temporary(app_client, True)
    output = Path(os.environ["ORALIA_REAL_COURSE_RUN"])
    output.mkdir(parents=True, exist_ok=False)
    prepared = prepare(app_client)
    (output / "preparation.json").write_text(
        json.dumps(prepared, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    cases = json.loads(
        Path("tests/fixtures/materials/real-course-questions.json").read_text(encoding="utf-8")
    )[os.environ.get("ORALIA_REAL_COURSE_PARTITION", "development")]
    session = checked(
        app_client.post(
            "/api/v1/sessions",
            json={"participant_code": RECIPIENT, "activity_configuration_id": prepared["activity_id"]},
        ),
        201,
    )
    sid = session["session_id"]
    observations, failures = [], []
    try:
        for case in cases:
            response = app_client.post(f"/api/v1/sessions/{sid}/study-turns", json={"text": case["text"]})
            body = response.json()
            with app_client.__db_sessionmaker__() as db:
                state = db.get(models.Session, sid).status
                events = (
                    db.query(models.TraceEvent).filter_by(session_id=sid, turn_id=body.get("turn_id")).all()
                )
                trace = [{"event": e.event_type, "payload": e.payload} for e in events]
            observation = {
                "input": case["text"],
                "expected": case,
                "actual": body,
                "http": response.status_code,
                "session_status": state,
                "trace": trace,
            }
            observations.append(observation)
            text = body.get("output_text") or ""
            if response.status_code != 200 or body.get("blocked") or not text or state != "active":
                failures.append("No authorized active response: " + case["text"])
            for term in case.get("contains", []):
                if term.casefold() not in text.casefold():
                    failures.append("Missing source meaning: " + term)
            pages = [
                prepared["provenance"]["pages"].get(s["location_ref"].split()[-1])
                for s in body.get("sources", [])
            ]
            if set(case.get("original_pages", [])) - set(pages):
                failures.append("Missing source page: " + str(pages))
            if case.get("limit") and body.get("dialogue_action") != "acknowledge_missing_info":
                failures.append("Unsupported example was not limited")
            if any(x in text.lower() for x in ["evaporación", "mil", "media aritmética", "rango numérico"]):
                failures.append("Unrelated old semantics")
            (output / "conversation.json").write_text(
                json.dumps(
                    {
                        "preparation": prepared,
                        "observations": observations,
                        "failures": failures,
                        "human_review": "pending",
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            if state != "active":
                break  # Never simulate the rest of a closed session.
        closed = app_client.post(f"/api/v1/sessions/{sid}/study-end", json={"retain": False, "scope": []})
        if closed.status_code != 200 or closed.json().get("status") != "closed_voluntary":
            failures.append("Voluntary closure not confirmed")
        (output / "closure.json").write_text(
            json.dumps(
                {
                    "http": closed.status_code,
                    "actual": closed.json(),
                    "kind": "own API closure, not academic success",
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
    finally:
        app_client.post(f"/api/v1/sessions/{sid}/study-end", json={"retain": False, "scope": []})
    assert len(observations) == len(cases) and not failures, failures
