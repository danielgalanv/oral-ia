import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Link, useLocation } from "react-router-dom";
import Inicio from "./routes/Inicio";
import Participante from "./routes/Participante";
import Tecnica from "./routes/Tecnica";
import Autoestudio from "./routes/Autoestudio";
import Gobierno from "./routes/Gobierno";
import DefensaOral from "./routes/DefensaOral";
import StudyChat from "./routes/StudyChat";
import "./styles.css";

function SiteHeader() {
  return useLocation().pathname === "/estudio" ? null : <header><nav aria-label="Navegación general"><Link to="/">Volver al inicio</Link></nav></header>;
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <SiteHeader />
      <Routes>
        <Route path="/" element={<Inicio />} />
        <Route path="/participante" element={<Participante />} />
        <Route path="/tecnica" element={<Tecnica />} />
        <Route path="/autoestudio" element={<Autoestudio />} />
        <Route path="/estudio" element={<StudyChat />} />
        <Route path="/defensa" element={<DefensaOral />} />
        <Route path="/gobierno" element={<Gobierno />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
);
