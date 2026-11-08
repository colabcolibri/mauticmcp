---
name: us-create
description: Creates a Meridian user story in SQLite after epics and versions exist. Use when adding work to the backlog with concrete acceptance criteria.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Create user story (Meridian)

> Delivery: `.meridian/meridian.db`. **Persist:** `update-us US-XXXX` (stdin heredoc). **Forbidden:** `docs/us/*.md`, drafts, helper `.py`.

## Read first

`writing-guide.md` · `us-template.md` · `show --full` on epic + related US

## Gate

`05_architecture` approved · epic + version in SQLite · user type in `03_user_types.md`

## What to write in each section

**Preamble** — three lines, user language:

- **As** — persona from `03_user_types.md` who cares about this slice.
- **I want** — what they can do in the product after this work (verb + object). Write a sentence, not the backlog title.
- **so that** — the outcome they feel: time saved, risk removed, workflow unblocked.

**### Acceptance** — 2–4 lines, each `[ ]` unchecked. Each line is something you can demo or inspect without reading the code. Split happy path and one edge case when the slice is risky.

**### Why** — 2–4 sentences in order: (1) what is missing or broken today, (2) what this US alone will change, (3) optional constraint or non-goal. Explain the slice; epic id stays in frontmatter only.

**### Where** — 2–4 sentences: version/epic context, which US ids you depend on and what they gave you, which US ids this unblocks, and environment scope (locale, tenant, stack) if it matters.

**### Out of scope** — one short paragraph on what this US explicitly does not do.

**Plan** at create: Architecture refs may cite `05` with § heading; Approach can wait for refine if Why/Where are solid.

If you cannot fill Why and Where from docs + `show --full`, **ask** — do not invent from the title alone.

## Commands

```bash
python3 .agent/scripts/meridian_delivery.py create-us --title "..." --epic EPIC-XX --version vX
python3 .agent/scripts/meridian_delivery.py update-us US-XXXX <<'EOF'
(full body per us-template.md, ready: false)
EOF
```

## Steps

1. Read epic, architecture, sibling US.
2. Draft full markdown using the section guide above.
3. Compare tone to `writing-guide.md` create example.
4. `update-us` with `ready: false`.

## Output

```txt
US created: US-XXXX
Next: /us-refine US-XXXX
```
