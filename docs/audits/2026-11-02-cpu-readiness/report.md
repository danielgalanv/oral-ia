# Preparación del chat en CPU — T194–T197

Se completan los cuatro bloques de CPU pedidos: uso con teclado/móvil, sesiones hasta cuota y cancelaciones repetidas, inventario documental y guion integrado. Se corrigieron cuatro defectos reproducidos. No se usó GPU ni se cargaron modelos generativos.

## Cambios y reproducciones

Solo se modifican dos archivos de producción: `apps/web/src/components/DiagnosticStudy.tsx` y `apps/web/src/styles.css`. Los demás cambios son pruebas, documentación y trazabilidad SpecKit. El [manifiesto](release-manifest.json) conserva 294 archivos de fuentes y pruebas en `release-source`.

1. **Foco perdido al comenzar y tras responder.** La [reproducción previa](browser-1793646529000/result.json) falla al pedir foco en el campo de pregunta después de Comenzar. La vista del alumno lo restaura al quedar disponible, sin robarlo al enlace de fuentes u otros controles. El formulario tiene nombre accesible propio, instrucciones sobre Enviar/Intro y registro de mensajes identificado.
2. **Borrador nuevo eliminado al recuperar una respuesta anterior.** La [reproducción previa](browser-1793646570264/result.json) espera la confirmación efectiva del servidor y demuestra que el texto editado desaparecía. Ahora se limpia solo si sigue siendo la pregunta entregada; se conserva un borrador nuevo sin enviarlo. No se modifica el texto académico.
3. **Desbordamiento móvil de preguntas sin espacios.** El [recorrido previo](browser-1793646735223/result.json) llega a doce respuestas y detecta desplazamiento horizontal a 320 px. Ahora los títulos y enlaces admiten corte visual de palabras largas; los botones del chat tienen un mínimo de 44 px de alto. No se recorta contenido.
4. **Latido detenido al pasar a segundo plano.** La [reproducción previa](background-1793647112568/result.json) muestra cero peticiones de estado al simular `visibilityState=hidden`. La vista del alumno sigue comprobando conexión también en ese estado, para que consultar una fuente no corte por sí mismo la sesión. Se conservan el plazo global, el lease de quince segundos sin peticiones válidas y la purga local desconectada. La política de la vista técnica anterior no cambia.

## Validación

- **716 pruebas Python aprobadas** en la [regresión](regression.log), incluidos los dos escenarios nuevos de `tests/integration/test_study_chat_endurance.py`. No es toda la suite del proyecto. Una advertencia de deprecación Starlette/httpx, sin fallos.
- **15 pruebas de interfaz aprobadas** en [ui-final.log](ui-final.log). [TypeScript](typescript-final.log), [ESLint](lint-final.log), [Black](black-check.log) y [Ruff focal](ruff-scoped-final.log) conformes. Ruff global mantiene diez diagnósticos existentes y cero nuevos, comparados con multiplicidad contra el baseline T090.
- La [comprobación automática final](cpu-smoke-1793647132183164900/result.json) pasa corpus, HTTP, construcción, visibilidad y navegador; cierra su servidor y comprueba el puerto libre. El [resultado de navegador](browser-1793647158623/result.json) conserva [captura móvil](browser-1793647158623/mobile-keyboard.png) y [escritorio](browser-1793647158623/desktop-recovery.png).
- El [log de visibilidad final](cpu-smoke-1793647132183164900/background.log) registra seis latidos, sesión vigente y cero cuota consumida tras simular segundo plano y esperar diecisiete segundos reales. Es visibilidad simulada, no una certificación frente a todas las políticas de suspensión de navegadores o del sistema operativo.
- Los [cortes de red finales](network-1793647198068/result.json) vuelven a pasar tras el cambio de heartbeat: confirmación perdida, respuesta preparada perdida, pregunta no recibida y purga local en hasta dieciséis segundos. Recuperar no genera otra respuesta.
- El [control de puerto ocupado](occupied-port.log) rechaza el arranque sin cerrar ni reutilizar el servicio existente.

