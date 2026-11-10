# Relectura proporcionada de respuestas existentes

28-10-2026. Addendum del coordinador a las evaluaciones históricas. Se aplica la política de answer-evaluation-calibration-audit.md. Solo lectura y documentación, sin GPU ni cambios de producto/tareas/gates. No sobrescribe textos, veredictos o recibos originales.

## Alcance y método

Leídos íntegros: initial.json, iteration-002/version-001 a003, las diez salidas de comparison-003 y structured-prompts/exposed-new-result.json: 15 artefactos de respuesta. structured-prompts/old es duplicado textual de T2-L y no se cuenta otra observación. Son tres preguntas, no quince casos independientes. Recovery-001 quedó fuera de la nueva adjudicación por ser una salida truncada; no se convierte su defecto de terminación en falsedad semántica.

Se aplican las obligaciones de las preguntas y los contextos ya conservados: trazabilidad y límites (NASA142/Procedimiento10/11), meta frente a criterio verificable (Requisitos20), aclaración de alcance sin prefijar implementación (NASA64/Requisitos5 y contexto T2). La relectura considera el ejemplo completo, distingue finalidad de garantía acreditada y admite ficción coherente. No se han cambiado las fuentes para justificar una aceptación.

Autor: mismo coordinador que emitió juicios previos, informado por la objeción docente. No ciego, independiente, revisión docente completa ni tasa de exactitud. La clasificación actual es juicio contextual documentado; no genera autoridad de publicación.

## Adjudicación por artefacto

|Artefacto|Corrección/adecuación académica actual|Observación y cambio respecto del juicio anterior|
|---|---|---|
|original initial|Aceptable|Explica relaciones, cambio y límite del análisis. Mayor bidireccionalidad/cobertura sería enriquecimiento. Se retira la obligación de ampliar hasta cubrir la excepción NASA y todos los límites. El párrafo indirecto se lee con «automáticamente» y análisis adicional.|
|iteration-002/001|Aceptable con redacción mejorable|«Evaluar independientemente» puede significar revisar calidad por separado del trazado, no imponer un revisor independiente universal. La lectura obligatoria anterior no era inequívoca. No exigir excepción NASA ausente. Lista de fuentes final incompleta: defecto de presentación separado.|
|iteration-002/002|Aceptable en contenido básico; presentación a corregir|No se demuestra nuevo error académico central; las notas repetidas y [fragment_id] literal dificultan la entrega. No etiquetar por eso incorrecta toda la explicación. No usar esta versión como mejor salida.|
|iteration-002/003|Aceptable con precisión de atribución mejorable|La calidad individual debe revisarse; atribuir esa frase al pasaje NASA es impreciso porque su objeto es la traza. Corregir referencia/redacción sin declarar fallo central de toda la respuesta. Independencia y efectos indirectos admiten lectura contextual.|
|comparison/exposed-L1|Aceptable en contenido; referencia concreta a corregir|La comprobación de corrección/cobertura de trazas está apoyada en NASA, no en la etiqueta Procedimiento11 usada en esa frase. Separar atribución de contenido.|
|comparison/exposed-L2|Aceptable|Se mantiene aceptación. Repetición y párrafo indirecto mejorables; no bloqueantes.|
|comparison/exposed-R1|Necesita corrección localizada del ejemplo|PT1 exige2s/1millón sin que RF1 o una premisa aparte fije ese objetivo. Las cifras ficticias son válidas; falta vincularlas como requisito/premisa adicional antes de usarlas para aceptar/rechazar una implementación. No se rechaza por inventar números. «Garantiza satisfacción» es otra formulación excesiva, cuyo peso debe juzgarse con sus límites explícitos.|
|comparison/exposed-R2|Aceptable con redacción mejorable|La sección de límites niega expresamente cumplimiento automático y exige implementación/evaluación. Las frases de «asegura» pueden leerse como finalidad. No hay base suficiente para el rechazo categórico previo; matizar esas frases sería mejora.|
|comparison/T1-initial|Necesita corregir la conclusión concreta|La conclusión vincula formular medida con garantía de satisfacer la meta general, sin una salvedad posterior que distinga formulación/cumplimiento. Puede enseñar esa inferencia errónea. Definición y ejemplo son útiles; no exigir población/protocolo exhaustivos a este ejemplo sencillo. No clasificar toda la respuesta como inútil.|
|comparison/T1-L|Aceptable|Distingue expresamente objetivo medible de garantía de satisfacción y universalidad de cifra. Se mantiene aceptación.|
|comparison/T1-R|Aceptable con mejora menor|Dice medir/probar cumplimiento y explica que el tiempo es ilustrativo y adaptable. «Asegurando» en este contexto admite lectura de finalidad del proceso de prueba, no que escribir el requisito baste. Se retira rechazo categórico; precisar que debe comprobarse mejoraría el cierre.|
|comparison/T2-initial|Aceptable con terminología mejorable|El ejemplo delimita nombres/descripciones. El cierre admite no añadir filtros/campos no solicitados, no una regla universal sobre filtros. No rechazo académico por esa lectura discutible. «Natural estructurado» es etiqueta poco precisa para una lista numerada, sin impedir entender el ejemplo.|
|comparison/T2-L|Aceptable, edición redundante/confusa|El cierre distingue explícitamente alcance funcional e implementación. El cuerpo anterior sigue poco feliz, pero puede referirse a adiciones no solicitadas mientras el cierre trata la categoría general. No contradicción inequívoca que invalide la idea central; sí edición mejorable y repetición innecesaria inducida por crítica excesiva.|
|comparison/T2-R|Aceptable en el ejemplo, con cautelas de alcance|Aclara campos/coincidencias/resultados con cliente y reserva opciones de solución. No debe generalizarse que el cliente nunca impone restricciones; el contexto no afirma «nunca» y trata este ejemplo. «Mejor solución» es lenguaje exagerado a matizar, no prueba de que la explicación de ambigüedad sea falsa.|
|structured-prompts/new|Aceptable con mejora opcional|Se ratifica rectificación docente/coordinador: no imponer extras fuera del ejemplo es lectura razonable. No acredita el supuesto fallo conceptual persistente. No se requiere otra reparación para demostrar desaparición de una frase que no era inequívocamente falsa.|

