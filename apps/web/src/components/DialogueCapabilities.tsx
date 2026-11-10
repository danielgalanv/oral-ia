import { useEffect, useState } from "react";
import { DialogueStatus, governanceRequest } from "../api/client";

const labels: Record<string, string> = { guided_controlled: "diálogo guiado con contenido docente revisado", extractive_limited: "extractivo limitado", degraded: "capacidad reducida" };

export default function DialogueCapabilities({ activityId, configured, current }: { activityId?: string; configured?: DialogueStatus; current?: DialogueStatus | null }) {
  const [preview, setPreview] = useState<DialogueStatus | null>(null);
  useEffect(() => {
    let active = true;
    if (activityId && /^[a-f0-9-]{36}$/i.test(activityId)) {
      governanceRequest<{ capabilities?: DialogueStatus }>(`/activities/${activityId}`)
        .then(result => { if (active) setPreview(result.capabilities ?? null); })
        .catch(() => { if (active) setPreview(null); });
    } else setPreview(null);
    return () => { active = false; };
  }, [activityId]);
  const value = current ?? configured ?? preview;
  if (!value) return null;
  return <section aria-label="Capacidades de la actividad">
    <p>Perfil: {labels[value.effective_profile] ?? value.effective_profile}.</p>
    <p>Proveedor efectivo observado: {value.provider === "reviewed-unit-renderer/v1" ? "compositor de unidades docentes v1" : value.provider === "fixed-dialogue-template/v1" ? "plantilla determinista autorizada" : value.provider === "ollama_local" ? "modelo Ollama local" : value.provider === "deterministic" ? "generador determinista" : "sin observación de generación en este turno"}.</p>
    {value.effective_profile === "guided_controlled" && <p>Las respuestas se componen desde unidades docentes publicadas. No es generación libre; la utilidad con personas sigue pendiente de validación.</p>}
    {value.effective_profile === "extractive_limited" && <p>Este perfil ofrece extractos y apoyo limitado por el material disponible.</p>}
    {value.effective_profile === "degraded" && <p>La capacidad efectiva se ha reducido. Sigue las opciones de la respuesta o solicita revisión docente.</p>}
    {value.readiness_detail && <p role="status">{value.readiness_detail}</p>}
    {value.pending_question && <section aria-label="Pregunta pendiente"><h2>Pregunta actual</h2><p>{value.pending_question.text}</p></section>}
    {!!value.available_topics?.length && <p>Temas disponibles: {value.available_topics.join(", ")}. Para cambiar, escribe «cambiar de tema» y confirma el tema propuesto.</p>}
    {value.pending_topic && <p>Para confirmar el cambio, escribe «confirmo: {value.pending_topic}».</p>}
  </section>;
}
