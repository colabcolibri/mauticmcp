-- US-0115: summary column for progressive disclosure (agents read summary before full body)

ALTER TABLE user_stories ADD COLUMN summary TEXT;
ALTER TABLE epics ADD COLUMN summary TEXT;
ALTER TABLE versions ADD COLUMN summary TEXT;
ALTER TABLE sprints ADD COLUMN summary TEXT;
