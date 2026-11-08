import { getJson, subscribe, DEFAULT_PORT_HINT } from "./api.js";
import {
  loadPersistedFilters,
  persistFilters,
  replaceSnapshot,
  setSelected,
  setView,
  state,
} from "./state.js";
import { renderBoard } from "./render-board.js";
import { relatedStoriesHtml, renderDecisionDetail, renderDocs, renderLists } from "./render-lists.js";
import { renderMarkdown } from "./render-md.js";
import { escapeHtml, renderShellError, setBanner } from "./render-state.js";
import {
  renderFilterColumns,
  resetFilters,
  syncFiltersToSnapshot,
  updateFilterChrome,
} from "./filters.js";
import { closeTopSheet, setSheetOpen } from "./sheets.js";

const viewRoot = document.querySelector("#view-root");
const detailBody = document.querySelector("#detail-body");
const detailTitle = document.querySelector("#detail-sheet-title");
const banner = document.querySelector("#app-banner");
const liveChip = document.querySelector("#live-chip");

if (window.mermaid) {
  window.mermaid.initialize({
    startOnLoad: false,
    theme: "dark",
    securityLevel: "strict",
    themeVariables: { background: "#1e1a15", primaryTextColor: "#f3ebe0" },
  });
}

loadPersistedFilters();

function setLive(mode) {
  state.live = mode;
  liveChip.textContent = mode === "on" ? "ao vivo" : mode === "refresh" ? "atualizando" : "offline";
  liveChip.classList.toggle("is-on", mode === "on");
  liveChip.classList.toggle("is-off", mode === "off");
}

async function paint() {
  document.getElementById("app")?.setAttribute("data-view", state.view);
  viewRoot.classList.toggle("view-board", state.view === "board");
  document.querySelectorAll("#app-nav button").forEach((btn) => {
    btn.setAttribute("aria-current", btn.dataset.view === state.view ? "page" : "false");
  });
  updateFilterChrome();
  renderFilterColumns(() => {
    updateFilterChrome();
    void paint();
  });
  if (state.view === "board") renderBoard(viewRoot);
  else if (state.view === "docs") await renderDocs(viewRoot, getJson);
  else renderLists(viewRoot, state.view);
}

async function loadSnapshot() {
  if (location.protocol === "file:") {
    setLive("off");
    setBanner(banner, DEFAULT_PORT_HINT);
    renderShellError("file-protocol", viewRoot);
    return;
  }
  setLive("refresh");
  try {
    const { ok, status, data } = await getJson("/api/snapshot");
    if (!ok && data?.error) {
      replaceSnapshot(null);
      setLive("off");
      setBanner(banner, data.hint || data.error);
      renderShellError(status === 503 ? "no-db" : "offline", viewRoot);
      return;
    }
    replaceSnapshot(data);
    syncFiltersToSnapshot();
    setBanner(banner, "");
    setLive("on");
    await paint();
    if (state.view === "board" && !(data.userStories || []).length) {
      renderShellError("empty-board", viewRoot);
    }
  } catch {
    setLive("off");
    setBanner(banner, "Servidor encerrado. " + DEFAULT_PORT_HINT);
    renderShellError("offline", viewRoot);
  }
}

function bindRelated(root) {
  root.querySelectorAll("[data-us]").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.dispatchEvent(
        new CustomEvent("monitor:select", { detail: { entity: "us", id: btn.getAttribute("data-us") } }),
      );
    });
  });
}

async function openSelection(detail) {
  if (!detail?.entity) return;
  setSelected(detail);

  if (detail.entity === "decision") {
    if (detailTitle) detailTitle.textContent = "Decisão";
    setSheetOpen("detail-sheet", true);
    renderDecisionDetail(detailBody, detail.date, detail.index);
    return;
  }

  const label = detail.entity === "doc" ? detail.id : `${detail.entity.toUpperCase()} ${detail.id || ""}`;
  if (detailTitle) detailTitle.textContent = label.trim();
  setSheetOpen("detail-sheet", true);

  if (detail.entity === "doc") {
    const { ok, data } = await getJson(`/api/doc?path=${encodeURIComponent(detail.id || "")}`);
    renderMarkdown(detailBody, ok ? data.raw : `Não encontrado: ${detail.id}`);
    return;
  }

  if (!detail.id) {
    detailBody.innerHTML = `<p class="empty-note">Seleção incompleta.</p>`;
    return;
  }

  const type = detail.entity === "us" ? "us" : detail.entity;
  const { ok, data } = await getJson(
    `/api/entity?type=${encodeURIComponent(type)}&id=${encodeURIComponent(detail.id)}`,
  );
  if (ok && data.raw) {
    renderMarkdown(detailBody, data.raw);
    detailBody.insertAdjacentHTML("beforeend", relatedStoriesHtml(type, detail.id));
    bindRelated(detailBody);
    return;
  }
  detailBody.innerHTML = `<p class="empty-note">${escapeHtml(data?.error || "Não encontrado")}</p>`;
}

document.querySelectorAll("#app-nav button").forEach((btn) => {
  btn.addEventListener("click", async () => {
    setView(btn.dataset.view);
    await paint();
  });
});

document.getElementById("open-filters")?.addEventListener("click", () => {
  setSheetOpen("filter-sheet", true, "open-filters");
});
document.getElementById("close-filters")?.addEventListener("click", () => {
  setSheetOpen("filter-sheet", false, "open-filters");
});
document.getElementById("filter-sheet-backdrop")?.addEventListener("click", () => {
  setSheetOpen("filter-sheet", false, "open-filters");
});
document.getElementById("reset-filters")?.addEventListener("click", () => {
  resetFilters();
  updateFilterChrome();
  void paint();
});
document.getElementById("close-detail")?.addEventListener("click", () => {
  setSheetOpen("detail-sheet", false);
});
document.getElementById("detail-sheet-backdrop")?.addEventListener("click", () => {
  setSheetOpen("detail-sheet", false);
});
document.getElementById("toggle-frozen")?.addEventListener("click", () => {
  state.showFrozen = !state.showFrozen;
  persistFilters();
  void paint();
});
document.getElementById("toggle-deprecated")?.addEventListener("click", () => {
  state.showDeprecated = !state.showDeprecated;
  persistFilters();
  void paint();
});
document.getElementById("toggle-narrative")?.addEventListener("click", () => {
  state.showNarrative = !state.showNarrative;
  persistFilters();
  void paint();
});

document.addEventListener("keydown", (ev) => {
  if (ev.key === "Escape") closeTopSheet();
});

document.addEventListener("monitor:select", (ev) => {
  void openSelection(ev.detail);
});

void loadSnapshot();
if (location.protocol !== "file:") {
  subscribe((info) => {
    if (info?.disconnected) {
      setLive("off");
      setBanner(banner, "Servidor encerrado. " + DEFAULT_PORT_HINT);
      return;
    }
    void loadSnapshot();
  });
}
