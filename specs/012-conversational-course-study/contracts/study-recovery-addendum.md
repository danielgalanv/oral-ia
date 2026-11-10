# Recuperación operativa del autoestudio diagnóstico

Versión 1, 29-10-2026. Aplica al perfil de inspección, no abre participantes.

- `question_too_long`: la pregunta sola excede el límite efectivo del encoder. Solicitar dividir/reformular. No cargar embeddings de esa pregunta ni llamar al generador.
- `search_context_too_long`: la pregunta cabe pero pregunta+referentes no. Solicitar explicitar el referente en una pregunta breve o cambiar explícitamente de tema si se trata de una consulta independiente. No eliminar el historial en silencio.
- `no_passages`: no se entregaron pasajes. Permitir reformular/consultar documentos. No declarar exclusión de la asignatura ni suficiencia de una selección no vacía.

En los tres casos: conservar pregunta editable e historial confirmado; cero reserva generativa nueva; candidato vacío; nada nuevo en historial; nada se reenvía automáticamente. Un nuevo intento tiene ID nuevo. Tras una reformulación que cabe, el flujo ordinario puede continuar desde el último texto realmente mostrado. Una retirada/alteración de fuentes sigue cerrando y purgando según el contrato previo; no se trata como un fallo recuperable conservando fuentes caducadas.

Los errores públicos usan mensajes fijos del host, no rutas o excepciones arbitrarias. Son orientación operativa, nunca respuestas académicas predefinidas. Cupo global, leases, consentimiento, presupuesto generativo y gates no cambian.
