import { api } from "/js/api.js";
import { auth } from "/js/auth.js";

const TIPO_ICONS = {
  vacante_compatible: "🔔",
  cambio_estado_postulacion: "📋",
  vacante_aprobada: "✓",
  vacante_rechazada: "✗",
  otro: "•",
};

export async function initNotifBadge(actionsContainerId) {
  if (!auth.isLoggedIn()) return;
  const container = document.getElementById(actionsContainerId);
  if (!container) return;

  // Insertar bell + dropdown al inicio del contenedor
  const wrapper = document.createElement("div");
  wrapper.style.cssText = "position:relative; display:inline-block;";
  wrapper.innerHTML = `
    <button id="notifBell" class="btn btn-ghost" style="font-size:14px; position:relative; padding-right:var(--space-5);">
      🔔
      <span id="notifCount" style="display:none; position:absolute; top:4px; right:4px; background:var(--color-accent); color:var(--color-bg); border-radius:50%; width:14px; height:14px; font-size:9px; font-family:var(--font-heading); font-weight:700; line-height:14px; text-align:center;"></span>
    </button>
    <div id="notifDropdown" style="display:none; position:absolute; right:0; top:calc(100% + 6px); width:300px; z-index:50; border-radius:var(--radius-md); overflow:hidden; box-shadow:0 8px 24px rgba(0,0,0,0.3);" class="card">
      <div style="display:flex; align-items:center; justify-content:space-between; padding:var(--space-3) var(--space-4); border-bottom:1px solid var(--color-neutral-200);">
        <span style="font-family:var(--font-heading); font-size:12px; letter-spacing:0.08em; text-transform:uppercase; opacity:0.5;">Notificaciones</span>
        <button id="marcarTodasBtn" style="font-size:11px; opacity:0.6; background:none; border:none; cursor:pointer; color:inherit;">Marcar todas leídas</button>
      </div>
      <div id="notifList" style="max-height:320px; overflow-y:auto;"></div>
    </div>`;

  container.insertBefore(wrapper, container.firstChild);

  const bell = document.getElementById("notifBell");
  const dropdown = document.getElementById("notifDropdown");
  const countBadge = document.getElementById("notifCount");
  const lista = document.getElementById("notifList");

  let notifs = [];

  function renderNotifs() {
    if (!notifs.length) {
      lista.innerHTML = `<p style="padding:var(--space-4); font-size:13px; opacity:0.5; text-align:center;">Sin notificaciones</p>`;
      return;
    }
    lista.innerHTML = notifs.slice(0, 10).map(n => `
      <div data-id="${n.id}" style="padding:var(--space-3) var(--space-4); border-bottom:1px solid var(--color-neutral-200); opacity:${n.leida ? '0.5' : '1'}; cursor:default; transition:opacity 0.2s;">
        <div style="display:flex; gap:var(--space-2); align-items:flex-start;">
          <span style="font-size:14px; flex-shrink:0;">${TIPO_ICONS[n.tipo] || '•'}</span>
          <div style="flex:1; display:flex; flex-direction:column; gap:2px;">
            <div style="font-size:13px; font-weight:600; line-height:1.3;">${n.titulo}</div>
            <div style="font-size:12px; opacity:0.6; line-height:1.4;">${n.mensaje}</div>
          </div>
        </div>
      </div>`).join("");

    // Marcar como leída al hacer hover
    lista.querySelectorAll("[data-id]").forEach(el => {
      el.addEventListener("mouseenter", async () => {
        const id = Number(el.dataset.id);
        const notif = notifs.find(n => n.id === id);
        if (notif && !notif.leida) {
          notif.leida = true;
          el.style.opacity = "0.5";
          updateCount();
          try { await api.marcarLeida(id); } catch {}
        }
      });
    });
  }

  function updateCount() {
    const unread = notifs.filter(n => !n.leida).length;
    if (unread > 0) {
      countBadge.style.display = "block";
      countBadge.textContent = unread > 9 ? "9+" : unread;
    } else {
      countBadge.style.display = "none";
    }
  }

  async function cargar() {
    try {
      notifs = await api.getNotificaciones();
      updateCount();
    } catch {}
  }

  bell.addEventListener("click", (e) => {
    e.stopPropagation();
    const open = dropdown.style.display === "block";
    dropdown.style.display = open ? "none" : "block";
    if (!open) renderNotifs();
  });

  document.addEventListener("click", () => { dropdown.style.display = "none"; });
  dropdown.addEventListener("click", (e) => e.stopPropagation());

  document.getElementById("marcarTodasBtn").addEventListener("click", async () => {
    notifs.forEach(n => { n.leida = true; });
    updateCount();
    renderNotifs();
    try { await api.marcarTodasLeidas(); } catch {}
  });

  await cargar();
  // Refrescar cada 30 segundos
  setInterval(cargar, 30000);
}
