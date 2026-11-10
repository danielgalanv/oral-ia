import { useEffect, useRef, useState } from "react";
import {
  DefenseClosureConsent,
  DefenseSessionTranscript,
  governanceRequest,
  SessionPrivacyView,
} from "../api/client";

export default function SessionPrivacyControls({
  sessionId,
  ended,
  onChoiceChange,
  allowChoice = true,
  onContentScope,
  confirmedChoice,
}: {
  sessionId: string;
  ended: boolean;
  onChoiceChange?: (choice: DefenseClosureConsent) => void;
  allowChoice?: boolean;
  onContentScope?: (scope: string[], eraseSummary?: boolean) => void;
  confirmedChoice?: DefenseClosureConsent;
}) {
  const contentScopeCallback = useRef(onContentScope);
  useEffect(() => { contentScopeCallback.current = onContentScope; }, [onContentScope]);
  const [privacy, setPrivacy] = useState<SessionPrivacyView | null>(null);
  const [scope, setScope] = useState<string[]>([]);
  useEffect(() => { if (confirmedChoice) setScope(confirmedChoice.scope); }, [confirmedChoice]);
  const [review, setReview] = useState<DefenseSessionTranscript | null>(null);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  useEffect(() => {
    let active = true;
    governanceRequest<SessionPrivacyView>(`/sessions/${sessionId}/privacy`)
      .then((value) => {
        if (active) {
          setPrivacy(value);
          if (ended || value.deleted) {
            if (!value.scope.includes("transcript")) setReview(null);
            contentScopeCallback.current?.(value.scope);
          }
        }
      })
      .catch(() => {});
    return () => {
      active = false;
    };
  }, [sessionId, ended]);
  function choose(item: string, selected: boolean) {
    const next = selected
      ? [...scope, item]
      : scope.filter((value) => value !== item);
    setScope(next);
    onChoiceChange?.({ retain: next.length > 0, scope: next });
  }
  return (
    <section aria-label="Privacidad de tu sesión">
      <h2>Privacidad de tu sesión</h2>
      <p>
        {privacy?.notice ??
          "Sesión local seudónima; la conservación requiere elección explícita. El audio se descarta."}
      </p>
      {privacy && (
        <p>
          Plazo:{" "}
          {privacy.retention_days === null
            ? "conservación no disponible"
            : `${privacy.retention_days} días`}
          . Acceso docente solo a lo consentido.
        </p>
      )}
      {allowChoice && privacy?.retention_authorized && !ended && (
        <fieldset>
          <legend>Tu elección se enviará al responder o finalizar</legend>
          <label>
            <input
              type="checkbox"
              checked={scope.includes("transcript")}
              disabled={privacy.allowed_scopes !== undefined && !privacy.allowed_scopes.includes("transcript")}
                  onChange={(event) => choose("transcript", event.target.checked)}
            />
            Conservar transcripción de esta sesión
          </label>
          <label>
            <input
              type="checkbox"
              checked={scope.includes("summary")}
              disabled={privacy.allowed_scopes !== undefined && !privacy.allowed_scopes.includes("summary")}
                  onChange={(event) => choose("summary", event.target.checked)}
            />
            Conservar resumen de esta sesión
          </label>
          <p>
            Sin seleccionar, se elimina el contenido al cerrar. No es necesario
            conservar para participar.
          </p>
        </fieldset>
      )}
      {allowChoice && (
        <button
          type="button"
          onClick={async () => {
            try {
              setReview(
                await governanceRequest<DefenseSessionTranscript>(
                  `/sessions/${sessionId}/transcript`,
                ),
              );
            } catch {
              setResult("No se pudo consultar la transcripción.");
            }
          }}
        >
          Revisar registro completo
        </button>
      )}
      {review && (
        <pre aria-label="Registro completo de tu sesión">
          {JSON.stringify(review, null, 2)}
        </pre>
      )}
      {ended && (
        <>
          <label>
            <input
              type="checkbox"
              checked={confirmDelete}
              onChange={(event) => setConfirmDelete(event.target.checked)}
            />
            Confirmo eliminar el contenido de mi sesión
          </label>
          <button
            type="button"
            disabled={!confirmDelete}
            onClick={async () => {
              try {
                await governanceRequest(
                  `/sessions/${sessionId}/content`,
                  { confirm: true },
                  "DELETE",
                );
                setReview(null);
                contentScopeCallback.current?.([], true);
                setResult(
                  "Contenido eliminado; solo permanece un recibo técnico sin texto.",
                );
              } catch {
                setResult("No se pudo eliminar el contenido.");
              }
            }}
          >
            Eliminar mi contenido
          </button>
        </>
      )}
      {result && <p role="status">{result}</p>}
    </section>
  );
}
