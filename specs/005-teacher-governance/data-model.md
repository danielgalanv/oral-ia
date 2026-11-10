# Modelo de datos — Feature 005



Se reutilizan ActivityConfiguration, RetentionPolicy (versionadas), Session, Turn,

ConsentRecord, Transcript/Correction y todas las identidades T090/T150.



## ActivityGovernance (nuevo)

activity_configuration_id PK/FK, family_id, version (unicidad familia/versión),

status draft|active|retired, model_id (local disponible), material_versions JSON

con document_id/version, created_at. Publicación solo docente; datos usados inmutables

salvo status. Activar retira activa previa de familia en una transacción; retirada no

borra configuraciones ni sesiones. Selección de agentes permanece en campos existentes.



## SessionPrivacyPreference (nuevo)

session_id PK/FK, retain bool, scope JSON cerrado transcript/summary, updated_at.

Solo propietario durante sesión activa; no equivale a ConsentRecord ni autoriza una

actividad. Cierre ganador registra consentimiento real y aplica scopes/plazo.



## SessionDeletionReceipt (nuevo)

session_id PK/FK, reason user_request|expiry|no_consent, deleted_at y counts JSON

solo conteos. Es idempotente; no copia respuestas, código participante ni contenido.

El recibo de borrado total excluye revisión/exportación. Borrado parcial por scopes

conserva el scope restante según consentimiento y política finita.



## Access credentials (efímero, no tabla)

hash de token, role, session_id opcional, monotonic expiry. Secreto en entorno,

no en la base. Reinicio/logout invalidan tokens. Separación de identidad real intacta.



## ExportBundle (efímero)

schema_version=1, alias lote, configuración/versiones saneadas, transcripción si scope,

resumen si scope, fuentes y traza con campos permitidos. No raw ORM, audio, secrets,

prompts o candidatos bloqueados. JSON/Markdown provienen de la misma proyección.



## Eliminación y transacciones

Contenido de Turn, GeneratedProposal, CognitiveState, StatePatch, InternalMessage,

PracticeQuestion, CoherenceIncident, GroundingVerificationResult y TraceEvent se

elimina o sanea por identidad de sesión. Los materiales autorizados no son contenido

del participante y no se borran. Las filas técnicas mínimas retienen IDs/versiones,

acciones y veredictos, nunca texto eliminado. Cierre T150 y commit exterior existentes.



## Metadatos mínimos y coherencia al cerrar



ActivityGovernance añade índice único parcial de family_id cuando status=active.

Se congelan selección de material y modelo de actividades históricas al primer uso.

Los materiales seleccionados se comprueban también al recuperar/reutilizar evidencia.



Los modos base/autoestudio pueden retener filas vacías de CognitiveState/InternalMessage/

PracticeQuestion como recibos de versión, pasos, intentos y tipos; se retiran todos los

campos de contenido, objetivos copiados, conceptos, hipótesis y texto. CoherenceIncident

ya contiene solo tipo/acción del sistema. Los TraceEvent se proyectan por claves técnicas

permitidas; study_session_summary sin scope retiene solo contador de turnos/duración.

La defensa conserva su eliminación previa de filas operativas además del recibo común.

Estos metadatos no son una vía de consulta de texto ni un permiso de revisión docente.



La preferencia es de sesión activa. El cierre voluntario recibe una elección efímera

aplicada solo por el ganador; no escribe una elección perdedora. El consentimiento

confirmado gobierna las vistas cerradas. Las exportaciones no incluyen estos blobs de

estado, prompts o contenido de mensajes; parten de la proyección revisable.



ActivityGovernance.source_activity_configuration_id es FK nullable a la configuración

de origen, también al duplicar como familia nueva. RetentionPolicy.content_scope se cruza

con la elección explícita; access_scope=participant_only excluye vistas y exportaciones

docentes aunque el propietario conserve su derecho de revisión. Ningún scope desconocido

concede acceso. Índice único parcial: una versión active por family_id.

