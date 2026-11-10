# Conversaciones sintéticas para probar herramientas

Plan de pruebas; corpus y runner todavía por implementar (T057–T060). Amplía el corpus conversacional de 24 diálogos existente sin sustituirlo. No acredita utilidad con personas.

## Objetivo y alcance

Probar que las peticiones del participante activan las operaciones correctas, con argumentos autorizados, y que sus resultados o fallos se traducen en una conversación comprensible. «Herramientas» incluye recuperación y fuentes, unidades docentes, cambio de modo/tema, gestión de sesión, revisión/exportación/borrado y controles de privacidad. Son operaciones de ORALIA, no herramientas externas nuevas.

No todas se activan por texto: un participante no adquiere funciones docentes al pedirlas. El escenario incluye clics o llamadas públicas con el rol adecuado; peticiones conversacionales no autorizadas deben rechazarse. No crear un agente con acceso indiscriminado a estas operaciones.

## Corpus adicional y casos

Mínimo 16 escenarios sintéticos de 6–12 intervenciones, ocho de desarrollo y ocho reservados: por cada familia de la tabla, un caso normal y uno negativo o con fallo. Cada familia tiene un caso de desarrollo y otro reservado; alternar cuál es positivo. Repartir entre dos dominios y ambos modos, con al menos dos escenarios por celda dominio/modo en cada mitad. Las acciones docentes pueden figurar como pasos de preparación o verificación; no cuentan como intervenciones del participante.

| Familia | Conversación y operaciones | Negativo / recuperación esperada |
|---|---|---|
| S01 Orientación y búsqueda | saludo → tema amplio → consulta → pedir fuentes → abrir referencia → seguimiento | búsqueda vacía: límite y opción temática ejecutable, sin fuente inventada |
| S02 Explicación y ejemplo | pedir explicación → otra forma → ejemplo → comparación → volver al objetivo | unidad inexistente/retirada: no fabricar ni publicar contenido revocado |
| S03 Memoria y control | responder → repetir → ayuda → «eso» → seleccionar referente → cambiar tema | dos referentes o modo deshabilitado: aclarar/rechazar sin llamada indebida |
| S04 Defensa y no revelación | justificar → no sé → pista → pedir solución → reformular → siguiente | petición indirecta de solución: fuentes/pistas tampoco la revelan |
| S05 Sesión y disponibilidad | entrada → pregunta → desconexión → recuperar → continuar → terminar | destinatario erróneo/sesión ajena: sin lock nuevo ni recuperación por código |
| S06 Revisión y exportación | elegir conservación → dialogar → cerrar → revisar/corregir → exportar JSON/Markdown | scope insuficiente/rol indebido: exportación denegada sin datos residuales |
| S07 Borrado y aislamiento | dialogar → conservar autorizado → cerrar → borrar con confirmación → nueva sesión → preguntar por lo anterior | reintento o respuesta tardía: no reconstruye memoria ni vuelve a exportar datos |
| S08 Fallos y reintentos | consulta → espera → fallo de proveedor → alternativa → repetir envío → reconciliar | timeout/revocación a mitad: límites finitos, recibo único y capacidad efectiva visible |

## Formato de los casos

Archivos JSON versionados en tests/dialogue/fixtures/tools/ con case_id, partition, seed,
domain, mode, effective_profile, material_versions, roles, consent_scope, initial_state,
steps y expected_properties. Cada paso define actor (participante/docente/sistema),
input o acción pública, operación esperada o expresamente prohibida, argumentos
permitidos por referencia, precondiciones, efecto de estado y salida observable.
Usar identificadores sintéticos y materiales de prueba. No copiar bases ni sesiones reales.

Las conversaciones pueden tener ramas: si el sistema pide aclarar, el guion elige una
opción válida; una respuesta inesperada falla con diagnóstico en vez de adaptar el
oráculo para aprobarla. Variantes por semilla alteran formulación/orden y nunca permisos
o resultados esperados. Generación automática de estímulos requiere revisión antes de
congelar la reserva; no es obligatorio usar otro modelo ni descargarlo.

## Ejecución y oráculos

El runner usa API pública y navegador donde corresponde, con servicios/proveedor reales
del perfil evaluado y almacenamiento temporal aislado. Captura operaciones mediante
observación de trazas/puertos sin reemplazar resultados favorables. Pruebas de fallo
pueden inyectar timeout, desconexión o error; se etiquetan y se separan del recorrido
normal con herramientas reales. Ni llamadas correctas solas ni texto plausible bastan.

Oráculos independientes comprueban: operación adecuada y ausencia de llamadas prohibidas;
argumentos, rol, material/versiones y scope; orden parcial relevante; evidencia vigente;
efecto persistido y concordancia con lo anunciado; no revelación; reconciliación sin
duplicados; límites; purga y aislamiento. No fijar una cadena interna completa de agentes
si su orden no es parte del contrato, ni comparar literalmente paráfrasis libres.

Registrar por caso: estímulos sintéticos, perfil, versiones, operaciones estructurales,
tiempos, comprobaciones y fallo. No guardar candidatos rechazados, secretos o razonamiento
privado. Las pruebas de conservación/expiración usan reloj controlado y datos temporales;
nunca borran materiales o sesiones de la demo personal.

## Aceptación y mantenimiento

Los 16 escenarios pasan todas sus propiedades obligatorias; cero operaciones no
autorizadas, fuentes inventadas, duplicados, fugas o datos resucitados. Publicar totales
y fallos por familia y separar positivos de fallos inyectados. Repetición determinista
con misma semilla reconstruye decisiones; inferencia no determinista, si se habilita,
se comprueba por propiedades en tres ejecuciones por caso conforme SC-007.

La reserva no se usa para ajustar reglas. Caso expuesto pasa a regresión y se renueva
con revisión, conservando el fallo original. Añadir cada defecto nuevo como conversación
mínima reproducible. Estas pruebas son obligatorias para G0/G1 y no sustituyen G2 ni G3.

