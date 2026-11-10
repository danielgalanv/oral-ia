# Quickstart009

uv run --offline --no-sync pytest tests/integration/test_teacher_material_pack.py -q
uv run --offline --no-sync pytest tests/integration/test_long_extractive_binding.py -q
pnpm.cmd --dir apps/web exec playwright test --config ../../tests/e2e/playwright.config.ts test_teacher_long_material.spec.ts
.\scripts\check-demo.ps1
Archivo04 original debe cargarse desde navegador/autorización real en workspace E2E
propio. No Reset de demo preparada. Matriz finita no prueba cualquier documento/semántica.
Resultados finales en implementation-evidence.md y materiales/docente/RESULTADO.md.
