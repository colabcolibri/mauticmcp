import { persistFilters, SPRINT_NONE, state } from "./state.js";
import { compactStoryNarrative } from "./story-narrative.js";

export function sprintKey(story) {
  return story.sprint || SPRINT_NONE;
}

export function sprintIdsInScope(stories) {
  const ids = new Set((stories || []).map(sprintKey));
  return [...ids].sort((a, b) => {
    if (a === SPRINT_NONE) return 1;
    if (b === SPRINT_NONE) return -1;
    return a.localeCompare(b, undefined, { numeric: true });
  });
}

function adoptSet(current, nextIds, known) {
  const next = new Set();
  if (!current) {
    for (const id of nextIds) next.add(id);
    return next;
  }
  for (const id of nextIds) {
    if (current.has(id) || !known.has(id)) next.add(id);
  }
  return next;
}

export function syncFiltersToSnapshot() {
  const snap = state.snapshot;
  if (!snap) return;
  const versionIds = (snap.versions || []).map((v) => v.id);
  const epicIds = (snap.epics || []).map((e) => e.id);
  const sprintIds = sprintIdsInScope(snap.userStories || []);
  state.selectedVersions = adoptSet(state.selectedVersions, versionIds, state.knownVersions);
  state.selectedEpics = adoptSet(state.selectedEpics, epicIds, state.knownEpics);
  state.selectedSprints = adoptSet(state.selectedSprints, sprintIds, state.knownSprints);
  state.knownVersions = new Set(versionIds);
  state.knownEpics = new Set(epicIds);
  state.knownSprints = new Set(sprintIds);
  persistFilters();
}

export function resetFilters() {
  const snap = state.snapshot || {};
  state.selectedVersions = new Set((snap.versions || []).map((v) => v.id));
  state.selectedEpics = new Set((snap.epics || []).map((e) => e.id));
  state.selectedSprints = new Set(sprintIdsInScope(snap.userStories || []));
  persistFilters();
}

export function filteredStories() {
  const all = state.snapshot?.userStories || [];
  const versions = state.selectedVersions;
  const epics = state.selectedEpics;
  const sprints = state.selectedSprints;
  if (!versions || !epics || !sprints) return all;
  if (versions.size === 0 || epics.size === 0 || sprints.size === 0) return [];
  return all.filter((s) => versions.has(s.version) && epics.has(s.epic) && sprints.has(sprintKey(s)));
}

export function narrativeCount(stories = filteredStories()) {
  return stories.filter((s) => compactStoryNarrative(s.preamble)).length;
}

function toggleLabel(on, noun, count) {
  const base = on ? `Ocultar ${noun}` : `Mostrar ${noun}`;
  return count > 0 ? `${base} (${count})` : base;
}

export function filterSummaryText() {
  const snap = state.snapshot;
  if (!snap) return "";
  const vAll = (snap.versions || []).length;
  const eAll = (snap.epics || []).length;
  const sAll = sprintIdsInScope(snap.userStories || []).length;
  const v = state.selectedVersions?.size ?? vAll;
  const e = state.selectedEpics?.size ?? eAll;
  const s = state.selectedSprints?.size ?? sAll;
  const parts = [];
  if (vAll && v !== vAll) parts.push(`${v}/${vAll} versões`);
  if (sAll && s !== sAll) parts.push(`${s}/${sAll} sprints`);
  if (eAll && e !== eAll) parts.push(`${e}/${eAll} épicos`);
  return parts.length ? parts.join(" · ") : "Tudo visível";
}

function renderChecks(root, items, selected, onToggle) {
  root.innerHTML = "";
  for (const item of items) {
    const label = document.createElement("label");
    label.className = "filter-check";
    const input = document.createElement("input");
    input.type = "checkbox";
    input.checked = selected.has(item.id);
    input.setAttribute("aria-label", item.title || item.label);
    const span = document.createElement("span");
    span.textContent = item.label;
    span.title = item.title || item.label;
    input.addEventListener("change", () => onToggle(item.id, input.checked));
    label.append(input, span);
    root.appendChild(label);
  }
}

