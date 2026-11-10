# Continuación exclusivamente CPU — 29 de octubre de 2026

Instrucción humana vigente: continuar sin GPU. No se ha cargado ningún modelo GPU, consultado NVIDIA, iniciado servidor, realizado inferencias ni tocado servicios ajenos. Se usan mocks y TestClient in-process; no se dan por hechas las seis preguntas reales del siguiente intento.

## Adaptación de presupuesto implementada

Perfil nuevo optativo `study-expanded/v1`:2048tokens/180s/16000caracteres. El histórico permanece768/50s/4000 y sigue siendo el default. Selección explícita mediante `--study-budget study-expanded/v1`, admitida solo con proveedor docente real optativo. No se ha ejecutado ese arranque.

El perfil conecta petición y mensajes ampliados, renderer/frame existente, deadline del binding, validación de candidata, display/shown, historial íntegro siguiente, catálogo/open/state/turn y aviso visible en UI. No se corta el texto mostrado a4000 al reutilizarlo. Se mantienen pregunta2000, tres pares mostrados, seis llamadas del proveedor real, cupo compartido, reloj global, cancelación, fuentes y publicación de participante cerrada. El deadline efectivo sigue acotado por el tiempo global restante. No se añade revisión/reparación automática por reutilizar la capacidad de transporte ampliada.

Las pruebas comprueban default intacto, salida mayor de4000 íntegra en display/ACK/historial, límite16000, perfil desconocido, frame2048/180000, metadatos API y deadline global menor que180. Los resultados son fixtures de transporte: no evidencian mejora semántica ni garantizan terminación de cualquier respuesta.

## Selección de comparaciones

`--study-coverage` habilita `comparison-coverage/v1` en la recuperación local CPU. Default de selección sin cambios; no se alteran fuentes ni se reindexa. Diversifica como máximo dos páginas de candidatas ya recuperadas atendiendo a facetas/encabezados generales; no fija sourceIDs para verificar/validar. Registra omisiones por cupo de páginas y conserva verificación de bytes y estado de suficiencia no evaluada.

El [análisis de P1 y sus fuentes](p1-source-analysis.md) distingue cobertura incompleta de la dicotomía no respaldada individual/conjunto. La nueva heurística tiene pruebas estructurales con conceptos sintéticos y cambio de tema; no se afirma que resuelva ya la respuesta real. No se han retocado los prompts para hacer pasar una salida expuesta.

## Entrega y límites

67pruebas Python y11pruebas Node aprobadas; TypeScript, Vite, ESLint, Ruff y Black correctos. Validaciones y contadores finales en pytest.log, ui-tests.log, ruff-final.log, black-final.log, eslint.log, tsc.log y build.log. Frontend compilado en web-dist de este dossier; no reemplaza apps/web/dist ni los builds históricos. No se ejecuta la orden de arranque de GPU ni una nueva prueba humana. La siguiente validación real sigue pendiente; no se modifican aceptaciones, IDs históricos o gates.
