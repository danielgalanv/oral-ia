"""CUDA-graph decode loop for the standalone GPU worker; no ORALIA imports, torch passed in.

Eager ``generate`` is bound by CPU kernel-launch overhead (~20 tok/s on this host). The decode
step is captured once per static-cache tier and replayed with a single launch; sampling runs
outside the graph. Only plain sampling for registered Qwen-family models is eligible: finite
decoders and anything unrecognised keep using ``generate``. Output is not bit-identical to
``generate`` (static cache numerics), so equivalence is a measured property, not a promise.
"""

import time

TIERS = (2048, 3072, 4096, 6144, 8192, 12288, 16384)  # finer tiers: attention scans the whole static cache
MAX_RESIDENT_TIERS = 4  # least-recently-used tiers are released to bound KV memory
CHUNK = 8  # host synchronisation (EOS/deadline) every CHUNK tokens
START_HEADROOM = 512
PREWARM_TIERS = (2048, 4096, 6144, 8192)  # captured at start so no request pays for graph capture
SUPPORTED_MODEL_TYPES = {"qwen2", "qwen3"}
SUPPORTED_OPTIONS = {"do_sample", "temperature", "top_p", "top_k", "min_p", "repetition_penalty"}
DECODER_NAME = "cuda_graph/v1"


def eligible(model_type, sample_options, finite_outputs, input_length, max_new_tokens):
    return (
        finite_outputs is None
        and model_type in SUPPORTED_MODEL_TYPES
        and set(sample_options) <= SUPPORTED_OPTIONS
        and not sample_options.get("min_p")
        and input_length + max_new_tokens <= TIERS[-1]
    )


def sample_next(torch, logits, seen, options):
    """One token from (1, V) logits following HF's processor order; stays on the device."""
    x = logits.float()
    penalty = options.get("repetition_penalty")
    if penalty and penalty != 1.0:
        x = torch.where(seen, torch.where(x < 0, x * penalty, x / penalty), x)
    if not options.get("do_sample"):
        return x.argmax(-1, keepdim=True)
    x = x / options.get("temperature", 1.0)
    top_k = options.get("top_k")
    if top_k and top_k > 0:
        kth = torch.topk(x, min(top_k, x.shape[-1])).values[:, -1:]
        x = x.masked_fill(x < kth, float("-inf"))
    top_p = options.get("top_p")
    if top_p is not None and top_p < 1.0:
        ordered, index = torch.sort(x, descending=True)
        probs = ordered.softmax(-1)
        drop = (probs.cumsum(-1) - probs) >= top_p  # the first token is always kept
        x = torch.full_like(x, float("-inf")).scatter(1, index, ordered.masked_fill(drop, float("-inf")))
    return torch.multinomial(x.softmax(-1), 1)


ATTENTION_NAME = "oralia_gqa_decode"


