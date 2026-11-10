"""Observation of the original 24 inputs under the opt-in navigation profile.

This is an exposed regression/audit, never a fresh reserve or human approval.
"""

import json
import os
from pathlib import Path

import pytest

from oralia.domain.dialogue.interpretation import normalized
from oralia.infrastructure.db import models
from tests.dialogue.api_fixture import prepare_guided

FIXTURES = Path(__file__).parents[1] / "dialogue/fixtures"
CASES = (
    json.loads((FIXTURES / "development.json").read_text(encoding="utf-8"))["cases"]
    + json.loads((FIXTURES / "acceptance-cycle-5/dialogues.json").read_text(encoding="utf-8"))["cases"]
)


@pytest.mark.skipif(
    not os.environ.get("ORALIA_SCREENLESS_AUDIT"), reason="explicit exposed 24-dialogue audit"
)
@pytest.mark.parametrize("case", CASES, ids=lambda case: case["case_id"])
def test_observe_original_inputs_without_visual_panels(app_client, case):
    folder = Path(os.environ["ORALIA_SCREENLESS_AUDIT"])
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / (case["case_id"] + ".json")
    assert not target.exists(), "preserve original observations"
    report = {
        "case_id": case["case_id"],
        "original_case": case,
        "observations": [],
        "profile": "guided_controlled",
        "navigation_policy": (
            "guided-screenless/v2" if os.environ.get("ORALIA_DIDACTIC_AUDIT") else "guided-screenless/v1"
        ),
        "reserve": False,
        "human_review": (
            "D01 prior reviewed version requires correction; this successor pending"
            if case["case_id"] == "D01"
            else "No evaluado"
        ),
        "audio_real": False,
    }
    prepared = prepare_guided(
        app_client,
        domain=case["domain"],
        mode=case["mode"],
        study_mode=case.get("study_mode"),
        screenless=True,
        pedagogy=bool(os.environ.get("ORALIA_DIDACTIC_AUDIT")),
    )
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/conversation-controls"
    try:
        for step, item in enumerate(case["steps"]):
            response = app_client.post(endpoint, json={"text": item["text"]})
            report["observations"].append(
                {
                    "step": step,
                    "input": item["text"],
                    "http_status": response.status_code,
                    "response": response.json(),
                }
            )
            target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            assert response.status_code == 200
            if normalized(item["text"]).startswith("confirmo: "):
                expected = normalized(item["text"])[10:]
                if expected in prepared["topics"]:
                    refs = response.json().get("dialogue_status", {}).get("rendered_unit_ids", [])
                    if refs:
                        with app_client.__db_sessionmaker__() as db:
                            assert {db.get(models.TeachingUnit, ref).topic_ref for ref in refs} == {expected}
                    else:
                        # A previously used protected question may be unavailable.
                        # A safe explicit limit must not be mistaken for topic substitution.
                        assert response.json()["dialogue_status"]["notice"] == "limited"
                        assert "no está disponible o permitido" in response.json()["output_text"]
    finally:
        # Outside the observed corpus: close only this synthetic session if still active.
        app_client.post(endpoint, json={"text": "terminar la sesión"})
        app_client.post(endpoint, json={"text": "confirmo cerrar"})
        report["teardown_is_not_a_participant_step"] = True
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
