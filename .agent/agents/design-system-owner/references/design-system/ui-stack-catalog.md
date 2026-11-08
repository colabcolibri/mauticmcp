# UI stack catalog — index

> Read after `docs/01_tech_stack.md`. Pick **one** row, then read **`stacks/{id}.md`** for the full implementation model.

## How to select

```txt
1. Read docs/01_tech_stack.md § Frontend.
2. Match row below.
3. Record id in 09 § Components → "Primary UI stack".
4. Read references/stacks/{id}.md before bootstrap, showcase, or UI implement-us.
```

| id | When to use | Implementation reference |
| -- | ----------- | ------------------------ |
| `ts-shadcn` | React/Next + shadcn/ui | [stacks/ts-shadcn.md](stacks/ts-shadcn.md) |
| `ts-mui` | React + MUI | [stacks/ts-mui.md](stacks/ts-mui.md) |
| `ts-chakra` | React + Chakra UI | [stacks/ts-chakra.md](stacks/ts-chakra.md) |
| `ts-ant` | React + Ant Design | [stacks/ts-ant.md](stacks/ts-ant.md) |
| `ts-tailwind-headless` | React + Tailwind + Radix/Headless (no shadcn CLI) | [stacks/ts-tailwind-headless.md](stacks/ts-tailwind-headless.md) |
| `py-streamlit` | Python Streamlit | [stacks/py-streamlit.md](stacks/py-streamlit.md) |
| `py-nicegui` | Python NiceGUI | [stacks/py-nicegui.md](stacks/py-nicegui.md) |
| `py-django-htmx` | Django + HTMX + Tailwind | [stacks/py-django-htmx.md](stacks/py-django-htmx.md) |
| `go-templ-htmx` | Go templ + HTMX + Tailwind | [stacks/go-templ-htmx.md](stacks/go-templ-htmx.md) |
| `rust-leptos` | Leptos / Dioxus + CSS/Tailwind | [stacks/rust-leptos.md](stacks/rust-leptos.md) |

### Embedded frontend (Wails, Tauri + Go)

Use frontend stack row (usually `ts-shadcn`). Backend does not own visual tokens.

---

## Quick reference (paths only)

| id | Primitives (read-only) | Composed | Theme entry |
| -- | ---------------------- | -------- | ----------- |
| `ts-shadcn` | `components/ui/*` | `components/app/*` | `globals.css` |
| `ts-mui` | `@mui/material` | `components/app/*` | `theme/theme.ts` |
| `ts-chakra` | `@chakra-ui/react` | `components/app/*` | `theme/index.ts` |
| `ts-ant` | `antd` | `components/app/*` | `ConfigProvider` token |
| `ts-tailwind-headless` | `components/ui/*` | `components/app/*` | `tokens.css` + tailwind |
| `py-streamlit` | `st.*` | `ui/composed/*.py` | `config.toml` + `theme.css` |
| `py-nicegui` | `ui.*` | `ui/composed/*.py` | `ui.colors` + dark_mode |
| `py-django-htmx` | `templates/ui/*` | `templates/composed/*` | `static/css/tokens.css` |
| `go-templ-htmx` | `views/ui/*.templ` | `views/composed/*.templ` | `static/css/tokens.css` |
| `rust-leptos` | `components/ui/*.rs` | `components/app/*.rs` | `style/app.css` |

Full theme (light/dark), showcase routes, and code patterns → **`stacks/{id}.md`**.

---

## Universal rules

1. **Semantic tokens** in `09` — map to stack-native API per stack file.
2. **One theme source** — no hex in feature code.
3. **Composed `App*`** — see `component-composition-pattern.md`.
4. **Showcase US slices** — see `showcase-us-slices.md`.
5. **Mood only** — optional DESIGN.md / awesome-design-md **after** stack is fixed.
