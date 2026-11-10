# Igual criterio de adecuación: material docente e Internet

31-10-2026. Petición expresa del usuario durante la repetición v5. Estado: cuatro
controles expuestos CPU terminados. Criterio común implementado; mejora parcial,
sin acreditación general del revisor.

## Cambio acotado

`web-review/v6` conserva **íntegro** el prefijo de política de v3 anterior al esquema
JSON: no forzar defectos, aceptar escenarios/cifras/nombres ficticios coherentes,
contrastar principios y conclusiones, distinguir propuesta y cumplimiento, y no
reparar mejoras opcionales. Una prueba comprueba igualdad exacta de ese prefijo.
El criterio es el mismo para material docente y fuentes de Internet.

Se mantiene el esquema de referencias: el revisor describe la afirmación y señala
`source_id`; el host presenta documento/página o URL desde metadatos originales.
No se requieren citas copiadas ni coincidencia literal del claim.

También se corrige una restricción tipológica de v5: `contradiction` puede señalar
una oposición con una fuente externa. No necesita fingir una fuente docente para
ello. **Declarar conflicto con el profesor sí exige referencia docente.** Se sigue
rechazando una referencia ajena, duplicada o de versión/documento incompatible.
La identidad de una referencia no demuestra que la crítica sea verdadera.

V5 y sus resultados quedan intactos. Su repetición de diez casos terminó antes de
modificar el código; las copias ejecutadas se preservaron. El nuevo perfil es
optativo y no cambia consumidores históricos ni autoriza participantes.

## Validación y ensayo separado

Cuatro controles nuevos de contrato fallaron antes del registro de v6. Tras
completar su registro y cableado pasan **164 pruebas CPU**; Black y Ruff conformes
en los cuatro archivos afectados. Se conserva el fallo intermedio de registro,
corregido antes de inferir. El bucle simulado revisión → reparación → revisión
conserva referencias y publicación deshabilitada.

Medición nativa con Qwen2.5-7B local CPU float32, ocho hilos, greedy: D03/D04 y
D05/D06, dos pares expuestos. Preguntas, borradores y fuentes idénticos a los
anteriores; oráculo separado, nunca enviado al modelo. Máximo cuatro llamadas y
1800 segundos incluyendo carga, 512 tokens/420 segundos por llamada. Mensajes
validados antes de carga: 1371–1434 tokens, sin recortes. Sin reintentos ni cambios
de prompt durante el ensayo. No hay GPU, red ni descargas de modelos.

La hipótesis es admitir los dos ejemplos válidos (identificadores ficticios y
umbral propuesto más exigente), manteniendo detección de las dos falsas
atribuciones/condiciones numéricas. No se adjudica aceptación general por estos
casos conocidos, no se consume la reserva histórica y no se alteran sus oráculos.
T175 permanece abierta para controles nuevos e integración independiente.

## Resultado observado

Cuatro llamadas completas, 820,047 segundos incluyendo carga, sin CUDA. No hubo
reintentos ni cambios de prompt durante su ejecución.

| Caso | Juicio académico sobre la revisión | Estado técnico original |
|---|---|---|
| D03, códigos ficticios coherentes | Vuelve a aceptar correctamente el ejemplo. | `no_issues_found` con acción `none`, que el enum original no admitía. |
| D04, falsa trazabilidad solo hacia el padre | Detecta el error real y marca correctamente rechazada la atribución externa. | Declara conflicto docente sin señalar el documento del profesor. |
| D05, propuesta de mínimo 5:1 frente a mínimo 4,5:1 | Sigue rechazándola erróneamente y exige excepciones excluidas por la pregunta. El ejemplo es válido: el error pertenece al revisor. | `issues_found` con acción `limit`, inconsistente con su decisión de reparar. |
| D06, falsa suficiencia de 3:1 para texto ordinario | Detecta correctamente el mínimo real 4,5:1. Las dos incidencias repiten esencialmente el mismo error. | Contrato válido; `external_support=supported` sigue siendo una clasificación mal justificada para la atribución falsa. |

En esta muestra se recupera la aceptación de uno de los dos ejemplos válidos y se
detectan los dos errores principales. **No se presenta el rechazo de D05 como
exigencia académica legítima ni como fallo del ejemplo.** El modelo sigue aplicando
el criterio de forma inconsistente. La eliminación de citas se conserva; los
identificadores emitidos corresponden a las fuentes recibidas. Las referencias
acreditan localización, no que todas las etiquetas del revisor sean verdaderas.

V5 había rechazado ambos positivos de estos pares. V6 recupera D03, pero no D05.
Esta observación no demuestra superioridad general ni aceptación docente; tampoco
valida conversación completa o reparación de respuestas nuevas.

## Compatibilidad técnica posterior, sin nueva inferencia

Tras terminar el ensayo se aplicó la regla registrada antes en
`idle-action-compat-plan.json`: únicamente para v6, `none` con `no_issues_found`
se presenta como `explanation`; con `insufficient_evidence`, como `limit`. No se
cambian status, incidencias, afirmaciones ni referencias. No se reinterpretan
decisiones contradictorias como `issues_found/none` o `no_issues_found/repair`.
V5 mantiene su comportamiento histórico.

Dos pruebas reprodujeron antes del ajuste el rechazo de esos alias; las cinco
pruebas de compatibilidad pasan después. La regresión final suma **169 pruebas
CPU aprobadas**, con el aviso previo de Starlette. Black conforme y Ruff global
con diez hallazgos existentes y cero nuevos frente al baseline, conservando
multiplicidad.

`compatibility-replay.json` aplica exclusivamente ese parser a las cuatro salidas
conservadas, sin llamar al modelo ni usar el oráculo. D03 y D06 pasan el contrato;
D04 y D05 conservan sus errores. Los originales no se sobrescriben ni se cuentan
como nuevas llamadas. Se preserva el código exacto de la ejecución anterior a la
compatibilidad. [Comparación íntegra](transcript-full.md).

## Conservación y cierre acotado

Coinciden 308 hashes históricos, 140 de los anteriores expedientes del revisor y
22 del manifiesto de fuentes/bancos. Ambos ensayos del día conservan sus entradas,
oráculos y código ejecutado. Los workers propios terminaron; no se tocaron procesos
ajenos, corpus activo, datos habituales, GPU ni presupuestos anteriores. Sin Reset
ni commits.

T177 completa implementación y medición del criterio común, no acreditación de
comportamiento fiable. T168/T169/T175 y Feature012 siguen abiertas. Ningún resultado
autoriza publicación: las críticas son falibles y el ejemplo válido de D05 sigue
considerándose aceptable en esta adjudicación técnica.
