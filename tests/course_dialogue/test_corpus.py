"""Multilingual rank plumbing using synthetic vectors; real retrieval measured separately."""

from oralia.course_dialogue.corpus import SemanticCatalog, select_pages


def test_semantic_ranking_does_not_require_shared_words():
    class Adapter:
        def embed(self, texts):
            return [[1, 0] if text in {"foreign words", "pregunta española"} else [0, 1] for text in texts]

    c = SemanticCatalog(
        [{"id": "wanted", "text": "foreign words"}, {"id": "unrelated", "text": "different"}], Adapter()
    )
    assert [p["id"] for p in select_pages(c, "pregunta española")] == ["wanted"]


def test_zero_similarity_does_not_return_an_arbitrary_page():
    class Adapter:
        def embed(self, texts):
            return [[1, 0] if text == "source" else [0, 1] for text in texts]

    c = SemanticCatalog([{"id": "p", "text": "source"}], Adapter())
    assert select_pages(c, "unknown") == []


def test_lexical_channel_does_not_confuse_contractor_with_contradiction():
    class Adapter:
        def embed(self, texts):
            return [[0, 0] for _ in texts]

    c = SemanticCatalog(
        [
            {"id": "wrong", "text": "Contractor review"},
            {"id": "correct", "text": "No contradictions in requirements"},
        ],
        Adapter(),
    )
    assert [p["id"] for p in select_pages(c, "contradicción")] == ["correct"]
