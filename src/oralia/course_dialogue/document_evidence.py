"""Lab-only whole-unit evidence over the already authorized academic catalog.

Retrieval proposes context. It neither verifies claims nor grants publication.
"""

import hashlib
import re
from dataclasses import dataclass

import pdfplumber

from oralia.course_dialogue.corpus import SOURCE_ROOT, load_catalog
from oralia.domain.materials.query_excerpt import terms


@dataclass(frozen=True)
class PagePosition:
    page_id: str
    page_number: int
    start: int | None
    end: int | None
    first_line: int | None
    last_line: int | None
    bbox: tuple[float, float, float, float] | None = None


@dataclass(frozen=True)
class EvidenceUnit:
    id: str
    kind: str
    text: str
    document_id: str
    original_sha256: str
    version: int
    positions: tuple[PagePosition, ...]
    heading: str
    text_sha256: str


@dataclass(frozen=True)
class RetrievalBudget:
    max_chars: int = 5000
    max_units: int = 8
    max_seed_units: int = 5
    max_neighbors: int = 2

    def validate(self):
        if not (100 <= self.max_chars <= 20000):
            raise ValueError("character budget outside lab bounds")
        if not (1 <= self.max_units <= 16):
            raise ValueError("unit budget outside lab bounds")
        if not (1 <= self.max_seed_units <= self.max_units):
            raise ValueError("seed budget outside unit budget")
        if not (0 <= self.max_neighbors <= self.max_units):
            raise ValueError("neighbor budget outside unit budget")


@dataclass(frozen=True)
class RetrievalResult:
    units: tuple[EvidenceUnit, ...]
    trace: tuple[dict, ...]
    chars_used: int
    catalog_page_ids: tuple[str, ...]
    catalog_documents: tuple[str, ...]
    scope: str = "authorized_ingested_catalog_only_not_complete_course"


def _line_records(text):
    records = []
    offset = 0
    for number, raw in enumerate(text.splitlines(keepends=True), start=1):
        end = offset + len(raw.rstrip("\r\n"))
        records.append((number, offset, end, raw.rstrip("\r\n")))
        offset += len(raw)
    return records


def _kind(line):
    value = line.lstrip()
    if not value:
        return "blank"
    if "|" in value or "\t" in value:
        return "table"
    if value.startswith(("•", "▪", "- ", "* ", "�")):
        return "list"
    return "paragraph"


def _make_unit(page, kind, records, heading):
    first, last = records[0], records[-1]
    start, end = first[1], last[2]
    text = page["text"][start:end]
    position = PagePosition(page["id"], page["page"], start, end, first[0], last[0])
    identity = f"{page['id']}:{start}:{end}:{kind}"
    return EvidenceUnit(
        id=identity,
        kind=kind,
        text=text,
        document_id=page["filename"],
        original_sha256=page["original_sha256"],
        version=page["version"],
        positions=(position,),
        heading=heading,
        text_sha256=hashlib.sha256(text.encode()).hexdigest(),
    )


def _page_units(page):
    text = page["text"]
    records = _line_records(text)
    if not records:
        raise ValueError("empty source page")
    heading = records[0][3].strip()
    body = records[1:]
    if body and re.match(r"\d{2}/\d{2}/\d{4}\s+Chapter\b", body[-1][3]):
        body = body[:-1]
    units = []
    group = []
    current_kind = None

    def flush():
        nonlocal group, current_kind
        if group:
            units.append(_make_unit(page, current_kind, group, heading))
        group, current_kind = [], None

    for record in body:
        kind = _kind(record[3])
        if kind == "blank":
            flush()
            continue
        # Wrapped lines remain with the current paragraph or list.
        if kind == "paragraph" and current_kind in {"paragraph", "list"}:
            group.append(record)
            continue
        if kind != current_kind:
            flush()
            current_kind = kind
        group.append(record)
    flush()
    for table in page.get("tables", ()):
        rows = table["rows"]
        if not rows or not all(isinstance(row, (list, tuple)) for row in rows):
            raise ValueError("invalid table rows")
        bbox = tuple(table["bbox"])
        if len(bbox) != 4:
            raise ValueError("invalid table box")
        table_text = "\n".join(" | ".join(str(cell or "") for cell in row) for row in rows)
        position = PagePosition(page["id"], page["page"], None, None, None, None, bbox)
        units.append(
            EvidenceUnit(
                id=f"{page['id']}:table:{len(units)}",
                kind="table",
                text=table_text,
                document_id=page["filename"],
                original_sha256=page["original_sha256"],
                version=page["version"],
                positions=(position,),
                heading=heading,
                text_sha256=hashlib.sha256(table_text.encode()).hexdigest(),
            )
        )
    return units


