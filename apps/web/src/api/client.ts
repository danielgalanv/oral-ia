// Thin, typed client over the local API — contracts/api-participante.md and
// contracts/api-tecnica.md. No cognitive logic lives in the frontend (plan.md).

const BASE = "/api/v1";

export class ApiError extends Error {
  constructor(
    public status: number,
    public detail: string,
    public code?: string,
  ) {
    super(`API error ${status}: ${detail}`);
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    const detail = body.detail;
    const message = typeof detail === "string"
      ? detail
      : typeof detail?.message === "string"
        ? detail.message
        : detail === undefined ? res.statusText : JSON.stringify(detail);
    throw new ApiError(res.status, message, typeof detail?.code === "string" ? detail.code : undefined);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

export class UnknownTurnResult extends Error {
  constructor(public requestId: string, public reconcile: () => Promise<unknown>) {
    super("No se ha podido confirmar el resultado. Consulta el envío antes de volver a enviar contenido.");
  }
}

async function requestTurn<T>(sessionId: string, path: string, payload: object): Promise<T> {
  const requestId = crypto.randomUUID();
  const init = { method: "POST", body: JSON.stringify({ ...payload, client_request_id: requestId }) };
  try {
    return await request<T>(path, init);
  } catch (error) {
    if (error instanceof ApiError && error.status < 500) throw error;
    // Keep identity/payload only in this page's memory. Querying never creates a
    // turn. Only a confirmed receipt permits projecting the same committed turn.
    throw new UnknownTurnResult(requestId, async () => {
      const receipt = await request<{ status: string }>(`/sessions/${sessionId}/requests/${requestId}`);
      if (receipt.status !== "completed") throw new Error("El resultado todavía no está confirmado.");
      return request<T>(path, init);
    });
  }
}

// --- Área técnica --------------------------------------------------------

export interface ActivityConfigurationInput {
  course_id: string;
  name: string;
  subject: string;
  objective: string;
  mode: string;
  language: string;
  max_turns: number;
  max_duration_seconds: number;
  retention_policy_id: string;
  general_knowledge_allowed?: boolean;
  required_agent_ids?: string[];
  optional_agent_ids?: string[];
}

export interface ActivityConfigurationSummary {
  id: string;
  family_id: string;
  version: number;
  name: string;
  immutable_since: string | null;
}

export function createActivity(
  data: ActivityConfigurationInput,
  familyId?: string,
): Promise<ActivityConfigurationSummary> {
  const qs = familyId ? `?family_id=${encodeURIComponent(familyId)}` : "";
  return request(`/activities${qs}`, {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export interface AgentDescriptor {
  id: string;
  name: string;
  version: string;
  capabilities: string[];
  availability_status: string;
}

export function listCatalogAgents(): Promise<AgentDescriptor[]> {
  return request("/catalog/agents");
}

export interface AgencySummary {
  id: string;
  name: string;
  version: string;
  availability_status: string;
}

export function listCatalogAgencies(): Promise<AgencySummary[]> {
  return request("/catalog/agencies");
}

export interface SessionSummary {
  id: string;
  status: string;
  started_at: string;
  ended_at: string | null;
  turn_count: number;
}

export function listSessions(status?: string): Promise<SessionSummary[]> {
  const qs = status ? `?status=${encodeURIComponent(status)}` : "";
  return request(`/sessions${qs}`);
}

export function getSessionDetail(sessionId: string): Promise<unknown> {
  return request(`/sessions/${sessionId}`);
}

export function getSessionTrace(sessionId: string): Promise<unknown> {
  return request(`/sessions/${sessionId}/trace`);
}

// --- Materiales autorizados y RAG (Feature 002) -----------------------------

export interface MaterialDocumentSummary {
  id: string;
  family_id: string;
  version: number;
  course_id: string;
  activity_configuration_ids: string[];
  filename: string;
  content_hash: string;
  mime_type: string;
  size_bytes: number;
  status: string;
  error_detail: string | null;
  retired_at: string | null;
  duplicate_of_document_id: string | null;
  created_at: string;
}

export interface MaterialCoverageSummary {
  total_documents: number;
  by_status: Record<string, number>;
  processed_count: number;
  error_count: number;
}

export interface MaterialDocumentDetail extends MaterialDocumentSummary {
  course_coverage: MaterialCoverageSummary;
}

export interface DuplicateConflict {
  existingDocumentId: string;
  conflictToken: string;
}

export async function uploadMaterial(
  courseId: string,
  file: File,
  activityConfigurationIds: string[] = [],
): Promise<MaterialDocumentSummary | { duplicate: DuplicateConflict }> {
  const form = new FormData();
  form.append("course_id", courseId);
  form.append("file", file);
  activityConfigurationIds.forEach((id) =>
    form.append("activity_configuration_ids", id),
  );

  const res = await fetch(`${BASE}/materials/documents`, {
    method: "POST",
    body: form,
  });
  const body = await res.json().catch(() => ({}));
  if (res.status === 409) {
    return {
      duplicate: {
        existingDocumentId: body.existing_document_id,
        conflictToken: body.conflict_token,
      },
    };
  }
  if (!res.ok) throw new ApiError(res.status, body.detail ?? res.statusText);
  return body as MaterialDocumentSummary;
}

export function listMaterials(
  courseId?: string,
): Promise<MaterialDocumentSummary[]> {
  const qs = courseId ? `?course_id=${encodeURIComponent(courseId)}` : "";
  return request(`/materials/documents${qs}`);
}

export function getMaterialDetail(
  documentId: string,
): Promise<MaterialDocumentDetail> {
  return request(`/materials/documents/${documentId}`);
}

export function activateMaterial(
  documentId: string,
): Promise<MaterialDocumentSummary> {
  return request(`/materials/documents/${documentId}/activate`, {
    method: "POST",
  });
}

export function deactivateMaterial(
  documentId: string,
): Promise<MaterialDocumentSummary> {
  return request(`/materials/documents/${documentId}/deactivate`, {
    method: "POST",
  });
}

export function resolveDuplicate(
  conflictToken: string,
  resolution: "link_existing" | "proceed_new",
): Promise<MaterialDocumentSummary> {
  return request(`/materials/documents/${conflictToken}/duplicate-resolution`, {
    method: "POST",
    body: JSON.stringify({ resolution }),
  });
}

export interface MaterialConflictRecordSummary {
  id: string;
  document_ids: string[];
  fragment_ids: string[];
  conflicting_claims: string[];
  detected_by_query: string;
  review_status: string;
  created_at: string;
  reviewed_at: string | null;
}

export function listMaterialConflicts(): Promise<
  MaterialConflictRecordSummary[]
> {
  return request("/materials/conflicts");
}

export function reviewMaterialConflict(
  conflictId: string,
): Promise<MaterialConflictRecordSummary> {
  return request(`/materials/conflicts/${conflictId}/review`, {
    method: "POST",
  });
}

// --- Área participante -----------------------------------------------------

export interface DialogueStatus {
  screenless_text_ready?: boolean;
  conservation?: DefenseClosureConsent | null;
  available_modes?: string[];
  pending_question?: { turn_id: string; text: string } | null;
  ready_for_entry?: boolean;
  readiness_detail?: string | null;
  configured_profile?: string;
  effective_profile: string;
  provider: string;
  available_topics?: string[];
  pending_topic?: string | null;
}

export interface DialogueControl {
  schema_version: 2;
  action: "repeat" | "rephrase" | "help" | "continue" | "example" | "comparison" | "topic_switch" | "mode_switch" | "finish";
  requested_mode?: "doubt_resolution" | "guided_explanation" | "practice_questions" | "presentation_preparation" | "concept_review";
  requested_topic?: string;
}

export interface StartSessionResponse {
  dialogue_status?: DialogueStatus;
  access_token?: string;
  privacy_notice?: string;
  session_id: string;
  ai_disclosure: string;
  activity: {
    name: string;
    objective: string;
    max_turns: number;
    max_duration_seconds: number;
    capabilities?: DialogueStatus;
  };
}

export function startSession(
  participantCode: string,
  activityConfigurationId: string,
): Promise<StartSessionResponse> {
  return request("/sessions", {
    method: "POST",
    body: JSON.stringify({
      participant_code: participantCode,
      activity_configuration_id: activityConfigurationId,
    }),
  });
}

export interface SubmitTurnResponse {
  session_status?: string;
  turn_id: string;
  dialogue_action: string;
  output_text: string | null;
  blocked?: boolean;
  state_version?: number;
}

export function submitTurn(
  sessionId: string,
  text: string,
  consent?: DefenseClosureConsent,
): Promise<SubmitTurnResponse> {
  return request(`/sessions/${sessionId}/turns`, {
    method: "POST",
    body: JSON.stringify({ text, closure_consent: consent }),
  });
}

export interface EndSessionResponse {
  session_id: string;
  status: string;
  confirmation_message: string;
}

export function endSession(
  sessionId: string,
  consent?: DefenseClosureConsent,
): Promise<EndSessionResponse> {
  return request(`/sessions/${sessionId}/end`, {
    method: "POST",
    body: consent ? JSON.stringify(consent) : undefined,
  });
}

// --- Agencia de autoestudio (Feature 003) -----------------------------------

export interface StudySource {
  document_id: string;
  document_version: number;
  location_ref: string;
  fragment_text: string;
}

export interface SubmitStudyTurnResponse {
  request_replayed?: boolean;
  replay_content_withheld?: boolean;
  dialogue_status?: DialogueStatus | null;
  turn_id: string;
  mode: string;
  dialogue_action: string;
  output_text: string | null;
  state_version: number | null;
  sources: StudySource[];
  general_knowledge_used: boolean;
  blocked?: boolean;
  session_closed?: boolean;
  session_status?: string;
  study_summary?: StudySummary | null;
}

export function submitStudyTurn(
  sessionId: string,
  text: string,
  consent?: DefenseClosureConsent,
  control?: DialogueControl,
): Promise<SubmitStudyTurnResponse> {
  return requestTurn(sessionId, `/sessions/${sessionId}/study-turns`, { text, closure_consent: consent, dialogue_control: control });
}

export type StudySummary = Record<string, unknown>;

export interface EndStudySessionResponse {
  session_id: string;
  status: string;
  study_summary: StudySummary | null;
}

export function endStudySession(
  sessionId: string,
  consent?: DefenseClosureConsent,
): Promise<EndStudySessionResponse> {
  return request(`/sessions/${sessionId}/study-end`, {
    method: "POST",
    body: consent ? JSON.stringify(consent) : undefined,
  });
}

// --- Agencia de defensa oral (Feature 004) ---------------------------------

export interface DefenseActivityConfigurationInput {
  initial_questions: string[];
  topics: string[];
  difficulty_hint: "baja" | "media" | "alta";
  voice_input_allowed: boolean;
  voice_output_allowed: boolean;
  summary_authorized: boolean;
  transcript_retention_authorized: boolean;
  output_authorization_policy?: Record<string, unknown>;
}

export interface DefenseActivityConfiguration extends Omit<
  DefenseActivityConfigurationInput,
  "output_authorization_policy"
> {
  id: string;
  activity_configuration_id: string;
}

export function configureDefenseActivity(
  activityId: string,
  data: DefenseActivityConfigurationInput,
): Promise<DefenseActivityConfiguration> {
  return request(`/tecnica/activities/${activityId}/defense-config`, {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export interface DefenseSpeechDescriptor {
  available: true;
  url: string;
  media_type: "audio/wav";
  text_sha256: string;
}

export interface DefenseTurnResponse {
  request_replayed?: boolean;
  replay_content_withheld?: boolean;
  dialogue_status?: DialogueStatus | null;
  defense_summary: Record<string, unknown> | null;
  session_status: string;
  turn_id: string;
  dialogue_action: "ask" | "clarify" | "acknowledge_missing_info" | "finish";
  dialogue_purpose: "deepen_current_topic" | "switch_topic" | null;
  output_text: string | null;
  state_version: number | null;
  sources: StudySource[];
  general_knowledge_used: boolean;
  blocked: boolean;
  speech: DefenseSpeechDescriptor | null;
}

export interface DefenseTranscriptResponse {
  transcript_id: string;
  raw_text: string;
  segments: Array<{
    text: string;
    start_ms: number | null;
    end_ms: number | null;
    confidence: number;
  }>;
  overall_confidence: number;
  low_confidence: boolean;
}

export interface DefenseClosureConsent {
  retain: boolean;
  scope: string[];
}

export function submitDefenseTurn(
  sessionId: string,
  text: string,
  closureConsent?: DefenseClosureConsent,
  control?: DialogueControl,
): Promise<DefenseTurnResponse> {
  return requestTurn(sessionId, `/defense-sessions/${sessionId}/defense-turns`, { text, closure_consent: closureConsent, dialogue_control: control });
}

export async function submitDefenseVoice(
  sessionId: string,
  audio: Blob,
): Promise<DefenseTranscriptResponse> {
  const form = new FormData();
  const extension = audio.type.includes("webm") ? "webm" : "wav";
  form.append("audio", audio, `answer.${extension}`);
  const response = await fetch(
    `${BASE}/defense-sessions/${sessionId}/defense-turns/voice`,
    {
      method: "POST",
      body: form,
    },
  );
  if (!response.ok) {
    const body = await response
      .json()
      .catch(() => ({ detail: response.statusText }));
    throw new ApiError(
      response.status,
      JSON.stringify(body.detail ?? response.statusText),
    );
  }
  return (await response.json()) as DefenseTranscriptResponse;
}

export function confirmDefenseTranscript(
  sessionId: string,
  transcriptId: string,
  correctedText: string | null,
  closureConsent?: DefenseClosureConsent,
): Promise<DefenseTurnResponse> {
  return request(`/defense-sessions/${sessionId}/defense-turns/voice/confirm`, {
    method: "POST",
    body: JSON.stringify({
      transcript_id: transcriptId,
      corrected_text: correctedText,
      closure_consent: closureConsent,
    }),
  });
}

export async function requestDefenseSpeech(
  descriptor: DefenseSpeechDescriptor,
  signal?: AbortSignal,
): Promise<Blob> {
  const response = await fetch(descriptor.url, {
    method: "POST",
    cache: "no-store",
    signal,
  });
  if (!response.ok) throw new ApiError(response.status, response.statusText);
  return await response.blob();
}

export interface EndDefenseSessionResponse {
  session_id: string;
  status: string;
  defense_summary: Record<string, unknown> | null;
}

export function getDefenseSettings(sessionId: string): Promise<{
  allowed_retention_scopes?: string[];
  low_confidence_threshold: number;
  voice_input_allowed: boolean;
  voice_output_allowed: boolean;
  transcript_retention_authorized: boolean;
}> {
  return request(`/defense-sessions/${sessionId}/settings`);
}

export function endDefenseSession(
  sessionId: string,
  consent = { retain: false, scope: [] as string[] },
): Promise<EndDefenseSessionResponse> {
  return request(`/defense-sessions/${sessionId}/defense-end`, {
    method: "POST",
    body: JSON.stringify(consent),
  });
}

export function getDefenseTrace(
  sessionId: string,
): Promise<Record<string, unknown>> {
  return request(`/tecnica/defense-sessions/${sessionId}/defense-trace`);
}

export interface DefenseSessionTranscript {
  turns: Array<{
    turn_id: string;
    input_text: string;
    output_text: string | null;
  }>;
  transcripts: Array<{
    transcript_id: string;
    turn_id: string | null;
    raw_text: string;
    corrections: string[];
  }>;
}
export function getDefenseTranscript(
  sessionId: string,
): Promise<DefenseSessionTranscript> {
  return request(`/defense-sessions/${sessionId}/defense-transcript`);
}

export function governanceRequest<T>(
  path: string,
  data?: unknown,
  method = data === undefined ? "GET" : "POST",
): Promise<T> {
  return request(path, {
    method,
    body: data === undefined ? undefined : JSON.stringify(data),
  });
}
export async function downloadSessionExport(
  ids: string[],
  format: "json" | "markdown",
  includeFreeText: boolean,
  reviewed: boolean,
): Promise<Blob> {
  const response = await fetch(`${BASE}/governance/exports`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_ids: ids,
      format,
      include_free_text: includeFreeText,
      reviewed_free_text: reviewed,
    }),
  });
  if (!response.ok)
    throw new ApiError(
      response.status,
      "No se pudo exportar la selección autorizada.",
    );
  return response.blob();
}
export interface SessionPrivacyView {
  allowed_scopes?: string[];
  retention_authorized: boolean;
  retention_days: number | null;
  notice: string;
  retain: boolean;
  scope: string[];
  deleted: boolean;
}
