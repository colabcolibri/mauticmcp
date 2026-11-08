# Full epic template

> **Writing quality:** read `.agent/references/templates/writing-guide.md`. Capability and Expected outcome are **prose paragraphs**, not feature lists.

```md
---
id: EPIC-XX
title: Short capability name
status: active
versions: [v1]
profiles: [Profile documented in 03_user_types.md]
outcome: "One sentence: epic done at product level."
---

# EPIC-XX — Short capability name

## Capability

**Minimum two short paragraphs.**

Paragraph 1 — user problem today (who suffers, in what workflow, what friction exists).

Paragraph 2 — what the product offers after this epic: behavior in user language. Mention main surfaces (app, extension) only when needed for clarity — not as a folder tree.

## Expected outcome

**One paragraph.** How the manager or user recognizes the epic is done — observable signal, not “all US ✅” alone (though that may be part of it).

## Out of scope for this epic

Bullets OK — each line explains what belongs elsewhere and **why** (another epic, later version, or US-level detail).

- …

## Notes

Optional: decisions, risks, links — explanatory when present.
```

## Writing rules

| Section | Do | Don't |
| ------- | -- | ----- |
| Capability | User problem → product behavior | List `src/` modules or US ids |
| Expected outcome | Observable “done” for manager/user | Copy frontmatter `outcome` word-for-word |
| Out of scope | Boundaries with rationale | Empty “see US” stubs |

## Epic status

| Value | Meaning |
| ----- | ----------- |
| `active` | Capability in delivery; US can be created |
| `complete` | Outcome reached; only closure or bugfix US |
| `paused` | Deliberately frozen |

## Reopening vs new epic

Prefer **creating a new epic** (e.g. `EPIC-12 — Auth advanced`) with a note referencing the closed epic — do not flip `complete` → `active` for large new scope. Small follow-ups (1–2 US) may attach to a related `active` epic. See `.agent/references/scrum/scrum-meridian-map.md`.

## Relationship with user stories

- Epic = **what** and **why** at product level.
- US = **executable slice** — explains itself via Why / Where / Approach; references `epic: EPIC-XX` only in frontmatter.
- New US → `/create-us` after `05_architecture` approved.

## After creating

1. `python3 .agent/scripts/validate_meridian.py <project-root>`
2. Plan US slices — each US should be a coherent story, not a task label.
