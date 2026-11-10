# Documento/página o URL, sin citas literales

Decisión del usuario aplicada el 31-10-2026. T174 completa en laboratorio; T175 pendiente de medición real.

## Comportamiento

El perfil `web-review/v5` ya no exige que el modelo copie una cita textual ni reproduzca literalmente la frase criticada. Describe la afirmación y el problema; para cada objeción señala las fuentes recibidas. El host obtiene el texto visible de un catálogo de localizaciones:

- **Requisitos, página 73**.
- **https://www.nasa.gov/reference/5-4-product-validation/**.

El modelo no inventa títulos, páginas ni URLs. Internamente se conservan identificador de fragmento, documento, versión, texto recuperado y referencias de la revisión. La presentación muestra los metadatos originales, deduplicando localizaciones iguales. El catálogo exige página positiva para documentos o URL HTTPS para webs; no infiere páginas a partir del nombre del archivo. Si falta esa información, se debe completar desde la procedencia antes de usar v5, no inventarla.

`SourceLocation` comprueba formato y correspondencia de documento/versión con los fragmentos entregados. La autorización y procedencia del catálogo son responsabilidad del host y de la revalidación existente; este módulo no acredita por sí solo que un número de página corresponda al PDF original. Tampoco descarga URLs.

## Cableado y límites

- Nuevo contrato en [web_review_references.py](../../../../src/oralia/course_dialogue/web_review_references.py).
- Perfil registrado y conectado a `WebRoundRequest`, revisión, reparación y nueva revisión de `WebReviewRounds`.
- `source_locations` se entrega desde el host y se copia a objetos inmutables; una mutación posterior del diccionario del llamante no cambia la página registrada.
- Los metadatos viajan dentro del mismo JSON protegido que los pasajes. No se concatenan como instrucciones ni se rompen los delimitadores del renderer.
- Las referencias ajenas, duplicadas o con documento/versión incompatible se rechazan. Una declaración de contradicción docente sigue requiriendo señalar una fuente docente; eso comprueba identidad, no que la fuente realmente se oponga.
- `claim` es una descripción libre del punto cuestionado. El bucle usa la respuesta completa para reparar, no necesita calcular un recorte a partir de una cita exacta.
- No se modifican ni vuelven a interpretar ensayos anteriores. V1–V4 permanecen disponibles para reproducibilidad; v5 se selecciona explícitamente con su catálogo de localizaciones. No se cambia a ciegas el contrato de consumidores antiguos que todavía no aportan esos metadatos.

Ejemplo de uso desde el host:

```python
loop = WebReviewRounds(
    generator, critic,
    budget=budget, revalidate=revalidate,
    prompt_version="web-review/v5",
    source_locations=authorized_locations_by_fragment,
)
trace = await loop.process(base_request)
# trace["source_references"] contiene las fuentes consultadas.
# trace["reviews"][i]["references"] contiene las referencias de esa revisión.
```

Una referencia correcta no transforma una crítica falsa en verdadera. Se mantiene `publication_allowed=False`, `participant_display=None` e `independent_semantics=False`. No se conectó la ampliación externa automática a participantes. El formato de respuesta académica ya previsto en FR-019 sigue siendo una referencia general legible, no citas por frase.

## Validación

**160 pruebas CPU aprobadas**, incluyendo 21 nuevas comprobaciones parametrizadas/de integración sobre localizaciones, referencias y bucle. Proveedores simulados: no se cargaron pesos, no hubo inferencias ni GPU. Un aviso de deprecación Starlette existente permanece en el log.

Las pruebas cubren paráfrasis de la afirmación, ausencia de `quote`, documento/página y URL construidos por el host, fuente ajena, duplicados, conflicto docente sustentado solo por referencia externa, metadatos ausentes o incompatibles, página booleana, URL con credenciales/esquema inválido/espacios, escape de delimitadores y copia inmutable. La integración simulada realiza revisión → corrección → nueva revisión y conserva los límites de publicación. Otra prueba muestra expresamente que una crítica semánticamente falsa puede cumplir el contrato: este parser no es un evaluador de verdad.

Black conforme en cuatro archivos afectados. Ruff global mantiene diez diagnósticos previos, sin nuevos, comparados con multiplicidad frente al baseline. Coinciden los 308 hashes históricos, 140 del revisor anterior y 22 de fuentes/bancos; las copias de código de las mediciones previas permanecen intactas.

T174 acredita implementación y pruebas de cableado. **T175 sigue abierta:** falta observar el modelo real usando el nuevo contrato, con controles que midan apoyo y falsos permisos/rechazos, no solo formato. No se afirma que eliminar citas haya resuelto sus errores conceptuales ni se atribuye una mejora al modelo sin medirla. T168/T169 y Feature012 permanecen abiertos. No se cambiaron gates, corpus activo, datos habituales, servicios ni presupuestos históricos; sin Reset ni commits.
