# Version template (release)

> **Writing quality:** read `.agent/references/templates/writing-guide.md`. Objective and Done criteria are **paragraphs** explaining the release theme.

```md
---
id: vX
title: Short release name
status: planned
outcome: "When this release is delivered at product level."
---

# vX — Short release name

## Objective

**Paragraph.** What changes for the user/manager in this release — theme, main capabilities, how it differs from the previous version. Not a bullet list of tickets.

## Done criteria

**Paragraph.** Observable condition to mark version `complete` — who validates, what they can do, what must be true in docs/product.

## Included in this version

Reference epics/US by id with **one line each** explaining why they belong (not copy-paste from epic body).

- EPIC-XX — …
- US-YYYY — … (when already known)

## Explicitly out

Bullets with short rationale — what waits for a later version and why.

- …

## Go-live checklist

### Product

- [ ] …

## Sprints

- `vX-S1` — theme of sprint in a phrase (row in SQLite `sprints`)
```

## Status

| Value | Meaning |
| ----- | ----------- |
| `planned` | Defined, not yet delivered |
| `active` | Release in progress |
| `complete` | Outcome reached |

## Relationship with US and epics

- US uses `version: vX` in frontmatter.
- Epic uses `versions: [vX]`.
- Release narrative lives **only** in this file.
