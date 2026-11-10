# Necesidad y proporcionalidad de los requisitos de ORALIA

27 de octubre de 2026. Anexo de decisión, no auditoría de cumplimiento ni modificación del producto. Reutiliza fuentes y evidencias congeladas de las auditorías anteriores; no interfiere con la implementación CPU en curso. No se inspecciona su progreso ni se presume que los defectos históricos sigan presentes tras sus correcciones.

**Hemos sobredimensionado la demostración de mecanismos y el proceso de validación respecto a la experiencia de estudio demostrada. No sobran la privacidad, los permisos, la fidelidad o la continuidad; sobran prescripciones y duplicaciones que se han tratado como si fueran esas necesidades.** Lo que falta para el uso no es otra capa de contratos: es una conversación generativa útil, una forma de autorizarla sin confundir permisos con verdad, cobertura documental suficiente y una operación local comprensible.

## Objetivos que conviene separar

| Objetivo | Necesidad real | Papel actual |
|---|---|---|
| Alumno y docente | Entender, aclarar, aplicar y practicar con materiales autorizados; preparar una actividad sin trabajo desproporcionado | Es el objetivo de producto vigente: tutor autónomo por chat, generado desde RAG. |
| Demostrador local | Arranque seguro y experiencia reproducible que muestre honestamente sus límites | Medio útil para presentar y operar; no debe convertirse en un segundo producto ni sustituir al tutor. |
| Investigación de arquitectura | Medir si agentes y verificadores aportan control, calidad y reutilización respecto a alternativas | Objetivo original legítimo, pero distinto de que un alumno pueda estudiar. No presupone superioridad multiagente ni exige nueva comparación sintética en cada cambio. |
| Seguridad y privacidad | Permisos fuera del LLM, fuentes autorizadas, consentimiento, aislamiento, cancelación y borrado conforme a lo prometido | Condiciones de uso que se conservan. El mecanismo puede simplificarse si mantiene garantías y pasa revisión. |
| Futuro | Voz, defensa más amplia y evolución de capacidades | Voz pospuesta, no eliminada. Robótica, perfiles longitudinales, web y autodesarrollo no son necesidades del chat actual. |

El conflicto principal está entre autonomía conversacional y una autorización diseñada para composición literal. Otro conflicto es el coste de verificar y registrar frente a la latencia, cobertura y mantenibilidad. Resolverlos requiere decidir contratos y criterios, no negar el objetivo humano ni introducir una revisión humana por turno como supuesto cumplimiento.

## Qué conservar y qué proponer cambiar

Conservar explicación pertinente, adaptación ante incomprensión, ficción coherente con premisas, fuentes internas exactas, referencias visibles legibles y límites honestos. Conservar también acceso, consentimiento, retirada de fuentes, estado de lo mostrado, idempotencia y cierre seguro. Esas necesidades derivan directamente del uso o de la seguridad, aunque su implementación concreta pueda mejorar.

Proponer simplificar el número prescrito de agentes/composiciones y los campos sin consumidor observable; fusionar la evidencia de regresión y los gates que comprueban lo mismo; sustituir snapshots repetidos por un manifiesto y objetos inmutables compartidos; usar paradas distintas para publicación conversacional y diagnóstico de casos independientes. Aplazar más repertorio extractivo, paneles secundarios, exportación masiva, comparación arquitectónica avanzada y voz. Preservar lo ya construido no obliga a seguir ampliándolo.

Proponer revisar los mecanismos de clasificación de alcance y segmentación: el permiso debe decidirse antes de generar, pero eso no exige necesariamente otro LLM antes de toda búsqueda autorizada. Una unidad documental completa no obliga a entregar bloques arbitrariamente grandes ni a prohibir fragmentación semántica trazable. Cambiar estos mecanismos no elimina las necesidades de alcance o de contexto.

**No se propone retirar el verificador ni el gate generativo.** Se propone precisar qué evidencia empírica permite avanzar y cómo se autoriza el contenido exacto. No se ha recuperado una necesidad humana de garantía lógica universal de toda frase libre; tampoco hay permiso para reducir las condiciones vigentes. La propuesta material necesita decisión explícita.

La [matriz de familias](familias-y-recomendaciones.md) cita IDs y origen para cada acción. El [mapa completo](requirements-necessity-map.json) conecta los 418 identificadores: 90 tienen una recomendación explícita por ID o grupo citado; 328 tienen adscripción provisional y dicen «no evaluado individualmente». No son 418 aprobaciones de necesidad ni un inventario perfecto de todos los escenarios sin ID. El [índice](family-id-index.md) permite revisar qué quedó dentro de cada familia.

## Qué falta y qué bloquea una vía práctica

Faltan criterios de «listo» ligados al episodio de estudio, tiempo y esfuerzo tolerables, flujo docente de preparación/cobertura, recuperación de errores sin bucles y prueba de utilidad/transferencia. Faltan una frontera de autorización generativa aceptada y evidencia de revisión semántica suficiente. Los modelos han mostrado errores concretos con fuentes presentes; no se demuestra incapacidad universal ni que una tarjeta mayor los resuelva. El corpus limitado y las páginas en cuarentena dejan huecos; las fuentes no cubiertas requieren expresar un límite, no excluir temas del temario.

La VRAM es finita, pero la configuración y latencia necesarias para una experiencia aceptable siguen sin estar determinadas. Las anotaciones y la revisión docente son un coste real: un sistema que obliga a atomizar todo el curso o revisar cada turno cambia la propuesta de valor. Los [bloqueos](bloqueos-practicos.md) separan límites físicos, fallos medidos, defectos corregibles y desconocidos, con mitigaciones y costes.

## Alcance recomendado

El mínimo viable conserva el objetivo: una actividad docente local por chat, sobre fuentes autorizadas preparadas, capaz de responder, reformular, construir un ejemplo y seguir una aplicación o cambio de foco, con referencias, límites, cierre y privacidad. No significa cubrir solo preguntas prefabricadas ni aprobar todo el curso desde tres PDF. Debe declarar su cobertura documental y no afirmar suficiencia donde falta material.

El alcance posterior añade mejor recuperación de tablas/diagramas relevantes, práctica y preparación de exposiciones más variadas, autoría más cómoda y evaluación humana de utilidad. La voz sigue para su fase posterior. No implementar ahora nuevas arquitecturas de agentes, formalización simbólica completa, GraphRAG, fine-tuning, una biblioteca de respuestas académicas ni un producto de revisión humana por turno como salida al bloqueo.

Las únicas decisiones materiales propuestas están en el [registro de decisiones](decisiones-para-el-usuario.md): contrato y criterio de publicación, separación de entregables de investigación, objetivos medibles de servicio y coste docente admisible. No se vuelve a preguntar temario, voz, referencias, ficción o disponibilidad GPU. Ninguna recomendación cambia requisitos, constitución o gates por sí sola.

La investigación primaria de educación, RAG y seguridad ya recopilada es suficiente para esta revisión de necesidad; [se reutiliza explícitamente](../2026-10-27-foundations-review/investigacion-final.md). No se repiten búsquedas ni se añade tecnología por estar disponible.
