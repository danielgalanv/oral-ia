"""Pinned scope descriptions are metadata, never academic answer evidence."""

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import pdfplumber


@dataclass(frozen=True)
class BlockMetadata:
    path: Path
    sha256: str

    def revalidate(self, binding, policy):
        raw = self.path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != self.sha256:
            raise ValueError("block metadata changed")
        data = json.loads(raw)
        if (
            data["schema_version"] != 1
            or data["metadata_version"] != 1
            or data["policy_sha256"] != binding.policy_sha256
        ):
            raise ValueError("block metadata bound to another policy")
        expected = {
            block: (category, index)
            for category in (
                "included_blocks",
                "excluded_as_standalone_blocks_for_this_activity",
                "prerequisites_not_extra_study_blocks",
            )
            for index, block in enumerate(policy.get(category, []))
        }
        rows = data["blocks"]
        if len(rows) != len(expected) or {row["id"] for row in rows} != set(expected):
            raise ValueError("block metadata inventory mismatch")
        presentation = policy["source_scope"]["presentation"]
        source = binding.source_root / presentation["file"]
        if hashlib.sha256(source.read_bytes()).hexdigest() != presentation["sha256"]:
            raise ValueError("block metadata source changed")
        with pdfplumber.open(source) as pdf:
            for row in rows:
                category, index = expected[row["id"]]
                ref = row["provenance"]
                if (
                    not row["title"].strip()
                    or not row["description"].strip()
                    or row["category"] != category
                    or ref["policy_pointer"] != f"/{category}/{index}"
                    or ref["document_sha256"] != presentation["sha256"]
                    or ref["document"] != presentation["file"]
                    or ref["page"] not in presentation["pages"]
                    or not ref["quote"].strip()
                    or ref["quote"] not in (pdf.pages[ref["page"] - 1].extract_text() or "")
                ):
                    raise ValueError("block description provenance mismatch")
        return data
