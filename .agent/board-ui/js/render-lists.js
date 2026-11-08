import { filteredStories } from "./filters.js";
import { state } from "./state.js";
import { escapeHtml } from "./render-state.js";

function emit(detail) {
  document.dispatchEvent(new CustomEvent("monitor:select", { detail }));
}

function progressBar(done, total) {
  const pct = total ? Math.round((done / total) * 100) : 0;
  return `<div class="progress" aria-label="${done} de ${total}"><span style="width:${pct}%"></span></div>`;
}

function usButtons(stories) {
  if (!stories.length) return "";
  return `<div class="entity-us">${stories
    .map(
      (s) =>
        `<button type="button" data-us="${escapeHtml(s.id)}"><span class="us-id">${escapeHtml(s.id)}</span>${escapeHtml(s.title || "")}</button>`,
    )
    .join("")}</div>`;
}

function bindEntityCards(root) {
  root.querySelectorAll("[data-open]").forEach((btn) => {
    btn.addEventListener("click", () =>
      emit({ entity: btn.getAttribute("data-entity"), id: btn.getAttribute("data-open") }),
    );
  });
  root.querySelectorAll("[data-us]").forEach((btn) => {
    btn.addEventListener("click", (ev) => {
      ev.stopPropagation();
      emit({ entity: "us", id: btn.getAttribute("data-us") });
    });
  });
  root.querySelectorAll("[data-decision-date]").forEach((btn) => {
    btn.addEventListener("click", () =>
      emit({
        entity: "decision",
        date: btn.getAttribute("data-decision-date"),
        index: Number(btn.getAttribute("data-decision-index") || "0"),
      }),
    );
  });
}

function pageWrap(title, meta, inner) {
  return `<section class="view-page">
    <header class="view-page-head"><h2>${escapeHtml(title)}</h2><p>${escapeHtml(meta)}</p></header>
    ${inner}
  </section>`;
}

export function renderLists(root, kind) {
  const snap = state.snapshot || {};
  const scoped = filteredStories();
  const all = snap.userStories || [];

  if (kind === "versions") {
    const items = snap.versions || [];
    const html = items
      .map((v) => {
        const related = all.filter((s) => s.version === v.id);
        const visible = scoped.filter((s) => s.version === v.id);
        const done = related.filter((s) => s.status === "✅").length;
        return `<article class="entity-card">
          <button type="button" class="entity-card-main" data-entity="version" data-open="${escapeHtml(v.id)}">
            <div class="entity-kicker">${escapeHtml(v.id)}</div>
            <h2>${escapeHtml(v.title || v.id)}</h2>
            <div class="meta-line">${escapeHtml(v.status || "")} · ${done}/${related.length} US · ${visible.length} no filtro</div>
          </button>
          ${progressBar(done, related.length)}
          ${usButtons(visible)}
        </article>`;
      })
      .join("");
    root.innerHTML = pageWrap("Versões", `${items.length} release(s)`, html || `<p class="empty-note">Sem versões</p>`);
  } else if (kind === "sprints") {
    const items = snap.sprints || [];
    const html = items
      .map((s) => {
        const related = all.filter((st) => st.sprint === s.id);
        const visible = scoped.filter((st) => st.sprint === s.id);
        const done = related.filter((st) => st.status === "✅").length;
        return `<article class="entity-card">
          <button type="button" class="entity-card-main" data-entity="sprint" data-open="${escapeHtml(s.id)}">
            <div class="entity-kicker">${escapeHtml(s.id)}</div>
            <h2>${escapeHtml(s.title || s.id)}</h2>
            <div class="meta-line">${escapeHtml(s.version || "")} · ${escapeHtml(s.status || "")} · ${done}/${related.length} US</div>
          </button>
          ${progressBar(done, related.length)}
          ${usButtons(visible)}
        </article>`;
      })
      .join("");
    root.innerHTML = pageWrap("Sprints", `${items.length} sprint(s)`, html || `<p class="empty-note">Sem sprints</p>`);
  } else if (kind === "epics") {
    const items = snap.epics || [];
    const html = items
      .map((e) => {
        const related = all.filter((s) => s.epic === e.id);
        const visible = scoped.filter((s) => s.epic === e.id);
        const done = related.filter((s) => s.status === "✅").length;
        return `<article class="entity-card">
          <button type="button" class="entity-card-main" data-entity="epic" data-open="${escapeHtml(e.id)}">
            <div class="entity-kicker">${escapeHtml(e.id)}</div>
            <h2>${escapeHtml(e.title || e.id)}</h2>
            <div class="meta-line">${escapeHtml(e.status || "")} · ${done}/${related.length} US · ${visible.length} no filtro</div>
          </button>
          ${progressBar(done, related.length)}
          ${usButtons(visible)}
        </article>`;
      })
      .join("");
    root.innerHTML = pageWrap("Épicos", `${items.length} épico(s)`, html || `<p class="empty-note">Sem épicos</p>`);
  } else if (kind === "decisions") {
    const dates = snap.decisions?.dates || [];
    const total = snap.decisions?.totalEntries || 0;
    const html = dates
      .map((d) => {
        const entries = (d.entries || [])
          .map((en, index) => {
            const preview = en.what_changed || en.why_changed || "";
            return `<button type="button" class="decision-card" data-decision-date="${escapeHtml(d.date)}" data-decision-index="${index}">
              <div class="decision-kicker">${escapeHtml(en.time || "—")}</div>
              <h4>${escapeHtml(en.title || "(sem título)")}</h4>
              ${preview ? `<p class="decision-preview">${escapeHtml(preview)}</p>` : ""}
            </button>`;
          })
          .join("");
        return `<section class="day-block"><h3>${escapeHtml(d.date)} <span class="count">${d.count} entrada(s)</span></h3>${entries}</section>`;
      })
      .join("");
    root.innerHTML = pageWrap(
      "Decisões",
      `${total} entrada(s) em ${dates.length} dia(s) — somente leitura`,
      html || `<p class="empty-note">Sem decisões no SQLite. Use /update-decisions-log.</p>`,
    );
  }
  bindEntityCards(root);
}

