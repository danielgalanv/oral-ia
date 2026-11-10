# Validación arquitectónica ORAL-IA

## Observaciones y límites

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

Celdas: 68; repeticiones por celda: 2.

## Métricas observadas

| Condición | n | Errores | Bloqueos | Timeouts | Recuperaciones | Traza completa | Latencia media ms |
|---|---|---|---|---|---|---|---|
| full | 34 | 0 | 4 | 2 | 10 | 34/34 | 102.979 |
| baseline | 34 | 0 | 2 | 0 | 2 | 0/0 | 79.516 |

JSON incluye n/media/min/max/desviación de cada métrica y latencia por agente. Desviación ausente con n<2; GPU/tokens y opiniones faltantes con motivo.

## Por escenario y configuración

| Escenario | Condición | Repetición | Decisión | Grounding | Coherencia | Error | Recuperación |
|---|---|---|---|---|---|---|---|
| agent_timeout | full | 0 | clarify | None | None | None | safe_fallback |
| agent_timeout | full | 1 | clarify | None | None | None | safe_fallback |
| academic_grade | full | 0 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| turn_limit | full | 0 | clarify | fundamentada | reformulate | None | None |
| out_of_scope | full | 0 | acknowledge_missing_info | None | None | None | None |
| turn_limit | baseline | 1 | respond | None | None | None | None |
| conversational_contradiction | baseline | 1 | respond | None | None | None | None |
| resource_unavailable | baseline | 1 | respond | None | None | None | None |
| model_unavailable | baseline | 0 | respond | None | None | None | None |
| model_unavailable | baseline | 1 | respond | None | None | None | None |
| unsupported_claim | full | 0 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| transcription_correction | full | 0 | finish | fundamentada | approved | None | None |
| resource_unavailable | baseline | 0 | respond | None | None | None | None |
| transcription_failure | baseline | 0 | respond | None | None | None | text_after_observed_stt_failure |
| index_unavailable | baseline | 0 | respond | None | None | None | None |
| repetition | baseline | 1 | respond | None | None | None | None |
| state_conflict | full | 0 | respond | fundamentada | approved | None | None |
| conflicting_sources | full | 1 | clarify | conflictiva | approved | None | None |
| conversational_contradiction | full | 1 | finish | fundamentada | block | None | None |
| academic_grade | baseline | 1 | block | None | None | None | None |
| index_unavailable | full | 0 | acknowledge_missing_info | None | None | None | missing_evidence_or_safe_output |
| state_conflict | baseline | 0 | respond | None | None | None | None |
| conversational_contradiction | full | 0 | finish | fundamentada | block | None | None |
| out_of_scope | baseline | 1 | respond | None | None | None | None |
| turn_limit | full | 1 | clarify | fundamentada | reformulate | None | None |
| index_unavailable | baseline | 1 | respond | None | None | None | None |
| transcription_correction | baseline | 1 | respond | fundamentada | approved | None | None |
| unsupported_claim | baseline | 1 | respond | None | None | None | None |
| turn_limit | baseline | 0 | respond | None | None | None | None |
| deletion | baseline | 1 | respond | None | None | None | None |
| conflicting_sources | baseline | 0 | respond | None | None | None | None |
| no_evidence | baseline | 1 | respond | None | None | None | None |
| transcription_failure | full | 0 | respond | fundamentada | approved | None | text_after_observed_stt_failure |
| index_unavailable | full | 1 | acknowledge_missing_info | None | None | None | missing_evidence_or_safe_output |
| conversational_contradiction | baseline | 0 | respond | None | None | None | None |
| clear_evidence | baseline | 0 | respond | None | None | None | None |
| model_unavailable | full | 0 | respond | fundamentada | approved | None | reserve_or_safe_output |
| transcription_failure | baseline | 1 | respond | None | None | None | text_after_observed_stt_failure |
| academic_grade | full | 1 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| agent_timeout | baseline | 1 | respond | None | None | None | None |
| deletion | baseline | 0 | respond | None | None | None | None |
| state_conflict | baseline | 1 | respond | None | None | None | None |
| out_of_scope | full | 1 | acknowledge_missing_info | None | None | None | None |
| repetition | baseline | 0 | respond | None | None | None | None |
| resource_unavailable | full | 1 | acknowledge_missing_info | None | None | None | missing_evidence_after_closed_worker |
| model_unavailable | full | 1 | respond | fundamentada | approved | None | reserve_or_safe_output |
| conflicting_sources | baseline | 1 | respond | None | None | None | None |
| transcription_correction | baseline | 0 | respond | fundamentada | approved | None | None |
| transcription_correction | full | 1 | finish | fundamentada | approved | None | None |
| repetition | full | 0 | clarify | fundamentada | reformulate | None | None |
| transcription_failure | full | 1 | respond | fundamentada | approved | None | text_after_observed_stt_failure |
| clear_evidence | full | 0 | respond | fundamentada | approved | None | None |
| no_evidence | baseline | 0 | respond | None | None | None | None |
| deletion | full | 0 | respond | fundamentada | approved | None | None |
| no_evidence | full | 1 | acknowledge_missing_info | None | None | None | None |
| conflicting_sources | full | 0 | clarify | conflictiva | approved | None | None |
| clear_evidence | baseline | 1 | respond | None | None | None | None |
| state_conflict | full | 1 | respond | fundamentada | approved | None | None |
| deletion | full | 1 | respond | fundamentada | approved | None | None |
| unsupported_claim | full | 1 | acknowledge_missing_info | no_fundamentada | approved | None | None |
| out_of_scope | baseline | 0 | respond | None | None | None | None |
| repetition | full | 1 | clarify | fundamentada | reformulate | None | None |
| unsupported_claim | baseline | 0 | respond | None | None | None | None |
| academic_grade | baseline | 0 | block | None | None | None | None |
| resource_unavailable | full | 0 | acknowledge_missing_info | None | None | None | missing_evidence_after_closed_worker |
| clear_evidence | full | 1 | respond | fundamentada | approved | None | None |
| no_evidence | full | 0 | acknowledge_missing_info | None | None | None | None |
| agent_timeout | baseline | 0 | respond | None | None | None | None |

## Efectos pareados de ablación

- no_grounding: 0 pares, 0 veredictos distintos y 0 salidas distintas. Coste medio del verificador completo: None ms.
- no_coherence: 0 pares, 0 veredictos distintos y 0 salidas distintas. Coste medio del verificador completo: None ms.

## Resultados negativos y datos faltantes

0 celdas de agencia con error o criterio de traza incompleto; no se ocultan ni cuentan como trazabilidad completa.
- full: 14 salidas con texto sin citas entregadas; 4 fallos de agente. Ver cada escenario; no inferir calidad académica.
- baseline: 32 salidas con texto sin citas entregadas; 0 fallos de agente. Ver cada escenario; no inferir calidad académica.

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
