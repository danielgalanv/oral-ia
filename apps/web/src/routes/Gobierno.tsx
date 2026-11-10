import { FormEvent, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { TeacherSessionRecovery } from "../components/SessionRecovery";
import {
  ApiError,
  downloadSessionExport,
  governanceRequest,
} from "../api/client";

type Activity = {
  id: string;
  family_id: string;
  version: number;
  name: string;
  subject: string;
  objective: string;
  mode: string;
  language: string;
  course_id: string;
  max_turns: number;
  max_duration_seconds: number;
  status: string;
  model_id: string;
  retention_days: number | null;
  retention_content_scope?: string;
  retention_access_scope?: string;
  material_versions: MaterialRef[];
  mode_config?: Record<string, unknown>;
  output_authorization_policy?: Record<string, unknown>;
};
type MaterialRef = { document_id: string; version: number };
type Catalog = {
  index_status: {
    status: string;
    version: string | null;
    integrity_verified: boolean;
  };
  models: string[];
  compositions: Record<string, string[]>;
  courses: { id: string; name: string }[];
  materials: (MaterialRef & {
    filename: string;
    course_id: string;
    status: string;
    fragments_indexed: number;
    error_code?: string | null;
  })[];
  output_templates: {
    template_id: string;
    version: number;
    topic_ref: string;
    purpose_ref: string;
    action_ref: string;
    message_type: string;
  }[];
};
type SessionRow = {
  session_id: string;
  status: string;
  scope: string[];
  turn_count: number;
};

export default function Gobierno() {
  const [authenticated, setAuthenticated] = useState(false);
  const [secret, setSecret] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [catalog, setCatalog] = useState<Catalog | null>(null);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [sessions, setSessions] = useState<SessionRow[]>([]);
  const [metrics, setMetrics] = useState<Record<string, unknown> | null>(null);
  const [review, setReview] = useState<Record<string, unknown> | null>(null);
  const [selected, setSelected] = useState<string[]>([]);
  const [includeText, setIncludeText] = useState(false);
  const [reviewedText, setReviewedText] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [courseId, setCourseId] = useState("");
  const [courseName, setCourseName] = useState("Curso ficticio local");
  const [name, setName] = useState("Defensa de práctica");
  const [subject, setSubject] = useState("Explicación de decisiones");
  const [objective, setObjective] = useState(
    "Preparar una explicación de las decisiones del proyecto",
  );
  const [mode, setMode] = useState("oral_defense");
  const [language, setLanguage] = useState("es");
  const [maxTurns, setMaxTurns] = useState(5);
  const [maxSeconds, setMaxSeconds] = useState(600);
  const [days, setDays] = useState(7);
  const [retentionContent, setRetentionContent] =
    useState("transcript,summary");
  const [retentionAccess, setRetentionAccess] = useState("local_teacher");
  const [modelId, setModelId] = useState("deterministic");
  const [initialQuestions, setInitialQuestions] = useState(
    "Explica la decisión principal de tu proyecto.",
  );
  const [topics, setTopics] = useState("arquitectura");
  const [difficulty, setDifficulty] = useState("media");
  const [knowledge, setKnowledge] = useState(false);
  const [retentionAllowed, setRetentionAllowed] = useState(false);
  const [summaryAllowed, setSummaryAllowed] = useState(true);
  const [voiceInput, setVoiceInput] = useState(false);
  const [voiceOutput, setVoiceOutput] = useState(false);
  const [materials, setMaterials] = useState<MaterialRef[]>([]);
  const [participant, setParticipant] = useState("");
  const [policy, setPolicy] = useState("");
  const [approvedPolicy, setApprovedPolicy] = useState(false);
  async function refresh() {
    const [nextCatalog, nextActivities, nextSessions, nextMetrics] =
      await Promise.all([
        governanceRequest<Catalog>("/governance/catalog"),
        governanceRequest<Activity[]>("/governance/activities"),
        governanceRequest<SessionRow[]>("/governance/sessions"),
        governanceRequest<Record<string, unknown>>("/governance/metrics"),
      ]);
    setCatalog(nextCatalog);
    setActivities(nextActivities);
    setSessions(nextSessions);
    setMetrics(nextMetrics);
  }
  useEffect(() => {
    governanceRequest<{ role: string }>("/auth/me")
      .then(async (value) => {
        if (value.role === "teacher") {
          setAuthenticated(true);
          await refresh();
        }
      })
      .catch(() => {});
  }, []);
  async function action(work: () => Promise<void>) {
    setBusy(true);
    setError(null);
    try {
      await work();
    } catch (reason) {
      setError(
        reason instanceof ApiError
          ? String(reason.detail)
          : "No se pudo completar la operación local.",
      );
    } finally {
      setBusy(false);
    }
  }
  async function login(event: FormEvent) {
    event.preventDefault();
    await action(async () => {
      const credential = secret;
      setSecret("");
      await governanceRequest("/auth/login", { secret: credential });
      setAuthenticated(true);
      await refresh();
    });
  }
  function preparePolicy() {
    if (!catalog || !participant.trim()) {
      setError(
        "Indica el código seudónimo destinatario antes de preparar la política.",
      );
      return;
    }
    const templates = catalog.output_templates.filter(
      (entry) =>
        entry.message_type === "normal" &&
        (mode === "oral_defense"
          ? entry.template_id.startsWith("defense-")
          : !entry.template_id.startsWith("defense-")),
    );
    const disclosures =
      mode === "oral_defense"
        ? [
            {
              category: "generated_defense",
              provenance: "defense-agency",
              recipient: participant,
            },
            {
              category: "defense_summary",
              provenance: "persisted_session_facts",
              recipient: participant,
            },
          ]
        : [
            {
              category: "texto",
              provenance: "activity_material",
              recipient: participant,
            },
          ];
    setPolicy(
      JSON.stringify(
        {
          schema_version: 1,
          policy_id: crypto.randomUUID(),
          policy_version: 1,
          allowed_recipients: [participant],
          allowed_disclosures: disclosures,
          allowed_scopes: {
            topics: [...new Set(templates.map((t) => t.topic_ref))],
            purposes: [...new Set(templates.map((t) => t.purpose_ref))],
            actions: [...new Set(templates.map((t) => t.action_ref))],
          },
          general_knowledge_allowed: knowledge,
          allowed_templates: templates.map((t) => [t.template_id, t.version]),
          allowed_operational_messages: [],
        },
        null,
        2,
      ),
    );
    setApprovedPolicy(false);
  }
  async function save(event: FormEvent) {
    event.preventDefault();
    await action(async () => {
      if (!approvedPolicy) throw new Error("policy not approved");
      const outputPolicy = JSON.parse(policy);
      let course = courseId;
      if (!course)
        course = (
          await governanceRequest<{ id: string }>("/governance/courses", {
            name: courseName,
            subject_code: "LOCAL",
          })
        ).id;
      const retention = await governanceRequest<{ id: string }>(
        "/governance/retention-policies",
        {
          retention_days: days,
          content_scope: retentionContent,
          access_scope: retentionAccess,
        },
      );
      const modeConfig =
        mode === "oral_defense"
          ? {
              initial_questions: initialQuestions.split("\n").filter(Boolean),
              topics: topics
                .split(",")
                .map((t) => t.trim())
                .filter(Boolean),
              difficulty_hint: difficulty,
              summary_authorized: summaryAllowed,
              transcript_retention_authorized: retentionAllowed,
              voice_input_allowed: voiceInput,
              voice_output_allowed: voiceOutput,
            }
          : {
              enabled_modes: [
                "doubt_resolution",
                "guided_explanation",
                "practice_questions",
                "presentation_preparation",
                "concept_review",
              ],
              summary_authorized: summaryAllowed,
              practice_reveals_solution: false,
              retention_authorized: retentionAllowed,
            };
      const activity = {
        course_id: course,
        name,
        subject,
        objective,
        mode,
        language,
        max_turns: maxTurns,
        max_duration_seconds: maxSeconds,
        retention_policy_id: retention.id,
        general_knowledge_allowed: knowledge,
        output_authorization_policy: outputPolicy,
        required_agent_ids: catalog?.compositions[mode] ?? [],
        optional_agent_ids: [],
      };
      const saved = editingId
        ? await governanceRequest<Activity>(
            `/governance/activities/${editingId}/duplicate`,
            {
              changes: {
                ...activity,
                mode_config: modeConfig,
                model_id: modelId,
                material_versions: materials,
              },
            },
          )
        : await governanceRequest<Activity>("/governance/activities", {
            activity,
            mode_config: modeConfig,
            model_id: modelId,
            material_versions: materials,
          });
      setNotice(
        `Borrador creado: ${saved.id} — versión ${saved.version}. Revisa y activa para nuevos usos.`,
      );
      setEditingId(null);
      await refresh();
    });
  }
  function edit(activity: Activity) {
    setEditingId(activity.id);
    setCourseId(activity.course_id);
    setName(activity.name);
    setSubject(activity.subject);
    setObjective(activity.objective);
    setMode(activity.mode);
    setLanguage(activity.language);
    setMaxTurns(activity.max_turns);
    setMaxSeconds(activity.max_duration_seconds);
    setDays(activity.retention_days ?? 7);
    setRetentionContent(
      activity.retention_content_scope === "session"
        ? "transcript,summary"
        : (activity.retention_content_scope ?? "transcript,summary"),
    );
    setRetentionAccess(
      activity.retention_access_scope === "participant_only"
        ? "participant_only"
        : "local_teacher",
    );
    setModelId(
      activity.model_id === "installation-default"
        ? "deterministic"
        : activity.model_id,
    );
    setMaterials(activity.material_versions);
    setPolicy(
      JSON.stringify(activity.output_authorization_policy ?? {}, null, 2),
    );
    setApprovedPolicy(false);
    const config = activity.mode_config ?? {};
    if (Array.isArray(config.initial_questions))
      setInitialQuestions(config.initial_questions.join("\n"));
    if (Array.isArray(config.topics)) setTopics(config.topics.join(", "));
    setRetentionAllowed(
      Boolean(
        config.transcript_retention_authorized ?? config.retention_authorized,
      ),
    );
    setSummaryAllowed(Boolean(config.summary_authorized));
    setNotice(
      "Edición como nueva versión; la configuración anterior no cambiará.",
    );
  }
  async function download(format: "json" | "markdown") {
    await action(async () => {
      const blob = await downloadSessionExport(
        selected,
        format,
        includeText,
        reviewedText,
      );
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `oralia-export.${format === "json" ? "json" : "md"}`;
      link.click();
      setTimeout(() => URL.revokeObjectURL(url), 0);
    });
  }
  if (!authenticated)
    return (
      <main>
        <h1>ORAL-IA — Gobierno docente</h1>
        <p>
          Acceso administrativo local. La credencial se configura fuera del
          repositorio.
        </p>
        {error && <p role="alert">{error}</p>}
        <form onSubmit={login}>
          <label>
            Credencial local
            <input
              type="password"
              autoComplete="current-password"
              required
              value={secret}
              onChange={(e) => setSecret(e.target.value)}
            />
          </label>
          <button disabled={busy}>Entrar al área docente</button>
        </form>
        <a href="/participante">Área de participante</a>
      </main>
    );
  return (
    <main>
      <h1>ORAL-IA — Gobierno docente</h1>
      <TeacherSessionRecovery />
      {import.meta.env.VITE_ORALIA_DEMO_PROFILE && (
        <p role="note">Demo local sin credencial docente. Usar únicamente datos ficticios.</p>
      )}
      <p>
        Configuración y evidencia del sistema; sin notas ni perfiles de
        estudiantes.
      </p>
      <button
        disabled={busy}
        onClick={() =>
          void action(async () => {
            await governanceRequest("/auth/logout", {});
            setAuthenticated(false);
            setReview(null);
            setSessions([]);
          })
        }
      >
        Cerrar acceso docente
      </button>
      {error && <p role="alert">{error}</p>}
      {notice && <p role="status">{notice}</p>}
      <section>
        <h2>
          {editingId ? "Editar como nueva versión" : "Nueva configuración"}
        </h2>
        <form onSubmit={save}>
          <fieldset disabled={busy}>
            <label>
              Asignatura
              <select
                value={courseId}
                onChange={(e) => {
                  setCourseId(e.target.value);
                  setMaterials([]);
                }}
              >
                <option value="">Crear asignatura local</option>
                {catalog?.courses.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </label>
            {!courseId && (
              <label>
                Nombre de asignatura
                <input
                  required
                  value={courseName}
                  onChange={(e) => setCourseName(e.target.value)}
                />
              </label>
            )}
            <label>
              Nombre de actividad
              <input
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </label>
            <label>
              Materia
              <input
                required
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
              />
            </label>
            <label>
              Objetivo
              <textarea
                required
                value={objective}
                onChange={(e) => setObjective(e.target.value)}
              />
            </label>
            <label>
              Modo y composición
              <select
                value={mode}
                onChange={(e) => {
                  setMode(e.target.value);
                  setApprovedPolicy(false);
                }}
              >
                <option value="oral_defense">Defensa oral</option>
                <option value="self_study">Autoestudio</option>
              </select>
            </label>
            <p>
              Agentes de la composición disponible:{" "}
              {catalog?.compositions[mode]?.join(", ")}. Sus contratos y
              controles obligatorios se mantienen.
            </p>
            <label>
              Modelo local
              <select
                value={modelId}
                onChange={(e) => setModelId(e.target.value)}
              >
                {catalog?.models.map((value) => (
                  <option key={value}>{value}</option>
                ))}
              </select>
            </label>
            <label>
              Idioma
              <input
                required
                maxLength={10}
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
              />
            </label>
            <label>
              Límite de turnos
              <input
                type="number"
                min={1}
                required
                value={maxTurns}
                onChange={(e) => setMaxTurns(Number(e.target.value))}
              />
            </label>
            <label>
              Límite de segundos
              <input
                type="number"
                min={1}
                required
                value={maxSeconds}
                onChange={(e) => setMaxSeconds(Number(e.target.value))}
              />
            </label>
            <label>
              Plazo finito de conservación en días
              <input
                type="number"
                min={0}
                required
                value={days}
                onChange={(e) => setDays(Number(e.target.value))}
              />
            </label>
            <label>
              Contenido permitido por la política de conservación
              <select
                value={retentionContent}
                onChange={(event) => setRetentionContent(event.target.value)}
              >
                <option value="transcript,summary">
                  Transcripción y resumen, elegibles por separado
                </option>
                <option value="transcript">Solo transcripción</option>
                <option value="summary">Solo resumen</option>
              </select>
            </label>
            <label>
              Acceso al contenido conservado
              <select
                value={retentionAccess}
                onChange={(event) => setRetentionAccess(event.target.value)}
              >
                <option value="local_teacher">
                  Participante y revisión docente autorizada
                </option>
                <option value="participant_only">Solo participante</option>
              </select>
            </label>
            <label>
              <input
                type="checkbox"
                checked={knowledge}
                onChange={(e) => {
                  setKnowledge(e.target.checked);
                  setApprovedPolicy(false);
                }}
              />
              Permitir conocimiento general etiquetado
            </label>
            <label>
              <input
                type="checkbox"
                checked={retentionAllowed}
                onChange={(e) => setRetentionAllowed(e.target.checked)}
              />
              Permitir elección de conservación
            </label>
            <label>
              <input
                type="checkbox"
                checked={summaryAllowed}
                onChange={(e) => setSummaryAllowed(e.target.checked)}
              />
              Autorizar resumen descriptivo
            </label>
            {mode === "oral_defense" && (
              <>
                <label>
                  Preguntas iniciales, una por línea
                  <textarea
                    value={initialQuestions}
                    onChange={(e) => setInitialQuestions(e.target.value)}
                  />
                </label>
                <label>
                  Temas autorizados separados por comas
                  <input
                    value={topics}
                    onChange={(e) => setTopics(e.target.value)}
                  />
                </label>
                <label>
                  Dificultad orientativa de preguntas
                  <select
                    value={difficulty}
                    onChange={(e) => setDifficulty(e.target.value)}
                  >
                    <option value="baja">Baja</option>
                    <option value="media">Media</option>
                    <option value="alta">Alta</option>
                  </select>
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={voiceInput}
                    onChange={(e) => setVoiceInput(e.target.checked)}
                  />
                  Entrada de voz local configurada
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={voiceOutput}
                    onChange={(e) => setVoiceOutput(e.target.checked)}
                  />
                  Salida de voz local configurada
                </label>
              </>
            )}
            <fieldset>
              <legend>Versiones de material autorizadas</legend>
              {catalog?.materials
                .filter((m) => m.course_id === courseId)
                .map((m) => (
                  <label key={m.document_id}>
                    <input
                      type="checkbox"
                      disabled={m.status !== "active"}
                      checked={materials.some(
                        (ref) => ref.document_id === m.document_id,
                      )}
                      onChange={(e) =>
                        setMaterials(
                          e.target.checked
                            ? [
                                ...materials,
                                {
                                  document_id: m.document_id,
                                  version: m.version,
                                },
                              ]
                            : materials.filter(
                                (ref) => ref.document_id !== m.document_id,
                              ),
                        )
                      }
                    />
                    {m.filename} v{m.version} — {m.status},{" "}
                    {m.fragments_indexed} fragmentos indexados{" "}
                    {m.error_code ? `— ${m.error_code}` : ""}
                  </label>
                ))}
            </fieldset>
            <label>
              Código seudónimo destinatario de la política
              <input
                value={participant}
                onChange={(e) => setParticipant(e.target.value)}
              />
            </label>
            <button type="button" onClick={preparePolicy}>
              Preparar política explícita para revisar
            </button>
            <label>
              Política de salida autorizada
              <textarea
                required
                rows={10}
                value={policy}
                onChange={(e) => {
                  setPolicy(e.target.value);
                  setApprovedPolicy(false);
                }}
              />
            </label>
            <label>
              <input
                type="checkbox"
                checked={approvedPolicy}
                onChange={(e) => setApprovedPolicy(e.target.checked)}
              />
              He revisado los permisos de salida de esta versión
            </label>
            <button disabled={!approvedPolicy || !policy}>
              {editingId ? "Crear versión sucesora" : "Guardar borrador"}
            </button>
            {editingId && (
              <button type="button" onClick={() => setEditingId(null)}>
                Cancelar edición
              </button>
            )}
          </fieldset>
        </form>
      </section>
      <section>
        <h2>Versiones de actividad</h2>
        <details>
          <summary>Materiales disponibles y estado</summary>
          <ul>
            {catalog?.materials.map((material) => (
              <li key={material.document_id}>
                {material.filename}, versión {material.version}:{" "}
                {material.status}; {material.fragments_indexed} fragmentos
                indexados.
              </li>
            ))}
          </ul>
        </details>
        {activities.map((a) => (
          <article
            key={a.id}
            aria-label={`Actividad ${a.name} versión ${a.version}`}
          >
            <h3>
              {a.name} v{a.version}
            </h3>
            <p>
              {a.id} — {a.status} — {a.max_turns} turnos
            </p>
            {a.status === "active" &&
              (a.mode === "self_study" || a.mode === "oral_defense") && (
                <p>
                  <Link
                    to={`${a.mode === "self_study" ? "/autoestudio" : "/defensa"}?activity=${encodeURIComponent(a.id)}`}
                  >
                    {a.mode === "self_study"
                      ? "Abrir actividad de autoestudio"
                      : "Abrir actividad de defensa"}
                  </Link>
                </p>
              )}
            <button disabled={busy} onClick={() => edit(a)}>
              Editar como nueva versión
            </button>
            <button
              disabled={busy}
              onClick={() =>
                void action(async () => {
                  const copy = await governanceRequest<Activity>(
                    `/governance/activities/${a.id}/duplicate`,
                    {
                      new_family: true,
                      changes: { name: `${a.name} (copia)` },
                    },
                  );
                  setNotice(
                    `Actividad duplicada como borrador: ${copy.id}. Revisa y activa.`,
                  );
                  await refresh();
                })
              }
            >
              Duplicar como nueva actividad
            </button>
            <button
              disabled={busy || a.status === "active"}
              onClick={() =>
                void action(async () => {
                  await governanceRequest(
                    `/governance/activities/${a.id}/activate`,
                    {},
                  );
                  await refresh();
                })
              }
            >
              Activar versión
            </button>
            <button
              disabled={busy || a.status === "retired"}
              onClick={() =>
                void action(async () => {
                  await governanceRequest(
                    `/governance/activities/${a.id}/retire`,
                    {},
                  );
                  await refresh();
                })
              }
            >
              Retirar versión
            </button>
          </article>
        ))}
      </section>
      <section>
        <h2>Sesiones consentidas vigentes</h2>
        <button disabled={busy} onClick={() => void action(refresh)}>
          Actualizar revisión
        </button>
        {sessions.length === 0 && <p>No hay sesiones revisables.</p>}
        {sessions.map((s) => (
          <div key={s.session_id}>
            <label>
              <input
                type="checkbox"
                checked={selected.includes(s.session_id)}
                onChange={(e) =>
                  setSelected(
                    e.target.checked
                      ? [...selected, s.session_id]
                      : selected.filter((id) => id !== s.session_id),
                  )
                }
              />
              Sesión {s.session_id} — {s.scope.join(", ")}
            </label>
            <button
              onClick={() =>
                void action(async () => {
                  setReview(
                    await governanceRequest(
                      `/governance/sessions/${s.session_id}`,
                    ),
                  );
                  setConfirmDelete(false);
                })
              }
            >
              Revisar sesión {s.session_id}
            </button>
          </div>
        ))}
        {review && (
          <section aria-label="Revisión consentida">
            <h3>Entradas, originales, correcciones y respuestas</h3>
            <pre>
              {JSON.stringify(
                { turns: review.turns, transcripts: review.transcripts },
                null,
                2,
              )}
            </pre>
            <h3>Resumen, fuentes, agentes y verificaciones</h3>
            <pre>
              {JSON.stringify(
                {
                  summary: review.summary,
                  sources: review.sources,
                  agents: review.agents,
                  verifications: review.verifications,
                  trace: review.trace,
                },
                null,
                2,
              )}
            </pre>
            <label>
              <input
                type="checkbox"
                checked={confirmDelete}
                onChange={(e) => setConfirmDelete(e.target.checked)}
              />
              Confirmo eliminar el contenido de esta sesión
            </label>
            <button
              disabled={!confirmDelete || busy}
              onClick={() =>
                void action(async () => {
                  await governanceRequest(
                    `/sessions/${review.session_id}/content`,
                    { confirm: true },
                    "DELETE",
                  );
                  setReview(null);
                  setSelected([]);
                  setNotice(
                    "Eliminación confirmada: contenido no disponible para revisión ni exportación.",
                  );
                  await refresh();
                })
              }
            >
              Eliminar sesión revisada
            </button>
          </section>
        )}
        <p>
          Los alias no garantizan anonimización del texto libre. Revisa su
          posible información personal antes de incluirlo.
        </p>
        <label>
          <input
            type="checkbox"
            checked={includeText}
            onChange={(e) => setIncludeText(e.target.checked)}
          />
          Incluir texto libre autorizado
        </label>
        <label>
          <input
            type="checkbox"
            checked={reviewedText}
            onChange={(e) => setReviewedText(e.target.checked)}
          />
          He revisado el texto libre de todas las sesiones seleccionadas
        </label>
        <button
          disabled={
            busy || selected.length === 0 || (includeText && !reviewedText)
          }
          onClick={() => void download("json")}
        >
          Exportar JSON
        </button>
        <button
          disabled={
            busy || selected.length === 0 || (includeText && !reviewedText)
          }
          onClick={() => void download("markdown")}
        >
          Exportar Markdown
        </button>
        <button
          disabled={busy}
          onClick={() =>
            void action(async () => {
              const result = await governanceRequest("/governance/purge", {});
              setNotice(`Purga completada: ${JSON.stringify(result)}`);
              await refresh();
            })
          }
        >
          Purgar expirados
        </button>
      </section>
      <section>
        <h2>Estado técnico del índice</h2>
        <pre>{JSON.stringify(catalog?.index_status, null, 2)}</pre>
        <p>
          Estos metadatos muestran la versión local; no acreditan integridad ni
          calidad de recuperación.
        </p>
        <button
          disabled={busy}
          onClick={() =>
            void action(async () => {
              const result = await governanceRequest(
                "/materials/index/rebuild",
                {},
              );
              setNotice(`Reconstrucción completada: ${JSON.stringify(result)}`);
              await refresh();
            })
          }
        >
          Reconstruir índice autorizado
        </button>
      </section>
      <section>
        <h2>Métricas agregadas del sistema</h2>
        <pre>{JSON.stringify(metrics, null, 2)}</pre>
      </section>
      <a href="/defensa">Participar en defensa</a>
      <a href="/autoestudio">Participar en autoestudio</a>
    </main>
  );
}
