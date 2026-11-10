import { useRef, useState, FormEvent } from "react";
import { useSearchParams } from "react-router-dom";
import {
  ApiError,
  DefenseClosureConsent,
  startSession,
  submitStudyTurn,
  endStudySession,
  StartSessionResponse,
  StudySource,
  StudySummary,
  DialogueStatus,
  UnknownTurnResult,
  SubmitStudyTurnResponse,
  DialogueControl,
} from "../api/client";

import SessionPrivacyControls from "../components/SessionPrivacyControls";
import SessionRecovery from "../components/SessionRecovery";
import DialogueCapabilities from "../components/DialogueCapabilities";
import UnknownTurn from "../components/UnknownTurn";
import DialogueActions, { controlLabel } from "../components/DialogueActions";
import ClosedConversation from "../components/ClosedConversation";
import DialogueTopics from "../components/DialogueTopics";

// Área de autoestudio (Feature 003) — FR-005/FR-018/FR-019. Ningún dato ni decisión
// cognitiva se procesa aquí: el cliente solo llama a la API y muestra lo que ella
// devuelve (T024). El indicador de conocimiento general usa exclusivamente
// `general_knowledge_used` de la respuesta de la API — nunca se infiere en el
// frontend (remediación F7, FR-019).

type TurnEntry = {
  role: "participant" | "system";
  text: string;
  sources?: StudySource[];
  generalKnowledgeUsed?: boolean;
};

