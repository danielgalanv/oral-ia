# Feature Specification: Vinculación extractiva larga

**Feature Branch**: 009-long-extractive-binding (sin Git/commits)
**Created**: 2026-10-18
**Status**: Implementada y validada localmente, incluido T016; analyze sin críticos y converge sin brechas
**Input**: Corrección acotada autorizada por usuario «pide corregirlo», verificada leyendo
el turno original en Auditoría ORALIA — Supervisión SpecKit. No escritores concurrentes.

## User Scenarios & Testing

### User Story 1 — Responder con material largo autorizado (Priority: P1)

Docente carga el archivo04 original y participante pregunta por temperatura del agua.
**Why this priority**: La extracción legítima no debe cerrar la sesión por incompatibilidad interna.
**Independent Test**: Archivo original cargado/extraído/indexado por servicios reales; respuesta con fuentes y sesión utilizable.
**Acceptance Scenarios**:
1. Given archivo04 sin modificar, When se publica y pregunta «¿A qué temperatura hierve el agua?», Then autoestudio responde con evidencia, sin invalid_context ni cierre de error por el recorte legítimo.
2. Given longitudes antes/en/después de400 y múltiples fragmentos Unicode, When se presenta extracción permitida, Then su texto y procedencia/versión/ubicación corresponden a la fuente vigente.
3. Given sesión con respuesta válida, When se envía otro turno, Then sigue siendo utilizable.

### User Story 2 — Mantener autorización cerrada (Priority: P1)

El sistema solo vincula texto verificable y preserva T090 y saneamiento.
**Why this priority**: Evitar corregir disponibilidad a costa de autoridad inventada.
**Independent Test**: Mutaciones de texto/metadatos/scope fracasan con salida nula/fallback acotado.
**Acceptance Scenarios**:
1. Given texto alterado o recorte arbitrario, When intenta pasar por extractivo, Then no obtiene autoridad ni texto libre permitido.
2. Given material fuera de scope,versión/ubicación/procedencia incorrectas o no autorizado, When se propone salida, Then sigue bloqueado y saneado; fallback no recursivo.

### User Story 3 — Recorrido docente completo (Priority: P1)

Docente usa el documento largo sin alterar demo preparada ni base habitual.
**Why this priority**: La prueba de frontera debe llegar al navegador y privacidad.
**Independent Test**: Ambos modos y ámbitos de conservación/cierre/exportación/eliminación; navegador con archivo04 real.
**Acceptance Scenarios**:
1. Given ambos modos, When elige scopes distintos o efímero y cierra, Then T150 conserva solo lo autorizado y revisión/exportación/borrado no regresan.
2. Given navegador autenticado, When carga archivo04 y publica actividad, Then recorre sesión/fuentes/cierre/revisión/exportación/borrado con archivo largo.
3. Given entorno demo preparado, When ejecuta regresiones, Then datos habituales/demo y paquetes previos siguen intactos, sin Reset.

## Edge Cases

399/400/401 caracteres, palabras sin espacios,cadenas Unicode/combining/espacios,
1–3fragmentos,4fragmentos recuperados con límite de3, texto recortado falseado,
fragmentos distintos con texto igual, datos/metadatos desalineados, versión retirada,
scopes/disclosure denegados, política/catálogo ausentes, sin evidencia y fallback bloqueado.

## Requirements

- **FR-001**: Reproducir primero archivo04 original por carga/extracción/índice reales y registrar fallo previo; no acortar ni sustituirlo.
- **FR-002**: Permitir extracción legítima larga mediante vínculo estructurado con fuente vigente; no invalid_context por diferencia interna de recorte; sesión utilizable.
- **FR-003**: Comprobar longitudes antes/en/después400,múltiples fragmentos,Unicode,procedencia/versión/ubicación; conservar acotación y determinismo de extracción.
- **FR-004**: Solo texto exacto reconstruible de datos autorizados obtiene propuesta; mutaciones,texto libre,scope/procedencia/versión/ubicación ajenos se deniegan,con salida nula saneada y fallback acotado.
- **FR-005**: Mantener T090/T150,verificadores,plantillas/políticas existentes,consentimiento/scopes,acceso/aislamiento y cierre/exportación/borrado en ambos modos.
- **FR-006**: Recorrido navegador docente con carga real archivo04,actividad,turno/fuentes,cierre,revisión,exportación y eliminación verificable; no solo seed breve.
- **FR-007**: Preservar datos habituales/demo preparados sin Reset ni commits; registrar fuente/paquetes previos y regenerar/reproducir evidencia actual si manifiesto cambia.
- **FR-008**: Suite determinista global,build/lint/Playwright,check-demo,Black afectados,Ruff Counter con multiplicidad frente baseline durable; sin nuevas infracciones.
- **FR-009**: Actualizar materiales/docente/RESULTADO.md con causa,cambios,comandos,resultados medidos y límites una vez corregido; no afirmar soporte universal ni validación semántica/humana/voz.
- **FR-010**: Artefactos SpecKit trazables y cierre solo analyze sin críticos y converge sin brechas obligatorias.

## Key Entities

Proyección extractiva canónica versionada; referencia a fragmento/version/ubicación,
hash de fuente/rango y texto exacto permitido; autorización existente sin autoridad del generador.

## Success Criteria

- **SC-001**: El caso04 falla antes y pasa después con respuesta/fuentes reales y segundo turno usable.
- **SC-002**: Matriz de frontera/procedencia pasa y todas las mutaciones preparadas se deniegan sin escape de texto ni ampliación de fallback.
- **SC-003**: Matriz ambos modos/scopes y recorrido largo navegador pasan con privacidad/exportación/borrado.
- **SC-004**: Gates sin regresiones,nuevos Ruff0,paquetes originales/hashes y recursos estables intactos,evidencia actual reproducible.

## Assumptions / Clarifications

### Session 2026-10-18

Cero preguntas: autorización y caso delimitados. Auditoría en otro chat está idle; escritor
único aquí. Perfil canónico cerrado sin aceptar parámetros del modelo; conservar400/3
existentes. Sin nuevos agentes/modelos/descargas ni cambios generales de arquitectura.
No se atribuye utilidad docente ni semántica general a pasar esta matriz finita.

## Aclaración de auditoría de carga (2026-10-18)

FR-006/SC-003 incluye carga inicialmente lenta:espera de red explícita finita de la
prueba,estado ocupado accesible y rechazo de dobles envíos sin falsificar respuesta.
El fallo independiente agotó15s,pero la DB temporal conserva04como processed,sin error;
no se interpreta como fallo del recorte ni como causa de latencia determinada. Medir
request/response de un proceso recién iniciado. Ensayo de entrega retardada explícito
usa respuesta real,sin reintento/skip ni sustituir contenido. Cualquier error sigue visible.
