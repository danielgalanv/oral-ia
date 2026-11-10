# Research008 — auditoría del flujo real

Decisión: quitar preflight en CLI start; start ya lo ejecuta dentro lifecycle_lock.
Evidencia: __main__.main start→launcher.check→launcher.start→check; full llama embed dos
veces en el mismo proceso, y cada check revisa dependencias/puertos/revisión. Alternativa
pasar validación previa al supervisor rechazada: permitiría una comprobación fuera lock.

Decisión: conservar API check_embeddings, verify_schema y seed/schema de preparación.
Son procesos diferentes; API necesita calentar su propio modelo antes de readiness y
preparación verifica instalación/migración. No hay intercambio de objeto modelo entre ellos.
Ingest usa embeddings si no existe seed; semántica no duplicada del preflight.

Decisión: hilo solo de mensajes, sin mover trabajos a otro hilo ni crear servicio.
Alternativas polling únicamente: no informa durante carga síncrona; worker para operaciones:
complica cancelación/propiedad. stderr conserva stdout JSON Check. Intervalo5s evita ruido.
No investigación externa necesaria: obligaciones resueltas por código y contratos locales.
