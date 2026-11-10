# Investigación012

Decisión: sucesora de011, no ampliación retrospectiva. La consulta literal y el planificador finito no satisfacen explicación adaptada/transferencia; no añadir diccionario de las frases de evaluación.

Recursos observados: ejecutable Ollama instalado; manifiesto qwen2.5:0.5b local (modelo397807936bytes). No hay listener11434 en la inspección inicial. No se descargará nada. Proceso de evaluación propio, puerto explícito libre, localhost, solo API local/modelo ya presente, sin nube.

Investigación delegada speckit-plan, solo lectura: confirma contrato T090 schema1 reconstructivo de catálogo+slots, grounding léxico insuficiente para entailment general. Referencias:010/contracts/authorization.md y generative-gate.md; output_authorization_contract.py, output_proposal_builder.py, grounding_verifier_agent.py. Instalar o ejecutar modelo no prueba G2.

Alternativas: expandir citas (no cumple objetivo), repertorio manual de preguntas (no prueba transferencia), convertir texto generado en referencia confiable (prohibido), segundo prompt del mismo modelo como aprobación (insuficiente). Se implementa primero ruta candidata observable independiente, contrato de afirmaciones derivadas y gate que rechaza todo lo no acreditado; nunca se conecta directamente a publicación participante.

Ruta de publicación sucesora requiere comprobación semántica independiente de transformaciones y política explícita; permanece trabajo obligatorio hasta demostrarla. La evaluación del modelo no sustituye ese trabajo ni redefine SC001. Autoría técnica de derivados no es revisión docente. La reserva se congela antes de inferencia; sucesivas ejecuciones se etiquetan expuestas.

Primeros fallos preservados: first-generation/readinessHTTP prematura; first-generation-ready/24llamadas con timeout durante carga, sin respuesta. No afirmar calidad de modelo ni diálogo a partir de esa serie. Ajuste de precarga explícita documentado en plan, sin ampliar plazos productivos.

La serie con JSONschema emite candidatas tipadas pero devuelve preguntas en lugar de explicar e inventa testigos ingleses. Se conserva completa en generation-structured-exposed. Se añade prueba de capacidad en lenguaje natural sin anotación/permiso para aislar complejidad de formato de capacidad didáctica: no hay publicación ni aprobación aunque la respuesta suene plausible. No es sustituto del contrato derivado ni supera G2.

## Inventario ampliado real

HuggingFace contiene snapshots completosQwen2.5-1.5B (3.087GB),7B (15.231GB),14B (29.540GB),Qwen3-8B (16.382GB); Gemma4-E4B solo configuración, no pesos. No confundir catálogoOllama0.5b con todos los recursos locales. PyTorch del proyecto2.13.0+cpu / transformers5.14.1, sin accelerate ni CUDA. Ollama observado usa RTX5090/32GiB, host191GiB. Decisión: importar safetensors7B ya presentes a almacén Ollama propio (sin cuantización ni descargas), backend GPU existente, no tercer agente/adapter ni biblioteca nueva. Alternativa de adapterTransformers requeriría backendGPU no presente o mediciónCPU distinta; conversión más compatible con puerto existente. Procedimiento primario: https://docs.ollama.com/import . La conversión no acredita calidad ni G2.
