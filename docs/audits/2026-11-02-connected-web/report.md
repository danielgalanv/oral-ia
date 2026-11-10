# T205 — Internet conectado al chat, validación CPU

La conexión está implementada en `/estudio`. Reutiliza adquisición pública, generador 14B, revisor Qwen3 con razonamiento y rondas de corrección existentes. **Esta entrega verifica cableado y controles técnicos con dobles explícitos: cero inferencias de modelos reales, cero uso de GPU y cero peticiones reales a Internet.** No acredita todavía el acierto de los juicios semánticos del revisor ni completa el autoestudio.

## Recorrido implementado

1. El RAG local y el historial realmente mostrado llegan a un control consultivo de suficiencia. Solo `needs_web`, dentro de un concepto autorizado y con política vigente de autoestudio, inicia ampliación. `sufficient` conserva la vía local; incertidumbre o exclusión no acreditada no se convierten en «no necesitas estudiar esto».
2. El servidor espera que la interfaz haya mostrado el aviso **«Voy a consultar información de Internet para completar esta explicación»**. La confirmación es automática tras renderizado visible, sin añadir un botón o una aprobación manual por pregunta. Cancelar antes de esa confirmación impide buscar y descargar.
3. Se reutiliza `WebEvidence`: vocabulario académico del host, catálogo público autorizado, HTTPS acotado, restricciones de destinos/redirecciones/bytes/plazos y procedencia. No se envían a Internet la pregunta libre, el historial ni los PDF docentes. La búsqueda actual es un catálogo curado por concepto, no un buscador general de toda la web.
4. Qwen3 recibe un control de respaldo/pertinencia de la evidencia externa. Otro control contrasta sus proposiciones con **todos los originales docentes activos**, por lotes explícitos; no solo con las páginas recuperadas inicialmente. En el paquete actual son 89 páginas docentes disponibles, distribuidas en siete lotes. Las referencias públicas archivadas no se etiquetan como originales del profesor. Páginas en cuarentena quedan excluidas.
5. Si los controles responden favorablemente, los pasajes externos entran en la misma petición del generador y en las rondas existentes de revisión/corrección. Un conflicto, una salida incompleta o una decisión incierta bloquean esa explicación. El acuerdo del modelo sigue siendo una señal consultiva cuya eficacia requiere medición real.
6. El host muestra **«Información de Internet»**, título, entidad y URL completa, separado de **«Fuentes consultadas»** del material local. Conserva internamente procedencia, hash, captura, controles y versiones; no expone el trace privado al alumno.
7. Se revalidan permiso, actividad y fuentes durante el recorrido y antes de lectura, recuperación o confirmación de una respuesta externa pendiente. La retirada durante la revisión tampoco entrega el texto generado. Las respuestas ya mostradas mantienen su historial durante la sesión y se puede continuar localmente sin nuevas adquisiciones. El cierre purga la sesión efímera; recargar la página también la descarta deliberadamente.

La bibliografía del revisor es opcional e informativa. **No se exige copiar hashes, IDs internos o citas por frase para aceptar su juicio.** Documento/página o URL bastan para orientar; ni un formato bibliográfico correcto ni su ausencia prueban la corrección académica. Se mantienen las instrucciones de tolerancia a ejemplos ficticios coherentes, repetición, estilo y mejoras opcionales, sin convertirlas en defectos sustantivos.

## Cambios

- `study_web_flow.py`: composición del recorrido y controles, comparación docente por lotes y procedencia externa.
- `web_control_request.py`, `web_review_frame.py`, `cached_transformers.py`: perfil registrado `web-control/v1` sobre el revisor Qwen3 existente, validación de mensajes efectivos y confirmaciones del worker. No usa el renderer académico de generación para clasificar.
- `reviewed_study.py`, `study_lab.py`, `study_lab_api.py`: integración por sesión, aviso/confirmación, cancelación, atribución pública, trace privado y bloqueo de entregas pendientes retiradas.
- `web_evidence.py`: adquisición independiente por turno. Conserva el plazo histórico de inspección manual, pero evita que el plazo de descarga invalide una generación posterior. Cada adquisición sigue acotada; no añade un cupo educativo acumulativo al alumno.
- `DiagnosticStudy.tsx`, `studyRuntime.ts`, estilos: aviso previo, errores identificables y fuentes legibles en móvil/escritorio. No añade cambio manual de tema ni opciones técnicas al alumno.
- `study-chat.ps1`: parámetro `-WebPolicy`, conservando el arranque local sin política habilitada. Spec/plan/tasks y guía actualizados; T205 registra solo este incremento técnico.

El [manifiesto](release-manifest.json) y `release-source` conservan los 18 archivos finales de código, pruebas y artefactos activos incluidos en esta entrega.

## Evidencia medida

