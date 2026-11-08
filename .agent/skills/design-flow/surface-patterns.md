# Surface patterns — web, app, extension

> Same **job**, different **chrome**. Do not clone one layout across breakpoints or platforms.

## Pick the pattern per surface

| Surface | Default navigation | Content | Avoid |
| ------- | ------------------ | ------- | ----- |
| **Web app** (desktop-first) | Sidebar or top nav; command palette optional | Multi-column when width allows | Hamburger that hides the only way to switch jobs |
| **Web responsive** | Sidebar → top bar or bottom tabs at the documented breakpoint | Single column; tables wrap or become cards | Horizontal page scroll; tiny tap targets |
| **Native / PWA mobile** | Bottom tabs (3–5) + stack; sheets for secondary | Thumb reach for primary action | Desktop sidebar; hover-only affordances |
| **Tablet** | Optional split (list | detail) | Persist selection | Treating tablet as “big phone” or “small desktop” with no rule |
| **IDE / extension webview** | **Host** chrome (activity bar, tabs); in-view toolbar wraps | Density of a work tool; inherit host theme | Marketing hero; hardcoded light/dark hex |
| **Marketing site** | Top nav, footer | Long scroll, SEO | App dashboard IA |

Document the breakpoint table in `09` § Responsive behavior. This file decides **what changes at each breakpoint**, not only pixel widths.

## Responsive rules (all interactive surfaces)

- Content stays inside the parent — no accidental `overflow-x` on `body` / page canvas
- Primary action remains visible without horizontal pan
- Forms stack labels above fields on narrow widths
- Data tables: card/list alternative **or** an explicit `.table-wrap` with a reason (secondary data, not the only way to complete the job)
- Touch: hit area ≥44×44px on phone; ≥28px height on dense IDE toolbars (stated in `09`)

## Cross-surface integrity

- Same job uses the **same words** (board, epic, sprint) on every surface
- State that exists on two surfaces has one source of truth in `05` (do not design conflicting filters)
- If a job is **out of scope** on a surface, say so in the flow table — do not leave a disabled clone

## When the product is one surface only

Still fill § Screen flows. Skip rows that do not apply; do not copy native tab-bar rules into a CLI.
