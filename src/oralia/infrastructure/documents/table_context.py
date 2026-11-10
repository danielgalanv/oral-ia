"""Bounded structural context, never inferred header semantics or numeric conversion."""

CONTEXT_LIMIT = 160


def _reference(text: str) -> str:
    compact = " ".join(text.split())
    return compact if len(compact) <= CONTEXT_LIMIT else compact[: CONTEXT_LIMIT - 1] + "…"


def contextual_cell(text: str, *, row: int, column: int, first_row: dict[int, str], row_start: str) -> str:
    """Keep main cell text intact; label bounded neighboring references as references.

    A first row can be data, so it must not be silently declared a header. The
    complete first-row/row-start text is also emitted at its own cell coordinate.
    """
    parts = [text]
    if row > 1:
        reference = _reference(first_row.get(column, ""))
        if reference:
            parts.append(f"Referencia de columna (fila 1): {reference}")
        if column > 1:
            reference = _reference(row_start)
            if reference:
                parts.append(f"Referencia inicial de fila: {reference}")
    return "\n".join(parts)
