const DASHBOARDS = {
  estudiante: "/pages/estudiante/home.html",
  empresa:    "/pages/empresa/home.html",
  referidor:  "/pages/referidor/home.html",
  moderador:  "/pages/moderador/home.html",
};

export const auth = {
  saveSession(tokenResponse) {
    localStorage.setItem("token", tokenResponse.access_token);
    localStorage.setItem("user", JSON.stringify({
      id:           tokenResponse.user_id,
      nombre:       tokenResponse.nombre,
      tipo_usuario: tokenResponse.tipo_usuario,
    }));
  },

  clearSession() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  },

  getUser() {
    try { return JSON.parse(localStorage.getItem("user")); }
    catch { return null; }
  },

  getToken() {
    return localStorage.getItem("token");
  },

  isLoggedIn() {
    return !!this.getToken();
  },

  redirectToDashboard() {
    const user = this.getUser();
    if (!user) { window.location.href = "/login.html"; return; }
    window.location.href = DASHBOARDS[user.tipo_usuario] || "/login.html";
  },

  // Llamar al inicio de cada página protegida
  requireAuth(allowedRoles = []) {
    if (!this.isLoggedIn()) {
      window.location.href = "/login.html";
      return null;
    }
    const user = this.getUser();
    if (allowedRoles.length && !allowedRoles.includes(user.tipo_usuario)) {
      window.location.href = "/login.html";
      return null;
    }
    return user;
  },

  logout() {
    this.clearSession();
    window.location.href = "/login.html";
  },
};
