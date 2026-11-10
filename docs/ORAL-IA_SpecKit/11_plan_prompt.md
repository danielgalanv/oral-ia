# Texto para `/speckit-plan`

Crea el plan técnico exclusivamente para la feature actual, después de inspeccionar el repositorio, la constitución, la especificación y las features ya implementadas. No reestructures componentes aprobados salvo que exista una incompatibilidad demostrable y documentada.

## Objetivo arquitectónico

Implementar un monolito modular local que haga visibles y medibles los contratos de agentes, la composición de agencias, el estado cognitivo, las memorias, las verificaciones, la trazabilidad y la degradación. No usar microservicios ni un framework de agentes que oculte estas propiedades en el MVP.

## Pila propuesta

- Python 3.12 administrado con `uv`.
- FastAPI para API y servidor local.
- Pydantic v2 para contratos, mensajes, estado, configuraciones y resultados de agentes.
- SQLAlchemy 2 y Alembic para persistencia relacional.
- SQLite en modo WAL para el MVP, con repositorios y adaptadores que permitan sustituirla en el futuro.
- Frontend React, TypeScript y Vite para las áreas de participante y profesor; mantener el cliente simple y sin lógica cognitiva.
- Comunicación HTTP local y, cuando proceda, eventos internos en proceso. No introducir RabbitMQ en el MVP.
- Adaptadores de inferencia para Ollama y servidores compatibles con OpenAI como vLLM; ninguna dependencia del dominio debe importar SDKs concretos.
- Embeddings locales mediante un adaptador configurable.
- ChromaDB persistente o un índice equivalente detrás de una interfaz `VectorStore`; justificar la elección tras revisar compatibilidad y necesidades de borrado/versionado.
- Extracción documental con adaptadores para PDF, DOCX, PPTX, TXT y Markdown.
- Faster-Whisper para STT local y Piper o equivalente local para TTS, únicamente en la feature de voz.
- `structlog` o registro JSON estructurado, `psutil` y soporte opcional de métricas GPU.
- Pytest, pytest-asyncio cuando sea necesario, pruebas de contrato y Playwright para los flujos web críticos.
- Docker Compose opcional para reproducibilidad, manteniendo también ejecución directa local.

Si el repositorio ya ha adoptado tecnologías equivalentes, conservarlas cuando satisfagan la constitución y justificar cualquier cambio.

## Organización recomendada

```text
apps/
  api/
  web/
src/oralia/
  domain/
    agents/
    agencies/
    messages/
    cognitive_state/
    memory/
    policies/
    sessions/
    materials/
    validation/
  application/
    commands/
    queries/
    orchestration/
    services/
  infrastructure/
    db/
    llm/
    embeddings/
    vector_store/
    documents/
    speech/
    telemetry/
  interfaces/
    api/
    web/
tests/
  unit/
  contract/
  integration/
  e2e/
  failure/
  benchmarks/
```

Ajusta esta estructura al repositorio real, pero conserva la separación dominio/aplicación/infraestructura/interfaces.

## Contratos principales

El plan debe definir esquemas versionados para:

- `AgentDescriptor` y `AgentContract`;
- `AgentRequest`, `AgentResult`, `AgentError` y `CancellationToken`;
- `InternalMessage` y sus tipos;
- `AgencyDefinition` y `ExecutionStep`;
- `SessionConfiguration` y sus versiones;
- `CognitiveState`, `StatePatch` y `StateVersion`;
- evidencias y fuentes recuperadas;
- `VerificationResult`;
- `DialogueAction`;
- transcripción original, segmentos dudosos y correcciones;
- eventos de trazabilidad y métricas;
- consentimiento, retención y exportación.

Los agentes deben implementarse mediante una interfaz asíncrona común con timeout, cancelación, validación de entrada/salida y contexto mínimo. No deben recibir acceso indiscriminado a toda la base de datos o al estado.

## Orquestación

Usar un orquestador explícito y comprobable. Las agencias deben definirse de forma declarativa o mediante código sencillo versionado. Debe distinguir pasos secuenciales, paralelismo limitado, condiciones, verificadores obligatorios, bloqueos, fallback y terminación.

El estado se actualiza mediante parches validados y control de versión. Un agente no modifica directamente objetos persistidos. Registrar la decisión estructurada del selector, no cadenas de razonamiento privadas.

## Persistencia

Separar:

- configuraciones y versiones;
- sesiones y turnos;
- snapshots o eventos del estado;
- materiales, documentos, fragmentos e índice;
- trazabilidad y métricas;
- consentimientos y políticas;
- transcripciones originales y corregidas;
- resultados experimentales.

Definir migraciones, claves, borrado, retención y estrategia para conservar referencias históricas a versiones retiradas sin volverlas recuperables en sesiones nuevas.

## Seguridad y privacidad

- Vincular a `127.0.0.1` por defecto.
- Validar tipos, tamaño y contenido de archivos.
- No ejecutar contenido de documentos.
- Proteger rutas docentes mediante credencial local y sesión segura.
- No almacenar audio ordinario.
- Evitar secretos en repositorio y registros.
- Implementar purga verificable.
- Mantener separación entre códigos e identidad real.
- Tratar el texto de documentos y participantes como datos no confiables; impedir que cambien políticas o instrucciones del sistema.

## RAG

Cuando la feature lo requiera, detallar ingestión, extracción, chunking reproducible, metadatos, embeddings, filtros de autorización, recuperación, versionado, citas, detección de conflictos, reconstrucción de índice y evaluación con conjunto etiquetado.

El plan debe incluir defensa frente a prompt injection documental: las instrucciones encontradas en materiales se tratan como contenido, no como órdenes para agentes.

## Voz

Cuando la feature lo requiera, diseñar captura temporal, STT local, confianza, segmentos dudosos, corrección versionada, descarte de audio, TTS de contenido aprobado y fallback completo a texto.

## Pruebas

Para cada historia de usuario, identificar pruebas independientes. Incluir:

- validación de esquemas y contratos;
- permisos y aislamiento de agentes;
- cambios y conflictos de estado;
- timeout, cancelación y fallback;
- bloqueo constitucional;
- filtrado de materiales;
- fuentes insuficientes y conflictivas;
- prompt injection en documentos o entradas;
- continuidad conversacional;
- ausencia de notas y evaluación;
- degradación de voz;
- consentimiento, exportación, eliminación y retención;
- reconstrucción de sesiones;
- comparación con baseline cuando corresponda.

No usar exclusivamente mocks del LLM. Mantener pruebas deterministas de componentes y un conjunto pequeño de pruebas de integración con un modelo local configurable, marcadas para poder omitirse en CI sin GPU.

## Observabilidad y criterios medibles

Definir eventos y métricas antes de implementar. Cada turno debe asociar correlación de sesión, agente, step y configuración. Medir latencia, errores, recursos, fuentes, verificaciones, bloqueos y cambios de estado.

El plan debe describir cómo demostrar los criterios de éxito de la feature, qué datos de prueba se necesitan y qué evidencia quedará en el repositorio.

## Fases del plan

1. Investigación breve y resolución de incógnitas técnicas reales.
2. Modelo de dominio y contratos.
3. Persistencia y migraciones.
4. Servicios de aplicación y orquestación.
5. Adaptadores de infraestructura.
6. API e interfaz.
7. Pruebas unitarias, de contrato, integración, fallo y E2E.
8. Datos de ejemplo y escenario demostrable.
9. Documentación y evaluación de conformidad constitucional.

No implementes funcionalidades de features posteriores, salvo interfaces o stubs mínimos necesarios para evitar acoplamiento.
