"""Source-location review contract. References establish identity, never entailment."""

import json
from typing import Literal
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, StrictInt, model_validator


class SourceLocation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    document_id: str = Field(min_length=1, max_length=500)
    document_version: StrictInt = Field(ge=1)
    document_title: str = Field(min_length=1, max_length=300)
    page: StrictInt | None = Field(default=None, ge=1)
    url: str | None = Field(default=None, max_length=2000)

    @model_validator(mode="after")
    def valid_location(self):
        if not self.document_title.strip():
            raise ValueError("empty document title")
        if self.url is not None:
            value = urlsplit(self.url)
            if (
                value.scheme != "https"
                or not value.hostname
                or value.username
                or value.password
                or any(char.isspace() for char in self.url)
            ):
                raise ValueError("source URL must be HTTPS without credentials")
        elif self.page is None:
            raise ValueError("document reference needs a page, web reference needs its URL")
        return self


class SourceReference(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source_id: str = Field(min_length=1, max_length=160)


class ReferenceIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["contradiction", "unsupported", "coverage", "ambiguity", "overclaim"]
    claim: str = Field(max_length=1000)
    explanation: str = Field(min_length=1, max_length=1200)
    evidence: list[SourceReference] = Field(max_length=3)


class ReferenceReview(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["issues_found", "no_issues_found", "insufficient_evidence"]
    external_support: Literal["supported", "rejected", "unknown", "not_used"]
    teacher_compatibility: Literal["compatible", "conflict", "unknown"]
    response_action: Literal["explanation", "limit", "repair"]
    issues: list[ReferenceIssue] = Field(max_length=3)

    @model_validator(mode="after")
    def consistent(self):
        if (self.status == "issues_found") != bool(self.issues):
            raise ValueError("issues must agree with review status")
        if (self.response_action == "repair") != (self.status == "issues_found"):
            raise ValueError("repair action and issues must agree")
        return self


def validate_locations(evidence, locations):
    ids = {item.fragment_id for item in evidence}
    if len(ids) != len(evidence) or set(locations) != ids:
        raise ValueError("source locations must match unique evidence IDs")
    for item in evidence:
        location = locations[item.fragment_id]
        if (location.document_id, location.document_version) != (item.document_id, item.document_version):
            raise ValueError("source location document/version mismatch")


def parse_reference_review(text, request, *, teacher_only_contradiction=True, idle_action_alias=False):
    validate_locations(request.evidence, request.source_locations)
    if idle_action_alias:
        payload = json.loads(text)
        if isinstance(payload, dict) and payload.get("response_action") == "none":
            action = {"no_issues_found": "explanation", "insufficient_evidence": "limit"}.get(
                payload.get("status")
            )
            if action is not None:
                # Canonicalise only a nonrepair presentation alias. Status, issues,
                # academic claims and source references remain exactly as emitted.
                payload = {**payload, "response_action": action}
        review = ReferenceReview.model_validate(payload)
    else:
        review = ReferenceReview.model_validate_json(text)
    sources = {item.fragment_id: item for item in request.evidence}
    for issue in review.issues:
        if not issue.explanation.strip() or (issue.kind != "coverage" and not issue.claim.strip()):
            raise ValueError("a concrete objection is required, not an exact quotation")
        ids = [reference.source_id for reference in issue.evidence]
        if len(ids) != len(set(ids)) or any(source_id not in sources for source_id in ids):
            raise ValueError("foreign or repeated source reference")
        if issue.kind != "unsupported" and not ids:
            raise ValueError("source reference required")
        if (
            teacher_only_contradiction
            and issue.kind == "contradiction"
            and not any(sources[source_id].document_id.startswith("teacher/") for source_id in ids)
        ):
            raise ValueError("teacher contradiction needs a teacher source reference")
    if review.teacher_compatibility == "conflict" and not any(
        sources[reference.source_id].document_id.startswith("teacher/")
        for issue in review.issues
        for reference in issue.evidence
    ):
        raise ValueError("teacher conflict needs a teacher source reference")
    return review


def readable_references(request, review=None):
    """Only trusted host metadata; never titles/pages/URLs invented by the critic."""
    validate_locations(request.evidence, request.source_locations)
    ids = (
        [item.fragment_id for item in request.evidence]
        if review is None
        else [ref.source_id for issue in review.issues for ref in issue.evidence]
    )
    rows = []
    seen = set()
    for source_id in ids:
        location = request.source_locations[source_id]
        key = (location.document_id, location.document_version, location.page, location.url)
        if key in seen:
            continue
        seen.add(key)
        row = dict(document=location.document_title, page=location.page, url=location.url)
        row["label"] = location.url if location.url else f"{location.document_title}, página {location.page}"
        rows.append(row)
    return rows


class MinimalReferenceReview(BaseModel):
    """One advisory decision; it does not assert source support or compatibility."""

    model_config = ConfigDict(extra="forbid")
    status: Literal["issues_found", "no_issues_found", "insufficient_evidence"]
    issues: list[ReferenceIssue] = Field(max_length=1)

    @model_validator(mode="after")
    def consistent(self):
        if (self.status == "issues_found") != bool(self.issues):
            raise ValueError("issues must agree with primary review status")
        return self


def parse_minimal_reference_review(text, request):
    minimal = MinimalReferenceReview.model_validate_json(text)
    # Versioned host derivation, not a repair of the model's semantic decision.
    # Unknown labels explicitly decline to infer support or teacher agreement.
    action = {"issues_found": "repair", "no_issues_found": "explanation", "insufficient_evidence": "limit"}
    derived = dict(
        **minimal.model_dump(),
        external_support="unknown",
        teacher_compatibility="unknown",
        response_action=action[minimal.status],
    )
    return parse_reference_review(json.dumps(derived), request, teacher_only_contradiction=False)
