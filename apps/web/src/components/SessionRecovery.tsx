import { useState } from "react";
import { ApiError, StartSessionResponse, governanceRequest } from "../api/client";

type OwnedSession = StartSessionResponse & { mode: string };

export default function SessionRecovery({ mode, onResume }: { mode: string; onResume: (session: StartSessionResponse) => void }) {
  const [owned, setOwned] = useState<OwnedSession | null>(null);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  async function find() {
    setBusy(true);
    try {
      const result = await governanceRequest<{ session: OwnedSession | null }>("/auth/owned-session");
      setOwned(result.session);
      setMessage(result.session ? "Se encontró una sesión con tu acceso vigente." : "Este navegador no tiene acceso vigente a una sesión activa. Si perdiste el acceso, solicita un cierre docente confirmado.");
    } catch { setMessage("No se pudo recuperar un acceso vigente. El código seudónimo no permite recuperar una sesión; solicita ayuda docente."); }
    finally { setBusy(false); }
  }
  return <section aria-label="Recuperación de sesión">
    <button type="button" disabled={busy} onClick={find}>Buscar mi sesión activa</button>
    {message && <p role="status">{message}</p>}
    {owned && owned.mode === mode && <button type="button" disabled={busy} onClick={async () => {
      setBusy(true);
      try { onResume(await governanceRequest<OwnedSession>(`/sessions/${owned.session_id}/resume`)); }
      catch (error) { setMessage(error instanceof ApiError ? error.detail : "No se pudo retomar la sesión."); }
      finally { setBusy(false); }
    }}>Retomar mi sesión</button>}
    {owned && owned.mode !== mode && <a href={owned.mode === "oral_defense" ? "/defensa" : owned.mode === "self_study" ? "/autoestudio" : "/participante"}>Abrir el modo de mi sesión para retomarla</a>}
  </section>;
}

export function TeacherSessionRecovery() {
  const [active, setActive] = useState<{ session_id: string; turn_count: number } | null>(null);
  const [confirmed, setConfirmed] = useState(false);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  return <section aria-label="Gestión de sesión activa">
    <h2>Sesión activa</h2>
    <button type="button" disabled={busy} onClick={async () => {
      setBusy(true); setConfirmed(false);
      try { const result = await governanceRequest<{ session: typeof active }>("/governance/active-session"); setActive(result.session); setMessage(result.session ? "Hay una sesión activa. No la cierres si la persona sigue utilizándola." : "No hay una sesión activa."); }
      catch { setMessage("No se pudo consultar la sesión activa."); }
      finally { setBusy(false); }
    }}>Comprobar sesión activa</button>
    {active && <>
      <p>Se aplicará la elección de conservación ya registrada. Este cierre no crea consentimiento.</p>
      <label><input type="checkbox" checked={confirmed} onChange={event => setConfirmed(event.target.checked)} />He revisado la sesión y confirmo el cierre docente</label>
      <button type="button" disabled={!confirmed || busy} onClick={async () => {
        setBusy(true);
        try { await governanceRequest(`/governance/sessions/${active.session_id}/close`, { confirm: true, reason: "owner_access_lost" }); setActive(null); setConfirmed(false); setMessage("Cierre docente confirmado. La sesión única vuelve a estar disponible."); }
        catch (error) { setMessage(error instanceof ApiError ? error.detail : "No se pudo cerrar la sesión."); }
        finally { setBusy(false); }
      }}>Cerrar sesión activa con confirmación</button>
    </>}
    {message && <p role="status">{message}</p>}
  </section>;
}
