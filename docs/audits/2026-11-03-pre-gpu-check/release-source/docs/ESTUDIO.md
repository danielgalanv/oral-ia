# Chat de autoestudio: estado y uso

La entrada actual es `/estudio`. Es una vista local de prueba docente con preguntas libres sobre requisitos de Ingeniería del Software, generación y revisión. No puntúa al alumno, no necesita rúbrica y todavía no se ha aceptado como tutor general para participantes. Voz y examen quedan fuera de esta comprobación del chat.

Internet es parte del alcance completo. Ya existe la conexión automática con una política explícita por actividad: insuficiencia local → aviso visible → adquisición acotada → contraste externo/docente → generación y revisión → «Información de Internet» y URL. El cableado está probado con dobles CPU; la eficacia semántica integrada queda pendiente de modelos reales. Sin política habilitada el arranque permanece local. No hay que entrar en `/web-inspect` para usar esta conexión.

Para una futura prueba real con GPU autorizada, el lanzador acepta `-WebPolicy`. El [catálogo de laboratorio v2](audits/2026-11-03-cpu-completion/policy-requirements-lab-v2.json) reúne cinco originales públicos de NASA, Sommerville y RFC. Es acotado, no todo Internet; adquirirlos no acredita por sí solo pertinencia ni respaldo:

```powershell
.\scripts\study-chat.ps1 -WebPolicy .\docs\audits\2026-11-03-cpu-completion\policy-requirements-lab-v2.json
```

Ese comando carga los modelos reales; no se ha ejecutado en la validación CPU actual. Se conserva el rechazo ante permiso retirado, conflicto o incertidumbre, sin completar de memoria ni calificar al alumno. El [informe de conexión](audits/2026-11-02-connected-web/report.md) detalla límites y pruebas.

## Preparar y arrancar

Desde PowerShell en `D:\Proyecto personal\ORALIA`, la preparación independiente de las inferencias es:

```powershell
.\scripts\study-chat.ps1 -PrepareOnly -NoBrowser
```

Construye una interfaz y un índice documental nuevos, con embeddings locales en CPU. No carga generador ni revisor, no usa GPU y no inicia el servidor. Informa de la carpeta creada bajo `.claude-scratch`; los intentos anteriores se conservan. Esta preparación no significa que el chat haya sido validado con modelos.

Cuando se vaya a probar con GPU disponible y autorizada:

```powershell
.\scripts\study-chat.ps1
```

Este segundo comando prepara su propio directorio y arranca el generador y revisor reales. Para reutilizar una preparación anterior, indicar la carpeta que imprimió el preparador:

```powershell
.\scripts\study-chat.ps1 -PreparedRun 'D:\Proyecto personal\ORALIA\.claude-scratch\study-chat-<carpeta-preparada>'
```

La reutilización es explícita y comprueba fuentes, código, entorno de recuperación e integridad del build/índice. Si cambiaron, rechaza el arranque y pide preparar de nuevo; no reconstruye o repara silenciosamente. `-PrepareOnly -NoBrowser -PreparedRun '<carpeta>'` comprueba la reutilización sin cargar generador/revisor ni abrir servidor. Preparaciones antiguas sin recibo `preparation.json` necesitan reconstruirse una vez. Cada arranque real recibe una carpeta de runtime y una copia de trabajo del índice nuevas: las escrituras internas de Chroma no alteran la preparación reutilizable. Copiar el índice no recalcula embeddings.

Abre la URL local anunciada, normalmente `http://127.0.0.1:8037/estudio`. `-Port` elige otro puerto; `-NoBrowser` evita abrir una pestaña. Si el puerto o recursos están ocupados no hay que cerrar procesos ajenos: elegir otro puerto o esperar. Ctrl+C detiene el servidor propio.

Los scripts requieren las dependencias ya instaladas. No instalan Node, pnpm, Python, modelos ni paquetes. La preparación restaura las variables de entorno de la consola al terminar, también si falla.

## Conversar

1. Pulsar Comenzar y escribir la pregunta. Intro inserta una línea; Enviar confirma la pregunta.
2. Preguntar de nuevo o pedir una aclaración/ejemplo. No hace falta un botón de cambio de tema: basta con formular la pregunta nueva.
3. Los mensajes distinguen Tú y ORALIA. Abrir Fuentes consultadas para ver referencias agrupadas por documento y página, sin repetir enlaces iguales. Identifica material consultado, no garantiza por sí solo cada afirmación.
4. Cancelar interrumpe una petición pendiente. Finalizar pide confirmación antes de descartar los mensajes y el borrador; Seguir estudiando o Escape conservan ambos.

