export type RuntimeStatus = {
  expires_at_unix_ms: number; remaining_seconds: number; expired: boolean; renewable: false;
};
export type RuntimeClock = { status: RuntimeStatus; sampledAt: number } | null;
export type StudyQuota = { used: number; maximum: number | null; remaining: number | null; exhausted: boolean };

export function remainingRuntime(clock: RuntimeClock, now: number): number | null {
  return clock ? Math.max(0, clock.status.remaining_seconds - Math.max(0, now - clock.sampledAt) / 1000) : null;
}
export function runtimeExpired(clock: RuntimeClock, now: number): boolean {
  return clock !== null && (clock.status.expired || remainingRuntime(clock, now) === 0);
}
export function canSend(open: boolean, connected: boolean, ready: boolean, busy: boolean, question: string, clock: RuntimeClock, now: number, quota?: StudyQuota | null): boolean {
  return open && connected && ready && !busy && !!question.trim() && !runtimeExpired(clock, now) && (!quota || quota.remaining === null || quota.remaining > 0);
}
export function acceptResponse(version: number, current: number, clock: RuntimeClock, now: number): boolean {
  return version === current && !runtimeExpired(clock, now);
}
export class StudyApiError extends Error {
  constructor(message: string, public code: string, public status?: number) { super(message); }
}
export function failureMessage(error: unknown, clock: RuntimeClock, now: number): string {
  if (runtimeExpired(clock, now) || error instanceof StudyApiError && error.code === "runtime_expired") {
    return "El runtime global ha caducado y el servidor puede haberse detenido. Se necesita un nuevo arranque explícito; recargar el modelo o reabrir la inspección no renueva el plazo. No hay una respuesta completa confirmada para la petición pendiente. La pregunta se conserva solo en esta pestaña y no se reenviará automáticamente.";
  }
  if (error instanceof StudyApiError && error.code === "network") {
    return "Se ha perdido la conexión con el servidor local. No se puede confirmar si recibió o completó la pregunta; esto no demuestra un fallo del modelo. La pregunta se conserva solo en esta pestaña y no se reenviará automáticamente. Compruebe el servidor antes de volver a abrir la inspección.";
  }
  if (error instanceof StudyApiError && ["lease_expired", "inspection_closed"].includes(error.code)) {
    return "La inspección se ha cerrado o ha caducado por falta de conexión activa. Vuelva a abrirla con consentimiento. Esto no renueva el runtime global. La pregunta pendiente se conserva solo en esta pestaña.";
  }
  if (error instanceof StudyApiError && ["permission_expired", "inspection_invalidated"].includes(error.code)) {
    return "Permiso o fuentes invalidados; contenido diagnóstico retirado. La pregunta pendiente se conserva solo en esta pestaña.";
  }
  return error instanceof Error ? error.message : String(error);
}
export function generationMessage(status: string, code?: string | null): string {
  const reasons: Record<string, string> = {
    web_permission_revoked: "Cambió el permiso de Internet; la respuesta externa pendiente no se entrega.",
    web_scope_uncertain: "No se ha confirmado el alcance o la insuficiencia local. Precisa la pregunta.",
    web_no_evidence: "No se ha obtenido información externa utilizable.",
    web_review_unresolved: "No se ha podido contrastar suficientemente la información de Internet.",
    web_conflict: "Posible conflicto con el material docente; no se incorpora como explicación.",
    review_unresolved: "No he podido completar una respuesta revisada. Puedes precisar la pregunta o intentarlo más tarde.",
    question_too_long: "La pregunta es demasiado larga para buscar en los materiales. Prueba a dividirla o escribir una pregunta más breve. La conversación se conserva y no se ha consumido una llamada al modelo.",
    search_context_too_long: "La pregunta junto con su contexto anterior es demasiado larga para la búsqueda. Reformula brevemente indicando el concepto al que te refieres, o marca Cambiar de tema si quieres iniciar una duda independiente. La conversación se conserva y no se ha consumido una llamada al modelo.",
    no_passages: "No he encontrado pasajes con los que responder esta consulta. Puedes reformularla o consultar los documentos. Esto no significa que el tema esté fuera de la asignatura. La conversación se conserva y no se ha consumido una llamada al modelo.",
    budget_exhausted: "Cupo de llamadas agotado. Los reintentos que llegan al proveedor también cuentan; reabrir no lo renueva. No es un error académico.",
    model_unavailable: "El modelo está detenido o no disponible. Recárguelo explícitamente si queda tiempo y cupo; la pregunta no se reenviará sola.",
    source_changed: "Las fuentes cambiaron o se retiraron; no se usará evidencia obsoleta.",
    context_invalid: "El contexto no cumple el contrato técnico. Esto no significa que la pregunta sea académicamente incorrecta.",
    retrieval_error: "Falló la recuperación de pasajes; no es un error académico.",
    transport_error: "Falló el transporte con el worker; no hay respuesta completa. Compruebe si el modelo necesita recarga.",
    generation_timeout: "La generación alcanzó su plazo. El worker puede haberse detenido; compruebe si aparece Recargar modelo local.",
    generation_length_limit: "La respuesta quedó incompleta al alcanzar el límite de tokens. No se añade al historial; no es una evaluación académica de la pregunta.",
    candidate_too_large: "La respuesta supera el límite técnico de presentación y no se añade al historial.",
    runtime_expired: "El runtime global ha caducado; requiere un nuevo arranque explícito.",
    invalidated_unknown: "Petición invalidada por causa técnica no identificada; no permite atribuir un fallo a la pregunta o a su contenido académico.",
  };
  if (code && reasons[code]) return reasons[code];
  const messages: Record<string, string> = {
    provider_error: "El proveedor devolvió un error de generación; no hay respuesta completa.",
    timeout: "La petición alcanzó su plazo de generación; no hay respuesta completa.",
    cancelled: "Petición cancelada; no se añadirá una candidata tardía.",
    invalidated: "Petición invalidada; este servidor no facilita una causa específica. No hay base para atribuir un error académico.",
  };
  return messages[status] ?? `No hay respuesta completa: ${status}.`;
}
