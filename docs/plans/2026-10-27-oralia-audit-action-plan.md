# ORALIA: plan de ejecución tras las auditorías globales

Fecha: 27 de octubre de 2026. Plan redactado por el chat coordinador después de leer las dos auditorías, contrastar los documentos de origen y reproducir el defecto de identidad de embeddings. No es una aceptación del tutor ni una modificación de sus gates.

## Decisión y objetivo

Continuar el proyecto sin reescribirlo. Primero corregir la base y separar capacidades; después demostrar un episodio de estudio útil. No continuar una escalera de prompts sobre Qwen2.5-7B ni acumular pruebas de infraestructura como sustituto de esa demostración.

El producto sigue siendo un tutor autónomo por chat que genera explicaciones desde RAG docente autorizado. No se sustituye por respuestas académicas predefinidas ni por revisión humana de cada turno. La ficción coherente está permitida; su interpretación y las conclusiones necesitan respaldo o premisas suficientes. Referencias visibles generales y legibles; procedencia interna exacta. Temario principal confirmado, sin bloques extra como temas autónomos. Voz aplazada e Internet desactivado durante sesiones.

### Fuentes del plan

- [Auditoría de fundamentos y requisitos](../audits/2026-10-27-foundations-review/informe.md).
- [Requisitos y autoridad](../audits/2026-10-27-foundations-review/matriz-requisitos-final.md).
- [Hallazgos F01–F21](../audits/2026-10-27-foundations-review/hallazgos-final.md).
- [Backlog auditado B01–B18](../audits/2026-10-27-foundations-review/backlog.md).
- [Arquitectura recomendada](../audits/2026-10-27-foundations-review/arquitectura-recomendada.md).
- [Investigación externa y sus límites](../audits/2026-10-27-foundations-review/investigacion-final.md).
- [Auditoría anterior de ensayos](../audits/2026-10-27-global-viability/informe.md).
- [Comparación local de generadores ya propuesta](../../specs/012-conversational-course-study/evidence/generator-capacity-decision-v1/decision.md).

Las auditorías son globales por áreas y trazan 418 identificadores, pero no certifican manualmente cada requisito ni cada línea del programa. Los defectos reproducidos, riesgos de componente y validaciones ausentes deben conservar esas categorías. No hay evidencia para atribuir los errores pedagógicos al defecto de caché, a NF4 o a la carga GPU.

## Forma de ejecución y límites

1. Una nueva tarea será el único escritor de implementación. Los chats anteriores quedan en consulta. No se crea otro checkout: el proyecto no es Git.
2. Trabajar con SpecKit sobre lo existente. Añadir tareas identificadas y relacionadas con este plan; no regenerar ni compactar spec/plan/tasks, no perder pendientes históricos y no marcar por mera existencia de código.
3. Antes de cambios, guardar un manifiesto de los archivos que se tocarán y localizar los recursos habituales, evidencias protegidas y perfiles anteriores. Los tests usan raíces temporales propias. No reindexar ni migrar bases habituales para probar.
4. Entregar bloques ejecutables con problema, cambio, pruebas y límites. Una propuesta de diseño no es implementación; un fixture no es evaluación real; una investigación publicada no es una solución validada en ORALIA.
5. No commits, Reset, borrado de originales, sobrescritura de evidencia o presupuestos históricos, uso de reserva para ajuste ni intervención en procesos ajenos. Conservar las seis pérdidas históricas como pérdidas, sin otra petición de backup.
6. Los comandos necesarios de CPU están autorizados; usar la revisión de permisos del entorno cuando proceda sin volver a preguntar por cada script. Un rechazo real debe describirse, no eludirse.
7. No descargas, instalaciones globales, nube, apertura de red de producto, participantes humanos ni cambio de alcance por defecto. Si hace falta uno de esos recursos, presentar una opción concreta con coste y motivo.
8. Pruebas proporcionadas: negativas que reproduzcan defectos, contratos, integración y regresión afectada. Suite amplia una vez al consolidar cambios compartidos; no repetirla sin cambios o causas nuevas. Ruff estructural por identidad y multiplicidad, además de Black.

