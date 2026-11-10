# Revisión con contenidos web variados — CPU

Petición: ampliar las pruebas con contenidos de Internet relacionados con la asignatura, sin GPU. Inicio 30-10-2026; finalización 31-10-2026. **Medición terminada; v4 no promovida.**

## Qué se está probando

Se revisan respuestas sintéticas controladas frente a pasajes originales de fuentes oficiales y material docente real. No son conversaciones generadas por el tutor ni respuestas académicas prefabricadas para participantes. Las cifras de este banco no acreditan utilidad con estudiantes, revisión docente ni verificación semántica general.

Fuentes capturadas, con HTML, extracción, recibos y hashes:

- [GOV.UK: historias de usuario](https://www.gov.uk/service-manual/agile-delivery/writing-user-stories).
- [NASA: gestión de requisitos y trazabilidad](https://www.nasa.gov/reference/6-0-crosscutting-technical-management/).
- [W3C: contraste mínimo](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), empleado como ejemplo de requisito no funcional medible, sin ampliar el temario obligatorio.
- [NASA: validación de producto](https://www.nasa.gov/reference/5-4-product-validation/).
- [GOV.UK: entrevistas en profundidad](https://www.gov.uk/service-manual/user-research/using-in-depth-interviews).

Las fuentes quedan en este expediente, sin incorporarlas al corpus activo. La descarga no demuestra por sí sola validez académica. Las páginas docentes utilizadas estaban disponibles, no en cuarentena. No se enviaron datos del profesor o alumnado a Internet.

## Desarrollo: seis casos con v3

| Caso | Resultado observado |
|---|---|
| D01, historia ficticia válida | Aceptada correctamente. |
| D02, falsa obligación de plantilla literal | Detecta el error principal, pero lo registra como conflicto docente con un testigo exclusivamente externo; contrato inválido. Añade una exigencia opcional sobre explicar la importancia del criterio de aceptación. |
| D03, trazabilidad válida | Aceptada correctamente; una etiqueta de límite no invalida el contenido. |
| D04, falsa exclusión de trazabilidad hacia delante | Detecta el error principal, pero no aporta el testigo docente exigido para su declaración de conflicto; contrato inválido. |
| D05, contraste hipotético más exigente que el mínimo | Aceptado correctamente. Inventar un valor coherente no es un error. |
| D06, mínimo numérico equivocado | Señala un problema distinto y mal fundado: confunde excepciones de contraste con obligaciones. Además excede el límite de longitud del testigo. No cuenta como acierto semántico. |

Las seis etiquetas superficiales coinciden con el resultado esperado, pero eso sería una métrica engañosa: solo tres salidas son utilizables y correctas; otras dos reconocen el problema principal sin producir un dictamen utilizable; la última razona mal. Seis llamadas completas, 875,297 segundos incluyendo carga, sin CUDA.

## Único ajuste experimental v4

Separa falta de apoyo externo y conflicto con el profesor, respeta condiciones/excepciones y pide una objeción principal breve. Conserva ejemplos ficticios coherentes y cobertura ajustada a la pregunta. No elimina controles de errores materiales. El perfil no es el predeterminado.

Una prueba reprodujo otra fisura: con una objeción por ronda, dos defectos diferentes tenían el mismo número de objeciones y el bucle paraba por esa igualdad. Solo v4 permite continuar ante un defecto diferente; conserva la parada por defecto repetido, texto idéntico, dos rondas y presupuestos.

La calibración se amplió prospectivamente de tres a cuatro casos expuestos para incluir D06 después de observar su fallo. Se conserva `adjustment-plan.json` y se registra la modificación antes de inferencia en `adjustment-plan-final.json`. Los cuatro casos de transferencia se crearon y congelaron antes del ajuste y no se usan para afinar.

## Corrección HTTP independiente

NASA devolvía cabeceras `Link` repetidas, legales para ese campo. Se combinan únicamente esas cabeceras; las cabeceras críticas duplicadas siguen rechazándose. Las pruebas reprodujeron el fallo antes del cambio y pasaron después; las dos páginas NASA se adquirieron después de corregirlo. No se siguen automáticamente esos enlaces. Se conservan los recibos fallidos originales.

Durante el cierre de una conexión apareció un aviso asíncrono Windows `ConnectionResetError` (10054). Los cuerpos y sus hashes se verificaron; el aviso permanece registrado y no se presenta el log como libre de incidencias.

## Validación y pendientes

139 pruebas focales y de regresión aprobadas en la comprobación final (`regression-final.log`), con un aviso existente de Starlette. Black conforme en los cinco archivos de código/pruebas afectados; AST idéntico antes y después del formato. Ruff global: diez hallazgos anteriores, cero nuevos comparando `(archivo, código, mensaje)` con multiplicidad frente al baseline. Integridad de HTML, unidades normalizadas, extracciones docentes y bancos comprobada con `verify_bank.py` y `verify_records.py`. Se conservan las copias exactas del código ejecutado, anteriores al formato.

### Incidencia de copia UTF-8

La preparación interactiva de la primera calibración omitió `encoding="utf8"` al leer los bancos originales. Windows los interpretó como cp1252 y la copia alteró caracteres antes de enviarlos al modelo. Se detuvo el intento tras tres respuestas completas; el cuarto turno estaba pendiente de resultado. Sus salidas y la selección provisional basada en ellas se conservan, pero quedan invalidadas para comparar perfiles. No se atribuye al modelo este defecto del experimento.

`utf8-incident.json` registra el sucesor `calibration-utf8`, con el mismo candidato y casos, sin reajuste de prompt. Antes de ejecutarlo se comprobó igualdad exacta de objetos con las entradas originales, leyendo siempre UTF-8. Los bancos iniciales se prepararon con UTF-8 explícito: ni el desarrollo ni la transferencia original están afectados. La transferencia todavía no había sido ejecutada.

### Calibración corregida y decisión

Dos respuestas completas bajo UTF-8 correcto bastan para incumplir los criterios de selección:

- **D02:** crítica principal válida y contrato formal válido. Sin embargo, presenta `User requirements are expressed as user stories or scenarios` como respaldo de flexibilidad de formato y de una oposición docente; ese pasaje no establece ninguna de las dos cosas. La corrección formal no acredita el razonamiento completo.
- **D05:** rechazo falso del ejemplo válido. Exige excluir el texto grande de una propuesta de 5:1 aunque el caso no requiere esa excepción; añade umbrales de tamaño y referencia a dispositivos móviles que el pasaje suministrado no establece. Además inventa el texto de `claim` y el contrato lo rechaza.

Se detiene v4 con dos resultados completos y el siguiente turno interrumpido; la regresión anterior C02 queda sin ejecutar. No se cuentan como errores semánticos los turnos no terminados. `early-stop.json` conserva la decisión. La espera automática de transferencia se bloqueó al no haber finalización normal; después se inició explícitamente la transferencia congelada bajo v3. No se creó un segundo candidato de prompt.

La transferencia usa copias byte a byte de los cuatro casos originales. No es una comparación causal v3/v4 en esos temas; v4 no superó la calibración. T168/T169 y la acreditación semántica siguen abiertas; no se habilitan participantes, publicación ni gates. No hay GPU, descargas de modelos, Reset ni commits.

## Transferencia terminada: cuatro casos nuevos, v3

| Caso | Contenido | Juicio sobre la revisión real |
|---|---|---|
| H01 | Verificación/validación correctas, ejemplo ficticio | Aceptación correcta, contrato válido. |
| H02 | Inversión de verificación y validación | Detecta el error principal y recupera la definición pertinente de NASA. La explicación es imprecisa al decir «no solo» necesidades; no respalda el supuesto conflicto docente con un testigo del profesor. Dos citas exceden el contrato. No utilizable automáticamente. |
| H03 | Entrevista abierta con seguimiento neutral | Aceptación correcta, contrato válido. No se exige cubrir una entrevista entera. |
| H04 | Preguntas dirigidas presentadas como neutrales | Detecta correctamente el defecto principal. Añade incidencias redundantes, no cita al profesor para su declaración de conflicto y altera la forma literal de `claim`; contrato inválido. No utilizable automáticamente. |

Cuatro llamadas completas, 913,671 segundos incluyendo carga. `completion.json` acredita `cuda_initialized=false`; el runtime es PyTorch CPU, float32, ocho hilos y modelo local existente Qwen2.5-7B. Ningún turno agotó tokens o plazo en desarrollo y transferencia.

**Lectura práctica:** v3 acepta los cinco ejemplos válidos del desarrollo y transferencia; no se observa rechazo excesivo de esos ejemplos. En cuatro de los cinco casos defectuosos reconoce el problema principal, pero no produce un dictamen formal y semánticamente suficiente; en el quinto razona sobre una excepción equivocada. Las diez etiquetas coinciden superficialmente con el oráculo, pero eso no es diez aciertos de revisión. Solo las cinco aceptaciones son íntegramente correctas y utilizables en este banco. No se debe confundir un límite formal de cita con la verdad del contenido, ni una crítica acertada con justificación completa de todos sus ejes.

El único ajuste v4 probado no mejora lo suficiente y añade un rechazo falso: queda experimental y fuera del flujo activo. No se endurece el criterio por estilo ni se modifican respuestas/oráculos para hacerlas pasar. Tampoco se propone otra campaña de prompts sobre estos casos ya expuestos. La falta de un revisor fiable sigue siendo una limitación acreditada por esta muestra, no una prueba de imposibilidad para todos los modelos.

## Coste, conservación y resultado de SpecKit

Se iniciaron 17 peticiones en total: seis de desarrollo, cuatro del intento inválido por codificación, tres de calibración corregida y cuatro de transferencia. Hay quince salidas completas: tres pertenecen al intento inválido y se excluyen de la evaluación; dos peticiones quedaron interrumpidas. Son doce salidas completas evaluables, incluyendo dos de calibración expuesta. No se cuentan interrupciones o casos sin ejecutar como errores semánticos. Detalle en `metrics.json` y registros por etapa.

Coinciden los 308 hashes históricos y los 140 de expedientes previos del revisor, además de los 22 archivos del manifiesto de fuentes/bancos. La transcripción [íntegra](transcript-full.md) incluye versiones correctas e incorrectas, pasajes suministrados y revisiones brutas, marcando el intento inválido. No se sobrescribieron resultados previos.

T171–T173 documentan corrección y medición ejecutadas; T168/T169, la integración autónoma, Feature012 y sus gates siguen abiertos. La revisión acotada spec/plan/tasks no detecta contradicción nueva con FR-014/020/022–024: la experimentación no autoriza publicación ni convierte una descarga en verificación. No es una auditoría global nueva de toda la feature. Las brechas ya están representadas en las tareas abiertas; no se duplican IDs.

Los árboles propios de inferencia se cerraron. No se tocaron procesos ajenos, datos habituales ni corpus activo. GPU no utilizada.
