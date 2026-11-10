"""Current-question-first retrieval; history remains the actual shown conversation."""

import re
import unicodedata


def referential(question):
    text = "".join(
        c for c in unicodedata.normalize("NFD", question.lower()) if unicodedata.category(c) != "Mn"
    )
    text = re.sub(r"[¿?¡!.,;:]", "", text).strip()
    return bool(
        re.fullmatch(
            r"(?:y )?(?:por que|como|y eso|eso por que|otro|otro mas|uno mas|que quiere decir|"
            r"como se haria|puedes aclararlo|aclaralo|aclaramelo|explicamelo|explicalo|no lo entiendo)",
            text,
        )
        # A long question carries its own context ("si un sistema debe funcionar en Windows y Linux, ¿cómo
        # clasificaríamos ese requisito?"): the demonstrative then points inside the question.
        or (
            len(text.split()) <= 10
            and re.search(
                r"\b(?:ese requisito|ese ejemplo|esa respuesta|lo anterior|mismo ejemplo|otra manera|"
                r"otra forma|reformularlo|explicarmelo|explicarlo)\b",
                text,
            )
        )
        or re.fullmatch(
            r"(?:pon|ponme|dame)(?: por favor)? (?:otro|un) ejemplo"
            r"(?: mas| sencillo| diferente| del mismo tipo| distinto del anterior)*",
            text,
        )
    )


def retrieval_context(question, history, manual=None):
    if manual is not None:
        return {
            "mode": "manual",
            "focus_change": manual,
            "references": [] if manual else [h["question"] for h in history[-2:]],
        }
    if not referential(question):
        return {"mode": "current_question", "focus_change": True, "references": []}
    anchor = next((h["question"] for h in reversed(history) if not referential(h["question"])), None)
    return {
        "mode": "followup" if anchor else "needs_referent",
        "focus_change": False,
        "references": [anchor] if anchor else [],
    }
