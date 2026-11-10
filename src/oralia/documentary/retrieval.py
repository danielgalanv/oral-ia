"""Opt-in retrieval-only composition for the reviewed v2 teacher package.

No generation or participant authority. All persisted data lives under a new root.
"""

import hashlib
import importlib.metadata
import json
import os
from pathlib import Path

from oralia.documentary.__main__ import CURRENT_PACKAGE, PACKAGES, confined, load_package
from oralia.documentary.study_errors import StudyFailure
from oralia.domain.materials.query_excerpt import terms
from oralia.infrastructure.embeddings.sentence_transformer_adapter import SentenceTransformerEmbeddingAdapter

ROOT = Path(__file__).resolve().parents[3]
DERIVED = ROOT / "materiales/docente/piloto-requisitos/recuperacion-v2.1"
SNAPSHOT = (
    Path.home()
    / ".cache/huggingface/hub/models--sentence-transformers--paraphrase-multilingual-MiniLM-L12-v2"
    / "snapshots/e8f8c211226b894fcb81acc59f3b34ba3efd5f42"
)
PROTOCOL = ROOT / "docs/audits/2026-10-27-retrieval-increment/protocol-v1.json"


def digest(value):
    return hashlib.sha256(value).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def offline():
    # This is an opt-in process entrypoint, never called by the ordinary profile.
    os.environ.update(
        HF_HUB_OFFLINE="1",
        TRANSFORMERS_OFFLINE="1",
        HF_HUB_DISABLE_TELEMETRY="1",
        CUDA_VISIBLE_DEVICES="",
        ANONYMIZED_TELEMETRY="False",
        HTTP_PROXY="http://127.0.0.1:9",
        HTTPS_PROXY="http://127.0.0.1:9",
        NO_PROXY="127.0.0.1,localhost",
    )


def source_snapshot(package, manifest_name="manifest-v2.json"):
    manifest, pages = load_package(package, manifest_name)
    files = {manifest_name: digest((package / manifest_name).read_bytes())}
    for doc in manifest["documents"]:
        for field in ("original", "extraction"):
            files[doc[field]] = digest(confined(package, doc[field]).read_bytes())
    return manifest, pages, files


def split_text(text, tokenizer, limit):
    """Exact character partition; special tokens counted, no encode truncation.

    Prefer whole lines (including table rows). A line exceeding capacity is split
    with offsets; the full reviewed page supplies table headers and continuation.
    """

    def count(s):
        return len(tokenizer.encode(s, add_special_tokens=True, truncation=False))

    start = 0
    while start < len(text):
        low, high = start + 1, len(text)
        best = start
        while low <= high:
            mid = (low + high) // 2
            if count(text[start:mid]) <= limit:
                best, low = mid, mid + 1
            else:
                high = mid - 1
        if best == start:
            raise ValueError("tokenizer capacity cannot hold a character")
        if best < len(text):
            newline = text.rfind("\n", start, best)
            if newline > start:
                best = newline + 1
        chunk = text[start:best]
        if count(chunk) > limit:
            raise ValueError("fragment exceeds effective token limit")
        yield start, best, chunk
        start = best


