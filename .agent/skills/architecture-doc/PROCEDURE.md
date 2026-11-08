---
name: architecture-doc
description: Create or review docs/05_architecture.md and detail files. Use with @technical-architect or /architecture.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Architecture document pass

> Owner station: `technical-architect`. Consult `security-champion` for auth/data boundaries — do not run as owner.

## Modes (`$ARGUMENTS`)

| Argument | Mode | Action |
| -------- | ---- | ------ |
| _(empty)_ | **full** | Standard architecture pass on `05` + detail files + diagrams |
| `mcp` | **mcp** | Agent tools / MCP contract — @technical-architect + `mcp-checklist.md` |

## Procedure

```txt
CONTEXT:
- User Request: $ARGUMENTS
- Mode: ARCHITECTURE DOC

RULES:
1. technical-architect Phase 0 gate
2. Read 00, 01, 02, 03, 04 before editing 05
3. Cross-check 06/07/08 if they exist — no contradictions
4. Keep 05 as overview + index; move deep specs to docs/architecture/*.md when warranted
5. Diagrams (skill generate-architecture-diagram):
   - Phase 0: glob docs/architecture/diagrams/*.{md,mmd} vs 05 § Architecture diagrams
   - Create/update runtime, database ER (from 06), integrations, flows — one file per view
   - Reconcile index: every on-disk file has a row; remove stale rows
   - Multi-file projects: refresh only files in scope of $ARGUMENTS, or all if "diagrams" / "visual" / "maps"
6. Maintain ## Architecture detail files table when architecture/*.md used
7. Set status draft or review — not approved without human
```

## Output

```txt
05_architecture status:
Detail files (if any):
Architecture diagrams:
Ready for review: yes | no
```
