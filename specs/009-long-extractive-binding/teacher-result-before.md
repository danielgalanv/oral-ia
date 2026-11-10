# Resultado de la verificación del paquete docente

Fecha: 18 de octubre de 2026. Sin cambios de producción, commits ni Reset de demo.

## Verificaciones aprobadas

- `uv run --offline --no-sync pytest tests/integration/test_teacher_material_pack.py -q`:
  **4 passed, 1 warning**, 11,52 s. Se usa el archivo 01 de este paquete, extracción,
  embeddings e índice locales reales, API con autenticación real y bases temporales.
- Casos: autoestudio y defensa, cada uno con conservación y sin conservación.
  Carga y activación de material, configuración/publicación, inicio, cierre,
  revisión por ámbitos, exportaciones JSON/Markdown y eliminación verificable.
  En autoestudio se exige respuesta con «100» y fuentes; defensa prueba pregunta inicial
  y ciclo de gestión, no garantiza una repregunta semánticamente útil.
- `pnpm.cmd --dir apps/web exec playwright test --config ../../tests/e2e/playwright.config.ts test_governance_flow.spec.ts test_demo_journey.spec.ts`:
  **2 passed**, 51,0 s. Los recorridos existentes comprueban navegación por teclado,
  fuentes, conservación, exportación, eliminación, defensa efímera, versionado,
  retirada, denegación y cierre de acceso. Usan sus propias fixtures: no equivalen
  a una carga manual del archivo 01 desde navegador.
- Black y Ruff del nuevo archivo de prueba: correctos, sin hallazgos.

## Incidencia encontrada, pendiente

El archivo 04 conserva el material largo con el que falló la primera comprobación:
autoestudio devolvió salida nula, `closed_error_safe`, autorización `invalid_context`.
El generador determinista recorta fragmentos, mientras el vínculo de autorización
extractiva exige correspondencia exacta con fragmentos completos. La incidencia se
envió al hilo de implementación para diagnóstico/corrección sin rebajar T090.
El archivo 01 se mantiene breve y sus cuatro pruebas pasan; esto no resuelve el
problema general de fragmentos largos ni acredita documentos arbitrarios.

Los archivos 02/03 y las preguntas de extensión son casos para ensayo docente;
no se declaran automáticamente validados. La fuente conflictiva es intencionadamente
incorrecta y nunca debe mezclarse con la actividad de demostración básica.

## Límites

Generación determinista, sin validación de voz real ni utilidad con personas.
No se repitió toda la suite global para esta entrega de materiales y pruebas.
No se alteró la base habitual ni se instalaron estas actividades en el seed preparado:
la guía explica cómo cargarlas voluntariamente como docente.
