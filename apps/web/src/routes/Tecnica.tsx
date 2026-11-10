import { useEffect, useRef, useState, FormEvent, ChangeEvent } from "react";
import DiagnosticStudy from "../components/DiagnosticStudy";
import type { RuntimeStatus } from "../components/studyRuntime";
import {
  ApiError,
  createActivity,
  listCatalogAgents,
  listCatalogAgencies,
  listSessions,
  getSessionDetail,
  getSessionTrace,
  uploadMaterial,
  listMaterials,
  activateMaterial,
  deactivateMaterial,
  resolveDuplicate,
  listMaterialConflicts,
  reviewMaterialConflict,
  AgentDescriptor,
  AgencySummary,
  SessionSummary,
  MaterialDocumentSummary,
  DuplicateConflict,
  MaterialConflictRecordSummary,
} from "../api/client";

// Área técnica/docente — FR-021 (mínima), FR-021a (sin credencial en esta feature: el
// backend expone un punto de extensión no-op; ver contracts/api-tecnica.md).

const emptyActivityForm = {
  course_id: "",
  name: "",
  subject: "",
  objective: "",
  mode: "texto",
  language: "es",
  max_turns: 10,
  max_duration_seconds: 900,
  retention_policy_id: "",
};

export default function Tecnica() {
  const [tab, setTab] = useState<"catalogo" | "actividad" | "sesiones" | "materiales">("catalogo");

  if (new URLSearchParams(window.location.search).get("documental") === "1") {
    return <main><h1>ORALIA — Materiales de requisitos</h1><DocumentaryMaterials /></main>;
  }

  return (
    <main>
      <h1>ORAL-IA — Área técnica</h1>
      <nav aria-label="Secciones del área técnica">
        <button aria-current={tab === "catalogo"} onClick={() => setTab("catalogo")}>
          Catálogo
        </button>{" "}
        <button aria-current={tab === "actividad"} onClick={() => setTab("actividad")}>
          Nueva actividad
        </button>{" "}
        <button aria-current={tab === "sesiones"} onClick={() => setTab("sesiones")}>
          Sesiones
        </button>{" "}
        <button aria-current={tab === "materiales"} onClick={() => setTab("materiales")}>
          Materiales
        </button>
      </nav>
      {tab === "catalogo" && <Catalogo />}
      {tab === "actividad" && <NuevaActividad />}
      {tab === "sesiones" && <Sesiones />}
      {tab === "materiales" && <Materiales />}
    </main>
  );
}

type DocumentaryPage = {
  id: string; page: number; section: string; text: string; status: string;
  reason: string; derivation: string; preview?: string; printed_page?: number;
};
type DocumentaryManifest = {
  package_id: string; scope: string; retrieval?: boolean;
  study_lab?: boolean; study_provider?: string; study_workflow_deadline_seconds?: number;
  study_runtime?: RuntimeStatus;
  documents: { id: string; filename: string; edition: string; author: string;
    domain: string; sha256: string; conditions: string; origin: string;
    available: number; quarantine: number }[];
  concepts: { label: string; passages: string[]; limits: string }[];
  limitations: string[]; discrepancies: string[];
};

