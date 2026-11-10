# Implementation Plan: Conversación guiada y recuperación del diálogo

**Branch**: sin Git; 010-guided-dialogue | **Date**: 2026-10-18 | **Spec**: [spec.md](spec.md)
**Estado**: implementación parcial; tareas y evidencia actuales en tasks.md y implementation-evidence.md. La planificación siguiente define obligaciones, no acredita aceptación.
**Input**: hallazgos de prueba de autoestudio y defensa, intención original de Features 003/004 y constitución vigente.

## Summary

Primero corregir continuidad y bucles; después proporcionar contenido y acciones explicativas autorizables; finalmente evaluar conversaciones completas y condiciones operativas. No resolver el problema poniendo más palabras clave al demo ni conectando un LLM a una puerta que solo autoriza extractos. La entrega verificable es un perfil de **diálogo guiado controlado**, reutilizable en dos dominios, con composición desde unidades docentes revisadas. La inferencia generativa local se evalúa por separado: si no satisface autorización y calidad, queda explícitamente no habilitada, sin fingir cumplimiento mediante fallback.

El objetivo es ayuda pertinente a una actividad docente, con intervención humana, no demostrar cuántos componentes se ejecutan. Infraestructura aprobada, aceptación conversacional y utilidad educativa humana tendrán estados distintos.

## Technical Context

**Language/Version**: Python 3.12 y TypeScript/React existentes; PowerShell 5.1/7 en el anfitrión.
**Primary Dependencies**: FastAPI, SQLAlchemy, Pydantic, Alembic, sentence-transformers/Chroma, proveedor GenerationPort y adaptadores existentes; no se aprueban nuevas dependencias por este plan.
**Storage**: SQLite actual + estado de diálogo JSON aditivo versionado; tablas teaching_units y turn_request_receipts descritas en data-model.md; corpus sintético en archivos.
**Testing**: pytest contrato/integración/fallos; Playwright real; runner de corpus por propiedades, pruebas con generador real para el perfil anunciado.
**Target Platform**: ordenador local Windows, localhost y sesiones sin Internet; no extrapolar rendimiento a otros equipos.
**Project Type**: aplicación web/API local con agencias dentro del mismo proceso.
**Performance Goals**: presupuestos por perfil visibles; conservar inicialmente límites de agentes existentes. Medir carga inicial y ejecución caliente separadas. Un perfil cuyo p95 supera su presupuesto no se publica: se informa o se aprueba manualmente otra versión del presupuesto, nunca se amplía en silencio.
**Constraints**: T090/T150, no evaluación, solución no revelada según política, consentimiento/purga, una sesión activa, sin downloads implícitas ni sesiones reales en fixtures.
**Scale/Scope**: dos modos, cinco modos internos de autoestudio, dos dominios de contenido, corpus definido en acceptance-matrix.md; sin ampliación de concurrencia.

## Constitution Check

Evaluación previa y posterior al diseño: conforme por diseño; la implementación todavía no está verificada.

| Principio | Aplicación y gate |
|---|---|
| I Finalidad | Solo acciones de apoyo y discrepancias de contenido, sin notas, diagnósticos ni roles de profesor. |
| II Contratos | Interpretación compartida v2 y propuestas tipadas; compatibility v1 y evolución documentada en contracts/. |
| III Estado | Contexto acotado en pizarra, patches versionados y rollback; no historial oculto ni memoria entre sesiones. |
| IV Separación | Intérprete propone intención; política decide; generador propone; verificadores y T090 controlan publicación. |
| V Materiales | Revalidación DB tras referencias y antes de mostrar; conflicto/inyección/revocación y referencias futuras son negativos obligatorios. |
| VI Gobierno | Unidades/actividades/perfiles nuevos requieren versión y publicación docente; no modificar actividades ya usadas. |
| VII Privacidad | Nuevo contenido sujeto a scopes; texto completo/teclado, acceso demo solo dentro del aislamiento ya autorizado. |
| VIII Trazabilidad | Razones operativas y proveedor real, no razonamiento privado ni candidatos rechazados. |
| IX Límites | Máximo una recuperación alternativa por turno; dos fallos de progreso disparan elección explícita; nunca bypass de gate. |
| X Evidencia | Corpus real multi-turno y reservado; separar dobles y providers; datos humanos pendientes. |
| XI Simplicidad | Extender agente existente mediante contrato versionado y políticas puras compartidas; sin nueva sociedad paralela ni microservicios. |

