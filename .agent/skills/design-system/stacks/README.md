# Stack implementation references

> **Read the file for your stack id** after `ui-stack-catalog.md` selection. These are **implementation models** — theme, paths, composed components, showcase, light/dark.

| Stack id | File | Runtime |
| -------- | ---- | ------- |
| `ts-shadcn` | [ts-shadcn.md](ts-shadcn.md) | React + shadcn/ui + Tailwind |
| `ts-mui` | [ts-mui.md](ts-mui.md) | React + Material UI |
| `ts-chakra` | [ts-chakra.md](ts-chakra.md) | React + Chakra UI |
| `ts-ant` | [ts-ant.md](ts-ant.md) | React + Ant Design |
| `ts-tailwind-headless` | [ts-tailwind-headless.md](ts-tailwind-headless.md) | React + Tailwind + Radix/Headless |
| `py-streamlit` | [py-streamlit.md](py-streamlit.md) | Python Streamlit |
| `py-nicegui` | [py-nicegui.md](py-nicegui.md) | Python NiceGUI / Reflex-like |
| `py-django-htmx` | [py-django-htmx.md](py-django-htmx.md) | Django + HTMX + Tailwind |
| `go-templ-htmx` | [go-templ-htmx.md](go-templ-htmx.md) | Go templ + HTMX + Tailwind |
| `rust-leptos` | [rust-leptos.md](rust-leptos.md) | Leptos / Dioxus + CSS |

## Layering

```txt
ui-stack-catalog.md     → pick id (index)
stacks/{id}.md          → how to implement (this folder)
component-composition-pattern.md → App* contract (all stacks)
showcase-us-slices.md   → default US breakdown for /design-showcase
```

## When to read

| Workflow | Read |
| -------- | ---- |
| `/design-pass bootstrap` | `stacks/{id}.md` § Theme + § Paths |
| `/design-showcase` | `stacks/{id}.md` § Showcase + `showcase-us-slices.md` |
| `/implement-us` (UI) | Full `stacks/{id}.md` for touched stack |

## Not included here

- Product-specific brand hex (comes from `00_scope` → `09`)
- Vendored third-party DESIGN.md brands
- Auto-generated code — agents implement per US
