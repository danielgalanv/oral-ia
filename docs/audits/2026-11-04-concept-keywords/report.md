# Palabras clave y revisión conceptual — 04-11-2026

## Resultado

Cuatro preguntas, dos recorridos: ocho respuestas completas, 16 llamadas. La versión nueva añadió palabras clave en 4/4. El revisor no pidió correcciones en ninguna de esas ocho respuestas. La lectura del conjunto no confirmó una inversión de los conceptos centrales; eso no valida cada afirmación ni todas sus fuentes. No se demuestra superioridad conceptual general, y subsisten limitaciones de recuperación y redacción. [Respuestas completas](transcript-mobile.html).

El piloto normal selecciona ahora generación v4, con palabras clave obligatorias. Conserva revisión v8: la revisión conceptual v9 permanece experimental, no promovida. No se cambian gates, publicación ni aceptación docente.

## Qué se implementó

Generación v4 conserva v3 y añade una lista final siempre visible. El host comprueba presencia sin inventar vocabulario ni editar la respuesta: si falta, pide una reparación y revisión real. Las comas también se aceptan como separadores. El control no bloquea por repeticiones o por superar la longitud sugerida. La prueba negativa CPU demuestra que una aceptación nativa no omite esta obligación de formato.

Revisión v9 conserva el contrato referenciado y pide identificar conceptos independientemente de la lista, contrastar denominaciones, significado y uso, y detectar definiciones bajo encabezados incorrectos. No contiene nombres de los conceptos del banco ni respuestas docentes prefijadas. Su razonamiento y su dictamen siguen siendo falibles. Es un primer prototipo guiado: no se ha construido un registro estructurado de definición/uso/fuente por concepto ni recuperación adicional de definiciones por concepto. Eso sigue pendiente en T219.

Las dos condiciones usaron exactamente los mismos pasajes RAG por pregunta, sin añadir una página a mano para hacer pasar un caso. No se usaron reglas específicas de completitud/complejidad. Los mensajes de generación v4 son idénticos al mantener el revisor estable v8 o elegir v9, comprobado en CPU. La interfaz sigue presentando texto académico, sin JSON al alumno. No se modificaron frontend, corpus, modelos o pesos.

## Controles independientes de respuestas

Tras las primeras comparaciones se congeló una segunda batería antes de ejecutar sus llamadas, sin modificar prompts. No es una reserva ciega ni transferencia acreditada. H_BAD es la salida histórica íntegra; H_GOOD y U_BAD/U_GOOD son respuestas diagnósticas derivadas, nunca texto atribuido al profesor. El oráculo separado no se envió a los modelos.

| Estímulo | Revisor v8 | Revisor conceptual v9 |
|---|---|---|
| H_BAD: error histórico Complejidad/Completeness | No lo objetó | JSON inválido; contenido bruto sin objeción útil |
| H_GOOD: definición correcta de completitud | Sin objeciones | Sin objeciones |
| U_BAD: definición de realizable atribuida a comprobable | Detectó la mezcla | Detectó la mezcla |
| U_GOOD: ambas definiciones correctamente distinguidas | Sin objeciones | Sin objeciones |

Ocho llamadas adicionales. La salida inválida de v9 contiene una comilla sobrante y se rechazó; no se reparó ni se contó como un permiso semántico. Su bloqueo formal tampoco demuestra que detectara el error. No hubo críticas falsas en los dos positivos breves, pero la muestra es mínima. La reparación GPU estaba prevista solo si v9 emitía una incidencia válida para H_BAD; no ocurrió y no se ejecutó. No se cuentan reparaciones no realizadas como fallos.

En total: 24 llamadas, ninguna reparación GPU aplicada, modelos propios cerrados. La presencia de listas está comprobada; la eficacia superior del revisor no.

## Criterios de lectura proporcionados

Las cifras y escenarios hipotéticos son válidos; no se exigen exhaustividad de una especificación real ni citas por frase. Se juzga la respuesta completa, incluidas sus condiciones explicadas después del ejemplo. K2 se acepta como ilustración de la independencia de criterios bajo un alcance hipotético pequeño, no como validación de un proyecto real. K3 arrastra un hueco del ranking: no recuperó las páginas de criterios 11/73. K4 conserva una errata («estadholders») y una formulación final mejorable; no se declara impecable por tener palabras clave.

## Validación y estado

684 pruebas de regresión CPU; 55 dirigidas finales después de conectar el perfil visible. Ruff mantiene diez hallazgos previos y cero nuevos, con multiplicidad. Los mapas de 308/140/22 entradas conservan hashes. [Comprobaciones](checks.json).

Las fuentes y resultados originales no se reescriben. Los dos cambios de formato posteriores conservan AST; la selección normal de v4 y aceptación de comas son cambios declarados. La regla terminológica específica anterior permanece en el recorrido estable; no se usó ni se presenta como solución general de este ensayo. La siguiente mejora de T219 debe hacer verificable qué conceptos/definiciones se contrastan, sin ajustar un diccionario a H_BAD/U_BAD.

Comando del piloto: `.\scripts\study-chat.ps1`. No hubo commits, Reset, audio, calificación, rúbricas o publicación para participantes. Voz y utilidad con estudiantes no se validan aquí.
