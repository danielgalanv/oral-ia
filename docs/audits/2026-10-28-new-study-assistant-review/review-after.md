# Contraste final por el asistente

Se releyeron pregunta, candidata inicial completa y los cinco pasajes íntegros
de la misma solicitud congelada. No existe versión corregida: el rechazo del
testigo ocurrió antes de reservar o enviar una llamada de reparación. No se
presenta el texto inicial como un «después» ni se inventa un contraste entre
dos versiones. Resultado del mínimo con reparación: incompleto.

- Concepto y aplicación: la relación necesidad→requisito→prueba y el análisis
  del cambio están respaldados por NASA142 y Procedimiento11. El ejemplo toma
  el problema de alcance de búsqueda de Requisitos13 y añade explícitamente
  datos hipotéticos. No hay motivo para rechazar esos datos como invención
  factual. No dice que el cambio ya esté aprobado.
- Omisión persistente: falta el recorrido inverso y la obligación de comprobar
  corrección/cobertura de los enlaces. NASA142 contiene ambas. La necesidad de
  esa comprobación limita lo que puede concluirse por disponer de una cadena.
- Límites: advierte que hace falta evaluar impactos adicionales. La mención
  hipotética de rendimiento, almacenamiento y seguridad es ilustrativa, no un
  diagnóstico observado. «No se derivan directamente» debe entenderse como
  límite de las relaciones representadas en ese ejemplo; no acredita que la
  trazabilidad sea incapaz de ayudar a descubrir impactos indirectos. No se
  eleva este matiz a una contradicción inequívoca.
- Procedencia visible: faltan fuentes consultadas en la respuesta inicial,
  pese a ser una obligación de la instrucción. El contexto sí las conserva.
- Corregidos: ninguno acreditado. Persistentes: omisión conceptual y falta de
  fuentes enumeradas. Nuevos: no evaluables sin otra versión. Pérdida de
  información entre versiones: no evaluable. No hay críticas sustantivas
  demostradas como equivocadas; sí un testigo mal transcrito por el asistente.

La crítica original se conserva intacta. Su segundo testigo escribía
«parent requirements» donde el PDF extraído contiene «parent require-\nments».
El validador admite normalización de espacios, no eliminación de guiones.
La corrección mecánica CPU acorta ese testigo a una subcadena literalmente
presente; mantiene explicación, pregunta, candidata y contexto. Pasa
parse_review, como registra cpu-witness-check.log. Eso prueba procedencia del
testigo, no verdad semántica ni que se haya ejecutado el corrector.

La lectura final mantiene fundada la objeción de cobertura, con el pasaje
completo disponible. No se marca supported ni aceptación humana. Esta revisión
la hace el asistente, no un verificador autónomo local. E2 y Feature012 siguen
abiertos. La segunda candidata no aportaría una comprobación distinta del fallo
de transporte, por lo que no se inicia.
