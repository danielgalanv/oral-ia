"""Question approval and transcript safety; no retrieval or model runs."""

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "docs/audits/2026-11-01-autostudy-approval/run.py"
spec = importlib.util.spec_from_file_location("autostudy_approval_runner", SCRIPT)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def prepare(folder):
    pack = runner.read(SCRIPT.parent / "questions.json")
    path = folder / "questions.json"
    path.write_text(json.dumps(pack, ensure_ascii=False), encoding="utf8")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    (folder / "protocol.json").write_text(json.dumps(dict(questions_sha256=digest)), encoding="utf8")
    return pack, digest


def test_proposed_questions_have_bounded_complete_histories():
    pack = runner.read(SCRIPT.parent / "questions.json")
    runner.validate_pack(pack)
    assert sum(len(c["turns"]) for c in pack["conversations"]) == 12
    assert all(2 * (len(c["turns"]) - 1) <= 8 for c in pack["conversations"])


@pytest.mark.parametrize("kind", ["missing", "wrong_hash", "false", "no_human_message", "changed_questions"])
def test_invalid_approval_never_authorizes_a_run(tmp_path, kind):
    pack, digest = prepare(tmp_path)
    if kind != "missing":
        approval = dict(
            approved=kind != "false",
            questions_sha256="0" * 64 if kind == "wrong_hash" else digest,
            user_message=(
                "" if kind == "no_human_message" else "Synthetic approval fixture, not real user validation"
            ),
        )
        (tmp_path / "approval.json").write_text(json.dumps(approval), encoding="utf8")
    if kind == "changed_questions":
        pack["conversations"][0]["turns"][0]["question"] += " Changed"
        (tmp_path / "questions.json").write_text(json.dumps(pack), encoding="utf8")
    with pytest.raises(ValueError):
        runner.require_approval(tmp_path)


def test_exact_question_version_can_be_approved_in_isolated_fixture(tmp_path):
    pack, digest = prepare(tmp_path)
    (tmp_path / "approval.json").write_text(
        json.dumps(
            dict(
                approved=True,
                questions_sha256=digest,
                user_message="Synthetic approval fixture, not real user validation",
            )
        ),
        encoding="utf8",
    )
    assert runner.require_approval(tmp_path)[0] == pack


def test_execute_without_user_validation_never_calls_runtime(tmp_path, monkeypatch):
    prepare(tmp_path)
    monkeypatch.setattr(runner, "HERE", tmp_path)
    monkeypatch.setattr("sys.argv", [str(SCRIPT), "--execute"])

    def forbidden(*args):
        raise AssertionError("No runtime before question approval")

    monkeypatch.setattr(runner, "execute", forbidden)
    with pytest.raises(ValueError, match="Pending user validation"):
        runner.main()


def test_mobile_report_escapes_content_and_labels_missing_answers(tmp_path):
    runner.render(tmp_path, [dict(id="A1", question="<script>bad</script>", status="review_incomplete")])
    page = (tmp_path / "transcript-mobile.html").read_text(encoding="utf8")
    assert "<script>" not in page and "&lt;script&gt;" in page
    assert "Sin respuesta final completa" in page


@pytest.mark.asyncio
async def test_unattended_flow_preserves_history_and_skips_only_dependent_turns(tmp_path, monkeypatch):
    import asyncio
    from contextlib import asynccontextmanager
    from types import SimpleNamespace

    import oralia.course_dialogue.cached_transformers as backend
    import oralia.documentary.retrieval as retrieval_module
    from oralia.infrastructure.generation.generation_port import GenerationOutcome

    pack = runner.read(SCRIPT.parent / "questions.json")
    protocol = runner.read(SCRIPT.parent / "protocol.json")
    for name in ["questions.json", "protocol.json"]:
        (tmp_path / name).write_bytes((SCRIPT.parent / name).read_bytes())
    (tmp_path / "approval.json").write_text(
        json.dumps(
            dict(
                approved=True,
                questions_sha256=protocol["questions_sha256"],
                user_message="Synthetic workflow fixture only",
            )
        ),
        encoding="utf8",
    )
    monkeypatch.setattr(runner, "HERE", tmp_path)
    monkeypatch.setattr(retrieval_module, "DERIVED", tmp_path / "absent-old-index")
    requests = []
    searches = []
    closed = []

    class Retrieval:
        identity = {"fixture": True}

        def __init__(self, **kwargs):
            assert kwargs["build"] is True

        def revalidate(self):
            pass

        def query(self, question, strategy, **kwargs):
            searches.append((question, kwargs))
            return dict(
                passages=[
                    dict(
                        id="fixture-page",
                        document_id="docente-fixture",
                        filename="Fixture.pdf",
                        page=1,
                        text="Synthetic source for workflow only.",
                    )
                ]
            )

    monkeypatch.setattr(retrieval_module, "Retrieval", Retrieval)

    class Provider:
        usable = True
        last_exchange = None

        async def generate(self, request):
            requests.append(request)
            if request.prompt_task == "generate":
                text = "Synthetic generated answer for workflow test."
            else:
                text = json.dumps(
                    dict(
                        status=(
                            "insufficient_evidence"
                            if request.question == pack["conversations"][0]["turns"][1]["question"]
                            else "no_issues_found"
                        ),
                        issues=[],
                    )
                )
            return GenerationOutcome(ok=True, text=text, finish_reason="stop", adapter="deterministic")

    @asynccontextmanager
    async def provider(*args, **kwargs):
        try:
            yield Provider()
        finally:
            closed.append(True)

    monkeypatch.setattr(backend, "cached_provider", provider)
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: SimpleNamespace(stdout="0, 1500, 30688"))
    real_sleep = asyncio.sleep

    async def fast_sleep(seconds):
        await real_sleep(0)

    monkeypatch.setattr(asyncio, "sleep", fast_sleep)
    await runner.execute(pack, protocol)
    out = next(tmp_path.glob("run-*"))
    result = runner.read(out / "result.json")
    rows = {x["id"]: x for x in result["turns"]}
    assert len(rows) == 12 and rows["A3"]["status"] == rows["A4"]["status"] == "skipped_dependent_turn"
    assert rows["B1"]["status"] == rows["C1"]["status"] == "critic_finished_unverified"
    assert len(closed) == 2
    generated = [q for q in requests if q.prompt_task == "generate"]
    assert all(q.didactic_profile == "study-dialogue/v1" for q in generated)
    by_question = {q.question: q for q in generated}
    b = pack["conversations"][1]["turns"]
    assert by_question[b[0]["question"]].conversation_history == []
    assert len(by_question[b[3]["question"]].conversation_history) == 6
    assert (
        by_question[b[1]["question"]].conversation_history[-1].content
        == "Synthetic generated answer for workflow test."
    )
    c3 = pack["conversations"][2]["turns"][2]["question"]
    assert next(options for question, options in searches if question == c3)["focus_change"] is True
