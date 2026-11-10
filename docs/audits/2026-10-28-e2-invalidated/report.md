# Incidencia activa: «invalidated» sin causa observable

**Hallazgo posterior de la prueba del coordinador:** P2 del nuevo ensayo devuelve
generation_length_limit, finish_reason=length,768tokens de salida,45875ms y2845
tokens de entrada, worker aún listo y cupo usado2/6. Esto identifica truncamiento
en esa P2, no la causa del antiguo paso5. El coordinador también ha registrado un
error de entrada por append en P3; no se proclaman seis preguntas exactas.
[Propuesta optativa de presupuesto ampliado, sin activar](study-budget-proposal.md).
No se ha tocado el servicio en curso ni iniciado otra inferencia/campaña.

**ENTREGA LISTA PARA EL COORDINADOR.** No queda implementación CPU pendiente.
Los fuentes Python y React/TypeScript del workspace son la versión corregida;
50pruebas Python y10Node, TypeScript, ESLint, Ruff, Black y Vite aprobados.
`completion.json` conserva sus hashes. No se ha iniciado otro servicio ni GPU.

**Frontend coherente preparado:**
`D:\Proyecto personal\ORALIA\docs\audits\2026-10-28-e2-invalidated\web-dist`.
El bundle es `assets/index-BELI38Ia.js` con su index.html y CSS del mismo build.
No usar el build aislado anterior runtime-expiry-ui ni los assets ordinarios
antiguos para dar por probada esta corrección de cupo/códigos. El CLI normal
sirve `apps/web/dist`: después de cerrar el runtime anterior y antes del nuevo
arranque, el coordinador debe publicar allí el build completo preparado (o
compilar desde los fuentes actuales), y después recargar su pestaña. Este chat
no ha reemplazado esos assets durante la sesión humana ni tocado8027/runtime006.

La nueva petición humana de ejecutar las seis preguntas será realizada por el
coordinador en su nuevo runtime. Aquí no se consumen llamadas ni se atribuye
aceptación de esa prueba todavía. El límite de seis incluye reintentos que hayan
llegado al proveedor; UI y API ya exponen ese contador sin reset por reentrada.

La causa específica de la sesión humana user-runtime-006 **no está demostrada**. El coordinador informa de servidor93584/8027 aún escuchando y GPU activa; no se atribuye esta incidencia a caducidad, cupo o calidad académica. La pestaña in-app con401 es otra sesión y no se ha usado como evidencia de Chrome. No se accedió a memoria, cookies, historial o recibos de esa sesión ni se modificó su runtime.

## Defecto comprobado y reproducciones CPU

El código anterior convertía tanto ValueError como OSError en status=invalidated sin retener un motivo público. El límite de seis llamadas, la falta de disponibilidad del worker, errores de contexto y recuperación podían desembocar en el mismo mensaje. Además, el cupo se reservaba antes de que el binding detectara un modelo detenido; repetir envíos a ese worker podía consumir llamadas sin generar otra respuesta.

Una regresión que exige budget_exhausted falló antes del cambio (regression-before.log) y pasa después. Con el guion exacto de cinco preguntas y sin reintentos, el proveedor fixture completa el paso5 y queda una llamada: **el paso5 por sí solo no prueba agotamiento**. Una sexta llamada expresamente sintética agota el cupo; una séptima queda bloqueada, y cerrar/reabrir conserva el contador. No se inventa la pregunta6 humana.

Otra reproducción simula timeout en la pregunta2 y worker detenido. Las siguientes preguntas/reintentos devuelven model_unavailable y mantienen dos llamadas consumidas; el turno fallido no entra en el historial. Una preparación explícita con mock vuelve a habilitar el proveedor sin renovar el contador. También se reproducen contexto inválido, recuperación fallida, transporte roto y fuentes retiradas. Son reproducciones técnicas con fixtures, no inferencias sobre lo sucedido realmente ni evaluaciones académicas.

Hipótesis compatibles con la observación humana: reintentos que hayan consumido las seis llamadas; worker detenido tras timeout/rotura de transporte; contexto/validación o recuperación fallida. Sin un recibo específico no se elige una de ellas. La sesión activa con código anterior no permite recuperar retroactivamente la excepción que descartó.

## Cambio preparado para siguiente arranque

- Errores públicos tipados: budget_exhausted, runtime_expired, model_unavailable, source_changed, context_invalid, retrieval_error, transport_error, generation_timeout y causa desconocida explícita. No se copian mensajes arbitrarios de excepciones, rutas o datos sensibles. Los estados antiguos se conservan para compatibilidad y se añade failure_code.
- Cupo compartido del runtime en open/state/turn/prepare: usadas, máximo, restantes y agotado. No se reinicia por reentrada. Una generación iniciada consume su reserva aunque falle; no se devuelven ni recalculan llamadas históricas. La disponibilidad se comprueba antes de reservar nuevas llamadas a un worker ya detenido.
- En la UI se muestra el cupo y se bloquea Enviar cuando no quedan llamadas. El resultado de cada turno actualiza cupo y disponibilidad inmediatamente, además del polling existente. Modelo detenido ofrece preparación explícita si quedan tiempo y cupo; agotamiento no puede eludirse recargando. No se reenvía el borrador automáticamente.
- Mensajes separados para límite de longitud, timeout, contexto, fuentes, transporte y causa desconocida. invalidated antiguo sin código no se convierte en una afirmación de cupo agotado ni en error académico. Los borradores pendientes se conservan según el contrato previo.
- Conservados permisos, validación de fuentes, descarte de historial/candidatas no confirmadas, caducidad global/lease y salida de participante cerrada. No se relajan controles para hacer pasar el guion.

## Validación y aplicación

50pruebas Python/API y10pruebas Node aprobadas; build, TypeScript, ESLint, Ruff y Black correctos. Recibos en pytest.log, ui-tests.log, ruff.log, black.log, eslint.log, tsc.log y build.log. Pruebas Python/API in-process y Node fake-clock/transporte/SSR; no abren servidor ni usan GPU. El build web está aislado en web-dist de este dossier; no se sustituyó apps/web/dist ni se tocó8027, PID93584, ejecución13952, user-runtime-006 o procesos ajenos.

El servicio activo sigue con sus clases/assets anteriores. Estos cambios requieren el siguiente relevo planificado y recarga de UI; no han sido aplicados a escondidas. La aceptación humana sigue pendiente. No nueva campaña, inferencias, reinicios, limpieza de sesiones, commits, Reset o mensajes interchat.
