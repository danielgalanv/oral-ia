# Decisión de ampliación web — 30-10-2026

## Decisión humana incorporada

El usuario autoriza que el autoestudio busque en Internet cuando falte información, advierta
su procedencia, contraste su validez y compruebe que no contradice el material docente.
Se registra como ampliación del mismo RAG, no como respuesta desde memoria del modelo ni
como navegación abierta. El examen no recibe este permiso automáticamente.

## Enmienda y sincronización

Constitución **1.0.0 → 2.0.0**. Cambio MAJOR porque introduce una excepción incompatible con
la exclusión general anterior de Internet durante sesiones y con la recuperación siempre
local. Se limita a documentación pública de autoestudio, por política de actividad, con
generación/revisión locales y consultas mínimas sin datos privados. Se conserva la fecha de
ratificación 2026-07-21 y se fija Last Amended en 2026-10-30. La instrucción humana es la
autorización para esta enmienda de desarrollo; el producto no cambia su gobernanza durante
una sesión de alumno.

Se sincronizaron spec FR-014/016/019 y FR-021–024, SC-009, plan, tareas T114–T118 pendientes,
contrato RAG, contrato web nuevo, README de proyecto, guía SpecKit y adenda del plan general.
La plantilla plan incluye los controles web pertinentes; spec/tasks templates son genéricas
y siguen compatibles. Se revisaron las diez skills SpecKit instaladas: la única mención
«CLAUDE-only» es el propio ejemplo de comprobación de la skill constitucional, no una
restricción operativa que requiera cambiarla. `docs/MVP.md` describe sesiones que no
requieren Internet: sigue siendo cierto para los perfiles existentes.

## Reglas materiales

- Primero, material local y ámbito de la asignatura. No convertir ausencia o score en
  exclusión del temario. Solo una política habilitada permite la ampliación externa.
- Informar del acceso externo y separar «Información de Internet» con títulos/enlaces de
  «Material del profesor». El enlace por sí solo no prueba validez.
- Revisar procedencia, autoría, contexto, vigencia pertinente y respaldo. Corroborar cuando
  sea necesario; duplicados no son fuentes independientes y no se impone un número mágico
  de páginas como garantía de verdad.
- Comparar afirmaciones con material docente pertinente y documentar qué se pudo revisar,
  ampliando más allá del top-k inicial cuando proceda. Una cuarentena o un documento no
  leído limita la conclusión de compatibilidad.
- Si aparece conflicto, no sustituir silenciosamente al profesor ni afirmar que sus textos
  sean infalibles: señalar la discrepancia y no incorporar la afirmación afectada como
  contenido establecido. Si el respaldo o contraste no se resuelve, indicar incertidumbre.
- Consultas mínimas sobre conceptos; no enviar historial, PDFs privados, datos personales,
  identificadores, audio o credenciales. Descargas públicas acotadas y cancelables,
  protección de destinos/redirects e instrucciones maliciosas, caché versionada/revocable.

## Estado real

**Cambio documental y de política, no implementación.** Los perfiles actuales siguen sin
acceso externo. T114–T118 continúan sin marcar; no se ha implementado un buscador ni
acreditado un verificador semántico. No se realizaron peticiones de red, inferencias,
instalaciones, cambios de runtime, migraciones o commits. No se alteran sesiones, índices,
resultados históricos, gates o consentimiento anterior.

Siguiente bloque: política/recibos y pruebas CPU con HTTP simulado, después adquisición y
contraste medido. La decisión de proveedor y los límites efectivos se fijarán antes del
ensayo correspondiente; no se presupone que los conectores de este chat estén disponibles
dentro del producto ni se solicita una credencial sin necesidad.

## Validación

Versión/fechas, ausencia de placeholders, 76 IDs de tareas únicos, T114–T118 pendientes,
requisitos nuevos y diez snapshots previos con hashes verificados en `validation.json`.
La comprobación de FR usó inicialmente un formato de ID sin ceros y falló; se corrigió
el comprobador, no se modificaron requisitos para hacerlo pasar.

No existe `.specify/extensions.yml`: no hay hooks constitucionales previos/posteriores.
Las diez copias previas se conservan en `before/`; la adenda al plan consolidado mantiene
el texto anterior fechado sin reinterpretar ensayos. Sin pruebas de modelos ni afirmaciones
de funcionamiento web real en esta entrega. La validación es documental, no un dictamen
de convergencia de Feature012.

[Contrato de implementación](../../../specs/012-conversational-course-study/contracts/web-evidence-fallback.md)
