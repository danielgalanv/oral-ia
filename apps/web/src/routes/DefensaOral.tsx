import ClosedConversation from "../components/ClosedConversation";
import SessionPrivacyControls from "../components/SessionPrivacyControls";
import SessionRecovery from "../components/SessionRecovery";
import DialogueCapabilities from "../components/DialogueCapabilities";
import UnknownTurn from "../components/UnknownTurn";
import DialogueActions, { controlLabel } from "../components/DialogueActions";
import { FormEvent, useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import {
  ApiError,
  confirmDefenseTranscript,
  DefenseSpeechDescriptor,
  DefenseTranscriptResponse,
  endDefenseSession,
  getDefenseSettings,
  getDefenseTranscript,
  DefenseSessionTranscript,
  requestDefenseSpeech,
  startSession,
  StartSessionResponse,
  DialogueStatus,
  submitDefenseTurn,
  submitDefenseVoice,
  UnknownTurnResult,
  DialogueControl,
} from "../api/client";

type Entry = {
  role: "participant" | "system";
  text: string;
  speech?: DefenseSpeechDescriptor;
  sources?: Awaited<ReturnType<typeof submitDefenseTurn>>["sources"];
  generalKnowledgeUsed?: boolean;
};

export default function DefensaOral() {
  const [capability, setCapability] = useState<DialogueStatus | null>(null);
  const [pending, setPending] = useState<UnknownTurnResult | null>(null);
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
  const [input, setInput] = useState("");
  const [turns, setTurns] = useState<Entry[]>([]);
  const [transcript, setTranscript] =
    useState<DefenseTranscriptResponse | null>(null);
  const [correction, setCorrection] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [ended, setEnded] = useState<string | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [paused, setPaused] = useState(false);
  const [busy, setBusy] = useState(false);
  const [pace, setPace] = useState("1");
  const [retainTranscript, setRetainTranscript] = useState(false);
  const [retainSummary, setRetainSummary] = useState(false);
  const [review, setReview] = useState<DefenseSessionTranscript | null>(null);
  const [reviewingClose, setReviewingClose] = useState(false);
  const [summary, setSummary] = useState<Record<string, unknown> | null>(null);
  const [settings, setSettings] = useState({
    allowed_retention_scopes: undefined as string[] | undefined,
    voice_input_allowed: false,
    voice_output_allowed: false,
    transcript_retention_authorized: false,
    low_confidence_threshold: 0.6,
  });
  const audio = useRef<HTMLAudioElement | null>(null);
  const recorder = useRef<MediaRecorder | null>(null);
  const chunks = useRef<Blob[]>([]);
  const mayUpload = useRef(true);
  const pendingSpeech = useRef<AbortController | null>(null);
  const mounted = useRef(true);
  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
      pendingSpeech.current?.abort();
      if (recorder.current?.state === "recording") recorder.current.stop();
      recorder.current?.stream.getTracks().forEach((track) => track.stop());
    };
  }, []);

  useEffect(
    () => () => {
      if (audioUrl) URL.revokeObjectURL(audioUrl);
    },
    [audioUrl],
  );

  function closureConsent() {
    const scope = [
      ...(retainTranscript ? ["transcript"] : []),
      ...(retainSummary ? ["summary"] : []),
    ];
    return { retain: scope.length > 0, scope };
  }

  async function start(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    try {
      const created = await startSession(participantCode, activityId);
      setSession(created);
      terminal.current = false;
      try {
        const nextSettings = await getDefenseSettings(created.session_id);
        setSettings({
          ...nextSettings,
          allowed_retention_scopes: nextSettings.allowed_retention_scopes,
        });
      } catch {
        /* Text remains available. */
      }
      display(await submitDefenseTurn(created.session_id, ""));
      setError(null);
    } catch (reason) {
      if (reason instanceof UnknownTurnResult) setPending(reason);
      setError(
        reason instanceof ApiError
          ? reason.detail
          : "No se pudo iniciar la defensa.",
      );
    } finally {
      setBusy(false);
    }
  }

  function display(result: Awaited<ReturnType<typeof submitDefenseTurn>>) {
    if (!mounted.current || terminal.current) return;
    setInput("");
    if (result.replay_content_withheld) setError("El envío está confirmado. Este resultado no incluye contenido que pueda volver a mostrarse; no se ha creado otro turno.");
    setPending(null);
    if (result.dialogue_status) setCapability(result.dialogue_status);
    const confirmed = result.dialogue_status?.conservation;
    if (confirmed) { setRetainTranscript(confirmed.scope.includes("transcript")); setRetainSummary(confirmed.scope.includes("summary")); }
    if (result.defense_summary) setSummary(result.defense_summary);
    if (result.dialogue_action === "finish") stopCapture();
    if (result.output_text === null) {
      if (result.dialogue_action === "finish") {
        terminal.current = true;
        setEnded(result.session_status ?? "closed_error_safe");
        clearContent((confirmed ?? closureConsent()).scope);
      }
      return;
    }
    setTurns((previous) => [
      ...previous,
      {
        role: "system",
        text: result.output_text!,
        speech: result.speech ?? undefined,
        sources: result.sources,
        generalKnowledgeUsed: result.general_knowledge_used,
      },
    ]);
    if (result.dialogue_action === "finish") {
      terminal.current = true;
      setEnded(result.session_status ?? "closed_limit_reached");
      clearContent((confirmed ?? closureConsent()).scope);
    }
  }

  async function send(e: FormEvent) {
    e.preventDefault();
    await sendTurn(input);
  }

  async function sendTurn(text: string, control?: DialogueControl) {
    if (!session || (!text.trim() && !control) || paused || ended || busy || pending) return;
    setBusy(true);
    setInput("");
    setTurns((previous) => [...previous, { role: "participant", text: control ? controlLabel(control) : text }]);
    try {
      display(
        await submitDefenseTurn(session.session_id, text, closureConsent(), control),
      );
    } catch (reason) {
      if (reason instanceof UnknownTurnResult) setPending(reason);
      setError(reason instanceof UnknownTurnResult ? reason.message : "No se pudo enviar la respuesta.");
      setInput(text);
    } finally {
      setBusy(false);
    }
  }

  async function startRecording() {
    if (recorder.current?.state === "recording") return;
    let capturedStream: MediaStream | null = null;
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      capturedStream = stream;
      mayUpload.current = true;
      if (!mounted.current) {
        stream.getTracks().forEach((track) => track.stop());
        return;
      }
      const next = new MediaRecorder(stream);
      chunks.current = [];
      next.ondataavailable = (event) => chunks.current.push(event.data);
      next.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());
        if (!session || !mounted.current || !mayUpload.current) return;
        try {
          const provisional = await submitDefenseVoice(
            session.session_id,
            new Blob(chunks.current, {
              type: next.mimeType.split(";")[0] || "audio/webm",
            }),
          );
          setTranscript(provisional);
          setCorrection(provisional.raw_text);
        } catch {
          setError("La voz no está disponible. Continúa por texto.");
        }
      };
      recorder.current = next;
      next.start();
    } catch {
      capturedStream?.getTracks().forEach((track) => track.stop());
      setError("No se pudo capturar audio. Continúa por texto.");
    }
  }

  function stopCapture() {
    mayUpload.current = false;
    pendingSpeech.current?.abort();
    audio.current?.pause();
    if (audioUrl) URL.revokeObjectURL(audioUrl);
    setAudioUrl(null);
    if (recorder.current && recorder.current.state !== "inactive")
      recorder.current.stop();
    recorder.current?.stream.getTracks().forEach((track) => track.stop());
  }

  async function confirmTranscript() {
    if (!session || !transcript || busy || ended || paused) return;
    setBusy(true);
    const corrected = correction === transcript.raw_text ? null : correction;
    try {
      const result = await confirmDefenseTranscript(
        session.session_id,
        transcript.transcript_id,
        corrected,
        closureConsent(),
      );
      setTurns((previous) => [
        ...previous,
        { role: "participant", text: correction },
      ]);
      display(result);
      setTranscript(null);
    } catch {
      setError("No se pudo confirmar. Puedes continuar por texto.");
    } finally {
      setBusy(false);
    }
  }

  async function play(speech: DefenseSpeechDescriptor) {
    pendingSpeech.current?.abort();
    const controller = new AbortController();
    pendingSpeech.current = controller;
    try {
      const blob = await requestDefenseSpeech(speech, controller.signal);
      if (controller.signal.aborted || !mounted.current) return;
      if (audioUrl) URL.revokeObjectURL(audioUrl);
      const next = URL.createObjectURL(blob);
      setAudioUrl(next);
    } catch {
      if (!controller.signal.aborted)
        setError("No se pudo reproducir la voz; el texto sigue disponible.");
    }
  }

  function clearContent(scope: string[], eraseSummary = false) {
    setPending(null); setInput("");
    if (!scope.includes("transcript")) {
      setTurns([]); setReview(null); setTranscript(null); setCorrection(""); setCapability(null);
      setSession(previous => previous ? { ...previous, dialogue_status: undefined } : null);
      pendingSpeech.current?.abort(); audio.current?.pause(); setAudioUrl(null);
    }
    if (eraseSummary && !scope.includes("summary")) setSummary(null);
    if (eraseSummary) { setContentDeleted(true); setPrivacyEpoch(value => value + 1); }
  }

  if (!session) {
    return (
      <main>
        <h1>ORAL-IA — Defensa oral</h1>
        <SessionRecovery mode="oral_defense" onResume={setSession} />
        <DialogueCapabilities activityId={activityId} />
        {error && <p role="alert">{error}</p>}
        <p>La voz es opcional y el audio se descarta.</p>
        {import.meta.env.VITE_ORALIA_DEMO_PROFILE && (
          <p role="note">Esta demo funciona por texto, sin audio configurado. Usa demo-007; la pregunta aparecerá escrita y podrás contestar en «Tu respuesta».</p>
        )}
        <form onSubmit={start}>
          <label htmlFor="defense-code">Código seudónimo</label>
          <input
            id="defense-code"
            required
            value={participantCode}
            onChange={(e) => setParticipantCode(e.target.value)}
          />
          <label htmlFor="defense-activity">Actividad</label>
          <input
            id="defense-activity"
            required
            value={activityId}
            onChange={(e) => setActivityId(e.target.value)}
          />
          <button type="submit" disabled={busy}>
            Iniciar defensa
          </button>
        </form>
      </main>
    );
  }

  return (
    <main>
      <h1>ORAL-IA — Defensa oral</h1>
      <DialogueCapabilities configured={session.activity?.capabilities} current={capability ?? session.dialogue_status} />
      {session.activity?.capabilities?.configured_profile === "guided_controlled" && !transcript && <DialogueActions disabled={busy || paused || !!pending || !!ended} onControl={control => void sendTurn("", control)} />}
      {pending && <UnknownTurn pending={pending} onResult={result => display(result as Awaited<ReturnType<typeof submitDefenseTurn>>)} />}
      {!settings.voice_input_allowed && !settings.voice_output_allowed && (
        <p role="note">Modo texto: lee la pregunta y escribe debajo en «Tu respuesta». Audio no habilitado en esta actividad.</p>
      )}
      <p className="ai-disclosure">{session.ai_disclosure}</p>
      {error && (
        <p role="alert" className="error-message">
          {error}
        </p>
      )}
      {ended && <p role="status">Sesión finalizada ({ended}).</p>}
      {ended && session.activity?.capabilities?.screenless_text_ready && <ClosedConversation key={privacyEpoch} sessionId={session.session_id} deleted={contentDeleted} onDeleted={() => clearContent([], true)} />}
      <div className="turn-log" role="log" aria-live="polite">
        {turns.map((turn, index) => (
          <div key={index} className={turn.role}>
            <p>{turn.text}</p>
            {turn.generalKnowledgeUsed && (
              <p role="note">
                Conocimiento general; no procede de los materiales de la
                actividad.
              </p>
            )}
            {!!turn.sources?.length && (
              <details className="sources-panel">
                <summary>Fuentes utilizadas</summary>
                <ul>
                  {turn.sources.map((source, sourceIndex) => (
                    <li key={`${source.document_id}-${sourceIndex}`}>
                      Documento {source.document_id}, versión{" "}
                      {source.document_version}, {source.location_ref}
                      <blockquote>{source.fragment_text}</blockquote>
                    </li>
                  ))}
                </ul>
              </details>
            )}
            {turn.speech && (
              <button type="button" onClick={() => void play(turn.speech!)}>
                Reproducir voz
              </button>
            )}
          </div>
        ))}
      </div>
      {audioUrl && (
        <audio
          ref={audio}
          src={audioUrl}
          controls
          autoPlay
          onLoadedMetadata={() => {
            if (audio.current) audio.current.playbackRate = Number(pace);
          }}
        />
      )}
      <p>
        Defensa de práctica sin calificación. Puedes responder por texto. El
        audio se descarta tras transcribirlo; la conservación requiere tu
        elección antes del cierre voluntario o por límite. Puedes revisar la
        transcripción completa durante la sesión.
      </p>
      <p>
        Límites: {session.activity?.max_turns ?? "según actividad"} turnos;{" "}
        {session.activity?.max_duration_seconds ?? "según actividad"} segundos.
      </p>
      <button
        type="button"
        disabled={!!ended}
        onClick={() => {
          setPaused(!paused);
          audio.current?.pause();
          if (!paused && recorder.current?.state === "recording")
            recorder.current.pause();
          else if (paused && recorder.current?.state === "paused")
            recorder.current.resume();
        }}
      >
        {paused ? "Reanudar" : "Pausar"}
      </button>
      <button
        type="button"
        onClick={() => {
          const last = [...turns]
            .reverse()
            .find((turn) => turn.role === "system");
          if (last?.speech) void play(last.speech);
          else if (last) setTurns((previous) => [...previous, last]);
        }}
      >
        Repetir pregunta
      </button>
      <label>
        Ritmo de voz
        <select
          value={pace}
          onChange={(event) => {
            setPace(event.target.value);
            if (audio.current)
              audio.current.playbackRate = Number(event.target.value);
          }}
        >
          <option value="0.75">Lento</option>
          <option value="1">Normal</option>
          <option value="1.25">Rápido</option>
        </select>
      </label>
      {transcript ? (
        <section>
          <h2>Revisa la transcripción</h2>
          <p>Los fragmentos marcados pueden necesitar corrección.</p>
          <ol aria-label="Segmentos transcritos">
            {transcript.segments.map((segment, index) => (
              <li
                key={`${index}-${segment.start_ms ?? "start"}`}
                className={
                  segment.confidence <
                  (settings.low_confidence_threshold ?? 0.6)
                    ? "low-confidence"
                    : undefined
                }
              >
                {segment.text}
                {segment.confidence <
                  (settings.low_confidence_threshold ?? 0.6) && (
                  <span className="sr-only"> — confianza baja</span>
                )}
              </li>
            ))}
          </ol>
          <textarea
            aria-label="Transcripción corregible"
            value={correction}
            onChange={(e) => setCorrection(e.target.value)}
          />
          <button type="button" onClick={() => void confirmTranscript()}>
            Confirmar texto
          </button>
          <button type="button" onClick={() => setTranscript(null)}>
            Continuar por texto
          </button>
        </section>
      ) : (
        <>
          <form onSubmit={send}>
            <label htmlFor="defense-input">Tu respuesta</label>
            <input
              id="defense-input"
              disabled={busy || paused || !!ended || !!pending}
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button
              type="submit"
              disabled={busy || !input.trim() || paused || !!ended || !!pending}
            >
              Enviar
            </button>
          </form>
          {settings.voice_input_allowed && (
            <>
              <button
                type="button"
                disabled={paused || !!ended}
                onClick={() => void startRecording()}
              >
                Grabar respuesta
              </button>
              <button
                type="button"
                onClick={() => {
                  if (recorder.current && recorder.current.state !== "inactive")
                    recorder.current.stop();
                }}
              >
                Detener grabación
              </button>
            </>
          )}
        </>
      )}
      {settings.transcript_retention_authorized && !ended && (
        <fieldset disabled={busy}>
          <legend>Conservación al finalizar</legend>
          <label>
            <input
              type="checkbox"
              checked={retainTranscript}
              disabled={
                settings.allowed_retention_scopes !== undefined &&
                !settings.allowed_retention_scopes.includes("transcript")
              }
              onChange={(event) => setRetainTranscript(event.target.checked)}
            />
            Conservar transcripción
          </label>
          <label>
            <input
              type="checkbox"
              checked={retainSummary}
              disabled={
                settings.allowed_retention_scopes !== undefined &&
                !settings.allowed_retention_scopes.includes("summary")
              }
              onChange={(event) => setRetainSummary(event.target.checked)}
            />
            Conservar resumen
          </label>
          <p>
            La selección se aplica también al alcanzar un límite. Sin selección,
            se eliminan al cerrar.
          </p>
        </fieldset>
      )}
      <button
        type="button"
        disabled={busy}
        onClick={async () => {
          try {
            setReview(await getDefenseTranscript(session.session_id));
          } catch {
            setError("No se pudo cargar la transcripción completa.");
          }
        }}
      >
        Revisar transcripción completa
      </button>
      {review && (
        <section aria-label="Transcripción completa de la sesión">
          <h2>Transcripción completa de la sesión</h2>
          <ol>
            {review.turns.map((turn) => (
              <li key={turn.turn_id}>
                {turn.input_text && <p>Participante: {turn.input_text}</p>}
                {turn.output_text && <p>Sistema: {turn.output_text}</p>}
              </li>
            ))}
          </ol>
          {review.transcripts.map((item) => (
            <div key={item.transcript_id}>
              <p>Original de voz: {item.raw_text}</p>
              {item.corrections.map((text, index) => (
                <p key={index}>Corrección: {text}</p>
              ))}
            </div>
          ))}
          {reviewingClose && !ended && (
            <p>
              Revisa el registro y tu elección de conservación antes de
              confirmar el cierre.
            </p>
          )}
        </section>
      )}
      <SessionPrivacyControls
        sessionId={session.session_id}
        ended={!!ended}
        allowChoice={false}
        onContentScope={clearContent}
      />
      {summary && (
        <pre aria-label="Resumen descriptivo">
          {JSON.stringify(summary, null, 2)}
        </pre>
      )}
      <button
        type="button"
        disabled={!!ended || busy}
        onClick={async () => {
          stopCapture();
          try {
            if (!reviewingClose) {
              setReview(await getDefenseTranscript(session.session_id));
              setReviewingClose(true);
              return;
            }
            const result = await endDefenseSession(
              session.session_id,
              closureConsent(),
            );
            setEnded(result.status);
            terminal.current = true;
            setSummary(result.defense_summary);
            clearContent(closureConsent().scope);
          } catch {
            setError("No se pudo finalizar la sesión.");
          }
        }}
      >
        {reviewingClose ? "Confirmar cierre de sesión" : "Finalizar sesión"}
      </button>
    </main>
  );
}