function DocumentaryMaterials() {
  const [catalog, setCatalog] = useState<DocumentaryManifest | null>(null);
  const [pages, setPages] = useState<DocumentaryPage[]>([]);
  const [docId, setDocId] = useState("");
  const [query, setQuery] = useState("");
  const [passage, setPassage] = useState("");
  const [quarantine, setQuarantine] = useState(false);
  const [error, setError] = useState("");
  const [closed, setClosed] = useState(false);
  const [busy, setBusy] = useState(false);
  const pending = useRef(0);

  async function getJson(path: string, init?: RequestInit) {
    const response = await fetch(path, init);
    if (!response.ok) throw new Error(`No se pudo consultar (HTTP ${response.status}). Vuelva a entrar.`);
    return response.json();
  }
  async function enter() {
    setBusy(true); setError("");
    try {
      await getJson("/documentary/enter", { method: "POST" });
      setCatalog(await getJson("/api/v1/documentary")); setClosed(false);
    } catch (e) { setError(String(e)); }
    finally { setBusy(false); }
  }
  async function selectDocument(id: string, selectedPassage = "") {
    const request = ++pending.current;
    setError(""); setPages([]); setDocId(id); setQuery(""); setPassage(selectedPassage);
    try {
      const rows = await getJson(`/api/v1/documentary/${encodeURIComponent(id)}/pages`);
      if (request === pending.current) setPages(rows);
    } catch (e) { if (request === pending.current) setError(String(e)); }
  }
  async function leave() {
    setBusy(true); setError(""); ++pending.current;
    try {
      await getJson("/documentary/leave", { method: "POST" });
      setCatalog(null); setPages([]); setDocId(""); setQuery(""); setPassage(""); setClosed(true);
    } catch (e) { setError(String(e)); }
    finally { setBusy(false); }
  }
  const doc = catalog?.documents.find(d => d.id === docId);
  const visible = pages.filter(p => (!passage || p.id === passage) && (quarantine || p.status === "disponible") &&
    `${p.section} ${p.text}`.toLocaleLowerCase().includes(query.toLocaleLowerCase()));
  return <section aria-labelledby="materiales-documentales">
    <h2 id="materiales-documentales">Consulta documental local de solo lectura</h2>
    <p>Perfil de prueba separado. Sin tutor generativo ni sesión de participante. No se conservan búsquedas. Revisión técnica parcial; aceptación docente pendiente.</p>
    {error && <p role="alert">{error}</p>}
    {!catalog ? <>
      {closed && <p role="status">Consulta cerrada. Puede volver a entrar; el paquete permanece intacto.</p>}
      <button disabled={busy} onClick={() => void enter()}>Entrar en consulta documental</button>
    </> : <>
      <p>Paquete: <strong>{catalog.package_id}</strong>. {catalog.scope}</p>
      <button disabled={busy} onClick={() => void leave()}>Cerrar consulta</button>
      {catalog.retrieval && <RetrievedPassages />}
      {catalog.study_lab && !busy && <DiagnosticStudy provider={catalog.study_provider ?? "disconnected"} deadlineSeconds={catalog.study_workflow_deadline_seconds ?? 50} initialRuntime={catalog.study_runtime} />}
      <details className="sources-panel"><summary>Cobertura por concepto</summary><ul>
        {catalog.concepts.map(c => <li key={c.label}><strong>{c.label}</strong>: {c.passages.map(ref => {
          const [id, number] = ref.split(":");
          const title = catalog.documents.find(d => d.id === id)?.filename ?? id;
          return <button key={ref} onClick={() => void selectDocument(id, ref)}>{title}, {id === "sommerville" ? "diapositiva" : id === "nasa-swe055" ? "sección" : "página"} {number.replace("-core", "")}</button>;
        })}. {c.limits}</li>)}
      </ul></details>
      <details className="sources-panel"><summary>Limitaciones y discrepancias entre fuentes</summary><ul>
        {[...catalog.limitations, ...catalog.discrepancies].map(x => <li key={x}>{x}</li>)}
      </ul></details>
      <h3>Documentos y versiones</h3>
      <ul>{catalog.documents.map(d => <li key={d.id}>
        <button onClick={() => void selectDocument(d.id)}>{d.filename}</button>
        {" — "}{d.available} páginas/secciones disponibles; {d.quarantine} en cuarentena. {d.edition}
      </li>)}</ul>
      {doc && <>
        <h3>{doc.filename}</h3><p>{doc.author}. Ámbito: {doc.domain}. {doc.edition}</p>
        <p>Origen: {doc.origin}</p><p>Condiciones: {doc.conditions}</p>
        <details><summary>Identidad del original</summary><p style={{ overflowWrap: "anywhere" }}>SHA-256: {doc.sha256}</p></details>
        <p><a href={`/api/v1/documentary/${doc.id}/original`} target="_blank" rel="noreferrer">Abrir original local</a> (PDF en navegador; PPTX/HTML como descarga local).</p>
        <label htmlFor="documentary-search">Buscar texto literal en este documento</label>{" "}
        <input id="documentary-search" value={query} onChange={e => { setQuery(e.target.value); setPassage(""); }} maxLength={200} />
        {passage && <button onClick={() => setPassage("")}>Ver todas las páginas de este documento</button>}
        <p><label><input type="checkbox" checked={quarantine} onChange={e => setQuarantine(e.target.checked)} /> Mostrar también cuarentena</label></p>
        <p role="status">{visible.length} páginas/secciones coincidentes. Búsqueda literal, sin ranking de relevancia.</p>
        {visible.map(p => <details className="sources-panel" key={p.id}>
          <summary>{p.id} — {doc.id === "nasa-swe055" ? "sección" : doc.id === "sommerville" ? "diapositiva" : "página PDF"} {p.page}{p.printed_page ? ` (impresa ${p.printed_page})` : ""}: {p.section} — {p.status}</summary>
          <p>{p.reason}</p><p>{p.derivation}</p>
          {doc.id !== "nasa-swe055" && doc.id !== "sommerville" && <p><a target="_blank" rel="noreferrer" href={`/api/v1/documentary/${doc.id}/original#page=${p.page}`}>Abrir original en página {p.page}</a></p>}
          <pre style={{ whiteSpace: "pre-wrap", fontFamily: "inherit" }}>{p.text}</pre>
          {p.preview && <details><summary>Ver página original renderizada</summary><img loading="lazy" style={{ maxWidth: "100%" }} alt={`Original ${doc.filename}, página ${p.page}`} src={`/api/v1/documentary/${doc.id}/preview/${p.page}`} /></details>}
        </details>)}
      </>}
    </>}
  </section>;
}

