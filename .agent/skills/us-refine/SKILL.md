---
name: us-refine
description: Refines a Meridian user story in SQLite for implementation — deepens Approach, architecture refs and tests. Use between /us-create and coding.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Refine user story (Meridian)

> `show --full` first. `update-us` replaces the whole body. **Never** `set-ready true` — story-checker only.

## Read first

`refine-checklist.md` · `writing-guide.md` (refine example) · target US · `05_architecture.md` + any `docs/architecture/*` cited

## What to deepen

Re-read Intent. If Why or Where are still one line, expand them using the same rules as create (problem → slice outcome → deps/unblocks).

**### Approach** — required. Minimum two bullets. Each bullet is one or two sentences covering:

- what you will change and why that layer,
- which module, route, or test area,
- what existing code you reuse (DRY),
- a constraint from architecture or security.

**### Architecture refs** — path plus exact `§ Heading` from `05` or a detail file under `docs/architecture/`.

**### API / DB impact** — name tables, endpoints, or migrations touched; or `_n/a_` with a short phrase why.

**### Planned** — how a reviewer verifies before merge:

- **manual** — numbered steps and expected result,
- **automated** — exact command and scope when `tests: required`.

Merge edits into the full document from `show --full`; do not send a partial patch.

## Commands

```bash
python3 .agent/scripts/meridian_delivery.py show US-XXXX --full
python3 .agent/scripts/meridian_delivery.py update-us US-XXXX <<'EOF'
(full markdown, ready: false)
EOF
```

## Steps

1. `show --full` + read cited architecture sections.
2. Fill Approach, refs, Planned per above.
3. Check `refine-checklist.md`.
4. `update-us`; `ready: false`.
5. Hand off to `/us-review`.

## Output

```txt
US refined: US-XXXX
Next: /us-review US-XXXX
```
