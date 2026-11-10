import { FormEvent, useEffect, useRef, useState } from "react";
import { governanceRequest } from "../api/client";

const deletedMessage = "Contenido eliminado; solo permanece un recibo técnico sin texto.";

export default function ClosedConversation({ sessionId, deleted, onDeleted }: {
  sessionId: string; deleted: boolean; onDeleted: () => void;
}) {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState(deleted ? deletedMessage : "Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido.");
  const [busy, setBusy] = useState(false);
  const generation = useRef(0);
  useEffect(() => () => { generation.current += 1; }, []);
  useEffect(() => { if (deleted) { generation.current += 1; setOutput(deletedMessage); setInput(""); setBusy(false); } }, [deleted]);
  async function send(event: FormEvent) {
    event.preventDefault();
    if (busy || !input.trim()) return;
    const current = ++generation.current;
    setBusy(true);
    try {
      const result = await governanceRequest<{ output_text: string | null; deleted?: boolean }>(`/sessions/${sessionId}/conversation-controls`, { text: input });
      if (generation.current !== current) return;
      setOutput(result.output_text ?? "No se ha autorizado una respuesta. No se ha cambiado el registro.");
      setInput("");
      if (result.deleted) onDeleted();
    } catch {
      if (generation.current === current) setOutput("No se pudo consultar el registro. No se ha confirmado ningún cambio; puedes volver a intentarlo.");
    } finally {
      if (generation.current === current) setBusy(false);
    }
  }
  return <section aria-label="Conversación del registro cerrado">
    <p>Recorrido por texto o transcripción. La integración de voz real sigue pendiente de validación.</p>
    <p role="status">{output}</p>
    <form onSubmit={send}>
      <label htmlFor="closed-conversation">Mensaje conversacional de revisión</label>
      <input id="closed-conversation" value={input} onChange={event => setInput(event.target.value)} disabled={busy} />
      <button type="submit" disabled={busy || !input.trim()}>Enviar al registro</button>
    </form>
  </section>;
}
