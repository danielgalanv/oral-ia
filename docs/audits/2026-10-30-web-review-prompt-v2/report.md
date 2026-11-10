# Corrección de prompts y reparación localizada — 30-10-2026

## Alcance y cambio técnico

Se aplicó un perfil optativo `web-review/v2`, preservando v1. El revisor ya no hereda
«Ayuda a estudiar» ni «no emitas IDs» del tutor. Su política propia separa respaldo
externo, compatibilidad docente y acción propuesta; exige explicar el defecto y el
cambio necesario. El corrector tiene otro rol y puede rechazar una crítica infundada.
Los datos/historial mantienen el escape existente y la plantilla nativa de Qwen.

Se reprodujo además un bloqueo tipográfico real: una cita exacta rodeada de comillas
adicionales era rechazada. Solo v2 admite quitar ese par de comillas de presentación
si el interior sigue siendo literal. El bruto no cambia y una frase con palabras
distintas sigue fallando. Esto no es verificación semántica ni arreglo de contenido.

## Qué se midió

Solo CPU, Qwen2.5-7B-Instruct existente, snapshot
`a09a35458c702b33eeacc393d103063234e8bc28`, float32, 8 hilos y greedy. No modelos nuevos,
descargas, GPU, web nueva, sesiones habituales, SQL, UI o participantes. Borradores
R01/R02/R04 expuestos del ensayo anterior: **diagnóstico de desarrollo, no transferencia**.
Las objeciones humanas y los criterios de evaluación no entran en los mensajes.

1. **Primera pasada:** hasta 7 llamadas/1200 s, 384 tokens/180 s por etapa. Se gastaron
   3 llamadas y 556,656 s. Las tres críticas quedaron parciales; no hubo reparación.
   Se conservan como límites de ejecución, no tres veredictos semánticos completos.
   El parcial R02 sí contiene una objeción observable equivocada contra una atribución
   correcta; no se le concede autoridad por producir texto.
2. **Completar R01 en CPU:** presupuesto separado, 3 llamadas/1200 s, 512 tokens/420 s.
   Los mismos mensajes v2 producen crítica completa, regeneración completa y revisión
   posterior en 539,828 s. No cambia el presupuesto de la aplicación (180 s), ni se
   reinicia el reloj de la primera pasada. La ruta nativa directa es diagnóstica.
3. **Parche localizado:** hasta 2 llamadas/600 s, parche 192 tokens/180 s y revisión
   512 tokens/420 s. El programa selecciona el primer tramo único señalado por la
   crítica automática, pide solo su sustitución y conserva lo que queda fuera.
   La crítica de cobertura sin anclaje queda sin procesar por ese editor, no declarada
   falsa automáticamente. No se introduce nuestra explicación del error en el prompt.

Los protocolos, entradas, mensajes efectivos, salidas completas/parciales y hashes
están en esta carpeta, `cpu-completion/` y `localized/`. Son presupuestos distintos,
prospectivos y conservados; no se fusionan con campañas anteriores.

## Contraste contra las fuentes

R01 proponía un tiempo de recuperación ficticio y afirmaba que el requisito era
realizable **por ser medible**. La página T73 distingue comprobabilidad de viabilidad
con presupuesto y tecnología. El ejemplo numérico es admisible; la inferencia no
queda justificada. No se exige que sus cifras aparezcan en el PDF.

La crítica completa identifica esa inferencia, aunque la etiqueta como contradicción
en vez de falta de premisas. Añade una exigencia excesiva: cubrir toda la lista NASA
de detección, informe y manejo de errores para este ejemplo. Por tanto contiene una
objeción útil y otra no necesaria, no dos defectos académicos confirmados.

La **regeneración completa falla**: conserva literalmente la inferencia inicial y
añade una propuesta más amplia. No se trata esa ficción adicional como falsedad por
no aparecer literalmente en la fuente; el fracaso probado es que mantiene el error
central. El post-revisor declara `no_issues_found`: una falsa aceptación observable.

El **parche localizado elimina la inferencia indebida** y conserva el requisito
hipotético y el resto del texto. Es una mejora concreta en un caso expuesto, no una
demostración general del crítico, del tutor autónomo o de la ampliación web.

Su post-revisor vuelve a equivocarse: llama contradicción al umbral ficticio de
cinco segundos porque no está en el PDF, y exige cubrir toda la lista NASA. No son
motivos válidos para rechazar este ejemplo como respuesta a esta pregunta. Por tanto
la mejora de reparación no acredita al mecanismo que decide su aceptación.
El parche y su post-revisión completaron dos llamadas en 371,328 s. En este trabajo
se ejecutaron ocho llamadas CPU en total, sin nuevas inferencias después.

