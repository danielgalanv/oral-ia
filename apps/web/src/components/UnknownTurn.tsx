import { useState } from "react";
import { ApiError, UnknownTurnResult } from "../api/client";

export default function UnknownTurn({ pending, onResult }: { pending: UnknownTurnResult; onResult: (result: unknown) => void }) {
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  async function reconcile() {
    setBusy(true);
    try {
      onResult(await pending.reconcile());
    } catch (error) {
      setMessage(error instanceof ApiError ? error.detail : "No se ha podido confirmar el resultado. No se ha enviado un turno nuevo.");
    } finally {
      setBusy(false);
    }
  }
  return <section aria-label="Envío sin confirmar">
    <p role="status">{pending.message} Recargar la página pierde esta referencia; puedes retomar tu sesión con el acceso de propietario.</p>
    <button type="button" disabled={busy} onClick={reconcile}>Consultar resultado del envío</button>
    {message && <p role="status">{message}</p>}
  </section>;
}
