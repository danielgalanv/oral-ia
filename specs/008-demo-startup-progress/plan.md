# Implementation Plan008

## Summary / Technical Context

Python3.12/PowerShell existentes, sin dependencias ni agentes nuevos. Mejorar consola del
supervisor con contextos de etapa y hilo de avisos que solo informa: operación siempre en
hilo principal para conservar señales, bloqueo y propiedad. threading.Event.wait(5)
interrumpible; finally detiene/join del avisador. Tiempo monotónico por etapa. Líneas
flush en salida de diagnóstico stderr; stdout de Check conserva JSON final parseable.

Nuevo src/oralia/demo/progress.py: catálogo cerrado de mensajes/acciones, contexto
stage(name, completion), aviso5s, saneamiento de secretos registrados. Fallos DemoError
con causa conocida; otros solo tipo y causa no determinada, diagnóstico saneado a log
propio cuando raíz válida. Nunca volcar variables/objetos/sesiones. Sin persistir secretos.
CLI no imprime excepción arbitraria. Fallo antes de raíz válida: no escribir fuera del
límite para diagnosticar; mostrar acción y tipo. Cancelación: mensaje separado y return130.

Integración en launcher.py: preflight por etapas dentro lock, una sola vez; secret o
secret_factory (CLI getpass/env) resuelta después de preflight, dentro mismo bloqueo.
Eliminar llamada redundante check de CLI; retener check de API en su propio proceso y
seed/schema en preparación (procesos diferentes). Conservar segunda comprobación ligera
de Node/Vite antes de Popen para no usar recursos desaparecidos; no cargar embeddings ahí.
Preparación se sigue esperando con timeout120; API/interfaz Popen indican proceso creado,
no disponibilidad. Un contexto de espera cubre bucle hasta readiness nonce de ambos;
termina antes de DEMO LISTA y navegador. Timeout90 y Stop20 sin cambios. Aviso de espera
full aclara calentamiento de API; TextOnly no anuncia carga ni fuentes.

src/oralia/demo/__main__.py: usar Progress tanto Check como Start; recoger credencial
solo al callback del supervisor. Errores/cancelación saneados; prepare/serve-api continúan
internos con logs normales sin credencial en argumentos. scripts/demo.ps1 y check-demo.ps1
no necesitan cambiar: stdout JSON y código de salida conservados.

## Constitution Check

I IA/sin notas; II contratos sin cambios; III estado sin cambios; IV T090/T150 intactos;
V recuperación sin cambios; VI políticas sin cambios; VII secretos minimizados/local;
VIII logs y hashes reales; IX timeouts/limpieza intactos; X gates antes de cierre;
XI solo observabilidad y eliminación de duplicado demostrado. PASS previo/postdiseño.
No esquema ni migraciones. No recursos alterados por ensayo: solo Start/Stop, sin Reset.

## Structure / Phases

Setup preservar→US1 etapas/espera→US2 errores/cancelación→US3 compatibilidad y ensayo→gates.
Pruebas nuevas tests/demo/test_progress.py antes de código; pruebas existentes de procesos
reales se mantienen. Check-demo real y Playwright, suite global (CLI de uso compartido),
Black afectados y Ruff Counter(ruta,código,mensaje) con multiplicidad baseline001.
Snapshot de fuentes007+originales006/007; generar paquete008/evidence-current/run/replay204
tras congelar Python. Medir ensayo primera observación y posterior, no comparar causalmente
rendimiento ni declarar caché fría. Tabla final y analyze/read-only, converge/append-only.
