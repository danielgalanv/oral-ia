import { useState } from "react";
import DiagnosticStudy from "../components/DiagnosticStudy";

export default function StudyChat() {
  const [provider, setProvider] = useState("pending");
  const [deadline, setDeadline] = useState(600);
  async function authorize() {
    const entered = await fetch("/documentary/enter", { method: "POST" });
    if (!entered.ok) throw new Error("No se ha podido iniciar la sesión.");
    const response = await fetch("/api/v1/documentary");
    if (!response.ok) throw new Error("No se ha podido cargar el material de estudio.");
    const catalog = await response.json();
    if (!catalog.study_chat) throw new Error("El chat no está habilitado en este servidor.");
    setProvider(catalog.study_provider);
    setDeadline(catalog.study_workflow_deadline_seconds ?? 600);
  }
  return <main className="study-chat"><h1>ORALIA · Autoestudio</h1><DiagnosticStudy studentView provider={provider} deadlineSeconds={deadline} onAuthorize={authorize} /></main>;
}
