import pytest
import torch

from oralia.course_dialogue import graph_decoder as g


def logits(*values):
    return torch.tensor([values], dtype=torch.float32)


def seen_none(vocab):
    return torch.zeros((1, vocab), dtype=torch.bool)


def test_greedy_and_top_k_one_pick_the_argmax():
    x = logits(0.1, 3.0, 0.2, 1.0)
    assert g.sample_next(torch, x, None, {"do_sample": False}).item() == 1
    torch.manual_seed(0)
    assert g.sample_next(torch, x, None, {"do_sample": True, "top_k": 1}).item() == 1


def test_top_p_keeps_at_least_the_first_token_and_never_samples_the_tail():
    x = logits(10.0, 0.0, 0.0, 0.0)
    for seed in range(20):
        torch.manual_seed(seed)
        assert g.sample_next(torch, x, None, {"do_sample": True, "top_p": 0.5}).item() == 0
    x = logits(2.0, 2.0, -50.0, -50.0)
    picks = set()
    for seed in range(40):
        torch.manual_seed(seed)
        picks.add(g.sample_next(torch, x, None, {"do_sample": True, "top_p": 0.95}).item())
    assert picks == {0, 1}


def test_repetition_penalty_moves_seen_tokens_like_hf():
    x = logits(2.0, 1.9, -1.0)
    seen = seen_none(3)
    seen[0, 0] = True
    assert g.sample_next(torch, x, seen, {"do_sample": False, "repetition_penalty": 1.5}).item() == 1
    assert g.sample_next(torch, x, seen, {"do_sample": False}).item() == 0


def test_temperature_changes_distribution_but_is_reproducible_with_the_seed():
    x = logits(1.0, 0.9, 0.8, 0.7)
    opts = {"do_sample": True, "temperature": 0.6, "top_k": 3, "top_p": 0.95}
    runs = []
    for _ in range(2):
        torch.manual_seed(42)
        runs.append([g.sample_next(torch, x, None, opts).item() for _ in range(10)])
    assert runs[0] == runs[1] and set(runs[0]) <= {0, 1, 2}


@pytest.mark.parametrize(
    "model_type,options,finite,n,m,expected",
    [
        (
            "qwen3",
            {"do_sample": True, "temperature": 0.6, "top_k": 20, "top_p": 0.95, "min_p": 0.0},
            None,
            3000,
            6144,
            True,
        ),
        ("qwen2", {"do_sample": False}, None, 100, 512, True),
        ("qwen3", {"do_sample": False}, ["a"], 100, 512, False),  # finite decoder stays on generate
        ("mistral", {"do_sample": False}, None, 100, 512, False),
        ("qwen3", {"do_sample": True, "min_p": 0.1}, None, 100, 512, False),
        ("qwen3", {"do_sample": True, "typical_p": 0.9}, None, 100, 512, False),
        ("qwen3", {"do_sample": False}, None, 9000, 8192, False),  # exceeds the largest tier
    ],
)
def test_only_registered_plain_sampling_is_eligible(model_type, options, finite, n, m, expected):
    assert g.eligible(model_type, options, finite, n, m) is expected


def test_kv_budget_matches_known_qwen3_8b_shape():
    class Config:
        num_hidden_layers, num_key_value_heads, head_dim = 36, 8, 128

    assert g.kv_bytes_per_token(Config) == 36 * 2 * 8 * 128 * 2


def test_grouped_query_decode_attention_matches_stock_attention_on_a_tiny_model():
    from transformers import Qwen3Config, Qwen3ForCausalLM

    torch.manual_seed(0)
    config = Qwen3Config(
        vocab_size=128,
        hidden_size=64,
        intermediate_size=128,
        num_hidden_layers=2,
        num_attention_heads=8,
        num_key_value_heads=2,
        head_dim=16,
        max_position_embeddings=64,
    )
    model = Qwen3ForCausalLM(config).eval()
    ids = torch.randint(0, 128, (1, 12))

    def step_logits():
        with torch.no_grad():
            out = model(input_ids=ids, use_cache=True)
            nxt = out.logits[:, -1:].argmax(-1)
            return model(input_ids=nxt, past_key_values=out.past_key_values, use_cache=True).logits[:, -1]

    stock = step_logits()
    g.install_gqa_decode_attention(torch, model)
    assert model.config._attn_implementation == g.ATTENTION_NAME
    patched = step_logits()
    assert torch.allclose(stock, patched, atol=1e-4, rtol=1e-4)
