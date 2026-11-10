"""Bounded, source-bound concept review. Recorded labels are not semantic authority."""

import copy
import hashlib
import json

from oralia.course_dialogue.concept_ledger import (
    COMPACT_VERSION,
    CatalogDecision,
    ConceptLedgerRequest,
    LedgerCoverageError,
    ThinkingConceptLedgerRequest,
    UseCheck,
    answer_units,
    ledger_status,
    parse_catalog,
    parse_compact,
    parse_ledger,
    unseen_designators,
    source_cards,
)
from oralia.course_dialogue.review_repair import ReviewRepairGenerationAdapter, complete


def source_binding(base):
    data = dict(
        question=base.student_input,
        evidence=[e.model_dump() for e in base.evidence],
        history=[m.model_dump() for m in base.conversation_history],
    )
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


class ConceptInputBudgetError(ValueError):
    """Pre-dispatch context refusal, never a semantic judgment."""


class ConceptLedgerReviewer:
    def __init__(
        self,
        planner,
        critic,
        *,
        budget,
        revalidate,
        record=None,
        batch_size=4,
        prompt_version="concept-ledger/v4",
        request_check=None,
    ):
        if type(batch_size) is not int or not 1 <= batch_size <= 8:
            raise ValueError("explicit answer batch budget required")
        if planner is None and prompt_version != COMPACT_VERSION:
            raise ValueError("only the compact one-call review may run without a planner")
        self.planner = (
            None
            if planner is None
            else ReviewRepairGenerationAdapter(planner, budget=budget, revalidate=revalidate, record=record)
        )
        self.critic = ReviewRepairGenerationAdapter(
            critic, budget=budget, revalidate=revalidate, record=record
        )
        self.batch_size = batch_size
        if prompt_version not in {
            "concept-ledger/v1",
            "concept-ledger/v2",
            "concept-ledger/v3",
            "concept-ledger/v4",
            COMPACT_VERSION,
        }:
            raise ValueError("unknown concept ledger version")
        self.prompt_version = prompt_version
        self.request_check = request_check
        self.revalidate = revalidate

    async def _ask(self, port, request, parser, trace):
        if self.request_check:
            self.request_check(request)
        outcome = await port.call("review", request, trace)
        if not complete(outcome):
            raise ValueError("concept stage incomplete")
        try:
            return parser(outcome.text)
        except ValueError as first:
            trace.setdefault("invalid_outputs", []).append(str(first))
            if trace["format_retries"]:
                raise
            trace["format_retries"] += 1
            retry = request.model_copy(deep=True)
            retry.format_reminder = True
            if self.request_check:
                self.request_check(retry)
            outcome = await port.call("review", retry, trace)
            if not complete(outcome):
                raise ValueError("concept format retry incomplete") from None
            return parser(outcome.text)

    async def review_compact(self, base, answer, *, catalogue=None, prepared=None, web_source_ids=()):
        """One ordinary call over the whole answer. Contract failures are kept, never re-asked."""
        base = base.model_copy(deep=True)
        if prepared is not None:
            if catalogue is not None:
                raise ValueError("choose prepared material or a turn catalogue, not both")
            catalogue = prepared.for_turn(base, revalidate=self.revalidate)
        if catalogue is None:
            catalogue = dict(binding=source_binding(base), decision=CatalogDecision(selected=[]).model_dump())
        elif catalogue.get("binding") != source_binding(base):
            raise ValueError("catalogue belongs to a different question, history or source revision")
        plan = parse_catalog(json.dumps(catalogue["decision"]), base.evidence)
        trace = dict(
            calls=[],
            checks=[],
            format_retries=0,
            status="running",
            publication_allowed=False,
            participant_display=None,
            independent_semantics=False,
            source_cards=source_cards(base.evidence),
            answer_units=answer_units(answer, attach_keywords=True),
            catalogue=catalogue,
        )
        self.last_trace = trace
        request = ThinkingConceptLedgerRequest(
            prompt_version=COMPACT_VERSION,
            web_source_ids=list(web_source_ids),
            purpose=base.purpose,
            instruction="Compact whole-answer concept review",
            question=base.student_input,
            evidence=base.evidence,
            draft=answer,
            conversation_history=base.conversation_history,
            selected_cards=plan.selected,
            missing_definitions=plan.missing_definitions,
            proposed_labels=plan.proposed_labels,
            assigned_units=[u["id"] for u in trace["answer_units"]],
            constraints={"max_tokens": 6144, "deadline_ms": 120000},
        )

        def technical(reason, detail=""):
            trace["status"] = "technical_failure"
            trace["technical_failure"] = dict(reason=reason, detail=detail)
            return trace

        try:
            if self.request_check:
                self.request_check(request)
        except ConceptInputBudgetError as exc:
            return technical("input_budget", str(exc))
        # Cancellation, revocation, deadline and call-budget errors propagate unchanged.
        outcome = await self.critic.call("review", request, trace)
        if not complete(outcome):
            return technical("incomplete_output")
        try:
            review = parse_compact(outcome.text, request)
        except ValueError as exc:
            trace.setdefault("invalid_outputs", []).append(str(exc))
            return technical("invalid_contract", str(exc))
        # Attribution is settled by the host from the text: a named standard-like designator that no source
        # contains (docente or web) promotes a flagged unit to a noticeable attribution; an attribution with
        # no such unseen name stays a doubt.
        units = {u["id"]: u["text"] for u in trace["answer_units"]}
        sources = [e.text for e in base.evidence]
        promoted, unverified = [], []
        for index, issue in enumerate(review.issues):
            text = units.get(issue.use_id, "")
            if issue.kind in ("attribution", "unsupported") and unseen_designators(text, sources):
                if issue.kind != "attribution" or issue.verdict != "incorrect":
                    review.issues[index] = issue.model_copy(update={"kind": "attribution", "verdict": "incorrect"})
                    promoted.append(issue.use_id)
            elif issue.kind == "attribution" and issue.verdict == "incorrect":
                review.issues[index] = issue.model_copy(update={"verdict": "uncertain"})
                unverified.append(issue.use_id)
        if promoted:
            trace["attribution_promoted"] = promoted
        if unverified:
            trace["attribution_unverified"] = unverified
        # Only objections (by the host's kind table) and genuine uncertainty are checks; the rest are notes.
        trace["checks"] = [
            dict(use_id=i.use_id, kind=i.kind, card_ids=i.card_ids, verdict=i.verdict, reason=i.reason)
            for i in review.issues
            if i in review.objections or i.verdict == "uncertain"
        ]
        trace["notes"] = [
            dict(use_id=i.use_id, kind=i.kind, card_ids=i.card_ids, reason=i.reason) for i in review.notes
        ]
        trace["status"] = review.status
        return trace

    async def review(self, base, answer, *, catalogue=None, prepared=None, web_source_ids=()):
        if self.prompt_version == COMPACT_VERSION:
            return await self.review_compact(
                base, answer, catalogue=catalogue, prepared=prepared, web_source_ids=web_source_ids
            )
        base = base.model_copy(deep=True)
        if prepared is not None:
            if catalogue is not None:
                raise ValueError("choose prepared material or a turn catalogue, not both")
            catalogue = prepared.for_turn(base, revalidate=self.revalidate)
        trace = dict(
            calls=[],
            checks=[],
            format_retries=0,
            status="running",
            publication_allowed=False,
            participant_display=None,
            independent_semantics=False,
            source_cards=source_cards(base.evidence),
            answer_units=answer_units(
                answer, attach_keywords=self.prompt_version in {"concept-ledger/v3", "concept-ledger/v4"}
            ),
        )
        self.last_trace = trace

        if catalogue is None:
            request = ConceptLedgerRequest(
                prompt_version=self.prompt_version,
                purpose=base.purpose,
                instruction="Source-only concept planning",
                ledger_stage="catalog",
                question=base.student_input,
                evidence=base.evidence,
                conversation_history=base.conversation_history,
                constraints={"max_tokens": 1024, "deadline_ms": 180000},
            )
            plan = await self._ask(
                self.planner, request, lambda text: parse_catalog(text, base.evidence), trace
            )
            catalogue = dict(binding=source_binding(base), decision=plan.model_dump())
        else:
            if catalogue.get("binding") != source_binding(base):
                raise ValueError("catalogue belongs to a different question, history or source revision")
            plan = parse_catalog(json.dumps(catalogue["decision"]), base.evidence)
        trace["catalogue"] = catalogue
        units = trace["answer_units"]
        offset = 0
        while offset < len(units):
            size = min(self.batch_size, len(units) - offset)
            while True:
                assigned = [u["id"] for u in units[offset : offset + size]]
                request = ThinkingConceptLedgerRequest(
                    prompt_version=self.prompt_version,
                    purpose=base.purpose,
                    instruction="Explicit concept use check",
                    question=base.student_input,
                    evidence=base.evidence,
                    draft=answer,
                    conversation_history=base.conversation_history,
                    selected_cards=plan.selected,
                    missing_definitions=plan.missing_definitions,
                    proposed_labels=plan.proposed_labels,
                    assigned_units=assigned,
                    constraints={"max_tokens": 8192, "deadline_ms": 180000},
                )
                try:
                    if self.request_check:
                        self.request_check(request)
                    ledger = await self._ask(
                        self.critic, request, lambda text, req=request: parse_ledger(text, req), trace
                    )
                    break
                except (ConceptInputBudgetError, LedgerCoverageError) as exc:
                    key = (
                        "coverage_batch_splits"
                        if isinstance(exc, LedgerCoverageError)
                        else "input_batch_splits"
                    )
                    trace.setdefault(key, []).append(dict(assigned=assigned, reason=str(exc)))
                    if size == 1 or (
                        isinstance(exc, LedgerCoverageError) and self.prompt_version != "concept-ledger/v4"
                    ):
                        raise
                    size = max(1, size // 2)
            trace["checks"].extend(c.model_dump() for c in ledger.checks)
            offset += size
        trace["status"] = ledger_status([UseCheck.model_validate(c) for c in trace["checks"]])
        if self.prompt_version == "concept-ledger/v4":
            trace = await self.augment_labels(base, answer, trace)
        return trace

    async def augment_labels(self, base, answer, original):
        from oralia.course_dialogue.concept_labels import ConceptLabelRequest, parse_label_relations

        if original["catalogue"]["binding"] != source_binding(base):
            raise ValueError("label check has a foreign source/question binding")
        if original["answer_units"] != answer_units(answer, attach_keywords=True):
            raise ValueError("label check has different answer units")
        if original["source_cards"] != source_cards(base.evidence):
            raise ValueError("label source catalogue changed")
        trace = copy.deepcopy(original)
        self.last_trace = trace
        trace["primary_status"] = trace["status"]
        trace["label_checks"] = []
        cards = {c["id"]: c for c in trace["source_cards"]}
        units = {u["id"]: u for u in trace["answer_units"]}
        targets = []
        for check in trace["checks"]:
            unit = units[check["use_id"]]
            named = [c for c in check["card_ids"] if cards[c]["source_name"]]
            if check["verdict"] == "correct" and unit["label"] and named:
                targets.append(dict(use_id=unit["id"], label=unit["label"], card_ids=named))
        trace["label_targets"] = targets
        for offset in range(0, len(targets), 4):
            batch = targets[offset : offset + 4]
            req = ConceptLabelRequest(
                purpose=base.purpose,
                instruction="Independent labels, no candidate description",
                question="Comparación de denominaciones",
                evidence=base.evidence,
                targets=batch,
                proposed_labels=trace["catalogue"]["decision"].get("proposed_labels", {}),
                constraints={"max_tokens": 1024, "deadline_ms": 180000},
            )
            result = await self._ask(
                self.planner, req, lambda text, r=req: parse_label_relations(text, r), trace
            )
            by_id = {t["use_id"]: t for t in batch}
            trace["label_checks"].extend(
                dict(**r.model_dump(), label=by_id[r.use_id]["label"], card_ids=by_id[r.use_id]["card_ids"])
                for r in result.relations
            )
        if any(r["relation"] == "different" for r in trace["label_checks"]):
            trace["status"] = "issues_found"
        elif trace["status"] == "no_issues_found" and any(
            r["relation"] == "uncertain" for r in trace["label_checks"]
        ):
            trace["status"] = "insufficient_evidence"
        return trace


def repair_observations(trace):
    """Bind model objections to original answer/source units; never invent a critique."""
    units = {u["id"]: u for u in trace["answer_units"]}
    cards = {c["id"]: c for c in trace["source_cards"]}
    observations = []
    for check in trace["checks"]:
        if check["verdict"] != "incorrect":
            continue
        sources = list(dict.fromkeys(cards[c]["source_id"] for c in check["card_ids"]))
        observations.append(
            dict(
                kind="concept_use",
                claim=units[check["use_id"]]["text"],
                explanation=check["reason"],
                evidence=[dict(source_id=s) for s in sources],
            )
        )
    for check in trace.get("label_checks", []):
        if check["relation"] != "different":
            continue
        sources = list(dict.fromkeys(cards[c]["source_id"] for c in check["card_ids"]))
        observations.append(
            dict(
                kind="concept_label",
                claim=units[check["use_id"]]["text"],
                explanation=check["reason"],
                evidence=[dict(source_id=s) for s in sources],
            )
        )
    if not observations or len(observations) > 5:
        raise ValueError("no repairable issues or correction budget exceeded; full ledger retained")
    return observations
