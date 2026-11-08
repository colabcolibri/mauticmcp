# Implementation model — `py-nicegui`

> Python NiceGUI (Quasar-based). Stack id: **`py-nicegui`**.

## Paths

| Layer | Path | Editable |
| ----- | ---- | -------- |
| Primitives | `ui.button`, `ui.dialog`, etc. | **No** |
| Composed | `ui/composed/*.py` | **Yes** |
| Theme | app startup `ui.colors` | **Yes** |
| Showcase | `pages/design/` modules or routes | **Yes** |

## Bootstrap

```bash
pip install nicegui
```

## Theme — light + dark

**At startup:**

```python
from nicegui import ui

ui.colors(
    primary="#2563eb",
    secondary="#64748b",
    accent="#f59e0b",
    dark="#0f172a",
    positive="#22c55e",
    negative="#ef4444",
)

# Dark mode: Quasar Dark plugin
ui.dark_mode().enable()  # or bind to toggle
```

Bind toggle:

```python
dark = ui.dark_mode()
ui.switch("Dark").bind_value(dark, "value")
```

Document Quasar token names in `09` § Colors.

## Composed templates

```python
# ui/composed/app_dialog.py
def app_dialog(title: str, body_builder, *, on_confirm=None):
    with ui.dialog() as dialog, ui.card():
        ui.label(title).classes("text-h6")
        body_builder()
        with ui.row():
            ui.button("Cancel", on_click=dialog.close)
            if on_confirm:
                ui.button("OK", on_click=on_confirm)
    return dialog
```

| Function | Primitives |
| -------- | ---------- |
| `app_dialog` | `ui.dialog`, `ui.card` |
| `app_form_field` | `ui.input`, `ui.label`, validation message |
| `app_page_header` | `ui.row` + `ui.label` + slot |

## Showcase

- Route `@ui.page('/design')` with subpages or tabs
- `/design/components` — import composed only

## Responsive

- `.classes('w-full max-w-screen-md mx-auto')`
- `ui.row().classes('flex-col md:flex-row')`

## Implement-us checklist

- [ ] `ui.colors` centralized
- [ ] `dark_mode()` wired if scope includes dark
- [ ] Composed modules return reusable builders