## Orden elegido

La seguridad de publicación sigue cerrada durante todos los bloques de laboratorio. Su diseño puede avanzar sin paralizar las correcciones independientes. La recuperación no es la explicación de un error que aparece con fuentes adecuadas presentes: por eso se separan ambos experimentos.

| Fase | Trabajo principal | Referencias auditadas | Dependencia y coste relativo |
|---|---|---|---|
| 0 | Fijar trazabilidad y base de ejecución | B04, F18, F21 | Inicio; bajo |
| 1 | Identidad, modo local y presupuestos efectivos | B01–B03, F01–F04 | Antes de comparar recursos; bajo/medio |
| 2 | Privacidad, recuperación de sesión y entrega | B05–B07, B09; F11–F16 | CPU; medio, con decisiones separadas |
| 3 | Autorización generativa y aceptación explícita | B08, F05–F06 | Diseño revisable; no activar sin aprobación |
| 4 | Recuperación común, alcance y representación | B10–B13; F07–F10 | Identidad validada; medio |
| 5 | Capacidad de generación y revisión independiente | B14–B15, F17–F19 | Configuración validada y presupuestos congelados |
| 6 | Episodio de estudio y experiencia de producto | B16–B17, F19–F20 | Candidatas defendibles; medio/alto |
| 7 | Transferencia, utilidad y aceptación | B18, F21 y gates históricos | Revisión humana y criterios explícitos |

### Fase 0. Base y trazabilidad

- Relacionar cada trabajo con requisito humano, contrato vigente o hipótesis experimental. Mantener diferencias entre el conceptual robótico, el MVP docente y el objetivo actual de chat. No reintroducir robótica, perfiles longitudinales o voz como trabajo inmediato.
- Comprobar que la versión recibida corresponde a la auditada; registrar cualquier diferencia antes de usar un hallazgo como vigente. El manifiesto no demuestra corrección, pero permite saber qué se prueba.
- Reutilizar recibos para modelo, tokenizer, plantilla, configuración efectiva, fuentes, texto mostrado, terminación y revisión. No añadir otro harness o snapshot gigante si bastan manifiestos y referencias.

**Salida:** tareas enlazadas, recursos protegidos identificados y una reproducción de los defectos prioritarios sin tocar datos habituales. Ninguna afirmación de conformidad global por extracción automática de IDs.

### Fase 1. Corregir identidad y configuración antes de más ensayos

**E1. Embeddings.** Reproducir A→B→A con dobles CPU y concurrencia. Corregir la caché para que la identidad efectiva corresponda a la solicitada, con una política de recursos acotada. No cambiar el encoder por defecto ni cargar varios modelos reales para probar la caché.

**E2. Ejecución local.** La carga de embeddings debe ser local de forma explícita o rechazar una configuración incompatible antes de intentar red. Probar variables ausentes, `0` y `1`, recurso inexistente y ningún acceso remoto, mediante un cargador simulado. No presentar `setdefault` como un bloqueo de red. No modificar variables globales del usuario de forma permanente.

**E3. Índice.** Incorporar fingerprint de encoder/revisión, dimensión, normalización, representación y versión de extracción/chunking. Un índice de igual dimensión y distinto espacio se rechaza. Un índice antiguo sin identidad se informa como no acreditado para la comparación nueva, no como corrupto. Preservar su lectura histórica; no reconstruirlo ni cambiar el puntero habitual automáticamente.

**E4. Presupuestos.** Eliminar la divergencia silenciosa entre solicitado y efectivo. Mantener límites seguros por backend, pero validarlos o negociarlos explícitamente antes del envío. Registrar capacidades, resultado y motivo; conservar compatibilidad de perfiles existentes. Probar 256, 512, 768, 1024 y 2048 tokens mediante transporte falso, sin exigir que todo backend acepte todos los tamaños. La salida `length` no se transforma en respuesta completa.

