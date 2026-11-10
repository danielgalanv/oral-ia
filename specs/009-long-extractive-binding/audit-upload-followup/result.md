# Seguimiento T016 — carga de material lenta

Fecha2026-10-18. Corrección de auditoría independiente, sin commits/Reset. El cierre
anterior y el contexto fallido se preservan en prior/ y audit-failed-context.md.

## Diagnóstico y límites de la causa

La auditoría agotó15s esperando respuesta POST /materials/documents. Su DB temporal
conservaba04 como processed,sin error_detail. Esto prueba que la ingestión terminó,
no cuándo llegó la respuesta ni la causa exacta del retardo. No se atribuye a una causa
no medida. Con el código de UI anterior, proceso API recién iniciado y caché local ya
preparada, se midieron10.705s hasta leer respuesta201/processed/hashoriginal. Evidencia:
normal-before-ui.json y diagnostic-normal-before-ui.log (recorrido completo aprobado).
No equivale a caché fría ni a mejora de rendimiento atribuible al parche.

Sí se comprobó un defecto de UX: mientras fetch estaba pendiente no había estado
ocupado ni bloqueo del formulario. Ahora muestra «Carga en curso. Esperando confirmación
del procesamiento y del índice local; la preparación inicial puede tardar», con role
status y aria-busy en formulario identificado. Archivo/asignatura/submit deshabilitados;
un ref síncrono rechaza incluso requestSubmit repetidos. finally libera controles;
errores reales siguen visibles y no se anuncia éxito antes de respuesta. Error de red
sin confirmación no se disfraza de rechazo del servidor: se indica comprobar catálogo
antes de volver a enviar. No reintentos automáticos ni aborto/timeout de producción nuevos.

La prueba separa controles15s de ingestión60s; total120s. Son presupuestos finitos de
prueba, no ETA ni promesa sobre hardware. No timeout0/retry/skip ni cambio de asserts100,
hash,cierre,exportación,borrado. La primera técnica de demora mediante route.fetch no
preservó bytes multipart; hash/processed lo detectaron y se descartó (validation-targeted.log).
La técnica final recibe el multipart original en API de pruebas,ejecuta call_next real y
retarda16s la entrega de esa respuesta. Middleware exclusivo de run_self_study_api.py;
no cambia autenticación,procesamiento,JSON ni aplicación de producción. No datos simulados
en las dos ingestiones04, ni elección arbitraria del tiempo desde producción.

## Resultados finales

| Caso | HTTP / estado | Tiempo hasta leer cuerpo | Solicitudes |
|---|---|---:|---:|
| Normal en suite (caché/estado ya usados por otras pruebas) | 201 / processed / hash04 correcto | 2773 ms | 1 |
| Lento con entrega16s controlada | 201 / processed / hash04 correcto | 18797 ms | 1 |
| Extensión no admitida,otro archivo ficticio | 422 real,error visible y controles liberados | 49 ms | 1 |

En el caso lento,2735 ms miden call_next del endpoint de pruebas (incluye sus
controles/procesamiento),más16000ms de demora controlada. No se presenta como carga fría.
La UI busy y dos requestSubmit adicionales se prueban sin generar otra petición. Normal
y lento completan consulta100/fuentes,cierre,revisión,JSON/Markdown y borrado404/409.

- Playwright completo:14passed (1.6m),comando97.65s; normal5.5s,lento22.2s,error0.612s de recorrido.
- Focal de3casos:3passed (1.3m),con ingestión e índice reales.
- Build/lint:exit0,1.8s/1.03s; sin advertencia ESLint pendiente.
- check-demo.ps1:exit0,69.19s,3checks aprobados.
- Black9 y Ruff afectados correctos; Ruff global Counter(ruta,código,mensaje),multiplicidad:10heredados,0nuevos.

Última puerta determinista921 y replay204 se conservan como evidencia del mismo código
Python de producción,verificado contra manifiesto: este seguimiento solo cambia UI y
harness/prueba E2E. No se afirman reejecutados aquí ni se regeneran paquetes innecesariamente.
18archivos estables,archivo04y paquetes previos intactos. Captura busy-real-response.png
inspeccionada. La auditoría externa conserva su criterio de aceptación; este informe no
la declara cerrada en nombre del auditor.

Comandos:pnpm.cmd --dir apps/web build; pnpm.cmd --dir apps/web lint;
pnpm.cmd --dir apps/web test:e2e; .\scripts\check-demo.ps1. Datos completos y logs en esta
carpeta,especialmente upload-normal/slow/error.json y validation-final.json.
