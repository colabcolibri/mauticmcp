---
name: ux-research
description: User research, personas, jobs-to-be-done, and journey inputs for 03_user_types and discovery. Use for /ux-pass. Not design tokens (/design-theme) or screen IA (/design-flow).
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# UX research (Meridian)

> **Scope:** `docs/03_user_types.md`, `docs/discovery/`, journey inputs for `design-system-owner`. Not `09` tokens or component code.

## Operator workflows

| Workflow | Purpose |
| -------- | ------- |
| `/ux-pass` | Personas, JTBD, research notes, journey hypotheses — full, `bootstrap`, or `US-XXXX` |

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/ux-research-checklist.md` | **Mandatory** — any `/ux-pass` |
| `docs/00_scope.md` | Always |
| `docs/discovery/product-brief.md` | When present |
| `docs/inventory/as-is.md` | Brownfield |
| Target US (`show US-XXXX --full`) | `us-align` mode |


## Modes (`$ARGUMENTS`)

| Argument | Mode | Action |
| -------- | ---- | ------ |
| _(empty)_ | **full** | Checklist on `03` + discovery notes |
| `bootstrap` | **bootstrap** | From `00_scope` + brief → draft personas skeleton |
| `US-XXXX` | **us-align** | Load US `--full`; map Acceptance user-facing criteria → persona/journey gaps |

---

## Procedure

```txt
- [ ] Read 00_scope + discovery brief
- [ ] ux-research-checklist.md
- [ ] Update 03_user_types (personas, goals, pains, out-of-scope users)
- [ ] Note journey hypotheses for /design-flow (do not replace design-system-owner)
- [ ] prepend-decision on material persona or compliance-facing user data changes
```

## Output

```txt
Mode: full | bootstrap | us-align
03_user_types status:
Personas updated:
Journey hypotheses for design-flow:
US follow-ups:
Next: /design-flow | /design-pass | human approve 03 | /refine-us US-XXXX
```
