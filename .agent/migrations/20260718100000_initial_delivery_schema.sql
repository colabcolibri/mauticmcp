-- Meridian 2.0 — initial delivery artifacts schema (US-0105)
-- Applied by meridian_db.apply_migrations()

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_migrations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  applied_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS versions (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  outcome TEXT,
  objective TEXT,
  done_criteria TEXT,
  included TEXT,
  explicitly_out TEXT,
  go_live TEXT,
  body_markdown TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS epics (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  outcome TEXT,
  profiles TEXT,
  versions TEXT,
  capability TEXT,
  expected_outcome TEXT,
  out_of_scope TEXT,
  notes TEXT,
  body_markdown TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS sprints (
  id TEXT PRIMARY KEY,
  version_id TEXT NOT NULL REFERENCES versions(id),
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  goal TEXT,
  done_when TEXT,
  stories_json TEXT,
  goal_body TEXT,
  scope_table TEXT,
  out_of_scope TEXT,
  retrospective TEXT,
  body_markdown TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS user_stories (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  epic_id TEXT NOT NULL REFERENCES epics(id),
  version_id TEXT NOT NULL REFERENCES versions(id),
  status TEXT NOT NULL,
  moscow TEXT NOT NULL,
  depends_on_json TEXT NOT NULL DEFAULT '[]',
  ready INTEGER NOT NULL DEFAULT 0,
  done_when TEXT NOT NULL,
  tests TEXT NOT NULL DEFAULT 'required',
  tests_status TEXT NOT NULL DEFAULT 'pending',
  preamble TEXT,
  intent_acceptance TEXT,
  intent_why TEXT,
  intent_where TEXT,
  plan_approach TEXT,
  plan_architecture_refs TEXT,
  plan_api_db TEXT,
  plan_security TEXT,
  plan_decisions TEXT,
  plan_planned TEXT,
  record_files TEXT,
  record_backend TEXT,
  record_frontend TEXT,
  record_scripts TEXT,
  record_executed TEXT,
  boundaries_out_of_scope TEXT,
  boundaries_notes TEXT,
  body_markdown TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS sprint_stories (
  sprint_id TEXT NOT NULL REFERENCES sprints(id) ON DELETE CASCADE,
  story_id TEXT NOT NULL REFERENCES user_stories(id) ON DELETE CASCADE,
  position INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (sprint_id, story_id)
);

CREATE TABLE IF NOT EXISTS decisions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  decision_date TEXT NOT NULL,
  entry_index INTEGER NOT NULL,
  title TEXT,
  payload_json TEXT NOT NULL,
  UNIQUE (decision_date, entry_index)
);

CREATE TABLE IF NOT EXISTS board_snapshots (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  source TEXT NOT NULL,
  card_count INTEGER NOT NULL DEFAULT 0,
  payload_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_user_stories_epic ON user_stories(epic_id);
CREATE INDEX IF NOT EXISTS idx_user_stories_version ON user_stories(version_id);
CREATE INDEX IF NOT EXISTS idx_sprints_version ON sprints(version_id);
CREATE INDEX IF NOT EXISTS idx_decisions_date ON decisions(decision_date);
