# Orientación accionable — evidencia 19-10-2026

T073/T074 terminadas;67/74 tareas. Se corrige una brecha de interfaz: la API y el panel de capacidades ya enumeraban los temas, pero la aclaración junto a la conversación no permitía seleccionarlos directamente. No se atribuye ausencia de opciones a todo el sistema ni error nuevo a la clasificación.

DialogueTopics muestra temas actuales devueltos por API junto al diálogo, propone cambio mediante el control topic_switch existente y pide confirmación. Confirmar envía solo la constante «confirmo», nunca una orden generada desde el nombre docente; el servidor resuelve el tema pendiente y vuelve a validar. La pregunta actual se mantiene hasta confirmar. Sin estado local adicional; enviar/resultado desconocido deshabilitan los controles y cierre efímero elimina la superficie. No cambian backend, contratos, plantillas, permisos ni corpus reservado.

## Resultados actuales

- Playwright completo:23/23 en4,5min. Casos nuevos: agua32,6s, programa9,6s; backend real sin sustitución favorable. Prueban selección por teclado, confirmación, contenido fundamentado/coherente, pregunta pendiente y desaparición tras cierre efímero/404 de revisión.
- API dirigida:3/3,10,99s; tema retirado ausente y control atrasado409 sin nuevo turno; argumentos privilegiados rechazados.
- Build/lint aprobados; Vite482ms es tiempo de empaquetado observado, no afirmación de rendimiento conversacional. Black: único test Python afectado sin cambios. Ruff estructural con multiplicidad frente a baseline durable:10 heredados,0 nuevos,39 retirados. format-validation-orientation.json.
- Guard histórico229 archivos/0 nuevas mutaciones en rojo y verde. Seis pérdidas previas no restauradas. Cuatro paquetes originales006–009 verificados intactos.
- Misma huella backend que evidence-semantic-current-20261019: verify_package pasa204 celdas. Se conserva el replay coincidente previo, sin repetirlo ni regenerarlo al no cambiar sus archivos. Igualmente, global1139 aprobadas/879 omitidas/1 aviso es la ejecución previa del mismo backend; no se presenta como reejecutada en este pase.
- Los tres SHA de datos habituales/demo personal/fixtures coinciden. Puertos propios8026/5196/8005/8015/5175 libres tras finalizar. Sin Reset, commits, consultas a API personal ni cierre de procesos ajenos.

## Fallos y comandos preservados

La primera invocación `pnpm.cmd --dir apps/web run test:e2e -- test_guided_orientation.spec.ts --grep agua` no filtró: ejecutó23. Resultado21 aprobados/2 fallidos en5,4min: agua falló correctamente por ausencia de región accionable; programa agotó tiempo por bloqueo de sesión abandonada tras el primer fallo y no cuenta como fallo semántico independiente. Se cerró esa sesión ficticia a través de ruta docente pública confirmada, solo tras comprobar /e2e-fixture en8005; nunca se accedió a la API personal. Se añadió finally a cada caso nuevo para cerrar únicamente su session_id ante fallo. Log y contextos rojos conservados aquí.

La invocación directa Node de Playwright falló antes de ejecutar pruebas por resolución de @playwright/test desde la configuración externa; feature010-orientation-browser-full.log. La ejecución verde usa el comando conocido `pnpm.cmd --dir apps/web run test:e2e`, sin parámetros de filtro. No se cambió instalación, PATH permanente ni dependencias.

Comandos adicionales: `uv run --no-sync pytest tests/integration/test_dialogue_revoked_context.py tests/contract/test_dialogue_controls.py -q --junitxml=.claude-scratch/feature010-orientation-api.xml`; `pnpm.cmd --dir apps/web run build`; `pnpm.cmd --dir apps/web run lint`; `uv run --no-sync black --check tests/integration/test_dialogue_revoked_context.py`; Ruff con protocolo Counter(ruta,código,mensaje) frente al baseline durable.

## Archivos de código de este pase

- apps/web/src/components/DialogueTopics.tsx (nuevo).
- apps/web/src/components/DialogueActions.tsx (rótulo de tema seleccionado).
- apps/web/src/routes/Autoestudio.tsx (integración junto a conversación).
- tests/e2e/test_guided_orientation.spec.ts (dos casos reales, limpieza propia).
- tests/integration/test_dialogue_revoked_context.py (refuerzo de retirada).

Fuente congelada source-orientation-20261019.json/zip:562 archivos. Documentación: docs/DEMO.md, quickstart.md, seis bloques humanos e índice, propuesta de disposición, tareas/evidencias y análisis actual. Los textos de los24 diálogos API no cambian; su revisión humana sigue pendiente. G2 no habilitado; voz real y G3 no validados. No se afirma mejora de rendimiento ni utilidad educativa.