function wireAllNone(allBtn, noneBtn, allOn, noneOn, onAll, onNone) {
  allBtn.className = "chip" + (allOn ? " on" : "");
  noneBtn.className = "chip" + (noneOn ? " on" : "");
  allBtn.onclick = onAll;
  noneBtn.onclick = onNone;
}

export function renderFilterColumns(onChange) {
  const snap = state.snapshot || {};
  const versions = (snap.versions || []).map((v) => ({
    id: v.id,
    label: v.id,
    title: `${v.id} — ${v.title || ""}`,
  }));
  const epics = (snap.epics || []).map((e) => ({
    id: e.id,
    label: e.id,
    title: `${e.id} — ${e.title || ""}`,
  }));
  const sprints = sprintIdsInScope(snap.userStories || []).map((id) => ({
    id,
    label: id === SPRINT_NONE ? "Sem sprint" : id,
    title: id === SPRINT_NONE ? "US sem sprint atribuído" : id,
  }));

  const vSel = state.selectedVersions || new Set();
  const eSel = state.selectedEpics || new Set();
  const sSel = state.selectedSprints || new Set();

  wireAllNone(
    document.getElementById("version-all"),
    document.getElementById("version-none"),
    versions.length > 0 && versions.every((v) => vSel.has(v.id)),
    vSel.size === 0,
    () => {
      state.selectedVersions = new Set(versions.map((v) => v.id));
      persistFilters();
      onChange();
    },
    () => {
      state.selectedVersions = new Set();
      persistFilters();
      onChange();
    },
  );
  wireAllNone(
    document.getElementById("sprint-all"),
    document.getElementById("sprint-none"),
    sprints.length > 0 && sprints.every((s) => sSel.has(s.id)),
    sSel.size === 0,
    () => {
      state.selectedSprints = new Set(sprints.map((s) => s.id));
      persistFilters();
      onChange();
    },
    () => {
      state.selectedSprints = new Set();
      persistFilters();
      onChange();
    },
  );
  wireAllNone(
    document.getElementById("epic-all"),
    document.getElementById("epic-none"),
    epics.length > 0 && epics.every((e) => eSel.has(e.id)),
    eSel.size === 0,
    () => {
      state.selectedEpics = new Set(epics.map((e) => e.id));
      persistFilters();
      onChange();
    },
    () => {
      state.selectedEpics = new Set();
      persistFilters();
      onChange();
    },
  );

  renderChecks(document.getElementById("version-list"), versions, vSel, (id, on) => {
    if (on) state.selectedVersions.add(id);
    else state.selectedVersions.delete(id);
    persistFilters();
    onChange();
  });
  renderChecks(document.getElementById("sprint-list"), sprints, sSel, (id, on) => {
    if (on) state.selectedSprints.add(id);
    else state.selectedSprints.delete(id);
    persistFilters();
    onChange();
  });
  renderChecks(document.getElementById("epic-list"), epics, eSel, (id, on) => {
    if (on) state.selectedEpics.add(id);
    else state.selectedEpics.delete(id);
    persistFilters();
    onChange();
  });
}

export function updateFilterChrome() {
  const summary = document.getElementById("filter-summary");
  if (summary) summary.textContent = filterSummaryText();
  const frozen = document.getElementById("toggle-frozen");
  const deprecated = document.getElementById("toggle-deprecated");
  const narrative = document.getElementById("toggle-narrative");
  const scoped = filteredStories();
  frozen?.classList.toggle("on", state.showFrozen);
  frozen?.setAttribute("aria-pressed", state.showFrozen ? "true" : "false");
  deprecated?.classList.toggle("on", state.showDeprecated);
  deprecated?.setAttribute("aria-pressed", state.showDeprecated ? "true" : "false");
  const narrativeN = narrativeCount(scoped);
  narrative?.classList.toggle("on", state.showNarrative);
  narrative?.classList.toggle("muted", narrativeN === 0);
  narrative?.setAttribute("aria-pressed", state.showNarrative ? "true" : "false");
  if (narrative) narrative.textContent = toggleLabel(state.showNarrative, "narrativa", narrativeN);
}
