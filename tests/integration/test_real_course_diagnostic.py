"""Transparent observation of the preserved external first preparation."""

import json
import os
import runpy
from pathlib import Path

import pytest


@pytest.mark.skipif(
    not os.environ.get("ORALIA_REAL_COURSE_DIAGNOSTIC"), reason="explicit local source diagnostic"
)
def test_observe_preserved_preparation(app_client, monkeypatch):
    from oralia.application.orchestration import self_study_agency_composer as composer
    from oralia.domain.agents.grounding_verifier_agent import GroundingVerifierAgent

    output = Path(os.environ["ORALIA_REAL_COURSE_DIAGNOSTIC"])
    output.mkdir(parents=True, exist_ok=False)
    records = []
    grounding = GroundingVerifierAgent.execute
    snapshot = composer.build_authorization_snapshot
    builder = composer.build_output_proposal
    decide = composer._decide_study_output

    async def observe_grounding(self, request, cancellation):
        result = await grounding(self, request, cancellation)
        records.append({"component": "grounding", "input": request.input, "output": result.output})
        return result

    def observe_snapshot(*args, **kwargs):
        try:
            result = snapshot(*args, **kwargs)
        except Exception as exc:
            records.append({"component": "snapshot", "error_type": type(exc).__name__, "error": str(exc)})
            raise
        records.append({"component": "snapshot", "value": result.model_dump(mode="json")})
        return result

    def observe_builder(*args, **kwargs):
        result = builder(*args, **kwargs)
        records.append({"component": "builder", "value": result.model_dump(mode="json")})
        return result

    async def observe_decide(*args, **kwargs):
        records.append(
            {"component": "final_candidate", "text": kwargs["text"], "fragments": kwargs["fragments_used"]}
        )
        result = await decide(*args, **kwargs)
        records.append({"component": "decision", "value": repr(result)})
        return result

    monkeypatch.setattr(GroundingVerifierAgent, "execute", observe_grounding)
    monkeypatch.setattr(composer, "build_authorization_snapshot", observe_snapshot)
    monkeypatch.setattr(composer, "build_output_proposal", observe_builder)
    monkeypatch.setattr(composer, "_decide_study_output", observe_decide)
    namespace = runpy.run_path(
        "materiales/docente/asignatura-real-20261021/test_autoestudio_extractivo_diagnostico.py"
    )
    original = namespace["test_observe_extractive_self_study"]
    original.__globals__["ROOT"] = output
    try:
        original(app_client)
    finally:
        (output / "observation.json").write_text(
            json.dumps(records, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
        )
    assert any(r["component"] == "final_candidate" for r in records)
