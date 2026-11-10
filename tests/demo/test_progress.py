import io
import socket
import time
from unittest.mock import Mock

import pytest

from oralia.demo import launcher
from oralia.demo.progress import Progress
from oralia.demo.resources import DemoError, DemoPaths


def test_long_stage_reports_elapsed_stops_and_never_completes_before_work():
    stream = io.StringIO()
    progress = Progress(stream=stream, interval=0.02)
    with progress.stage("dependencias"):
        time.sleep(0.07)
        assert "[ESPERA]" in stream.getvalue()
        assert "[OK]" not in stream.getvalue()
    value = stream.getvalue()
    assert "transcurridos" in value and "carga inicial" in value
    assert "%" not in value and "restante" not in value
    time.sleep(0.04)
    assert stream.getvalue() == value
    assert "[OK]" in value


@pytest.mark.parametrize("error", [KeyboardInterrupt(), DemoError("Puerto ocupado. Elija otro puerto.")])
def test_failure_and_cancel_stop_not_complete(error):
    stream = io.StringIO()
    progress = Progress(stream=stream, interval=0.01)
    with pytest.raises(type(error)):
        with progress.stage("dependencias"):
            raise error
    value = stream.getvalue()
    assert "[OK]" not in value
    assert "[CANCELADO]" in value if isinstance(error, KeyboardInterrupt) else "[FALLO]" in value
    time.sleep(0.03)
    assert value == stream.getvalue()


def test_unknown_error_is_honest_and_diagnostic_redacts_secret(tmp_path):
    paths = DemoPaths(tmp_path)
    paths.initialize()
    secret = "fictitious-credential-never-print-this"
    stream = io.StringIO()
    progress = Progress(stream=stream, paths=paths)
    progress.protect(secret)
    with pytest.raises(RuntimeError):
        with progress.stage("preparacion"):
            raise RuntimeError(secret)
    assert "causa no determinada" in stream.getvalue()
    log = (paths.root / "logs/startup.log").read_text(encoding="utf-8")
    assert "RuntimeError" in log and "[OCULTO]" in log
    assert secret not in stream.getvalue() + log


@pytest.mark.parametrize("text_only", [False, True])
def test_preflight_real_order_and_text_only(monkeypatch, tmp_path, text_only):
    calls = []
    monkeypatch.setattr(launcher, "dependencies", lambda: calls.append("dependencies"))
    monkeypatch.setattr(launcher, "check_ports", lambda *_: calls.append("ports"))
    monkeypatch.setattr(launcher, "check_embeddings", lambda: calls.append("embeddings"))
    stream = io.StringIO()
    result = launcher.check(DemoPaths(tmp_path), text_only=text_only, progress=Progress(stream=stream))
    assert calls == ["dependencies", "ports"] + ([] if text_only else ["embeddings"])
    assert ("embeddings locales" in stream.getvalue()) is not text_only
    assert "DEMO LISTA" not in stream.getvalue()
    assert result["api"] == "http://127.0.0.1:8010"


def test_occupied_port_names_stage_and_does_not_request_secret(monkeypatch, tmp_path):
    monkeypatch.setattr(launcher, "dependencies", lambda: None)
    factory = Mock(return_value="secret-must-not-be-requested")
    with socket.socket() as server:
        server.bind(("127.0.0.1", 0))
        server.listen()
        api = server.getsockname()[1]
        with pytest.raises(DemoError, match="ocupado"):
            launcher.start(
                DemoPaths(tmp_path), secret_factory=factory, api_port=api, web_port=api - 1, text_only=True
            )
    factory.assert_not_called()


def test_cli_start_defers_secret_and_does_not_repeat_check(monkeypatch):
    from oralia.demo import __main__ as cli

    monkeypatch.setattr("sys.argv", ["demo", "start", "--text-only", "--no-browser"])
    monkeypatch.setenv("ORALIA_DEMO_ADMIN_SECRET", "fictitious-process-only-credential")
    check = Mock(side_effect=AssertionError("duplicate preflight"))
    start = Mock()
    monkeypatch.setattr(launcher, "check", check)
    monkeypatch.setattr(launcher, "start", start)
    assert cli.main() == 0
    check.assert_not_called()
    kwargs = start.call_args.kwargs
    assert kwargs["secret_factory"]() == "fictitious-process-only-credential"
    assert kwargs["text_only"] and kwargs["no_browser"]


def test_cli_check_keeps_stdout_json_without_credential_or_servers(monkeypatch, capsys, tmp_path):
    import json

    from oralia.demo import __main__ as cli

    monkeypatch.setattr("sys.argv", ["demo", "check", "--text-only", "--workspace", str(tmp_path)])
    monkeypatch.setattr(launcher, "dependencies", lambda: None)
    monkeypatch.setattr(launcher, "check_ports", lambda *_: None)
    monkeypatch.setattr(
        cli.secrets, "token_urlsafe", Mock(side_effect=AssertionError("credential requested"))
    )
    monkeypatch.setattr(launcher, "start", Mock(side_effect=AssertionError("server started")))
    assert cli.main() == 0
    output = capsys.readouterr()
    assert json.loads(output.out)["profile"] == "text_only: sin fuentes"
    assert "[INICIO]" in output.err and "embeddings" not in output.err


def test_readiness_cancel_cleans_owned_children_and_no_false_ready(monkeypatch, tmp_path, capsys):
    with socket.socket() as first, socket.socket() as second:
        first.bind(("127.0.0.1", 0))
        second.bind(("127.0.0.1", 0))
        api, web = first.getsockname()[1], second.getsockname()[1]
    monkeypatch.setattr(launcher, "_json_at", Mock(side_effect=KeyboardInterrupt))
    launcher.start(
        DemoPaths(tmp_path),
        secret="fictitious-long-enough-credential",
        api_port=api,
        web_port=web,
        text_only=True,
        no_browser=True,
    )
    launcher.check_ports(api, web)
    output = capsys.readouterr()
    assert "[CANCELADO]" in output.err
    assert "DEMO LISTA" not in output.out
    assert not (DemoPaths(tmp_path).root / "run.json").exists()
