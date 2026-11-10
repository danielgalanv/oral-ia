# Resumen de la noche (06-11-2026)

## Revisores sobre el conjunto etiquetado (mayoría de semillas)

`recall_exact` = error inyectado marcado en su unidad; `recall_any_unit` = marcado en cualquier unidad; `false_critique` = correcto con aviso.

| configuración | detecta (unidad) | detecta (alguna) | falsas críticas | avisos en respuestas desconocidas | fallos técnicos | acuerdo entre semillas | s/caso | semillas |
|---|---|---|---|---|---|---|---|---|
| mistral24b-nothink-schema (mayoría de 18 semillas) | 0.733 | 0.733 | 0.167 | 0.0 | 0 | 0.849 | 5.2 | 18 |
| q25-14b-nothink-schema (mayoría de 18 semillas) | 0.4 | 0.4 | 0.083 | 0.0 | 0 | 0.755 | 3.6 | 18 |
| q3-8b-nothink-schema (mayoría de 3 semillas) | 0.333 | 0.333 | 0.292 | 0.071 | 0 | 0.849 | 3.2 | 3 |
| q3-8b-think-free (mayoría de 3 semillas) | 0.467 | 0.533 | 0.25 | 0.0 | 0 | 0.717 | 5.9 | 3 |
| q3-8b-think-g1 (mayoría de 3 semillas) | 0.2 | 0.2 | 0.0 | 0.0 | 0 | 0.868 | 9.6 | 3 |
| q3-8b-think-schema (mayoría de 3 semillas) | 0.467 | 0.467 | 0.375 | 0.071 | 0 | 0.66 | 6.1 | 3 |
| v2-mistral24b-nothink-schema (mayoría de 18 semillas) | 0.667 | 0.667 |  | 0.014 | 0 | 0.907 | 7.3 | 18 |
| v2-q25-14b-nothink-schema (mayoría de 18 semillas) | 0.333 | 0.333 |  | 0.0 | 0 | 0.828 | 3.9 | 18 |
| v2-q3-8b-nothink-schema (mayoría de 3 semillas) | 0.333 | 0.333 |  | 0.023 | 0 | 0.938 | 4.7 | 3 |
| v2-q3-8b-think-schema (mayoría de 3 semillas) | 0.417 | 0.417 |  | 0.047 | 0 | 0.833 | 5.7 | 3 |
| [v1] mayoría entre configuraciones | 0.4 | 0.4 | 0.083 | 0.0 | 0 |  |  |  |
| [v1] unión de configuraciones (máx. sensibilidad) | 0.8 | 0.8 | 0.5 | 0.143 | 0 |  |  |  |
| [v2] mayoría entre configuraciones | 0.333 | 0.333 |  | 0.0 | 0 |  |  |  |
| [v2] unión de configuraciones (máx. sensibilidad) | 0.75 | 0.75 |  | 0.084 | 0 |  |  |  |

## Latencia de turno completo con llama.cpp (14B genera, 8B revisa)

- repetición 1: generación 3.8 s, revisión 3.3 s, turno 7.1 s (máx. 8.6 s)
- repetición 2: generación 3.8 s, revisión 4.0 s, turno 7.9 s (máx. 10.9 s)
- repetición 3: generación 3.8 s, revisión 3.6 s, turno 7.4 s (máx. 10.2 s)

## Réplica de la tubería completa (215 preguntas sintéticas)

- página de origen entre las 5 recuperadas (bge-m3 + reranker): 0.949
- estados de la revisión: {'no_issues_found': 199, 'insufficient_evidence': 4, 'issues_found': 12}
- avisos al alumno por tipo: {'wrong_concept': 11, 'contradiction': 1}
- generación media 6.0 s (4 en paralelo), revisión media 5.5 s

## Recuperación (215 preguntas sintéticas; acierto de la página de origen)

