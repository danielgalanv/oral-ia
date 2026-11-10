# Revisión más tolerante — perfil v3, 30-10-2026

## Cambio aplicado

Perfil optativo `web-review/v3` para el revisor experimental. V1/v2 y el tutor
general conservan sus instrucciones. Se selecciona explícitamente mediante
`prompt_version="web-review/v3"`; no se activa un nuevo flujo de participantes.

El criterio es adecuación académica a la pregunta, no perfección:

- Los escenarios, cifras y requisitos hipotéticos coherentes no necesitan aparecer
  literalmente en el PDF. Basta que el marco de ejemplo esté claro por el contexto.
- Una propuesta normativa no afirma que un sistema existente ya la cumpla.
- Las mejoras opcionales, estilo y cobertura de toda una lista docente no justifican
  reparar una respuesta suficiente para una pregunta sencilla.
- Los hechos académicos y las conclusiones sí requieren apoyo: no se disculpan
  contradicciones, atribuciones falsas ni cumplimiento/viabilidad sin premisas.
- Se pide como máximo una incidencia material, con frase, motivo y evidencia.
  Las mejoras opcionales no se transmiten al corrector como defectos obligatorios.

No se convierte un `no_issues_found` en autorización de publicación, ni se debilitan
la validación de testigos, los gates, el acceso a fuentes o el consentimiento.

## Calibración real CPU

Qwen2.5-7B-Instruct, snapshot `a09a35458c702b33eeacc393d103063234e8bc28`, float32,
8 hilos, greedy y plantilla nativa. Pesos ya locales, sin descargas, GPU o red nueva.
Los mensajes efectivos y brutos se conservan; el oráculo solo se usa para medir.

Primera pareja: dos versiones expuestas de R01, una con el parche correcto del
ensayo anterior y otra con la inferencia original. Mismas fuentes y pregunta.
Protocolo previo: máximo dos llamadas/900 s incluyendo carga, 512 tokens/420 s por
llamada, cero reintentos o cambios de prompt durante el ensayo.

| Caso | Resultado observado | Interpretación acotada |
|---|---|---|
| C01, respuesta reparada | `no_issues_found` | Deja de rechazar el umbral ficticio de cinco segundos y de exigir toda la lista NASA. |
| C02, inferencia original | `no_issues_found` | Omite que ser medible no demuestra realizabilidad; se conserva como permiso falso respecto al criterio previo. |

Ambas llamadas terminaron completas, con contrato válido y cero reparaciones de
formato. Tiempo de la pareja: 122,328 s. El resultado **no** acredita una mejora
global: reduce una objeción equivocada pero no conserva la detección de ese error.
No se cambia el oráculo de C02 para hacerlo pasar después de observar la salida.

Después se congeló **C03**, un control adicional de contradicción explícita, sin
cambiar el prompt: una respuesta sintética invierte la definición de verificabilidad
de la página docente 73. Se altera la respuesta de ensayo, nunca el PDF ni una cita
del profesor. Presupuesto separado: una llamada/450 s, hasta 512 tokens/420 s.
Su propósito es distinguir tolerancia a un texto con matices de aceptar cualquier
cosa. Su resultado no sustituye C02 ni convierte esta calibración en reserva nueva.

C03 produjo `issues_found / conflict / repair` con testigo literal válido de T73:
identificó correctamente que la verificabilidad implica poder comprobar el requisito,
no su imposibilidad de comprobación. Emitió también una incidencia de cobertura sobre
viabilidad, pertinente a la pregunta recibida; no respetó la preferencia de una sola
incidencia del prompt, aunque el contrato existente permite hasta tres. No se ocultó
ni reparó su salida. Terminó completo en 262,297 s incluyendo carga. Tres llamadas
CPU en total, con presupuestos separados y sin tocar los anteriores.

Balance: acepta el positivo, omite una inferencia incorrecta y detecta una oposición
conceptual explícita. La mayor tolerancia está observada en este pequeño diagnóstico,
pero no hay evidencia para usar este candidato como decisor semántico acreditado.
No se infiere rendimiento en GPU, generalización o superioridad global frente a v2.

## Pruebas e integridad

Tres negativos fallan antes de implementar v3; después **131 pruebas dirigidas**
aprueban. Comprueban la selección del rol, ausencia de reparación innecesaria con
dobles, mantenimiento de la ruta de reparación material y rechazo de testigos
inventados, además de las regresiones previas. No se presentan como prueba de
capacidad semántica; esta proviene de las llamadas reales y su contraste con fuentes.

Black y Ruff en los archivos afectados; Ruff global comparado con multiplicidad
frente al baseline de diez diagnósticos anteriores. Se conservan los originales,
los expedientes anteriores y sus presupuestos. No se modifican la interfaz,
migraciones, datos habituales ni T090/T150. Sin Reset ni commits.

`final-checks.json` acredita cero diagnósticos Ruff nuevos, 308 hashes históricos y
92 archivos del dossier anterior conservados. [Transcripción íntegra](transcript.md)
con las tres respuestas examinadas y sus juicios, sin correcciones manuales de texto.
`cleanup.json` confirma que no queda proceso propio de inferencia.

Archivos: `web_review_prompts.py`, `web_review_rounds.py`, pruebas de ese módulo y
adendas de spec/plan/tasks. Datos, protocolos y código ejecutado en este dossier.
Los ejecutores rechazan reutilizar resultados por escritura exclusiva. Para otra
ejecución crear carpeta y presupuesto nuevos; estos casos ya están expuestos.

## Límite del resultado

Suavizar el criterio no equivale a validar al revisor como autoridad. Esta es una
calibración pequeña sobre desarrollo conocido, revisada de forma no ciega por el
coordinador, no aprobación docente o validación independiente de conversaciones.
T168/T169 y las tareas semánticas anteriores siguen pendientes; no se abre G2,
SC001 ni publicación. No se propone volver a exigir que las cifras inventadas de
un ejemplo aparezcan en la fuente para compensar las omisiones del modelo.

## SpecKit acotado

Prerrequisitos de Feature012 y checklists previos resueltos; sin hooks registrados.
Análisis de FR-014/020/022/023, plan y T170: el nuevo perfil distingue ficción de
afirmaciones académicas, conserva trazas y controles y no contradice la constitución
al permanecer experimental, local y sin publicación. No se detecta contradicción
crítica nueva en este incremento. T170 se completa como implementación y calibración,
no como validez acreditada. No aparece una nueva pieza de implementación ausente en
su alcance; las brechas semánticas/de integración ya tienen T168/T169 pendientes.
No se declara convergencia global de Feature012 ni se cierran esas tareas por tres
juicios. Los IDs y estados anteriores a T170 permanecen intactos.
