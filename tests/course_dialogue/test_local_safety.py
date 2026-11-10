"""Owned resources cannot replace another local listener or overwrite an unmarked root."""

import socket
from pathlib import Path

import pytest

from oralia.course_dialogue.__main__ import lab_root
from oralia.course_dialogue.local_provider import owned_provider


def test_occupied_explicit_port_is_preserved(tmp_path, monkeypatch):
    monkeypatch.setattr("oralia.course_dialogue.local_provider.shutil.which", lambda _: "installed-provider")
    with socket.socket() as foreign:
        foreign.bind(("127.0.0.1", 0))
        foreign.listen()
        port = foreign.getsockname()[1]
        with pytest.raises(OSError):
            with owned_provider(tmp_path, port):
                pytest.fail("foreign port accepted")
        assert foreign.fileno() != -1
        assert not (tmp_path / "provider-stdout.log").exists()


def test_unmarked_root_is_not_replaced(tmp_path):
    root = tmp_path / ".oralia-course-dialogue-lab"
    root.mkdir()
    (root / "data").write_text("keep")
    with pytest.raises(FileNotFoundError):
        lab_root(tmp_path)
    assert (root / "data").read_text() == "keep"


def test_marked_root_reuses_and_rejects_hardlinked_files(tmp_path):
    root = lab_root(tmp_path)
    assert lab_root(tmp_path) == root
    target = tmp_path / "usual-file"
    target.write_text("unchanged")
    (root / "linked").hardlink_to(target)
    with pytest.raises(ValueError, match="enlace duro"):
        lab_root(tmp_path)
    assert target.read_text() == "unchanged"


def test_operation_lock_excludes_a_second_process_and_releases(tmp_path):
    import subprocess
    import sys

    from oralia.course_study.__main__ import owned_lock

    root = lab_root(tmp_path)
    code = (
        "from pathlib import Path; import sys; "
        "from oralia.course_study.__main__ import owned_lock; "
        "handle=owned_lock(Path(sys.argv[1])); handle.__enter__(); handle.__exit__(None,None,None)"
    )
    with owned_lock(root):
        second = subprocess.run(
            [sys.executable, "-c", code, str(root)], capture_output=True, text=True, timeout=10
        )
        assert second.returncode != 0 and "Ya hay un autoestudio" in second.stderr
    with owned_lock(root):
        pass
    assert (root / "marker.json").is_file()


@pytest.mark.asyncio
async def test_inspection_cancellation_discards_memory_without_a_participant_session(monkeypatch):
    from oralia.course_dialogue import __main__ as cli

    inputs = iter(["Pregunta ficticia", KeyboardInterrupt()])
    messages = []

    def read(prompt):
        value = next(inputs)
        if isinstance(value, BaseException):
            raise value
        return value

    async def fake(*args, **kwargs):
        return {
            "input": "Pregunta ficticia",
            "raw_candidate": "CANDIDATA FICTICIA SOLO TEST",
            "publication_allowed": False,
        }

    monkeypatch.setattr(cli, "propose", fake)
    await cli.inspect_loop([], read=read, write=messages.append)
    assert any("NO APROBADAS" in message for message in messages)
    assert any("No hubo publicación participante" in message for message in messages)


@pytest.mark.asyncio
async def test_controlled_inspection_sources_and_exit_without_persistence(monkeypatch):
    import json

    from oralia.course_dialogue.__main__ import inspect_drafts
    from oralia.course_dialogue.draft_dialogue import DraftCurriculum
    from oralia.domain.agents.agent_contract import AgentResult
    from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent

    sources = json.loads(
        Path("specs/012-conversational-course-study/evidence/source-catalog.json").read_text(encoding="utf-8")
    )
    c = DraftCurriculum(catalog=sources)

    async def fake(self, request, cancellation):
        if request.input["text"] == "DUDA SINTÉTICA SIN REFERENTE":
            return AgentResult(status="ok", output={"semantic_plan": {"act": "clarify"}})
        assert request.input["text"] == "PREGUNTA SINTÉTICA DE PRUEBA"
        return AgentResult(
            status="ok", output={"semantic_plan": {"act": "explain", "goal_ref": "validacion_requisitos"}}
        )

    monkeypatch.setattr(StudyIntentInterpreterAgent, "execute", fake)
    inputs = iter(
        [
            "/fuentes",
            "PREGUNTA SINTÉTICA DE PRUEBA",
            "DUDA SINTÉTICA SIN REFERENTE",
            "/fuentes",
            "/estado",
            "/salir",
        ]
    )
    messages = []
    events = []
    await inspect_drafts(
        c, object(), read=lambda _: next(inputs), write=messages.append, on_event=events.append
    )
    assert any("página original" in text for text in messages)
    assert any("not_assessed" in text for text in messages)
    assert any("NO APROBADOS" in text for text in messages)
    assert "No hubo publicación participante" in messages[-1]
    assert any(e["event"] == "before_planning" for e in events)
    assert any(
        e["event"] == "actual_preview" and e["preview"]["publication_allowed"] is False for e in events
    )
    assert events[-1]["event"] == "inspection_closed" and events[-1]["participant_session"] is False
