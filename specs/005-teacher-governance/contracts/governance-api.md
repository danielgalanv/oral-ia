# Contrato de gobierno local — v1



Todas las rutas /api/v1 exigen autorización salvo health, login, creación de sesión

participante y descripción pública de actividad. Docente: bearer de instalación o

cookie de acceso emitida por login; participante: token secreto de su sesión, nunca

solo su código. 401 sin token/expirado, 403 rol/origen/propiedad, 503 sin instalación.

Todas las respuestas de revisión/exportación/autenticación llevan Cache-Control no-store.



| Ruta | Actor y resultado |

|---|---|

| POST /api/v1/auth/login | {secret}, cookie HttpOnly/SameSite y expiración; errores genéricos |

| POST /api/v1/auth/logout | revoca token/cookie, idempotente |

| GET /api/v1/auth/me | rol y expiración, sin secreto |

| POST /api/v1/sessions | inicia por versión publicada; entrega token de propietario/cookie y aviso de privacidad |

| GET /api/v1/governance/activities | docente, versiones completas saneadas y ciclo |

| POST /api/v1/governance/activities | docente, nueva configuración con retención finita, modo, modelo, agentes/materiales; borrador |

| POST /api/v1/governance/activities/{id}/duplicate | docente, nueva familia o versión con procedencia; valores validados |

| POST /api/v1/governance/activities/{id}/activate | docente, valida fuentes/modelos/controles; activa y retira anterior |

| POST /api/v1/governance/activities/{id}/retire | docente, no nuevos inicios; historia intacta |

| GET /api/v1/governance/catalog | modelos/agentes disponibles y estados de material/índice |

| POST /api/v1/sessions/{id}/privacy | propietario, {retain,scope}; solo activa y autorización/plazo finitos |

| GET /api/v1/sessions/{id}/privacy | propietario, aviso/scopes/plazo/elección y resultado |

| GET /api/v1/governance/sessions | docente, solo consentidas cerradas vigentes no eliminadas |

| GET /api/v1/governance/sessions/{id} | docente, revisión por scope; 404 no revisable |

| POST /api/v1/governance/exports | docente, ids[1..100], format json|markdown, include_free_text, reviewed_free_text; 409 si texto sin revisión, rechazo de lote mixto |

| DELETE /api/v1/sessions/{id}/content | docente o propietario, {confirm:true}; 409 activa, recibo sin contenido y comprobación |

| POST /api/v1/governance/purge | docente, contadores de expiración; sin tocar vigente/materiales |

| GET /api/v1/governance/metrics | docente, agregado de funcionamiento y faltantes, nunca por participante |



Las rutas históricas técnicas son administrativas y sus vistas de contenido también

se filtran por consentimiento. El contenido de sesiones ajenas nunca es accesible con

token participante. Acceso a materiales administrativos solo docente.



UI: /gobierno con login/logout, formulario versionado, publicación y retiro, listado

consentido, detalle con secciones inequívocas, revisión de texto libre, descarga JSON/

Markdown, confirmación de borrado y métricas. La UI participante conserva token en

memoria/cookie, no localStorage, y ofrece revisión/privacidad/eliminación por texto.



La política limita content_scope a transcript, summary o ambos; access_scope puede

ser local_teacher o participant_only. Este último bloquea revisión/exportación docente,

no la revisión propia autorizada. Materiales fijados por documento/versión; el catálogo

de índice declara integrity_verified=false hasta comprobación específica.

