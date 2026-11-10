import json

import pytest

from oralia.course_dialogue.concept_ledger import source_cards
from oralia.course_dialogue.concept_review_loop import ConceptLedgerReviewer
from oralia.course_dialogue.lab_request import RepairGenerationRequest
from oralia.course_dialogue.prepared_concepts import PreparedConcepts, prepare
from oralia.course_dialogue.review_repair import CallBudget
from oralia.infrastructure.generation.generation_port import EvidenceItem, GenerationOutcome


def fixture(tmp_path):
    originals = {}
    evidence = []
    for i in range(2):
        path = tmp_path / f"source-{i}.pdf"
        path.write_bytes(f"original {i}".encode())
        originals[f"d{i}"] = path
        evidence.append(
            EvidenceItem(
                fragment_id=f"d{i}:1",
                document_id=f"d{i}",
                document_version=2,
                text=f"• Concepto{i}. Definición original completa.\n",
            )
        )
    return originals, evidence


def test_reused_catalogue_is_question_independent_and_keeps_all_source_context(tmp_path):
    files, evidence = fixture(tmp_path)
    store = prepare(tmp_path / "cache", evidence, files, corpus_id="course")
    assert store.project(evidence)["cards"] == source_cards(evidence)
    first = RepairGenerationRequest(
        purpose="explicacion", instruction="Test", student_input="Pregunta uno", evidence=evidence
    )
    second = first.model_copy(update={"student_input": "Pregunta dos"})
    a = store.for_turn(first, revalidate=lambda: None)
    b = store.for_turn(second, revalidate=lambda: None)
    assert a["binding"] != b["binding"]
    assert a["decision"] == b["decision"]
    assert a["prepared_revision"] == b["prepared_revision"]


@pytest.mark.parametrize("change", ["text", "version", "original", "withdrawal", "tamper"])
def test_stale_withdrawn_or_modified_cache_is_rejected(tmp_path, change):
    files, evidence = fixture(tmp_path)
    store = prepare(tmp_path / "cache", evidence, files, corpus_id="course")
    if change == "text":
        evidence[0] = evidence[0].model_copy(update={"text": "Otro contenido"})
    if change == "version":
        evidence[0] = evidence[0].model_copy(update={"document_version": 3})
    if change == "original":
        files["d0"].write_bytes(b"changed PDF")
    if change == "withdrawal":
        store.source_files.pop("d0")
    if change == "tamper":
        manifest = json.loads((tmp_path / "cache/manifest.json").read_bytes())
        (tmp_path / "cache/documents" / (manifest["documents"]["d0"] + ".json")).write_text("{}")
        with pytest.raises(ValueError, match="altered"):
            PreparedConcepts(tmp_path / "cache", files)
    else:
        with pytest.raises(ValueError):
            store.project(evidence)


def test_update_only_changes_affected_document_and_preserves_old_revision(tmp_path):
    files, evidence = fixture(tmp_path)
    root = tmp_path / "cache"
    prepare(root, evidence, files, corpus_id="course")
    old = json.loads((root / "manifest.json").read_bytes())
    unchanged = root / "documents" / (old["documents"]["d1"] + ".json")
    stamp = unchanged.stat().st_mtime_ns
    evidence[0] = evidence[0].model_copy(update={"text": "• Otro concepto. Una definición nueva."})
    prepare(root, evidence, files, corpus_id="course")
    new = json.loads((root / "manifest.json").read_bytes())
    assert new["documents"]["d1"] == old["documents"]["d1"]
    assert new["documents"]["d0"] != old["documents"]["d0"]
    assert unchanged.stat().st_mtime_ns == stamp
    assert (root / "documents" / (old["documents"]["d0"] + ".json")).exists()


@pytest.mark.asyncio
async def test_review_consumes_prepared_sources_without_online_catalogue_model(tmp_path):
    files, evidence = fixture(tmp_path)
    store = prepare(tmp_path / "cache", evidence, files, corpus_id="course")

    class Planner:
        async def generate(self, request):
            raise AssertionError("online catalogue generation must not occur")

    class Critic:
        async def generate(self, request):
            return GenerationOutcome(
                ok=True,
                text='{"card_ids":["C1"],"verdict":"correct","reason":"Uso contrastado"}',
                finish_reason="stop",
                adapter="deterministic",
            )

    budget = CallBudget(maximum=1)
    reviewer = ConceptLedgerReviewer(Planner(), Critic(), budget=budget, revalidate=lambda: None)
    base = RepairGenerationRequest(
        purpose="explicacion", instruction="Test", student_input="Una pregunta", evidence=evidence
    )
    trace = await reviewer.review(base, "Una explicación sin encabezado", prepared=store)
    assert trace["status"] == "no_issues_found" and budget.used == 1
    assert trace["catalogue"]["prepared_revision"] == store.revision


def test_policy_is_revalidated_even_with_unchanged_prepared_pdf(tmp_path):
    files, evidence = fixture(tmp_path)
    store = prepare(tmp_path / "cache", evidence, files, corpus_id="course")
    base = RepairGenerationRequest(
        purpose="explicacion", instruction="Test", student_input="Pregunta", evidence=evidence
    )

    def revoked():
        raise ValueError("activity policy revoked")

    with pytest.raises(ValueError, match="revoked"):
        store.for_turn(base, revalidate=revoked)


def test_revocation_before_commit_preserves_previous_catalogue(tmp_path):
    files, evidence = fixture(tmp_path)
    root = tmp_path / "cache"
    prepare(root, evidence, files, corpus_id="course")
    before = (root / "manifest.json").read_bytes()
    calls = 0

    def revoke_before_commit():
        nonlocal calls
        calls += 1
        if calls == 2:
            raise ValueError("authorisation revoked before commit")

    evidence[0] = evidence[0].model_copy(update={"text": "• Otro concepto. Definición modificada."})
    with pytest.raises(ValueError, match="revoked"):
        prepare(root, evidence, files, corpus_id="course", revalidate=revoke_before_commit)
    assert (root / "manifest.json").read_bytes() == before
