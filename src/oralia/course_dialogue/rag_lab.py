"""Diagnostic RAG turn over authorized local evidence; never publishes."""

import hashlib
import inspect
import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Literal

from oralia.course_dialogue.context import current_request, plan_context
from oralia.course_dialogue.local_expansion import retrieve_with_local_expansion
from oralia.course_dialogue.pedagogical_profile import instruction_for_profile
from oralia.course_dialogue.reference_presentation import consulted_sources
from oralia.infrastructure.generation.generation_port import (
    EvidenceItem,
    GenerationConstraints,
    GenerationRequest,
)

Status = Literal["sufficient", "insufficient", "conflict", "unknown"]
ScopeStatus = Literal["in_scope", "out_of_scope", "uncertain_scope", "mixed", "operational"]

RAG_INSTRUCTION = (
    "Diagnóstico local. Responde en español a la pregunta actual usando solo los pasajes "
    "recuperados. El historial resuelve referentes, no es fuente académica. "
    "No añadas hechos de memoria. Distingue inferencias con premisas y ejemplos hipotéticos. "
    "Si falta apoyo para alguna parte, expresa el límite. Responde de forma conversacional. "
    "El sistema añadirá referencias legibles a las fuentes consultadas."
)


@lru_cache(maxsize=4)
def _trusted_catalog(source_root, profile, source_hashes, decisions_sha256):
    from oralia.course_dialogue.document_evidence import load_authorized_units

    if profile == "selected":
        return load_authorized_units(source_root)
    if profile == "full":
        from oralia.course_dialogue.full_corpus import load_full_teacher_catalog

        return load_authorized_units(source_root, catalog_loader=load_full_teacher_catalog)
    raise ValueError("unknown laboratory catalog profile")


@dataclass(frozen=True)
class ActivityScopeBinding:
    """Lab binding to an approved scope file and one current SQL activity version."""

    engine: object
    activity_id: str
    activity_version: int
    course_id: str
    policy_path: Path
    policy_sha256: str
    source_root: Path | None = None
    catalog_profile: Literal["selected", "full"] = "selected"
    decisions_sha256: str | None = None

    def revalidate(self, db):
        from oralia.infrastructure.db import models

        if db is None or db.get_bind().engine is not self.engine:
            raise ValueError("scope policy bound to another database engine")
        db.expire_all()
        activity = db.get(models.ActivityConfiguration, self.activity_id, populate_existing=True)
        if (
            activity is None
            or activity.version != self.activity_version
            or activity.course_id != self.course_id
        ):
            raise ValueError("scope policy bound to stale or foreign activity")
        governance = db.get(models.ActivityGovernance, self.activity_id, populate_existing=True)
        if governance is None or governance.version != self.activity_version or governance.status != "active":
            raise ValueError("scope policy activity is not active")
        contents = self.policy_path.read_bytes()
        if hashlib.sha256(contents).hexdigest() != self.policy_sha256:
            raise ValueError("scope policy changed since binding")
        policy = json.loads(contents)
        if (
            policy.get("approval_status") != "approved"
            or policy.get("approval_kind") != "scope_only"
            or policy.get("participant_publication_allowed") is not False
            or policy.get("activity_id") != self.activity_id
            or policy.get("activity_version") != self.activity_version
            or policy.get("course_id") != self.course_id
        ):
            raise ValueError("scope policy is unapproved or not bound to activity")
        source_scope = policy.get("source_scope")
        if source_scope:
            if self.source_root is None:
                raise ValueError("scope source root is required")
            sources = [source_scope["presentation"], *source_scope["authorized_lab_documents"]]
            for source in sources:
                path = self.source_root / source["file"]
                if hashlib.sha256(path.read_bytes()).hexdigest() != source["sha256"]:
                    raise ValueError("scope source changed since binding")
        if self.catalog_profile == "full":
            from oralia.course_dialogue.full_corpus import DECISIONS

            if (
                not self.decisions_sha256
                or hashlib.sha256(DECISIONS.read_bytes()).hexdigest() != self.decisions_sha256
            ):
                raise ValueError("teacher page decisions changed since binding")
        return policy

    def assert_decision(self, scope, policy):
        if scope.status not in {"in_scope", "out_of_scope", "mixed"}:
            return
        if scope.authority_ref != self.policy_sha256:
            raise ValueError("scope decision does not reference bound policy")
        if scope.status in {"in_scope", "mixed"} and scope.block_id not in policy["included_blocks"]:
            raise ValueError("scope decision has no included block in bound policy")
        if (
            scope.status in {"out_of_scope", "mixed"}
            and scope.excluded_block_id not in policy["excluded_as_standalone_blocks_for_this_activity"]
        ):
            raise ValueError("scope decision has no excluded block in bound policy")
        if (
            scope.status in {"out_of_scope", "mixed"}
            and policy.get("boundary_rules", {}).get("exclusion_is_standalone_only")
            and not scope.standalone_excluded_block
        ):
            raise ValueError("scope exclusion is not a standalone block")

    def assert_catalog(self, catalog, units, policy):
        """Reject evidence outside the policy's pinned laboratory documents."""
        source_scope = policy.get("source_scope")
        if not source_scope:
            raise ValueError("scope policy has no source inventory")
        if self.source_root is None:
            raise ValueError("scope source root is required")
        source_hashes = tuple(
            (item["file"], item["sha256"]) for item in source_scope["authorized_lab_documents"]
        )
        trusted_pages, trusted_units = _trusted_catalog(
            self.source_root, self.catalog_profile, source_hashes, self.decisions_sha256
        )
        if catalog != trusted_pages or units != trusted_units:
            raise ValueError("catalog differs from verified source extraction")
        allowed = {item["file"]: item["sha256"] for item in source_scope["authorized_lab_documents"]}
        pages = {}
        for page in catalog:
            if (
                page["filename"] not in allowed
                or page["original_sha256"] != allowed[page["filename"]]
                or page["id"] in pages
            ):
                raise ValueError("catalog contains foreign or changed source")
            pages[page["id"]] = page
        for unit in units:
            if (
                unit.document_id not in allowed
                or unit.original_sha256 != allowed[unit.document_id]
                or not unit.positions
                or any(
                    position.page_id not in pages
                    or pages[position.page_id]["filename"] != unit.document_id
                    or pages[position.page_id]["version"] != unit.version
                    for position in unit.positions
                )
                or hashlib.sha256(unit.text.encode()).hexdigest() != unit.text_sha256
            ):
                raise ValueError("evidence unit is foreign or changed")


