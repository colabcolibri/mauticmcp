# Template — Record section shape (NOT a full US body)

> ⛔ **This is NOT a user story to copy into `update-us` or `patch-record`.**  
> On `/complete-us`, run `show US-XXXX --full` first, then **add** a filled `## Record` to that existing document.  
> Read **`close-us-contract.md`** before closing.

> **US creation:** placeholders under `## Record` in a new US.  
> **Closure (`✅`):** fill **only** `## Record` (and flip acceptance `[x]`) in the **existing** US from `show --full` — skill `us-complete`.

## Placeholder on creation (status `❌`) — create/refine only

Use when **creating** a US (`/create-us`). **Do not paste this block on `/complete-us`.**

```md
## Record

### Files

_(fill on close)_

### Backend

_(fill on close or _n/a_)_

### Frontend

_(fill on close or _n/a_)_

### Scripts / Docs

_(fill on close or _n/a_)_

### Executed

_(pending until close)_
```

## Record on completion (status `✅`) — example subsection content only

Copy **only** the `### Files` … `### Executed` content into the **existing** `## Record` section of the US from `show --full`. Do not replace Intent or Plan.

```md
## Record

### Files

- `src/features/monitor/VersionFilterBar.tsx` — shared filter bar
- `src/context/MonitorVersionFilterContext.tsx` — version state across tabs
- `src/features/monitor/MonitorDashboard.tsx` — provider wiring

### Backend

- _n/a_

### Frontend

- Shared React context across Delivery and Board tabs.
- Selected version persists when switching tabs.
- Default: `active` version; fallback last version with US in folder.

### Scripts / Docs

- _n/a_

### Executed

- `pnpm build` — passed
- manual — filter persists across tabs
- **suggested commit:** `feat(scope): short summary (US-XXXX)`
- **git commit:** `abc1234` — feat(scope): short summary (US-XXXX) _(add after manager commits; omit until then)_
```

## Rules

| Rule | Detail |
| ----- | ------- |
| Load first | `show US-XXXX --full` — the US body is **that output**, not this file |
| Additive close | Change Record + acceptance + status only — see `close-us-contract.md` |
| Persist | Prefer `patch-record`; else `update-us` with **entire** markdown from `show --full` |
| Paths | Relative to app root or repo; include folder |
| One line per file | What changed in that file |
| Empty layers | `_n/a_` — do not omit heading |
| Plan vs delivery | Do **not** delete Plan/Approach bullets on close; remove only Planned items that were explicitly cancelled |
| Global decisions | `prepend-decision` CLI; local US record stays here |
| Git | US ✅ = docs closed; **commit is human after** `/complete-us` — see `commit-after-us-close.md` |

## Anti-patterns (block `✅`)

- Pasting this template (or `us-template.md`) as the full US body
- `_(fill on close)_` still present in Record
- Only "No functional change" without listing files when there was a change
- Acceptance `[x]` without match in Record or Executed
- Generic list without paths ("monitor components updated")
- Why/Where/Approach shorter after close than before `show --full`
