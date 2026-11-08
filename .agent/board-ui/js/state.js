export const SPRINT_NONE = "__none__";

const STORAGE_KEY = "meridian-html-board-filters";

export const state = {
  view: "board",
  snapshot: null,
  selected: null,
  selectedVersions: null,
  selectedEpics: null,
  selectedSprints: null,
  showFrozen: false,
  showDeprecated: false,
  showNarrative: false,
  mobileColumn: "backlog",
  live: "off",
  knownVersions: new Set(),
  knownEpics: new Set(),
  knownSprints: new Set(),
};

export function loadPersistedFilters() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    const data = JSON.parse(raw);
    if (Array.isArray(data.versions)) state.selectedVersions = new Set(data.versions);
    if (Array.isArray(data.epics)) state.selectedEpics = new Set(data.epics);
    if (Array.isArray(data.sprints)) state.selectedSprints = new Set(data.sprints);
    state.showFrozen = !!data.showFrozen;
    state.showDeprecated = !!data.showDeprecated;
    state.showNarrative = !!data.showNarrative;
  } catch {
    /* ignore */
  }
}

export function persistFilters() {
  try {
    sessionStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        versions: [...(state.selectedVersions || [])],
        epics: [...(state.selectedEpics || [])],
        sprints: [...(state.selectedSprints || [])],
        showFrozen: state.showFrozen,
        showDeprecated: state.showDeprecated,
        showNarrative: state.showNarrative,
      }),
    );
  } catch {
    /* ignore */
  }
}

export function replaceSnapshot(snap) {
  state.snapshot = snap;
}

export function setView(view) {
  state.view = view;
}

export function setSelected(sel) {
  state.selected = sel;
}
