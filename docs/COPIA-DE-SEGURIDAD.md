# Copia de seguridad y restauración

El proyecto es un repositorio git local (sin remoto) desde el 07-11-2026. Git guarda código, tests, scripts, documentación, paquetes documentales derivados y auditorías. **No guarda** (ver `.gitignore`): `.tools` (modelos GGUF y llama.cpp, ~27 GB, se pueden volver a descargar/convertir), `.venv`, `node_modules`, cachés, los originales y PDF docentes (`materiales/**/originales`, zips) y `registro-avisos/` (preguntas de alumnos).

## Hacer una copia
```powershell
git add -A; git commit -m "descripción"      # confirma antes lo que quieras conservar
.\scripts\backup.ps1 -Destino 'E:\copias-oralia'   # sin -Destino: ..\ORALIA-backup\<fecha>
```
Genera `oralia.bundle` (todo el historial), `materiales-originales.zip` (originales docentes y registro de avisos) y `SHA256SUMS.txt`. **Copia luego esa carpeta a otro disco o servicio**: una copia en el mismo disco no protege de un fallo del disco. La del 07-11-2026 está en `..\ORALIA-backup\2026-11-07` (mismo disco).

## Restaurar
```powershell
git clone oralia.bundle ORALIA              # recupera código e historial
cd ORALIA; Expand-Archive ..\materiales-originales.zip -DestinationPath . -Force   # originales y registro de avisos
```
Después: `python -m venv .venv` e instalar dependencias (`pyproject.toml`), modelos en `.tools/models` (ver `docs/CONTINUAR.md`: Qwen3-8B, Qwen2.5-14B y Mistral-Small-24B en GGUF Q4_K_M y llama.cpp b12138) y `pnpm --dir apps/web install`. Los paquetes documentales comprueban hashes de los originales: si no coinciden, no arrancan.
