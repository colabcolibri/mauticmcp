# Showcase catalog pattern

> Plan with `/design-showcase`; implement only via `/implement-us`.

## Minimum route map

| Route | Purpose |
| ----- | ------- |
| `/design` | Index — links to sections, stack id, token source |
| `/design/tokens` | Colors, typography, spacing swatches |
| `/design/components` | All composed templates + states |
| `/design/patterns` | Page layouts (form, list, detail, empty state) |
| `/design/dark` | Dark theme variant (if in scope) |

Adjust base path to product router (`app/design/`, `pages/design/`, extension webview route).

## Minimum composed inventory

Each row in `09` § Components inventory → one anchor on `/design/components`:

| Template | States to demo |
| -------- | -------------- |
| AppButton | variants, sizes, disabled, loading |
| AppDialog | open/closed, with/without description, destructive variant |
| AppSheet | side, sizes |
| AppFormField | default, error, disabled |
| AppInput / AppSelect | focus, error |
| AppCard | default, interactive |
| AppEmptyState | with/without action |
| AppPageHeader | with action slot |
| AppDataTable or AppListRow | if data UI in scope |

## Page rules

1. Import **only** from composed path (`components/app/*`), never demo raw `ui/*` in isolation.
2. Each section shows **all variants** documented in `09`.
3. Responsive: narrow viewport note or toggle (375px minimum).
4. Link back to `09` section in page footer for humans.

## US slicing (typical)

| US | Delivers |
| -- | -------- |
| DS-S1 | Theme tokens wired to stack |
| DS-S2 | `/design` shell + navigation |
| DS-S3 | `/design/components` gallery |
| DS-S4 | Patterns + responsive/dark (if scope) |

Create with `/create-us` under design enabler epic; `ready: false` until `/refine-us`.

## Extension / non-router products

- VS Code webview: dedicated webview route or static HTML catalog in `media/design-catalog.html` linked from docs.
- Streamlit: multi-page `pages/design_*.py` mirroring route names.

Document actual paths in `09` § Showcase catalog.
