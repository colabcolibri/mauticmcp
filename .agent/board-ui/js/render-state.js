import { DEFAULT_PORT_HINT } from "./api.js";

export function renderShellError(kind, target) {
  const copy = {
    "no-db": `SQLite ausente. Na raiz do produto: python3 .agent/scripts/meridian_delivery.py bootstrap`,
    offline: `Servidor encerrado. Suba de novo: ${DEFAULT_PORT_HINT}`,
    "file-protocol": `Abra a URL impressa no terminal, não o arquivo. ${DEFAULT_PORT_HINT}`,
    "empty-board": "Nenhuma user story neste banco.",
  };
  target.innerHTML = `<p class="empty-note">${escapeHtml(copy[kind] || copy.offline)}</p>`;
}

export function setBanner(el, text) {
  if (!text) {
    el.classList.remove("is-visible");
    el.textContent = "";
    return;
  }
  el.classList.add("is-visible");
  el.textContent = text;
}

export function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}
