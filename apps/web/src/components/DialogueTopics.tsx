import { DialogueControl, DialogueStatus } from "../api/client";

export default function DialogueTopics({ current, disabled, onChoose, onConfirm }: {
  current?: DialogueStatus | null;
  disabled: boolean;
  onChoose: (control: DialogueControl) => void;
  onConfirm: () => void;
}) {
  const topics = [...new Set(current?.available_topics ?? [])];
  if (!topics.length) return null;
  const pending = current?.pending_topic;
  return <section aria-label="Elegir tema de estudio">
    <h2>¿Qué quieres estudiar?</h2>
    <p>Elige un tema publicado para consultar su explicación o practicar. Primero se propone el tema; debes confirmar el cambio.</p>
    <ul>{topics.map(topic => <li key={topic}>
      <button type="button" disabled={disabled} onClick={() => onChoose({ schema_version: 2, action: "topic_switch", requested_topic: topic })}>Elegir {topic}</button>
    </li>)}</ul>
    {pending && topics.includes(pending) && <div>
      <p>Se propone {pending}. La pregunta actual se mantiene hasta confirmar.</p>
      <button type="button" disabled={disabled} onClick={onConfirm}>Confirmar tema {pending}</button>
    </div>}
  </section>;
}
