# Validación arquitectónica ORAL-IA

## Observaciones y límites

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

Celdas: 306; repeticiones por celda: 3.

## Métricas observadas

| Condición | n | Errores | Bloqueos | Timeouts | Recuperaciones | Traza completa | Latencia media ms |
|---|---|---|---|---|---|---|---|
| no_grounding | 51 | 0 | 12 | 3 | 15 | 51/51 | 184.732 |
| baseline | 51 | 0 | 3 | 0 | 3 | 0/0 | 137.913 |
| presentation | 51 | 0 | 6 | 3 | 15 | 51/51 | 165.061 |
| full | 51 | 0 | 6 | 3 | 15 | 51/51 | 160.802 |
| top1 | 51 | 0 | 6 | 3 | 15 | 51/51 | 165.891 |
| no_coherence | 51 | 0 | 3 | 3 | 15 | 51/51 | 171.095 |

JSON incluye n/media/min/max/desviación de cada métrica y latencia por agente. Desviación ausente con n<2; GPU/tokens y opiniones faltantes con motivo.

## Por escenario y configuración

| Escenario | Condición | Repetición | Decisión | Grounding | Coherencia | Error | Recuperación |
|---|---|---|---|---|---|---|---|
| turn_limit | no_grounding | 0 | clarify | fundamentada | reformulate | None | None |
| turn_limit | baseline | 0 | respond | None | None | None | None |
| academic_grade | presentation | 1 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| out_of_scope | full | 0 | acknowledge_missing_info | None | None | None | None |
| state_conflict | full | 2 | respond | fundamentada | approved | None | None |
| clear_evidence | top1 | 1 | respond | fundamentada | approved | None | None |
| repetition | no_grounding | 0 | clarify | fundamentada | reformulate | None | None |
| conversational_contradiction | no_grounding | 0 | finish | fundamentada | block | None | None |
| turn_limit | top1 | 1 | clarify | fundamentada | reformulate | None | None |
| academic_grade | no_coherence | 1 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| agent_timeout | baseline | 1 | respond | None | None | None | None |
| model_unavailable | no_coherence | 2 | respond | fundamentada | approved | None | reserve_or_safe_output |
| no_evidence | no_grounding | 2 | acknowledge_missing_info | None | None | None | None |
| out_of_scope | baseline | 1 | respond | None | None | None | None |
| unsupported_claim | presentation | 2 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| resource_unavailable | no_coherence | 2 | acknowledge_missing_info | None | None | None | missing_evidence_after_closed_worker |
| turn_limit | no_coherence | 1 | respond | fundamentada | approved | None | None |
| deletion | no_grounding | 2 | respond | fundamentada | approved | None | None |
| academic_grade | full | 2 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| clear_evidence | presentation | 0 | re_ask | fundamentada | approved | None | None |
| turn_limit | baseline | 2 | respond | None | None | None | None |
| out_of_scope | no_coherence | 1 | acknowledge_missing_info | None | None | None | None |
| deletion | full | 2 | respond | fundamentada | approved | None | None |
| unsupported_claim | no_coherence | 2 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| deletion | no_coherence | 2 | respond | fundamentada | approved | None | None |
| clear_evidence | full | 0 | respond | fundamentada | approved | None | None |
| model_unavailable | baseline | 0 | respond | None | None | None | None |
| agent_timeout | full | 2 | clarify | None | None | None | safe_fallback |
| model_unavailable | no_coherence | 1 | respond | fundamentada | approved | None | reserve_or_safe_output |
| repetition | full | 0 | clarify | fundamentada | reformulate | None | None |
| out_of_scope | full | 1 | acknowledge_missing_info | None | None | None | None |
| resource_unavailable | presentation | 1 | acknowledge_missing_info | None | None | None | missing_evidence_after_closed_worker |
| transcription_correction | presentation | 1 | finish | fundamentada | approved | None | None |
| out_of_scope | baseline | 2 | respond | None | None | None | None |
| index_unavailable | full | 0 | acknowledge_missing_info | None | None | None | missing_evidence_or_safe_output |
| conflicting_sources | presentation | 0 | clarify | conflictiva | approved | None | None |
| no_evidence | presentation | 0 | acknowledge_missing_info | None | None | None | None |
| repetition | full | 2 | clarify | fundamentada | reformulate | None | None |
| state_conflict | presentation | 2 | re_ask | fundamentada | approved | None | None |
| conversational_contradiction | baseline | 2 | respond | None | None | None | None |
| conversational_contradiction | top1 | 0 | finish | fundamentada | block | None | None |
| turn_limit | full | 0 | clarify | fundamentada | reformulate | None | None |
| agent_timeout | top1 | 2 | clarify | None | None | None | safe_fallback |
| clear_evidence | no_coherence | 1 | respond | fundamentada | approved | None | None |
| state_conflict | baseline | 2 | respond | None | None | None | None |
| no_evidence | presentation | 1 | acknowledge_missing_info | None | None | None | None |
| index_unavailable | no_grounding | 2 | acknowledge_missing_info | None | None | None | missing_evidence_or_safe_output |
| clear_evidence | full | 1 | respond | fundamentada | approved | None | None |
| conversational_contradiction | presentation | 2 | finish | fundamentada | block | None | None |
| deletion | top1 | 1 | respond | fundamentada | approved | None | None |
| transcription_correction | top1 | 0 | finish | fundamentada | approved | None | None |
| transcription_correction | no_coherence | 2 | finish | fundamentada | approved | None | None |
| academic_grade | presentation | 0 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| turn_limit | presentation | 2 | clarify | fundamentada | reformulate | None | None |
| agent_timeout | top1 | 0 | clarify | None | None | None | safe_fallback |
| unsupported_claim | presentation | 1 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| unsupported_claim | no_grounding | 0 | finish | fundamentada | approved | None | None |
| agent_timeout | presentation | 2 | clarify | None | None | None | safe_fallback |
| transcription_failure | no_grounding | 2 | respond | fundamentada | approved | None | text_after_observed_stt_failure |
| clear_evidence | presentation | 1 | re_ask | fundamentada | approved | None | None |
| transcription_failure | top1 | 1 | respond | fundamentada | approved | None | text_after_observed_stt_failure |
| academic_grade | no_grounding | 0 | finish | fundamentada | approved | None | None |
| no_evidence | baseline | 0 | respond | None | None | None | None |
| unsupported_claim | baseline | 0 | respond | None | None | None | None |
| state_conflict | no_coherence | 2 | respond | fundamentada | approved | None | None |
| model_unavailable | top1 | 1 | respond | fundamentada | approved | None | reserve_or_safe_output |
| conversational_contradiction | baseline | 1 | respond | None | None | None | None |
| conflicting_sources | full | 1 | clarify | conflictiva | approved | None | None |
| resource_unavailable | no_coherence | 1 | acknowledge_missing_info | None | None | None | missing_evidence_after_closed_worker |
| conversational_contradiction | top1 | 2 | finish | fundamentada | block | None | None |
| out_of_scope | top1 | 1 | acknowledge_missing_info | None | None | None | None |
| deletion | baseline | 1 | respond | None | None | None | None |
| conversational_contradiction | baseline | 0 | respond | None | None | None | None |
| transcription_failure | presentation | 0 | re_ask | fundamentada | approved | None | text_after_observed_stt_failure |
| turn_limit | top1 | 2 | clarify | fundamentada | reformulate | None | None |
| agent_timeout | baseline | 0 | respond | None | None | None | None |
| conversational_contradiction | no_grounding | 1 | finish | fundamentada | block | None | None |
| repetition | baseline | 2 | respond | None | None | None | None |
| transcription_correction | no_coherence | 0 | finish | fundamentada | approved | None | None |
| no_evidence | full | 0 | acknowledge_missing_info | None | None | None | None |
| transcription_correction | no_coherence | 1 | finish | fundamentada | approved | None | None |
| no_evidence | no_coherence | 0 | acknowledge_missing_info | None | None | None | None |
| index_unavailable | no_coherence | 1 | acknowledge_missing_info | None | None | None | missing_evidence_or_safe_output |
| transcription_correction | top1 | 1 | finish | fundamentada | approved | None | None |
| index_unavailable | full | 1 | acknowledge_missing_info | None | None | None | missing_evidence_or_safe_output |
| state_conflict | presentation | 1 | re_ask | fundamentada | approved | None | None |
| transcription_correction | full | 2 | finish | fundamentada | approved | None | None |
| unsupported_claim | top1 | 2 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| index_unavailable | presentation | 1 | acknowledge_missing_info | None | None | None | missing_evidence_or_safe_output |
| unsupported_claim | no_grounding | 2 | finish | fundamentada | approved | None | None |
| out_of_scope | no_grounding | 1 | acknowledge_missing_info | None | None | None | None |
| conversational_contradiction | full | 1 | finish | fundamentada | block | None | None |
| conversational_contradiction | full | 0 | finish | fundamentada | block | None | None |
| resource_unavailable | baseline | 2 | respond | None | None | None | None |
| transcription_correction | presentation | 2 | finish | fundamentada | approved | None | None |
| state_conflict | baseline | 0 | respond | None | None | None | None |
| deletion | full | 1 | respond | fundamentada | approved | None | None |
| state_conflict | no_grounding | 2 | respond | fundamentada | approved | None | None |
| conflicting_sources | full | 2 | clarify | conflictiva | approved | None | None |
| academic_grade | full | 0 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| model_unavailable | no_coherence | 0 | respond | fundamentada | approved | None | reserve_or_safe_output |
| conflicting_sources | top1 | 2 | clarify | conflictiva | approved | None | None |
| resource_unavailable | full | 0 | acknowledge_missing_info | None | None | None | missing_evidence_after_closed_worker |
| agent_timeout | no_coherence | 2 | clarify | None | None | None | safe_fallback |
| academic_grade | top1 | 0 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| repetition | full | 1 | clarify | fundamentada | reformulate | None | None |
| transcription_correction | baseline | 0 | respond | fundamentada | approved | None | None |
| out_of_scope | full | 2 | acknowledge_missing_info | None | None | None | None |
| agent_timeout | no_grounding | 1 | clarify | None | None | None | safe_fallback |
| transcription_correction | no_grounding | 1 | finish | fundamentada | approved | None | None |
| turn_limit | presentation | 0 | clarify | fundamentada | reformulate | None | None |
| index_unavailable | no_coherence | 2 | acknowledge_missing_info | None | None | None | missing_evidence_or_safe_output |
| conversational_contradiction | no_coherence | 0 | respond | fundamentada | approved | None | None |
| out_of_scope | no_coherence | 0 | acknowledge_missing_info | None | None | None | None |
| state_conflict | top1 | 0 | respond | fundamentada | approved | None | None |
| transcription_failure | baseline | 0 | respond | None | None | None | text_after_observed_stt_failure |
| academic_grade | baseline | 0 | block | None | None | None | None |
| out_of_scope | no_coherence | 2 | acknowledge_missing_info | None | None | None | None |
| state_conflict | full | 1 | respond | fundamentada | approved | None | None |
| state_conflict | baseline | 1 | respond | None | None | None | None |
| index_unavailable | no_grounding | 1 | acknowledge_missing_info | None | None | None | missing_evidence_or_safe_output |
| transcription_correction | full | 1 | finish | fundamentada | approved | None | None |
| no_evidence | full | 2 | acknowledge_missing_info | None | None | None | None |
| clear_evidence | no_grounding | 1 | respond | fundamentada | approved | None | None |
| out_of_scope | presentation | 2 | acknowledge_missing_info | None | None | None | None |
| repetition | no_coherence | 2 | respond | fundamentada | approved | None | None |
| no_evidence | top1 | 0 | acknowledge_missing_info | None | None | None | None |
| model_unavailable | full | 2 | respond | fundamentada | approved | None | reserve_or_safe_output |
| conversational_contradiction | no_grounding | 2 | finish | fundamentada | block | None | None |
| repetition | top1 | 2 | clarify | fundamentada | reformulate | None | None |
| transcription_failure | full | 0 | respond | fundamentada | approved | None | text_after_observed_stt_failure |
| deletion | baseline | 0 | respond | None | None | None | None |
| deletion | no_grounding | 1 | respond | fundamentada | approved | None | None |
| index_unavailable | baseline | 1 | respond | None | None | None | None |
| clear_evidence | top1 | 0 | respond | fundamentada | approved | None | None |
| transcription_correction | no_grounding | 2 | finish | fundamentada | approved | None | None |
| deletion | top1 | 0 | respond | fundamentada | approved | None | None |
| model_unavailable | full | 1 | respond | fundamentada | approved | None | reserve_or_safe_output |
| deletion | top1 | 2 | respond | fundamentada | approved | None | None |
| repetition | baseline | 1 | respond | None | None | None | None |
| out_of_scope | top1 | 2 | acknowledge_missing_info | None | None | None | None |
| resource_unavailable | presentation | 0 | acknowledge_missing_info | None | None | None | missing_evidence_after_closed_worker |
| transcription_failure | full | 2 | respond | fundamentada | approved | None | text_after_observed_stt_failure |
| model_unavailable | no_grounding | 0 | respond | fundamentada | approved | None | reserve_or_safe_output |
| agent_timeout | no_coherence | 1 | clarify | None | None | None | safe_fallback |
| turn_limit | top1 | 0 | clarify | fundamentada | reformulate | None | None |
| unsupported_claim | no_coherence | 0 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| unsupported_claim | no_coherence | 1 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| agent_timeout | no_coherence | 0 | clarify | None | None | None | safe_fallback |
| unsupported_claim | no_grounding | 1 | finish | fundamentada | approved | None | None |
| academic_grade | full | 1 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| clear_evidence | baseline | 0 | respond | None | None | None | None |
| agent_timeout | baseline | 2 | respond | None | None | None | None |
| state_conflict | top1 | 2 | respond | fundamentada | approved | None | None |
| academic_grade | top1 | 2 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| turn_limit | no_coherence | 0 | respond | fundamentada | approved | None | None |
| model_unavailable | no_grounding | 2 | respond | fundamentada | approved | None | reserve_or_safe_output |
| academic_grade | no_coherence | 0 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| clear_evidence | presentation | 2 | re_ask | fundamentada | approved | None | None |
| academic_grade | no_grounding | 1 | finish | fundamentada | approved | None | None |
| unsupported_claim | presentation | 0 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| clear_evidence | no_grounding | 0 | respond | fundamentada | approved | None | None |
| repetition | no_coherence | 1 | respond | fundamentada | approved | None | None |
| transcription_failure | top1 | 0 | respond | fundamentada | approved | None | text_after_observed_stt_failure |
| transcription_failure | no_coherence | 2 | respond | fundamentada | approved | None | text_after_observed_stt_failure |
| academic_grade | no_coherence | 2 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| state_conflict | no_grounding | 1 | respond | fundamentada | approved | None | None |
| out_of_scope | no_grounding | 2 | acknowledge_missing_info | None | None | None | None |
| index_unavailable | full | 2 | acknowledge_missing_info | None | None | None | missing_evidence_or_safe_output |
| clear_evidence | full | 2 | respond | fundamentada | approved | None | None |
| model_unavailable | no_grounding | 1 | respond | fundamentada | approved | None | reserve_or_safe_output |
| no_evidence | baseline | 1 | respond | None | None | None | None |
| index_unavailable | top1 | 2 | acknowledge_missing_info | None | None | None | missing_evidence_or_safe_output |
| index_unavailable | top1 | 1 | acknowledge_missing_info | None | None | None | missing_evidence_or_safe_output |
| repetition | no_coherence | 0 | respond | fundamentada | approved | None | None |
| unsupported_claim | top1 | 0 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| transcription_correction | top1 | 2 | finish | fundamentada | approved | None | None |
| model_unavailable | presentation | 2 | re_ask | fundamentada | approved | None | reserve_or_safe_output |
| unsupported_claim | baseline | 1 | respond | None | None | None | None |
| unsupported_claim | top1 | 1 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| resource_unavailable | baseline | 1 | respond | None | None | None | None |
| conflicting_sources | no_coherence | 2 | clarify | conflictiva | approved | None | None |
| resource_unavailable | no_grounding | 0 | acknowledge_missing_info | None | None | None | missing_evidence_after_closed_worker |
| clear_evidence | no_coherence | 2 | respond | fundamentada | approved | None | None |
| unsupported_claim | baseline | 2 | respond | None | None | None | None |
| no_evidence | full | 1 | acknowledge_missing_info | None | None | None | None |
| agent_timeout | presentation | 1 | clarify | None | None | None | safe_fallback |
| index_unavailable | presentation | 2 | acknowledge_missing_info | None | None | None | missing_evidence_or_safe_output |
| conversational_contradiction | presentation | 1 | finish | fundamentada | block | None | None |
| repetition | presentation | 1 | clarify | fundamentada | reformulate | None | None |
| academic_grade | top1 | 1 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| transcription_failure | baseline | 2 | respond | None | None | None | text_after_observed_stt_failure |
| academic_grade | no_grounding | 2 | finish | fundamentada | approved | None | None |
| state_conflict | full | 0 | respond | fundamentada | approved | None | None |
| repetition | baseline | 0 | respond | None | None | None | None |
| conflicting_sources | no_coherence | 1 | clarify | conflictiva | approved | None | None |
| transcription_failure | no_grounding | 1 | respond | fundamentada | approved | None | text_after_observed_stt_failure |
| academic_grade | baseline | 2 | block | None | None | None | None |
| unsupported_claim | full | 1 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| transcription_failure | presentation | 1 | re_ask | fundamentada | approved | None | text_after_observed_stt_failure |
| clear_evidence | baseline | 2 | respond | None | None | None | None |
| clear_evidence | top1 | 2 | respond | fundamentada | approved | None | None |
| transcription_failure | presentation | 2 | re_ask | fundamentada | approved | None | text_after_observed_stt_failure |
| agent_timeout | full | 1 | clarify | None | None | None | safe_fallback |
| index_unavailable | baseline | 0 | respond | None | None | None | None |
| resource_unavailable | full | 2 | acknowledge_missing_info | None | None | None | missing_evidence_after_closed_worker |
| conversational_contradiction | no_coherence | 2 | respond | fundamentada | approved | None | None |
| clear_evidence | baseline | 1 | respond | None | None | None | None |
| deletion | no_grounding | 0 | respond | fundamentada | approved | None | None |
| clear_evidence | no_grounding | 2 | respond | fundamentada | approved | None | None |
| no_evidence | no_grounding | 0 | acknowledge_missing_info | None | None | None | None |
| no_evidence | baseline | 2 | respond | None | None | None | None |
| index_unavailable | top1 | 0 | acknowledge_missing_info | None | None | None | missing_evidence_or_safe_output |
| conflicting_sources | no_grounding | 0 | respond | fundamentada | approved | None | None |
| transcription_correction | baseline | 1 | respond | fundamentada | approved | None | None |
| resource_unavailable | top1 | 1 | acknowledge_missing_info | None | None | None | missing_evidence_after_closed_worker |
| no_evidence | presentation | 2 | acknowledge_missing_info | None | None | None | None |
| deletion | presentation | 0 | re_ask | fundamentada | approved | None | None |
| turn_limit | full | 1 | clarify | fundamentada | reformulate | None | None |
| index_unavailable | no_grounding | 0 | acknowledge_missing_info | None | None | None | missing_evidence_or_safe_output |
| turn_limit | full | 2 | clarify | fundamentada | reformulate | None | None |
| transcription_failure | top1 | 2 | respond | fundamentada | approved | None | text_after_observed_stt_failure |
| transcription_failure | full | 1 | respond | fundamentada | approved | None | text_after_observed_stt_failure |
| state_conflict | no_coherence | 0 | respond | fundamentada | approved | None | None |
| agent_timeout | no_grounding | 2 | clarify | None | None | None | safe_fallback |
| conflicting_sources | top1 | 1 | clarify | conflictiva | approved | None | None |
| repetition | no_grounding | 2 | clarify | fundamentada | reformulate | None | None |
| transcription_failure | no_grounding | 0 | respond | fundamentada | approved | None | text_after_observed_stt_failure |
| academic_grade | baseline | 1 | block | None | None | None | None |
| conversational_contradiction | top1 | 1 | finish | fundamentada | block | None | None |
| agent_timeout | full | 0 | clarify | None | None | None | safe_fallback |
| repetition | presentation | 2 | clarify | fundamentada | reformulate | None | None |
| model_unavailable | presentation | 1 | re_ask | fundamentada | approved | None | reserve_or_safe_output |
| out_of_scope | baseline | 0 | respond | None | None | None | None |
| transcription_failure | no_coherence | 1 | respond | fundamentada | approved | None | text_after_observed_stt_failure |
| turn_limit | no_grounding | 2 | clarify | fundamentada | reformulate | None | None |
| turn_limit | presentation | 1 | clarify | fundamentada | reformulate | None | None |
| state_conflict | no_grounding | 0 | respond | fundamentada | approved | None | None |
| state_conflict | no_coherence | 1 | respond | fundamentada | approved | None | None |
| model_unavailable | presentation | 0 | re_ask | fundamentada | approved | None | reserve_or_safe_output |
| resource_unavailable | baseline | 0 | respond | None | None | None | None |
| resource_unavailable | top1 | 0 | acknowledge_missing_info | None | None | None | missing_evidence_after_closed_worker |
| repetition | presentation | 0 | clarify | fundamentada | reformulate | None | None |
| resource_unavailable | no_coherence | 0 | acknowledge_missing_info | None | None | None | missing_evidence_after_closed_worker |
| no_evidence | no_coherence | 2 | acknowledge_missing_info | None | None | None | None |
| transcription_failure | baseline | 1 | respond | None | None | None | text_after_observed_stt_failure |
| model_unavailable | top1 | 2 | respond | fundamentada | approved | None | reserve_or_safe_output |
| transcription_correction | baseline | 2 | respond | fundamentada | approved | None | None |
| transcription_correction | full | 0 | finish | fundamentada | approved | None | None |
| unsupported_claim | full | 0 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| conflicting_sources | presentation | 2 | clarify | conflictiva | approved | None | None |
| index_unavailable | presentation | 0 | acknowledge_missing_info | None | None | None | missing_evidence_or_safe_output |
| conflicting_sources | no_grounding | 2 | respond | fundamentada | approved | None | None |
| out_of_scope | no_grounding | 0 | acknowledge_missing_info | None | None | None | None |
| model_unavailable | baseline | 2 | respond | None | None | None | None |
| agent_timeout | top1 | 1 | clarify | None | None | None | safe_fallback |
| conflicting_sources | no_grounding | 1 | respond | fundamentada | approved | None | None |
| out_of_scope | presentation | 0 | acknowledge_missing_info | None | None | None | None |
| conversational_contradiction | presentation | 0 | finish | fundamentada | block | None | None |
| transcription_correction | no_grounding | 0 | finish | fundamentada | approved | None | None |
| deletion | presentation | 1 | re_ask | fundamentada | approved | None | None |
| model_unavailable | baseline | 1 | respond | None | None | None | None |
| repetition | top1 | 0 | clarify | fundamentada | reformulate | None | None |
| resource_unavailable | full | 1 | acknowledge_missing_info | None | None | None | missing_evidence_after_closed_worker |
| transcription_failure | no_coherence | 0 | respond | fundamentada | approved | None | text_after_observed_stt_failure |
| conversational_contradiction | full | 2 | finish | fundamentada | block | None | None |
| out_of_scope | top1 | 0 | acknowledge_missing_info | None | None | None | None |
| conversational_contradiction | no_coherence | 1 | respond | fundamentada | approved | None | None |
| turn_limit | no_grounding | 1 | clarify | fundamentada | reformulate | None | None |
| deletion | no_coherence | 1 | respond | fundamentada | approved | None | None |
| model_unavailable | full | 0 | respond | fundamentada | approved | None | reserve_or_safe_output |
| resource_unavailable | no_grounding | 1 | acknowledge_missing_info | None | None | None | missing_evidence_after_closed_worker |
| academic_grade | presentation | 2 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| resource_unavailable | presentation | 2 | acknowledge_missing_info | None | None | None | missing_evidence_after_closed_worker |
| state_conflict | top1 | 1 | respond | fundamentada | approved | None | None |
| no_evidence | no_grounding | 1 | acknowledge_missing_info | None | None | None | None |
| deletion | full | 0 | respond | fundamentada | approved | None | None |
| deletion | baseline | 2 | respond | None | None | None | None |
| turn_limit | baseline | 1 | respond | None | None | None | None |
| resource_unavailable | no_grounding | 2 | acknowledge_missing_info | None | None | None | missing_evidence_after_closed_worker |
| deletion | no_coherence | 0 | respond | fundamentada | approved | None | None |
| clear_evidence | no_coherence | 0 | respond | fundamentada | approved | None | None |
| repetition | top1 | 1 | clarify | fundamentada | reformulate | None | None |
| unsupported_claim | full | 2 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| no_evidence | top1 | 1 | acknowledge_missing_info | None | None | None | None |
| no_evidence | top1 | 2 | acknowledge_missing_info | None | None | None | None |
| resource_unavailable | top1 | 2 | acknowledge_missing_info | None | None | None | missing_evidence_after_closed_worker |
| transcription_correction | presentation | 0 | finish | fundamentada | approved | None | None |
| deletion | presentation | 2 | re_ask | fundamentada | approved | None | None |
| conflicting_sources | full | 0 | clarify | conflictiva | approved | None | None |
| index_unavailable | baseline | 2 | respond | None | None | None | None |
| conflicting_sources | presentation | 1 | clarify | conflictiva | approved | None | None |
| no_evidence | no_coherence | 1 | acknowledge_missing_info | None | None | None | None |
| agent_timeout | presentation | 0 | clarify | None | None | None | safe_fallback |
| conflicting_sources | no_coherence | 0 | clarify | conflictiva | approved | None | None |
| conflicting_sources | top1 | 0 | clarify | conflictiva | approved | None | None |
| conflicting_sources | baseline | 2 | respond | None | None | None | None |
| agent_timeout | no_grounding | 0 | clarify | None | None | None | safe_fallback |
| turn_limit | no_coherence | 2 | respond | fundamentada | approved | None | None |
| model_unavailable | top1 | 0 | respond | fundamentada | approved | None | reserve_or_safe_output |
| state_conflict | presentation | 0 | re_ask | fundamentada | approved | None | None |
| conflicting_sources | baseline | 1 | respond | None | None | None | None |
| out_of_scope | presentation | 1 | acknowledge_missing_info | None | None | None | None |
| repetition | no_grounding | 1 | clarify | fundamentada | reformulate | None | None |
| conflicting_sources | baseline | 0 | respond | None | None | None | None |
| index_unavailable | no_coherence | 0 | acknowledge_missing_info | None | None | None | missing_evidence_or_safe_output |

