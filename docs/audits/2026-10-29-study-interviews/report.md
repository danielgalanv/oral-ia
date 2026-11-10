# Otra materia del curso: entrevistas para descubrir requisitos

## Resultado

Tres preguntas nuevas, tres respuestas completas del modelo real, sin reintentos, truncamientos ni cambios de código. La conversación empieza sin historial previo y conserva las respuestas efectivamente recibidas para los seguimientos. **La muestra resulta útil para estudiar el tema**, con una imprecisión de clasificación en el ejemplo que se describe abajo.

1. **Explicación:** correcta en lo esencial. Las entrevistas ayudan a conocer trabajo, necesidades y relación con el sistema; distingue las entrevistas cerradas basadas en preguntas preparadas de las abiertas que exploran temas y explica su combinación.
2. **Ejemplo de biblioteca:** ofrece ocho preguntas pertinentes sobre problemas actuales, volumen de préstamos, información registrada, plazos, proceso deseado, mejoras, beneficios y restricciones. No convierte respuestas imaginarias en requisitos reales de la biblioteca. **El etiquetado de algunas preguntas como abiertas/cerradas es impreciso:** «¿Cuáles son los principales problemas…?» invita a una respuesta abierta aunque esté bajo «Preguntas Cerradas». Hay que distinguir el formato de una pregunta del hecho de que forme parte de un guion preparado. Esto no invalida la utilidad de esas preguntas para la entrevista solicitada, pero no se presenta esa clasificación como impecable.
3. **Por qué no bastan las entrevistas:** explicación aceptable. Señala conocimiento tácito que los usuarios no articulan, ambigüedad, necesidades en conflicto y cambios, y propone complementarlas. Se contrasta con los pasajes recuperados 52, 53, 60, 61 y 13. La frase inicial sobre conocimiento del dominio es algo amplia; el desarrollo posterior explica correctamente el problema de lo que se da por supuesto. No se rechaza toda la respuesta por una errata ortográfica o por no enumerar todas las técnicas existentes.

No se impuso un formato de respuesta ideal ni se penalizó repetir títulos o utilizar ejemplos hipotéticos. Es una revisión técnica de las respuestas de ORALIA, no evaluación del estudiante ni aceptación docente general.

## Qué se ejecutó

- `DiagnosticStudy` y `RealStudyProvider`, con Qwen2.5-14B NF4 local, perfil nativo y `study-dialogue/v1` vigente, greedy/semilla 42; 2048 tokens y 180 segundos por turno.
- Recuperación dense CPU real sobre el paquete v2, sin fijar páginas para el modelo. Las páginas 60–61 se recuperaron por el flujo normal. Se contrastaron además directamente con el PDF original para revisar las respuestas; ese contraste no se inyectó como respuesta esperada al modelo.
- Una sola carga de modelo y tres llamadas académicas. El límite compartido de seis llamadas del proveedor se conserva; las tres restantes no se consumieron.
- Integración directa, **no nueva prueba de navegador**. La confirmación de preview la hace el harness para conservar el contexto; no implica aprobación académica automática. Se mantiene `semantic_support: unverified` y no se habilitan participantes.

Los recibos completos `turn-01.json` a `turn-03.json` conservan preguntas, evidencia, solicitudes, transporte efectivo, texto bruto, preview, resultados y tiempos. El historial contiene respectivamente 0, 2 y 4 mensajes. Todas las salidas terminan con `stop`; 431, 564 y 502 tokens nuevos (1497 en total). Latencias observadas de generación: 25,046; 32,109 y 29,125 segundos. Son tiempos de esta ejecución, no una comparación de rendimiento.

## Conservación y cierre

Los hashes de los cuatro módulos registrados son iguales antes y después. **308 archivos preservados**, incluidos los originales del paquete y las once respuestas de la prueba anterior. No hubo cambios de producción, ajustes del prompt/ranking, descargas, Reset ni commits.

El worker y su árbol terminaron con recibo de limpieza positivo. No se abrió servidor público ni se alteraron procesos ajenos. Medición final: 1319 MiB ocupados y 0 % de utilización GPU.

## Evidencias

- [Conversación íntegra para móvil](transcript-mobile.html)
- [Texto completo](transcript-mobile.md)
- [Controles de ejecución y fuentes](execution-checks.json)
- [Páginas originales contrastadas](original-reference-pages.json)
- [Protocolo previo a las llamadas](protocol.json)

Esta muestra nueva de tres turnos es evidencia acotada de funcionamiento en otro contenido del curso; no demuestra calidad general en toda la asignatura.
