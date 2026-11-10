"""Audit stream changes no model-visible data and never claims semantic support."""

import json

from scripts.run_readable_reference_probe import RecordingWriter


def test_recording_writer_preserves_messages_and_budget_and_captures_sent_frame(tmp_path):
    class Writer:
        def __init__(self):
            self.sent = []

        def write(self, raw):
            self.sent.append(json.loads(raw))

    original = Writer()
    frames = []
    path = tmp_path / "frames.json"
    writer = RecordingWriter(original, frames, path)
    frame = {
        "id": "fixture",
        "messages": [{"role": "user", "content": "fixture"}],
        "max_tokens": 512,
        "deadline_ms": 30000,
        "finite_outputs": None,
    }
    writer.write((json.dumps(frame) + "\n").encode())
    assert original.sent[0] == {**frame, "audit_config": True}
    assert json.loads(path.read_text(encoding="utf-8")) == original.sent == frames
    writer.write(b'{"type":"stop"}\n')
    assert len(frames) == 1
    assert original.sent[-1] == {"type": "stop"}
