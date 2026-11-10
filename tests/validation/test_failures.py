import pytest

from oralia.validation.experiment import run_cell
from oralia.validation.protocol import SCENARIOS, Protocol


@pytest.mark.asyncio
@pytest.mark.parametrize("scenario", [s for s in SCENARIOS if s.fault])
async def test_failures_are_observed_and_do_not_escape_or_corrupt_state(scenario):
    result = await run_cell(Protocol(conditions=["full"], repetitions=1), scenario, "full", 0)
    assert result["error"] is None, result
    assert result["injection_applied"]
    if scenario.fault == "agent_timeout":
        assert any(c["status"] == "timeout" for c in result["components"])
        assert result["recovery"]
    elif scenario.fault in {"model", "index", "stt", "resources"}:
        assert result["recovery"]
    elif scenario.fault == "state":
        assert result["state"]["stale_update_rejected"] is True
    elif scenario.fault == "limit":
        assert result["status"] == "closed_limit_reached"
    elif scenario.fault == "delete":
        assert result["deleted"]
    elif scenario.fault == "correction":
        assert result["transcription"]["original_preserved"]
        assert result["transcription"]["corrected_input_used"]
