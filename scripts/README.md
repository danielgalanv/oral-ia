# Entradas y ejecutores

## Uso actual

- `study-chat.ps1`: piloto de chat; `-PrepareOnly` es CPU, arranque normal carga modelos y requiere GPU libre. Ver `docs/ESTUDIO.md`.
- `clean_workspace.py`: vista previa/limpieza acotada de cachés; nunca datos o evidencias.
- Preparar solo conceptos: `uv run python -m oralia.documentary.concepts --output .claude-scratch/prepared-concepts-nuevo`.

## Demostradores anteriores

`demo.ps1`, `check-demo.ps1`, `course-study.ps1`, `course-dialogue.ps1` tienen otros contratos y alcance. Ver su documentación y `docs/MVP.md`; no confundir un pase con validación del chat actual.

## Diagnósticos y ensayos históricos

Los `audit_*`, `freeze_*`, `trial_*`, `diagnose_*`, `rehearse_*`, `run_*` y otros preparadores/verificadores están referenciados por informes, hashes y bancos. Se conservan en su ubicación por reproducibilidad. **No ejecutarlos todos ni asumir que son una suite de instalación**: pueden cargar modelos, necesitar fuentes particulares o consumir un presupuesto. Consultar el protocolo/argumentos antes. Nuevos ejecutores deben tener finalidad, salida propia nueva y presupuesto; no sobrescribir paquetes previos.
