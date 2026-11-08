-- US-0191 — WIP flag for derived Doing column (not a new status emoji)
ALTER TABLE user_stories ADD COLUMN in_progress INTEGER NOT NULL DEFAULT 0;
