# Lectura completa del contraste expuesto

Autor: asistente actual, con conocimiento de ramas; no experimento ciego.
Se leyeron la pregunta, borrador inicial T2, crítica depurada, las cinco fuentes
íntegras y ambas salidas completas, tras congelar el par. No se solicitó al
modelo local una revisión de sí mismo. Los originales ya contrastados siguen
vigentes y hasheados; no se incorpora la página13 omitida por empaquetado.

## Anterior — old

Reproduce el patrón observado en comparison-003: mantiene «detalles de diseño
innecesarios ... filtros adicionales ... otros campos» y añade al final que
pueden ser alcance funcional y que no deben considerarse innecesarios. El
defecto no se resuelve porque la negación exista en otra frase: hay contradicción
interna. Es la misma salida textual anterior de T2-L (verificación exacta en
checks finales), con nueva llamada y presupuesto propios.

## Estructura nueva — new

Cambia el cuerpo: retira aquella frase del penúltimo párrafo y no conserva la
salvedad contradictoria añadida del anterior. Eso muestra que hubo una edición
real de estructura, no simple anexado de texto. Pero el cierre vuelve a decir
«sin ordenar la inclusión de detalles de diseño innecesarios, como filtros
adicionales o búsqueda en otros campos». Traslada la clasificación incorrecta
en vez de corregirla: funcionalidades/campos pueden expresar necesidades que
deben aclararse con el cliente. NASA64 describe entradas/salidas/restricciones
y comunicación; Requisitos5 pide no predefinir solución, no descartar ese alcance.

La nueva salida mejora coherencia formal al quitar la afirmación contraria,
pero sigue sin incorporar la distinción académica pedida. No se marca como
éxito por ser más breve (436 frente a480tokens) o por reescribir el cuerpo.

## Resto de la respuesta, omisiones y revisión de la crítica

Ambas explican por qué una palabra amplia admite interpretaciones distintas y
conservan el ejemplo hipotético coherente de productos, campos y resultados.
No se exige que esos datos aparezcan literalmente en el documento. No se fuerza
todo detalle NASA o técnica de elicitación como cobertura obligatoria.
No se detecta un error nuevo inequívoco de otro concepto en new; persiste el
defecto prioritario, con distinta localización. La posible precisión terminológica
de llamar «lenguaje natural estructurado» a una lista no fue la incidencia de
este contraste; no se usa para fabricar una victoria o un nuevo cupo.

La crítica atómica se sostiene: no exige añadir filtros, solo no clasificarlos
como innecesarios por su tipo. No hay crítica demostrada como equivocada en
este par. La cautela sobre no imponer diseño se conserva como intención útil;
el fallo es confundir esa cautela con descartar potencial alcance funcional.

Inputs distintos2911(old)/2889(new), misma pregunta, borrador, observaciones,
fuentes, modelo/snapshot, NF4, greedy/semilla42, límites2048/180s y plantilla
nativa. Qwen14 no tenía duplicación previa de especiales: el resultado no se
atribuye a corregir BOS. No se cambió RAG o muestreo simultáneamente.

## Decisión de parada

Ninguna salida cumple el criterio de corrección de este caso. La estructura
nueva NO incorporó el defecto confirmado: se activa la condición autorizada
de parada y no se ejecutan las dos preguntas nuevas ya congeladas. No se
consume el resto de las ocho llamadas para buscar aprobación. No se selecciona
la última por defecto ni se añade una síntesis académica no revisada.

Resultado: infraestructura/perfiles implementados y comprobados; prueba
académica negativa de incorporación. No demuestra que la configuración explique
todos los errores ni incapacidad universal de la familia. Sin permiso de
participante, supported, aceptación docente o cierre E2/Feature012.
