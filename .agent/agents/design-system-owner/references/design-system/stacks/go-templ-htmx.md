# Implementation model — `go-templ-htmx`

> Go + templ + HTMX + Tailwind. Stack id: **`go-templ-htmx`**.

## Paths

| Layer | Path | Editable |
| ----- | ---- | -------- |
| Primitives | `views/ui/*.templ` | **Read-only** after baseline |
| Composed | `views/composed/*.templ` | **Yes** |
| Tokens | `static/css/tokens.css` | **Yes** |
| CSS build | `static/css/app.css` (Tailwind output) | **Yes** |
| Showcase | `views/design/*.templ` + handlers | **Yes** |

## Bootstrap

```bash
go install github.com/a-h/templ/cmd/templ@latest
npm install -D tailwindcss
```

## Theme — light + dark

**File:** `static/css/tokens.css` — same CSS vars pattern as Django stack.

**Layout templ:**

```templ
templ BaseLayout(dark bool) {
  <html class={ templ.KV("dark", dark) }>
    <head><link rel="stylesheet" href="/static/css/tokens.css"/></head>
    <body>{ children... }</body>
  </html>
}
```

Toggle: handler sets cookie `theme=dark`, re-render layout.

## Composed templates

```templ
// views/composed/app_dialog.templ
type AppDialogProps struct {
  Title string
  Body templ.Component
  Footer templ.Component
  Open bool
}

templ AppDialog(p AppDialogProps) {
  <dialog open={ p.Open } class="rounded-lg ...">
    <h2>{ p.Title }</h2>
    @p.Body
    if p.Footer != nil {
      <footer>@p.Footer</footer>
    }
  </dialog>
}
```

Run `templ generate` after edits.

## Showcase routes

| Path | Handler |
| ---- | ------- |
| `/design` | `DesignIndex` |
| `/design/tokens` | swatch templ |
| `/design/components` | composed demos |

## HTMX

- `hx-get="/design/components/dialog-demo"` returns composed fragment
- Partial swaps into `#catalog-root`

## Implement-us checklist

- [ ] `templ generate` in CI/build
- [ ] Tokens.css single source
- [ ] Composed props structs match composition pattern
