"""Value-closed projection for retained technical traces (schema v1).

Free-form reasons, model names and unknown/custom identifiers are omitted. This
projection describes operations; it is neither a content store nor a validator of
academic correctness. New codes must be reviewed here or in their domain enum.
"""

import math
import re
from typing import get_args

from oralia.domain.agents.agent_contract import AgentResultStatus
from oralia.domain.dialogue.contracts import StudyMode
from oralia.domain.policies.output_authorization_contract import AuthorizationReason
from oralia.domain.policies.output_template_catalog import DEFAULT_OUTPUT_TEMPLATE_CATALOG
from oralia.infrastructure.generation.generation_port import GenerationPurpose

_VERDICTS = frozenset({"approved", "block", "reformulate", "clarify", "acknowledge_missing_info"})
_GROUNDING = frozenset(
    {"fundamentada", "parcialmente_fundamentada", "no_fundamentada", "no_verificable", "conflictiva"}
)
_MODES = frozenset(get_args(StudyMode)) | {"oral_defense", "self_study"}
_CODES = frozenset(reason.value for reason in AuthorizationReason) | {
    "renderer_timeout",
    "abandoned",
    "owner_access_lost",
}
_ENUMS = {
    "status": frozenset(get_args(AgentResultStatus))
    | {
        "active",
        "completed",
        "degraded",
        "blocked",
        "closed_voluntary",
        "closed_limit_reached",
        "closed_teacher_confirmed",
        "closed_timeout",
        "closed_error",
        "closed_error_safe",
    },
    "dialogue_action": {"respond", "ask", "clarify", "finish", "acknowledge_missing_info"},
    "purpose": frozenset(get_args(GenerationPurpose))
    | {"deepen_current_topic", "switch_topic", "clarify_previous_answer", "initial_question"},
    "decision": {"retain", "discard"},
    "scope": {"transcript", "summary"},
    "adapter": {"deterministic", "ollama", "transformers_local", "guided_controlled", "direct-baseline-v2"},
    "model": {"deterministic"},
    "component": {"teacher", "defense-summary", "self-study", "defense-agency"},
    "mode": _MODES,
    "requested_mode": _MODES,
    "previous_mode": _MODES,
    "enabled_modes": _MODES,
    "grounding_verdict": _GROUNDING,
    "coherence_verdict": _VERDICTS,
    "verdict": _VERDICTS | _GROUNDING,
    "combined_outcome": _VERDICTS,
    "severity_source": {"grounding", "coherence", "both", "tie_coherence"},
    "message_type": {"normal", "operational"},
    "generation_status": {"ok", "error", "timeout", "cancelled", "unavailable", "fallback"},
    "recovery_action": {
        "none",
        "clarify",
        "reformulate",
        "switch_topic",
        "finish",
        "retry",
        "block",
        "pedir_aclaracion",
        "reformular",
        "reducir_respuesta",
    },
    "incident_types": {
        "contradiccion",
        "condiciones_no_comparables",
        "repeticion",
        "ausencia_progreso",
        "exceso_turnos_mismo_concepto",
        "perdida_objetivo",
    },
    "reason_codes": _CODES,
    "template_id": frozenset(entry.template_id for entry in DEFAULT_OUTPUT_TEMPLATE_CATALOG.entries),
    "step_id": {
        "interpret",
        "generate",
        "fallback",
        "verify-non-disclosure",
        "constitution",
        "retrieve",
        "generate-question",
        "verify-fallback",
        "generate-response",
        "verify-grounding",
        "verify-coherence",
        "constitutional-control",
        "study-intent-interpreter",
        "grounding-verifier",
        "coherence-verifier",
    },
    "agent_id": {
        "material-retriever",
        "response-generator",
        "practice-question-agent",
        "grounding-verifier",
        "coherence-verifier",
        "constitutional-control",
        "study-intent-interpreter",
        "safe-fallback",
        "followup-question-agent",
        "interpreter-deterministic",
        "solution-non-disclosure-verifier",
    },
    "role": {"generator", "verifier", "control", "retriever", "presenter"},
}
_BOOLS = {"blocked", "fallback_used", "required", "switched"}
_NUMBERS = {
    "state_version",
    "attempt",
    "turn_count",
    "incident_count",
    "duration_seconds",
    "latency_ms",
    "policy_version",
    "template_version",
    "timeout_ms",
    "fallback_attempt",
    "activity_version",
    "snapshot_version",
}
_IDS = {"verification_result_id", "proposal_id", "activity_configuration_id", "policy_id"}
_HASHES = {"policy_sha256", "template_sha256", "binding_sha256"}
_ID_LISTS = {"fragment_ids", "evidence_fragment_ids"}
_LISTS = {"scope", "enabled_modes", "reason_codes", "incident_types"}
_OBJECTS = {"authorization_context"}
_OBJECT_LISTS = {"activated_steps"}
_UUID = re.compile(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\Z")
_SHA = re.compile(r"[0-9a-f]{64}\Z")


def technical_payload(payload):
    """Retain only values with an explicit technical schema; return a fresh tree."""
    if not isinstance(payload, dict):
        return {}
    result = {}
    for key, value in payload.items():
        if value is None:
            continue
        if key in _BOOLS and type(value) is bool:
            result[key] = value
        elif key in _NUMBERS and type(value) in (int, float) and 0 <= value <= 2**53 and math.isfinite(value):
            result[key] = value
        elif key in _IDS and isinstance(value, str) and _UUID.fullmatch(value):
            result[key] = value
        elif key in _HASHES and isinstance(value, str) and _SHA.fullmatch(value):
            result[key] = value
        elif key in _ID_LISTS and isinstance(value, (list, tuple)):
            result[key] = [item for item in value if isinstance(item, str) and _UUID.fullmatch(item)]
        elif key in _LISTS and isinstance(value, (list, tuple)):
            result[key] = [item for item in value if isinstance(item, str) and item in _ENUMS[key]]
        elif key in _ENUMS and isinstance(value, str) and value in _ENUMS[key]:
            result[key] = value
        elif key in _OBJECTS and isinstance(value, dict):
            result[key] = technical_payload(value)
        elif key in _OBJECT_LISTS and isinstance(value, (list, tuple)):
            result[key] = [technical_payload(item) for item in value if isinstance(item, dict)]
    return result
