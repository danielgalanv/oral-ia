"""Resource preservation tests; fake bytes here are not generated PDF evidence."""

import hashlib
import json

import pytest

from oralia.course_dialogue.review_preparation import selected_materials


def test_incomplete_selection_folder_is_preserved(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "book.pdf").write_bytes(b"FAKE SOURCE ONLY TEST")
    output = tmp_path / "selection"
    output.mkdir()
    (output / "keep.txt").write_text("keep")
    with pytest.raises(ValueError, match="incomplete"):
        selected_materials(output, [], {"topic": ("book.pdf", (1,))}, source)
    assert (output / "keep.txt").read_text() == "keep"


def test_existing_selection_reuses_bytes_and_rejects_changed_original(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    original = source / "book.pdf"
    original.write_bytes(b"FAKE ORIGINAL")
    output = tmp_path / "selection"
    output.mkdir()
    derived = output / "012-topic-selected.pdf"
    derived.write_bytes(b"FAKE DERIVED")
    manifest = {
        "topic": {
            "original_name": "book.pdf",
            "pages": {"1": 1},
            "original_sha256": hashlib.sha256(original.read_bytes()).hexdigest(),
            "derived_name": derived.name,
            "derived_sha256": hashlib.sha256(derived.read_bytes()).hexdigest(),
        }
    }
    (output / "provenance.json").write_text(json.dumps(manifest))
    assert selected_materials(output, [], {"topic": ("book.pdf", (1,))}, source) == manifest
    original.write_bytes(b"CHANGED FAKE ORIGINAL")
    with pytest.raises(ValueError, match="changed"):
        selected_materials(output, [], {"topic": ("book.pdf", (1,))}, source)
    assert derived.read_bytes() == b"FAKE DERIVED"


def test_material_manifest_cannot_redirect_read_to_an_unrelated_path(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "book.pdf").write_bytes(b"FAKE ORIGINAL")
    output = tmp_path / "selection"
    output.mkdir()
    manifest = {
        "topic": {
            "original_name": "book.pdf",
            "original_sha256": hashlib.sha256(b"FAKE ORIGINAL").hexdigest(),
            "pages": {"1": 1},
            "derived_name": "../unrelated",
            "derived_sha256": "0" * 64,
        }
    }
    (output / "provenance.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="metadata"):
        selected_materials(output, [], {"topic": ("book.pdf", (1,))}, source)


def test_review_root_refuses_unmarked_existing_data_and_reuses_owned_root(tmp_path):
    from oralia.course_dialogue.review_preparation import review_root

    fingerprint = "a" * 64
    existing = tmp_path / ("review-" + fingerprint[:12])
    existing.mkdir()
    (existing / "keep").write_text("unchanged")
    with pytest.raises(ValueError, match="marker"):
        review_root(tmp_path, fingerprint)
    assert (existing / "keep").read_text() == "unchanged"
    other = "b" * 64
    created = review_root(tmp_path, other)
    assert review_root(tmp_path, other) == created
    with pytest.raises(ValueError, match="marker"):
        review_root(tmp_path, "b" * 12 + "c" * 52)


@pytest.mark.parametrize("fingerprint", ["../usual", "z" * 64, "a" * 63])
def test_review_root_requires_complete_hex_fingerprint(tmp_path, fingerprint):
    from oralia.course_dialogue.review_preparation import review_root

    with pytest.raises(ValueError, match="fingerprint"):
        review_root(tmp_path, fingerprint)
    assert list(tmp_path.iterdir()) == []


def test_semantic_policy_identity_preserves_legacy_and_uses_another_root():
    from oralia.course_dialogue.review_preparation import packet_fingerprint

    packet = {"units": [{"id": "fictional"}]}
    legacy = hashlib.sha256(json.dumps(packet, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    assert packet_fingerprint(packet) == legacy
    assert packet_fingerprint(packet, semantic_policy=True) != legacy


def test_semantic_preparation_rejects_ordinary_root_before_database_access(tmp_path):
    from oralia.course_dialogue.review_preparation import packet_fingerprint, prepare, review_root

    root = review_root(tmp_path, packet_fingerprint({"units": []}))
    with pytest.raises(ValueError, match="separate marked"):
        prepare(root, {"units": []}, [], {}, tmp_path, semantic_policy=True)
    assert not (root / "review.db").exists()


def test_reuse_copies_identical_verified_bytes_and_is_idempotent(tmp_path):
    from oralia.course_dialogue.review_preparation import reuse_selected_materials

    originals = tmp_path / "originals"
    originals.mkdir()
    (originals / "book.pdf").write_bytes(b"FAKE ORIGINAL; NO PDF GENERATION")
    source = tmp_path / "existing"
    source.mkdir()
    data = b"FAKE PREEXISTING SELECTED BYTES"
    name = "012-topic-selected.pdf"
    (source / name).write_bytes(data)
    manifest = {
        "topic": {
            "original_name": "book.pdf",
            "pages": {"1": 1},
            "derived_name": name,
            "original_sha256": hashlib.sha256((originals / "book.pdf").read_bytes()).hexdigest(),
            "derived_sha256": hashlib.sha256(data).hexdigest(),
        }
    }
    (source / "provenance.json").write_text(json.dumps(manifest))
    destination = tmp_path / "new"
    selection = {"topic": ("book.pdf", (1,))}
    assert reuse_selected_materials(destination, source, [], selection, originals) == manifest
    assert reuse_selected_materials(destination, source, [], selection, originals) == manifest
    assert (destination / name).read_bytes() == (source / name).read_bytes() == data
    (source / name).write_bytes(b"TAMPERED")
    with pytest.raises(ValueError, match="changed"):
        reuse_selected_materials(destination, source, [], selection, originals)
    assert (destination / name).read_bytes() == data


def test_reuse_never_creates_a_pdf_when_prepared_materials_are_missing(tmp_path):
    from oralia.course_dialogue.review_preparation import reuse_selected_materials

    destination = tmp_path / "new"
    with pytest.raises(ValueError, match="ordinary review"):
        reuse_selected_materials(destination, tmp_path / "missing", [], {}, tmp_path)
    assert not destination.exists()