No se modifica la constitución. La tabla no constituye prueba de cumplimiento del producto.

## Decisiones de arquitectura

### A. Interpretación compartida, decisión explícita

Evolucionar StudyIntentInterpreterAgent a contrato v2 con responsabilidad de interpretación conversacional reutilizable por defensa; conservar adaptador de salida v1 para consumidores anteriores. El nombre histórico puede conservarse hasta una migración justificada. Los cinco modos de estudio y el acto conversacional son ejes separados. No duplicar clasificadores en cada compositor ni usar la salida del modelo como autoridad para elegir acciones.

Normalización Unicode/case/acentos solo para clasificación; mantener texto literal para historial. Señales negativas y mezcla de intenciones tienen precedencia definida. Salida incluye candidatos, confidence_kind y estado ambiguous. Pruebas deben incluir frases no empleadas para redactar las reglas; la confianza heurística no es probabilidad calibrada.

### B. Contexto explícito de sesión

Añadir campo opcional JSON dialogue_context a CognitiveState y snapshot, con schema_version=1 y valores vacíos para sesiones previas. Migración Alembic aditiva: no reinterpretar historia ni escribir anclas falsas. Extender StatePatch mediante esquema cerrado y update por base_version; contexto y turno se persisten en la misma transacción exterior.

Guardar referencia a último turno autorizado/pregunta pendiente y objetivo temático; no copiar indefinidamente su texto. Mantener una ventana de hasta 4 referencias relevantes para desambiguación, 8 concepts relevantes derivados de tema/evidencia, 3 hipótesis de intención, 1 referente elegido por acción. Resolver texto desde filas autorizadas; acceso a una referencia no concede permiso de uso. Vaciar/revalidar en cambio de tema, cierre, revocación o pérdida de scope. Defaults versionados de la política dialog-policy/v1, modificables solo por configuración manual.

### C. Política de diálogo y recuperación

Seleccionar acción antes de generar. repeat conserva la pregunta/salida; rephrase preserva objetivo; help da pista graduada permitida; continue avanza un subobjetivo; topic_switch elige temario; ambiguity aclara. La consulta de recuperación usa original_content_query + current_topic + pending_question según la intención, no concatena sin límite el historial ni trata «ahora/no/puedes» como temas.

Un saludo no dispara búsqueda semántica. Una consulta temática amplia usa objetivo/índice de temas y evidencia actual; no exige una cadena exacta. No hay cierre automático por repetir legítimamente una pregunta. Fallos de contenido insuficiente son estados distintos de fallo de autorización o de agente.

Repetición: comparador recibe intención/objetivo y firma de salida, no solo Jaccard. Solo repeat explícito puede repetir texto intencionadamente, siempre con revalidación; ampliar tema debe cambiar subobjetivo/contenido cuando exista. Primer estancamiento cambia estrategia; segundo ofrece botones y opciones textuales cuya elección se procesa realmente. No suprimir globalmente coherencia ni su control de contradicción.

### D. Explicación autorizada sin un permiso circular

Primera entrega: material docente organizado en unidades revisadas (fact, explanation, example, comparison, question, hint) con IDs, fuente/versiones, condiciones y relaciones; contenido declarativo independiente de agentes, no hardcodes del agua. Se reutiliza la gobernanza para crear/editar borrador, validar referencias, revisar y publicar; no cargar datasets editados como instrucciones de modelo.

ProposalPlan contiene template_ref, unidades/fragmentos referenciados, transformaciones de un conjunto cerrado y action/purpose. El renderer reconstruye desde DB/configuración publicada, no desde valores del generador. Solo se admiten composición/selección, extracto canónico y envoltorios/reformulaciones docentes revisados para ese objetivo. Las nuevas categorías/procedencias/plantillas requieren política manual versionada y tests exactos; templates dinámicas creadas a partir del candidato no son autorización.

Los verificadores controlan grounding de todas las afirmaciones, coherencia relevante, no revelación y T090. Una paráfrasis libre de Ollama **no** se convierte en unidad revisada automáticamente. Estudiar un contrato futuro de afirmaciones derivadas en sandbox con evidencia etiquetada y pruebas adversariales. No habilitarlo si depende solo de overlap léxico o aprobación del mismo generador.

### E. Discrepancia factual y no revelación

