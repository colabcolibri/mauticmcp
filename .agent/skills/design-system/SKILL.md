---
name: design-system
description: Maintains docs/09_design_system.md and stack-aware UI bootstrap — shadcn, MUI, Chakra, Ant Design, Streamlit, NiceGUI, Django HTMX, Go templ, Leptos; composed App* templates over read-only primitives. Use for /design-pass, /design-showcase, /design-review, 09_design_system, tokens, showcase catalog, or UI acceptance criteria.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Design system (Meridian)

> **Escopo:** `docs/09_design_system.md`. US com UI: `meridian_delivery.py show US-XXXX --full`.

> Authoring: `.agent/skills/doc.md` (selective reading + `references/`).

## Operator workflows

| Workflow | Purpose |
| -------- | ------- |
| `/design-pass` | Create/update `09` — stack, components, showcase index |
| `/design-showcase` | Plan catalog routes + showcase US (no code) |
| `/design-review` | Audit live UI vs `09` + showcase (no code) |

Siblings: `design-flow` (`/design-flow`), `design-theme` (`/design-theme`).

## Selective reading

| File | When to read |
| ---- | ------------ |
| `references/design-system-checklist.md` | **Mandatory** — any pass on `09` |
| `references/stack-bootstrap.md` | **Mandatory** — `/design-pass bootstrap` or empty `09` |
| `references/ui-stack-catalog.md` | **Mandatory** — pick stack id |
| `references/stacks/{id}.md` | **Mandatory** — implementation model for chosen stack |
| `references/showcase-us-slices.md` | **Mandatory** — `/design-showcase` US breakdown |
| `references/component-composition-pattern.md` | **Mandatory** — components, showcase, review |
| `references/showcase-catalog-pattern.md` | **Mandatory** — `/design-showcase` |
| `references/design-review-checklist.md` | **Mandatory** — `/design-review` |
| Target US (`show US-XXXX --full`) | `us-align` or `us-scope` modes |

## When to trigger

- `/design-pass`, `/design-showcase`, `/design-review` (flow/theme: those skills)
- Create or deepen `09_design_system.md`
- Before `/refine-us` on Must US with visual Acceptance
- Stack change in `01_tech_stack.md`


## Modes (`$ARGUMENTS`)

| Argument | Mode | Action |
| -------- | ---- | ------ |
| _(empty)_ | **full** | Checklist pass on entire `09` |
| `bootstrap` | **bootstrap** | Read `01_tech_stack.md` → pick stack id → `stack-bootstrap.md` → fill tokens + paths |
| `US-XXXX` | **us-align** | Load US `--full`; map Acceptance UI → `09` sections; suggest Plan refs |

---

## Procedure (design-pass)

```txt
Task progress:
- [ ] Read 00_scope, 01_tech_stack, 04_principles, 05_architecture
- [ ] ui-stack-catalog.md → stacks/{id}.md
- [ ] stack-bootstrap.md + component-composition-pattern.md
- [ ] design-system-checklist.md → update 09
- [ ] US Plan refs / showcase / review follow-ups
```

## Anti-patterns

- Product code (use `/design-showcase` → `/implement-us`)
- Edit installed primitives (`components/ui/*`, etc.)
- Bootstrap brand before stack id
- Approve `09` without human

## Output

```txt
Workflow:
Stack id:
Primitive path:
Composed path:
09 status:
Next:
```

## Workflow steps (from `/design-pass`)

```txt
```txt
CONTEXT:
- User Request: $ARGUMENTS
- Mode: DESIGN PASS

RULES:
1. If no 09_design_system.md → copy § Document stub from `.agent/references/templates/phase-docs/09-design-system.md`
2. Run mode procedure (full | bootstrap | us-align)
3. Walk design-system-checklist.md
4. Recommend /refine-us if Must UI US Plan missing 09 refs
5. Recommend /design-flow when § Screen flows is empty; /design-theme when Colors/Typography are placeholders
6. Recommend /design-showcase when Components or Showcase sections empty
7. prepend-decision on material stack or token changes
```

---
```

## Workflow steps (from `/design-showcase`)

```txt
```txt
CONTEXT:
- User Request: $ARGUMENTS
- Mode: DESIGN SHOWCASE

RULES:
1. Read 09 § Components + § Showcase catalog
2. Propose route map: /design, /design/tokens, /design/components, /design/patterns (adjust to product)
3. List minimum composed templates with all states (see showcase-catalog-pattern.md)
4. create-us per `showcase-us-slices.md` — each US Plan cites `stacks/{id}.md` sections
5. Update 09 § Showcase catalog table with planned routes and US ids
6. Cross-link /design-pass if 09 gaps found
```

---
```

## Workflow steps (from `/design-review`)

```txt
```txt
CONTEXT:
- User Request: $ARGUMENTS
- Mode: DESIGN REVIEW

RULES:
1. Read 09 + component-composition-pattern.md
2. Check: tokens, type roles, composed vs edited primitives, screen-flow row, responsive, a11y baseline
3. Compare showcase routes (if any) to 09 § Showcase catalog
4. Classify gaps: doc fix (/design-pass) | code fix (US) | both
5. Never mark 09 approved — human only
```

---
```