export async function renderDocs(root, getJson) {
  const { ok, data } = await getJson("/api/docs");
  const docs = ok ? data.docs || [] : [];
  const rows =
    docs
      .map(
        (d) =>
          `<button type="button" class="list-row" data-doc="${escapeHtml(d.path)}">${escapeHtml(d.path)}</button>`,
      )
      .join("") || `<p class="empty-note">Sem markdown em docs/</p>`;
  root.innerHTML = pageWrap("Docs", `${docs.length} arquivo(s)`, `<div class="list-block">${rows}</div>`);
  root.querySelectorAll("[data-doc]").forEach((btn) => {
    btn.addEventListener("click", () => emit({ entity: "doc", id: btn.getAttribute("data-doc") }));
  });
}

export function relatedStoriesHtml(entity, id) {
  const all = state.snapshot?.userStories || [];
  let related = [];
  if (entity === "version") related = all.filter((s) => s.version === id);
  else if (entity === "epic") related = all.filter((s) => s.epic === id);
  else if (entity === "sprint") related = all.filter((s) => s.sprint === id);
  if (!related.length) return "";
  return `<div class="related-block"><h3>User stories</h3>${related
    .map(
      (s) =>
        `<button type="button" class="related-row" data-us="${escapeHtml(s.id)}"><strong>${escapeHtml(s.id)}</strong> — ${escapeHtml(s.title || "")}</button>`,
    )
    .join("")}</div>`;
}

function fieldHtml(label, value) {
  if (!value) return "";
  return `<div class="field"><span class="field-label">${escapeHtml(label)}</span><p class="field-value">${escapeHtml(value)}</p></div>`;
}

export function findDecision(date, index) {
  const day = (state.snapshot?.decisions?.dates || []).find((d) => d.date === date);
  if (!day) return null;
  const entry = (day.entries || [])[index];
  if (!entry) return null;
  return { date, entry };
}

export function renderDecisionDetail(target, date, index) {
  const found = findDecision(date, index);
  if (!found) {
    target.innerHTML = `<p class="empty-note">Decisão não encontrada.</p>`;
    return;
  }
  const { entry } = found;
  const doc = entry.affected_document
    ? `<button type="button" class="related-row" data-doc="${escapeHtml(entry.affected_document)}">${escapeHtml(entry.affected_document)}</button>`
    : "";
  target.innerHTML = `
    <p class="entity-kicker">${escapeHtml(date)} · ${escapeHtml(entry.time || "—")}</p>
    <h1 class="sheet-title">${escapeHtml(entry.title || "(sem título)")}</h1>
    ${fieldHtml("O que mudou", entry.what_changed)}
    ${fieldHtml("Por quê", entry.why_changed)}
    ${fieldHtml("Impacto", entry.impact)}
    ${fieldHtml("Responsável", entry.responsible)}
    ${doc ? `<div class="field"><span class="field-label">Documento</span>${doc}</div>` : ""}
  `;
  target.querySelector("[data-doc]")?.addEventListener("click", () => {
    emit({ entity: "doc", id: entry.affected_document });
  });
}
