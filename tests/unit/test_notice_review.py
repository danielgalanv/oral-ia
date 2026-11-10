"""Teacher review of the notice log: reading, marking and the local-only web page."""

import json

import pytest
from fastapi.testclient import TestClient

from oralia.documentary import notice_review
from oralia.documentary.notice_review_app import create_review_app


def entry(identifier, at, kinds=("contradiction",)):
    return dict(
        version="notice-log/v1",
        id=identifier,
        at=at,
        question="¿Qué es X?",
        answer="Respuesta.",
        sources=["d:1"],
        status="issues_found",
        notice_kinds=list(kinds),
        reviewer_findings=[dict(use_id="U1", kind=kinds[0], verdict="incorrect", reason="motivo", unit_text="texto")],
        reviewer_model="m",
    )


@pytest.fixture
def directory(tmp_path):
    lines = [entry("a1", "2026-11-06T10:00:00+00:00"), entry("b2", "2026-11-06T11:00:00+00:00", ("wrong_concept",))]
    (tmp_path / "avisos.jsonl").write_text("\n".join(json.dumps(e) for e in lines) + "\nbasura\n", encoding="utf8")
    return tmp_path


def test_notices_come_newest_first_ignore_broken_lines_and_carry_the_last_mark(directory):
    notice_review.mark("a1", "dudoso", "primero", directory)
    notice_review.mark("a1", "falsa_alarma", "segundo", directory)
    rows = notice_review.notices(directory)
    assert [r["id"] for r in rows] == ["b2", "a1"] and rows[0]["mark"] is None
    assert rows[1]["mark"]["veredicto"] == "falsa_alarma" and rows[1]["mark"]["nota"] == "segundo"
    summary = notice_review.summary(directory)
    assert summary["total"] == 2 and summary["evaluados"] == 1 and summary["por_veredicto"] == {"falsa_alarma": 1}
    assert summary["por_tipo"] == [dict(tipo="contradiction", veredicto="falsa_alarma", n=1)]


def test_marking_rejects_unknown_ids_and_verdicts(directory):
    with pytest.raises(KeyError):
        notice_review.mark("nope", "acierto", "", directory)
    with pytest.raises(ValueError):
        notice_review.mark("a1", "quizas", "", directory)


def test_the_page_lists_and_marks_but_only_for_local_hosts(directory):
    client = TestClient(create_review_app(directory), base_url="http://127.0.0.1:8038")
    assert "Revisión de avisos" in client.get("/").text
    listing = client.get("/api/avisos").json()
    assert [a["id"] for a in listing["avisos"]] == ["b2", "a1"] and listing["resumen"]["total"] == 2
    ok = client.post("/api/avisos/a1/marca", json={"veredicto": "acierto", "nota": "bien"})
    assert ok.status_code == 200 and notice_review.marks(directory)["a1"]["nota"] == "bien"
    assert client.post("/api/avisos/a1/marca", json={"veredicto": "quizas"}).status_code == 422
    assert client.post("/api/avisos/zzz/marca", json={"veredicto": "acierto"}).status_code == 404
    foreign = client.post("/api/avisos/a1/marca", json={"veredicto": "acierto"}, headers={"origin": "http://evil.example"})
    assert foreign.status_code == 403
    remote = TestClient(create_review_app(directory), base_url="http://miservidor.example")
    assert remote.get("/api/avisos").status_code == 403


def test_refusals_are_logged_like_notices_and_listed_for_the_teacher(tmp_path):
    from oralia.documentary.notice_log import record_rejection

    identifier = record_rejection(
        tmp_path / "avisos.jsonl", "¿Qué es Scrum?", "scope_outside", "No he encontrado esa cuestión…", "¿Qué es un caso de uso?"
    )
    assert identifier and record_rejection(None, "x", "scope_outside", "y") is None
    rows = notice_review.notices(tmp_path)
    assert rows[0]["kind"] == "rechazo" and rows[0]["notice_kinds"] == ["scope_outside"]
    assert rows[0]["previous_question"] == "¿Qué es un caso de uso?" and rows[0]["reviewer_findings"] == []
    notice_review.mark(identifier, "falsa_alarma", "debía responderse", tmp_path)
    assert notice_review.summary(tmp_path)["por_tipo"] == [dict(tipo="scope_outside", veredicto="falsa_alarma", n=1)]


def test_purge_removes_old_entries_and_their_marks(tmp_path):
    from datetime import datetime, timedelta, timezone

    from oralia.documentary import notice_review as review

    now = datetime(2026, 11, 7, tzinfo=timezone.utc)
    rows = [
        {"id": "viejo", "at": (now - timedelta(days=200)).isoformat()},
        {"id": "nuevo", "at": (now - timedelta(days=3)).isoformat()},
    ]
    (tmp_path / "avisos.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf8")
    (tmp_path / "etiquetas.jsonl").write_text("".join(json.dumps({"id": r["id"]}) + "\n" for r in rows), encoding="utf8")
    assert review.purge(180, tmp_path, now) == 1
    assert [r["id"] for r in review.read_lines(tmp_path / "avisos.jsonl")] == ["nuevo"]
    assert [r["id"] for r in review.read_lines(tmp_path / "etiquetas.jsonl")] == ["nuevo"]
    assert review.purge(0, tmp_path, now) == 1 and review.read_lines(tmp_path / "avisos.jsonl") == []
