"""Opt-in retrieval with bge-m3 dense search plus a Qwen3 reranker over the same reviewed pages.

Measured on 215 synthetic questions (docs/audits/2026-11-06-retrieval-bench): source page in the top 5 for 0.95
against 0.67 for the MiniLM + lexical fusion. The corpus mixes English slides and Spanish questions, so there is no
lexical branch. Pages, passages, budget and identity checks are those of `Retrieval`; only the ranking changes.
Ranking runs in a loopback GPU service (scripts/ranker_server.py) that reads the models from the local cache.
"""

import hashlib

import httpx

from oralia.documentary.retrieval import Retrieval, canonical, split_text
from oralia.documentary.study_errors import StudyFailure

EMBEDDER = "BAAI/bge-m3"
RERANKER = "Qwen/Qwen3-Reranker-0.6B"
CANDIDATES = 20


class ModernRetrieval:
    """Ranking by the loopback service `scripts/ranker_server.py` (GPU); the project process holds no model."""

    def __init__(self, *, ranker_url="http://127.0.0.1:8092", client=None, **options):
        self.base = Retrieval(**options)
        import numpy as np
        from transformers import AutoTokenizer

        self.np, self.url = np, ranker_url.rstrip("/")
        self.client = client or httpx.Client(timeout=120)
        try:
            self.client.get(self.url + "/health").raise_for_status()
        except httpx.HTTPError as error:
            raise ValueError(f"ranking service not available at {self.url}") from error
        self.tokenizer = AutoTokenizer.from_pretrained(EMBEDDER, local_files_only=True)
        chunks, self.owner = [], []
        for page_id, page in sorted(self.base.pages.items()):
            for _, _, chunk in split_text(page["text"], self.tokenizer, 512):
                chunks.append(chunk)
                self.owner.append(page_id)
        self.index = np.array(self.post("/embed", texts=chunks)["vectors"], dtype="float32")
        self.first_fragment = {}
        for fragment in self.base.fragments:
            self.first_fragment.setdefault(fragment["page_id"], fragment["id"])
        identity = {"base": self.base.fingerprint["revision"], "embedder": EMBEDDER, "reranker": RERANKER}
        self.fingerprint = dict(
            self.base.fingerprint,
            encoder=f"{EMBEDDER}+{RERANKER}",
            revision=hashlib.sha256(canonical(identity)).hexdigest(),
        )

    def __getattr__(self, name):  # pages, documents, manifest, config, revalidate, ...
        if name == "base":
            raise AttributeError(name)
        return getattr(self.base, name)

    def post(self, path, **body):
        response = self.client.post(self.url + path, json=body)
        response.raise_for_status()
        return response.json()

    def dense_pages(self, query):
        vector = self.np.array(self.post("/embed", texts=[query])["vectors"][0], dtype="float32")
        best = {}
        for score, page_id in zip(self.index @ vector, self.owner):
            if score > best.get(page_id, -2.0):
                best[page_id] = float(score)
        return [page_id for page_id, _ in sorted(best.items(), key=lambda kv: (-kv[1], kv[0]))[:CANDIDATES]]

    def rerank(self, query, page_ids):
        scores = self.post("/rerank", query=query, documents=[self.base.pages[i]["text"] for i in page_ids])["scores"]
        order = sorted(range(len(page_ids)), key=lambda i: (-scores[i], page_ids[i]))
        return [page_ids[i] for i in order], max(scores, default=None)

    def query(self, question, strategy="rerank", *, history=(), focus_change=False):
        if not question.strip() or len(question) > 2000:
            raise ValueError("invalid retrieval request")
        self.base.revalidate()
        query = question if focus_change else " ".join([*history[-2:], question])
        if len(self.tokenizer.encode(query, add_special_tokens=True, truncation=False)) > 512:
            raise StudyFailure("search_context_too_long")
        try:
            pages, relevance = self.rerank(query, self.dense_pages(query))
        except httpx.HTTPError as error:
            raise StudyFailure("retrieval_error") from error
        ranked = [self.first_fragment[page_id] for page_id in pages]
        result = self.base.assemble(ranked, question, history, focus_change, strategy)  # the caller binds the strategy name it asked for
        result["identity"] = self.fingerprint["revision"]
        result["ranking"] = "bge-m3+rerank"
        # Probability that the best page answers the question (reranker): used to say "the material does not cover this".
        result["relevance"] = relevance
        return result
