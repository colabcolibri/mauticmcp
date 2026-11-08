# Epic close integrity — `/complete-epic`

## Hard blocks (CLI raises)

- Any Must US whose status is not `✅`, `🚫`, or `🧊`
- Epic with **zero** user stories
- Frontmatter `outcome` shorter than a real sentence (observable product signal)

## Confirm before persist

1. `lifecycle-hygiene` / list Must US for the epic.
2. Re-read `## Expected outcome` — still true?
3. Large leftover work → **new epic**, do not reopen `complete`.
4. `update-epic` full markdown, `status: complete`.

## Forbidden

- Closing because hygiene invited the slash while Must US are still ❌
- Completing an epic that never had stories
- Flipping `complete` → `active` for a new capability