- [Regresión final](final-regression.log): **766 pruebas aprobadas**, una advertencia de deprecación Starlette/httpx ya existente. Incluye diálogo, adaptadores, sesión/API, límites, recuperación, preparación y adquisición/conexión web. No es toda la suite del proyecto.
- [Pruebas dirigidas](corrected-tests.log): **119 aprobadas** en una revisión anterior a los dos últimos controles de retirada/plazo; su ámbito se superpone con la regresión final y no debe sumarse como casos únicos.
- [Interfaz](ui-tests.log): **18 aprobadas**; TypeScript, [build](build.log) y [ESLint](lint.log) conformes.
- [Navegador final](browser-004/result.json): dos adquisiciones simuladas solo después del aviso visible; URL y atribución externa; seguimiento; retirada de permiso; tercer turno local sin nueva adquisición; sin desbordamiento horizontal móvil; cierre confirmado. Tres generaciones simuladas, ninguna inferencia real. Sin errores JS ni peticiones externas reales. [Móvil](browser-004/mobile-internet.png) y [escritorio](browser-004/desktop-after-revocation.png).
- El adaptador de producción, con transporte simulado, valida el nuevo perfil y las confirmaciones de razonamiento/renderer; no solo se prueba una llamada directa al doble del revisor.
- Negativos: conflicto, incertidumbre, contenido con instrucciones detectadas, cancelación antes del aviso, retirada durante descarga/revisión y entre generación y entrega por cuatro rutas; ninguna salida no autorizada se incorpora al historial. La prueba de plazo envejece el reloj de adquisición tras descargar y verifica que no caduca por ello una generación posterior.
- [Comprobaciones finales](final-checks.json): Ruff **10 existentes, 0 nuevos**, comparación estructural con multiplicidad. Los grupos históricos de **308, 140 y 22** archivos conservan hashes; no se suman como archivos únicos. Puerto 8059 libre y servicios propios detenidos. Black conforme. Sin Reset, commits o detención de procesos ajenos.

## Fallos conservados

Los primeros controles reprodujeron códigos públicos web no registrados y el rechazo del nuevo tipo por la validación tipada del adaptador. Se corrigieron y se verificaron las rutas finales. Una edición posterior colocó metadatos docentes en la construcción de evidencia externa: Ruff y las pruebas detectaron la variable incorrecta; el [fallo](final-tests.log) se conserva y la [regresión final](final-regression.log) pasa tras corregirlo.

El primer arranque del fixture falló por PYTHONPATH antes de abrir servicios. Dos recorridos de navegador fallaron por errores del montaje: se esperaba conservar una sesión efímera después de recargarla y se intentó retirar el permiso por una ruta de fixture bloqueada por el filtro HTTP existente. Se corrigieron esos montajes, sin cambiar la política de purga o el filtro de producción. `browser-001`, `browser-002` y sus logs se conservan; `browser-003` y `browser-004` pasan.

## Política y uso posterior

[Política RFC de laboratorio](policy-rfc-lab.json): habilitada explícitamente para esta actividad de autoestudio, reutilizando una fuente ya adquirida en el proyecto. Su lectura se comprobó sin descargar. Es un catálogo de una fuente con cobertura limitada; no autoriza examen, navegación libre o incorporación automática sin controles. No se instala como política por defecto.

Cuando se autorice una prueba real con GPU, el comando documentado es:

```powershell
.\scripts\study-chat.ps1 -WebPolicy .\docs\audits\2026-11-02-connected-web\policy-rfc-lab.json
```

**Ese comando carga modelos reales y no se ejecutó aquí.** Una preparación anterior al cambio puede quedar obsoleta por su fingerprint; se crea una nueva sin Reset ni alteración del corpus. `-PrepareOnly -NoBrowser` sigue preparando sin generador/revisor ni servidor.

Para reproducir la conexión HTTP en CPU sin modelos ni red pública:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/integration/test_connected_web_chat.py -q --basetemp .claude-scratch/pytest-connected-web-reproduce-001
node --test tests/unit/test_study_runtime_ui.mjs
```

## Límites y siguiente comprobación

Los controles están cableados al proveedor real, pero sus decisiones en esta entrega son fixtures. Falta ejecutar el recorrido con modelos reales y revisar respuestas completas bajo el criterio docente ya acordado, incluyendo un caso suficiente local, otro ampliado, un seguimiento y un conflicto/insuficiencia reales. **T191 y los pendientes semánticos T117/T152/T157 siguen abiertos; G2, SC001 y publicación no se aprueban.**

La adquisición actual admite HTML/texto públicos, con catálogo y destinos autorizados; no supera restricciones de acceso ni incorpora PDF web por esta vía. Se rechazan duplicados detectados y documentos con patrones de inyección, sin afirmar que el detector garantice seguridad frente a toda instrucción maliciosa. Textos externos de más de 6.000 caracteres se excluyen y se anotan; más de 8.000 caracteres externos conjuntos no entran al generador. No se recortan silenciosamente. Una página docente individual que exceda el lote de 8.000 caracteres exige revisión pendiente. Estos límites pueden dejar una consulta sin evidencia; no son un fallo académico del alumno ni una demostración de exclusión del temario. La selección de fragmentos largos y la ampliación del catálogo no quedan acreditadas por esta prueba.

No hay evaluación del alumno, rúbrica, registro de audio o persistencia nueva de conversaciones. La autorización de Internet y su necesidad para completar el autoestudio se mantienen; el resultado CPU acredita su integración técnica, no su utilidad académica final.