@dataclass(frozen=True)
class ScopeAssessment:
    status: ScopeStatus
    authority_ref: str | None = None
    reason: str = ""
    in_scope_question: str | None = None
    excluded_part: str | None = None
    block_id: str | None = None
    excluded_block_id: str | None = None
    standalone_excluded_block: bool = False

    def validate(self):
        if self.status not in {"in_scope", "out_of_scope", "uncertain_scope", "mixed", "operational"}:
            raise ValueError("invalid scope status")
        if not self.reason.strip():
            raise ValueError("scope reason required")
        if self.status in {"out_of_scope", "mixed"} and (
            not self.authority_ref or not self.authority_ref.strip()
        ):
            raise ValueError("confirmed exclusion requires teacher scope authority")
        if self.status == "mixed" and (
            not self.in_scope_question
            or not self.in_scope_question.strip()
            or not self.excluded_part
            or not self.excluded_part.strip()
        ):
            raise ValueError("mixed scope requires both question parts")


@dataclass(frozen=True)
class SufficiencyAssessment:
    status: Status
    reviewer_id: str
    reason: str

    def validate(self):
        if self.status not in {"sufficient", "insufficient", "conflict", "unknown"}:
            raise ValueError("invalid sufficiency status")
        if not self.reviewer_id.strip() or not self.reason.strip():
            raise ValueError("assessment identity and reason required")


