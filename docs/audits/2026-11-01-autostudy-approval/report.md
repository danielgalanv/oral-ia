# Prueba automática de autoestudio: doce preguntas aprobadas

El intento configurado terminó: **12 respuestas completas, 25 llamadas y ninguna truncación o deadline**. Las respuestas y sus revisiones están conservadas sin retoques. T185 acredita la preparación y ejecución del ensayo; no constituye aceptación docente ni evaluación del alumno.

- [Doce preguntas y respuestas, fuentes y observaciones](run-20261101-214928/readable-mobile.html).
- [Transcripción Markdown con los textos finales](run-20261101-214928/transcript.md).
- [Recibos originales y trazas completas](run-20261101-214928/result.json).
- [Métricas y cierre de procesos](run-20261101-214928/summary.json).

## Recorrido realmente utilizado

Guion aprobado por el usuario: tres conversaciones independientes de cuatro turnos, con el historial íntegro de lo realmente mostrado dentro de cada una. Preguntas vinculadas a la aprobación mediante SHA256 `8410a6dcd2f7b26f3b766b648887046cb5476993cefb65ea17df5acffb9dbc53`. No se añadieron respuestas esperadas ni objeciones del coordinador a los mensajes enviados a los modelos.

RAG real sobre el paquete docente autorizado v2, estrategia rrf y selección comparison-coverage/v1. El índice habitual tenía un fingerprint de implementación antiguo: cada intento construyó su índice aislado sin modificarlo. No se inyectaron páginas ideales. El preflight CPU encontró pasajes en las doce consultas, lo que no prueba su suficiencia. Se usaron documentos locales, incluidos los materiales autorizados de NASA/Sommerville; no hubo búsquedas web nuevas.

Generador Qwen2.5-14B NF4, perfil didáctico existente study-dialogue/v1, 1536 tokens por primera respuesta. Revisor Qwen3-8B NF4 con razonamiento, muestreo propio y presupuesto 8192 tokens para razonamiento más dictamen. Hasta dos correcciones con el generador estaban previstas; **ninguna se activó**. Se conservaron los dictámenes finales, sin publicar razonamiento interno. El historial mantiene el contenido completo y el cambio explícito de tema descarta contexto de búsqueda anterior.

Es un ensayo de laboratorio del recuperador, proveedor y orquestación reales; **no una prueba nueva del navegador o de la API de participantes**. La salida sigue como diagnóstico y publication_allowed permanece false.

## Resultado medido

| Concepto | Resultado |
|---|---:|
| Respuestas completas incorporadas al diálogo diagnóstico | 12 |
| Generaciones iniciales | 12 |
| Intentos de revisión | 13 |
| Dictámenes finales sin objeciones | 12 |
| JSON de revisión inválidos | 1, seguido de repetición registrada en B4 |
| Correcciones de contenido | 0 |
| Truncamientos, deadlines o seguimientos omitidos | 0 |
| Tokens nuevos, incluido razonamiento | 9877 |
| Suma de latencias de las llamadas al modelo | 794,629 s |

El resultado demuestra que el ensayo desatendido termina. No demuestra que el revisor detecte todos los errores ni que las rondas hayan mejorado respuestas: no hubo ninguna corrección de contenido en esta ejecución. La repetición de B4 pidió de nuevo un dictamen válido; no reparó silenciosamente su JSON ni cambió la respuesta del generador.

## Revisión técnica posterior, proporcionada a la pregunta

Las definiciones principales, los ejemplos funcionales, el valor hipotético de 0,3 segundos y la distinción entre trazabilidad y cumplimiento resultan útiles. C4 propone una contradicción directa y coherente. Repetir una estructura no se considera incorrecto por sí mismo. Los números inventados y escenarios coherentes se aceptan como ejemplos.

Hay puntos concretos para mejorar:

