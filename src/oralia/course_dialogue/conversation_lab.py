"""Conversation wiring over the existing RAG laboratory, never participant output.

Injected review verdicts exercise interfaces. This module supplies no semantic
evaluator, scope classifier, academic answers, network or model loader.
"""

import asyncio
import inspect
from copy import deepcopy
from dataclasses import dataclass
from time import perf_counter

from oralia.course_dialogue.rag_lab import diagnostic_rag_turn


class SourcePolicyInvalid(ValueError):
    """Only binding failures use this category; provider/reviewer errors do not."""


class _CheckedBinding:
    def __init__(self, binding):
        self.binding = binding

    def _call(self, method, *args):
        try:
            return getattr(self.binding, method)(*args)
        except (ValueError, OSError) as error:
            raise SourcePolicyInvalid(str(error)) from error

    def revalidate(self, db):
        return self._call("revalidate", db)

    def assert_catalog(self, catalog, units, policy):
        return self._call("assert_catalog", catalog, units, policy)

    def assert_decision(self, scope, policy):
        return self._call("assert_decision", scope, policy)


@dataclass(frozen=True)
class PostReview:
    status: str
    reviewer_id: str
    reason: str
    simulated: bool

    def validate(self):
        if self.status not in {"supported", "rejected", "unknown"}:
            raise ValueError("invalid post-review verdict")
        if not self.reviewer_id.strip() or not self.reason.strip() or type(self.simulated) is not bool:
            raise ValueError("post-review identity, reason and simulation declaration required")


