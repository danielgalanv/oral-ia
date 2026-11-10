# Research007

Decisión supervisor foreground y solicitud Stop validada. Razón: Windows no ofrece SIGTERM
portable por consola; usar Popen guardado evita PIDs reciclados y procesos ajenos. Alternativa
kill por puertos/nombres descartada; no servicio externo. Preparación: módulos existentes
SQLAlchemy/Alembic, ingest/activate/publish. No pipeline cognitivo nuevo.

Decisión credencial manual oculta; alternativa contraseña demo conocida o almacenada
rechazada. Node/Vite sin secretos. Cachés HF preinstaladas solo lectura, demo tmp/config/
index/files separados. TextOnly explícito si falta embedding, nunca embeddings simulados.

Decisión navegación por activity ID no secreto + modo desde lista autorizada. API sigue
validando tokens, actividad y propiedad. Mantener inputs manuales por compatibilidad.
Snapshot006 antes de modificaciones; paquete nuevo separado y replay con código actual.
No desconocidos bloqueantes, investigación realizada sobre interfaces locales existentes.
