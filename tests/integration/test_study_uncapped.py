"""Study has no educational question quota; experiments retain explicit budgets."""

import pytest

from oralia.documentary.real_study_provider import RealStudyProvider
from oralia.documentary.study_lab import DiagnosticStudy
from tests.integration.test_study_chat_resume import make_client
from tests.integration.test_study_presentation_delivery import enter, turn
from tests.unit.test_study_lab import RetrievalFixture, identifier


def test_more_than_twelve_questions_and_reentry_without_student_quota():
    client, provider, _ = make_client()
    with client:
        enter(client)
        for _ in range(15):
            key = identifier()
            assert turn(client, key).json()["status"] == "prepared_unverified"
            client.post(f"/api/v1/study-lab/{key}/shown", json={})
        snapshot = client.get("/api/v1/study-lab/resume").json()
        assert len(snapshot["messages"]) == 15 and snapshot["quota"]["remaining"] is None
        assert snapshot["quota"]["maximum"] is None and not snapshot["quota"]["exhausted"]
        client.post("/api/v1/study-lab/close", json={})
        enter(client)
        assert turn(client, identifier()).json()["status"] == "prepared_unverified"
        assert len(provider.requests) == 16


def test_reviewed_runtime_preserves_finite_trials_but_uncaps_normal_study(tmp_path):
    normal = RealStudyProvider(tmp_path / "normal", reviewed=True)
    trial = RealStudyProvider(tmp_path / "trial", reviewed=True, experimental_limits=True)
    assert trial.trial_budget.maximum == 12 and trial.review_budget.maximum == 84
    assert normal.trial_budget.maximum is None and normal.review_budget.maximum is None
    for _ in range(90):
        normal.trial_budget.reserve()
        normal.review_budget.reserve()
    assert normal.review_budget.used == 90 and normal.trial_budget.used == 90
    normal.trial_budget.started -= 3000
    normal.review_budget.started -= 3000
    with pytest.raises(ValueError):
        normal.trial_budget.reserve()
    with pytest.raises(ValueError):
        normal.review_budget.reserve()
    with pytest.raises(ValueError):
        RealStudyProvider(tmp_path / "legacy", experimental_limits=False)


async def test_reviewed_pipeline_continues_after_old_internal_ceiling(tmp_path):
    from tests.course_dialogue.test_web_review_rounds import Provider
    from tests.unit.test_reviewed_study_chat import PASS

    owner = RealStudyProvider(tmp_path / "normal", reviewed=True, experimental_limits=False)
    owner.adapter, owner.critic_adapter = Provider("Respuesta simulada"), Provider(PASS)
    owner.review_budget.used = 84
    owner.trial_budget.used = 12
    lab = DiagnosticStudy(
        RetrievalFixture(),
        owner,
        authority=lambda: True,
        budget=owner.trial_budget,
        course="test",
        activity="test",
    )
    result = await lab.turn("Pregunta sin cupo educativo", identifier())
    assert result["status"] == "prepared_unverified"
    assert owner.review_budget.used == 86 and owner.trial_budget.used == 13
