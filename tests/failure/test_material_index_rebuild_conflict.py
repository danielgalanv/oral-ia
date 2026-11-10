"""US7 failure test: two simultaneous index-rebuild requests — one succeeds, the other
gets 409 (Edge Case, research.md §9)."""

from __future__ import annotations

import pytest

from oralia.application.services.index_rebuild_lock_service import (
    IndexRebuildAlreadyInProgress,
    acquire,
    release,
)


@pytest.mark.failure
def test_second_concurrent_rebuild_rejected(db_session):
    lock = acquire(db_session)
    with pytest.raises(IndexRebuildAlreadyInProgress):
        acquire(db_session)

    release(db_session, lock)
    # After release, a new rebuild is allowed again.
    second_lock = acquire(db_session)
    release(db_session, second_lock)
