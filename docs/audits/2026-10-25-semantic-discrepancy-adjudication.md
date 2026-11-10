# Contraste de tres discrepancias semánticas

25 de octubre de 2026. Revisión técnica del asistente auditor, independiente del modelo generador y del modelo verificador. No es revisión docente ni una segunda pasada ciega: el auditor había leído las objeciones antes de contrastarlas con las fuentes. No concede G2, SC001 ni permiso de publicación.

Se leyeron directamente los JSON originales de `specs/012-conversational-course-study/evidence/chat-comparison-v2-context-echo-capture-first/` y se extrajeron las páginas originales mediante `load_catalog()`, sin inferencia ni uso de GPU. Se revisaron además los protocolos y los scripts de calibración/revisión del verificador. No se alteraron paquetes, código ni tareas.

## Fuentes observadas

- `procedure:10`: calidad de la especificación, incluida completitud respecto de lo que se conoce que debe hacer el sistema.
- `procedure:11`: no ambigüedad significa una sola interpretación; comprobabilidad exige poder definir pruebas con coste y tiempo razonables; también distingue realizabilidad y trazabilidad.
- `procedure:12`: validar contrasta el sistema descrito con necesidades y obtiene aprobación; enumera reuniones y prototipado de interfaz como tareas.
- `requirements:73`: comprobaciones de validez respecto a necesidades, consistencia, completitud, realismo y verificabilidad. No atribuye automáticamente esas propiedades a cualquier frase de requisito.

## Resultado por discrepancia

### B, turno `example`

La respuesta inventa el registro de un perfil con nombre, apellido y correo y afirma que cumple criterios como «correcto, completo, verificable». Las páginas definen criterios, pero no establecen el alcance, restricciones, tecnología, dependencias o pruebas de ese sistema ficticio. Los supuestos mostrados son tesis generales sobre validación, no condiciones suficientes del escenario.

**Adjudicación técnica:** la conclusión de que cumple el conjunto de criterios es `sin_apoyo` bajo los supuestos aportados. Eso no prueba que el requisito sea necesariamente incorrecto o imposible de verificar; prueba que el texto no ha justificado la garantía que afirma. El ejemplo puede ilustrar una funcionalidad no necesitada, pero no acredita por ello su calidad completa.

### C, turno `example`

La respuesta presenta «registrar productos con sus características» como requisito claro/bien redactado, sin precisar qué características, restricciones o resultado constituyen el registro. Añade que la falta de ajuste a necesidades se detectaría en validación «no durante la revisión de calidad».

**Adjudicación técnica:** no está justificada la claridad específica del requisito. La exclusión categórica de la revisión de calidad tampoco se deduce del material: distinguir finalidades no demuestra que sus hallazgos sean mutuamente excluyentes. La revisión no debe convertir esa falta de prueba en una afirmación universal de que ninguna frase similar puede ser clara dentro de un glosario que aquí no se ha proporcionado.

### C, turno `error`

La respuesta corrige acertadamente que la aprobación del cliente no garantiza ausencia de ambigüedad. Después afirma que una ambigüedad «no se detectaría durante la validación con el cliente, pero sí durante la revisión de la calidad».

**Adjudicación técnica:** el primer punto es compatible con las fuentes; el segundo absoluto es `sin_apoyo`. `procedure:12` contempla reuniones y prototipos, sin excluir que al utilizarlos aparezcan interpretaciones distintas. Tampoco hay garantía de detección automática en una revisión de calidad. La conclusión válida es que una aprobación no sustituye la comprobación de no ambigüedad, no que cada actividad tenga descubrimientos exclusivos o infalibles.

## Qué demuestra sobre el verificador

El resultado `accept` de esos tres turnos es un falso permiso respecto de la regla congelada que exigía apoyo para las afirmaciones centrales. Una respuesta puede contener una explicación principal correcta y, a la vez, una conclusión importante sin apoyo.

Los scripts ensayados solicitan una única decisión `accept/reject` por respuesta completa. No devuelven descomposición de afirmaciones, pasajes, premisas ni abstención. Se identifican como diagnósticos y nunca como autorización, lo cual es correcto. Su éxito en siete controles breves no demuestra que detecten un defecto localizado dentro de una respuesta larga y mayoritariamente plausible. Los tres casos reales impiden utilizar ese resultado como verificación semántica suficiente.

## Continuación acotada

Conservar los originales y estas discrepancias; no recalcular 16/16 como éxito. Preparar, sin GPU, controles nuevos de respuesta compuesta: explicación principal correcta con una sola conclusión sin apoyo, su versión corregida y una inferencia válida condicionada. Identificar las copias modificadas como controles derivados, nunca como transcriptos reales. Congelar las decisiones esperadas y el mecanismo antes de cualquier nuevo ensayo.

Una posible evaluación por afirmaciones debe señalar la proposición exacta, las premisas/pasaje y `supported/unsupported/unknown`, con agregación que no oculte un error central por la calidad del resto. Es una hipótesis a comprobar, no un verificador ya disponible ni una orden de acumular más prompts. Si no distingue esos controles y no transfiere a respuestas nuevas, registrar el límite y no integrarlo.

La revisión de estas tres discrepancias no cubre exhaustivamente los 16 turnos ni sustituye las dos pasadas requeridas o la revisión docente. La GPU no interviene en este contraste de fuentes; los fallos de plazos anteriores siguen clasificados por separado.