El navegador usa Chromium local con GPU de renderizado desactivada y generador/revisor simulados explícitamente. Comprueba teclado para Comenzar, escribir, Enviar y Fuentes; el foco no se pierde al comprobar estado. Verifica entrada multilínea sin envío al pulsar Intro, conservación del borrador recuperado, doce mensajes, bloqueo al agotar cuota, Finalizar y diseño a 390/320 px y escritorio. No hubo peticiones externas ni errores JavaScript. Estas comprobaciones no constituyen una auditoría WCAG completa ni una prueba con lector de pantalla real.

La prueba HTTP extensa usa doce respuestas simuladas de más de cinco mil caracteres: conserva los doce recibos visibles, confirma sin duplicar y envía exactamente las tres últimas interacciones al proveedor. La cuota no se renueva al cerrar/reabrir; la decimotercera pregunta no llama al proveedor. Cuatro cancelaciones en curso no promueven texto cancelado al historial; la siguiente petición puede completarse.

Se conservan también intentos intermedios: una fixture de sesión larga necesitó declarar el plazo correcto de 600 segundos; un primer control de borrador comprobaba demasiado pronto, antes de la confirmación, y fue corregido antes de reproducir el fallo; otra ejecución de navegador reutilizó un presupuesto ya gastado y se repitió en una instancia propia nueva. Esos intentos no se cuentan como fallos académicos ni pruebas finales válidas. El formateador que quedó esperando en el sandbox se cerró por PID y comando identificados de esta tarea; la comprobación final terminó correctamente fuera de ese bloqueo.

## Cobertura documental

La [auditoría por bloque](corpus-review.md) y su [inventario](corpus-audit.json) verifican nueve documentos, 789 unidades declaradas: 117 disponibles y 672 en cuarentena. Los doce bloques tienen referencias existentes y disponibles; se conservan sus límites explícitos. Se comprobaron hashes de originales, extracciones, texto de unidades y previews declarados, sin discrepancias.

La cuarentena incluye portadas y material no seleccionado, además de limitaciones de extracción. No significa que se hayan perdido 672 páginas. INCOSE no está incorporado; los complementos NASA/Sommerville son subconjuntos. La auditoría no acredita cobertura de toda la asignatura, recuperación efectiva para cada formulación, apoyo semántico de una respuesta ni aceptación docente. No se retiró nada de cuarentena ni se alteraron originales.

## Repetición y siguiente prueba

Desde la raíz de ORALIA se puede repetir el smoke CPU:

```powershell
.venv\Scripts\python.exe docs\audits\2026-11-02-cpu-readiness\run_cpu.py
```

Usa el puerto 8051 solo si está libre, resultados nuevos, fixtures y un servidor propio con petición de parada. No instala dependencias, no inicia modelos y no requiere GPU. La regresión amplia de 716 pruebas y los cortes de red se documentan por separado; el smoke no los presenta como repetidos íntegramente.

El [guion integrado](guion-prueba.md) reutiliza las doce preguntas ya aprobadas, distingue funcionamiento de calidad académica y separa cancelación/recarga de la conversación docente para no gastar su cuota. Ejemplos ficticios coherentes, repetir una estructura útil y mejoras opcionales de estilo no son motivos automáticos de rechazo.

T194–T197 quedan completadas en CPU. **T191 sigue abierta**: falta comprobar el chat integrado con 14B y Qwen3 reales. No se modifican prompts, severidad del revisor, modelos, gates ni publicación. Una limitación práctica permanece explícita: la petición al generador contiene las tres últimas interacciones; no ofrece memoria semántica ilimitada aunque la vista conserve el historial de la sesión. Las restricciones de tablas/gráficos y de suspensión efectiva del navegador siguen vigentes.

## Preservación y cierre

Las [comprobaciones finales](final-checks.json) verifican los grupos históricos de 308, 140 y 22 archivos, sin cambios de hashes; no se suman como archivos únicos. Todos los servidores propios de esta ronda están detenidos y el puerto 8051 está libre. No hubo cambios de datos habituales o de demo, descargas, migraciones, Reset, commits, GPU ni inferencia nueva.