## Efectos pareados de ablación

- no_grounding: 51 pares, 9 veredictos distintos y 9 salidas distintas. Coste medio del verificador completo: 0.5679527789147364 ms.
- no_coherence: 51 pares, 9 veredictos distintos y 9 salidas distintas. Coste medio del verificador completo: 0.03336409691912241 ms.

## Resultados negativos y datos faltantes

0 celdas de agencia con error o criterio de traza incompleto; no se ocultan ni cuentan como trazabilidad completa.
- no_grounding: 15 salidas con texto sin citas entregadas; 6 fallos de agente. Ver cada escenario; no inferir calidad académica.
- baseline: 48 salidas con texto sin citas entregadas; 0 fallos de agente. Ver cada escenario; no inferir calidad académica.
- presentation: 21 salidas con texto sin citas entregadas; 6 fallos de agente. Ver cada escenario; no inferir calidad académica.
- full: 21 salidas con texto sin citas entregadas; 6 fallos de agente. Ver cada escenario; no inferir calidad académica.
- top1: 21 salidas con texto sin citas entregadas; 6 fallos de agente. Ver cada escenario; no inferir calidad académica.
- no_coherence: 21 salidas con texto sin citas entregadas; 6 fallos de agente. Ver cada escenario; no inferir calidad académica.

