import { FormEvent, RefObject, useCallback, useEffect, useRef, useState } from "react";
import { acceptResponse, canSend, failureMessage, generationMessage, remainingRuntime, runtimeExpired, RuntimeClock, RuntimeStatus, StudyApiError, StudyQuota } from "./studyRuntime";
import WebInspection, { WebEvidenceView, WebReceipt, WebState } from "./WebInspection";

type Passage = { id?: string; filename: string; page: number; section?: string; text?: string; original_url: string };
type Receipt = {
  id: string; question: string; status: string; diagnostic_preview: string | null;
  raw_candidate?: string | null; provider_kind: string; retrieval?: { passages: Passage[]; omitted_context?: unknown[] };
  review_repair?: unknown;
  web_sources?: {title: string; url: string; entity: string; captured_at: string}[];
  review_notice?: {items: {kind: string; message: string}[]; guidance: string} | null;
};

export function groupStudySources(passages: Passage[]) {
  const groups = new Map<string, Passage[]>();
  for (const passage of passages) {
    const key = passage.original_url.split("#")[0];
    const group = groups.get(key) ?? [];
    if (!group.some(item => item.original_url === passage.original_url)) group.push(passage);
    groups.set(key, group);
  }
  return [...groups];
}

function studentFailure(error: unknown): string {
  if (error instanceof StudyApiError) {
    if (error.code === "network") return "No se ha podido confirmar la respuesta. Comprueba la conexión antes de volver a intentarlo.";
    if (["runtime_expired", "lease_expired", "permission_expired", "inspection_closed"].includes(error.code)) return "La sesión ha finalizado. Puedes comenzar otra conversación si el servicio sigue disponible.";
    if (error.code === "source_changed") return "El material de estudio ha cambiado. Finaliza y vuelve a comenzar.";
  }
  return "No he podido completar la respuesta. Puedes intentarlo de nuevo o finalizar la conversación.";
}

export async function api(path: string, body?: object, signal?: AbortSignal) {
  let response: Response;
  try { response = await fetch(`/api/v1/study-lab/${path}`, {
    method: body ? "POST" : "GET", headers: body ? { "Content-Type": "application/json" } : {},
    body: body ? JSON.stringify(body) : undefined, signal,
  }); } catch (error) {
    if (signal?.aborted) throw error;
    throw new StudyApiError("Servidor local no accesible.", "network");
  }
  if (!response.ok) {
    const data = await response.json().catch(() => null);
    const detail = data?.detail;
    throw new StudyApiError(typeof detail === "string" ? detail : detail?.message ?? `Servidor: HTTP ${response.status}.`, detail?.code ?? "http", response.status);
  }
  try { return await response.json(); }
  catch (error) {
    if (signal?.aborted) throw error;
    throw new StudyApiError(error instanceof SyntaxError ? "El servidor devolvió un recibo ilegible; no se confirma una respuesta completa." : "Se perdió la conexión al recibir el resultado.", error instanceof SyntaxError ? "protocol" : "network");
  }
}

export function RuntimeNotice({ clock, now, deadlineSeconds }: { clock: RuntimeClock; now: number; deadlineSeconds: number }) {
  const remaining = remainingRuntime(clock, now);
  if (!clock || remaining === null) return null;
  const seconds = Math.ceil(remaining);
  return <p role="status">Runtime global: {Math.floor(seconds / 60)}:{String(seconds % 60).padStart(2, "0")} restantes; caduca a las {new Date(clock.status.expires_at_unix_ms).toLocaleTimeString("es-ES")}. {runtimeExpired(clock, now) ? "Plazo agotado; envío deshabilitado." : remaining < deadlineSeconds ? "Queda menos que el máximo de una respuesta; una petición puede interrumpirse al caducar." : ""} El plazo no se renueva con actividad, recarga ni reentrada.</p>;
}

function ResponseWait({ since }: { since: number }) {
  const [seconds, setSeconds] = useState(() => Math.max(0, Math.floor((performance.now() - since) / 1000)));
  useEffect(() => {
    const timer = window.setInterval(() => setSeconds(Math.max(0, Math.floor((performance.now() - since) / 1000))), 1000);
    return () => window.clearInterval(timer);
  }, [since]);
  return <span className="study-wait"><span role="status">Preparando la respuesta…</span> <span role="timer" aria-live="off" aria-label="Tiempo de espera">{seconds} s</span></span>;
}

