"""Delivery lifecycle checks with simulated ports; no academic validation."""

import copy

import pytest
from test_lab_conversation import setup


@pytest.mark.asyncio
async def test_repeated_preparation_and_confirmation_never_duplicate_history():
    lab, _, _ = setup()
    row = await lab.turn("consistencia requisitos")
    assert lab.prepare_display(row["turn_id"]) == lab.prepare_display(row["turn_id"])
    assert lab.history == []
    lab.acknowledge_display(row["turn_id"])
    once = copy.deepcopy(lab.history)
    with pytest.raises(ValueError, match="pending display"):
        lab.acknowledge_display(row["turn_id"])
    with pytest.raises(ValueError, match="pending display"):
        lab.prepare_display(row["turn_id"])
    assert lab.history == once
    assert len(lab.history) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("prepare_before_discard", [False, True])
async def test_discarded_pending_delivery_does_not_replace_displayed_referent(prepare_before_discard):
    lab, _, provider = setup()
    first = await lab.turn("consistencia requisitos")
    lab.prepare_display(first["turn_id"])
    lab.acknowledge_display(first["turn_id"])
    before = copy.deepcopy(lab.history)
    pending = await lab.turn("Cambiemos de tema: consistencia de otra especificación")
    if prepare_before_discard:
        lab.prepare_display(pending["turn_id"])
    lab.discard_pending()
    lab.discard_pending()  # discarding twice is harmless
    assert lab.history == before
    with pytest.raises(ValueError, match="pending display"):
        lab.acknowledge_display(pending["turn_id"])
    followup = await lab.turn("¿Por qué?")
    assert followup["academic_query"] == first["academic_query"]
    assert "otra especificación" not in followup["academic_query"]
    assert all(
        "otra especificación" not in message.content for message in provider.requests[-1].conversation_history
    )
    assert lab.history == before
    # Returned rows are snapshots; lifecycle updates are read from fresh receipts.
    assert lab.receipts[pending["turn_id"] - 1]["display_discarded"] is True
