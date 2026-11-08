# Phase doc template — `09_design_system.md` (UI only)

**Agent:** `design-system-owner`  
**Product path:** `docs/09_design_system.md`  
**Skip:** headless / CLI-only products  
**Deepen:** `/design-pass bootstrap` → `/design-showcase` → `/design-review`

---

## What this document is for

`09_design_system` is the **visual and UX contract**: screen flows, theme modes, type ramp, tokens, components, responsive rules, accessibility baseline, showcase catalog. UI Must US cite this in Plan after `approved`. Product code uses composed templates — not edited vendor primitives.

## When to write and revisit

| Moment | Action |
| ------ | ------ |
| Init (UI products) | Stub after `01` indicates UI stack |
| Stack/theme change | `review`; update tokens + paths — `/design-theme` |
| New UI epic | Extend screen flows + component inventory + showcase rows — `/design-flow` |
| Before closing UI US | `/design-review` against this doc |

## How to complete each section

Follow stub order. Pick **stack id** from `ui-stack-catalog.md` in Overview. Document **primitive path** (read-only) and **composed path** (`App*` templates). Fill token tables with semantic names + theme keys, not only hex. Fill **Theme modes** and a type **ramp** (one size per role). Fill **Screen flows** (jobs, states, mermaid). Breakpoints must include what changes at each width and no horizontal overflow. Showcase catalog lists routes or planned US for catalog.

## Depth checklist

- [ ] Stack id recorded
- [ ] Primitive vs composed paths explicit
- [ ] Screen flows filled (`/design-flow`)
- [ ] Theme modes + type ramp filled (`/design-theme`)
- [ ] Component inventory lists composed templates
- [ ] a11y baseline filled
- [ ] `design-system-checklist.md` satisfied before `approved`


## Mid-project review (doc drift)

Phase docs are **living contracts**. Re-open this file when:

- Stack, auth, or deployment changes materially
- A US or epic introduces a new surface not covered here
- `/audit-docs` or validator flags gaps
- Before marking a new epic `active` if it touches this domain

**Procedure:** set `status: review` → edit sections → run cross-doc checks below → log via `/update-decisions-log` → human sets `approved` again. Never edit `approved` docs silently.

## Cross-doc checks

- UI stack matches `01`
- Layers in `05` include frontend module paths
- US Plan refs cite `09` sections when `approved`

## Related

- `design-system`, `design-flow`, `design-theme` skills; `/design-pass`, `/design-flow`, `/design-theme`, `/design-review`
---

## Document stub

> **Copy to product `docs/`:** from the opening `---` frontmatter below through the end of this section. Replace every `_(…)_` and empty table cell with real content. Do not copy this heading or the blockquote.

---
title: Design System
status: draft
version: 1.0
updated: YYYY-MM-DD
depends_on: [01_tech_stack.md, 04_principles.md, 05_architecture.md]
blocks: []
---

# 09 — Design system

## Overview

_UI product — fill via `/design-pass bootstrap` after `01_tech_stack.md` is drafted._

- **Surfaces:** _(web app | extension webviews | mobile — from scope)_
- **Primary UI stack:** _(id from `ui-stack-catalog.md`, e.g. `ts-shadcn`)_
- **Mood:** _(link `04_principles.md` — work tool vs marketing)_

## Colors

_Semantic tokens — document theme file path, not only hex._

| Token | Role | Theme key / CSS var |
| ----- | ---- | ------------------- |
| primary | Main actions | |
| background | Page canvas | |
| foreground | Body text | |
| muted | Secondary text | |
| destructive | Danger actions | |
| border | Dividers | |

## Theme modes

| Mode | When it applies | Token set / file |
| ---- | --------------- | ---------------- |
| _(host / light / dark / system)_ | | |

_Same semantic roles in every mode. `/design-theme`._

## Typography

| Role | Use | Size / weight / line-height | Stack key |
| ---- | --- | --------------------------- | --------- |
| h1 | Screen title (one per view) | | |
| h2 | Section | | |
| body | Default copy | | |
| label | Fields, chips | | |
| caption | Meta, ids | | |
| code | Mono | | |

_One size per role. Do not skip heading levels. `/design-theme`._

## Layout

- **Spacing scale:** _(e.g. 4px base / Tailwind default)_
- **Container max-width:** _
- **Grid:** _

## Elevation and depth

_(shadows or tonal layers — stack-specific)_

## Shapes

- **Border radius:** _(sm / md / lg tokens)_

## Components

- **Primitives (read-only):** _(e.g. `components/ui/` — never edit for product)_
- **Composed templates:** _(e.g. `components/app/` — `AppDialog`, …)_
- **Composition:** config-driven props (`title`, `description`, `body`, `footer`, `variant`, `size`)

### Inventory (composed)

| Template | Purpose | Showcase route |
| -------- | ------- | -------------- |
| AppDialog | Modal flows | `/design/components#dialog` |
| _add rows via `/design-showcase`_ | | |

## Do's and don'ts

- Do use semantic tokens and composed `App*` templates.
- Do cite this doc in UI US Plan Architecture refs.
- Don't edit installed primitive files (shadcn `ui/*`, MUI package, etc.).
- Don't hardcode hex in feature code.

## Responsive behavior

| Breakpoint | Width | Notes |
| ---------- | ----- | ----- |
| mobile | | |
| tablet | | |
| desktop | | |

Content areas must not cause horizontal overflow (`overflow-x`). At each breakpoint, document **what changes** (stack, sheet, hide nav) — `/design-flow` + `surface-patterns.md`.

## Screen flows

_Jobs → screens → states. `/design-flow`. Skip for CLI-only._

| Flow | Surfaces | Entry | Empty | Error | Exit |
| ---- | -------- | ----- | ----- | ----- | ---- |
| | | | | | |

```mermaid
flowchart LR
  A[Entry] --> B[Primary screen]
  B --> C[Success]
```

## Accessibility baseline

- Focus visible on interactive elements
- Contrast: WCAG AA minimum for text
- Touch targets: 44×44px minimum on mobile
- Form fields: visible labels and error text

## Showcase catalog

| Route | Contents | Status |
| ----- | -------- | ------ |
| `/design` | Overview + nav | planned |
| `/design/tokens` | Colors, type, spacing | planned |
| `/design/components` | Composed templates + states | planned |

_Plan routes via `/design-showcase`; implement via gated `/implement-us`._

## Gate

Human sets `status: approved` before Must US with visual Acceptance ship.

