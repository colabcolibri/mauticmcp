# Implementation model — `py-django-htmx`

> Django templates + HTMX + Tailwind. Stack id: **`py-django-htmx`**.

## Paths

| Layer | Path | Editable |
| ----- | ---- | -------- |
| Primitives | `templates/ui/*.html` — base partials | **Read-only** after first version |
| Composed | `templates/composed/*.html` | **Yes** |
| Tokens | `static/css/tokens.css` | **Yes** |
| Tailwind build | `static/css/app.css` | **Yes** |
| Showcase | `templates/design/*.html` + views | **Yes** |

## Bootstrap

```bash
pip install django django-htmx
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init
```

## Theme — light + dark

**File:** `static/css/tokens.css`

```css
:root {
  --color-bg: #ffffff;
  --color-fg: #0f172a;
  --color-primary: #2563eb;
  --color-muted: #64748b;
  --radius-md: 0.375rem;
}
html.dark {
  --color-bg: #0f172a;
  --color-fg: #f8fafc;
  --color-primary: #60a5fa;
}
```

**Base template:**

```html
<html class="{% if request.COOKIES.theme == 'dark' %}dark{% endif %}">
<link rel="stylesheet" href="{% static 'css/tokens.css' %}">
<link rel="stylesheet" href="{% static 'css/app.css' %}">
```

**Toggle:** HTMX `hx-post="/toggle-theme/"` sets cookie + `hx-swap="none"`.

**Tailwind:** `darkMode: 'class'` in `tailwind.config.js`; utilities `bg-[var(--color-bg)]` or map in `@layer`.

## Composed templates

```django
{# templates/composed/app_dialog.html #}
<dialog id="{{ id }}" class="rounded-lg shadow-lg p-0 ...">
  <header class="px-4 py-3 border-b"><h2>{{ title }}</h2></header>
  <div class="p-4">{% block body %}{{ body }}{% endblock %}</div>
  {% if footer %}<footer class="px-4 py-3 border-t">{{ footer }}</footer>{% endif %}
</dialog>
```

Include via `{% include "composed/app_dialog.html" with title=... body=... %}`.

## Showcase

| URL | View | Template |
| --- | ---- | -------- |
| `/design/` | `design_index` | `design/index.html` |
| `/design/tokens/` | `design_tokens` | swatches |
| `/design/components/` | `design_components` | all composed |

## HTMX patterns

- Dialog partial: `hx-get="/dialog/delete/"` → returns composed fragment
- `hx-target="#modal-root"`

## Implement-us checklist

- [ ] Tokens in one CSS file
- [ ] `templates/ui/` frozen; product in `composed/`
- [ ] Dark via `class` on `html`
