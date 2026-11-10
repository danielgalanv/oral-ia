# Diagnóstico técnico de invalidated y cupo compartido

Incidencia en prueba humana user-runtime-006: no hay recibo disponible para identificar la causa específica y el coordinador informa de servidor activo. No atribuirla automáticamente a caducidad, presupuesto o calidad académica. Dossier: docs/audits/2026-10-28-e2-invalidated/.

El estado compatible invalidated incorpora failure_code seguro para cupo agotado, modelo no disponible, fuentes cambiadas, contexto inválido, recuperación/transporte y causa técnica desconocida. Timeout y salida incompleta se explican por separado. No se publican mensajes arbitrarios de excepciones. Una retirada de fuentes conserva su causa tipada tras purgar, sin resucitar recibos o historial.

El cupo pertenece al runtime y se expone como usadas/máximo/restantes/agotado. Reentrada y preparación no lo reinician. Cada generación iniciada conserva su reserva incluso si falla; la disponibilidad previa evita consumir nuevas llamadas contra un worker ya detenido. UI bloquea Enviar con cupo0 y actualiza disponibilidad/cupo tras cada turno. Modelo detenido requiere preparación explícita, si queda tiempo y cupo; nunca reenvío automático.

La regresión de observabilidad falla antes y pasa después. Cinco preguntas exactas sin reintentos dejan una de seis llamadas; el paso5 no demuestra agotamiento. Las reproducciones de timeout/reintentos, fuentes, contexto y transporte son CPU con mocks, no evidencia causal de Chrome.50pruebas Python y10Node, build/lint correctos. Sin GPU ni cambios en sesión activa/assets ordinarios; aplicación pendiente del siguiente arranque planificado. Prueba humana/aceptación/gates sin cierre.
