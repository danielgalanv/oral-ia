"""Current-row authorization of v2 quotations; fixtures do not claim real teaching evidence."""

import asyncio
import uuid
from datetime import timedelta

import pytest

from oralia.application.orchestration.self_study_agency_composer import _decide_study_output
from oralia.domain.materials.query_excerpt import select_query_excerpts
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from tests.integration.test_t090_self_study_fallback_red import _local_context


@pytest.mark.parametrize(
    "mutation",
    [
        "none",
        "altered",
        "full_fragment",
        "query",
        "retired",
        "version",
        "deindexed",
        "expired",
        "foreign_course",
        "permission",
    ],
)
def test_query_projection_reconstructed_from_current_source(tmp_path, mutation):
    overrides = {"policy_id": "material-self-study/v2"}
    if mutation == "permission":
        overrides["allowed_disclosures"] = []
    with _local_context(
        tmp_path,
        mode="doubt_resolution",
        allowed_templates=[["material-fragment-response", 1], ["material-fragment-response-2", 1]],
        policy_overrides=overrides,
    ) as (db, session, _, _):
        activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
        activity.objective = "Consultar requisitos desde su fuente"
        row = db.get(models.MaterialFragment, "fragment-t096")
        row.text = (
            "Validar requisitos\n• Objetivo: contrastar necesidades de clientes.\n"
            "• Riesgos: producto inadecuado."
        )
        db.flush()
        fragment = {
            "fragment_id": row.id,
            "document_id": row.document_id,
            "document_version": row.document_version,
            "location_ref": row.location_ref,
            "text": row.text,
        }
        query = "Qué significa validar requisitos"
        candidate = select_query_excerpts([fragment], query)[0].text
        if mutation == "altered":
            candidate += " La calificación es nueve."
        elif mutation == "full_fragment":
            candidate = row.text
        elif mutation == "query":
            query = "Qué riesgos hay al validar requisitos"
        elif mutation == "retired":
            db.get(models.MaterialDocument, row.document_id).status = "retired"
        elif mutation == "version":
            fragment["document_version"] = 2
        elif mutation == "deindexed":
            row.indexing_status = "pending"
        elif mutation == "expired":
            row.valid_until = utcnow() - timedelta(seconds=1)
        elif mutation == "foreign_course":
            other = models.Course(name="Curso ajeno", subject_code="OTHER")
            db.add(other)
            db.flush()
            db.get(models.MaterialDocument, row.document_id).course_id = other.id
        db.flush()
        turn = models.Turn(
            id=str(uuid.uuid4()), session_id=session.id, index=1, input_text=query, status="in_progress"
        )
        db.add(turn)
        db.flush()
        result = asyncio.run(
            _decide_study_output(
                db,
                session=session,
                turn_id=turn.id,
                text=candidate,
                fragments_used=[fragment],
                general_knowledge_used=False,
                material_query=query,
            )
        )
        if mutation == "none":
            assert not result.blocked and result.output_text == candidate
        else:
            assert result.blocked and result.output_text is None