async def diagnostic_rag_turn(
    catalog,
    units,
    text,
    history,
    *,
    scope_assessor,
    assessor,
    provider,
    binding=None,
    db=None,
    lexical_profile="literal",
    pedagogical_profile="baseline",
):
    """Use an injected assessor; fixture verdicts are not real semantic evidence."""
    policy = binding.revalidate(db) if binding is not None else None
    plan = plan_context(text, history)
    scope = scope_assessor(plan.current_request, plan.academic_query, history)
    if inspect.isawaitable(scope):
        scope = await scope
    # A scope assessor can wait; do not retrieve under a stale activity/policy.
    if binding is not None:
        policy = binding.revalidate(db)
    if not isinstance(scope, ScopeAssessment):
        raise ValueError("trusted scope assessment required")
    scope.validate()
    if binding is not None:
        binding.assert_decision(scope, policy)
        binding.assert_catalog(catalog, units, policy)
    scope_notice = None
    if scope.status == "out_of_scope":
        scope_notice = (
            "Ese tema no forma parte del contenido de esta asignatura " "y no necesitas estudiarlo para ella."
        )
    elif scope.status == "uncertain_scope":
        scope_notice = "No puedo confirmar si ese tema entra en la asignatura. ¿Puedes precisar la duda?"
    elif scope.status == "operational":
        scope_notice = "Esta solicitud corresponde a los controles de la sesión."
    elif scope.status == "mixed":
        scope_notice = (
            "La otra parte no forma parte del contenido de esta asignatura "
            "y no necesitas estudiarla para ella."
        )
        plan = plan_context(scope.in_scope_question, history)
    if scope.status in {"out_of_scope", "uncertain_scope", "operational"}:
        return {
            "input": text,
            "academic_query": plan.academic_query,
            "scope_assessment": scope,
            "scope_result": scope.status,
            "scope_notice": scope_notice,
            "evidence_attempts": None,
            "assessments": (),
            "displayed_kind": "operational",
            "displayed_text": scope_notice,
            "publication_allowed": False,
            "participant_display": None,
            "semantic_support": "unverified",
            "generation_request": None,
            "outcome": None,
            "raw_candidate": None,
            "laboratory_preview": None,
            "citation_check": None,
            "history_omissions": None,
        }
    displayed = tuple(
        row["displayed_text"]
        for row in history
        if row.get("displayed_text") and row.get("displayed_kind") in {"laboratory_preview", "candidate"}
    )
    explicit_switch = bool(
        re.search(r"\b(?:cambi(?:o|a|emos)\s+de\s+tema|hablemos\s+de\s+otra\s+cosa)\b", text, re.I)
        or re.match(r"^\s*(?:ahora\b|sobre\b|en\s+cuanto\s+a\b)", current_request(text), re.I)
    )
    focus_change = explicit_switch and bool(history)
    first = retrieve_with_local_expansion(
        units,
        catalog,
        plan.academic_query,
        displayed_history=displayed,
        focus_change=focus_change,
        lexical_profile=lexical_profile,
    )
    before = assessor(plan.current_request, first.delivered)
    if inspect.isawaitable(before):
        before = await before
    before.validate()
    if binding is not None:
        policy = binding.revalidate(db)
        binding.assert_decision(scope, policy)
        binding.assert_catalog(catalog, units, policy)
    attempts = first
    after = before
    if before.status == "insufficient":
        attempts = retrieve_with_local_expansion(
            units,
            catalog,
            plan.academic_query,
            displayed_history=displayed,
            focus_change=focus_change,
            insufficient=True,
            lexical_profile=lexical_profile,
        )
        after = assessor(plan.current_request, attempts.delivered)
        if inspect.isawaitable(after):
            after = await after
        after.validate()
        if binding is not None:
            policy = binding.revalidate(db)
            binding.assert_decision(scope, policy)
            binding.assert_catalog(catalog, units, policy)
    receipt = {
        "input": text,
        "academic_query": plan.academic_query,
        "focus_change": focus_change,
        "assessments": (before, after) if after is not before else (before,),
        "evidence_attempts": attempts,
        "publication_allowed": False,
        "semantic_support": "unverified",
        "participant_display": None,
        "scope_assessment": scope,
        "scope_notice": scope_notice,
        "scope_result": "mixed_pending_evidence" if scope.status == "mixed" else "in_scope_pending_evidence",
    }
    history_window = history[-4:]
    history_omissions = {
        "older_turns": max(0, len(history) - len(history_window)),
        "oversized_fields": [
            {"turn": len(history) - len(history_window) + index, "field": field, "chars": len(row[field])}
            for index, row in enumerate(history_window)
            for field in ("input", "displayed_text")
            if isinstance(row.get(field), str) and len(row[field]) > 4000
        ],
    }
    receipt["history_omissions"] = history_omissions
    if history_omissions["oversized_fields"] or (
        history_omissions["older_turns"] and not focus_change and plan.academic_query != plan.current_request
    ):
        return {
            **receipt,
            "displayed_kind": "operational",
            "displayed_text": (
                "El contexto anterior es demasiado extenso. " "¿Puedes precisar el referente de tu duda?"
            ),
            "reason": "history_context_limit",
            "generation_request": None,
            "outcome": None,
            "raw_candidate": None,
            "laboratory_preview": None,
            "citation_check": None,
        }
    if after.status != "sufficient" or not attempts.delivered.units:
        reason = "conflict" if after.status == "conflict" else "insufficient_or_unknown"
        return {
            **receipt,
            "scope_result": (
                "mixed_in_scope_insufficient_evidence"
                if scope.status == "mixed"
                else "in_scope_insufficient_evidence"
            ),
            "displayed_kind": "operational",
            "displayed_text": (
                "Las fuentes consultadas contienen información que requiere aclaración."
                if reason == "conflict"
                else "No encuentro respaldo suficiente en las fuentes consultadas. ¿Puedes concretar la duda?"
            ),
            "reason": reason,
            "generation_request": None,
            "outcome": None,
            "raw_candidate": None,
            "laboratory_preview": None,
            "citation_check": None,
        }
    context = []
    for row in history_window:
        permitted_input = row.get("permitted_input", row.get("input"))
        if permitted_input:
            context.append({"role": "user", "content": permitted_input})
        if row.get("displayed_text"):
            context.append({"role": "assistant", "content": row["displayed_text"]})
    request = GenerationRequest(
        purpose="explicacion",
        instruction=instruction_for_profile(RAG_INSTRUCTION, pedagogical_profile),
        student_input=(
            plan.current_request
            if plan.academic_query == plan.current_request
            else f"Referente mostrado: {plan.academic_query}\nPregunta: {plan.current_request}"
        ),
        conversation_history=context,
        evidence=[
            EvidenceItem(
                fragment_id=unit.id,
                document_id=(
                    f"{unit.document_id} | páginas " + ",".join(str(p.page_number) for p in unit.positions)
                ),
                document_version=unit.version,
                text=f'<pasaje id="{unit.id}">\n{unit.text}\n</pasaje>',
            )
            for unit in attempts.delivered.units
        ],
        general_knowledge_allowed=False,
        constraints=GenerationConstraints(max_tokens=512, deadline_ms=30000),
    )
    # Assessment may wait on external review or mutate the backing inventory.
    # Recheck at dispatch, rather than letting the post-generation check detect
    # that withdrawn evidence has already reached the provider.
    if binding is not None:
        policy = binding.revalidate(db)
        binding.assert_decision(scope, policy)
        binding.assert_catalog(catalog, units, policy)
    outcome = await provider.generate(request)
    if binding is not None:
        policy = binding.revalidate(db)
        binding.assert_decision(scope, policy)
        binding.assert_catalog(catalog, units, policy)
    preview = outcome.text if outcome.ok and outcome.finish_reason == "stop" else None
    expected = {unit.id for unit in attempts.delivered.units}
    cited = set(re.findall(r"\[([^\[\]]+)\]", preview or ""))
    citation_check = {
        "known": tuple(sorted(cited & expected)),
        "foreign": tuple(sorted(cited - expected)),
        "missing": not cited,
        "semantic_support": "unverified",
    }
    sources = consulted_sources(attempts.delivered.units)
    return {
        **receipt,
        "scope_result": (
            "mixed_in_scope_with_evidence" if scope.status == "mixed" else "in_scope_with_evidence"
        ),
        "displayed_kind": "laboratory_preview" if preview else "operational",
        "displayed_text": (
            preview + "\n\n" + sources["display_text"]
            if preview
            else "La respuesta no se completó; puedes intentarlo de nuevo."
        ),
        "source_presentation": sources,
        "generation_request": request,
        "outcome": outcome,
        "raw_candidate": outcome.text,
        "laboratory_preview": preview,
        "citation_check": citation_check,
    }
