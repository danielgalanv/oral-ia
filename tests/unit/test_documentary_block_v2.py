"""Real v2 corpus boundaries and reversible, explicit package selection."""

import hashlib
import json
import shutil
import subprocess
import sys

import pytest
from fastapi.testclient import TestClient

from oralia.documentary.__main__ import MANIFEST, PACKAGE, PACKAGES, create_app, load_package


def test_explicit_version_and_default_remain_separate():
    old, _ = load_package(PACKAGE)
    new, pages = load_package(*PACKAGES["v2"])
    assert old["package_id"].endswith("v1.1") and old["available"] == 43
    assert new["package_id"].endswith("v2") and new["available"] > 43
    assert new["predecessor"]["sha256"] == hashlib.sha256((PACKAGE / MANIFEST).read_bytes()).hexdigest()
    assert len(new["concepts"]) == 13
    assert all(
        r["qa_state"] != "no_revisado"
        for k in ["docente-requisitos", "docente-procedimiento"]
        for r in pages[k]
    )


def test_unextracted_figures_remain_blocked_and_original_ambiguity_visible():
    _, pages = load_package(*PACKAGES["v2"])
    req = {r["page"]: r for r in pages["docente-requisitos"]}
    assert req[4]["status"] == "disponible"
    assert req[44]["status"] == "cuarentena" and req[44]["qa_state"] == "fallo_extraccion"
    assert req[45]["status"] == "cuarentena"
    assert req[32]["derivation"].startswith("Lectura por columna")
    proc = {r["page"]: r for r in pages["docente-procedimiento"]}
    assert "Registrar problemas" in proc[13]["section"]
    assert "trazabilidad hacia atrás" in proc[13]["text"]
    assert "inversión" in proc[13]["reason"]
    assert len(proc[13]["context_required"]) == 2


def test_v2_local_access_originals_inert_html_and_close():
    root, name = PACKAGES["v2"]
    with TestClient(create_app(root, manifest_name=name), base_url="http://127.0.0.1") as client:
        assert client.get("/api/v1/documentary").status_code == 401
        client.post("/documentary/enter")
        assert "oralia_documentary_teacher" not in client.cookies
        catalog = client.get("/api/v1/documentary").json()
        assert catalog["package_id"].endswith("v2")
        for doc in catalog["documents"]:
            original = client.get(f"/api/v1/documentary/{doc['id']}/original")
            assert hashlib.sha256(original.content).hexdigest() == doc["sha256"]
        html = client.get("/api/v1/documentary/nasa-swe055/original")
        assert "attachment" in html.headers["content-disposition"]
        assert "connect-src 'self'" in html.headers["content-security-policy"]
        assert client.post("/api/v1/materials", json={}).status_code == 405
        assert client.post("/api/v1/sessions", json={}).status_code == 405
        client.post("/documentary/leave")
        assert client.get("/api/v1/documentary/docente-requisitos/preview/4").status_code == 401
        client.post("/documentary/enter")
        assert client.get("/api/v1/documentary/docente-requisitos/preview/4").status_code == 200


def test_every_concept_targets_available_unit_and_inventory_counts():
    root, _ = PACKAGES["v2"]
    manifest, pages = load_package(*PACKAGES["v2"])
    rows = {r["id"]: r for units in pages.values() for r in units}
    for doc in manifest["documents"]:
        units = pages[doc["id"]]
        assert len(units) == doc["extracted_units"]
        assert sum(r["status"] == "disponible" for r in units) == doc["available"]
        assert all(r["source_sha256"] == doc["sha256"] for r in units)
    coverage = json.loads((root / "coverage-v2.json").read_text(encoding="utf-8"))
    assert len(coverage) == 12 and all(c["after"] for c in coverage)
    for concept in manifest["concepts"]:
        for ref in concept["passages"]:
            assert rows[ref]["status"] == "disponible"
    assert not manifest["concepts"][-1]["passages"]  # No invented INCOSE acquisition.


def test_v2_rejects_changed_preview(tmp_path):
    root, name = PACKAGES["v2"]
    manifest, pages = load_package(root, name)
    doc = manifest["documents"][1]
    row = pages[doc["id"]][1]
    shutil.copyfile(root / doc["original"], tmp_path / "original.pdf")
    doc["original"] = "original.pdf"
    row["preview"] = "preview.png"
    (tmp_path / "preview.png").write_bytes(b"changed preview")
    data = json.dumps([row], ensure_ascii=False).encode()
    (tmp_path / "rows.json").write_bytes(data)
    doc["extraction"] = "rows.json"
    doc["extraction_sha256"] = hashlib.sha256(data).hexdigest()
    manifest["documents"] = [doc]
    manifest["concepts"] = []
    (tmp_path / name).write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="Preview hash mismatch"):
        load_package(tmp_path, name)


def test_package_versions_do_not_revoke_each_others_cookie():
    root, name = PACKAGES["v2"]
    with (
        TestClient(create_app(), base_url="http://127.0.0.1:8025") as old,
        TestClient(create_app(root, manifest_name=name), base_url="http://127.0.0.1:8024") as new,
    ):
        old.post("/documentary/enter")
        new.cookies.update(old.cookies)
        new.post("/documentary/enter")
        old.cookies.update(new.cookies)
        assert old.get("/api/v1/documentary").status_code == 200
        assert new.get("/api/v1/documentary").status_code == 200
        new.post("/documentary/leave")
        assert old.get("/api/v1/documentary").status_code == 200


def test_v2_process_has_no_model_imports():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; from oralia.documentary.__main__ import create_app, PACKAGES; "
            "r,n=PACKAGES['v2']; create_app(r, manifest_name=n); "
            "assert not any(k in sys.modules for k in "
            "['torch','transformers','sentence_transformers','chromadb'])",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
