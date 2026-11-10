import socket

import pytest

from oralia.demo.resources import DemoError, DemoPaths, check_ports, child_environment


def test_paths_reject_unmarked_data_and_links_and_reset_cancellation(tmp_path):
    paths = DemoPaths(tmp_path)
    paths.root.mkdir()
    (paths.root / "important.txt").write_text("do not touch")
    with pytest.raises(DemoError):
        paths.initialize()
    assert (paths.root / "important.txt").read_text() == "do not touch"


def test_environment_isolated_and_web_never_receives_credentials(tmp_path, monkeypatch):
    monkeypatch.setenv("ORALIA_DB_URL", "sqlite:///habitual.db")
    monkeypatch.setenv("ORALIA_ALLOW_LAN", "1")
    monkeypatch.setenv("ORALIA_ADMIN_SECRET", "habitual-secret")
    paths = DemoPaths(tmp_path)
    env = child_environment(paths, 5180, secret="secret-for-demo-only")
    assert paths.root.as_posix() in env["ORALIA_DB_URL"]
    assert env["ORALIA_ALLOW_LAN"] == "0"
    assert env["HF_HUB_OFFLINE"] == "1"
    assert env["ORALIA_ADMIN_SECRET"] == "secret-for-demo-only"
    assert "ORALIA_ADMIN_SECRET" not in child_environment(paths, 5180)
    assert "secret-for-demo-only" not in repr(paths)


def test_occupied_port_is_never_replaced_or_closed():
    with socket.socket() as server:
        server.bind(("127.0.0.1", 0))
        server.listen()
        port = server.getsockname()[1]
        with pytest.raises(DemoError, match="ocupado"):
            check_ports(port, port + 1 if port < 65535 else port - 1)
        assert server.getsockname()[1] == port


def test_missing_embedding_offers_text_without_network_or_fake_sources(monkeypatch):
    from oralia.demo.resources import check_embeddings
    from oralia.infrastructure.embeddings.sentence_transformer_adapter import (
        SentenceTransformerEmbeddingAdapter,
    )

    def absent(_self, _texts):
        raise OSError("injected missing local cache")

    monkeypatch.setattr(SentenceTransformerEmbeddingAdapter, "embed", absent)
    with pytest.raises(DemoError, match="TextOnly"):
        check_embeddings()
