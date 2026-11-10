"""Activity scope is explicit and independent of permission to fetch Internet pages."""

import json
from pathlib import Path

import pytest

from oralia.documentary.web_evidence import load_web_evidence


def test_scope_survives_web_disable_but_not_scope_change(tmp_path):
    root = Path(__file__).resolve().parents[2]
    config = json.loads(
        (
            root / "docs/audits/2026-11-03-study-controls-v3/resume-20261104/policy-requirements-lab-v4.json"
        ).read_text(encoding="utf8")
    )
    path = tmp_path / "policy.json"
    path.write_text(json.dumps(config), encoding="utf8")
    port = load_web_evidence(path)
    port.check_policy()
    port.check_activity_scope()
    config["policy"]["enabled"] = False
    path.write_text(json.dumps(config), encoding="utf8")
    port.check_activity_scope()
    with pytest.raises(ValueError):
        port.check_policy()
    config["activity_scope"]["version"] += 1
    path.write_text(json.dumps(config), encoding="utf8")
    with pytest.raises(ValueError):
        port.check_activity_scope()


def test_web_permission_is_not_itself_exclusive_course_scope(tmp_path):
    root = Path(__file__).resolve().parents[2]
    config = json.loads(
        (
            root / "docs/audits/2026-11-03-study-controls-v3/resume-20261104/policy-requirements-lab-v4.json"
        ).read_text(encoding="utf8")
    )
    del config["activity_scope"]
    path = tmp_path / "policy.json"
    path.write_text(json.dumps(config), encoding="utf8")
    port = load_web_evidence(path)
    port.check_policy()
    with pytest.raises(ValueError):
        port.check_activity_scope()
