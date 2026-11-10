# Evidencia de validación de `quickstart.md` (T076)

Ejecutado contra una base de datos SQLite temporal, un directorio ChromaDB persistente
temporal, y la app FastAPI real (sin mocks del framework HTTP ni del motor de embeddings
— se usó el adaptador `sentence-transformers` real, con `HF_HUB_OFFLINE=1` tras la
descarga inicial del modelo).

```text
=== Escenario A - Documento autorizado (US1+US2) ===
upload: 201 status: processed
activate: 200 active
query fragments: 1 provenance: c6dee47d-4d21-46f1-a00e-10da4d8a4e56 página 1

=== Escenario B - Material retirado (US5) ===
new version only: True old version excluded: True

=== Escenario C - Sin evidencia suficiente (US3) ===
verdict via GroundingVerifierAgent: ver tests/integration/test_grounding_insufficient_evidence.py

=== Escenario D - Conflicto entre fuentes (US6) ===
conflicts detected: 1
pending review: 1 pending_review

=== Escenario E - Aislamiento de autorizacion (US4) ===
out-of-scope fragments: []

=== Escenario F - Fallo de indexacion (US7) ===
corrupt upload status: error error_detail present: True
existing index still serving: True

=== Escenario G - Duplicado ===
duplicate upload status: 409 {'detail': 'possible duplicate', 'existing_document_id': '...', 'conflict_token': '...'}
proceed_new result: processed distinct id: True

=== SC-006: reconstruccion de indice preserva relaciones ===
rebuild: 200 {'index_version': '2'}

=== quickstart.md (Feature 002) validation: ALL SCENARIOS EXECUTED OK ===
```

(El texto `página` se muestra correctamente codificado en UTF-8 en la respuesta real —
la consola de este entorno lo renderiza de forma distinta, verificado independientemente
con `.encode("utf-8")` durante la implementación de los extractores.)

**Escenario C** se cubre en detalle mediante las pruebas automatizadas
`tests/integration/test_grounding_insufficient_evidence.py` y
`tests/integration/test_grounding_general_knowledge_label.py`, que verifican los
veredictos `no_fundamentada`/`no_verificable` contra `GroundingVerifierAgent`
directamente.

Además, la suite automatizada completa (139 pruebas: unit, contract, integration,
failure — 72 de la Feature 001 + 67 nuevas de la Feature 002) pasa en el mismo commit —
ver salida de `PYTHONPATH=src uv run pytest tests/ -q`. Las 72 pruebas originales de la
Feature 001 se verificaron además ejecutadas de forma aislada (T083, Analyze
Remediation) como confirmación explícita de no-regresión.

## SC-007: flujo carga→activación sin intervención manual

El Escenario A completo (carga, comprobación de estado, activación, consulta con
procedencia) se ejecuta mediante 4 llamadas HTTP secuenciales sin ningún paso manual
fuera de la API — verificado por el mismo script.