def build_units(catalog):
    """Build complete blocks; cross-page join requires explicit source metadata."""
    pages = list(catalog)
    if len({page["id"] for page in pages}) != len(pages):
        raise ValueError("duplicate source page")
    result = []
    previous_page = None
    for page in pages:
        current = _page_units(page)
        if page.get("continues_from_previous"):
            if (
                previous_page is None
                or previous_page["filename"] != page["filename"]
                or previous_page["page"] + 1 != page["page"]
                or not result
                or not current
                or result[-1].kind != current[0].kind
                or result[-1].kind not in {"paragraph", "list"}
            ):
                raise ValueError("unjustified page continuation")
            left, right = result.pop(), current.pop(0)
            joined = left.text + "\n" + right.text
            result.append(
                EvidenceUnit(
                    id=left.id + "+" + right.id,
                    kind=left.kind,
                    text=joined,
                    document_id=left.document_id,
                    original_sha256=left.original_sha256,
                    version=left.version,
                    positions=left.positions + right.positions,
                    heading=left.heading,
                    text_sha256=hashlib.sha256(joined.encode()).hexdigest(),
                )
            )
        result.extend(current)
        previous_page = page
    return result


def retrieve_units(
    units,
    catalog,
    question,
    *,
    displayed_history=(),
    focus_change=False,
    budget=None,
    lexical_profile="literal",
    broaden_candidates=False,
):
    """Whole-unit lexical retrieval across every supplied authorized page."""
    budget = budget or RetrievalBudget()
    budget.validate()
    if type(broaden_candidates) is not bool:
        raise ValueError("candidate broadening must be an explicit boolean")
    pages = {page["id"]: page for page in catalog}
    if len(pages) != len(catalog):
        raise ValueError("duplicate authorized page")
    page_ids = tuple(page["id"] for page in catalog)
    documents = tuple(dict.fromkeys(page["filename"] for page in catalog))
    if not question.strip():
        raise ValueError("current question required")
    if lexical_profile == "literal":
        tokenize = terms
    elif lexical_profile == "bilingual-v1":
        from oralia.course_dialogue.retrieval_terms import retrieval_terms

        tokenize = retrieval_terms
    else:
        raise ValueError("unknown retrieval lexical profile")
    query_terms = tokenize(question)
    # Original slides mix Spanish questions and English testing terminology.
    # This is a retrieval aid, never a semantic support judgment.
    if "prueb" in query_terms:
        query_terms.update({"test", "testi"})
    history_terms = set() if focus_change else tokenize(" ".join(displayed_history[-2:]))
    indexed = list(units)
    for unit in indexed:
        if hashlib.sha256(unit.text.encode()).hexdigest() != unit.text_sha256 or not unit.positions:
            raise ValueError("evidence unit text or positions changed")
        source_parts = []
        for span in unit.positions:
            page = pages.get(span.page_id)
            if (
                page is None
                or page["filename"] != unit.document_id
                or page["original_sha256"] != unit.original_sha256
                or page["version"] != unit.version
                or page["page"] != span.page_number
            ):
                raise ValueError("evidence unit outside authorized catalog")
            if span.bbox is None and (
                span.start is None or span.end is None or not 0 <= span.start < span.end <= len(page["text"])
            ):
                raise ValueError("evidence unit source span changed")
            if span.bbox is None:
                source_parts.append(page["text"][span.start : span.end])
            if span.bbox is not None and len(span.bbox) != 4:
                raise ValueError("invalid evidence table box")
            if span.bbox is not None:
                matches = [
                    "\n".join(" | ".join(str(cell or "") for cell in row) for row in table["rows"])
                    for table in page.get("tables", ())
                    if tuple(table["bbox"]) == span.bbox
                ]
                if unit.text not in matches:
                    raise ValueError("evidence table outside authorized page")
        if source_parts and "\n".join(source_parts) != unit.text:
            raise ValueError("evidence unit source text changed")
    ranked = []
    for index, unit in enumerate(indexed):
        words = tokenize(unit.text + " " + unit.heading)
        query_hits = query_terms & words
        history_hits = history_terms & words
        score = 4 * len(query_hits) + len(history_hits)
        if query_hits or (history_hits and not focus_change):
            ranked.append((score, len(query_hits), index, unit, query_hits, history_hits))
    strongest_query_hits = max((row[1] for row in ranked), default=0)
    if strongest_query_hits >= 2:
        ranked = [row for row in ranked if row[1] >= 2]
    ranked.sort(key=lambda row: (-row[0], -row[1], row[2]))
    # Preserve nearby complementary perspectives, but do not force a weak
    # document into the request merely to increase document count.
    strongest_count = sum(row[0] == ranked[0][0] for row in ranked) if ranked else 0
    cutoff = (ranked[0][0] - (0 if strongest_count >= 2 else 4)) if ranked else 0
    if broaden_candidates and ranked:
        # One externally requested expansion admits a wider lexical band;
        # the earlier two-query-concept filter and all budgets still apply.
        cutoff = min(cutoff, ranked[0][0] / 2)
    low_relevance = [row for row in ranked if row[0] < cutoff]
    ranked = [row for row in ranked if row[0] >= cutoff]
    selected = []
    trace = []
    chars_used = 0
    selected_indices = set()
    selected_docs = set()
    neighbors_used = 0

    def add(row, reason):
        nonlocal chars_used
        score, _, index, unit, query_hits, history_hits = row
        if index in selected_indices:
            return False
        if len(selected) >= budget.max_units or chars_used + len(unit.text) > budget.max_chars:
            trace.append({"unit_id": unit.id, "score": score, "decision": "omitted_budget", "reason": reason})
            return False
        selected.append(unit)
        selected_indices.add(index)
        selected_docs.add(unit.document_id)
        chars_used += len(unit.text)
        trace.append(
            {
                "unit_id": unit.id,
                "score": score,
                "decision": "selected",
                "reason": reason,
                "query_hits": sorted(query_hits),
                "history_hits": sorted(history_hits),
                "page_ids": [span.page_id for span in unit.positions],
            }
        )
        return True

    # First preserve a relevant perspective from each available document.
    for row in ranked:
        if len(selected) >= budget.max_seed_units:
            break
        if row[3].document_id not in selected_docs:
            add(row, "document_perspective")
    for row in ranked:
        if len(selected) >= budget.max_seed_units:
            break
        add(row, "relevance")
    for seed_index in sorted(selected_indices):
        if neighbors_used >= budget.max_neighbors:
            break
        for index in (seed_index - 1, seed_index + 1):
            if not 0 <= index < len(indexed) or index in selected_indices:
                continue
            unit, seed = indexed[index], indexed[seed_index]
            if unit.document_id != seed.document_id:
                continue
            if abs(unit.positions[0].page_number - seed.positions[-1].page_number) > 1:
                continue
            if add((0, 0, index, unit, set(), set()), "adjacent_context"):
                neighbors_used += 1
            if neighbors_used >= budget.max_neighbors:
                break
    for row in ranked:
        if row[2] not in selected_indices and not any(entry["unit_id"] == row[3].id for entry in trace):
            trace.append({"unit_id": row[3].id, "score": row[0], "decision": "not_selected"})
    for row in low_relevance:
        trace.append({"unit_id": row[3].id, "score": row[0], "decision": "not_selected_low_relevance"})
    scope = (
        "three_authorized_teacher_pdfs_lab_reviewed_text"
        if catalog
        and all(
            page.get("corpus_scope") == "three_authorized_teacher_pdfs_lab_reviewed_text" for page in catalog
        )
        else "authorized_ingested_catalog_only_not_complete_course"
    )
    return RetrievalResult(tuple(selected), tuple(trace), chars_used, page_ids, documents, scope)


def load_authorized_units(source_root=SOURCE_ROOT, catalog_loader=load_catalog):
    """Read the existing selected pages and optional original table boxes; no new sources."""
    catalog = [dict(page) for page in catalog_loader(source_root)]
    by_document = {}
    for page in catalog:
        by_document.setdefault(page["filename"], []).append(page)
    for filename, pages in by_document.items():
        path = source_root / filename
        if hashlib.sha256(path.read_bytes()).hexdigest() != pages[0]["original_sha256"]:
            raise ValueError("original document changed during extraction")
        with pdfplumber.open(path) as pdf:
            for page in pages:
                found = pdf.pages[page["page"] - 1].find_tables()
                page["tables"] = [{"bbox": tuple(table.bbox), "rows": table.extract()} for table in found]
    return catalog, build_units(catalog)
