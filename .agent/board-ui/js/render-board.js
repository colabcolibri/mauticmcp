import { filteredStories } from "./filters.js";
import { state } from "./state.js";
import { escapeHtml } from "./render-state.js";
import { compactStoryNarrative } from "./story-narrative.js";

const ORDER = ["backlog", "todo", "doing", "🔶", "🧪", "✅", "🧊", "🚫"];
const ALWAYS = ["backlog", "todo", "doing", "🔶", "🧪", "✅"];
const LABELS = {
  backlog: "📋 Backlog",
  todo: "📌 Todo",
  doing: "🔨 Doing",
  "🔶": "🔶 Partial",
  "🧪": "🧪 Tests",
  "✅": "✅ Done",
  "🧊": "🧊 Frozen",
  "🚫": "🚫 Deprecated",
};
const COL_KEY = {
  backlog: "backlog",
  todo: "todo",
  doing: "doing",
  "🔶": "partial",
  "🧪": "tests",
  "✅": "done",
  "🧊": "frozen",
  "🚫": "deprecated",
};

export function groupByColumn(stories) {
  const groups = {};
  for (const col of ORDER) groups[col] = [];
  for (const story of stories) {
    const col = story.column || "backlog";
    if (!groups[col]) groups[col] = [];
    groups[col].push(story);
  }
  return groups;
}

function visibleColumns() {
  return [
    ...ALWAYS,
    ...(state.showFrozen ? ["🧊"] : []),
    ...(state.showDeprecated ? ["🚫"] : []),
  ];
}

function cardHtml(story) {
  const sel = state.selected?.id === story.id ? " is-selected" : "";
  const meta = [story.epic, story.version, story.moscow]
    .filter(Boolean)
    .map((x) => `<span class="chip">${escapeHtml(x)}</span>`)
    .join("");
  const sprint = story.sprint
    ? `<div class="card-sprint">${escapeHtml(story.sprint)}</div>`
    : "";
  const narrativeText = state.showNarrative ? compactStoryNarrative(story.preamble) : null;
  const narrative = narrativeText
    ? `<div class="card-narrative">${escapeHtml(narrativeText)}</div>`
    : "";
  return `<button type="button" class="card${sel}" data-id="${escapeHtml(story.id)}">
    <div class="card-id">${escapeHtml(story.id)}</div>
    <div class="card-title">${escapeHtml(story.title || "")}</div>
    ${narrative}
    ${sprint}
    <div class="card-meta">${meta}</div>
  </button>`;
}

function columnHtml(col, groups) {
  const cards = (groups[col] || []).map(cardHtml).join("") || `<p class="empty-note">Vazio</p>`;
  return `<section class="column" data-col="${COL_KEY[col] || col}">
      <div class="column-head"><span>${LABELS[col] || col}</span><span class="column-count">${(groups[col] || []).length}</span></div>
      <div class="column-body">${cards}</div>
    </section>`;
}

function bindCards(root) {
  root.querySelectorAll(".card").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.dispatchEvent(
        new CustomEvent("monitor:select", {
          detail: { entity: "us", id: btn.getAttribute("data-id") },
        }),
      );
    });
  });
}

function captureScroll(root) {
  const track = root.querySelector(".board-track");
  const columns = {};
  root.querySelectorAll(".board-track .column").forEach((col) => {
    const key = col.getAttribute("data-col");
    const body = col.querySelector(".column-body");
    if (key && body) columns[key] = body.scrollTop;
  });
  const mobileCol = root.querySelector(".board-mobile .column");
  const mobileBody = mobileCol?.querySelector(".column-body");
  return {
    trackLeft: track?.scrollLeft || 0,
    columns,
    mobileCol: mobileCol?.getAttribute("data-col") || "",
    mobileTop: mobileBody?.scrollTop || 0,
  };
}

function restoreScroll(root, snap) {
  if (!snap) return;
  const track = root.querySelector(".board-track");
  if (track) track.scrollLeft = snap.trackLeft;
  root.querySelectorAll(".board-track .column").forEach((col) => {
    const key = col.getAttribute("data-col");
    const body = col.querySelector(".column-body");
    if (!body || key == null) return;
    if (Object.prototype.hasOwnProperty.call(snap.columns, key)) {
      body.scrollTop = snap.columns[key];
    }
  });
  const mobileCol = root.querySelector(".board-mobile .column");
  const mobileBody = mobileCol?.querySelector(".column-body");
  if (mobileBody && mobileCol?.getAttribute("data-col") === snap.mobileCol) {
    mobileBody.scrollTop = snap.mobileTop;
  }
}

export function renderBoard(root) {
  const scroll = captureScroll(root);
  const stories = filteredStories();
  const groups = groupByColumn(stories);
  const cols = visibleColumns();
  const columns = cols.map((col) => columnHtml(col, groups)).join("");
  const mobileOptions = cols
    .map(
      (col) =>
        `<option value="${escapeHtml(col)}" ${state.mobileColumn === col ? "selected" : ""}>${LABELS[col]}</option>`,
    )
    .join("");
  if (!cols.includes(state.mobileColumn)) state.mobileColumn = "backlog";
  const mobileCards =
    (groups[state.mobileColumn] || []).map(cardHtml).join("") || `<p class="empty-note">Vazio</p>`;

  root.innerHTML = `<div class="board-track">${columns}</div>
    <div class="board-mobile">
      <div class="board-mobile-bar">
        <label class="empty-note">Coluna
          <select id="mobile-col">${mobileOptions}</select>
        </label>
      </div>
      <div class="column" data-col="${COL_KEY[state.mobileColumn] || "backlog"}">
        <div class="column-head"><span>${LABELS[state.mobileColumn] || ""}</span><span class="column-count">${(groups[state.mobileColumn] || []).length}</span></div>
        <div class="column-body">${mobileCards}</div>
      </div>
    </div>`;

  const select = root.querySelector("#mobile-col");
  select?.addEventListener("change", () => {
    state.mobileColumn = select.value;
    renderBoard(root);
  });
  bindCards(root);
  restoreScroll(root, scroll);
}
