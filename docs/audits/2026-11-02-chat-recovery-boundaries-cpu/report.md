# Recuperación: cancelación, doble envío y reentrada

Incremento exclusivamente CPU. Se añaden tres pruebas HTTP con proveedores explícitamente simulados; no cambian módulos de producción, respuestas académicas ni criterios del revisor.

## Resultados

- Cancelar una candidata pendiente conserva solo el historial confirmado, mantiene la cuota consumida y rechaza una confirmación tardía de la candidata cancelada. La pregunta siguiente recibe únicamente el historial confirmado.
- Cerrar y volver a entrar no recupera recibos antiguos ni reinicia la cuota. La confirmación de un recibo de la sesión cerrada se rechaza.
- Durante una generación en curso, tanto el reenvío del mismo identificador como un segundo identificador se rechazan sin lanzar otra generación ni consumir otra unidad de cuota. Recuperar muestra ocupado, sin respuesta parcial.

Los tres casos pasan sin modificar producción. No se encontró un defecto adicional en estas rutas concretas.

## Validación reproducible

```powershell
.venv/Scripts/python.exe -m pytest tests/integration/test_study_chat_resume.py tests/integration/test_study_presentation_delivery.py tests/unit/test_study_lab.py -q --basetemp .claude-scratch/pytest-recovery-193
.venv/Scripts/python.exe -m black --check --workers 1 tests/integration/test_study_chat_resume.py
.venv/Scripts/python.exe -m ruff check tests/integration/test_study_chat_resume.py
```

Resultado: **40 pruebas aprobadas**, Black conforme y Ruff sin hallazgos en el archivo modificado. Una advertencia de deprecación de Starlette/httpx; no hubo fallos. Son pruebas HTTP en proceso, no una repetición del recorrido de navegador ni inferencia real.

No se cargaron modelos, no se usó GPU, no se iniciaron servidores externos ni se modificaron datos de demo, PDF, paquetes históricos o modelos. T191 y la aceptación conversacional real siguen pendientes. Este incremento no acredita calidad semántica ni utilidad con estudiantes.
