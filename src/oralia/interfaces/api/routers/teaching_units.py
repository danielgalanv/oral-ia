"""Teacher-only unit authoring under the existing local governance access guard."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, StrictBool
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from oralia.application.services import teaching_unit_service as units
from oralia.infrastructure.db import models
from oralia.interfaces.api.deps.db import get_db

router = APIRouter(prefix="/api/v1/governance/teaching-units", tags=["governance"])


def view(unit):
    return {
        "id": unit.id,
        "family_id": unit.family_id,
        "version": unit.version,
        "status": unit.status,
        **units.unit_input(unit).model_dump(mode="json"),
    }


@router.get("")
def list_units(course_id: str, db: Session = Depends(get_db, scope="function")):
    return [
        view(unit)
        for unit in db.query(models.TeachingUnit)
        .filter_by(course_id=course_id)
        .order_by(models.TeachingUnit.family_id, models.TeachingUnit.version)
    ]


@router.post("", status_code=201)
def create_unit(data: units.TeachingUnitInput, db: Session = Depends(get_db, scope="function")):
    try:
        return view(units.create(db, data))
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from None


@router.post("/{unit_id}/versions", status_code=201)
def successor(unit_id: str, data: units.TeachingUnitInput, db: Session = Depends(get_db, scope="function")):
    try:
        return view(units.successor(db, unit_id, data))
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from None
    except IntegrityError:
        raise HTTPException(409, "Versión concurrente: consulta las unidades antes de reintentar.") from None


class ReviewInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reviewed: StrictBool


@router.post("/{unit_id}/publish")
def publish(unit_id: str, data: ReviewInput, db: Session = Depends(get_db, scope="function")):
    try:
        return view(units.publish(db, unit_id, reviewed=data.reviewed))
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from None


@router.post("/{unit_id}/retire")
def retire(unit_id: str, db: Session = Depends(get_db, scope="function")):
    try:
        return view(units.retire(db, unit_id))
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from None