export default function Autoestudio() {
  const [searchParams] = useSearchParams();
  const [session, setSession] = useState<StartSessionResponse | null>(null);
  const terminal = useRef(false);
  const [contentDeleted, setContentDeleted] = useState(false);
  const [privacyEpoch, setPrivacyEpoch] = useState(0);
  const [participantCode, setParticipantCode] = useState(
    import.meta.env.VITE_ORALIA_DEMO_PROFILE ? "demo-007" : "",
  );
  const [activityId, setActivityId] = useState(
    () => searchParams.get("activity") ?? "",
  );
  const [error, setError] = useState<string | null>(null);
  const [turns, setTurns] = useState<TurnEntry[]>([]);
  const [input, setInput] = useState("");
  const [ended, setEnded] = useState<string | null>(null);
  const [studySummary, setStudySummary] = useState<StudySummary | null>(null);
  const [sending, setSending] = useState(false);
  const [capability, setCapability] = useState<DialogueStatus | null>(null);
  const [pending, setPending] = useState<UnknownTurnResult | null>(null);
  const [privacyChoice, setPrivacyChoice] = useState<DefenseClosureConsent>({
    retain: false,
    scope: [],
  });

  async function onStart(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      const started = await startSession(participantCode, activityId);
      setSession(started);
      terminal.current = false;
      setTurns([]);
      setEnded(null);
      setStudySummary(null);
    } catch (err) {
      setError(
        err instanceof ApiError
          ? `No se pudo iniciar la sesión: ${err.detail}`
          : "No se pudo iniciar la sesión. Compruebe los datos e inténtelo de nuevo.",
      );
    }
  }

  async function onSendTurn(e: FormEvent) {
    e.preventDefault();
    await send(input);
  }

  async function send(text: string, control?: DialogueControl) {
    if (!session || (!text.trim() && !control) || sending || pending) return;
    setError(null);
    setSending(true);
    setInput("");
    setTurns((prev) => [...prev, { role: "participant", text: control ? controlLabel(control) : text }]);
    try {
      const result = await submitStudyTurn(
        session.session_id,
        text,
        privacyChoice,
        control,
      );
      display(result);
    } catch (err) {
      if (err instanceof UnknownTurnResult) setPending(err);
      setError(err instanceof ApiError ? `No se pudo enviar el mensaje: ${err.detail}` : "El resultado del envío no está confirmado.");
    } finally {
      setSending(false);
    }
  }

  function display(result: SubmitStudyTurnResponse) {
      if (terminal.current) return;
      if (result.replay_content_withheld) setError("El envío está confirmado. Este resultado no incluye contenido que pueda volver a mostrarse; no se ha creado otro turno.");
      if (result.dialogue_status) setCapability(result.dialogue_status);
      const confirmed = result.dialogue_status?.conservation;
      if (confirmed) setPrivacyChoice(confirmed);
      if (result.output_text !== null) {
        const outputText = result.output_text;
        setTurns((prev) => [
          ...prev,
          {
            role: "system",
            text: outputText,
            sources: result.sources,
            generalKnowledgeUsed: result.general_knowledge_used,
          },
        ]);
      }
      if (result.session_closed) {
        terminal.current = true;
        setEnded(result.session_status ?? "closed_limit_reached");
        setStudySummary(result.study_summary ?? null);
        clearContent((confirmed ?? privacyChoice).scope);
      }
      setPending(null);
  }

  async function onEnd() {
    if (!session) return;
    setError(null);
    try {
      const result = await endStudySession(session.session_id, privacyChoice);
      terminal.current = true;
      setEnded(result.status);
      setStudySummary(result.study_summary);
      clearContent(privacyChoice.scope);
    } catch {
      setError("No se pudo finalizar la sesión. Puede intentarlo de nuevo.");
    }
  }

  function clearContent(scope: string[], eraseSummary = false) {
    setPending(null); setInput("");
    if (!scope.includes("transcript")) {
      setTurns([]); setCapability(null);
      setSession(previous => previous ? { ...previous, dialogue_status: undefined } : null);
    }
    if (eraseSummary && !scope.includes("summary")) setStudySummary(null);
    if (eraseSummary) { setContentDeleted(true); setPrivacyEpoch(value => value + 1); }
  }

  if (!session) {
    return (
      <main>
        <h1>ORAL-IA — Autoestudio</h1>
        <SessionRecovery mode="self_study" onResume={setSession} />
        <DialogueCapabilities activityId={activityId} />
        {error && (
          <p className="error-message" role="alert">
            {error}
          </p>
        )}
        <form onSubmit={onStart}>
          <div className="field">
            <label htmlFor="participant_code">
              Código de participante (seudónimo)
            </label>
            <input
              id="participant_code"
              required
              value={participantCode}
              onChange={(e) => setParticipantCode(e.target.value)}
              aria-describedby="participant_code_hint"
            />
            <p id="participant_code_hint">
              {import.meta.env.VITE_ORALIA_DEMO_PROFILE
                ? "Las actividades preparadas de esta demo autorizan demo-007. No escribas tu nombre."
                : "No use su nombre real ni datos personales."}
            </p>
          </div>
          <div className="field">
            <label htmlFor="activity_id">Identificador de actividad</label>
            <input
              id="activity_id"
              required
              value={activityId}
              onChange={(e) => setActivityId(e.target.value)}
            />
          </div>
          <button type="submit">Iniciar sesión</button>
        </form>
      </main>
    );
  }

  if (ended) {
    return (
      <main>
        <h1>ORAL-IA — Autoestudio</h1>
        <p role="status">Sesión finalizada ({ended}).</p>
        <SessionPrivacyControls sessionId={session.session_id} ended onContentScope={clearContent} />
        {session.activity?.capabilities?.screenless_text_ready && <ClosedConversation key={privacyEpoch} sessionId={session.session_id} deleted={contentDeleted} onDeleted={() => clearContent([], true)} />}
        {studySummary && (
          <section aria-label="Resumen de estudio">
            <h2>Resumen de estudio</h2>
            <pre>{JSON.stringify(studySummary, null, 2)}</pre>
          </section>
        )}
      </main>
    );
  }

  return (
    <main>
      <h1>ORAL-IA — Autoestudio</h1>
      <DialogueCapabilities configured={session.activity?.capabilities} current={capability ?? session.dialogue_status} />
      {session.activity?.capabilities?.configured_profile === "guided_controlled" && <DialogueActions disabled={sending || !!pending || !!ended} modes={capability?.available_modes ?? session.activity?.capabilities.available_modes} onControl={control => void send("", control)} />}
      {pending && <UnknownTurn pending={pending} onResult={result => display(result as SubmitStudyTurnResponse)} />}
      <p className="ai-disclosure" role="status">
        {session.ai_disclosure}
      </p>
      {error && (
        <p className="error-message" role="alert">
          {error}
        </p>
      )}
      <div className="turn-log" role="log" aria-live="polite">
        {turns.map((t, i) => (
          <div
            key={i}
            className={t.role === "participant" ? "participant" : "system"}
          >
            <p>{t.text}</p>
            {t.role === "system" && t.generalKnowledgeUsed && (
              <p className="general-knowledge-indicator" role="note">
                Conocimiento general (no procede de los materiales de la
                asignatura)
              </p>
            )}
            {t.role === "system" && t.sources && t.sources.length > 0 && (
              <details className="sources-panel">
                <summary>Fuentes</summary>
                <ul>
                  {t.sources.map((s, si) => (
                    <li key={si}>
                      {s.document_id} (v{s.document_version}) — {s.location_ref}
                      : {s.fragment_text}
                    </li>
                  ))}
                </ul>
              </details>
            )}
          </div>
        ))}
      </div>
      {session.activity?.capabilities?.configured_profile === "guided_controlled" && <DialogueTopics current={capability ?? session.dialogue_status} disabled={sending || !!pending || !!ended} onChoose={control => void send("", control)} onConfirm={() => void send("confirmo")} />}
      <form onSubmit={onSendTurn}>
        <label htmlFor="turn_input">Tu mensaje</label>
        <input
          id="turn_input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={sending || !!pending}
        />
        <button type="submit" disabled={sending || !input.trim() || !!pending}>
          Enviar
        </button>
      </form>
      <SessionPrivacyControls
        sessionId={session.session_id}
        ended={!!ended}
        onChoiceChange={setPrivacyChoice}
        confirmedChoice={privacyChoice}
      />
      <button disabled={sending || !!ended} onClick={onEnd}>
        Finalizar sesión
      </button>
    </main>
  );
}
