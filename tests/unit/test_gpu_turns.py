import asyncio

import pytest

from oralia.documentary.gpu_turns import GroupExclusion, TurnTakingProvider


async def hold(exclusion, group, log, name, seconds=0.02):
    async with exclusion.use(group):
        log.append(("in", group, name))
        await asyncio.sleep(seconds)
        log.append(("out", group, name))


@pytest.mark.asyncio
async def test_calls_of_one_group_overlap_but_the_other_group_never_runs_at_the_same_time():
    exclusion, log = GroupExclusion(), []
    await asyncio.gather(
        *[hold(exclusion, "gen", log, f"g{i}") for i in range(3)],
        *[hold(exclusion, "rev", log, f"r{i}") for i in range(3)],
    )
    active = {"gen": 0, "rev": 0}
    for kind, group, _ in log:
        active[group] += 1 if kind == "in" else -1
        other = "rev" if group == "gen" else "gen"
        assert active[other] == 0  # never both groups at once
    assert max(sum(1 for k, g, _ in log[:i] if k == "in" and g == "gen") for i in range(len(log))) == 3


@pytest.mark.asyncio
async def test_a_waiting_group_goes_before_new_arrivals_of_the_active_group():
    exclusion, log = GroupExclusion(), []
    first = asyncio.create_task(hold(exclusion, "gen", log, "g0", 0.05))
    await asyncio.sleep(0.01)
    waiting = asyncio.create_task(hold(exclusion, "rev", log, "r0"))
    await asyncio.sleep(0.01)
    late = asyncio.create_task(hold(exclusion, "gen", log, "g1"))
    await asyncio.gather(first, waiting, late)
    order = [name for kind, _, name in log if kind == "in"]
    assert order == ["g0", "r0", "g1"]


@pytest.mark.asyncio
async def test_the_wrapper_passes_calls_and_attributes_through_and_releases_on_errors():
    class Inner:
        model_label = "m"

        async def generate(self, request):
            if request == "boom":
                raise RuntimeError("x")
            return request

    exclusion = GroupExclusion()
    wrapped = TurnTakingProvider(Inner(), exclusion, "gen")
    assert wrapped.model_label == "m" and await wrapped.generate("ok") == "ok"
    with pytest.raises(RuntimeError):
        await wrapped.generate("boom")
    assert await asyncio.wait_for(TurnTakingProvider(Inner(), exclusion, "rev").generate("again"), 1) == "again"
