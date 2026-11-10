# Cuatro mejoras del autoestudio — 3/4 de noviembre de 2026

El recorrido técnico está implementado y medido con Qwen2.5-14B NF4 y Qwen3-8B con razonamiento. El banco aprobado produjo **12/12 respuestas mostradas**. Esto no significa que las doce fueran semánticamente perfectas: B4 reprodujo una denominación incorrecta y se corrigió después con la comprobación documentada abajo. La revisión automática general sigue siendo falible. Feature 012, la aceptación docente, la utilidad con alumnos y la publicación permanecen abiertas.

## Cambios y evidencia

| Bloque | Resultado concreto | Límite |
|---|---|---|
| Contrato del control | Decisión finita tras razonamiento, sin bibliografía generada ni recorte o transformación de etiquetas. Frames y presupuestos se comprueban en el worker. | Una salida válida puede contener una decisión semántica incorrecta. |
| Responder frente a confirmar la premisa | El alcance se decide por separado. Con pasajes locales se genera y revisa el borrador real antes de intentar ampliarlo. B2/B3/C2 se mostraron dentro de la conversación completa. | No basta un clasificador de suficiencia previo: v3/v4 conservaron falsos bloqueos. |
| Ejemplos y revisión | Perfil optativo de ejemplos con premisas explícitas. Se descartó la búsqueda de contraejemplos que repitió la falsa dependencia cifrado/autenticación. Se añadió una comprobación terminológica estrecha con testigo literal de fuente. | No es un verificador general de hechos o razonamiento. Una defensa puntual no acredita transferencia general. |
| Internet | Catálogo versionado y pertinente, adquisición HTTPS real, aviso, fuentes separadas y contraste de 89 unidades docentes en siete lotes, sin reducir esa cobertura. Dos positivos completos. | Es consulta de originales autorizados y enlaces permitidos, no un buscador general de toda la web. |

Los límites siguen siendo **180 s/etapa y 600 s/turno**. El banco final usa el runtime normal de 1.800 s; no se alargó para pasar. Los perfiles históricos se conservan. La entrega al participante sigue cerrada y las respuestas son para inspección docente.

## Defectos de funcionamiento encontrados

