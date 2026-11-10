"""Unit tests for the deterministic segmenter's reproducibility across repeated runs
with the same config (FR-007)."""

from __future__ import annotations

from oralia.domain.materials.segmenter import ExtractedBlock, segment_blocks

_LONG_TEXT = (
    "Primera oracion con contenido de prueba. Segunda oracion algo mas larga para "
    "forzar la division en varios fragmentos distintos y comprobar el comportamiento. "
    "Tercera oracion final del parrafo de prueba.\n\n"
    "Segundo parrafo con otra oracion de prueba. Y una oracion mas para completar el "
    "bloque de texto usado en esta prueba unitaria del segmentador determinista."
)


def test_same_input_and_config_produce_identical_output():
    blocks = [ExtractedBlock(text=_LONG_TEXT, location_ref="página 1")]
    result1 = segment_blocks(blocks, chunk_size=80, overlap=10)
    result2 = segment_blocks(blocks, chunk_size=80, overlap=10)

    assert result1 == result2
    assert len(result1) > 1  # sanity: the text is long enough to actually split


def test_sequence_index_is_monotonic_and_contiguous():
    blocks = [
        ExtractedBlock(text=_LONG_TEXT, location_ref="página 1"),
        ExtractedBlock(text="Otro bloque de texto en la segunda página.", location_ref="página 2"),
    ]
    segments = segment_blocks(blocks, chunk_size=80, overlap=10)
    indices = [s.sequence_index for s in segments]
    assert indices == list(range(len(segments)))


def test_short_block_is_not_split():
    blocks = [ExtractedBlock(text="Texto corto.", location_ref="línea 1")]
    segments = segment_blocks(blocks, chunk_size=800, overlap=100)
    assert len(segments) == 1
    assert segments[0].text == "Texto corto."


def test_different_chunk_size_changes_output_deterministically():
    blocks = [ExtractedBlock(text=_LONG_TEXT, location_ref="página 1")]
    small = segment_blocks(blocks, chunk_size=50, overlap=5)
    large = segment_blocks(blocks, chunk_size=500, overlap=5)
    assert len(small) >= len(large)
    # Re-running with the same (smaller) config again must reproduce byte-for-byte.
    assert segment_blocks(blocks, chunk_size=50, overlap=5) == small
