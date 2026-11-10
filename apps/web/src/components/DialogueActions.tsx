import { useState } from "react";
import { DialogueControl } from "../api/client";

const actions: Array<[DialogueControl["action"], string]> = [["repeat", "Repetir"], ["rephrase", "Otra forma"], ["help", "Ayuda"], ["continue", "Continuar"], ["topic_switch", "Otro tema"]];
const modeLabels: Record<string, string> = { doubt_resolution: "Resolver una duda", guided_explanation: "Explicación guiada", practice_questions: "Preguntas de práctica", presentation_preparation: "Preparar una exposición", concept_review: "Revisar conceptos" };

export function controlLabel(control: DialogueControl) {
  if (control.action === "topic_switch" && control.requested_topic) return `Elegir tema: ${control.requested_topic}`;
  return control.action === "mode_switch" ? modeLabels[control.requested_mode ?? ""] ?? "Cambiar modo" : actions.find(([action]) => action === control.action)?.[1] ?? "Control de diálogo";
}

export default function DialogueActions({ disabled, modes = [], onControl }: { disabled: boolean; modes?: string[]; onControl: (control: DialogueControl) => void }) {
  const [mode, setMode] = useState<DialogueControl["requested_mode"] | "">("");
  return <section aria-label="Controles de diálogo">
    {actions.map(([action, label]) => <button key={action} type="button" disabled={disabled} onClick={() => onControl({ schema_version: 2, action })}>{label}</button>)}
    {!!modes.length && <div><label htmlFor="guided-mode">Modo de estudio</label><select id="guided-mode" disabled={disabled} value={mode} onChange={event => setMode(event.target.value as DialogueControl["requested_mode"])}><option value="">Elige un modo habilitado</option>{modes.filter(value => modeLabels[value]).map(value => <option key={value} value={value}>{modeLabels[value]}</option>)}</select><button type="button" disabled={disabled || !mode || !modes.includes(mode)} onClick={() => mode && onControl({ schema_version: 2, action: "mode_switch", requested_mode: mode })}>Cambiar modo de estudio</button></div>}
  </section>;
}