La lectura final es no ciega y acotada: **una inferencia corregida en un caso expuesto**,
una aceptación falsa tras la regeneración completa y objeciones excesivas tras el
parche. No se construye una tasa de éxito general con esos datos ni se considera
la falta de nuevas fuentes en la cifra ficticia como error del ejemplo.

## Limitación del selector descubierta durante el ensayo

Una comilla de cierre después del punto hizo que el selector inicial tomase dos
oraciones como un tramo. El objetivo real permanece en `localized/selection.json`;
no se presenta retroactivamente como una única oración. En este resultado el modelo
conservó el ejemplo que estaba dentro del tramo y retiró la inferencia defectuosa.
Se añadió una regresión específica que falla antes y pasa después de corregir ese
límite del selector. Ese último ajuste solo se verificó en CPU sin otra inferencia:
la respuesta real publicada en este dossier corresponde al tramo anterior, conservado.

## Evidencia y límites de interpretación

- [Transcripción inicial y regeneración completa](transcript.md).
- [Respuesta íntegra obtenida con el parche](answer-observed.md).
- Los mensajes del parche están en `localized/patch-input.json`, su bruto en
  `localized/patch-output.json`, y la post-revisión en `localized/post-output.json`.
- Las referencias de T22/T73/N209 son los fragmentos originales aportados al ensayo;
  no se ha probado aquí recuperación o adquisición nuevas ni comparación de todo el curso.
- R02 utiliza un apunte contrafactual experimental aislado, nunca una modificación ni
  una acusación al material del profesor real.
- El acuerdo del revisor, EOS, JSON válido, coincidencia literal y conservación del
  texto no acreditan por sí solos la verdad. La lectura de contenido de este informe
  la hace el coordinador contra las fuentes, sobre casos conocidos; no es ciega ni
  aceptación docente ni un evaluador automático acreditado.

## Archivos y verificación

Producción experimental: `web_review_prompts.py`, `web_review_rounds.py` y
`web_local_patch.py`; pruebas `test_web_review_rounds.py` y `test_web_local_patch.py`;
adendas de spec/plan/tasks. No se cambia el prompt general de los otros perfiles,
el transporte habitual, las políticas de actividad ni los presupuestos históricos.

Antes de la separación: 2 negativos fallan y 10 pruebas pasan; después 12 pasan.
El negativo de comillas de cita falla antes de la normalización; después la selección
de regresiones alcanza 127 pruebas correctas. El fallo de límite de oración se
reproduce por separado; su corrección deja **128 pruebas correctas**. Black/Ruff
se comprueban en los archivos afectados y Ruff
global se compara con multiplicidad, sin borrar los diez diagnósticos existentes.

`after-changes-checks.json` acredita los 308 hashes históricos y 245 archivos recientes
preservados, los cambios posteriores de código frente a cada congelado y la igualdad
del mensaje efectivo del revisor antes/después del ajuste tipográfico. `cleanup.json`
confirma que no quedan procesos de los tres ejecutores propios.

Los primeros `freeze.json` y `final-checks.json` reflejan el código ejecutado en cada
fase, no una promesa de que producción nunca cambie después. Las correcciones
posteriores del parser/selector se registran por separado; no se recalculan aquellos
hashes para fingir que ya estaban durante los ensayos. `executed-code/` conserva el
código inicial congelado. Para repetir, crear otro dossier y congelar explícitamente
su versión; los ejecutores rechazan reutilizar relojes/resultados. Reproducir los
bytes originales exige usar el código archivado, no ejecutar ciegamente sobre una
versión posterior. Los casos ya expuestos no sirven de reserva nueva.

Feature012 sigue abierta. T161–T163 y las tareas semánticas/de integración anteriores
no se consideran resueltas por este resultado. Sin commits, Reset ni gates abiertos.

## SpecKit: analyze/converge acotados

Checklist previo 29/29 completo, prerrequisitos resueltos a Feature012 y sin hooks
en `.specify/extensions.yml`. Revisión de FR-011/012/014/019/020/022/023 y SC-009:
las tareas del incremento tienen correspondencia con spec/plan y evidencia; no se
introduce una nueva autorización de red, publicación, evaluación del alumno o GPU.
No se detecta contradicción crítica nueva en este alcance. Esto no certifica de nuevo
todos los artefactos históricos ni todos los requisitos de Feature012.

T164–T167 completan el incremento técnico y el diagnóstico registrado, no la capacidad
general. Converge produce `tasks_appended`: dos hallazgos HIGH/partial trazados en
T168 (crítico todavía no fiable para ficción/cobertura) y T169 (validación con casos
nuevos e integración aún pendientes). Se conservan T161–T163 y los pendientes web.
No se marca convergencia completa, aceptación docente ni G2.
