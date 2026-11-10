import { useState, FormEvent } from "react";
import {
  ApiError,
  DefenseClosureConsent,
  startSession,
  submitTurn,
  endSession,
  StartSessionResponse,
} from "../api/client";

import SessionPrivacyControls from "../components/SessionPrivacyControls";

// Área de participante — FR-010, FR-012, FR-012b. Ningún dato ni decisión cognitiva se
// procesa aquí: el cliente solo llama a la API y muestra lo que ella devuelve.

type TurnEntry = { role: "participant" | "system"; text: string };

export default function Participante() {
  const [session, setSession] = useState<StartSessionResponse | null>(null);
  const [participantCode, setParticipantCode] = useState("");
  const [activityId, setActivityId] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [turns, setTurns] = useState<TurnEntry[]>([]);
  const [input, setInput] = useState("");
  const [ended, setEnded] = useState<string | null>(null);
  const [sending, setSending] = useState(false);
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
      setTurns([]);
      setEnded(null);
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
    if (!session || !input.trim()) return;
    setError(null);
    setSending(true);
    const text = input;
    setInput("");
    setTurns((prev) => [...prev, { role: "participant", text }]);
    try {
      const result = await submitTurn(session.session_id, text, privacyChoice);
      if (result.session_status && result.session_status !== "active")
        setEnded(result.session_status);
      if (result.output_text !== null) {
        const outputText = result.output_text;
        setTurns((prev) => [...prev, { role: "system", text: outputText }]);
      }
    } catch (err) {
      setError(
        err instanceof ApiError
          ? `No se pudo enviar el mensaje: ${err.detail}`
          : "No se pudo enviar el mensaje. Puede intentarlo de nuevo.",
      );
    } finally {
      setSending(false);
    }
  }

  async function onEnd() {
    if (!session) return;
    setError(null);
    try {
      const result = await endSession(session.session_id, privacyChoice);
      setEnded(result.confirmation_message);
    } catch {
      setError("No se pudo finalizar la sesión. Puede intentarlo de nuevo.");
    }
  }

  if (!session) {
    return (
      <main>
        <h1>ORAL-IA — Participante</h1>
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
              No use su nombre real ni datos personales.
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
        <h1>ORAL-IA — Participante</h1>
        <p role="status">{ended}</p>
        <SessionPrivacyControls sessionId={session.session_id} ended />
      </main>
    );
  }

  return (
    <main>
      <h1>ORAL-IA — Participante</h1>
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
            {t.text}
          </div>
        ))}
      </div>
      <form onSubmit={onSendTurn}>
        <label htmlFor="turn_input">Tu mensaje</label>
        <input
          id="turn_input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={sending}
        />
        <button type="submit" disabled={sending || !input.trim()}>
          Enviar
        </button>
      </form>
      <SessionPrivacyControls
        sessionId={session.session_id}
        ended={!!ended}
        onChoiceChange={setPrivacyChoice}
      />
      <button disabled={sending || !!ended} onClick={onEnd}>
        Finalizar sesión
      </button>
    </main>
  );
}