Comparar la afirmación del participante y las condiciones de la fuente como datos diferentes. Una discrepancia numérica simple requiere misma magnitud, unidad y contexto explícitos. Ante aproximación, unidades distintas, negación ambigua o condiciones ausentes: aclarar, no declarar error. En defensa, preguntar primero por la justificación o condición documentada, sin hacer pasar la fuente por lo dicho por el usuario ni mezclar ebullición y evaporación.

El docente define reveal_policy por actividad. Pistas, reformulación, panel de fuentes y resumen respetan el mismo permiso. En práctica sin solución no basta esconder expected_answer del texto: fragmentos/exemplos visibles tampoco pueden entregarla indirectamente. Si no es posible ayudar sin revelar, explicitar límite y ofrecer otra pregunta.

### F. Perfiles y contenido suficientes

Perfiles: extractive_limited (reserva identificada), guided_controlled (objetivo de entrega), generative_local_candidate (sandbox, no publicado hasta gate adicional). Mostrar perfil configurado/efectivo y cambio por timeout. Evaluar un modelo local ya disponible no prueba aptitud por estar instalado; registrar nombre/digest, parámetros, límites, hardware y resultados. Sin recursos suficientes: estudio no aprobado, no tests falsamente pasados.

Contenido de desarrollo sobre agua: presión/temperatura, ebullición vs evaporación, condensación, congelación y límites; cada unidad revisada con condiciones. Segundo dominio ficticio, p.ej. separación de responsabilidades de un pequeño programa local, con fuentes y objetivos propios. Conservar agua original dos frases y archivo04 como regresiones; crear materiales/sucesoras nuevos sin Reset. Mínimos por dominio: 5 objetivos, 2 ejemplos, 2 contrastes y 3 preguntas con pistas escalonadas; si el docente solo carga texto plano sin unidades, sigue disponible extractivo_limited y su capacidad no se sobredeclara.

### G. Operación y continuidad de interfaz

Preflight de inicio verifica destinatario y disponibilidad sin publicar preguntas ni adquirir lock hasta que todo sea válido; actividad legacy sin política sigue fail closed con mensaje útil. No validar identidad por el código ni ampliar allowed_recipients automáticamente.

Recuperación de sesión: propietario autenticado puede reabrir su sesión desde el estado activo; tras reinicio y pérdida de token no hay recuperación por seudónimo. Docente autorizado puede cerrar sesión abandonada con confirmación, motivo estructural y política de retención existente, mediante T150 y comandos públicos; no SQL, no cierre automático ni Reset.

Petición mutante con client_request_id único por sesión y payload_hash. Reintento idéntico devuelve estado persistido autorizado vigente; reutilizar ID con payload distinto da conflicto. Una respuesta vieja tras cierre no resucita texto ni contexto. Reconciliar resultado desconocido antes de enviar de nuevo; no tratar todos los errores de red como petición fallida.

Pregunta y Tu respuesta siempre visibles si activa; controles de voz solo si disponibles. Fuentes cerca de la respuesta con nombre/versión/ubicación y avisos cuando no hay evidencia. UI en español, teclado, estado ocupado e información de límites. No rediseño visual integral.

## Project Structure

### Documentation (this feature)

spec.md; plan.md; research.md; data-model.md; contracts/dialogue.md; contracts/authorization.md;
acceptance-matrix.md; risk-register.md; quickstart.md; tasks.md; requirement-coverage.md;
checklists/requirements.md; checklists/dialogue-safety.md; action-plan.md.

### Source Code (repository root)

- Existentes: src/oralia/domain/agents/study_intent_interpreter.py, coherence_verifier_agent.py, followup_question_agent.py; domain/cognitive_state/{cognitive_state.py,state_patch.py}; application/orchestration/{self_study_agency_composer.py,defense_agency_composer.py}; infrastructure/generation/{generation_port.py,deterministic_adapter.py,ollama_adapter.py}; infrastructure/db/models.py.
- Nuevos previstos: src/oralia/domain/dialogue/{contracts.py,context.py,policy.py}; application/services/{dialogue_context_service.py,dialogue_retrieval_service.py,teaching_unit_service.py}; domain/materials/teaching_unit.py; infrastructure/db/migrations/versions/t010_dialogue_context.py.
- Gobierno/publicación: activity_governance_service.py, routers/{governance.py,participante.py,self_study.py,oral_defense.py}, services/session_privacy_service.py, session_export_service.py.
- UI: apps/web/src/{api/client.ts,routes/Autoestudio.tsx,routes/DefensaOral.tsx,routes/Gobierno.tsx,components/SessionRecovery.tsx}.
- Pruebas nuevas: tests/{unit,contract,integration,failure}/test_dialogue_*.py; tests/dialogue/{fixtures,runner.py}; tests/e2e/test_guided_dialogue.spec.ts. Rutas propuestas no afirman que ya existen.