type RetrievedPassage = {
  id: string; filename: string; page: number; printed_page?: number; section: string;
  text: string; author: string; edition: string; derivation: string; original_url: string;
};
function RetrievedPassages() {
  const [question, setQuestion] = useState("");
  const [reference, setReference] = useState("");
  const [focusChange, setFocusChange] = useState(false);
  const [rows, setRows] = useState<RetrievedPassage[]>([]);
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const alive = useRef(true);
  useEffect(() => { alive.current = true; return () => { alive.current = false; }; }, []);
  async function search(e: FormEvent) {
    e.preventDefault(); setBusy(true); setRows([]); setMessage("");
    try {
      const params = new URLSearchParams({ question, reference, focus_change: String(focusChange) });
      const response = await fetch(`/api/v1/retrieval?${params}`);
      if (!response.ok) throw new Error(`Recuperación no disponible (HTTP ${response.status}).`);
      const data = await response.json();
      if (alive.current) { setRows(data.passages); setMessage(data.passages.length ? data.notice :
        "No se recuperaron pasajes con este presupuesto. Esto no significa que el tema esté fuera del curso."); }
    } catch (e) { if (alive.current) setMessage(String(e)); }
    finally { if (alive.current) setBusy(false); }
  }
  return <section aria-labelledby="retrieved-heading">
    <h3 id="retrieved-heading">Pasajes recuperados</h3>
    <p>Escriba una pregunta natural. Solo se buscan pasajes; no se genera una respuesta ni se evalúa al alumno. Su pertinencia y suficiencia requieren revisión.</p>
    <form onSubmit={e => void search(e)}>
      <label htmlFor="retrieval-question">Pregunta sobre los materiales</label>{" "}
      <input id="retrieval-question" value={question} maxLength={2000} onChange={e => setQuestion(e.target.value)} required />
      <p><label htmlFor="retrieval-reference">Referente mostrado (opcional para un seguimiento)</label>{" "}
      <input id="retrieval-reference" value={reference} maxLength={500} onChange={e => setReference(e.target.value)} /></p>
      <p><label><input type="checkbox" checked={focusChange} onChange={e => setFocusChange(e.target.checked)} /> Cambio de tema: descartar referente</label></p>
      <button disabled={busy} type="submit">{busy ? "Buscando…" : "Recuperar pasajes"}</button>
    </form>
    <p role="status">{message}</p>
    {rows.map(p => <article key={p.id}>
      <h4>{p.filename} — página/sección {p.page}{p.printed_page ? ` (impresa ${p.printed_page})` : ""}: {p.section}</h4>
      <p>{p.author}. {p.edition}</p><p>{p.derivation}</p>
      <a href={p.original_url} target="_blank" rel="noreferrer">Consultar original de {p.filename}, página {p.page}</a>
      <pre style={{ whiteSpace: "pre-wrap", fontFamily: "inherit" }}>{p.text}</pre>
    </article>)}
  </section>;
}