- **B2:** usa la media como criterio de aceptación sin explicitar ese supuesto. Puede acordarse una media, pero debe distinguirse de un percentil o de un límite por búsqueda. No se declara incorrecta toda la explicación por este detalle; conviene precisar qué se ha acordado medir antes de concluir cumplimiento.
- **B3:** la respuesta llega literalmente envuelta en JSON con mensaje_mostrado. Su conclusión inicial sobre medir frente a poder implementar es adecuada. El renderer también utiliza ese nombre al envolver el historial; eso identifica una hipótesis de arrastre de formato, no demuestra su causa.
- **B4:** llama Complejidad a una descripción de completitud. Es una corrección terminológica concreta. La respuesta se dispersa en una lista general en vez de concretar tanto las condiciones del ejemplo.
- **A1:** agrupa integración y dominio bajo no funcionales, mientras la diapositiva docente los enumera aparte. La convención del curso debe aclararse sin invalidar todos los ejemplos.
- **C3:** el conflicto del inventario tiene sentido respecto al requisito anterior que permitía eliminar productos. Agregar y prohibir eliminar, aislados, no son contradictorios. Se valoró el contexto completo; conviene explicitar ese referente, no rechazarlo como si no existiera.

Las observaciones completas están separadas en technical-review.json y en la vista legible. Son revisión posterior del coordinador contra los pasajes y el diálogo, no una pasada ciega ni aceptación del profesor. No se usaron para modificar las generaciones del ensayo. La aprobación humana recibida era del guion, no de las respuestas.

## Configuración, intentos previos y recursos

Se conservan dos intentos anteriores: run-20261101-212725 terminó sin llamadas por recursos; run-20261101-213912 generó tres candidatas con instrucciones genéricas y terminó en el deadline del revisor de A3 bajo memoria compartida. Detecté que el arnés no había seleccionado el perfil didáctico del chat, lo corregí y preservé los 261 archivos congelados de cada intento. Esos resultados anteriores no se mezclan con los doce del intento configurado ni se usan como fallos semánticos del chat correcto.

Tras la orden explícita «Si detén todo lo de T», se identificaron y detuvieron ocho procesos de T y sus hijos, incluido el backend que relanzaba Dolphin. No se borraron archivos ni resultados. T permanece detenido. ComfyUI experimental se mantuvo abierto y solo se pidió liberar modelos cuando su cola estaba vacía. La telemetría registra presión de memoria; no se atribuye a procesos ajenos ni se utiliza para clasificar rendimiento de modelos.

Los dos árboles GPU propios terminaron y sus recibos confirman el cierre. Comprobación final: ningún proceso T o worker GPU ORALIA restante; GPU 0 %, aproximadamente 1 GB ocupado por el entorno.

## Verificación y reproducción

601 pruebas del módulo course_dialogue superadas; una advertencia previa de Starlette/httpx. Black y Ruff focales conformes. Ruff global conserva diez diagnósticos y cero nuevos con comparación por archivo, código y mensaje, incluyendo multiplicidad. Los grupos históricos de 308, 140 y 22 archivos conservan todos sus hashes al cierre. Los 261 archivos congelados del intento se copiaron y verificaron en executed-code.

La ampliación de producción es optativa: WebReviewRounds acepta el perfil didáctico registrado para generación y mantiene el valor por defecto para experimentos anteriores. Las pruebas verifican que llega al frame del proveedor y que el revisor no lo hereda.

Desde la raíz ORALIA:

```powershell
$env:PYTHONPATH='src'
$env:PYTHONIOENCODING='utf-8'
.venv/Scripts/python.exe docs/audits/2026-11-01-autostudy-approval/run.py --execute
```

La aprobación solo vale para el hash del guion conservado. Sin aprobación o si cambian las preguntas, el arnés no carga modelos. Si faltan recursos espera hasta treinta minutos; no detiene otros proyectos automáticamente. Cada ejecución crea una carpeta nueva y conserva fallos y versiones. No hubo Reset, commits, publicación ni apertura de gates.
