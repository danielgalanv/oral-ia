# Plan nocturno (06-11-2026, de 02:10 a 09:30)

Trabajo sin intervención. Reglas que me impongo: no cambio nada por defecto en el chat estable, no descargo nada más de lo autorizado
(llama.cpp, bge-m3, Qwen3-Embedding-0.6B, Qwen3-Reranker-0.6B), todo lo nuevo va a carpetas nuevas y la GPU queda libre a las 9:15.

## Ya medido antes de dormir
- llama.cpp (build b12138, CUDA 13.4, `.tools/llama.cpp`): Qwen3-8B Q4_K_M 241 tok/s y 13-14 mil tok/s de prefill; Qwen2.5-14B Q4_K_M 146 tok/s
  y 7,3-7,9 mil tok/s de prefill; con 8 secuencias en paralelo el 8B da 1.128 tok/s agregados (el nuestro: ~100 y ~50 tok/s).
- 232 preguntas sintéticas: 45 s con llama.cpp frente a >24 min con mi decodificador.
- Recuperación (215 preguntas sintéticas, 117 páginas): R@5 actual 0,670; bge-m3 solo 0,930; Qwen3-Embedding 0,912; con reranker 0,949/0,958.

## Cola (en este orden)
1. **Proveedor llama.cpp** (`course_dialogue/llama_server_provider.py`) con salida JSON restringida por esquema; pruebas CPU.
2. **Latencia de turno** con llama.cpp (generación 14B + revisión 8B), 4 preguntas × 3 repeticiones.
3. **Matriz de revisión** sobre `eval-set-v1` (53 casos) con tres semillas por configuración:
   Qwen3-8B razonando (libre y con esquema), Qwen2.5-14B sin razonar (esquema), Mistral-Small-24B sin razonar (esquema, otra familia).
4. **Recuperación**: contextual retrieval (contexto en español por página), reranker, consulta reescrita; elegir la mejor configuración.
5. **Análisis sin GPU**: conjunto de jueces por mayoría, umbrales, simulación del aviso al alumno.
6. **Repeticiones con más semillas** de las dos mejores configuraciones hasta las 9:00.
7. 9:00-9:30: `SUMMARY.md` y actualización de `docs/CONTINUAR.md`.

Los resultados se guardan en esta carpeta; el orquestador escribe `queue.log` con cada hito.
