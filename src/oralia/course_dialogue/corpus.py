"""Selected academic pages from original PDFs; no student/admin content."""

import hashlib
from pathlib import Path

import pdfplumber

SOURCE_ROOT = Path(
    "C:\Users\<usuario>\\OneDrive - Universidad Politécnica de "
    "Madrid\\Docencia\\Ingeniería del software\\22-23\\Traspis"
)
SELECTION = {
    "procedure": ("6 - Procedimiento requisitos.pdf", (10, 11, 12)),
    "requirements": ("5 - Requisitos.pdf", (14, 53, 56, 72, 73, 74, 75, 76)),
    "testing": ("12 - Testing.pdf", (4, 7, 8, 9, 11, 15)),
}


def load_catalog(source_root=SOURCE_ROOT):
    result = []
    for key, (name, pages) in SELECTION.items():
        path = source_root / name
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        with pdfplumber.open(path) as pdf:
            for number in pages:
                text = pdf.pages[number - 1].extract_text() or ""
                if not text.strip():
                    raise ValueError(f"Academic page has no text: {name}, {number}")
                result.append(
                    {
                        "id": f"{key}:{number}",
                        "filename": name,
                        "original_sha256": digest,
                        "version": 1,
                        "page": number,
                        "text": text,
                        "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
                        "derivation": "mechanical_text_extraction",
                        "teacher_review": "pending",
                    }
                )
    return result


def select_pages(catalog, query, history=(), limit=8):
    if isinstance(catalog, SemanticCatalog):
        return catalog.select(query, history, limit)
    # General lexical retrieval for deterministic plumbing tests only.
    from oralia.domain.materials.query_excerpt import terms

    words = terms(query)
    # The caller supplies the resolved contextual query. Appending the last
    # input here would contaminate an explicit switch of academic focus.
    ranked = sorted(enumerate(catalog), key=lambda pair: (-len(words & terms(pair[1]["text"])), pair[0]))
    return [item for _, item in ranked[:limit] if words & terms(item["text"])]


class SemanticCatalog(list):
    """Local multilingual ranking; reuse installed embedding adapter, no new agent."""

    def __init__(self, pages, adapter=None):
        import os

        from oralia.infrastructure.embeddings.sentence_transformer_adapter import (
            SentenceTransformerEmbeddingAdapter,
        )

        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
        super().__init__(pages)
        self.adapter = adapter or SentenceTransformerEmbeddingAdapter()
        self.vectors = self.adapter.embed([p["text"] for p in pages])

    def select(self, query, history, limit):
        import collections
        import math
        import re

        from oralia.domain.materials.query_excerpt import normalized

        def lexical_terms(text):
            return {word[:7] for word in re.findall(r"[a-z]+", normalized(text)) if len(word) >= 4}

        q = self.adapter.embed([query])[0]

        def cosine(a, b):
            denominator = math.sqrt(sum(x * x for x in a) * sum(x * x for x in b))
            return sum(x * y for x, y in zip(a, b, strict=True)) / denominator if denominator else 0

        semantic = sorted(
            ((cosine(q, v), i) for i, v in enumerate(self.vectors)), key=lambda p: (-p[0], p[1])
        )
        tokens = [lexical_terms(p["text"]) for p in self]
        counts = collections.Counter(t for items in tokens for t in items)
        title_terms = set().union(*(lexical_terms(p.get("filename", "")) for p in self))
        query_terms = lexical_terms(query) - title_terms
        lexical = sorted(
            (
                (sum(math.log(1 + len(self) / (1 + counts[t])) for t in query_terms & items), i)
                for i, items in enumerate(tokens)
            ),
            key=lambda p: (-p[0], p[1]),
        )
        chosen = []
        # Diverse retrieval channels: neither lexical nor embedding ranking alone
        # may erase the only source that names an operation.
        for score, index in lexical[: limit // 2]:
            if score > 0:
                chosen.append(index)
        for score, index in semantic:
            if score >= 0.35 and index not in chosen:
                chosen.append(index)
            if len(chosen) >= limit:
                break
        return [self[i] for i in chosen[:limit]]