function Catalogo() {
  const [agents, setAgents] = useState<AgentDescriptor[]>([]);
  const [agencies, setAgencies] = useState<AgencySummary[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([listCatalogAgents(), listCatalogAgencies()])
      .then(([a, g]) => {
        setAgents(a);
        setAgencies(g);
      })
      .catch((e) => setError(e instanceof ApiError ? e.detail : "No se pudo cargar el catálogo"));
  }, []);

  return (
    <section aria-labelledby="catalogo-heading">
      <h2 id="catalogo-heading">Catálogo de agentes y agencias (FR-003)</h2>
      {error && (
        <p className="error-message" role="alert">
          {error}
        </p>
      )}
      <h3>Agentes ({agents.length})</h3>
      <ul>
        {agents.map((a) => (
          <li key={a.id}>
            {a.name} v{a.version} — {a.availability_status} — {a.capabilities.join(", ")}
          </li>
        ))}
      </ul>
      <h3>Agencias ({agencies.length})</h3>
      <ul>
        {agencies.map((a) => (
          <li key={a.id}>
            {a.name} v{a.version} — {a.availability_status}
          </li>
        ))}
      </ul>
    </section>
  );
}

function NuevaActividad() {
  const [form, setForm] = useState(emptyActivityForm);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setResult(null);
    try {
      const created = await createActivity({
        ...form,
        max_turns: Number(form.max_turns),
        max_duration_seconds: Number(form.max_duration_seconds),
      });
      setResult(`Actividad creada: ${created.name} (versión ${created.version}).`);
      setForm(emptyActivityForm);
    } catch (e) {
      setError(
        e instanceof ApiError
          ? `No se pudo crear la actividad: ${e.detail}`
          : "No se pudo crear la actividad. Inténtelo de nuevo.",
      );
    }
  }

  return (
    <section aria-labelledby="actividad-heading">
      <h2 id="actividad-heading">Nueva configuración de actividad (FR-001)</h2>
      {error && (
        <p className="error-message" role="alert">
          {error}
        </p>
      )}
      {result && <p role="status">{result}</p>}
      <form onSubmit={onSubmit}>
        <div className="field">
          <label htmlFor="course_id">Identificador de asignatura (course_id)</label>
          <input
            id="course_id"
            required
            value={form.course_id}
            onChange={(e) => setForm({ ...form, course_id: e.target.value })}
          />
        </div>
        <div className="field">
          <label htmlFor="name">Nombre</label>
          <input
            id="name"
            required
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
        </div>
        <div className="field">
          <label htmlFor="objective">Objetivo</label>
          <input
            id="objective"
            required
            value={form.objective}
            onChange={(e) => setForm({ ...form, objective: e.target.value })}
          />
        </div>
        <div className="field">
          <label htmlFor="max_turns">Límite de turnos</label>
          <input
            id="max_turns"
            type="number"
            min={1}
            required
            value={form.max_turns}
            onChange={(e) => setForm({ ...form, max_turns: Number(e.target.value) })}
          />
        </div>
        <div className="field">
          <label htmlFor="max_duration_seconds">Duración máxima (segundos)</label>
          <input
            id="max_duration_seconds"
            type="number"
            min={1}
            required
            value={form.max_duration_seconds}
            onChange={(e) => setForm({ ...form, max_duration_seconds: Number(e.target.value) })}
          />
        </div>
        <div className="field">
          <label htmlFor="retention_policy_id">Identificador de política de conservación</label>
          <input
            id="retention_policy_id"
            required
            value={form.retention_policy_id}
            onChange={(e) => setForm({ ...form, retention_policy_id: e.target.value })}
          />
        </div>
        <button type="submit">Crear actividad</button>
      </form>
    </section>
  );
}