El campo de pregunta permanece disponible mientras se recorre el historial. Ver últimos mensajes permite volver al final sin perder lo escrito. Durante una respuesta se muestra el tiempo transcurrido, sin inventar etapas internas de generación o revisión.

El chat no muestra instrucciones, JSON de transporte ni razonamiento interno del revisor. Los escenarios y cifras ficticios coherentes pueden ilustrar conceptos; no se consideran automáticamente hechos de la fuente o estándares obligatorios.

## Límites y recuperación

- La conversación es temporal en memoria, no una transcripción persistente recuperable tras cerrar. No se graba audio.
- El autoestudio normal no tiene cupo educativo de preguntas ni de llamadas acumuladas al revisor. Los ensayos pueden activar `-ExperimentalLimits` (doce preguntas/84 llamadas en el perfil revisado); esos cupos son controles del experimento, no restricciones del alumno. Se conservan los plazos técnicos de servicio/petición y las rondas acotadas por respuesta. Cerrar o recargar no renueva el plazo global del proceso; el prototipo actual tiene una disponibilidad temporal finita.
- Ante un corte transitorio, Recuperar conexión consulta la sesión vigente; no vuelve a enviar la pregunta. Un borrador nuevo sin enviar se conserva. Si no hay conexión válida, los mensajes visibles se purgan en hasta dieciséis segundos.
- La vista del alumno mantiene el latido en segundo plano para consultar fuentes. Suspensión del ordenador, cierre del navegador o limitaciones de temporizadores pueden interrumpirlo; no se promete recuperación después de caducar.
- El generador recibe las tres últimas interacciones. Aunque la vista conserve más mensajes, no es memoria ilimitada. El cambio de tema y algunos seguimientos se detectan mediante reglas conservadoras, no mediante una clasificación semántica general acreditada.
- El paquete actual tiene nueve documentos y 117 unidades disponibles, con cuarentena y huecos explícitos. No es toda la asignatura ni incluye INCOSE. Tablas y gráficos pueden requerir consultar el original.
- `/estudio` tiene conectada la ampliación web bajo política explícita, pero no ofrece todavía revisión semántica autónoma acreditada. El catálogo es acotado; respaldo y compatibilidad reales siguen pendientes. No debe presentarse como una fuente externa validada automáticamente.

## Comprobación y ensayo

El [guion docente vigente](audits/2026-11-03-pre-gpu-check/guion-gpu.md) reutiliza las doce preguntas aprobadas y distingue el modo normal sin cupo de los experimentos limitados. El guion fechado anterior se conserva, pero su expectativa de bloqueo tras doce preguntas no se aplica al autoestudio normal. La [preparación CPU](audits/2026-11-02-cpu-readiness/report.md) comprueba operación con proveedores simulados explícitos; no acredita calidad de respuestas reales.

La prueba integrada con el proveedor GPU sigue pendiente (T191). No se reemplaza por inferencias lentas en CPU ni por respuestas simuladas. La [auditoría documental](audits/2026-11-02-cpu-readiness/corpus-review.md) distingue disponibilidad, cuarentena y cobertura de los bloques. Los demostradores anteriores de [MVP](MVP.md) y [demo](DEMO.md) conservan sus instrucciones y alcance histórico; no son esta entrada de chat.

[Preparación del ensayo docente y registros descriptivos](piloto/README.md). Al pulsar Finalizar se pueden descargar JSON y Markdown con preguntas, respuestas mostradas, fuentes, conteos y repeticiones textuales. No hay audio, calificación o identificación automática de conceptos. La copia descargada permanece en el equipo; cerrar purga la sesión del programa. Las plantillas CSV manuales siguen disponibles.

El [catálogo de laboratorio v2](audits/2026-11-03-cpu-completion/policy-requirements-lab-v2.json) añade originales NASA y un capítulo de Sommerville en St Andrews a RFC 2119; no cambia las políticas existentes ni se activa por defecto. Para una futura prueba con modelos reales y GPU autorizada, pasar ese archivo mediante `-WebPolicy`. Las páginas largas se recuperan por pasajes literales con contexto, offsets y omisiones registradas, en vez de rechazarse solo por superar 6.000 caracteres. La selección no garantiza pertinencia ni verdad. [Informe CPU](audits/2026-11-03-cpu-completion/report.md).
