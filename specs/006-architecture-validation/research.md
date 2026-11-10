# Research — 006

Decisión: compositor real con puertos scoped en CLI. Razón: medir integración existente
sin bypass de producción. Pipeline paralelo y opciones API descartados. Inspeccionados
run_study_turn, GenerationPort, agentes y fixtures existentes; no importar tests.

Decisión: corpus incorporado/base temporal/modelo determinista. Razón: reproducible sin
red/datos reales. Ranking lexical declarado; no medir LLM/Chroma mediante proxy oculto.

Decisión: hashes ordenados de código e inputs, igualdad estructural. Razón: no hay Git,
tiempos/UUID varían. JSON/Markdown con motivos para ausencias; no inventar opiniones.
Sin nuevas dependencias; todos los desconocidos de diseño resueltos con interfaces locales.