Las aceptaciones no afirman precisión perfecta ni validez universal. Se preservan defectos técnicos/de presentación donde existen. Los dos juicios de corrección localizada identifican una consecuencia comprensible para aprendizaje: confundir criterio no establecido con obligación del requisito, o formulación medible con cumplimiento demostrado. Son juicios razonados actuales, no etiquetas de verdad de un nuevo benchmark.

## Qué conclusiones se rectifican

1. La original de trazabilidad no necesitaba iniciar un ciclo obligatorio por omitir todo el recorrido inverso o una excepción NASA. La crítica indujo ampliaciones que luego se castigaron por sus propias imprecisiones. No afirmar que todas las reparaciones eran necesarias.
2. iteration-002 no acredita por sí sola incapacidad de producir una explicación útil: sus rechazos dependían de exhaustividad y lecturas excesivas. Se mantienen hechos de ejecución, terminaciones, límites, preservación y parada; cambia la interpretación de calidad que motivó la parada.
3. comparison-003 ya no respalda «ninguna estrategia funcionó en T2» ni la comparación de éxito/fallo anterior. Había una inicial aprovechable; repararla no era condición necesaria. L mejoró una conclusión T1, pero no se demuestra una superioridad general ni ventaja en todas las preguntas.
4. structured-prompts acredita implementación, tokenización y cambio de edición, no que la nueva estructura haya fallado en corregir un error conceptual demostrado de T2. Tampoco demuestra mejora semántica: el criterio previo estaba mal calibrado y no se ejecutó transferencia.
5. No recalcular un porcentaje de calidad con estas15 salidas: son versiones dependientes de tres preguntas y el revisor no es independiente. No presentar los textos re-adjudicados como reserva nueva.

## Antes de continuar

No hacen falta nuevas inferencias para «aprobar» estas frases. Conservar perfiles técnicos útiles. El siguiente incremento debe tratar aceptabilidad, materialidad y dudas del revisor por separado, y probar conversaciones completas representativas, revisando las respuestas como explicaciones docentes contextualizadas. Antes de una nueva campaña, actualizar el protocolo de evaluación y registrar ejemplos de aceptable imperfecta/error material/incertidumbre; no entrenar en estos ejemplos y volver a contar acierto como transferencia.

No se abren automáticamente gates o participantes: este addendum rectifica evaluación del contenido; privacidad, funcionamiento integrado y decisiones del piloto tienen su propia evidencia. Tampoco requiere garantía universal ni perfección lingüística para un ensayo docente. El informe previo answer-evaluation-calibration-audit.md y esta tabla deben acompañar cualquier uso futuro de las conclusiones de los ensayos afectados.
