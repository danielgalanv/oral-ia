# Revisión de necesidad y proporcionalidad

27 de octubre de 2026. Este informe propone qué obligaciones conservar o cambiar; no certifica cumplimiento ni modifica requisitos, tareas, constitución o gates. Trabaja con las fuentes congeladas de las auditorías previas, sin interferir con la implementación CPU en curso. No se presume que sus correcciones estén pendientes o terminadas.

**El proyecto se ha sobredimensionado en demostración arquitectónica, restricciones de mecanismo y repetición de evidencias. No sobran la seguridad, la privacidad ni la fidelidad docente. Lo que falta es demostrar una experiencia de estudio útil, con cobertura real, recuperación ante fallos y coste asumible.** No hay que sustituir el tutor autónomo por respuestas prefabricadas o revisión humana de cada turno para aparentar cumplimiento.

## Objetivos y conflictos

El objetivo vigente de producto es ayudar al alumno a entender, aclarar y aplicar conceptos por chat, con respuestas generadas desde RAG docente. El docente necesita preparar y actualizar una actividad sin convertirse en autor de cada respuesta. El demostrador local sirve para operar y presentar esa experiencia, pero no es otro producto. La investigación de agentes sigue siendo un objetivo legítimo original, distinto de que una persona pueda estudiar. Permisos, consentimiento, fuentes vigentes y control de recursos son condiciones comunes. Voz está pospuesta; robótica, perfiles longitudinales y web no son necesidades del chat actual.

Hay dos conflictos sin resolver por completo: la autorización literal frente a la generación libre y el coste de verificar/documentar frente a cobertura, latencia y mantenimiento. Más contratos no eliminan esos conflictos. La propuesta es conservar las garantías y cambiar los mecanismos que no aportan valor demostrado, mediante decisiones prospectivas y versionadas.

## Valoración de todos los identificadores

Se leyó el texto completo recuperado de cada identificador y su contexto de las doce especificaciones. El registro final contiene disposición, motivo, familia, fuente y línea para los 418 IDs. No queda ninguno con mera asignación automática por feature. Se detectó que `012/SC001` es una referencia no normalizada a `012/SC-001`: el inventario contiene 417 definiciones formales y ese alias documental, no 418 obligaciones independientes.

| Disposición propuesta | IDs |
|---|---:|
| Conservar por seguridad |133|
| Conservar para el uso actual |98|
| Sustituir el mecanismo, conservando la necesidad |94|
| Aplazar nuevas ampliaciones, manteniendo compatibilidad |59|
| Retirar del criterio de listo del producto actual |17|
| Decisión pendiente por conflicto o aceptación insuficientemente definida |10|
| Fusionar obligaciones equivalentes o alias |7|

Estos conteos no miden ahorro, criticidad o porcentaje de finalización: un requisito puede contener varias obligaciones y las cláusulas de seguridad se repiten entre features. Aplazar no significa desproteger una ruta existente, sustituir no significa quitar el control y retirar del criterio del chat no significa eliminar la investigación del proyecto.

Consultar [disposición individual](individual-review-final.md), [JSON](individual-review-final.json), [CSV](individual-review-final.csv) y [resumen de cobertura](individual-review-summary.json). El [índice final de familias](final-family-index.md) conecta todos los IDs con las recomendaciones. Los registros iniciales con 328 pendientes se conservan como borradores y quedan superados por esta revisión completa.

## Dónde se ha sobredimensionado

