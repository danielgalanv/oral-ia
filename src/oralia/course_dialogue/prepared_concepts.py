"""Source-bound, content-addressed concept preparation; never a bank of answers."""

import hashlib
import json
import os
from pathlib import Path
from uuid import uuid4

from oralia.course_dialogue.concept_ledger import source_cards
from oralia.infrastructure.generation.generation_port import EvidenceItem

SCHEMA = "prepared-concepts/v1"
EXTRACTOR = "literal-bullets-and-full-context/v1"


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def prepare(
    root, evidence, source_files, *, corpus_id, locations=None, proposed_labels=None, revalidate=None
):
    """Build/reuse immutable documents; replace only the derived manifest atomically.

    source_files is the caller's currently authorised map, never a path from cache.
    Labels are optional proposals keyed by fragment and local card ID, not truths.
    """
    root = Path(root)
    if revalidate:
        revalidate()
    initial = {key: digest(path) for key, path in source_files.items()}
    root.mkdir(parents=True, exist_ok=True)
    documents = {}
    grouped = {}
    seen = set()
    for item in evidence:
        item = EvidenceItem.model_validate(item)
        if item.fragment_id in seen:
            raise ValueError("duplicate prepared fragment")
        seen.add(item.fragment_id)
        if item.document_id not in source_files:
            raise ValueError("source document not currently authorised")
        grouped.setdefault(item.document_id, []).append(item)
    for document, items in sorted(grouped.items()):
        versions = {item.document_version for item in items}
        if len(versions) != 1:
            raise ValueError("mixed document versions")
        pages = {}
        for item in sorted(items, key=lambda e: e.fragment_id):
            cards = source_cards([item])
            labels = (proposed_labels or {}).get(item.fragment_id, {})
            if not set(labels) <= {c["id"] for c in cards if c["source_name"]}:
                raise ValueError("proposed name has no literal definition")
            if any(not isinstance(v, str) or not v.strip() or len(v) > 120 for v in labels.values()):
                raise ValueError("invalid proposed name")
            pages[item.fragment_id] = dict(
                evidence=item.model_dump(),
                cards=cards,
                location=(locations or {}).get(item.fragment_id, {}),
                proposed_labels=labels,
                label_state="proposed_not_teacher_approved",
            )
        data = dict(
            schema=SCHEMA,
            extractor=EXTRACTOR,
            document_id=document,
            document_version=next(iter(versions)),
            original_sha256=initial[document],
            pages=pages,
        )
        encoded = canonical(data)
        key = hashlib.sha256(encoded).hexdigest()
        path = root / "documents" / f"{key}.json"
        path.parent.mkdir(exist_ok=True)
        if path.exists():
            if path.read_bytes() != encoded:
                raise ValueError("existing content-addressed document was altered")
        else:
            with path.open("xb") as stream:
                stream.write(encoded)
        documents[document] = key
    if not documents:
        raise ValueError("no authorised material to prepare")
    if any(digest(source_files[key]) != value for key, value in initial.items()):
        raise ValueError("original material changed during preparation")
    if revalidate:
        revalidate()
    manifest = dict(schema=SCHEMA, extractor=EXTRACTOR, corpus_id=corpus_id, documents=documents)
    temporary = root / f"manifest-{uuid4().hex}.tmp"
    temporary.write_bytes(canonical(manifest))
    os.replace(temporary, root / "manifest.json")
    return PreparedConcepts(root, source_files)


class PreparedConcepts:
    def __init__(self, root, source_files):
        self.root = Path(root).resolve()
        self.source_files = {key: Path(path) for key, path in source_files.items()}
        raw = (self.root / "manifest.json").read_bytes()
        self.revision = hashlib.sha256(raw).hexdigest()
        manifest = json.loads(raw)
        if manifest.get("schema") != SCHEMA or manifest.get("extractor") != EXTRACTOR:
            raise ValueError("unknown prepared concept schema/extractor")
        self.documents = {}
        for document, key in manifest["documents"].items():
            if not isinstance(key, str) or len(key) != 64 or any(c not in "0123456789abcdef" for c in key):
                raise ValueError("invalid content address")
            path = (self.root / "documents" / f"{key}.json").resolve()
            if not path.is_relative_to(self.root):
                raise ValueError("catalogue path escapes root")
            if digest(path) != key:
                raise ValueError("prepared definition file was altered")
            data = json.loads(path.read_bytes())
            if data.get("schema") != SCHEMA or data.get("extractor") != EXTRACTOR:
                raise ValueError("unknown prepared document")
            if data["document_id"] != document:
                raise ValueError("foreign prepared document")
            for fragment, page in data["pages"].items():
                item = EvidenceItem.model_validate(page["evidence"])
                if (item.document_id, item.document_version, item.fragment_id) != (
                    document,
                    data["document_version"],
                    fragment,
                ) or page["cards"] != source_cards([item]):
                    raise ValueError("prepared definition is not the literal source unit")
            self.documents[document] = data

    def project(self, evidence):
        """Project only exact retrieved evidence, after checking live original files."""
        cards, labels, seen = [], {}, set()
        requested = {item.document_id for item in evidence}
        for document in requested:
            if document not in self.source_files or document not in self.documents:
                raise ValueError("prepared source absent or no longer authorised")
            if digest(self.source_files[document]) != self.documents[document]["original_sha256"]:
                raise ValueError("original document changed; prepare affected document again")
        for item in evidence:
            if item.fragment_id in seen:
                raise ValueError("duplicate retrieved fragment")
            seen.add(item.fragment_id)
            page = self.documents[item.document_id]["pages"].get(item.fragment_id)
            if page is None or page["evidence"] != item.model_dump():
                raise ValueError("retrieved page/version/text differs from prepared source")
            for local in page["cards"]:
                key = f"C{len(cards)+1}"
                cards.append(dict(local, id=key))
                if local["id"] in page["proposed_labels"]:
                    labels[key] = page["proposed_labels"][local["id"]]
        if len(cards) > 64:
            raise ValueError("prepared turn exceeds unchanged card budget; nothing truncated")
        return dict(cards=cards, proposed_labels=labels, revision=self.revision)

    def for_turn(self, base, *, revalidate):
        from oralia.course_dialogue.concept_review_loop import source_binding

        revalidate()
        projected = self.project(base.evidence)
        revalidate()
        return dict(
            binding=source_binding(base),
            prepared_revision=self.revision,
            decision=dict(
                selected=[c["id"] for c in projected["cards"]],
                proposed_labels=projected["proposed_labels"],
                missing_definitions=[],
            ),
        )
