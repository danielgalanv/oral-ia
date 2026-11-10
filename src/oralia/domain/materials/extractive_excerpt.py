"""Closed material-excerpt/v1 projection, shared by generator and trusted binder.

Offsets address Python string characters in the unmodified source. A future change
to trimming, limit, word boundary or ellipsis must use a new profile version.
"""

from dataclasses import dataclass
from hashlib import sha256


@dataclass(frozen=True)
class ExcerptV1:
    text: str
    start: int
    end: int
    source_sha256: str


def extractive_excerpt(source: str) -> ExcerptV1:
    stripped = source.strip()
    start = len(source) - len(source.lstrip())
    truncated = len(stripped) > 400
    body = stripped[:400].rsplit(" ", 1)[0] if truncated else stripped
    return ExcerptV1(
        text=body + ("…" if truncated else ""),
        start=start,
        end=start + len(body),
        source_sha256=sha256(source.encode("utf-8")).hexdigest(),
    )
