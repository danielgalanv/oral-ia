# Visibilidad de caducidad del runtime optativo

Incidencia posterior a E2: user-runtime-004 terminó al límite global de900s y el usuario recibió Failed to fetch. Es una pérdida del servidor al caducar, no evidencia de fallo académico del modelo. Dossier nuevo: docs/audits/2026-10-28-e2-interactive/runtime-expiry-ui/.

Contrato: estado del runtime real con deadline/restante/expired/renewable=false;410/runtime_expired antes de admitir inferencia o mostrar/confirmar una candidata tras el límite. La UI muestra el plazo global separado del máximo por pregunta y del lease15s. El reloj local bloquea envío y entrega tardía aun sin servidor. Conserva únicamente el borrador no confirmado en memoria de la pestaña y no reenvía automáticamente. Cerrar explícitamente descarta; no se añade almacenamiento persistente.

Conexión perdida, lease cerrado, fuentes/permiso invalidados, modelo detenido y fallo de generación tienen mensajes distintos. Las comprobaciones de conexión existentes son visibles y se pausan con la pestaña oculta; no prolongan runtime ni presupuesto. Ninguna renovación o carga GPU implícita.

CPU:50pruebas Python y9pruebas Node fake-clock/transporte/SSR, build y lint correctos. Sin servicio ni GPU nuevos; assets preparados en salida aislada y aplicación al runtime activo pendiente del coordinador. Sin nueva aceptación humana, cambio de IDs/estados históricos o apertura de participante.
