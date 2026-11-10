# Prueba012

## Entrada actual de chat — 02-11-2026

Consultar [uso actual, preparación CPU y límites](../../docs/ESTUDIO.md). La vista sencilla es `/estudio`, mediante `scripts/study-chat.ps1`. `-PrepareOnly -NoBrowser` solo prepara interfaz e índice en CPU, sin generador ni revisor. La inferencia integrada real se valida con GPU disponible; no se repite en CPU como sustituto. Las secciones siguientes conservan experimentos y entradas anteriores y no implican que todas sean el modo vigente.

## Comparación pedagógica parcial — sin promoción de perfil

`pedagogical_profile="pedagogy-v1"` es una extensión general optativa; el valor por defecto `baseline` conserva su instrucción. No implica respaldo semántico ni disponibilidad para participante. Los ejemplos hipotéticos coherentes pueden inventar valores y condiciones: el respaldo documental se exige al principio y la interpretación, no a cada detalle del escenario.

[Resultados y decisión](evidence/pedagogical-comparison-recovery-run-v1/report.md) · [Texto realmente mostrado](evidence/pedagogical-comparison-recovery-run-v1/transcript.md) · [Salidas crudas completas](evidence/pedagogical-comparison-recovery-run-v1/raw-candidates.md).

La comparación de tres casos se interrumpió: A-baseline completo, dos turnos completos de A-mejora y su ejemplo truncado. B/C no se ejecutaron. No se promueve el perfil ni se repite para completar artificialmente el banco; publicación y gates permanecen cerrados. Los preparadores y ejecutores conservan cada intento en directorios propios y rechazan sobrescritura.

## Referencias documentales legibles — decisión del 27-10-2026

El recorrido RAG actual presenta «Fuentes consultadas» con documentos y páginas útiles añadidos por el host. No exige IDs entre corchetes ni citas por frase al modelo. La lista identifica documentos entregados al generador, no respaldo semántico verificado. Las unidades y trazas exactas permanecen internas; publicación y gates sustantivos siguen cerrados.

[Cambio, pruebas y resultados de tres controles nuevos](evidence/readable-reference-run-2026-10-27/report.md) · [Transcripción real sin formato técnico obligatorio](evidence/readable-reference-run-2026-10-27-resource-recheck/transcript.md).

La primera ST01 sigue conservada bajo su contrato anterior y no se aprueba retrospectivamente. El ejemplo nuevo tiene problemas de justificación separados de la presentación. El ensayo acotado ya terminó: estos enlaces permiten revisarlo, no autorizan repetir variantes o abrir participante.

## Avance ejecutable solo CPU: conversación RAG de laboratorio

[Transcripción legible de seis turnos](evidence/cpu-rag-progress-v1/conversation-final-transcript.md) y [recibos](evidence/cpu-rag-progress-v1/conversation-final.json): política/SQL/PDF reales de solo lectura y catálogo vigente de 139 páginas; proveedor, alcance y evaluadores **simulados**. Demuestra cableado y estado, no capacidad pedagógica ni suficiencia semántica.

```powershell
.venv\Scripts\python.exe -m scripts.run_cpu_conversation_lab --name otra-demostracion-cpu
```

El nombre debe ser nuevo: no sobrescribe demostraciones previas. No importa proveedores de modelos ni carga pesos o embeddings. La primera demostración conserva un bloqueo de cambio de tema posteriormente reproducido y corregido; `conversation-final` conserva la ejecución posterior. [Medición CPU de seis preguntas nuevas](evidence/cpu-rag-progress-v1/report.md): controles y pasajes originales congelados antes de medir, sin utilizar reserva.

```powershell
.venv\Scripts\python.exe -m scripts.evaluate_cpu_retrieval --profile bilingual-v1 --output otra-medicion.json
```

La revisión simulada no habilita participante, G2 ni publicación. La prueba GPU mínima preparada sigue sin ejecutar y requiere confirmación expresa de disponibilidad, aunque transcurran las tres horas comunicadas.