No se midieron GPU, tokens reales, utilidad/facilidad/calidad percibida, preparación de explicaciones ni tiempo docente. CPU/RSS son del proceso completo, no atribución causal por agente.

## Comparabilidad

- Deterministic extractive model and lexical fixture ranking; no LLM/Chroma performance inference.
- Baseline uses direct model plus lexical input evidence and pure constitutional rules, lacks T090 coordination/state changes; no comparable agency trace denominator.
- Faults without matching baseline component are not applied there; injection_applied records this.
- Presentation changes purpose; correction uses defense command even in baseline cell, a shared auxiliary probe, excluded from inference of direct-model speed.
- Latency includes DB setup/cleanup; component latency excludes it. RSS is sampled, not peak. Cold/warm costs may differ.
- Synthetic proposals injected equally across conditions; this probes verifiers, not model error prevalence.

## Inferencias y propuesta de evolución

Las diferencias de veredicto al retirar un verificador identifican su efecto en estas fixtures; no estiman frecuencia real de errores. Los controles finales pueden seguir bloqueando o reconstruyendo la salida, de modo que aprobar grounding no implica entregar el candidato.
Conservar controles constitucionales/privacidad y verificadores mientras se amplía el conjunto etiquetado. Medir Ollama/índice real en hardware declarado, separar calentamiento de ejecución y recoger piloto humano consentido antes de decidir optimizaciones. Simplificar componentes solo con beneficio medido; no activar cambios automáticamente.