**Salida:** identidad y carga local demostradas, incompatibilidades de índice rechazadas y frame coherente con el presupuesto aceptado. Rollback documentado; ningún índice o modelo nuevo activado por esta corrección.

### Fase 2. Comprobar las garantías que dábamos por seguras

**S1. Registros técnicos.** Trazar productores y consumidores de `technical_payload`. Introducir esquemas de evento o validación de valores/códigos para las superficies que prometen metadato cerrado; una lista de claves no basta. Probar sentinels anidados, cierre sin conservación, exportación y reconstrucción de trazas. No afirmar una fuga explotable a partir del contraejemplo aislado ni borrar evidencia antigua.

**S2. Caída y concurrencia.** En bases y procesos propios, probar pérdida de token, sesión aún activa, reintento, dos conexiones/procesos, cierre ganador y respuesta tardía. Reutilizar CAS y permisos actuales. Proponer por separado cualquier política nueva de sesión abandonada; no cerrar sesiones del usuario por un timeout inventado.

**S3. Entrega y datos no confiables.** Probar idempotencia, copias defensivas de recibos/catálogos, cancelación y retirada entre revisión, preparación y confirmación. Incluir delimitadores imitados e instrucciones en documentos ficticios. El LLM no puede habilitar herramientas ni modificar autoridad. Escapar texto elimina ambigüedad de formato, no garantiza resistencia semántica a inyección.

**S4. Borrado.** Documentar por superficie qué significa expirar acceso, purgar contenido y eliminar temporales, y qué ocurre con WAL, logs y copias. Probar las promesas actuales en datos sintéticos. No cambiar almacenamiento, activar un VACUUM global ni prometer borrado forense sin modelo de amenaza y decisión humana.

**Salida:** defectos concretos corregidos, riesgos restantes delimitados y pruebas de integración. Si no se reproduce un riesgo de inspección, conservarlo como supuesto, sin fabricar una vulnerabilidad ni añadir complejidad preventiva sin necesidad.

### Fase 3. Resolver la frontera de autorización sin sortearla

Preparar una propuesta de contrato sucesor optativo para texto generado y revisado. Debe identificar el contenido exacto, sesión, actividad, configuración, fuentes vigentes y autoridad de revisión; el permiso se invalida si cambia cualquiera de las condiciones relevantes. El generador no puede emitirse su propio permiso.

Precisar clases de error, apoyo, pertinencia, cobertura y abstención, distinguiendo criterios finitos de ensayo de garantías universales. Mantener las condiciones vigentes mientras no se apruebe su evolución. No usar un nuevo nombre `trusted_text`, `supported` o un hash como certificación de verdad.

Se pueden construir contratos y pruebas en laboratorio con autoridades simuladas claramente etiquetadas. **La integración que cambie T090 o permita publicar necesita revisión humana del resultado concreto.** Preparar negativos de sustitución de texto/sesión/fuentes, cancelación y permisos reutilizados, además de compatibilidad y rollback.

**Salida:** diseño revisable y pruebas de no bypass; producción y participante cerrados. No es necesario esperar esa aprobación para continuar trabajo independiente de laboratorio.

### Fase 4. Recuperación y alcance como capacidades medibles

**R1. Puerto común.** Adaptar las unidades ricas de 012 y el recuperador denso existente de 002 a una frontera comparable. Conservar el léxico bilingüe como baseline. Mismo corpus, IDs, permisos y reglas de retirada; la autoridad no procede de Chroma ni de scores.

**R2. Ranking.** Registrar candidatos antes y después de filtros, aporte total del historial y omisiones. Comparar pregunta, referente explícito e historial acotado, sin reglas por IDs de R04/R05. Medir recall de candidatos, pertinencia adjudicada, contexto entregado y latencia por separado. Una unión híbrida debe normalizar o combinar rankings de forma justificada, no sumar scores incompatibles. Reranking solo cuando sobrevivan los candidatos pertinentes.