**Coordinación GPU vigente (26-10-2026):** antes de cargar pesos, ejecutar inferencias o cualquier prueba GPU, describir prueba, modelo, duración estimada y presupuesto, y esperar confirmación explícita de disponibilidad del usuario. La autorización general anterior y la telemetría por sí solas no sustituyen esa coordinación. Mantener telemetría antes/durante/después una vez confirmada; no tocar procesos ajenos. El último diagnóstico tuvo uso concurrente confirmado por el usuario: conservar su salida, sin comparabilidad de rendimiento ni conclusión general del modelo. Trabajo offline CPU permitido solo sin inicializar CUDA; no iniciar otro ensayo por defecto.

La entrada actual011 sigue siendo `.\scripts\course-study.ps1` (extractiva). La sucesora se prepara por separado como banco de candidatas, con `.\scripts\course-dialogue.ps1` una vez implementado. Solo entradas sintéticas de evaluación, sin participantes ni datos de alumnos. Qwen local ya instalado, no descargas. No abrir la demo habitual ni publicar candidatas.

Examinar transcriptos reales de primeras explicaciones y seguir según la respuesta efectiva. Salida0 o JSON válido no acredita utilidad. Publicación generativa sigue cerrada hasta G2 suficiente; revisión docente/humana y voz son comprobaciones separadas. Comandos finales medidos se completarán con evidencia.

## Inspección interactiva implementada

Desde PowerShell en el workspace:

```powershell
.\scripts\course-dialogue.ps1 -InspectCandidates -ControlledDrafts
```

Solo preguntas ficticias. Modelo local7B/NF4 propone objetivo/acto; el texto mostrado procede del paquete técnico de77unidades/7objetivos pendiente de revisión docente. No es una respuesta libre del modelo ni una sesión participante. No se conserva la entrada por defecto. `/estado` muestra objetivo/pregunta pendiente sin nota; `/fuentes` enumera referencias del último borrador; `/salir` o EOF detienen el worker propio y liberan el lock. No hay Reset ni servicios TCP nuevos.

Requiere el runtime CUDA existente `D:\ai-toolkit\venv\Scripts\python.exe` y el snapshotlocal Qwen2.5-7B indicado en cached_transformers.py; no instala ni descarga recursos. Carga con límite90s y avisos cada10s; inferencia explícita30s. Si faltan recursos o memoria se informa del rechazo, sin cambiar de modelo silenciosamente. La ruta libre separada usa `-InspectCandidates -NaturalProbe` (1.5B) o el proveedor explícito Ollama; no combinar NaturalProbe con ControlledDrafts.

La serie real de tres repeticiones de desarrollo falla al sustituir la explicación de conflictos por una pregunta. Véase [revisión](evidence/controlled-review-context.md). Este comando permite inspeccionar el trabajo pendiente; no habilita el tutor ni acredita utilidad.

## Inspección experimental por ámbito — contrato4.0.0

```powershell
.\scripts\course-dialogue.ps1 -InspectCandidates -ControlledDrafts -DraftModel 14b-nf4 -SemanticVersion 3
```

Opción explícita; el comando anterior mantiene su comportamiento por defecto.
El paquete actual contiene83unidades/7objetivos/3relaciones, todas pendientes de
revisión. La clasificación de ámbito y las etapas de intención comparten30s;
no hay reintentos ni cambio automático de modelo. Los diagnósticos expuestos
registran6/9parejas esperadas con Qwen3 y7/9con14B: no constituyen aceptación.

La preparación docente separada ya existe en
`.oralia-course-dialogue-lab/review-1259d85b0ecc`:3documentos,83borradores,
0sesiones, actividad en borrador. Puede verificarse/reutilizarse mediante
`.venv\Scripts\python.exe -m oralia.course_dialogue.review_preparation` en un
proceso nuevo. No publica ni crea sesiones. Conserva el entorno previo77 y los
bytes de los tres PDF seleccionados. El recorrido participante todavía no está
integrado; no usar este comando como acceso de participante ni aprobación docente.

## Configuración semántica docente separada

```powershell
.venv\Scripts\python.exe -m oralia.course_dialogue.review_preparation --semantic-policy
```

