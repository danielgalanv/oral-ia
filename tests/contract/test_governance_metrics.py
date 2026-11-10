def test_aggregate_metrics_mark_missing_values_and_catalog_is_local(app_client):
    response = app_client.get("/api/v1/governance/metrics")
    assert response.status_code == 200
    body = response.json()
    assert body["scope"] == "system_aggregate"
    assert body["latency_ms_mean"] is None
    assert body["missing"]["perceived_usefulness"] == "not_collected"
    assert "participant_code" not in str(body)
    catalog = app_client.get("/api/v1/governance/catalog")
    assert catalog.status_code == 200
    assert "deterministic" in catalog.json()["models"]
    assert "constitutional-control" in catalog.json()["compositions"]["oral_defense"]


def test_index_status_is_read_only_and_does_not_claim_integrity(app_client, tmp_path, monkeypatch):
    monkeypatch.setenv("ORALIA_VECTOR_STORE_PATH", str(tmp_path))
    missing = app_client.get("/api/v1/governance/catalog").json()["index_status"]
    assert missing["status"] == "not_initialized"
    (tmp_path / "index_version.json").write_text('{"version": 3}', encoding="utf-8")
    observed = app_client.get("/api/v1/governance/catalog").json()["index_status"]
    assert observed["version"] == "3" and observed["integrity_verified"] is False
    (tmp_path / "index_version.json").write_text("broken metadata", encoding="utf-8")
    assert (
        app_client.get("/api/v1/governance/catalog").json()["index_status"]["status"]
        == "metadata_unavailable"
    )
    assert not (tmp_path / "chroma.sqlite3").exists()
