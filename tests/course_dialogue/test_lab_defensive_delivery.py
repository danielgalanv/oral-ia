"""External receipt mutation cannot change bytes committed to shown history."""

from test_lab_conversation import setup


async def test_returned_receipt_cannot_replace_pending_display():
    lab, _, _ = setup()
    row = await lab.turn("consistencia requisitos")
    expected = row["displayed_text"]
    row["displayed_text"] = "unreviewed replacement"
    row["review"] = None
    assert lab.prepare_display(row["turn_id"]) == expected
    lab.acknowledge_display(row["turn_id"])
    assert lab.history[-1]["displayed_text"] == expected


async def test_receipt_collection_cannot_replace_pending_display():
    lab, _, _ = setup()
    row = await lab.turn("consistencia requisitos")
    expected = row["displayed_text"]
    lab.receipts[-1]["displayed_text"] = "unreviewed replacement"
    assert lab.prepare_display(row["turn_id"]) == expected


async def test_history_snapshot_cannot_add_unshown_text():
    lab, _, _ = setup()
    lab.history.append({"input": "fake", "displayed_text": "unshown text"})
    assert lab.history == []


async def test_catalog_snapshots_cannot_replace_source_text():
    lab, _, _ = setup()
    expected = lab.catalog
    exposed = lab.catalog
    exposed.clear()
    assert lab.catalog == expected
    assert lab.catalog is not exposed