Ejecutar en un proceso nuevo. Requiere la selección PDF ya verificada de la
revisión ordinaria; copia exactamente esos bytes y no regenera PDF. Prepara o
comprueba idempotentemente `.oralia-course-dialogue-lab/review-dcf4dd1c03e0`,
con política `guided-semantic-candidate/v1`, 83 unidades en borrador y los modos
duda y explicación guiada. No publica, no configura un proveedor, no crea
sesiones y no sustituye ninguna de las dos revisiones anteriores. La segunda
ejecución medida tardó 2,81 s y conservó tres documentos y 83 unidades.

El enlace optativo por API normal está probado con material ficticio e
intenciones simuladas, incluida conservación, cierre confirmado, dos formatos
de exportación, borrado y sesión nueva sin contexto heredado. El curso real
sigue no disponible: falta G2 suficiente y revisión docente explícita.

La serie `transfer-readable-goals-qwen3-exposed` conserva 30 turnos del modelo
local y 30 borradores técnicos, pero 0/6 conversaciones supera todos los
observadores. El JSON válido, las fuentes presentes y las pruebas HTTP no
acreditan pertinencia ni utilidad con personas. El árbol propio del modelo
quedó detenido, según su recibo de limpieza.

## Comparación de chat A/B/C y política de GPU

El ensayo nuevo está en `evidence/chat-comparison-extended-first/` y su protocolo previo en `evidence/chat-comparison-extended-protocol.json`. A usa el selector/renderer de borradores técnicos; B contesta sobre páginas originales; C comparte B y añade guía pedagógica. Son candidatas sintéticas, no respuestas habilitadas. El primer piloto y el seguimiento interrumpido también se conservan. La revisión técnica independiente y la investigación del colapso de tiempo se enlazan desde `evidence/chat-comparison-report.md`.

Mientras ComfyUI u otro proceso comparte la GPU, no se puntúa capacidad o rendimiento con inferencias afectadas. Antes de cualquier futura ejecución debe comprobarse propiedad de procesos, memoria y uso de GPU, y registrarse telemetría antes/durante/después; un instante libre no acredita comparabilidad. No cerrar procesos ajenos ni elevar el plazo de30s. Los deadlines observados sin aislamiento suficiente son resultados de ejecución no concluyentes para capacidad. Las pruebas deterministas pueden ejecutarse con `CUDA_VISIBLE_DEVICES=-1`. G2, SC001 y la revisión docente siguen pendientes.

Después de que el usuario confirmara la GPU libre, se hicieron dos ensayos completos nuevos A/B/C con telemetría previa, periódica y posterior. [Resultado y diálogos](evidence/chat-comparison-gpu-free-report.md). El primer desarrollo tuvo8/8salidas completas por variante, con fallos didácticos observables; la revisión única de V2 retrocedió a4/8B y5/8C en la conversación mostrada. La condición de parada congelada impide consumir la reserva o seguir ajustando prompts en esta serie. Una corrección estructural posterior tiene solo prueba determinista y auditoría poshoc, no una conversación real nueva. ComfyUI continuó sin intervención. G2/SC001 siguen pendientes.

La [captura diagnóstica posterior del V2 final](evidence/chat-v2-final-capture-report.md) sí ejecutó una conversación nueva de ocho entradas por variante: A8/B6/C7 candidatas completas, con ejemplo B ausente por deadline y GPU variable. Activó otra condición de parada y no consumió reserva. El [arreglo determinista posterior](evidence/chat-v2-context-echo-fix-report.md) separa tema/petición y filtra ecos exactos del campo `question`; pasó174pruebas del módulo antes de su primera conversación real. Ninguno de estos datos autoriza G2/SC001 ni contenido participante.

Después de liberar la GPU, la [captura con esos bytes corregidos](evidence/chat-v2-context-echo-capture-report.md) produjo A/B/C8/8 salidas completas, con ejemplo mostrado, consulta limpia y ecos de `question` omitidos. La revisión técnica inicial encuentra problemas de contenido y no equivale a doble revisión independiente; la reserva permanece cerrada. Ningún resultado valida utilidad humana o voz real.
