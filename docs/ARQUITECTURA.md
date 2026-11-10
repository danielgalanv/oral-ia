# Mapa del código y los flujos

## Piloto actual de chat

`scripts/study-chat.ps1` prepara interfaz/índice/catálogo en una carpeta propia y arranca `oralia.documentary`. La entrada del alumno es `/estudio`.

1. `documentary/study_preparation.py`: recibo v2 e integridad de preparación y copias de índice.
2. `documentary/retrieval.py`, `comparison_coverage.py`, `chat_context.py`: recuperación local CPU, selección y contexto. La recuperación no demuestra respaldo semántico.
3. `documentary/study_lab.py`, `study_lab_api.py`, `reviewed_study.py`, `real_study_provider.py`: sesión, salida realmente mostrada, llamada a modelos y orquestación del piloto.
4. `documentary/study_web_flow.py`, `web_evidence.py`, `web_passages.py`, `web_review.py`: ampliación externa restringida, procedencia y revisión. `config/requirements-study-policy*.json` controla actividad/permiso; habilitar web no garantiza validez de contenido.
5. `course_dialogue/structured_request.py`, `model_prompt_profiles.py`, `thinking_review_request.py`, `cached_transformers.py`, `owned_worker.py`: contratos, prompts por checkpoint y trabajadores locales. Aunque estén en course_dialogue, algunos son compartidos por el piloto; no borrar la carpeta como si toda fuera descartable.
6. `apps/web/src`: interfaz React. La preparación construye una copia aislada; no sirve todos los directorios privados del workspace.

El piloto usa generación `study-dialogue/v4`, revisión estable `web-review/v8` y control `web-control/v5`. Su guardia terminológica estrecha sigue siendo una mitigación específica, no un verificador universal.

## Revisión conceptual experimental

`course_dialogue/concept_ledger.py`, `concept_labels.py` y `concept_review_loop.py` implementan el registro por unidades y nombres. No se promueven al piloto: repiten contexto, necesitan recuperaciones de formato/cobertura y producen falsas críticas.

`prepared_concepts.py` persiste unidades originales por documento/version/hash; `documentary/concepts.py` prepara el paquete. `review(..., prepared=...)` evita planificar de nuevo el catálogo, pero no valida automáticamente sus candidatos ni resuelve la latencia del revisor. Los 40 candidatos detectados incluyen también guías/escenarios; no llamarlos glosario aprobado.

## Núcleo y demostradores previos

`domain/`: entidades, políticas y contratos de dominio. `application/`: agentes y servicios. `infrastructure/`: SQL, generación, embeddings y otros adaptadores. `interfaces/`: API y dependencias. `apps/api/main.py` arranca el API histórico; `demo/`, `course_study/` y los lanzadores `demo.ps1`, `course-study.ps1`, `course-dialogue.ps1` conservan demostradores distintos. Sus pruebas no acreditan automáticamente el chat generativo actual.

Las migraciones están en `src/oralia/infrastructure/db/migrations` (configuración en `alembic.ini`). Verificar la ruta configurada antes de una operación; no reinicializar bases locales existentes.

## Dónde está la verdad de cada cosa

- Estado y siguiente paso: `docs/CONTINUAR.md`.
- Requisitos/plan/tareas/contratos: `specs/012-conversational-course-study/` y constitución `.specify/memory/constitution.md`.
- Política de actividad ejecutada: configuración versionada y recibo del arranque, no un texto histórico aislado.
- Resultados medidos: recibos y paquetes de `docs/audits`; quedan inmutables aunque una conclusión posterior cambie.
- Originales, extracción, disponibilidad/cuarentena y derechos: manifiesto del paquete docente, no el estado `processed` por sí solo.

La separación entre código, datos y evidencias se mantiene en sus rutas para no invalidar importaciones y hashes. Las guías de entrada son actuales; las evidencias antiguas no se reescriben.
