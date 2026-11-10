# Revalidación nueva de las seis evidencias de Feature 009

19 de octubre de 2026. Ejecución nueva, no restauración de originales. No se modifican sus hashes ni se declara T061 restaurada.

Comando: `pnpm.cmd --dir apps/web exec playwright test --config ../../tests/e2e/playwright.config.ts test_teacher_long_material.spec.ts --output <esta carpeta>/artifacts --reporter=line`.

Resultado: **3/3 Playwright aprobados**, 1,4 minutos mostrados por Playwright (incluye preparación). Sin reintentos añadidos, cambios de producción ni Reset. Datos y servidores temporales aislados; puertos 5175/8005/8015 libres al finalizar. No se detuvieron servicios ajenos.

| Caso | HTTP | Estado | Lectura del cuerpo desde inicio | Peticiones |
|---|---|---|---:|---:|
| Normal | 201 | processed, hash del archivo 04 correcto | 10.584 ms | 1 |
| Lento | 201 | processed, hash del archivo 04 correcto | 19.155 ms | 1 |
| Error de extensión | 422 | error esperado, formulario recuperado | 49 ms | 1 |

Caso lento: 16.000 ms de demora controlada en entrega, 3.094 ms del endpoint medidos por el harness. No confundir con carga fría, mejora de rendimiento ni latencia universal.

Normal y lento comprueban carga del archivo 04 original, actividad docente, pregunta/respuesta con fuentes, cierre, revisión, exportaciones JSON/Markdown y borrado en datos de prueba. El caso lento verifica aviso de carga y rechazo de envíos duplicados. Error utiliza un archivo ficticio no admitido. Se inspeccionaron visualmente las tres capturas generadas. La interfaz muestra proveedor determinista y perfil de capacidad reducida: este recorrido no acredita diálogo guiado, generación libre, voz ni utilidad con personas.

Las seis evidencias nuevas están agrupadas en evidence/: browser-long-material.png, browser-long-slow.png, busy-real-response.png, upload-normal.json, upload-slow.json y upload-error.json. Originales nativos de esta ejecución en artifacts/. Histórico: **229 archivos comprobados, cero cambios**, informe historical-preservation.json. Logs y resultado de proceso: playwright.log y run-result.json. Hashes nuevos: sha256-manifest.json.

Esta revalidación aporta evidencia actual para los comportamientos probados. No recupera la ejecución histórica ni decide por el usuario la disposición de su pérdida; la revisión humana de los diálogos de Feature 010 es independiente.
