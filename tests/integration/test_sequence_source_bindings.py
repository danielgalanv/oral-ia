"""All proposal formats must retain literal witnesses for copied context units."""

import json
import os
from pathlib import Path

import pytest

from tests.dialogue.package_fixture import prepare_package


@pytest.mark.skipif(not os.environ.get("ORALIA_SEQUENCE_BINDINGS"), reason="explicit four-format binding")
def test_sequence_units_bind_in_all_four_formats(app_client):
    output = Path(os.environ["ORALIA_SEQUENCE_BINDINGS"])
    output.mkdir(parents=True, exist_ok=False)
    records = []
    for stream in ["agua-docx", "programa-docx", "programa-pptx", "datos-pdf"]:
        try:
            pack = prepare_package(app_client, stream, technical_publish=True, policy_version=4)
            assert len(pack["witnesses"]) == pack["technical_units"]
            for witness in pack["witnesses"].values():
                assert witness["source_refs"] and witness["normalized_quote"]
                assert witness["human_review"].startswith("pending")
                assert all(
                    ref["document_id"] in {d["id"] for d in pack["documents"].values()}
                    for ref in witness["source_refs"]
                )
            if stream == "programa-pptx":
                assert (
                    pack["witnesses"]["programa-validacion-storage-boundary"]["source_role"] == "supplement"
                )
            records.append({"stream": stream, "passed": True, "witnesses": pack["witnesses"]})
        except (AssertionError, ValueError) as error:
            records.append(
                {"stream": stream, "passed": False, "error_type": type(error).__name__, "error": str(error)}
            )
        (output / (stream + ".json")).write_text(
            json.dumps(records[-1], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    summary = {
        "formats": 4,
        "passed": sum(r["passed"] for r in records),
        "failures": [r for r in records if not r["passed"]],
    }
    (output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    assert summary["passed"] == 4, summary["failures"]
