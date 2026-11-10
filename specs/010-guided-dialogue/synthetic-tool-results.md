# Conversaciones sintéticas de herramientas — 19-10-2026

**SC-009 no aprobada todavía**. Desarrollo 04: 8/8. Primera reserva: 5/8;
los 16 guiones fueron ejecutados, sin contar los nueve unit tests de oráculos como
conversaciones. Resultados íntegros en `tool-runs/`; resumen en first-tool-summary.json.

Los fallos iniciales de desarrollo se conservaron: resolver catálogo no equivale a
renderizar texto, un comando de modo de estudio en defensa debe rechazarse, una sesión
nueva no hereda consentimiento y la inyección de timeout debía ejercitarse realmente.
Los spies de operaciones devuelven valores de las funciones originales. Solo la
inyección etiquetada de timeout genera un fallo; nunca una respuesta favorable.

La primera reserva detectó tres problemas del mapeo del harness: una ruta inexistente
para desactivar material, una petición de modo prohibido que el oráculo esperaba
erróneamente aceptar y un orden distinto de cierre/borrado en S07-H. No se borran estos
resultados ni se presentan como defectos de producto confirmados. Los casos pasan a
regresión del harness; completar el mapeo y una reserva revisada sigue pendiente.

Las peticiones registran método/ruta/cuerpo, rol resuelto desde un único grant real,
HTTP status y efectos persistidos de turno, contexto, recibos y consentimiento. Los
tokens solo se usan en memoria; no aparecen en observaciones ni en URLs. Los argumentos
de unidades se cotejan contra los IDs publicados de la actividad. No se concede rol
docente por escribir una petición: revisión/exportación autorizadas son llamadas con
el grant docente; el participante recibe el rechazo correspondiente.

La consulta de catálogo y la proyección de fuentes se registran con sus cantidades:
un resultado vacío no acredita una cita entregada. La calidad conversacional completa
y la precisión de actos pertenecen además a acceptance-results.md, cuyo G1 sigue
fallido. Ninguna prueba demuestra utilidad con personas ni voz real.


## Nuevas reservas de herramientas

La regresión del mapeo original pasó 8/8 en 16,04 s. La segunda reserva con ocho
variantes entre dominios pasó 5/8 en 16,72 s. S06/S07/S08 detectaron otra suposición
del runner: solo dos cadenas exactas contaban como cierre, aunque el producto cerraba
correctamente con otras formulaciones. Es fallo del mapeo/oráculo, no un cierre
incorrecto de producto; los informes originales quedan conservados.

La tercera reserva contiene ocho variantes entre modos con expected_terminal anotado
explícitamente en cada paso antes de ejecutar. El oráculo de estado usa esa anotación,
nunca la salida del intérprete ni la respuesta de la API como verdad esperada.
**8/8 aprobadas, 18,74 s**, reports tool-runs/2026-10-19-tools-third-reserved.
Son conversaciones sintéticas mapeadas expresamente a operaciones públicas observadas;
no demuestran selección autónoma de herramientas mediante texto ni utilidad humana.


Validación del código archivado: 8 desarrollo + 8 tercera reserva, **16/16 aprobadas en 28,31 s**, XML feature010-tools-verified-16.xml y tool-runs/2026-10-19-tools-verified-16. Se conservan fallos previos; no se confunde el mapeo explícito de las peticiones con inferencia autónoma de herramientas.