- Cantidades de agentes, composiciones y campos cognitivos sin un consumidor claro se han usado como prueba de avance del producto. Son instrumentos de investigación, no evidencia de que el alumno entienda mejor.
- Los perfiles extractivos y sus ejemplos publicados resolvían problemas históricos concretos. Ampliar ese repertorio no satisface el objetivo actual de generar desde documentos.
- Snapshots completos, nuevos paquetes de 204 celdas y suites repetidas pueden duplicar coste sin añadir evidencia. Se pueden consolidar con manifiestos, referencias inmutables y pruebas según impacto, conservando primeros fallos e integridad.
- Parar publicación y continuidad ante un fallo es correcto; abandonar todos los controles diagnósticos autónomos no siempre lo es. Separar sus protocolos evita perder información sin inventar conversación.
- Preclasificar antes de toda búsqueda, prohibir cualquier división semántica de unidades o exigir la misma repetición de ensayos a una configuración determinista son decisiones de mecanismo que necesitan justificación.
- Un gate de permisos no prueba verdad y una revisión semántica favorable no otorga permiso. Duplicar nombres de gates no sustituye definir sus responsabilidades y evidencia.

La [matriz razonada por familias](familias-y-recomendaciones.md) explica las acciones con IDs y origen. Los cambios incompatibles con contratos o constitución siguen requiriendo su revisión; esta auditoría no los ejecuta.

## Qué falta de verdad para usarlo

Un flujo docente de preparación y cobertura, conversación natural que cambie de estrategia ante incomprensión, ejemplos con premisas suficientes, continuación tras error sin bucles y una definición honesta de listo. Faltan objetivos acordados de tiempo y carga de revisión, mantenimiento de fuentes/modelos y evaluación de utilidad o transferencia separada de satisfacción y conteos de tests.

El alcance permitido tiene nueve bloques principales. El catálogo académico actual tiene tres PDF de Requisitos, Procedimiento y Testing; la presentación delimita el temario. Eso no acredita cobertura útil de los nueve bloques. Las otras diapositivas docentes ya autorizadas pueden incorporarse registrando versión, selección y activación según política; no hace falta reautorizar la asignatura. No se pueden convertir los huecos de incorporación o cuarentena en temas excluidos.

Para probar utilidad se puede escoger un episodio acotado con fuentes suficientes, sin cambiar el alcance del producto. Para cubrir los nueve bloques hace falta un inventario por bloque y estimar extracción, QA y revisión; no se conoce aún su coste total. Declarar temporalmente qué está respaldado es honesto; reducir permanentemente el producto a tres PDF requeriría decisión humana.

## Límites prácticos y alcance proporcionado

Hay fallos empíricos de generación y revisión con fuentes presentes; la configuración local suficiente sigue sin demostrarse. La memoria física es finita, pero no está probado que la VRAM sea el bloqueo causal ni que una compra solucione la semántica. Corpus, diagramas, anotación y revisión docente también tienen costes. Los defectos de identidad/configuración son corregibles y no deben confundirse con limitaciones inherentes. Véase el [registro de bloqueos y mitigaciones](bloqueos-practicos.md).

El mínimo viable recomendado conserva autonomía, generación RAG, fuentes, alcance, privacidad y cierre seguro: una actividad local con dudas, reformulación, ejemplo y aplicación o cambio de foco completos, evaluados con documentos suficientes y límites visibles. El alcance deseable posterior mejora cobertura de los nueve bloques, tablas/diagramas relevantes, práctica, exposición y autoría; voz queda para su fase. No implementar ahora más agentes por cantidad, GraphRAG, formalización completa del curso, fine-tuning, nuevas integraciones o una biblioteca de respuestas académicas.

Siguen sin vía práctica demostrada la publicación generativa con revisión suficiente y cobertura útil a un coste local/ docente tolerable. Las alternativas son resolver esas incertidumbres o mantener el perfil sin publicación; cambiar a respuestas prefabricadas, lenguaje formal o revisión de cada turno es otra decisión de producto, no la conclusión automática de esta revisión.

Las [decisiones materiales preparadas](decisiones-para-el-usuario.md) son separar los hitos de producto/investigación, aprobar contrato y aceptación generativa, fijar servicio tolerable y limitar trabajo docente. No se pregunta de nuevo temario, voz, referencias, ficción o disponibilidad GPU. La [investigación primaria previa](../2026-10-27-foundations-review/investigacion-final.md) basta como soporte; no se añaden tecnologías porque existan.