export function QuestionForm({ question, busy, focusChange, enabled, deadlineSeconds, onSubmit, onQuestion, onFocus, onCancel, studentView = false, inputRef, waitingSince = null }: {
  question: string; busy: boolean; focusChange: boolean; enabled: boolean; deadlineSeconds: number;
  onSubmit: (event: FormEvent) => void; onQuestion: (value: string) => void;
  onFocus: (value: boolean) => void; onCancel: () => void;
  studentView?: boolean;
  inputRef?: RefObject<HTMLTextAreaElement>;
  waitingSince?: number | null;
}) {
  return <form onSubmit={onSubmit} aria-label={studentView ? "Enviar pregunta" : "Pregunta diagnóstica"} aria-busy={studentView ? undefined : busy}>
    <label htmlFor="diagnostic-question">{studentView ? "Tu pregunta" : "Pregunta de laboratorio"}</label>
    <textarea ref={inputRef} id="diagnostic-question" aria-describedby={studentView ? "study-question-help" : undefined} value={question} disabled={busy} maxLength={2000} required onChange={e => onQuestion(e.target.value)} />
    {studentView && <p id="study-question-help">Escribe tu pregunta y pulsa Enviar. Intro permite escribir otra línea.</p>}
    {!studentView && <label><input type="checkbox" disabled={busy} checked={focusChange} onChange={e => onFocus(e.target.checked)} /> Cambiar de tema y descartar referente anterior</label>}
    <button type="submit" disabled={!enabled}>{studentView ? "Enviar" : "Enviar al diagnóstico"}</button>
    {busy && <>{studentView && waitingSince !== null ? <ResponseWait since={waitingSince} /> : <span role="status">{studentView ? "Conectando…" : `Esperando diagnóstico; máximo ${deadlineSeconds} segundos por pregunta, sujeto al plazo global.`}</span>}<button type="button" onClick={onCancel}>{studentView ? "Cancelar" : "Cancelar petición"}</button></>}
  </form>;
}