class LaboratoryConversation:
    def __init__(
        self,
        catalog,
        units,
        *,
        binding,
        db,
        scope_assessor,
        assessor,
        provider,
        post_reviewer,
        interfaces_are_simulated,
        lexical_profile="bilingual-v1",
        pedagogical_profile="baseline",
    ):
        if binding is None or post_reviewer is None or type(interfaces_are_simulated) is not bool:
            raise ValueError("binding, separate post-review and simulation declaration required")
        self._catalog, self._units = deepcopy(catalog), deepcopy(units)
        self.binding, self.db = binding, db
        self._checked_binding = _CheckedBinding(binding)
        self.scope_assessor, self.assessor = scope_assessor, assessor
        self.provider, self.post_reviewer = provider, post_reviewer
        self.interfaces_are_simulated = interfaces_are_simulated
        self.lexical_profile = lexical_profile
        self.pedagogical_profile = pedagogical_profile
        self._history = []
        self._receipts = []
        self._pending = None
        self._busy = False

    @property
    def receipts(self):
        """Inspection snapshots cannot mutate delivery authority or historical receipts."""
        return deepcopy(self._receipts)

    @property
    def history(self):
        return deepcopy(self._history)

    @property
    def catalog(self):
        return deepcopy(self._catalog)

    @property
    def units(self):
        return deepcopy(self._units)

    def _revalidate(self):
        policy = self._checked_binding.revalidate(self.db)
        self._checked_binding.assert_catalog(self._catalog, self._units, policy)

    async def turn(self, text):
        if self._busy or self._pending is not None:
            raise RuntimeError("turn running or pending display acknowledgement")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("current question required")
        self._busy = True
        started = perf_counter()
        timings = {}
        row = {
            "input": text,
            "turn_id": len(self._receipts) + 1,
            "publication_allowed": False,
            "participant_display": None,
            "interfaces_are_simulated": self.interfaces_are_simulated,
            "independent_semantics": False,
            "display_acknowledged": False,
        }

        async def timed(name, function, *args):
            begin = perf_counter()
            try:
                value = function(*args)
                return await value if inspect.isawaitable(value) else value
            finally:
                timings[name] = timings.get(name, 0) + (perf_counter() - begin) * 1000

        class TimedProvider:
            async def generate(_, request):
                row["generation_request"] = request
                outcome = await timed("generation", self.provider.generate, request)
                row["outcome"] = outcome
                row["raw_candidate"] = outcome.text
                return outcome

        async def scope(*args):
            return await timed("scope", self.scope_assessor, *args)

        async def assess(*args):
            return await timed("sufficiency", self.assessor, *args)

        def block(reason, message):
            row.update(
                reason=reason, displayed_kind="operational", displayed_text=message, laboratory_preview=None
            )

        try:
            self._revalidate()
            result = await diagnostic_rag_turn(
                self._catalog,
                self._units,
                text,
                tuple(deepcopy(self._history)),
                scope_assessor=scope,
                assessor=assess,
                provider=TimedProvider(),
                binding=self._checked_binding,
                db=self.db,
                lexical_profile=self.lexical_profile,
                pedagogical_profile=self.pedagogical_profile,
            )
            row.update(result)
            if row.get("laboratory_preview") is not None:
                review = await timed(
                    "post_review",
                    self.post_reviewer,
                    row["generation_request"],
                    row["raw_candidate"],
                    row["evidence_attempts"].delivered,
                )
                if not isinstance(review, PostReview):
                    raise TypeError("typed post-review required")
                review.validate()
                row["review"] = review
                self._revalidate()
                if review.status != "supported":
                    block(
                        "post_review_" + review.status,
                        "La revisión no ha confirmado esta respuesta. ¿Puedes concretar la duda?",
                    )
                else:
                    row["semantic_support"] = (
                        "simulated_supported" if review.simulated else "review_reported_supported"
                    )
                    if row.get("scope_notice"):
                        row["displayed_text"] = row["scope_notice"] + "\n\n" + row["displayed_text"]
            self._revalidate()
        except asyncio.CancelledError:
            row.update(reason="cancelled", displayed_kind=None, displayed_text=None, laboratory_preview=None)
            raise
        except SourcePolicyInvalid as error:
            row["error_type"] = type(error).__name__
            block(
                "source_or_policy_invalid", "La política o las fuentes han cambiado o no están disponibles."
            )
        except Exception as error:
            row["error_type"] = type(error).__name__
            block("pipeline_error", "No se ha completado el turno. Puedes volver a plantear la duda.")
        finally:
            timings["total"] = (perf_counter() - started) * 1000
            row["timings_ms"] = timings
            self._receipts.append(row)
            self._busy = False
        self._pending = row
        return deepcopy(row)

    def acknowledge_display(self, turn_id):
        """Call only after the lab actually shows the prepared text.

        A UI should revalidate immediately before showing too. A failed final
        revalidation never appends even the prepared preview to model history.
        """
        row = self._pending
        if row is None or row["turn_id"] != turn_id:
            raise ValueError("no matching pending display")
        if row["displayed_kind"] == "laboratory_preview":
            self._revalidate()
        visible = {
            "input": row["input"],
            "displayed_text": row["displayed_text"],
            "displayed_kind": row["displayed_kind"],
            "display_kind": "candidate" if row["displayed_kind"] == "laboratory_preview" else "operational",
            "permitted_input": None,
        }
        if row["displayed_kind"] == "laboratory_preview":
            visible["academic_topic"] = row["academic_query"]
            scope = row["scope_assessment"]
            visible["permitted_input"] = scope.in_scope_question if scope.status == "mixed" else row["input"]
        self._history.append(visible)
        row["display_acknowledged"] = True
        self._pending = None

    def prepare_display(self, turn_id):
        """Revalidate just before the calling lab renderer shows the text."""
        row = self._pending
        if row is None or row["turn_id"] != turn_id:
            raise ValueError("no matching pending display")
        if row["displayed_kind"] == "laboratory_preview":
            self._revalidate()
        return row["displayed_text"]

    def discard_pending(self):
        """A failed/unshown display must not become conversation history."""
        if self._pending is not None:
            self._pending["display_discarded"] = True
            self._pending = None

    def transcript(self):
        lines = ["# Conversación de laboratorio — publicación cerrada"]
        if self.interfaces_are_simulated:
            lines.append("SIMULADO: proveedores y evaluadores de prueba; no valida calidad semántica.")
        for row in self._receipts:
            lines.extend([f"\n## Turno {row['turn_id']}", f"Pregunta: {row['input']}"])
            label = (
                "Texto mostrado"
                if row["display_acknowledged"]
                else "Texto preparado, no confirmado como mostrado"
            )
            lines.append(f"{label}: {row.get('displayed_text') or '(ninguno)'}")
            lines.append(
                f"Límite/bloqueo: {row.get('reason', 'sin bloqueo técnico; no autoriza publicación')}"
            )
            review = row.get("review")
            if review:
                lines.append(
                    f"Revisión: {review.status}; {review.reviewer_id}; {review.reason}; "
                    f"simulado={review.simulated}"
                )
            lines.append(
                "Tiempos (ms): " + ", ".join(f"{key}={value:.1f}" for key, value in row["timings_ms"].items())
            )
            attempts = row.get("evidence_attempts")
            if attempts:
                lines.append(
                    f"Recuperación: {attempts.reason}; caracteres={attempts.delivered.chars_used}; "
                    "suficiencia no inferida del score"
                )
                lines.append(
                    "Pasajes entregados al proveedor:"
                    if row.get("generation_request")
                    else "Pasajes recuperados, sin llamada al proveedor:"
                )
                for unit in attempts.delivered.units:
                    pages = ",".join(str(span.page_number) for span in unit.positions)
                    lines.append(
                        f"Fuente: {unit.document_id}; versión {unit.version}; páginas {pages}; "
                        f"id={unit.id}; sha256={unit.original_sha256}\n{unit.text}"
                    )
        return "\n\n".join(lines) + "\n"