1. El control anterior mezclaba formato, bibliografía, alcance y la posibilidad de contestar. Sus decisiones no eran suficientemente fiables para impedir que el generador intentase una explicación con fuentes locales. El flujo nuevo conserva una decisión de alcance explícita y revisa el borrador real; no convierte una etiqueta fallida en otra.
2. El catálogo enviaba validación de requisitos a la página de **validación del producto**, trazabilidad al resumen del capítulo 6.0 y definición/tipos a RFC 2119. Se sustituyeron por contexto de requisitos y fuentes más pertinentes. NASA documenta la trazabilidad en [6.2 Requirements Management](https://www.nasa.gov/reference/6-2-requirements-management/); el complemento de [Sommerville](https://software-engineering-book.com/web/requirements-standard/) describe requisitos funcionales, no funcionales e interfaces. Su referencia a IEEE 830-1998 se identifica como histórica, no como norma vigente.
3. En el ensayo histórico lento, el primer lote de contraste generó 540 tokens y tardó 136,625 s. El replay dio el mismo texto final y el mismo número de tokens en 29,217 s. La demora se encontraba en la llamada de inferencia, no en la descarga ni en una respuesta más larga. **La causa histórica de esa degradación GPU no quedó demostrada.** Liberar caché inactiva recuperó memoria, pero los ensayos on/off no demostraron una mejora de latencia. Véase [comparación](./latency-forensics.json).
4. La primera variante local primero dejó pasar una receta ajena al curso y el revisor la aceptó. Se conserva en run-002. Se añadió alcance de actividad explícito, separado de suficiencia y permiso de Internet. Los dos controles de cocina/geografía posteriores emitieron avisos del host antes de llamar al generador académico.

## Resultados que no deben confundirse

| Ejecución | Resultado |
|---|---|
| v3, 03-11 | 10/12 entregas; B3/C2 bloqueadas; suficiencia falsa con pasajes vacíos rechazada por el host. Contraejemplo C4 incorrecto. |
| v4, 04-11, run-001 | 9/12 entregas; mantuvo falsos bloqueos y el catálogo anterior no aportó respaldo suficiente al positivo web. No se promovió como filtro de suficiencia. |
| Local primero, run-002 | Tres regresiones resueltas y web útil en 339.144 s; receta fuera de alcance mostrada indebidamente. Esta variante sin alcance no se promovió. |
| Alcance separado, run-003 | Tres regresiones resueltas; dos avisos fuera de actividad sin generación académica; web útil en 339.214 s. |
| Banco final, run-004 | 12/12 respuestas realmente mostradas y contrastadas con el DOM. Tres conversaciones completas, no historial reconstruido. B4 contenía el error terminológico conservado. |
| Corrección B4, run-005 | 148.323 s; dos versiones, una reparación real y revisión posterior. Solo se restauró contexto previamente mostrado; no es una nueva conversación ciega. |

Los controles de alcance aislados dieron cuatro etiquetas correctas de cinco llamadas ejecutadas. U1 («¿Y eso?» sin contexto) no obtuvo la etiqueta esperada; la ruta real lo intercepta antes del modelo con la petición de referente, comprobada en CPU. P2 no llegó al modelo por un tipo incorrecto de historial en el runner privado; se conserva como fallo del runner, no como fallo semántico. La misma pregunta con historial sí pasó por la integración real B2. No se cuentan como seis aciertos.

El primer replay auxiliar P1/P2 del 03-11 también falló antes de revisar: un adaptador fixture tenía un valor fuera del enum. No acredita capacidad ni incapacidad del modelo. Todas las salidas y fallos originales permanecen.

## B4: comprobación terminológica, no cambio silencioso

La página 73 de **5 - Requisitos.pdf** dice «Completeness» y pregunta si se incluyen todas las funciones requeridas por el cliente. La respuesta lo llamó «Complejidad». La fuente no tiene esa confusión.

La regla **source-term-completeness/v1** solo actúa cuando concurren la etiqueta equivocada, la descripción de cobertura de funciones y el testigo literal recuperado. Comprueba posiciones del tramo y de la fuente. Excluye preguntas genuinas sobre complejidad, distinciones negadas y descripciones de coste algorítmico. En el replay de las doce candidatas solo señaló B4. No conoce preguntas o IDs del banco y no contiene una respuesta docente prefabricada.

El veredicto nativo inicial «no_issues_found» se mantiene en la traza; la observación del host se registra aparte. El modelo recibe esa observación con el pasaje, genera la corrección y vuelve a revisarse. No se reemplaza una palabra después de generar. La respuesta nueva usa «Completitud». El alcance de esta defensa es deliberadamente pequeño.

## Lectura técnica del contenido

Las distinciones centrales B3 (medible no implica realizable) y C2 (trazas no prueban por sí solas cumplimiento) ya reciben explicación. Los valores ficticios, las listas no exhaustivas y la repetición de una estructura no se rechazaron por sí solos.

Quedan aspectos para revisión docente: la explicación A2 del control de temperatura admite una formulación más inequívoca; C4 hace explícito «en cualquier momento» dentro del escenario, pero conviene no justificar esa disponibilidad como consecuencia general de «tiempo real». No se presenta un ejemplo inventado como una norma técnica ni se exige una especificación industrial exhaustiva a cada respuesta. La adecuación y utilidad pedagógica final las decide el docente.

## Uso y límites

```powershell
.\scripts\study-chat.ps1
# Misma actividad con Internet desactivado:
.\scripts\study-chat.ps1 -Offline
```

El lanzador selecciona la política de esta actividad piloto ya autorizada por el usuario. El runtime genérico sigue sin permiso web implícito; otras actividades necesitan su propia política. `-ActivityPolicy` permite indicar otra política explícita. El alcance de la actividad está versionado independientemente del permiso web: retirar Internet no concede permisos nuevos ni elimina el alcance local; retirar/cambiar el alcance invalida su uso. No se infiere exclusión de toda la asignatura por ausencia de pasajes.

El revisor local no está acreditado como verificador semántico general. El banco es conocido y sirve de regresión, no es reserva ni prueba ciega de transferencia. No se validaron voz, audio ni utilidad con alumnos. No hubo commits, Reset, migraciones, borrado de datos habituales ni restauración de evidencias históricas perdidas. T no se reanuda.

## Evidencia consultable

- [Conversaciones completas y corrección posterior](./transcript-full.md) · [Lectura móvil](./transcript-mobile.html).
- [Resumen mecánico](./results-summary.json), [protocolo final](./final-bank-protocol.json), [protocolo con alcance](./scoped-protocol.json), [protocolo terminológico](./terminology-protocol.json).
- Regresión y preparación CPU: `cpu-final.log`; comparación estructural Ruff: `ruff-comparison-final.json`; preservación: `preservation.json`; cierre: `cleanup-verified.json`.
- Snapshots de código y recibos originales dentro de cada `run-*`. El único ajuste posterior de estilo del módulo terminológico conserva el AST completo: `terminology-style-only.json`.

El número final de pruebas y el resultado de consistencia SpecKit se registran en `release-checks.json`, sin equiparar pruebas estructurales a aceptación semántica.


## Comprobaciones finales

744 pruebas CPU aprobadas (241,02 s), incluida preparación real del lanzador sin cargar modelos. Black: 160 archivos conformes tras formato de un test; Ruff estructural con multiplicidad: diez hallazgos existentes, cero nuevos. Los mapas históricos verifican 308, 140 y 22 entradas —467 rutas únicas— sin cambios. El manifiesto de ejecución contiene 268 archivos fuente: una diferencia posterior es exclusivamente formato, con AST completo idéntico, en la comprobación terminológica. La política normal coincide byte por byte con la v4 medida; la variante offline conserva el mismo alcance. [Recibo final](release-checks.json).

Se preservan además los intentos de herramientas que fallaron antes de inferir, incluido el primer presupuesto de salida finita v3 no admitido por el host; se corrigió el registro específico dentro de los mismos 8192 tokens/180 segundos, sin ampliar los límites generales. Un intento de Black paralelo quedó esperando subprocessos en el sandbox: se cerraron exclusivamente sus tres procesos propios y la comprobación se repitió en un único worker. Estos incidentes operativos no son fallos semánticos del modelo.

Cierre comprobado: cero workers GPU propios, GPU al 0 % (3002 MiB ocupados por el sistema y aplicaciones residentes). Los dos procesos T existentes **permanecen suspendidos**, con sus ocho hilos suspendidos; no se han terminado ni reanudado. Las dos guardas temporales de suspensión del equipo quedaron liberadas, sin cambiar su configuración permanente.