export default function DiagnosticStudy({ provider, deadlineSeconds = 50, initialRuntime = null, studentView = false, onAuthorize }: { provider: string; deadlineSeconds?: number; initialRuntime?: RuntimeStatus | null; studentView?: boolean; onAuthorize?: () => Promise<void> }) {
  const [open, setOpen] = useState(false);
  const ownsSession = useRef(false);
  const [webState, setWebState] = useState<WebState | null>(null);
  const [webReceipt, setWebReceipt] = useState<WebReceipt | null>(null);
  const [webNotice, setWebNotice] = useState<{id: string; text: string} | null>(null);
  const webNoticeElement = useRef<HTMLParagraphElement>(null);
  const [question, setQuestion] = useState("");
  const [focusChange, setFocusChange] = useState(false);
  const [busy, setBusy] = useState(false);
  const [waitingSince, setWaitingSince] = useState<number | null>(null);
  // Answer text as it is written (before its review); shown only to the student who asked it.
  const [partial, setPartial] = useState<{ phase: string; text: string } | null>(null);
  const [confirmClose, setConfirmClose] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [exportError, setExportError] = useState("");
  const [atLatest, setAtLatest] = useState(true);
  const [modelReady, setModelReady] = useState(true);
  const [modelPreparing, setModelPreparing] = useState(false);
  const [connected, setConnected] = useState(true);
  const [quota, setQuota] = useState<StudyQuota | null>(null);
  const quotaRef = useRef<StudyQuota | null>(null);
  const [runtimeEnded, setRuntimeEnded] = useState(false);
  const [clock, setClock] = useState<RuntimeClock>(() => initialRuntime ? { status: initialRuntime, sampledAt: performance.now() } : null);
  const [now, setNow] = useState(() => performance.now());
  const runtime = useRef(clock);
  const expiredHandled = useRef(false);
  const [error, setError] = useState("");
  const [rows, setRows] = useState<Receipt[]>([]);
  const [pending, setPending] = useState<Receipt | null>(null);
  const [technical, setTechnical] = useState<Receipt | null>(null);
  const epoch = useRef(0);
  const locked = useRef(false);
  const abort = useRef<AbortController | null>(null);
  const candidate = useRef<HTMLPreElement>(null);
  const questionInput = useRef<HTMLTextAreaElement>(null);
  const messageLog = useRef<HTMLDivElement>(null);
  const closeDialog = useRef<HTMLDialogElement>(null);
  const continueButton = useRef<HTMLButtonElement>(null);
  const followLatest = useRef(true);
  const lastContact = useRef(performance.now());
  const attempt = useRef<{id: string; question: string} | null>(null);

  useEffect(() => {
    if (confirmClose && open) { setExportError(""); closeDialog.current?.showModal(); continueButton.current?.focus(); }
    else closeDialog.current?.close();
  }, [confirmClose, open]);

  useEffect(() => {
    if (followLatest.current && messageLog.current) messageLog.current.scrollTop = messageLog.current.scrollHeight;
  }, [rows, pending, partial?.text]);

  useEffect(() => {
    if (!studentView || !open || !busy || waitingSince === null || pending) { setPartial(null); return; }
    let disposed = false;
    const poll = () => {
      api("partial").then(result => { if (!disposed && result.text) setPartial({ phase: result.phase, text: result.text }); }).catch(() => undefined);
    };
    const timer = window.setInterval(poll, 400);
    return () => { disposed = true; window.clearInterval(timer); };
  }, [studentView, open, busy, waitingSince, pending]);

  useEffect(() => {
    if (!studentView || !open || busy || !connected || !modelReady) return;
    const input = questionInput.current;
    // Restore keyboard flow, without stealing focus from sources or other controls.
    if (input && (document.activeElement === document.body || input.form?.contains(document.activeElement))) input.focus();
  }, [studentView, open, busy, connected, modelReady]);

  const updateState = useCallback((state: { web?: WebState; runtime?: RuntimeStatus | null; provider_ready?: boolean; provider_preparing?: boolean; quota?: StudyQuota; web_notice?: {id: string; text: string} | null }, sampledAt = performance.now()) => {
    lastContact.current = sampledAt;
    if ("web_notice" in state) setWebNotice(state.web_notice ?? null);
    if (state.web) { setWebState(state.web); if (!state.web.enabled) setWebReceipt(null); }
    setModelReady(state.provider_ready !== false); setModelPreparing(state.provider_preparing === true);
    if (state.quota) { quotaRef.current = state.quota; setQuota(state.quota); }
    if (state.runtime) {
      runtime.current = { status: state.runtime, sampledAt }; setClock(runtime.current);
    }
  }, []);

  useEffect(() => {
    if (!webNotice || !open || !studentView) return;
    const version = epoch.current;
    const frame = requestAnimationFrame(() => {
      if (document.visibilityState === "visible" && version === epoch.current && webNoticeElement.current?.textContent === webNotice.text) {
        void api(`web-notice/${webNotice.id}/shown`, {}).catch(error => {
          if (version === epoch.current) setError(studentFailure(error));
        });
      }
    });
    return () => cancelAnimationFrame(frame);
  }, [webNotice, open, studentView]);

  const loseSession = useCallback((error: unknown) => {
    setWebNotice(null);
    setWaitingSince(null); setConfirmClose(false);
    if (studentView && ownsSession.current && error instanceof StudyApiError && error.code === "network") {
      ++epoch.current; abort.current?.abort();
      setBusy(false); locked.current = false; setConnected(false);
      setError("Se ha perdido la conexión. La conversación sigue en pantalla mientras se recupera la sesión.");
      return;
    }
    ownsSession.current = false;
    ++epoch.current; abort.current?.abort(); setRows([]); setPending(null); setTechnical(null);
    setWebReceipt(null); setWebState(null);
    setOpen(false); setBusy(false); locked.current = false; setConnected(false);
    if (error instanceof StudyApiError && error.code === "runtime_expired") setRuntimeEnded(true);
    setError(studentView ? studentFailure(error) : failureMessage(error, runtime.current, performance.now()));
  }, [studentView]);

  useEffect(() => {
    if (!studentView || !open || connected) return;
    const timer = window.setInterval(() => {
      if (performance.now() - lastContact.current >= 15000) loseSession(new StudyApiError("", "lease_expired"));
    }, 500);
    return () => window.clearInterval(timer);
  }, [studentView, open, connected, loseSession]);

  useEffect(() => {
    if (!clock) return;
    const timer = window.setInterval(() => setNow(performance.now()), 500);
    return () => window.clearInterval(timer);
  }, [clock]);

  useEffect(() => {
    if (!runtimeExpired(clock, now) || expiredHandled.current) return;
    expiredHandled.current = true;
    setRuntimeEnded(true);
    ++epoch.current; abort.current?.abort(); setRows([]); setPending(null); setTechnical(null);
    setOpen(false); setBusy(false); locked.current = false; setConnected(false);
    setError(failureMessage(new StudyApiError("", "runtime_expired"), clock, now));
  }, [clock, now]);

  useEffect(() => {
    function discard() {
      ++epoch.current; abort.current?.abort();
      if (studentView && !ownsSession.current) return;
      ownsSession.current = false;
      void fetch("/api/v1/study-lab/close", { method: "POST", keepalive: true });
    }
    window.addEventListener("pagehide", discard);
    return () => { window.removeEventListener("pagehide", discard); discard(); };
  }, [studentView]);

  useEffect(() => {
    if (!open) return;
    const timer = window.setInterval(() => {
      if (!studentView && document.visibilityState !== "visible") return;
      const version = epoch.current;
      const sampledAt = performance.now();
      void api("state").then(state => {
        if (version === epoch.current) updateState(state, sampledAt);
      }).catch(error => {
        if (version !== epoch.current) return;
        loseSession(error);
      });
    }, 3000);
    return () => window.clearInterval(timer);
  }, [open, studentView, loseSession, updateState]);

  useEffect(() => {
    if (!pending) return;
    const version = epoch.current;
    let disposed = false;
    // Acknowledge only the exact inert text committed to the visible DOM.
    const frame = requestAnimationFrame(() => {
      if (disposed || !acceptResponse(version, epoch.current, runtime.current, performance.now()) || candidate.current?.textContent !== pending.diagnostic_preview) return;
      void api(`${pending.id}/shown`, {}).then(() => {
        if (!disposed && acceptResponse(version, epoch.current, runtime.current, performance.now())) {
          setRows(old => old.some(row => row.id === pending.id) ? old : [...old, pending]); setPending(null);
          const deliveredQuestion = attempt.current?.question ?? pending.question;
          setQuestion(draft => draft === deliveredQuestion ? "" : draft);
          attempt.current = null; setFocusChange(false); setBusy(false); locked.current = false;
        }
      }).catch(e => {
        if (!disposed && version === epoch.current) {
          loseSession(e);
        }
      });
    });
    return () => { disposed = true; cancelAnimationFrame(frame); };
  }, [pending, loseSession]);

  async function enter() {
    if (locked.current || runtimeEnded || runtimeExpired(runtime.current, performance.now())) return;
    locked.current = true; setBusy(true); setError(""); setWaitingSince(null); setConfirmClose(false); followLatest.current = true; setAtLatest(true);
    const version = ++epoch.current;
    try {
      if (onAuthorize) await onAuthorize();
      const state = await api("open", { ephemeral_inspection_consent: true });
      if (version === epoch.current) { ownsSession.current = true; setRows([]); setOpen(true); setConnected(true); updateState(state); }
    } catch (e) { if (version === epoch.current) loseSession(e); }
    finally { if (version === epoch.current) { locked.current = false; setBusy(false); } }
  }

  async function send(e: FormEvent) {
    e.preventDefault();
    if (locked.current || !canSend(open, connected, modelReady, busy, question, runtime.current, performance.now(), quotaRef.current)) return;
    locked.current = true; setBusy(true); setError(""); setTechnical(null); setWaitingSince(performance.now());
    followLatest.current = true; setAtLatest(true);
    const version = ++epoch.current;
    const controller = new AbortController(); abort.current = controller;
    try {
      attempt.current = {id: crypto.randomUUID(), question};
      const result = await api("turn", { ...attempt.current, ...(!studentView ? { focus_change: focusChange } : {}) }, controller.signal);
      if (!acceptResponse(version, epoch.current, runtime.current, performance.now())) return;
      setWebNotice(null);
      updateState(result);
      if (result.status === "prepared_unverified") {
        const receipt = await api(`${result.id}/display`, undefined, controller.signal);
        if (acceptResponse(version, epoch.current, runtime.current, performance.now())) { setPending(receipt); return; }
      } else {
        const receipt = await api(`${result.id}/receipt`, undefined, controller.signal);
        if (version === epoch.current) {
          const webLimits: Record<string, string> = {
            web_scope_uncertain: "No he podido confirmar el alcance o qué información falta. Puedes precisar la pregunta.",
            web_no_evidence: "No he encontrado información externa utilizable. Puedes reformular la pregunta o consultar el material docente.",
            web_review_unresolved: "No he podido contrastar suficientemente la información de Internet. No la incorporo a una respuesta.",
            web_conflict: "La información de Internet presenta un posible conflicto con el material docente. No la incorporo como explicación; consulta al profesor.",
          };
          setTechnical(receipt); setError(studentView ? (webLimits[result.failure_code] ?? (result.failure_code === "review_unresolved" ? "No he podido completar una respuesta revisada. Puedes precisar la pregunta o intentarlo más tarde." : "No he podido completar la respuesta. Puedes reformular la pregunta o intentarlo más tarde.")) : generationMessage(result.status, result.failure_code ?? receipt.failure_code));
        }
      }
    } catch (e) { if (version === epoch.current) loseSession(e); }
    if (version === epoch.current) { setBusy(false); locked.current = false; }
  }

  async function reconnect() {
    if (locked.current || !open || runtimeExpired(runtime.current, performance.now())) return;
    const version = ++epoch.current;
    let awaitingDisplay = false;
    setBusy(true); locked.current = true; setWaitingSince(null);
    const sampledAt = performance.now();
    try {
      const snapshot = await api("resume");
      if (!acceptResponse(version, epoch.current, runtime.current, performance.now())) return;
      updateState(snapshot, sampledAt);
      if (!acceptResponse(version, epoch.current, runtime.current, performance.now())) return;
      setRows(snapshot.messages); setPending(snapshot.candidate);
      if (snapshot.candidate) {
        setConnected(true); setError(""); awaitingDisplay = true;
      } else if (snapshot.busy) {
        setConnected(false); setError("El servicio sigue preparando la respuesta. Puedes volver a comprobar la conexión o finalizar.");
      } else {
        setConnected(true); setError("Conexión recuperada.");
        if (attempt.current && snapshot.messages.some((row: Receipt) => row.id === attempt.current?.id)) {
          if (question === attempt.current.question) setQuestion("");
          attempt.current = null;
        }
      }
    } catch (e) { if (version === epoch.current) loseSession(e); }
    finally { if (version === epoch.current && !awaitingDisplay) { setBusy(false); locked.current = false; } }
  }

  async function downloadReport(format: "json" | "markdown") {
    const version = epoch.current;
    setExporting(true);
    setExportError("");
    const controller = new AbortController();
    const timer = window.setTimeout(() => controller.abort(), 15000);
    try {
      const response = await fetch(`/api/v1/study-lab/export?format=${format}`, {credentials: "same-origin", cache: "no-store", signal: controller.signal});
      if (!response.ok) throw new Error("export unavailable");
      const blob = await response.blob();
      if (version !== epoch.current) return;
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url; anchor.download = `oralia-sesion.${format === "json" ? "json" : "md"}`;
      document.body.appendChild(anchor); anchor.click(); anchor.remove();
      window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    } catch {
      if (version === epoch.current) setExportError("No se ha podido descargar la sesión. La conversación se conserva mientras sigas aquí.");
    } finally { window.clearTimeout(timer); setExporting(false); }
  }

  async function stop(close: boolean) {
    setWebNotice(null);
    setConfirmClose(false); setWaitingSince(null);
    ++epoch.current; abort.current?.abort(); setPending(null); setTechnical(null);
    setWebReceipt(null);
    setBusy(true); locked.current = true;
    if (provider.startsWith("REAL_")) { setModelReady(false); setModelPreparing(false); }
    if (close) { ownsSession.current = false; attempt.current = null; setOpen(false); setRows([]); setQuestion(""); }
    try { await api(close ? "close" : "cancel", {}); setError(close ? (studentView ? "Conversación finalizada." : "Inspección cerrada; contenido descartado.") : "Petición cancelada."); }
    catch (e) { setError(close ? "Inspección cerrada y contenido descartado en esta pestaña. No se pudo confirmar el cierre con el servidor; su lease no se seguirá renovando." : failureMessage(e, runtime.current, performance.now())); }
    finally { setBusy(false); locked.current = false; }
  }

  async function prepareModel() {
    const version = epoch.current;
    setModelPreparing(true); setError("");
    try {
      const state = await api("prepare", {});
      if (version === epoch.current) updateState(state);
    } catch (e) { if (version === epoch.current) loseSession(e); }
  }

  async function inspectWeb(concept: string) {
    const localReceipt = technical?.id ?? rows.at(-1)?.id;
    if (locked.current || !localReceipt) return;
    locked.current = true; setBusy(true); setWebReceipt(null); setError("");
    const version = ++epoch.current;
    const controller = new AbortController(); abort.current = controller;
    try {
      const result = await api("web-inspect", { id: crypto.randomUUID(), local_receipt: localReceipt, concept, confirmed_in_scope_gap: true, notice_shown: true }, controller.signal);
      if (version === epoch.current) setWebReceipt(result);
    } catch (e) {
      if (version === epoch.current) setError(failureMessage(e, runtime.current, performance.now()));
    } finally { if (version === epoch.current) { locked.current = false; setBusy(false); } }
  }

  function sources(row: Receipt) {
    if (studentView) {
      const groups = groupStudySources(row.retrieval?.passages ?? []);
      return <>{groups.length > 0 && <details><summary>Fuentes consultadas</summary><ul>{groups.map(([key, group]) => <li key={key}><span>{group[0].filename}: </span>{group.map((p, index) => <span key={p.original_url}>{index > 0 ? ", " : ""}<a href={p.original_url} aria-label={`${p.filename}, página ${p.page}`} target="_blank" rel="noreferrer">página {p.page}</a></span>)}</li>)}</ul></details>}{!!row.review_notice?.items?.length && <section className="study-review-notice" role="note" aria-label="Aviso sobre la respuesta"><strong>Aviso</strong><ul>{row.review_notice.items.map(item => <li key={item.kind}>{item.message}</li>)}</ul><p>{row.review_notice.guidance}</p></section>}{!!row.web_sources?.length && <section className="study-internet" aria-label="Información de Internet"><strong>Información de Internet</strong><ul>{row.web_sources.map(source => <li key={source.url}>{source.title} · {source.entity}: <a href={source.url} target="_blank" rel="noreferrer">{source.url}</a></li>)}</ul></section>}</>;
    }
    return <details><summary>Fuentes consultadas y pasajes recibidos</summary>
      {row.retrieval?.passages.map(p => <article key={p.id}>
        <p>{p.filename}, página {p.page}. {p.section}</p>
        <a href={p.original_url} target="_blank" rel="noreferrer">Abrir original local en esta página</a>
        <pre style={{ whiteSpace: "pre-wrap" }}>{p.text}</pre>
      </article>)}
      <p>Omisiones de contexto: {JSON.stringify(row.retrieval?.omitted_context ?? [])}</p>
    </details>;
  }

  if (studentView) return <section className={`study-conversation${open ? " is-open" : ""}`} aria-label="Conversación de autoestudio">
    {provider.startsWith("FIXTURE") && <p role="note">Modo de prueba con respuestas simuladas.</p>}
    {!open && !runtimeEnded && <><p>Puedes preguntar sobre el material de la asignatura. Las respuestas pueden contener errores: contrástalas con el material. La conversación se conserva temporalmente durante esta sesión.</p><p>Este asistente funciona con modelos que se ejecutan en un ordenador de la universidad; tus preguntas no se envían a servicios de IA externos. Tu correo @alumnos.upm.es se comprueba mediante Cloudflare Access. Cuando una respuesta recibe un aviso de posible error o el asistente rechaza una pregunta, esa pregunta y la respuesta (sin tu nombre ni tu correo) se guardan para que el profesor mejore el sistema y se borran al terminar el curso. No escribas datos personales tuyos ni de otras personas. El uso es voluntario y no afecta a tu calificación.</p><button disabled={busy} onClick={() => void enter()}>Entendido, comenzar</button></>}
    {error && <p role="status">{runtimeEnded ? "La sesión ha finalizado." : error}</p>}
    {open && <>
      <div className="study-sessionbar"><button disabled={busy && !abort.current} onClick={() => setConfirmClose(true)}>Finalizar</button></div>
      {!connected && <button disabled={busy} onClick={() => void reconnect()}>Recuperar conexión</button>}
      <div className="study-log-frame">
      <div ref={messageLog} className="study-messages" role="log" aria-label="Mensajes de autoestudio" aria-live="polite" aria-relevant="additions text" onScroll={e => { const log = e.currentTarget; const latest = log.scrollHeight - log.scrollTop - log.clientHeight < 48; followLatest.current = latest; setAtLatest(latest); }}>{rows.map(row => <article key={row.id}><div className="study-user-message"><span className="study-author">Tú</span><h2>{row.question}</h2></div><span className="study-author">ORALIA</span><pre>{row.diagnostic_preview}</pre>{sources(row)}</article>)}
      {pending && <article><div className="study-user-message"><span className="study-author">Tú</span><h2>{pending.question}</h2></div><span className="study-author">ORALIA</span><pre ref={candidate}>{pending.diagnostic_preview}</pre>{sources(pending)}</article>}
      {!pending && partial && <article className="study-streaming" aria-live="off"><div className="study-user-message"><span className="study-author">Tú</span><h2>{attempt.current?.question}</h2></div><span className="study-author">ORALIA</span><pre>{partial.text}</pre><p className="study-streaming-state">{partial.phase === "reviewing" ? "Comprobando la respuesta…" : "Escribiendo la respuesta…"}</p></article>}</div>
      {!atLatest && <button className="study-latest" onClick={() => { followLatest.current = true; setAtLatest(true); if (messageLog.current) messageLog.current.scrollTop = messageLog.current.scrollHeight; }}>Ver últimos mensajes</button>}
      </div>
      <div className="study-composer">
      {webNotice && <p ref={webNoticeElement} role="status">{webNotice.text}</p>}
      {!modelReady && <><p role="status">{modelPreparing ? "Restableciendo el servicio…" : "El servicio no está disponible en este momento."}</p>{!modelPreparing && <button disabled={busy || runtimeEnded || quota?.exhausted} onClick={() => void prepareModel()}>Reintentar</button>}</>}
      {quota?.exhausted && <p role="status">El presupuesto de este ensayo técnico se ha agotado. Puedes finalizarlo.</p>}
      <QuestionForm studentView inputRef={questionInput} waitingSince={waitingSince} question={question} busy={busy} focusChange={false}
        enabled={canSend(open, connected, modelReady, busy, question, clock, now, quota)} deadlineSeconds={deadlineSeconds}
        onSubmit={e => void send(e)} onQuestion={setQuestion} onFocus={setFocusChange} onCancel={() => void stop(false)} />
      </div>
      <dialog ref={closeDialog} className="study-close-dialog" aria-labelledby="study-close-title" aria-describedby="study-close-description" onCancel={() => setConfirmClose(false)}>
        <h2 id="study-close-title">¿Finalizar la conversación?</h2>
        <p id="study-close-description">Se descartarán los mensajes de esta sesión y el borrador que no hayas enviado.</p>
        <p>Puedes descargar una copia local antes de finalizar. Esa copia no se borra al cerrar; no incluye audio ni calificaciones.</p>
        {exportError && <p role="alert">{exportError}</p>}
        <button type="button" disabled={busy || exporting} onClick={() => void downloadReport("json")}>Descargar sesión JSON</button>
        <button type="button" disabled={busy || exporting} onClick={() => void downloadReport("markdown")}>Descargar sesión Markdown</button>
        <button ref={continueButton} type="button" autoFocus onClick={() => setConfirmClose(false)}>Seguir estudiando</button>
        <button type="button" disabled={exporting} onClick={() => void stop(true)}>Finalizar y descartar</button>
      </dialog>
    </>}
  </section>;

  return <section aria-labelledby="diagnostic-study-title">
    <h3 id="diagnostic-study-title">Inspección docente de candidatas — laboratorio</h3>
    <p role="note"><strong>IA: contenido no verificado (unverified). Suficiencia no evaluada (not_assessed).
      Participante cerrado.</strong> Esta inspección no aprueba calidad académica.</p>
    <p>Proveedor: <strong>{provider}</strong>. {provider === "disconnected" ? "Generador desconectado; no se carga un LLM al enviar." : provider.startsWith("FIXTURE") ? "FIXTURE de transporte CPU; no genera contenido académico." : runtimeEnded || runtimeExpired(clock, now) ? "Runtime caducado; generación deshabilitada." : !connected ? "Conexión con el servidor sin confirmar; generación deshabilitada." : !modelReady ? modelPreparing ? "Modelo en preparación." : "Modelo detenido." : "Proveedor local de inspección; candidatas sin verificar."}</p>
    {deadlineSeconds === 200 && <p>Autocrítica experimental: una revisión, como máximo una reparación y una revisión posterior. Máximo 50 segundos por llamada y 200 por pregunta. Un resultado sin objeciones no significa aprobación.</p>}
    {deadlineSeconds === 180 && <p>Perfil de estudio ampliado optativo: hasta 2048 tokens, 180 segundos por pregunta y 16000 caracteres por respuesta. Se conserva íntegra la respuesta mostrada al continuar. El cupo y el plazo global no se renuevan.</p>}
    <p>El tratamiento de tablas y ciertas estructuras gráficas es limitado. Algunas preguntas pueden requerir consultar el original o no disponer de evidencia suficiente.</p>
    <p>Al entrar autoriza memoria temporal de preguntas y candidatas para esta inspección local. Se descarta al cerrar o caducar el acceso; sin conexión se purga en hasta 16 segundos. No se guarda una transcripción en disco.</p>
    <RuntimeNotice clock={clock} now={now} deadlineSeconds={deadlineSeconds} />
    {quota && <p role="status">Cupo del runtime: {quota.remaining} de {quota.maximum} llamadas restantes ({quota.used} consumidas). Los reintentos que llegan al proveedor cuentan; cerrar o reabrir no renueva el cupo.{quota.exhausted && " Cupo agotado; envío deshabilitado."}</p>}
    {open && !quota && <p>Este servidor no informa del cupo restante; no se presume que esté agotado.</p>}
    {open && <p>Conexión de inspección: comprobación cada 3 segundos mientras esta pestaña está visible; caduca tras 15 segundos sin actividad de conexión. Esto no renueva el runtime global.</p>}
    {error && <p role="status">{error}</p>}
    {!open && <button disabled={busy || runtimeEnded || runtimeExpired(clock, now)} onClick={() => void enter()}>Entrar en inspección temporal</button>}
    {(open || question.length > 0) && <>
      {open && <button disabled={busy && !pending && !abort.current} onClick={() => void stop(true)}>Cerrar inspección y descartar</button>}
      {open && !modelReady && <p role="status">{modelPreparing ? "Preparando el modelo local; espere a que termine." : "El modelo local está detenido. Recárguelo para seguir."}</p>}
      {open && !modelReady && <button disabled={busy || modelPreparing || runtimeExpired(clock, now) || quota?.exhausted} onClick={() => void prepareModel()}>Recargar modelo local</button>}
      <QuestionForm question={question} busy={busy} focusChange={focusChange}
        enabled={canSend(open, connected, modelReady, busy, question, clock, now, quota)} deadlineSeconds={deadlineSeconds}
        onSubmit={e => void send(e)} onQuestion={setQuestion} onFocus={setFocusChange} onCancel={() => void stop(false)} />
      {rows.map(row => <article key={row.id}><h4>Pregunta: {row.question}</h4>
        <p>Candidata diagnóstica unverified — {row.provider_kind}</p>
        <pre style={{ whiteSpace: "pre-wrap" }}>{row.diagnostic_preview}</pre>{sources(row)}
        <details><summary>Texto bruto del proveedor (sin autoridad de publicación)</summary><pre>{row.raw_candidate}</pre></details>
        {row.review_repair != null && <details><summary>Candidata inicial, revisión y reparación (no verificadas)</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(row.review_repair, null, 2)}</pre></details>}
      </article>)}
      {pending && <article><p>Candidata diagnóstica unverified — {pending.provider_kind}</p>
        <pre ref={candidate} style={{ whiteSpace: "pre-wrap" }}>{pending.diagnostic_preview}</pre>{sources(pending)}</article>}
      {technical && <details><summary>Recibo técnico incompleto; no añadido al historial</summary><pre>{JSON.stringify(technical, null, 2)}</pre></details>}
      {open && <WebInspection state={webState} localReceipt={technical?.id ?? rows.at(-1)?.id ?? null} busy={busy} inspect={inspectWeb} cancel={() => void stop(false)} />}
      {open && webState?.enabled && webReceipt && <WebEvidenceView receipt={webReceipt} />}
    </>}
  </section>;
}