function Sesiones() {
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [selected, setSelected] = useState<unknown | null>(null);
  const [trace, setTrace] = useState<unknown | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listSessions()
      .then(setSessions)
      .catch(() => setError("No se pudieron cargar las sesiones."));
  }, []);

  async function openSession(id: string) {
    setError(null);
    try {
      const [detail, sessionTrace] = await Promise.all([getSessionDetail(id), getSessionTrace(id)]);
      setSelected(detail);
      setTrace(sessionTrace);
    } catch {
      setError("No se pudo cargar el detalle de la sesión.");
    }
  }

  return (
    <section aria-labelledby="sesiones-heading">
      <h2 id="sesiones-heading">Sesiones activas e históricas (US6, FR-020)</h2>
      {error && (
        <p className="error-message" role="alert">
          {error}
        </p>
      )}
      <ul>
        {sessions.map((s) => (
          <li key={s.id}>
            <button onClick={() => openSession(s.id)}>
              {s.id.slice(0, 8)} — {s.status} — {s.turn_count} turnos
            </button>
          </li>
        ))}
      </ul>
      {selected != null && (
        <>
          <h3>Detalle de sesión</h3>
          <pre>{JSON.stringify(selected, null, 2)}</pre>
          <h3>Trazabilidad completa (FR-016)</h3>
          <pre>{JSON.stringify(trace, null, 2)}</pre>
        </>
      )}
    </section>
  );
}

