-- Meridian 2.0 — story_dependencies junction (US→US FK graph)
-- Applied by meridian_db.apply_migrations()

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS story_dependencies (
  story_id TEXT NOT NULL REFERENCES user_stories(id) ON DELETE CASCADE,
  depends_on_id TEXT NOT NULL REFERENCES user_stories(id) ON DELETE CASCADE,
  position INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (story_id, depends_on_id),
  CHECK (story_id != depends_on_id)
);

CREATE INDEX IF NOT EXISTS idx_story_dependencies_depends ON story_dependencies(depends_on_id);

-- Backfill from depends_on_json (skip unknown ids — validator will catch on next upsert)
INSERT OR IGNORE INTO story_dependencies (story_id, depends_on_id, position)
SELECT us.id, dep.value, CAST(dep.key AS INTEGER)
FROM user_stories AS us,
     json_each(
       CASE
         WHEN us.depends_on_json IS NULL OR TRIM(us.depends_on_json) = '' THEN '[]'
         WHEN json_valid(us.depends_on_json) THEN us.depends_on_json
         ELSE '[]'
       END
     ) AS dep
WHERE dep.value IN (SELECT id FROM user_stories)
  AND dep.value != us.id;
