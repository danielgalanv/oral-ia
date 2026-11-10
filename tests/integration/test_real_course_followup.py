"""Observe a curriculum followup; no invented response replaces the actual API."""

import json
import os
from pathlib import Path

import pytest

from oralia.course_study.preparation import RECIPIENT, checked, prepare


@pytest.mark.skipif(not os.environ.get("ORALIA_REAL_COURSE_FOLLOWUP"), reason="explicit real course followup")
def test_client_method_followup(app_client, monkeypatch):
    from oralia.domain.materials import query_excerpt

    calls = []
    original = query_excerpt.select_query_excerpts

    def observe(evidence, query):
        items = list(evidence)
        result = original(items, query)
        calls.append(
            {
                "query": query,
                "evidence": [item.model_dump() if hasattr(item, "model_dump") else item for item in items],
                "selected_ids": [span.fragment_id for span in result],
            }
        )
        return result

    monkeypatch.setattr(query_excerpt, "select_query_excerpts", observe)
    output = Path(os.environ["ORALIA_REAL_COURSE_FOLLOWUP"])
    output.mkdir(parents=True, exist_ok=False)
    prepared = prepare(app_client)
    session = checked(
        app_client.post(
            "/api/v1/sessions",
            json={"participant_code": RECIPIENT, "activity_configuration_id": prepared["activity_id"]},
        ),
        201,
    )
    sid = session["session_id"]
    observations = []
    try:
        for text in ["¿Qué significa validar los requisitos?", "¿Cómo lo haríamos con el cliente?"]:
            response = app_client.post(f"/api/v1/sessions/{sid}/study-turns", json={"text": text})
            observations.append({"input": text, "http": response.status_code, "actual": response.json()})
        (output / "conversation.json").write_text(
            json.dumps(
                {"preparation": prepared, "observations": observations, "human_review": "pending"},
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        (output / "selection-observation.json").write_text(
            json.dumps(calls, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        answer = observations[-1]["actual"].get("output_text") or ""
        assert "Reuniones" in answer and "prototipado" in answer
        assert not observations[-1]["actual"].get("blocked")
    finally:
        app_client.post(f"/api/v1/sessions/{sid}/study-end", json={"retain": False, "scope": []})