def install_gqa_decode_attention(torch, model):
    """Single-query attention that never materialises the repeated K/V (grouped-query attention).

    The stock SDPA path repeats K/V once per query group whenever a mask is present, which multiplies the
    memory traffic of every decode step on long contexts. Prefill and anything with more than one query keep
    the stock implementation, so only the decode step changes.
    """
    from transformers import AttentionInterface
    from transformers.integrations.sdpa_attention import sdpa_attention_forward

    def attention(
        module, query, key, value, attention_mask, dropout=0.0, scaling=None, is_causal=None, **kwargs
    ):
        if query.shape[2] != 1 or not hasattr(module, "num_key_value_groups"):
            return sdpa_attention_forward(
                module,
                query,
                key,
                value,
                attention_mask,
                dropout=dropout,
                scaling=scaling,
                is_causal=is_causal,
                **kwargs,
            )
        batch, heads, _, dim = query.shape
        groups = module.num_key_value_groups
        scale = scaling if scaling is not None else dim**-0.5
        scores = torch.matmul(query.view(batch, heads // groups, groups, dim), key.transpose(-1, -2)) * scale
        if attention_mask is not None:
            mask = attention_mask[:, :, :, : key.shape[-2]]
            scores = scores.masked_fill(~mask, float("-inf")) if mask.dtype == torch.bool else scores + mask
        probs = scores.float().softmax(-1).to(value.dtype)
        out = torch.matmul(probs, value).view(batch, heads, 1, dim)
        return out.transpose(1, 2).contiguous(), None

    AttentionInterface.register(ATTENTION_NAME, attention)
    model.set_attn_implementation(ATTENTION_NAME)


def kv_bytes_per_token(config):
    head_dim = getattr(config, "head_dim", None) or config.hidden_size // config.num_attention_heads
    return config.num_hidden_layers * 2 * config.num_key_value_heads * head_dim * 2


class GraphDecoder:
    def __init__(self, torch, model, eos_ids):
        self.torch, self.model = torch, model
        self.eos = sorted({int(i) for i in eos_ids})
        self.tiers = {}
        self.pool = None
        self.growths = 0  # mid-answer cache-tier changes, for diagnostics

    def _tier(self, size):
        torch = self.torch
        found = self.tiers.get(size)
        if found:
            self.tiers[size] = self.tiers.pop(size)  # most recently used last
            return found
        while len(self.tiers) >= MAX_RESIDENT_TIERS:
            oldest = self.tiers.pop(next(iter(self.tiers)))
            if oldest["graph"] is not None:
                oldest["graph"].reset()
            oldest.clear()
            torch.cuda.empty_cache()
        from transformers import StaticCache

        need = int(kv_bytes_per_token(self.model.config) * size * 1.25) + 512 * 1024**2
        # Memory the allocator already holds but is not using also serves the new cache.
        available = (
            torch.cuda.mem_get_info()[0] + torch.cuda.memory_reserved() - torch.cuda.memory_allocated()
        )
        if available < need:
            raise MemoryError(f"static cache tier {size} needs {need} bytes")
        found = dict(
            size=size,
            cache=StaticCache(config=self.model.config, max_cache_len=size),
            ids=torch.zeros((1, 1), dtype=torch.long, device="cuda"),
            pos=torch.zeros(1, dtype=torch.long, device="cuda"),
            graph=None,
            logits=None,
        )
        self.tiers[size] = found
        return found

    def _step(self, tier):
        out = self.model(
            input_ids=tier["ids"],
            position_ids=tier["pos"].view(1, 1),
            cache_position=tier["pos"],
            past_key_values=tier["cache"],
            use_cache=True,
        )
        return out.logits[:, -1, :]

    def _capture(self, tier):
        torch = self.torch
        side = torch.cuda.Stream()
        side.wait_stream(torch.cuda.current_stream())
        with torch.cuda.stream(side):
            for _ in range(3):
                self._step(tier)
        torch.cuda.current_stream().wait_stream(side)
        tier["graph"] = torch.cuda.CUDAGraph()
        if self.pool is None:  # all tiers share one private pool: only one graph replays at a time
            self.pool = torch.cuda.graph_pool_handle()
        with torch.cuda.graph(tier["graph"], pool=self.pool):
            tier["logits"] = self._step(tier)

    def generate(self, input_ids, max_new_tokens, options, deadline):
        """Never builds an autograd graph, whatever the caller's grad mode (it would hold ~20 GB)."""
        with self.torch.inference_mode():
            return self._generate(input_ids, max_new_tokens, options, deadline)

    def _generate(self, input_ids, max_new_tokens, options, deadline):
        """Return the generated ids (1-D tensor, EOS included like `generate`) or raise."""
        torch = self.torch
        vocab = self.model.config.vocab_size
        prompt_len = input_ids.shape[1]
        seen = None
        if options.get("repetition_penalty"):
            seen = torch.zeros((1, vocab), dtype=torch.bool, device="cuda").scatter_(1, input_ids, True)
        eos = torch.tensor(self.eos, device="cuda")
        tokens = torch.empty(max_new_tokens, dtype=torch.long, device="cuda")
        size = next(t for t in TIERS if t >= min(prompt_len + START_HEADROOM, TIERS[-1]) or t == TIERS[-1])
        tier, logits = self._prefill(input_ids, size)
        n = checked = 0

        def finish(limit):
            hit = torch.isin(tokens[checked:limit], eos).nonzero()
            return checked + int(hit[0, 0]) + 1 if len(hit) else None

        while True:
            token = sample_next(torch, logits, seen, options)
            tokens[n : n + 1] = token.view(1)
            if seen is not None:
                seen.scatter_(1, token, True)
            n += 1
            if n % CHUNK == 0 or n == max_new_tokens:
                stop = finish(n)
                if stop is not None:
                    return tokens[:stop]
                checked = n
                if n >= max_new_tokens or time.monotonic() >= deadline:
                    return tokens[:n]
            position = prompt_len + n - 1  # where `token` is fed next
            if position >= tier["size"]:
                stop = finish(n)
                if stop is not None:
                    return tokens[:stop]
                checked = n
                self.growths += 1
                size = next(t for t in TIERS if t > tier["size"])
                prefix = torch.cat([input_ids, tokens[:n].view(1, -1)], dim=1)
                tier, logits = self._prefill(prefix, size)
                continue
            tier["ids"].copy_(token)
            tier["graph"].replay()
            tier["pos"].add_(1)
            logits = tier["logits"]

    def prewarm(self, sizes=PREWARM_TIERS, token_id=0):
        dummy = self.torch.full((1, 8), token_id, dtype=self.torch.long, device="cuda")
        with self.torch.inference_mode():
            for size in sizes:
                self._prefill(dummy, size)
        self.torch.cuda.synchronize()

    def _prefill(self, prefix, size):
        """Prefill into the tier, capturing its graph on first use; return fresh logits."""
        torch = self.torch
        tier = self._tier(size)
        length = prefix.shape[1]
        if length >= size:
            raise ValueError("prefix does not fit its cache tier")

        def run():
            tier["cache"].reset()
            out = self.model(
                input_ids=prefix,
                cache_position=torch.arange(length, device="cuda"),
                past_key_values=tier["cache"],
                use_cache=True,
                logits_to_keep=1,
            )
            tier["pos"].fill_(length)
            return out.logits[:, -1, :]

        logits = run()
        if tier["graph"] is None:
            tier["ids"].copy_(prefix[:, -1:])  # warm/capture writes at `pos` are overwritten by the real step
            self._capture(tier)
            logits = run()
        return tier, logits
