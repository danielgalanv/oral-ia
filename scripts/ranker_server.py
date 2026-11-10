"""Loopback ranking service: bge-m3 embeddings and Qwen3-Reranker scores on the GPU.

Run with a Python that has CUDA torch and transformers (the project venv is CPU-only):
    D:/ai-toolkit/venv/Scripts/python.exe scripts/ranker_server.py [--port 8092]
Models come from the local Hugging Face cache; nothing is downloaded. Endpoints (JSON, 127.0.0.1 only):
    POST /embed  {"texts": [...]}                -> {"vectors": [[...], ...]}  (L2-normalised, CLS pooling)
    POST /rerank {"query": "...", "documents": [...]} -> {"scores": [...]}     (P(yes), 0..1)
    GET  /health
"""

import argparse
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", HF_HUB_DISABLE_TELEMETRY="1")
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import torch  # noqa: E402
from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer  # noqa: E402

EMBEDDER, RERANKER = "BAAI/bge-m3", "Qwen/Qwen3-Reranker-0.6B"
PAGE_CHARS, MAX_RERANK_TOKENS = 2500, 1400
PREFIX = (
    "<|im_start|>system\nJudge whether the Document meets the requirements based on the Query and the Instruct "
    'provided. Note that the answer can only be "yes" or "no".<|im_end|>\n<|im_start|>user\n'
)
SUFFIX = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
INSTRUCTION = (
    "Dada una pregunta de un estudiante en español, encuentra la página del material de la asignatura "
    "(en español o inglés) que contiene la respuesta"
)

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16 if device == "cuda" else torch.float32
embed_tok = AutoTokenizer.from_pretrained(EMBEDDER)
embed_model = AutoModel.from_pretrained(EMBEDDER, dtype=dtype).to(device).eval()
rank_tok = AutoTokenizer.from_pretrained(RERANKER, padding_side="left")
rank_model = AutoModelForCausalLM.from_pretrained(RERANKER, dtype=dtype).to(device).eval()
YES, NO = rank_tok.convert_tokens_to_ids("yes"), rank_tok.convert_tokens_to_ids("no")
lock = threading.Lock()


def embed(texts, batch=16):
    out = []
    for start in range(0, len(texts), batch):
        enc = embed_tok(texts[start : start + batch], padding=True, truncation=True, max_length=512, return_tensors="pt")
        with torch.inference_mode():
            hidden = embed_model(**enc.to(device)).last_hidden_state[:, 0]
        out += torch.nn.functional.normalize(hidden.float(), dim=-1).cpu().tolist()
    return out


def rerank(query, documents, batch=5):
    scores = []
    for start in range(0, len(documents), batch):
        texts = [
            f"{PREFIX}<Instruct>: {INSTRUCTION}\n<Query>: {query}\n<Document>: {d[:PAGE_CHARS]}{SUFFIX}"
            for d in documents[start : start + batch]
        ]
        enc = rank_tok(texts, padding=True, truncation=True, max_length=MAX_RERANK_TOKENS, return_tensors="pt")
        with torch.inference_mode():
            logits = rank_model(**enc.to(device)).logits[:, -1, :]
        pair = torch.stack([logits[:, NO], logits[:, YES]], 1).float()
        scores += torch.softmax(pair, 1)[:, 1].cpu().tolist()
    return scores


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self.reply(200 if self.path == "/health" else 404, {"status": "ok", "device": device})

    def do_POST(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            with lock:
                try:
                    if self.path == "/embed":
                        return self.reply(200, {"vectors": embed(body["texts"])})
                    if self.path == "/rerank":
                        return self.reply(200, {"scores": rerank(body["query"], body["documents"])})
                finally:
                    # Return the activation memory: the GPU is shared with the llama.cpp servers and a few MB
                    # held here push their weights out of VRAM (the servers then slow down 10x).
                    if device == "cuda":
                        torch.cuda.empty_cache()
            self.reply(404, {"error": "unknown endpoint"})
        except Exception as error:  # a malformed request must not stop the service
            self.reply(400, {"error": str(error)[:200]})

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8092)
    port = parser.parse_args().port
    print(f"ranker listo en 127.0.0.1:{port} ({device})", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
