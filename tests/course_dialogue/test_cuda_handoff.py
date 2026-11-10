from types import SimpleNamespace

from oralia.course_dialogue.cuda_handoff import cuda_handoff


def test_handoff_releases_unused_pool_without_changing_live_allocations():
    pool = {"reserved": 100}

    def empty():
        pool["reserved"] = 40

    torch = SimpleNamespace(
        cuda=SimpleNamespace(
            memory_allocated=lambda: 40, memory_reserved=lambda: pool["reserved"], empty_cache=empty
        )
    )
    old = cuda_handoff(torch, False)
    assert old["before"] == old["after"] == {"allocated": 40, "reserved": 100}
    new = cuda_handoff(torch, True)
    assert new["after"] == {"allocated": 40, "reserved": 40}