function Materiales() {
  const [courseId, setCourseId] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [documents, setDocuments] = useState<MaterialDocumentSummary[]>([]);
  const [conflicts, setConflicts] = useState<MaterialConflictRecordSummary[]>([]);
  const [pendingConflict, setPendingConflict] = useState<DuplicateConflict | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const uploadInFlight = useRef(false);

  function refresh(course: string) {
    if (!course) return;
    listMaterials(course)
      .then(setDocuments)
      .catch(() => setError("No se pudieron cargar los materiales de la asignatura."));
  }

  function refreshConflicts() {
    listMaterialConflicts()
      .then(setConflicts)
      .catch(() => setError("No se pudieron cargar los conflictos pendientes."));
  }

  useEffect(() => {
    refresh(courseId);
  }, [courseId]);

  useEffect(() => {
    refreshConflicts();
  }, []);

  async function onReviewConflict(conflictId: string) {
    setError(null);
    try {
      await reviewMaterialConflict(conflictId);
      refreshConflicts();
    } catch (err) {
      setError(
        err instanceof ApiError
          ? `No se pudo marcar el conflicto como revisado: ${err.detail}`
          : "No se pudo marcar el conflicto como revisado.",
      );
    }
  }

  function onFileChange(e: ChangeEvent<HTMLInputElement>) {
    setFile(e.target.files?.[0] ?? null);
  }

  async function onUpload(e: FormEvent) {
    e.preventDefault();
    if (uploadInFlight.current || !file || !courseId) return;
    uploadInFlight.current = true;
    setUploading(true);
    setError(null);
    setStatus("Carga en curso. Esperando confirmación del procesamiento y del índice local; la preparación inicial puede tardar.");
    setPendingConflict(null);
    try {
      const result = await uploadMaterial(courseId, file);
      if ("duplicate" in result) {
        setPendingConflict(result.duplicate);
        setStatus(null);
      } else {
        setStatus(`"${result.filename}" cargado — estado: ${result.status}.`);
        refresh(courseId);
      }
      setFile(null);
    } catch (err) {
      setStatus(null);
      setError(err instanceof ApiError ? `No se pudo cargar el documento: ${err.detail}` : "No se pudo confirmar la carga. Compruebe la lista de documentos antes de volver a enviar.");
    } finally {
      uploadInFlight.current = false;
      setUploading(false);
    }
  }

  async function onResolveDuplicate(resolution: "link_existing" | "proceed_new") {
    if (!pendingConflict) return;
    setError(null);
    try {
      const result = await resolveDuplicate(pendingConflict.conflictToken, resolution);
      setStatus(`Resolución aplicada — estado: ${result.status}.`);
      setPendingConflict(null);
      refresh(courseId);
    } catch (err) {
      setError(err instanceof ApiError ? `No se pudo resolver el duplicado: ${err.detail}` : "No se pudo resolver el duplicado.");
    }
  }

  async function onToggleActive(doc: MaterialDocumentSummary) {
    setError(null);
    try {
      if (doc.status === "active") {
        await deactivateMaterial(doc.id);
      } else {
        await activateMaterial(doc.id);
      }
      refresh(courseId);
    } catch (err) {
      setError(
        err instanceof ApiError
          ? `No se pudo cambiar el estado del material: ${err.detail}`
          : "No se pudo cambiar el estado del material.",
      );
    }
  }

  return (
    <section aria-labelledby="materiales-heading">
      <h2 id="materiales-heading">Materiales autorizados (FR-001, FR-011, FR-013)</h2>
      {error && (
        <p className="error-message" role="alert">
          ⚠ {error}
        </p>
      )}
      {status && <p role="status">{status}</p>}

      <div className="field">
        <label htmlFor="materiales-course-id">Identificador de asignatura (course_id)</label>
        <input id="materiales-course-id" disabled={uploading} value={courseId} onChange={(e) => setCourseId(e.target.value)} />
      </div>

      <form onSubmit={onUpload} aria-label="Carga de documento" aria-busy={uploading}>
        <div className="field">
          <label htmlFor="materiales-file">Documento (PDF, DOCX, PPTX, TXT o Markdown)</label>
          <input
            id="materiales-file"
            disabled={uploading}
            type="file"
            accept=".pdf,.docx,.pptx,.txt,.md"
            onChange={onFileChange}
          />
        </div>
        <button type="submit" disabled={uploading || !file || !courseId}>
          Cargar documento
        </button>
      </form>

      {pendingConflict && (
        <div role="alert" className="error-message">
          <p>
            ⚠ Posible duplicado del documento {pendingConflict.existingDocumentId.slice(0, 8)}. Elija cómo
            proceder:
          </p>
          <button onClick={() => onResolveDuplicate("link_existing")}>
            Es el mismo documento (enlazar)
          </button>{" "}
          <button onClick={() => onResolveDuplicate("proceed_new")}>
            Es un documento distinto (continuar)
          </button>
        </div>
      )}

      <h3>Documentos de la asignatura ({documents.length})</h3>
      <ul>
        {documents.map((doc) => (
          <li key={doc.id}>
            {doc.filename} — v{doc.version} — estado: <strong>{doc.status}</strong>
            {doc.error_detail && <span> — {doc.error_detail}</span>}
            {(doc.status === "active" || doc.status === "inactive" || doc.status === "processed") && (
              <>
                {" "}
                <button onClick={() => onToggleActive(doc)}>
                  {doc.status === "active" ? "Desactivar" : "Activar"}
                </button>
              </>
            )}
          </li>
        ))}
      </ul>

      <h3>Conflictos pendientes de revisión (FR-022a)</h3>
      {conflicts.length === 0 && <p>No hay conflictos pendientes.</p>}
      <ul>
        {conflicts.map((c) => (
          <li key={c.id}>
            <p>Detectado con la consulta: «{c.detected_by_query}»</p>
            <ul>
              {c.conflicting_claims.map((claim, i) => (
                <li key={i}>{claim}</li>
              ))}
            </ul>
            <button onClick={() => onReviewConflict(c.id)}>Marcar como revisado</button>
          </li>
        ))}
      </ul>
    </section>
  );
}
