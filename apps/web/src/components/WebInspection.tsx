import { useState } from "react";

export type WebState = { enabled: boolean; concepts: string[]; policy_version: number | null };
type Document = { title: string; entity: string; url: string; captured_at: string; edition: string | null; fragments: string[]; approval: string; duplicate_of: string | null };
export type WebReceipt = { status: string; documents: Document[]; errors: string[] };

export function WebEvidenceView({ receipt }: { receipt: WebReceipt }) {
  return <section aria-label="Información de Internet">
    <h4>Información de Internet</h4>
    <p>Documentos descargados para inspección. Respaldo externo y compatibilidad docente inciertos; no entregados al modelo ni aprobados como explicación.</p>
    <p role="status">Estado: {receipt.status}. {receipt.errors.join(", ")}</p>
    {receipt.documents.map((doc, index) => <article key={index}>
      <a href={doc.url} target="_blank" rel="noreferrer noopener">{doc.title}</a>
      <p>{doc.entity}. Edición: {doc.edition ?? "no identificada"}. Consulta: {doc.captured_at}. {doc.approval}.</p>
      {doc.duplicate_of && <p>Copia detectada; no cuenta como corroboración independiente.</p>}
      <details><summary>Texto extraído no confiable</summary><pre style={{ whiteSpace: "pre-wrap" }}>{doc.fragments.join("\n")}</pre></details>
    </article>)}
  </section>;
}

export default function WebInspection({ state, localReceipt, busy, inspect, cancel }: {
  state: WebState | null; localReceipt: string | null; busy: boolean;
  inspect: (concept: string) => Promise<void>; cancel: () => void;
}) {
  const [concept, setConcept] = useState("");
  const [confirmed, setConfirmed] = useState(false);
  if (!state?.enabled) return <p>Ampliación web deshabilitada (offline). No se consulta Internet.</p>;
  return <section aria-label="Inspección web restringida">
    <p role="note">Voy a consultar información de Internet para completar esta explicación. Solo sale el concepto académico preconfigurado; no se envían preguntas, historial ni documentos docentes.</p>
    <p>Política de actividad v{state.policy_version}. La revisión semántica autónoma está pendiente. Esta inspección no incorpora contenido externo a respuestas académicas.</p>
    <label>Concepto autorizado <select disabled={busy} value={concept} onChange={e => { setConcept(e.target.value); setConfirmed(false); }}>
      <option value="">Seleccione un concepto</option>{state.concepts.map(value => <option key={value} value={value}>{value}</option>)}
    </select></label>
    <label><input type="checkbox" checked={confirmed} disabled={busy} onChange={e => setConfirmed(e.target.checked)} />
      Como docente, dejo constancia de que este concepto pertenece a la actividad y falta respaldo local. El ranking o la ausencia de pasajes no bastan para decidirlo.
    </label>
    <button disabled={busy || !localReceipt || !concept || !confirmed} onClick={() => void inspect(concept)}>Consultar fuentes públicas para inspección</button>
    {busy && <button onClick={cancel}>Cancelar adquisición pública</button>}
  </section>;
}
