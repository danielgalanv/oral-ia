"""Human-readable attribution of consulted documents, not claim verification."""


def consulted_sources(units):
    documents = {}
    for unit in units:
        key = (unit.document_id, unit.version, unit.original_sha256)
        row = documents.setdefault(
            key,
            {
                "document": unit.document_id,
                "version": unit.version,
                "original_sha256": unit.original_sha256,
                "pages": [],
                "unit_ids": [],
            },
        )
        row["unit_ids"].append(unit.id)
        row["pages"] = sorted(set(row["pages"]) | {span.page_number for span in unit.positions})
    readable = []
    for row in documents.values():
        pages = row["pages"]
        label = "pág. " + str(pages[0]) if len(pages) == 1 else "págs. " + ", ".join(map(str, pages))
        readable.append(row["document"] + (f" ({label})" if pages and len(pages) <= 3 else ""))
    return {
        "display_text": "Fuentes consultadas: " + "; ".join(readable) if readable else "",
        "documents": list(documents.values()),
        "selection": "documents_of_evidence_delivered_to_generator",
        "claim_support_verified": False,
    }
