"""Connected web fallback. Structural checks do not calibrate semantic judgements."""

import asyncio
import copy
import re
import uuid
from urllib.parse import urlsplit

from pydantic import ValidationError

from oralia.course_dialogue.review_repair import complete
from oralia.course_dialogue.web_control_request import (
    FINITE_CONTROL_VERSIONS,
    WebControlRequest,
    WebControlVerdict,
    finite_control_schema,
    parse_finite_control,
)
from oralia.course_dialogue.web_review_references import SourceLocation
from oralia.documentary.study_errors import StudyFailure
from oralia.documentary.web_passages import select_web_passages
from oralia.infrastructure.generation.generation_port import EvidenceItem


# A question can mix a study doubt with an unrelated request ("¿Qué es un requisito? Y de paso, recomiéndame novelas").
_SPLIT = re.compile(r"\s*(?:[?¿!¡]|\by de paso\b|\bde paso\b|\bademás\b|\bpor cierto\b|\by también\b)\s*", re.I)


def question_parts(question):
    parts = [part.strip(" ,.;:") for part in _SPLIT.split(question)]
    return [part for part in parts if len(part.split()) >= 3]


class StudyWebFlow:
    def __init__(self, owner, web, retrieval, activity, revalidate, notify):
        if web.policy.activity != activity or web.policy.mode != "self_study":
            raise ValueError("Web policy must be enabled for this self-study activity")
        self.owner, self.web, self.retrieval = owner, web, retrieval
        self.revalidate, self.notify = revalidate, notify
        self.trace = {}
        self.sources = []
        self.narrowed = None  # in-scope part of a mixed question, set by admit_local

    def guard(self):
        self.revalidate()
        try:
            self.web.check_policy()
        except ValueError:
            raise StudyFailure("web_permission_revoked") from None

    def scope_guard(self):
        self.revalidate()
        try:
            self.web.check_activity_scope()
        except ValueError:
            raise StudyFailure("scope_policy_required") from None

    async def judge(self, control, base, evidence, concepts=()):
        guard = self.scope_guard if control == "scope" else self.guard
        guard()
        version = getattr(self.owner, "control_prompt_version", "web-control/v1")
        scope = getattr(self.web, "activity_scope", None)
        if control == "scope" and scope is None:
            raise StudyFailure("scope_policy_required")
        request = WebControlRequest(
            purpose=base.purpose,
            instruction="Registered advisory web control",
            question=base.student_input,
            control=control,
            allowed_concepts=list(concepts),
            evidence=evidence,
            conversation_history=base.conversation_history,
            prompt_version=version,
            scope_binding=(
                {**dict(scope), "concepts": list(scope["concepts"])} if control == "scope" else None
            ),
            output_schema=(
                finite_control_schema(control, concepts) if version in FINITE_CONTROL_VERSIONS else None
            ),
        )
        # Web controls may run on their own model (the llama.cpp provider uses the generator server).
        control_adapter = getattr(self.owner, "control_adapter", None) or self.owner.critic_adapter
        for attempt in range(2):
            guard()
            self.owner.review_budget.reserve()
            async with asyncio.timeout(
                min(180, max(0, self.owner.deadline - asyncio.get_running_loop().time()))
            ):
                result = await control_adapter.generate(request)
            guard()
            self.trace.setdefault("controls", []).append(
                {
                    "control": control,
                    "request": request.model_dump(),
                    "outcome": result.model_dump(),
                    "transport": copy.deepcopy(getattr(control_adapter, "last_exchange", None)),
                    "decision_contract": version,
                    "rationale_source": (
                        "host_metadata_not_model_explanation"
                        if version in FINITE_CONTROL_VERSIONS
                        else "model_advisory"
                    ),
                }
            )
            if not complete(result):
                raise StudyFailure("web_review_unresolved")
            try:
                if version in FINITE_CONTROL_VERSIONS:
                    if (
                        result.parameters.get("finite_decoder") != 1
                        or result.parameters.get("finite_after_thinking") != 1
                    ):
                        raise StudyFailure("web_review_unresolved")
                    verdict = parse_finite_control(result.text, control, concepts)
                else:
                    verdict = WebControlVerdict.model_validate_json(result.text)
                break
            except ValueError as error:
                if version in FINITE_CONTROL_VERSIONS:
                    raise StudyFailure("web_review_unresolved") from error
                syntax_only = isinstance(error, ValidationError) and all(
                    item["type"] == "json_invalid" for item in error.errors()
                )
                if attempt or not syntax_only:
                    raise StudyFailure("web_review_unresolved") from error
                self.trace.setdefault("format_retries", []).append(
                    {"control": control, "reason": "json_invalid"}
                )
                request = request.model_copy(deep=True)
                request.format_reminder = True
        valid = {
            "scope": {"in_scope", "outside", "unknown"},
            "gap": {"sufficient", "needs_web", "outside", "unknown"},
            "support": {"supported", "rejected", "unknown"},
            "compatibility": {"compatible", "conflict", "unknown"},
        }[control]
        if verdict.status not in valid or not verdict.reason.strip():
            raise StudyFailure("web_review_unresolved")
        if control == "gap" and verdict.status == "needs_web" and verdict.concept not in concepts:
            raise StudyFailure("web_scope_uncertain")
        if control == "scope" and verdict.status == "in_scope" and verdict.concept not in concepts:
            raise StudyFailure("scope_uncertain")
        # Bibliographic wording is advisory, not a semantic proof or an acceptance gate.
        return verdict

    async def judge_scope(self, base):
        """Scope of the question on its own; only if it needs context (`unknown`), with the previous question.

        Measured on follow-ups ("dame un ejemplo de eso") the judge given the whole previous answer admitted 44 % of
        them; the previous question plus the follow-up admitted 86-93 %, and asking the question alone first keeps
        off-topic questions out even right after a valid turn (0 of 42 admitted).
        """
        concepts = self.web.policy.concepts
        alone = base.model_copy(update={"conversation_history": []})
        verdict = await self.judge("scope", alone, [], concepts)
        previous = next((m.content for m in reversed(base.conversation_history) if m.role == "user"), None)
        if verdict.status != "unknown" or previous is None:
            return verdict
        joined = alone.model_copy(update={"student_input": f"{previous} {base.student_input}"[:2000]})
        return await self.judge("scope", joined, [], concepts)

    async def admit_local(self, base):
        self.trace = {"status": "activity_scope_check", "controls": [], "publication_allowed": False}
        self.sources = []
        self.narrowed = None
        verdict = await self.judge_scope(base)
        if verdict.status == "outside":
            parts = question_parts(base.student_input)
            kept = []
            if len(parts) > 1:  # judged on their own; only the parts inside the scope are answered
                for part in parts[:4]:
                    one = await self.judge_scope(base.model_copy(update={"student_input": part}))
                    if one.status == "in_scope":
                        kept.append(part)
            if not kept:
                raise StudyFailure("scope_outside")
            self.narrowed = " ".join(kept)
        elif verdict.status != "in_scope":
            raise StudyFailure("scope_uncertain")
        self.trace["status"] = "activity_scope_admitted_not_answer_verified"

    async def extend(self, base, locations):
        self.trace = {"status": "local_check", "controls": [], "publication_allowed": False}
        self.sources = []
        gap = await self.judge("gap", base, base.evidence, self.web.policy.concepts)
        if gap.status == "sufficient":
            if not base.evidence:
                self.trace["status"] = "empty_local_sufficient_rejected"
                raise StudyFailure("web_no_evidence")
            self.trace["status"] = "local_sufficient"
            return base, locations
        if gap.status != "needs_web":
            raise StudyFailure("web_scope_uncertain")
        from oralia.documentary.web_evidence import LocalGap

        turn = self.web.for_turn()
        decision_id = str(uuid.uuid4())
        receipt = await turn.acquire(
            decision_id,
            LocalGap(
                turn.policy.activity,
                gap.concept,
                "in_scope",
                "insufficient",
                decision_id,
                (
                    f"qwen3-finite-advisory/{self.owner.control_prompt_version.split('/')[-1]}"
                    if getattr(self.owner, "control_prompt_version", None) in FINITE_CONTROL_VERSIONS
                    else "qwen3-advisory-web-control/v1"
                ),
                gap.reason,
                "current-chat-turn",
                simulated=self.owner.diagnostic_label.startswith("FIXTURE"),
            ),
            self.notify,
        )
        self.guard()
        self.trace["acquisition"] = copy.deepcopy(receipt)
        documents = [
            d for d in receipt["documents"] if not d.get("duplicate_of") and not d.get("injection_detected")
        ]
        if not documents:
            raise StudyFailure("web_no_evidence")
        external = []
        remaining = 8000
        selected_documents = []
        for position, doc in enumerate(documents):
            text = "\n".join(doc["fragments"])
            header = (
                f"Información de Internet. URL: {doc['url']}; "
                f"entidad: {doc['entity']}; edición: {doc['edition']}\n"
            )
            allowance = min(6000, remaining // (len(documents) - position) - len(header))
            if allowance < 256:
                self.trace.setdefault("omitted_external", []).append(
                    {"url": doc["url"], "reason": "context_budget"}
                )
                continue
            selection = select_web_passages(
                text,
                base.student_input,
                gap.concept,
                [m.content for m in base.conversation_history[-2:]],
                allowance,
                preferred_ranges=doc.get("primary_text_ranges"),
            )
            if selection["source_sha256"] != doc["text_sha256"]:
                raise StudyFailure("web_no_evidence")
            self.trace.setdefault("web_passages", []).append({"url": doc["url"], **selection})
            if not selection["text"]:
                continue
            text = header + selection["text"]
            remaining -= len(text)
            selected_documents.append(doc)
            external.append(
                EvidenceItem(
                    fragment_id="web:" + doc["capture_sha256"],
                    text=text,
                    document_id="internet/" + doc["capture_sha256"],
                    document_version=turn.policy.version,
                )
            )
        if not external or sum(len(item.text) for item in external) > 8000:
            raise StudyFailure("web_no_evidence")
        support = await self.judge("support", base, external)
        if support.status != "supported":
            raise StudyFailure("web_review_unresolved")
        # Compare all active teacher-supplied units, not only initial top-k. Batches are explicit.
        batches, batch, chars = [], [], 0
        for key, page in self.retrieval.pages.items():
            if page["status"] != "disponible":
                continue
            origin = self.retrieval.documents[page["document_id"]].get("origin", "")
            if urlsplit(origin).scheme in {"http", "https"}:
                continue  # Archived public references are not relabelled as teacher originals.
            text = page["text"]
            if len(text) > 8000:
                raise StudyFailure("web_review_unresolved")
            if batch and chars + len(text) > 8000:
                batches.append(batch)
                batch, chars = [], 0
            filename = self.retrieval.documents[page["document_id"]]["filename"]
            batch.append(
                EvidenceItem(
                    fragment_id="teacher:" + key,
                    text=f"Documento docente: {filename}; página {page['page']}\n{text}",
                    document_id="teacher/" + page["document_id"],
                    document_version=2,
                )
            )
            chars += len(text)
        if batch:
            batches.append(batch)
        if not batches:
            raise StudyFailure("web_review_unresolved")
        for batch in batches:
            verdict = await self.judge("compatibility", base, external + batch)
            if verdict.status != "compatible":
                raise StudyFailure(
                    "web_conflict" if verdict.status == "conflict" else "web_review_unresolved"
                )
        evidence = list(base.evidence)
        updated = dict(locations)
        for item in external:
            doc = next(d for d in selected_documents if item.fragment_id == "web:" + d["capture_sha256"])
            evidence.append(item)
            updated[item.fragment_id] = SourceLocation(
                document_id=item.document_id,
                document_version=item.document_version,
                document_title=doc["title"],
                url=doc["url"],
            )
            self.sources.append(
                {
                    "title": doc["title"],
                    "url": doc["url"],
                    "entity": doc["entity"],
                    "captured_at": doc["captured_at"],
                }
            )
        self.trace.update(status="external_ready_unverified", teacher_batches=len(batches))
        return base.model_copy(update={"evidence": evidence}), updated
