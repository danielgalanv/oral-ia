"""Read-only document profile: real package, no embeddings or participant routes."""

import hashlib
import json
import shutil
import sys

import pytest
from fastapi.testclient import TestClient

from oralia.documentary.__main__ import MANIFEST, PACKAGE, confined, create_app, load_package


def test_package_provenance_and_coverage():
    manifest, pages = load_package(PACKAGE)
    assert manifest["available"] == 43
    assert len(manifest["documents"]) == 5
    assert not next(c for c in manifest["concepts"] if c["label"] == "INCOSE")["passages"]
    assert next(p for p in pages["docente-procedimiento"] if p["page"] == 13)["status"] == "cuarentena"
    assert next(p for p in pages["sommerville"] if p["page"] == 60)["status"] == "cuarentena"
    assert next(p for p in pages["nasa-seh"] if p["page"] == 212)["status"] == "cuarentena"
    assert next(p for p in pages["nasa-seh"] if p["page"] == 210)["printed_page"] == 200


def test_access_close_reenter_and_no_participant_routes():
    with TestClient(create_app(), base_url="http://127.0.0.1") as client:
        assert client.get("/api/v1/documentary").status_code == 401
        assert client.post("/documentary/enter").status_code == 200
        assert client.get("/api/v1/documentary").status_code == 200
        result = client.get("/api/v1/documentary/docente-procedimiento/pages")
        assert "Comprensible" in result.text
        assert client.post("/api/v1/sessions", json={}).status_code == 405
        assert client.post("/api/v1/materials", json={}).status_code == 405
        assert client.post("/documentary/leave").status_code == 200
        assert client.get("/api/v1/documentary/docente-procedimiento/original").status_code == 401
        assert client.post("/documentary/enter").status_code == 200
        assert client.get("/api/v1/documentary").status_code == 200


def test_origin_host_and_unknown_document_rejected():
    with TestClient(create_app(), base_url="http://127.0.0.1") as client:
        assert (
            client.post("/documentary/enter", headers={"Origin": "https://external.example"}).status_code
            == 403
        )
        assert client.post("/documentary/enter", headers={"Host": "external.example"}).status_code == 403
        client.post("/documentary/enter")
        assert client.get("/api/v1/documentary/unknown/original").status_code == 404
        assert client.get("/api/v1/documentary/nasa-seh/preview/1").status_code == 404


def test_original_and_html_archives():
    with TestClient(create_app(), base_url="http://127.0.0.1") as client:
        client.post("/documentary/enter")
        original = client.get("/api/v1/documentary/docente-procedimiento/original")
        assert (
            hashlib.sha256(original.content).hexdigest()
            == "27a7defe182ecdc4c209a56fd7c220f120ed02c997c2c898dc292bcb13e4e409"
        )
        archive = client.get("/api/v1/documentary/nasa-swe055/original")
        assert "attachment" in archive.headers["content-disposition"]
        assert "connect-src 'self'" in archive.headers["content-security-policy"]
        assert (
            client.get("/api/v1/documentary/docente-procedimiento/preview/11").headers["content-type"]
            == "image/png"
        )


def test_package_rejects_changed_original(tmp_path):
    source = PACKAGE / MANIFEST
    manifest = json.loads(source.read_text(encoding="utf-8"))
    doc = manifest["documents"][0]
    doc["original"] = "wrong.pdf"
    (tmp_path / "wrong.pdf").write_bytes(b"changed")
    (tmp_path / MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="Original hash mismatch"):
        load_package(tmp_path)


def test_package_rejects_changed_extraction(tmp_path):
    manifest = json.loads((PACKAGE / MANIFEST).read_text(encoding="utf-8"))
    manifest["documents"] = manifest["documents"][:1]
    doc = manifest["documents"][0]
    doc["original"] = "original.pdf"
    shutil.copyfile(PACKAGE / "originales/5 - Requisitos.pdf", tmp_path / "original.pdf")
    doc["extraction"] = "changed.json"
    (tmp_path / "changed.json").write_text("[]", encoding="utf-8")
    (tmp_path / MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="Extraction hash mismatch"):
        load_package(tmp_path)


def test_paths_cannot_escape_package(tmp_path):
    with pytest.raises(ValueError):
        confined(tmp_path, "../pyproject.toml")


def test_profile_import_does_not_load_models():
    import subprocess

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import sys; from oralia.documentary.__main__ import create_app; "
                "create_app(); assert not any(n in sys.modules for n in "
                "['torch','transformers','sentence_transformers','chromadb'])"
            ),
        ],
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
