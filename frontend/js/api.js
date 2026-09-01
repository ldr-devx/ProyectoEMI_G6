const API_BASE = "http://localhost:8000/api";

async function apiFetch(path, options = {}) {
  const token = localStorage.getItem("token");
  const headers = { "Content-Type": "application/json", ...options.headers };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (res.status === 401) {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "/login.html";
    return;
  }

  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || `Error ${res.status}`);
  return data;
}

export const api = {
  // Auth
  registro: (body) => apiFetch("/auth/registro", { method: "POST", body: JSON.stringify(body) }),
  login: (body) => apiFetch("/auth/login", { method: "POST", body: JSON.stringify(body) }),

  // Usuarios
  getMe: () => apiFetch("/usuarios/me"),
  updateMe: (body) => apiFetch("/usuarios/me", { method: "PUT", body: JSON.stringify(body) }),
  getPerfil: (id) => apiFetch(`/usuarios/${id}`),

  // Vacantes
  getVacantes: (params = {}) => {
    const q = new URLSearchParams(params).toString();
    return apiFetch(`/vacantes${q ? "?" + q : ""}`);
  },
  getVacante: (id) => apiFetch(`/vacantes/${id}`),
  publicarVacante: (body) => apiFetch("/vacantes/", { method: "POST", body: JSON.stringify(body) }),
  misVacantes: () => apiFetch("/vacantes/mis-vacantes/publicadas"),

  // Postulaciones
  postular: (vacante_id) => apiFetch("/postulaciones/", { method: "POST", body: JSON.stringify({ vacante_id }) }),
  misPostulaciones: () => apiFetch("/postulaciones/mis-postulaciones"),
  postulacionesPorVacante: (vacante_id) => apiFetch(`/postulaciones/vacante/${vacante_id}`),
  actualizarEstado: (id, body) => apiFetch(`/postulaciones/${id}/estado`, { method: "PUT", body: JSON.stringify(body) }),

  // Moderación
  getCola: () => apiFetch("/moderacion/cola"),
  getHistorial: () => apiFetch("/moderacion/historial"),
  moderarVacante: (id, body) => apiFetch(`/moderacion/vacantes/${id}`, { method: "PUT", body: JSON.stringify(body) }),

  // Notificaciones
  getNotificaciones: () => apiFetch("/notificaciones/"),
  marcarLeida: (id) => apiFetch(`/notificaciones/${id}/leer`, { method: "PUT" }),
  marcarTodasLeidas: () => apiFetch("/notificaciones/leer-todas", { method: "PUT" }),

  // Certificaciones
  agregarCertificacion: (body) => apiFetch("/certificaciones/", { method: "POST", body: JSON.stringify(body) }),
  misCertificaciones: () => apiFetch("/certificaciones/mis-certificaciones"),
  certsPendientes: () => apiFetch("/certificaciones/pendientes"),
  verificarCert: (id) => apiFetch(`/certificaciones/${id}/verificar`, { method: "PUT" }),
  rechazarCert: (id) => apiFetch(`/certificaciones/${id}/rechazar`, { method: "PUT" }),
};
