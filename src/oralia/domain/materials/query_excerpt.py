"""material-query-excerpt/v2: bounded literal bullet selection, no output authority.

Opt-in only. Offsets refer to the unmodified indexed fragment. Query heuristics
select quotations, never assess a participant or create a pedagogical answer.
"""

import re
import unicodedata
from dataclasses import dataclass
from hashlib import sha256

PROFILE_ID = "material-self-study/v2"
_STOP = set(
    (
        "que como por para con del las los una uno unos unas esto eso significa "
        "significado explica estudiar estudiando entiendo hola buenas tardes noches dias "
        "sistema software ingenieria diapositiva dice define quiero puedes pueda pueda "
        "cual hay hace hacer sirve sirven"
    ).split()
)
_GENERIC = {"objet", "riesg", "tarea", "model"}
_ACTION_WORDS = "hacer hacerlo hacemos hariamos haria realizamos realizar tareas riesgos procedimiento pasos"


def normalized(text):
    return "".join(c for c in unicodedata.normalize("NFD", text.lower()) if unicodedata.category(c) != "Mn")


def terms(text):
    return {
        re.sub(r"(?:ar|er|ir|es|os|as|s)$", "", word)[:5]
        for word in re.findall(r"[a-z]+", normalized(text))
        if len(word) > 2 and word not in _STOP
    }


@dataclass(frozen=True)
class QueryExcerpt:
    fragment_id: str
    text: str
    start: int
    end: int
    source_sha256: str


def select_query_excerpts(evidence, query):
    """At most two whole blocks from at most eight current caller-supplied fragments.

    This function grants no permission: the binder independently re-reads rows,
    checks identity/lifecycle/course/activity and reconstructs every selected span.
    """
    if not isinstance(query, str) or not query.strip() or len(query) > 4000:
        return []
    value = normalized(query)
    if re.search(r"ejemplo|inventa|genera un", value):
        return []  # This closed profile does not generate examples.
    comparison = bool(re.search(r"compar|diferen|versus", value))
    kind = "objetivo"
    if re.search(r"riesg|salir mal|si no", value):
        kind = "riesgos"
    elif re.search(r"como|tareas|realiz|haria|hacemos", value):
        kind = "tareas"
    query_terms = terms(query)
    query_label_words = set(re.findall(r"[a-z]+", value))
    blocks = []
    for item in list(evidence)[:8]:
        source = item.text if hasattr(item, "text") else item["text"]
        key = str(item.fragment_id if hasattr(item, "fragment_id") else item["fragment_id"])
        if not isinstance(source, str) or len(source) > 20000:
            continue
        footer = re.search(r"(?m)^(?:\d{1,2}/\d{1,2}/\d{4}|Chapter\s+\d)", source)
        end_of_body = footer.start() if footer else len(source)
        bullets = list(re.finditer(r"(?m)^[ \t]*[•▪]\s*", source[:end_of_body]))
        heading = source[: bullets[0].start()].strip() if bullets else ""
        for index, match in enumerate(bullets):
            end = bullets[index + 1].start() if index + 1 < len(bullets) else end_of_body
            start = match.start()
            while start < end and source[start].isspace():
                start += 1
            while end > start and source[end - 1].isspace():
                end -= 1
            content = source[start:end]
            label = re.split(r"[:.\n]", source[match.end() : end], maxsplit=1)[0]
            label_terms = terms(label) - _GENERIC
            label_words = set(re.findall(r"[a-z]+", normalized(label))) - {"no", "el", "la"}
            exact_label = bool(label_terms and label_words and label_words <= query_label_words)
            label_kind = normalized(label).strip()
            if not exact_label and not (
                label_kind.startswith("objetivo") if comparison else label_kind.startswith(kind)
            ):
                continue
            # A structural field may refer to an object declared elsewhere in
            # this same source (e.g. its objective). Never infer a missing object.
            object_terms = query_terms - terms(_ACTION_WORDS)
            contextual_field = (
                not comparison
                and kind in {"tareas", "riesgos"}
                and label_kind.startswith(kind)
                and bool(object_terms)
                and object_terms <= terms(source[:end_of_body])
            )
            score = (
                (1 if contextual_field else 0)
                + (100 if exact_label else 0)
                + 4 * len(query_terms & terms(heading))
                + len(query_terms & terms(content))
            )
            if score <= 0 or end - start > 1000:
                continue
            # Include the literal heading with an initial objective; never splice it.
            if index == 0 and label_kind.startswith("objetivo"):
                start = 0
                while start < end and source[start].isspace():
                    start += 1
            if end - start > 1200:
                continue
            if comparison:
                # Contrast includes the documented criteria/tasks of both operations,
                # adding actual source information rather than repeating a definition.
                end = end_of_body
                while end > start and source[end - 1].isspace():
                    end -= 1
                if end - start > 1200:
                    continue
            span = QueryExcerpt(key, source[start:end], start, end, sha256(source.encode()).hexdigest())
            blocks.append((score, heading, span))
    blocks.sort(key=lambda row: -row[0])
    if not blocks:
        return []
    if not comparison:
        return [blocks[0][2]]
    selected, headings = [], set()
    for _, heading, span in blocks:
        identity = normalized(heading)
        if identity in headings:
            continue
        headings.add(identity)
        selected.append(span)
        if len(selected) == 2:
            return selected
    return []
