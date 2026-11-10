import { Link } from "react-router-dom";

export default function Inicio() {
  const profile = import.meta.env.VITE_ORALIA_DEMO_PROFILE;
  return (
    <main>
      <h1>ORALIA — apoyo docente local</h1>
      <p>
        Sistema de IA: puede cometer errores y no sustituye al profesorado. No
        asigna notas.
      </p>
      {profile && (
        <section aria-label="Entorno de demostración">
          <h2>Demostración con datos ficticios</h2>
          <p>
            Generación determinista; no demuestra funcionamiento de un LLM real
            ni utilidad con personas. Voz real sin validar.
          </p>
          <p>
            {profile === "text_only"
              ? "Recorrido textual sin fuentes: embeddings no preparados."
              : "Fuentes del material ficticio recuperadas con embeddings locales."}
          </p>
          <p>
            Esta demo local permite entrar en el área docente sin credencial.
            Usa únicamente datos ficticios.
            Abre allí una actividad y usa el código ficticio{" "}
            <strong>demo-007</strong>. El código no es una contraseña.
          </p>
        </section>
      )}
      <nav aria-label="Accesos principales">
        <p>
          <Link to="/gobierno">Área docente</Link> — actividades, materiales y
          revisión autorizada.
        </p>
        <p>
          <Link to="/participante">Área participante</Link>
        </p>
        <p>
          <Link to="/autoestudio">Autoestudio</Link> ·{" "}
          <Link to="/defensa">Defensa oral por texto</Link>
        </p>
      </nav>
      <p>
        La conservación es opcional. Lee el aviso, elige sus ámbitos y cierra la
        sesión antes de abrir otra.
      </p>
    </main>
  );
}