**Structure Decision**: extender componentes y puertos existentes; la única nueva responsabilidad cognitiva es el contrato conversacional compartido, implementado mediante evolución del intérprete existente. Servicios puros no son agentes adicionales.

## Secuencia y puertas de entrega

1. **Bloque A — Evidencia y contratos**: fijar regresiones históricas, corpus reservado, capacidades y presupuesto. Sin estas pruebas no se empieza a «mejorar prompts».
2. **Bloque B — Contexto y acciones**: migración, intérprete, recuperación y política anticiclos. Demostrar ambas conversaciones con contenido controlado y límites.
3. **Bloque C — Apoyo docente**: unidades revisadas/gobierno, explicaciones/pistas, discrepancias, no revelación y estudio de generación local. No sustituir calidad por un saludo amable.
4. **Bloque D — Uso autónomo**: preflight, sesión ocupada/recuperación, idempotencia, modalidad y fuentes.
5. **Bloque E — Aceptación y cierre**: corpus reservado, navegador, fallos, privacidad y regresión global; luego analyze/converge y evidencia por perfil.

No implantar todo en un único parche opaco. Cada bloque exige contratos/pruebas y revisión de evidencia antes del siguiente. Orden de archivos y dependencias en tasks.md.

## Gates de cierre y seguimiento futuro

**G0 técnico**: contratos, migraciones, unit/integración/fallos, global, frontend y validación operativa pasan; T090/T150 y privacidad intactos.
**G1 diálogo guiado**: SC-001–SC-008 y corpus completo pasan en guided_controlled con proveedor real (renderer/unidades), sin mocks de interpretación/generación decisivos. Cero casos históricos pendientes. Revisar transcriptos sintéticos de forma humana con rúbrica de sistema.
**G2 generativo**: solo si se pretende publicar ese perfil, contract/claim verification + proveedor local real + tres ejecuciones/caso + revisión independiente; sin modelo o gate fallido = perfil no disponible. G1 no permite afirmar G2.
**G3 utilidad con personas**: seguimiento posterior con consentimiento; no es requisito inventado para marcar la implementación de G1 ni se deduce de ella.

Comparación arquitectónica: además de reproducir las 204 celdas previas sin reescribir su paquete, T053 ejecuta los 24 diálogos nuevos de forma pareada con la agencia y el baseline monolítico existente, usando los mismos materiales, políticas, proveedor y presupuestos. Informar propiedades aprobadas, violaciones, latencia y coste por caso; no atribuir mejoras a multiagencia si cambian contenido o proveedor entre condiciones. Si el baseline necesita un adaptador de contrato v2, documentarlo y probarlo; nunca sustituir el baseline por respuestas favorables. La comparación evalúa sistemas, no estudiantes.

Futuro separado: voz local real tras calidad textual, corpus de más asignaturas, mejora semántica de verificadores, recuperación avanzada y evaluación del coste frente al baseline. Ninguno habilita nube, notas o perfilado.

## Complexity Tracking

No excepción constitucional propuesta. La migración, la composición docente estructurada y la idempotencia se justifican por estado reconstruible, salida autorizable y errores ya observados; se descartan memoria privada del LLM, bypass de autorización y nueva arquitectura distribuida.


## Ampliación solicitada: conversaciones sintéticas de herramientas

FR-033/SC-009 añaden 16 escenarios (8 desarrollo/8 reservados) a los 24 diálogos existentes, según [protocolo](synthetic-tool-conversations.md). T057 diseña casos antes de implementar herramientas; T058 prueba oráculos antes de ampliar runner T059; T060 ejecuta antes del cierre. No se crea un agente con permisos nuevos: API/UI y herramientas actuales con roles vigentes, servicios reales, almacenamiento temporal y fallos inyectados identificados. La aceptación comprueba llamada, argumentos, efecto persistido y respuesta, no solo prosa. G0/G1 incluyen SC-009.
