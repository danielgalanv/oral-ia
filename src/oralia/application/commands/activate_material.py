"""activate_material / deactivate_material commands.

FR-011: activation is rejected unless the document has finished processing.
FR-013: deactivation is reversible — it only flips ``status`` and never touches
``retired_at``.
FR-013a: a retired (or not-yet-active) version can never be assigned to a *new*
activity — ``assign_to_activity`` requires the document to already be active.
"""

from __future__ import annotations

from sqlalchemy.orm import Session as SASession

from oralia.infrastructure.db import models


class MaterialDocumentNotFoundError(LookupError):
    pass


class DocumentNotProcessedError(ValueError):
    """FR-011."""


class DocumentRetiredError(ValueError):
    """FR-015: a retired version is irreversibly excluded from ever becoming active again."""


class DocumentNotActiveError(ValueError):
    """FR-013a."""


def _get_document(db: SASession, document_id: str) -> models.MaterialDocument:
    document = db.get(models.MaterialDocument, document_id)
    if document is None:
        raise MaterialDocumentNotFoundError(document_id)
    return document


def activate_material(db: SASession, document_id: str) -> models.MaterialDocument:
    document = _get_document(db, document_id)
    if document.retired_at is not None:
        raise DocumentRetiredError(f"document {document_id} is retired and cannot be (re)activated")
    if document.status not in ("processed", "inactive"):
        raise DocumentNotProcessedError(f"document {document_id} is not processed (status={document.status})")
    document.status = "active"
    db.add(document)
    db.flush()
    return document


def deactivate_material(db: SASession, document_id: str) -> models.MaterialDocument:
    document = _get_document(db, document_id)
    document.status = "inactive"
    db.add(document)
    db.flush()
    return document


def assign_to_activity(
    db: SASession, document_id: str, activity_configuration_id: str
) -> models.MaterialDocument:
    document = _get_document(db, document_id)
    if document.retired_at is not None or document.status != "active":
        raise DocumentNotActiveError(
            f"document {document_id} must be active (and not retired) to be assigned to a new activity"
        )
    if activity_configuration_id not in document.activity_configuration_ids:
        document.activity_configuration_ids = [
            *document.activity_configuration_ids,
            activity_configuration_id,
        ]
        db.add(document)
        db.flush()
    return document
