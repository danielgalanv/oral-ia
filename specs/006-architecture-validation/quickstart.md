# Quickstart — 006

Desde raíz, uv instalado, sin Ollama/STT/red:

```powershell
uv run --no-sync python -m oralia.validation run --output .claude-scratch/validation006 --repetitions 2 --seed 42 --authorize-synthetic-ablations
uv run --no-sync python -m oralia.validation replay --package .claude-scratch/validation006
uv run --no-sync pytest tests/validation/ -q
```

Directorio nuevo; leer report.md/results.json/manifest.json. Ranking lexical y modelo
determinista son condiciones controladas, no benchmark LLM/RAG real. GPU/tokens/utilidad
humana faltantes con motivos. Sin base de producción ni descargas. Evidencia medida
se añadirá a implementation-evidence.md al ejecutar, no se presupone éxito.

## Ejecución medida

Paquete final: evidence/ (204 celdas,17 escenarios,6 condiciones,2 repeticiones,
semilla42). experiment-run.log y experiment-replay.log contienen el resultado real;
replay comprueba las204 decisiones estructurales, no igualdad de tiempos o UUID.
No cambiar archivos de src/oralia entre run y replay: el manifiesto detecta cambio de
código. Conservar la versión de código correspondiente si se mueve el paquete.

Modelo/parámetros: DeterministicGenerationAdapter, max_tokens256, sin sampling/modelo
LLM. Configuración de fixture fijada en experiment.py bajo hash: lenguaes, conocimiento
generalfalse,20turnos(1en límite),300segundos, políticas sintéticas explícitas. Ranking
lexical top3/top1; corpus versionado y anotación preparada de conflicto. No es una medida
de descubrimiento semántico ni de índice vectorial. Presentation cambia propósito/modo.

Trazabilidad completa: ejecución sin error, componentes observados, autorización final,
un evento terminal completed/degraded/blocked y cadena de parches continua de versión
inicial a final. Bloqueado/degradado son finales observables; no equivalen a ausencia de
traza. Baseline sin coordinación: denominador0 y porcentaje null(no comparable).
Reformulaciones cuentan veredictos/acciones de reformulación, no calidad de redacción.
Las latencias de agentes excluyen sustitutos de ablación; component_latency_ms incluye
su coste de transporte y la puerta de política, que no se cuentan como agentes.

CPU tiempo de proceso y RSS antes/después, no pico ni atribución por agente. Contexto
mide caracteres de consulta/evidencia, no tokens/prompt completo. Faltantes GPU/tokenizer,
modelo/índice/voz reales y piloto humano con motivos explícitos. Baseline no posee puertos
de fallo de agentes/índice: injection_applied=false para esos casos. Corrección es sonda
auxiliar real de defensa incluso en celda baseline; no comparar su latencia como modelo directo.
