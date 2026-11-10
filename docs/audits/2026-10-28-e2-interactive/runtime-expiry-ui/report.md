# Incidencia «Failed to fetch»: caducidad visible del runtime

El usuario informó de un fallo después de preguntar. El coordinador confirmó que user-runtime-004, arrancado con900s, terminó mediante Shutting down / Application shutdown complete / Finished50444 y dejó de escuchar en8027. Los recibos locales se leyeron sin modificarlos: worker-001/worker-cleanup.json registra returncode0 y árbol detenido; gpu-after.json registra2051/32607MiB y2% de uso. El intervalo monotónico entre gpu-before y gpu-after es900,969s. Esta evidencia es consistente con la caducidad global comprobada por el coordinador; no permite imputar un error académico, una pregunta incorrecta ni un fallo de calidad al LLM. No se dispone aquí del log stdout de esa sesión para atribuir otros detalles de la petición.

## Cambio preparado

- Solo el proveedor real optativo expone runtime global: instante de vencimiento, segundos restantes, caducado y renewable=false. Catálogo, apertura, estado y preparación entregan este estado. El reloj y el presupuesto existentes no se modifican.
- La API rechaza con410/runtime_expired una nueva apertura, pregunta o recarga tras el límite. Vuelve a comprobarlo al terminar la generación; display/shown también lo comprueban. El binding del proveedor limita la espera al deadline global y rechaza una entrega que lo atraviese, aunque el adaptador devolviera después.
- La UI muestra cuenta atrás e instante de caducidad; advierte cuando resta menos que el máximo por pregunta. El contador local no hace solicitudes y bloquea el envío al llegar a cero aunque ya no exista servidor. Una respuesta tardía también se descarta por reloj/epoch.
- Se distinguen conexión perdida, runtime caducado, lease/inspección cerrada, permiso/fuentes retirados, modelo detenido/preparando y error real de generación. Un fallo de fetch al enviar o al leer el cuerpo no confirma recepción, finalización o error del modelo.
- El borrador queda en memoria de la pestaña, editable y sin reenvío automático. Solo se vacía tras confirmación shown, o al cerrar y descartar explícitamente. No se añade localStorage ni persistencia en servidor. Recargar/cerrar la página puede perder el borrador: no se promete recuperación persistente.
- La comprobación de conexión existente cada3s se explica en pantalla y se pausa con la pestaña oculta. El lease sigue siendo15s. Ninguna comprobación, reentrada o recarga amplía el runtime; no se añade renovación ni encendido de GPU automático.

## Verificación CPU

50pruebas Python aprobadas, incluidas cuatro nuevas: vencimiento visible sin renovación/reentrada; bloqueo de candidata al caducar durante generación; distinción de lease con reloj falso; rechazo de salida del adaptador tras deadline. TestClient es in-process y no abre puerto.

9pruebas Node aprobadas con reloj falso, transporte fetch simulado y SSR de los componentes React reales: bloqueo de envío, rechazo tardío, mensajes distintos, borrador editable, runtime expirado inicial, Failed to fetch sin reintento, desconexión al recibir y aborto explícito. Son pruebas CPU/SSR, no una nueva prueba interactiva de navegador ni aceptación humana.

TypeScript, Vite, ESLint de los tres archivos web afectados, Ruff y Black correctos. Recibos: pytest.log, ui-tests.log, tsc.log, build.log, eslint.log, ruff.log y black.log.

## Entrega sin interferir con la prueba activa

No se inició GPU, modelo, servidor ni listener; no se consultó ni modificó el runtime activo,8027 o procesos ajenos. No se aplicó reset, no se modificaron user-runtime-004 ni los históricos y no se enviaron mensajes interchat.

El build se deja en web-dist dentro de este dossier, separado de apps/web/dist. Los cambios Python solo entrarán en un próximo arranque planificado. El runtime actualmente iniciado por el coordinador no incorpora estas clases cargadas ni esta UI aislada. Para aplicarlo hay que programar el relevo, compilar/publicar los assets ordinarios y recargar la página con consentimiento; no se ha hecho a escondidas. Un servidor antiguo sin metadatos conserva la explicación de red, pero no permite inventar el instante real de vencimiento.

La prueba personal del usuario sigue pendiente. No se modifica T103 como aceptada, no se cierra Feature012 ni se abren participante/G2/SC001/T090/T150. Todo contenido continúa unverified/not_assessed y sin autoridad de publicación.
