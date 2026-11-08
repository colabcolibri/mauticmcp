-- US-centric sprint assignment (sprint_id on user_stories; sprint_stories remains derived cache)
-- Data repair + unique story_id: reconcile_sprint_links() in meridian_db.bootstrap()

PRAGMA foreign_keys = ON;

ALTER TABLE user_stories ADD COLUMN sprint_id TEXT REFERENCES sprints(id) ON DELETE SET NULL;
ALTER TABLE user_stories ADD COLUMN sprint_position INTEGER;

CREATE INDEX IF NOT EXISTS idx_user_stories_sprint ON user_stories(sprint_id);
