"""Presence/shape only: explicit keywords never establish semantic correctness."""

import re


def keyword_terms(text):
    match = re.search(r"(?im)^\s*(?:\*\*)?Palabras clave(?:\*\*)?\s*:\s*(?:\*\*)?([^\r\n]+)\s*$", text)
    if match is None:
        return []
    terms = [term.strip().strip("* .") for term in re.split(r"[;,]", match[1])]
    # This is a presence check, not a new semantic or editorial gate. Repetition,
    # separators and the suggested list length must not suppress a useful answer.
    return [term for term in terms if any(char.isalnum() for char in term)]