Usar primero recursos locales ya disponibles y nuevos índices aislados. Un encoder o reranker nuevo requiere una propuesta de checkpoint/licencia, dependencias, coste y presupuesto antes de descargarlo. No añadir frameworks ni grafos por defecto.

**R3. Alcance.** Ensayar una variante optativa que permita una búsqueda de solo lectura en fuentes autorizadas antes de decidir una pregunta incierta, manteniendo la decisión de alcance antes de generar. Comparar con el flujo actual. Recuperación vacía, alta similitud o aparición de una palabra no prueban inclusión/exclusión. Mantener política docente, partes mixtas y controles operativos fuera de ese error conceptual. No pedir al docente enumerar todos los temas del universo.

**R4. Representación.** Priorizar las 26 páginas en cuarentena por preguntas reales y causa de extracción. Aprovechar extractores/formato autorizado existentes antes de proponer OCR o parser nuevo. Revisar tablas, listas, encabezados y figuras contra el original; no levantar cuarentena solo porque aparezca texto. Un cambio de representación crea versión y procedencia; no duplica silenciosamente PDF/PPTX.

**Salida:** comparación sobre controles nuevos no ajustados al resultado, y decisión de conservar/rechazar cada estrategia. No promover una variante que solo añada contexto sin valor. Extracción incompleta sigue visible como cobertura pendiente, no como fuera del temario.

### Fase 5. Generación y verificación, sin otra escalera de prompts

**G1. Diagnóstico de generador.** Tras E4, consumir la propuesta existente 7B/14B si sus hashes y entradas siguen válidos: mismas condiciones, fuente fija frente a RAG normal, hasta 16 respuestas y dos calentamientos, 768 tokens por respuesta y un máximo global de 20 minutos. Presupuesto propio; no usar restos de bancos anteriores. Si hace falta una modificación técnica prospectiva, documentarla antes, conservando la propuesta previa. No introducir Mistral como fallback automático.

La evidencia fija aísla interpretación; no se anuncia como recuperación de producto. La comparación pequeña no declara un ranking universal. Si ambas candidatas fallan con contexto adecuado, entregar la limitación y opciones, no otro prompt. Si solo falla RAG, intervenir en recuperación/contexto. Truncamientos limitan la inferencia y se conservan.

**G2. Evaluación separada.** Estudiar una señal especializada distinta de los jueces fallidos, aprovechando la investigación de RefChecker, NLI u otros evaluadores publicados sin darlos por validados. Antes de construir: candidato concreto, soporte de español, licencia, dependencias, recursos y criterio de abandono. No descargar ni entrenar automáticamente.

Medir apoyo de afirmaciones centrales y conclusiones, omisiones del extractor, negación/modalidad, pertinencia y cobertura; incluir ficción válida y rechazo falso. Separar calibración y transferencia. Cero errores en un banco finito no es garantía externa; rechazar todo tampoco permite continuar. Si no hay candidato viable con los recursos autorizados, registrar esa limitación y la decisión concreta que falta, sin construir otro contrato vacío.

**G3. Tutoría.** Reutilizar la política pedagógica como hipótesis, no como perfil validado. Explicación directa cuando se pide, otra estrategia ante dificultad, ejemplos coherentes y práctica opcional. No obligar a un examen o una plantilla en cada turno. Sin perfiles longitudinales ni diagnósticos de capacidad del alumno.

**Salida:** decisión sobre candidatas de generación y revisión por separado, con errores, cobertura y costes observados. Ningún resultado habilita publicación por sí solo.

### Fases 6 y 7. Producto útil, transferencia y aceptación

Preparar y observar un episodio completo: duda → incomprensión → ejemplo → aplicación o matiz/cambio, desde el texto realmente mostrado. Seguir el [experimento auditado](../audits/2026-10-27-foundations-review/experimento-minimo.md). No sustituir salidas del modelo por textos escritos a mano ni incorporar al historial un bruto rechazado.