class Retrieval:
    def __init__(self, root=DERIVED, package=None, *, build=False, selection_profile=None, manifest_name=None):
        if selection_profile not in {None, "comparison-coverage/v1"}:
            raise ValueError("Unknown retrieval selection profile")
        self.selection_profile = selection_profile
        offline()
        self.root = Path(root)
        default_package, default_manifest = PACKAGES[CURRENT_PACKAGE]
        self.package = package or default_package
        self.manifest_name = manifest_name or (default_manifest if package is None else "manifest-v2.json")
        if self.root.resolve() == self.package.resolve() or self.root.resolve().is_relative_to(
            self.package.resolve()
        ):
            raise ValueError("derived root must be isolated from source package")
        self.manifest, pages, self.sources = source_snapshot(self.package, self.manifest_name)
        self.pages = {
            p["id"]: dict(p, document_id=doc)
            for doc, rows in pages.items()
            for p in rows
            if p["status"] == "disponible"
        }
        if len(self.pages) != sum(p["status"] == "disponible" for rows in pages.values() for p in rows):
            raise ValueError("duplicate page identity")
        self.documents = {d["id"]: d for d in self.manifest["documents"]}
        self.config = json.loads(PROTOCOL.read_text(encoding="utf8"))
        # Fail before loading if any required local resource is absent.
        required = [
            "config.json",
            "tokenizer.json",
            "tokenizer_config.json",
            "modules.json",
            "sentence_bert_config.json",
            "1_Pooling/config.json",
        ]
        if not SNAPSHOT.is_dir() or any(not (SNAPSHOT / f).is_file() for f in required):
            raise ValueError("required local encoder/tokenizer resource absent; no download")
        model_files = {
            str(f.relative_to(SNAPSHOT)): digest(f.read_bytes())
            for f in sorted(SNAPSHOT.rglob("*"))
            if f.is_file()
        }
        if not any(f.endswith((".safetensors", ".bin")) for f in model_files):
            raise ValueError("local encoder weights absent")
        self.adapter = SentenceTransformerEmbeddingAdapter(str(SNAPSHOT), device="cpu", normalize=True)
        self.model = self.adapter._get_model()
        if str(self.model.device) != "cpu":
            raise ValueError("explicit CPU not confirmed")
        self.tokenizer = self.model.tokenizer
        self.limit = min(self.model.max_seq_length, self.tokenizer.model_max_length)
        effective = {
            "snapshot": SNAPSHOT.name,
            "files": model_files,
            "dimension": self.model.get_embedding_dimension(),
            "pooling": str(self.model[1]),
            "normalization": "l2",
            "device": "cpu",
            "limit_with_specials": self.limit,
            "versions": {
                x: importlib.metadata.version(x)
                for x in ["sentence-transformers", "transformers", "tokenizers", "torch", "chromadb"]
            },
            "representation": "reviewed-v2-exact-character-offsets/v1",
            "implementation_sha256": digest(Path(__file__).read_bytes()),
            "adapter_sha256": digest(
                (ROOT / "src/oralia/infrastructure/embeddings/sentence_transformer_adapter.py").read_bytes()
            ),
            "protocol_sha256": digest(PROTOCOL.read_bytes()),
            "sources": self.sources,
        }
        self.identity = effective
        self.fingerprint = {
            "encoder": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            "revision": digest(canonical(effective)),
            "dimension": effective["dimension"],
            "normalization": "l2;mean-pooling;cpu",
            "representation": effective["representation"],
            "extraction": digest(canonical(self.sources)),
            "chunking": f"exact-offset-lines/v1;specials-included;limit={self.limit}",
        }
        from oralia.infrastructure.vector_store.chroma_store import ChromaVectorStore

        receipt = self.root / "identity.json"
        exists = receipt.is_file()
        if exists and json.loads(receipt.read_text(encoding="utf8")) != effective:
            raise ValueError("effective identity mismatch; refusing query or rebuild")
        if not exists and not build:
            raise ValueError("isolated index absent; explicit build required")
        if not exists and self.root.exists() and any(self.root.iterdir()):
            raise ValueError("unknown derived root; refusing overwrite")
        self.fragments = []
        for id, page in sorted(self.pages.items()):
            for start, end, text in split_text(page["text"], self.tokenizer, self.limit):
                self.fragments.append(
                    {"id": f"{id}@{start}:{end}", "page_id": id, "start": start, "end": end, "text": text}
                )
        self.by_id = {f["id"]: f for f in self.fragments}
        self.store = ChromaVectorStore(str(self.root / "chroma"), fingerprint=self.fingerprint)
        if not exists:
            embeddings = self.adapter.embed([f["text"] for f in self.fragments])
            self.revalidate()
            self.store.rebuild(
                [
                    (f["id"], v, {"course_id": self.manifest["package_id"]})
                    for f, v in zip(self.fragments, embeddings, strict=True)
                ]
            )
            (self.root / "fragments.json").write_bytes(canonical(self.fragments))
            receipt.write_bytes(canonical(effective))
        elif json.loads((self.root / "fragments.json").read_text(encoding="utf8")) != self.fragments:
            raise ValueError("stored representation changed")
        self.revalidate()

    def revalidate(self):
        for name, expected in self.sources.items():
            if digest(confined(self.package, name).read_bytes()) != expected:
                raise ValueError("package changed or withdrawn; reopen a new isolated version")

    def query(self, question, strategy="lexical", *, history=(), focus_change=False):
        if strategy not in self.config["strategies"] or not question.strip() or len(question) > 2000:
            raise ValueError("invalid retrieval request")
        self.revalidate()
        if len(self.tokenizer.encode(question, add_special_tokens=True, truncation=False)) > self.limit:
            raise StudyFailure("question_too_long")
        query = question if focus_change else " ".join([*history[-2:], question])
        if len(self.tokenizer.encode(query, add_special_tokens=True, truncation=False)) > self.limit:
            raise StudyFailure("search_context_too_long")
        qt = terms(query)
        # Reuse existing lexical terms and weighted match count. No bank vocabulary.
        lexical = sorted(
            [(4 * len(qt & terms(f["text"])), f["id"]) for f in self.fragments], key=lambda x: (-x[0], x[1])
        )
        lexical = [id for score, id in lexical if score > 0][: self.config["candidates"]]
        dense = []
        if strategy in {"dense", "rrf"}:
            embedding = self.adapter.embed([query])[0]
            matches = self.store.query(
                embedding, {"course_id": self.manifest["package_id"]}, self.config["candidates"]
            )
            dense = [
                m.fragment_id for m in sorted(matches, key=lambda m: (-m.relevance_score, m.fragment_id))
            ]
            if any(id not in self.by_id for id in dense):
                raise ValueError("index returned foreign fragment")
        if strategy == "rrf":
            scores = {}
            for ranking in (lexical, dense):
                for position, id in enumerate(ranking, 1):
                    scores[id] = scores.get(id, 0) + 1 / (self.config["rrf_k"] + position)
            ranked = sorted(scores, key=lambda id: (-scores[id], id))[: self.config["candidates"]]
        else:
            ranked = lexical if strategy == "lexical" else dense
        return self.assemble(ranked, question, history, focus_change, strategy)

    def assemble(self, ranked, question, history, focus_change, strategy):
        """Whole reviewed pages in rank order under the context budget (shared by every ranking strategy)."""
        selection = None
        if getattr(self, "selection_profile", None) == "comparison-coverage/v1":
            from oralia.documentary.comparison_coverage import diversify

            ranked, selection = diversify(ranked, self.by_id, self.pages, question, history, focus_change)
        passages, seen, chars, omitted = [], set(), 0, []
        for id in ranked:
            f = self.by_id[id]
            p = self.pages[f["page_id"]]
            if p["id"] in seen:
                continue
            if selection is not None and len(passages) >= self.config["context_units"]:
                seen.add(p["id"])
                omitted.append({"id": p["id"], "reason": "context unit limit"})
                continue
            # Deliver whole reviewed pages: never sever table/header relationships.
            # Over-budget pages remain candidates, with explicit omission evidence.
            if chars + len(p["text"]) > self.config["context_chars"]:
                omitted.append({"id": p["id"], "reason": "whole-page context exceeds remaining budget"})
                continue
            doc = self.documents[p["document_id"]]
            passages.append(
                {
                    "fragment": f,
                    "id": p["id"],
                    "text": p["text"],
                    "document_id": doc["id"],
                    "filename": doc["filename"],
                    "author": doc["author"],
                    "edition": doc["edition"],
                    "page": p["page"],
                    "printed_page": p.get("printed_page"),
                    "section": p["section"],
                    "derivation": p["derivation"],
                    "source_sha256": doc["sha256"],
                    "text_sha256": p["text_sha256"],
                    "raw_text_sha256": digest(p["raw_text"].encode()),
                    "original_url": f"/api/v1/documentary/{doc['id']}/original"
                    + (f"#page={p['page']}" if doc["original"].endswith(".pdf") else ""),
                }
            )
            chars += len(p["text"])
            seen.add(p["id"])
            if selection is None and len(passages) >= self.config["context_units"]:
                break
        self.revalidate()  # includes changes while encoding/querying
        return {
            "strategy": strategy,
            "candidates": [self.by_id[id] for id in ranked],
            "passages": passages,
            "context_chars": chars,
            "omitted_context": omitted,
            "selection": selection,
            "sufficiency": "not_assessed",
            "notice": (
                "Pasajes recuperados. El ranking no acredita verdad, " "suficiencia ni exclusión del temario."
            ),
            "identity": self.fingerprint["revision"],
        }
