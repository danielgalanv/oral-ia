# E2 real recuperada — 28 de octubre de 2026

La autorización humana «Saca todo de la GPU y úsala tu» permitió liberar las cargas que impedían el arranque. Se detuvo exclusivamente llama-server PID104664, identificado con dolphin-venice-Q5_K_M.gguf, y se solicitaron descargas de modelos a ComfyUI8190/8191 sin cerrar sus interfaces. La VRAM bajó de21060 a1963MiB sobre32607MiB. No se borraron datos. La memoria del escritorio permanece.

Esta recuperación tiene reloj nuevo explícito, finito de900s desde18:39:29 aproximadamente, y máximo seis llamadas académicas incluyendo la cancelada. No modifica el preflight anterior ni convierte en válido su cierre fuera de45min. El relevo de proceso conserva el mismo started_monotonic y cuatro llamadas ya usadas mediante handoff-clock.json. No se reiniciaron estos presupuestos al recargar ni reabrir.

Se verificó en navegador real la interfaz existente, con Qwen2.5-14B NF4, renderer estructurado nativo, corpus v2 e índice existente en CPU. No fixture. Se completaron las cuatro preguntas consecutivas: definición, tipos, explicación alternativa y ejemplos retomando el calendario. Las capturas turn-01..04-ui.txt contienen las preguntas, candidatas y los cinco pasajes/documentos/páginas realmente expandidos por turno. La captura normaliza espacios; no se presenta como exportación byte a byte del proveedor.

La quinta llamada se canceló durante actividad GPU medida al31%; no apareció candidata tardía. El worker y su árbol quedaron detenidos según worker-runtime-002/worker-001/worker-cleanup.json. Se cerró la inspección, se reabrió vacía y se pulsó Recargar modelo local. La sexta llamada produjo otra candidata completa con fuentes, recogida en turn-06-after-reload-ui.txt y verified-result-ui.png. Finalmente se cerró y descartó el historial en la interfaz.

Se añadió recarga explícita separada de generación: el estado distingue detenido/preparando/listo y deshabilita Enviar mientras no está listo. Una sola recarga por runtime; no renueva reloj ni seis llamadas. La preparación revalida autorización y fuentes antes y después. La cancelación sigue matando el worker, y las peticiones conservan768tokens/50s/4000caracteres. Tres cargas técnicas en total: arranque inicial, relevo tras incorporar recuperación y recarga posterior a cancelar. Ninguna comparación adicional de prompts.

Revisión proporcionada: las cuatro respuestas del episodio y la de recuperación son aceptables con mejoras menores. Distinguen funcional/no funcional, usan ejemplos plausibles y sostienen el referente cuando se pide. Puede mejorarse concisión, explicitar otras clasificaciones y marcar más claramente los ejemplos hipotéticos; no se considera fallo material ni se exige reparación por vocablos aislados como «garantiza». No se afirma exhaustividad o suficiencia semántica. Todas siguen unverified/not_assessed, publication_allowed=false y participant_display=null.

Validación:46pruebas CPU aprobadas, build TypeScript/Vite correcto y Ruff sin hallazgos. tests-final.log, web-build.log y ruff-final.log. El primer proceso se detuvo mediante interrupción de su sesión de ejecución: no emitió worker-cleanup.json; la devolución de VRAM a1963MiB quedó medida y no se inventa un recibo de cierre ordenado.

El segundo runtime caducó y detuvo servidor y árbol GPU, pero registró TimeoutError durante su cierre. Después se limitó el timeout al arranque y se dejó al watchdog solicitar el cierre normal. Una regresión CPU nueva comprueba que el watchdog alcanza request_shutdown antes del teardown. Esta última corrección no se volvió a ejecutar en GPU; el resto del flujo sí. current-code conserva la versión capturada antes de este ajuste, y final-code la versión entregada. La escritura final del informe ocurrió después del límite operativo; no se hicieron nuevas inferencias ni se amplió el runtime.

La verificación técnica E2 se ha ejecutado; aceptación/prueba personal del usuario pendiente. T103 no se marca automáticamente aceptada. Feature012/T077global/T090/T150/G2/SC001 y participante permanecen sin apertura. La prueba termina sin inferencias adicionales ni runtime indefinido. Véase completion.json para el estado final de recursos.

Para una prueba personal posterior, desde D:\Proyecto personal\ORALIA, con GPU libre y un directorio nuevo exclusivo:

```powershell
.venv\Scripts\python.exe -m oralia.documentary --package v2 --retrieval --study-lab --real-provider --runtime-output docs/audits/2026-10-28-e2-interactive/user-runtime-001 --runtime-seconds 900 --port 8027 --no-browser
```

Esperar Application startup complete, abrir http://127.0.0.1:8027/tecnica?documental=1, entrar en consulta e inspección temporal. Este mismo arranque/configuración ya se ha probado; el directorio user-runtime-001 es nuevo y no se ha ejecutado como sesión extra. Se limita a15min/seis preguntas, con una recarga explícita posible. No abre LAN ni modo participante.
