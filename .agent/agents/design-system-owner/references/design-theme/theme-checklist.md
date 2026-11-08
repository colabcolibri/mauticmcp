# Theme checklist

> Use with `/design-theme`. Persist in `09` § Colors and § Theme modes.

## Source of truth

- [ ] **One** token source named (CSS variables file, theme object, native `ColorScheme`, host `--vscode-*`)
- [ ] Feature code consumes **semantic** tokens (`background`, `foreground`, `destructive`) — not raw brand names only
- [ ] Hex/rgb appear in the token file (or host theme), not in feature components — except documented data viz
- [ ] Stack id in `09` matches `01_tech_stack.md`

## Semantic roles (minimum)

| Role | Pass when |
| ---- | --------- |
| canvas / background | Page vs surface vs overlay are distinct **or** explicitly the same |
| foreground | Body text contrast vs canvas documented (AA for body) |
| muted | Secondary text; not the same as disabled |
| border | Dividers; not used as the only focus indicator |
| primary | Main actions; hover/active if the stack has them |
| destructive | Danger; not the same hue as primary |
| focus | Visible ring or equivalent |

Optional but named if used: success, warning, link, overlay/scrim.

## Modes

- [ ] Modes listed: `light` / `dark` / `system` / `host` (IDE) / `high-contrast` — only those that exist
- [ ] Each mode maps to the **same semantic roles** (no “dark mode missing destructive”)
- [ ] `system` / `host` described: who wins (OS vs in-app toggle vs editor theme)
- [ ] Elevation in dark mode is not a leftover light shadow (prefer opacity / lighter surface)

## Integrity (fail if true)

- A screen introduces a one-off palette (“this wizard is blue”)
- Light and dark invert meaning (e.g. destructive becomes primary)
- Contrast for body text obviously fails on the documented pair
- Marketing landing and app shell share no documented relationship (either same tokens or **explicit** second theme with a name)

## Cross-check

- [ ] `design-flow` density (work tool vs marketing) matches token contrast (not pastel-on-pastel for a dense IDE)
- [ ] Status in UI is not color-only (text or icon) — aligns with `09` a11y
