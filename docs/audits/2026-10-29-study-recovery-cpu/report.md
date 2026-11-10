# I5 acotado: continuar tras límites de búsqueda

Inicio documental: 29-10-2026. Implementación y validación: **30-10-2026**, exclusivamente CPU. T110–T113 completadas en el alcance descrito; no se cierra I5 completo ni Feature 012.

## Comportamiento incorporado

El recuperador diferencia una pregunta que por sí sola supera el límite efectivo del encoder de una pregunta que cabe pero cuyo contexto acumulado no. El primer caso pide dividir/reformular; el segundo propone precisar el referente o activar expresamente «Cambiar de tema» para una duda independiente. No se recortan preguntas o referencias para hacerlas caber.

La recuperación sin pasajes tiene también un mensaje concreto: reformular o consultar documentos, sin declarar que el tema esté fuera de la asignatura. No se interpreta una selección no vacía como prueba de suficiencia.

En esos tres casos no se llama al generador, no se reserva cuota nueva, no se añade una respuesta ficticia al historial y no se cierra la conversación. Se conserva la pregunta editable y el último texto confirmado. Una nueva pregunta válida continúa normalmente; no hay reenvío automático. La retirada o modificación de fuentes sigue purgando según los controles anteriores.

Son mensajes operativos fijos del host, no respuestas académicas predefinidas. La generación académica, sus prompts, los modelos y los permisos de publicación no cambian.

## Reproducción y pruebas

Las pruebas nuevas reprodujeron cinco fallos antes de la corrección y un control positivo ya pasaba. El primer borrador de un doble de recuperación vacía omitía identidad/estrategia; se corrigió el doble para representar un resultado válido antes de conservar la ejecución roja definitiva. No se debilitó la comprobación de identidad para hacer pasar la prueba.

- **79 pruebas Python aprobadas:** capacidad efectiva, rechazo antes de embeddings, historial, cuota, reintentos con ID nuevo, duplicados, continuidad, retirada de fuentes, errores, límites generativos y binding.
- **12 pruebas UI aprobadas:** mensajes accionables, formulario, reloj, cuota y errores; son política/SSR CPU, no inferencia semántica.
- TypeScript, Vite y ESLint aprobados. El build nuevo está en `web-dist/`, sin sustituir los builds anteriores.
- Black conforme y Ruff sin hallazgos en los archivos modificados. Ruff global `src tests`: diez diagnósticos existentes y cero nuevos. Comparación mediante Counter de ruta relativa/código/mensaje, conservando multiplicidad, con `chat-comparison-ruff-current-final.json`; no se afirma Ruff global limpio.

Registros: `red-python.log`, `red-ui.log`, `green-python.log`, `green-ui.log`, `tsc.log`, `build.log`, `lint.log`, `ruff-global.json` y `final-checks.json`.

## Navegador real, sin GPU

Se sirvió el frontend actualizado con **recuperación dense real en CPU** sobre el paquete v2 y un proveedor **FIXTURE_CPU_NO_LLM**, visible como tal en la interfaz. La fixture no emite respuestas académicas ni demuestra calidad del LLM.

1. Enviar «¿Qué es un requisito?» y confirmar una salida de transporte: cuota usada 1.
2. Enviar una entrada repetitiva de prueba que excede la capacidad. Aparece el mensaje de pregunta demasiado larga; el primer turno continúa visible, el campo sigue editable y la cuota permanece en 1.
3. Reformular con «¿Puedes explicar qué es un requisito funcional?». Se muestra otra salida fixture con los dos mensajes del primer turno en contexto: cuota 2.
4. Enviar una pregunta que cabe sola pero, junto con las dos preguntas previas, excede el límite. Aparece el mensaje de contexto demasiado largo; cuota permanece en 2.
5. Mantener esa misma entrada y activar «Cambiar de tema». Ahora la búsqueda cabe y la salida fixture tiene cero mensajes anteriores: cuota 3.
6. Pulsar «Cerrar inspección y descartar» y verificar que desaparece el contenido temporal.

La secuencia de cuota real fue **1, 1, 2, 2, 3**. Hubo tres salidas de transporte y dos rechazos operativos antes de generación; no son cinco respuestas académicas. Los trece recibos `browser-001.json`–`browser-013.json` conservan estados y solicitudes. La ausencia de pasajes se probó con dobles válidos y mensajes UI: **no se anuncia una recuperación dense vacía real ni detección de insuficiencia semántica**.

El control del navegador se recuperó reiniciando únicamente el kernel de automatización que había quedado sin conexión en la ronda anterior; no se hizo Reset de ORALIA ni de datos. Se usó la skill SpecKit Implement para el bloque acotado y el control de navegador para esta comprobación. No se iniciaron subagentes ni otros chats.

## Integridad y parada

El cambio de hash en `retrieval.py` exige otra identidad. Se creó únicamente `isolated-index/` dentro de este dossier; no se reescribió ni reconstruyó un índice histórico. Su identidad confirma `device: cpu`. No se cargó un modelo generativo, inicializó CUDA ni consultó/modificó la GPU.

Los 308 archivos de corpus/recibos históricos del baseline de preservación siguen iguales. El dossier `before/` conserva los siete archivos originales anteriores a estos cambios, con su manifiesto. Los módulos modificados son `retrieval.py`, `study_errors.py`, `study_lab.py` y `studyRuntime.ts`; además se actualizaron pruebas y los artefactos SpecKit de este bloque. Sin SQL/migraciones, descargas, cambios de fuentes, datos de alumnos, commits ni Reset.

El servidor propio de prueba (PID 45140, puerto 8037) terminó **limpiamente con código 0** mediante su archivo de control; Uvicorn confirmó `Application shutdown complete`. No quedan ese PID ni listener en 8037. No se detuvieron procesos ajenos.

## SpecKit y límites siguientes

Prerequisitos: Feature 012; checklists `capacity-decision` 8/8, `final-local-candidate` 9/9 y `requirements` 12/12, sin pendientes. No existe `.specify/extensions.yml`, por lo que no hay hooks previos/posteriores que ejecutar. Workspace sin Git; ignores existentes verificados. El alcance autorizado es T110–T113, no todos los pendientes históricos. La comprobación acotada de spec/plan/contrato/tareas conserva FR-014/017, las puertas semánticas y T090/T150.

Queda fuera de esta entrega decidir si pasajes recuperados bastan académicamente, resolver sus contradicciones o declarar un tema excluido. Esas capacidades no se obtienen de un error de capacidad o de que el buscador devuelva resultados. Tampoco se reevaluó el contenido del modelo con esta prueba CPU.

## Evidencia visible

- [Límite de contexto con conversación conservada](context-limit.png)
- [Límite de pregunta](recoverable-limit.png)
- [Estado visible tras continuar](continued-visible.txt)
- [Controles finales y comparación de preservación](final-checks.json)
- [Contrato](../../../specs/012-conversational-course-study/contracts/study-recovery-addendum.md)

Para repetir la comprobación, usar una carpeta y un índice de prueba nuevos; los recibos se abren en modo exclusivo y no se reutiliza el dossier para sobrescribir esta evidencia.
