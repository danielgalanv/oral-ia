# Contraste final por el asistente — reparación real incompleta

Autor: asistente actual. Se leyeron de nuevo la pregunta, la respuesta inicial
COMPLETA, los cinco pasajes COMPLETOS y TODO el texto que devolvió la única
llamada de reparación. No hay autocrítica ni post-review del14B. La salida nueva
terminó `length` a768tokens y48,078s: se cortó en «Fuente: 6 - Procedimiento
requisitos». No se inventa su continuación ni se declara una segunda versión
completa. El contraste siguiente evalúa solo el texto recibido; no acredita
una reparación completa.

## Avances observados, sin contar éxito de una versión completa

1. La nueva frase «la trazabilidad permite también el recorrido inverso, desde
   los requisitos hasta las necesidades del cliente» añade una dirección que
   faltaba. Respaldo: NASA142, «Each requirement should be traced back to a
   parent/source requirement or expectation in a baselined document». Es un
   avance conceptual, aunque no muestra el recorrido inverso desde una prueba
   ni aplica ese recorrido al ejemplo completo. No basta añadir la palabra
   bidireccional: aquí sí explica una dirección antes ausente.
2. «la trazabilidad no garantiza que el trazado sea correcto ni que cubra
   íntegramente al requisito superior» expresa el límite omitido. NASA142
   requiere comprobar corrección y atención completa al requisito padre.
   La frase es un avance real; la oración siguiente describe de modo impreciso
   qué debe comprobarse, como se registra abajo.

No se cuentan como dos defectos totalmente resueltos: ambos avances pertenecen
a la única objeción original de cobertura y están en una salida incompleta.

## Persistencias y omisiones

- Se conserva el ejemplo hipotético coherente y el análisis de qué requisito
  y pruebas revisar. No se penalizan citas médicas pasadas como hechos inventados:
  son datos declarados de un ejemplo. Su principio está respaldado por NASA142;
  el alcance de búsqueda ilustra la ambigüedad de Requisitos13.
- La parte sobre impactos indirectos conserva «no se derivan directamente».
  Sigue faltando explicitar que es un límite de los enlaces representados,
  no una incapacidad universal de la trazabilidad para ayudar a descubrirlos.
  Se mantiene como matiz, no como contradicción demostrada.
- Las fuentes pasan de ausentes a una lista iniciada: NASA142 está identificada,
  pero la segunda referencia se corta. Procedencia visible aún incompleta.
- El recorrido inverso prueba→requisito no está explicado y no se demuestra
  cobertura completa del ejemplo. No se exige repetir toda la página NASA.

## Problemas nuevos en el texto recibido

1. **Sobreafirmación de garantía.** «asegurando que cada requisito tenga un
   origen claro y que no haya requisitos redundantes o inconsistentes» atribuye
   al recorrido inverso un aseguramiento que los enlaces no prueban. NASA142
   pide evaluar las trazas y resolver duplicaciones; Procedimiento10 distingue
   consistencia interna/externa como cualidades que deben comprobarse. La frase
   posterior que niega garantías no elimina esta tensión del texto completo.
2. **Condición de origen demasiado universal.** «cada requisito debe estar
   trazado hacia su necesidad de origen» no conserva la alternativa de NASA142:
   «or identified as self-derived and concurrence on it sought from the next
   higher level requirements sources». La fuente admite requisitos derivados
   de buenas prácticas o decisiones de diseño bajo esa condición. No se deben
   eliminar esas excepciones al resumir; la objeción original no pidió hacerlo.
3. **Comprobación independiente mal delimitada.** «Es necesario evaluar
   independientemente la consistencia y la precisión de cada requisito para
   asegurar que no existan ambigüedades o redundancias» transforma «independently
   if possible» de NASA142 en una necesidad incondicional y desplaza el objeto
   de comprobación de corrección/cobertura de la traza a calidad individual.
   Procedimiento10/11 sí respaldan comprobar calidad, pero no esa equivalencia
   ni esa garantía. Es un problema de condición y síntesis, con evidencia
   disponible; no una ausencia del ranking.

Los tres hallazgos nuevos no son tres errores del alumno ni una nota: describen
el texto generado. No son una tasa de calidad extrapolable. Se separan de las
persistencias y del truncamiento operativo.

## Balance y crítica del revisor

Una objeción original de cobertura con dos componentes: avances parciales en
ambos; cero reparaciones completas aceptables. Una omisión de procedencia
visible persiste por corte. Tres hallazgos nuevos localizados arriba. No se
observó eliminación del ejemplo ni del análisis de cambio: se conservaron,
pero se perdieron condiciones de la fuente en las adiciones. No hay crítica
semántica original demostrada como equivocada. El testigo original mal
transcrito sigue reconocido como error mecánico del asistente, corregido en
CPU antes de esta carga; no se reescribe su evidencia histórica.

El `outcome` exterior de repair.json es el INICIAL conservado por el adaptador,
no la salida nueva. La reparación recibida se encuentra en
`trace.calls[0].outcome` y en el recibo `*-result.json`; su `ok=false` y
`finish_reason=length` permanecen intactos. No contar texto inicial retornado
como prueba de que el modelo no cambió nada.

Resultado: se completó la invocación pendiente y su revisión asistida, con
resultado negativo de terminación y defectos nuevos. No hay revisión semántica
autónoma local resuelta, publicación ni tutor aprobado. No se hace otra llamada
para acortar o aprobar este mismo caso. E2/Feature012 y gates siguen como antes.