Separar dos modos de evaluación: diagnóstico offline de casos independientes —que puede conservar más fallos para analizarlos— y entrega conversacional —que respeta los bloqueos vigentes—. Un stop de una conversación no impide observar otros controles independientes si estaba previsto y presupuestado; no sirve para inventar continuidad.

La ruta final debe permitir preparar actividad, conocer cobertura, preguntar, seguir la fuente y cerrar con conservación comprensible, por texto y teclado. Reutilizar la aplicación; no construir otro panel técnico. Mostrar claramente si es preview, extractivo o generativo disponible.

La aceptación necesita revisión docente y revisores identificados donde lo exigen los gates, transferencia y repeticiones vigentes. La utilidad humana se evalúa después con consentimiento; no se infiere de satisfacción, longitud o conteo de turnos. La comparación arquitectónica pareada es un experimento distinto, no otra ejecución de las 204 celdas como prueba de aprendizaje.

**Salida:** conversación completa revisada y criterios de aceptación documentados; si falta un requisito, permanece abierto. G2, SC001 y publicación solo cambian mediante su procedimiento y aprobación correspondiente.

## GPU, recursos y autorizaciones

La última instrucción humana declara GPU disponible para las pruebas necesarias, incluidas intensivas si aportan evidencia. No es permiso para una secuencia indefinida de candidatos. Antes de cada bloque, anunciar modelo, propósito, presupuesto y duración estimada; comprobar carga/VRAM y registrar durante/después. Un residente no prueba competencia; memoria de KV/allocator no prueba actividad ajena. Si aparecen uso concurrente o condiciones inciertas, detener o aplazar solo el trabajo propio y no comparar sus tiempos. No pedir de nuevo permisos para cada comando local; una nueva indisponibilidad declarada por el usuario prevalece.

No comenzar con GPU mientras haya defectos de configuración que invaliden el experimento. Una tarea nueva no debe abrir otro worker a la vez que otro chat. Preservar los 49 hashes protegidos y los presupuestos anteriores sin reinterpretar sus resultados. Cualquier ensayo nuevo tiene manifiesto y contabilidad independientes.

## Qué se implementa ya y qué queda sujeto a decisión

**Ya autorizado:** corregir defectos reproducidos, completar pruebas y trazabilidad, comprobar privacidad y estado con datos propios, recuperar por puertos existentes y desarrollar variantes reversibles de laboratorio dentro de la política actual. Comenzar por fases 0 y 1 y continuar las partes independientes de fase 2, sin detenerse solo para entregar otro plan.

**Revisión humana antes de activar:** contrato sucesor de autorización y criterios materiales de publicación, política de sesiones abandonadas o borrado forense, nuevos recursos/descargas/servicios, apertura web/LAN, cambios de alcance y participación de personas. Preparar resultados concretos para la revisión; no preguntar por abstracciones ni bloquear trabajo independiente esperando esas decisiones.

**No priorizar:** más agentes o microservicios, GraphRAG, formalización completa del curso, fine-tuning sin evaluación suficiente, nuevas colecciones de prompts, voz, memoria longitudinal y más paquetes sintéticos presentados como utilidad docente.

## Entregas y control de avance

Cada bloque entrega: hallazgo/requisito → cambio → evidencia → limitación → siguiente decisión. Actualizar SpecKit conservando IDs y pendientes. Mantener un registro legible de defectos corregidos, supuestos refutados, limitaciones medidas y validaciones pendientes. Solo llamar corregido a lo que supere su criterio.

No prometer fechas ni porcentajes de producto terminado. El primer hito útil es una base de identidad/configuración verificable; el siguiente, una conversación de estudio completa y conceptualmente fiel. Este plan no asegura el resultado de investigación: establece cómo evitar repetir fallos y tomar decisiones con evidencia.
