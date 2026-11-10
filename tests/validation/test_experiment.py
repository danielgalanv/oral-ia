import pytest

from oralia.validation.experiment import run_cell
from oralia.validation.protocol import SCENARIOS, Protocol


@pytest.mark.asyncio
async def test_real_composer_and_direct_baseline_produce_measured_different_traces():
    p = Protocol(repetitions=1)
    baseline = await run_cell(p, SCENARIOS[0], "baseline", 0)
    full = await run_cell(p, SCENARIOS[0], "full", 0)
    assert baseline["components"][0]["agent_id"] == "direct-model"
    assert any(c["agent_id"] == "grounding-verifier" for c in full["components"])
    assert full["grounding_verdict"] == "fundamentada"
    assert full["metrics"]["retrieval_precision"]["value"] == 1
    assert full["metrics"]["cpu_seconds"]["source"] == "process_time"
    assert full["metrics"]["gpu_memory_mb"]["value"] is None
    assert full["state"]["after"] > full["state"]["before"]
    assert full["error"] is None


@pytest.mark.asyncio
async def test_ablation_changes_verifier_observation_and_restores_production_class():
    from oralia.application.orchestration import self_study_agency_composer as composer

    original = composer.GroundingVerifierAgent
    p = Protocol(ablations_authorized=True, conditions=["full", "no_grounding"], repetitions=1)
    full = await run_cell(p, SCENARIOS[4], "full", 0)
    ablated = await run_cell(p, SCENARIOS[4], "no_grounding", 0)
    assert full["grounding_verdict"] == "no_fundamentada"
    assert ablated["grounding_verdict"] == "fundamentada"
    assert ablated["ablations"] == ["grounding-verifier"]
    assert composer.GroundingVerifierAgent is original
    with pytest.raises(ValueError):
        await run_cell(Protocol(), SCENARIOS[0], "no_grounding", 0)


@pytest.mark.asyncio
async def test_coherence_ablation_and_top1_change_only_recorded_factors():
    p = Protocol(ablations_authorized=True, conditions=["full", "no_coherence", "top1"], repetitions=1)
    full = await run_cell(p, SCENARIOS[5], "full", 0)
    ablated = await run_cell(p, SCENARIOS[5], "no_coherence", 0)
    assert full["coherence_verdict"] == "block"
    assert ablated["coherence_verdict"] == "approved"
    all_sources = await run_cell(p, SCENARIOS[2], "full", 0)
    top1 = await run_cell(p, SCENARIOS[2], "top1", 0)
    assert len(all_sources["retrieved_ids"]) == 2
    assert len(top1["retrieved_ids"]) == 1
    assert top1["metrics"]["retrieval_recall"]["value"] == 0.5


@pytest.mark.asyncio
async def test_constitutional_grade_block_survives_both_ablations():
    conditions = ["baseline", "full", "no_grounding", "no_coherence"]
    p = Protocol(ablations_authorized=True, conditions=conditions, repetitions=1)
    for condition in conditions:
        result = await run_cell(p, SCENARIOS[14], condition, 0)
        assert result["error"] is None
        assert "Tu nota es 9" not in (result["output_text"] or "")
        if condition != "baseline":
            assert "output_authorization_attempt" in result["event_types"]


@pytest.mark.asyncio
async def test_blocked_and_degraded_terminal_events_are_traceable_not_lost_turns():
    p = Protocol(conditions=["full"], repetitions=1)
    for scenario in (SCENARIOS[5], SCENARIOS[7]):
        result = await run_cell(p, scenario, "full", 0)
        assert result["fully_traced"]
        assert result["reconstruction"]["patch_chain"]
