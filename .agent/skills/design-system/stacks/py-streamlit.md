# Implementation model — `py-streamlit`

> Python Streamlit dashboards. Stack id: **`py-streamlit`**.

## Paths

| Layer | Path | Editable |
| ----- | ---- | -------- |
| Primitives | `st.*` widgets | **No** (framework API) |
| Composed | `ui/composed/*.py` — factory functions | **Yes** |
| Theme config | `.streamlit/config.toml` | **Yes** |
| Custom CSS | `assets/theme.css` | **Yes** |
| Showcase | `pages/design_*.py` (multipage) | **Yes** |

## Bootstrap

```toml
# .streamlit/config.toml
[theme]
base = "light"
primaryColor = "#2563eb"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8fafc"
textColor = "#0f172a"
font = "sans serif"
```

Dark: Streamlit theme is **limited** — for full dark custom UI use injected CSS + `st.session_state.theme` toggle.

## Theme — light + dark (custom)

**File:** `assets/theme.css`

```css
:root {
  --primary: #2563eb;
  --bg: #ffffff;
  --fg: #0f172a;
  --muted: #64748b;
}
[data-theme="dark"] {
  --primary: #60a5fa;
  --bg: #0f172a;
  --fg: #f8fafc;
  --muted: #94a3b8;
}
```

**Inject once** in `app.py`:

```python
def inject_theme():
    with open("assets/theme.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
```

Toggle: `st.toggle("Dark mode")` → set `st.session_state["theme"]` → `st.markdown(f'<div data-theme="...">', unsafe_allow_html=True)` wrapper pattern.

## Composed templates

```python
# ui/composed/app_dialog.py
def app_dialog(title: str, body_fn, *, key: str, open: bool):
    if open:
        with st.expander(title, expanded=True):  # or st.dialog() if available
            body_fn()
```

| Function | Role |
| -------- | ---- |
| `app_dialog(...)` | title + body callable + actions |
| `app_form_field(label, key, error=None)` | label + input + error text |
| `app_page_header(title, actions=None)` | columns layout |

## Showcase (multipage)

| Page file | Content |
| --------- | ------- |
| `pages/design_1_overview.py` | Index |
| `pages/design_2_tokens.py` | Color blocks via `st.color_picker` display or HTML swatches |
| `pages/design_3_components.py` | Call composed functions |

## Responsive

- `st.columns([1,2,1])` for layout
- Avoid wide `st.dataframe` without `use_container_width=True`

## Implement-us checklist

- [ ] Theme in `config.toml` + optional CSS vars
- [ ] Composed functions, not 50-line `st.button` blocks in pages
- [ ] No subclassing Streamlit internals