| sistema | R@1 | R@5 | R@10 | MRR |
|---|---|---|---|---|
| léxico actual [modern] | 0.149 | 0.4 | 0.521 | 0.275 |
| denso minilm (actual) [modern] | 0.414 | 0.712 | 0.805 | 0.555 |
| denso mpnet-base (en caché) [modern] | 0.493 | 0.772 | 0.847 | 0.619 |
| denso BAAI/bge-m3 [modern] | 0.637 | 0.93 | 0.972 | 0.76 |
| denso Qwen/Qwen3-Embedding-0.6B [modern] | 0.647 | 0.912 | 0.953 | 0.766 |
| RRF actual (léxico+minilm) [modern] | 0.335 | 0.67 | 0.819 | 0.497 |
| léxico actual [ctx] | 0.381 | 0.716 | 0.814 | 0.515 |
| denso minilm (actual) [ctx] | 0.381 | 0.647 | 0.749 | 0.501 |
| denso mpnet-base (en caché) [ctx] | 0.502 | 0.73 | 0.823 | 0.617 |
| denso BAAI/bge-m3 [ctx] | 0.647 | 0.907 | 0.967 | 0.762 |
| denso Qwen/Qwen3-Embedding-0.6B [ctx] | 0.637 | 0.907 | 0.949 | 0.758 |
| RRF actual (léxico+minilm) [ctx] | 0.488 | 0.767 | 0.874 | 0.612 |

Con reranker [modern]:
- denso minilm (actual): R@1 0.414 → 0.707, R@5 0.712 → 0.907, MRR 0.555 → 0.795 (0.22 s/consulta)
- denso mpnet-base (en caché): R@1 0.493 → 0.702, R@5 0.772 → 0.902, MRR 0.619 → 0.789 (0.16 s/consulta)
- denso BAAI/bge-m3: R@1 0.637 → 0.74, R@5 0.93 → 0.949, MRR 0.76 → 0.835 (0.16 s/consulta)
- denso Qwen/Qwen3-Embedding-0.6B: R@1 0.647 → 0.721, R@5 0.912 → 0.958, MRR 0.766 → 0.827 (0.14 s/consulta)

Con reranker [ctx]:
- denso minilm (actual): R@1 0.381 → 0.688, R@5 0.647 → 0.847, MRR 0.501 → 0.761 (0.18 s/consulta)
- denso mpnet-base (en caché): R@1 0.502 → 0.688, R@5 0.73 → 0.902, MRR 0.617 → 0.781 (0.15 s/consulta)
- denso BAAI/bge-m3: R@1 0.647 → 0.73, R@5 0.907 → 0.963, MRR 0.762 → 0.831 (0.16 s/consulta)
- denso Qwen/Qwen3-Embedding-0.6B: R@1 0.637 → 0.716, R@5 0.907 → 0.963, MRR 0.758 → 0.822 (0.14 s/consulta)

## Incidencias de la cola

- 2026-11-06 02:26:23 END generate-answers exit=1 in 26 s
- 2026-11-06 02:26:24 END build-eval-v2 exit=1 in 0 s
- 2026-11-06 02:26:49 skip rerank-modern: reranked-modern.json exists
- 2026-11-06 02:32:23 skip eval-q25-14b-nothink-schema: results-q25-14b-nothink-schema.json exists
- 2026-11-06 02:32:50 skip rerank-modern: reranked-modern.json exists
- 2026-11-06 02:32:57 skip generate-answers: answers.json exists
- 2026-11-06 02:32:57 skip build-eval-v2: cases.json exists

## Hallazgos adicionales

- Seguimientos (100 preguntas): solo el seguimiento R@5 0,67; pregunta anterior + seguimiento (actual) 0,94; reescritura por el modelo 0,87. No hace falta reescribir.
- Recuperación contextual (contexto añadido a cada página): sin mejora (bge-m3 R@5 0,907 frente a 0,930; con reranker 0,963 frente a 0,949; diferencias dentro del ruido).
- Latencia de turno completo con llama.cpp (14B genera, 8B revisa): media 7,5 s, máx. 10,9 s (12 turnos).
- Revisor: Mistral-24B sin razonamiento y con esquema detecta más (0,73 en v1 con 18 semillas; 0,67 en v2) pero con 0,17 de falsas críticas; Qwen2.5-14B es el más preciso (0,08 de falsas críticas, 0,40 de detección). Con el modo aviso (no rechaza), la sensibilidad de Mistral compensa su falsa alarma; decisión pendiente del docente.
- Muestras pequeñas (15 casos con error en v1): leer las diferencias con cautela.
