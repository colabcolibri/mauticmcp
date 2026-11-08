# Implementation model — `rust-leptos`

> Leptos or Dioxus + Tailwind/CSS. Stack id: **`rust-leptos`**.

## Paths

| Layer | Path | Editable |
| ----- | ---- | -------- |
| Primitives | `src/components/ui/*.rs` — thin wrappers | **Read-only** after baseline |
| Composed | `src/components/app/*.rs` | **Yes** |
| Styles | `style/app.css` or Tailwind output | **Yes** |
| Showcase | `src/app/design/*.rs` routes | **Yes** |

## Bootstrap (Leptos + Tailwind)

```bash
cargo add leptos leptos_router
# tailwind: npm + build script → include_str!("../style/app.css")
```

## Theme — light + dark

**File:** `style/app.css`

```css
:root {
  --color-bg: #ffffff;
  --color-fg: #0f172a;
  --color-primary: #2563eb;
}
.dark {
  --color-bg: #0f172a;
  --color-fg: #f8fafc;
  --color-primary: #60a5fa;
}
```

**Toggle (Leptos):**

```rust
let (dark, set_dark) = create_signal(false);
view! {
  <html class=move || if dark.get() { "dark" } else { "" }>
  <button on:click=move |_| set_dark.update(|d| !*d)>"Toggle"</button>
}
```

Use Tailwind `dark:` variants with `class="dark"` on ancestor.

## Composed templates

```rust
#[component]
pub fn AppDialog(
    #[prop(into)] title: String,
    children: Children,
    #[prop(optional)] description: Option<String>,
    open: ReadSignal<bool>,
    on_close: Callback<()>,
) -> impl IntoView {
    view! {
        <Show when=move || open.get()>
            <div role="dialog" class="rounded-lg border bg-[var(--color-bg)]">
                <h2>{title}</h2>
                {description.map(|d| view! { <p class="text-muted">{d}</p> })}
                {children()}
            </div>
        </Show>
    }
}
```

Dioxus: same props pattern with `Element` / `rsx!`.

## Showcase routes (Leptos router)

| Route | Component |
| ----- | --------- |
| `/design` | `DesignHome` |
| `/design/tokens` | `DesignTokens` |
| `/design/components` | `DesignComponents` |

## Responsive

- Tailwind `md:` `lg:` classes on containers
- `max-w-full overflow-x-auto` on tables

## Implement-us checklist

- [ ] CSS vars in `app.css` linked from root layout
- [ ] `#[component]` composed in `components/app/`
- [ ] Dark signal + `class="dark"` documented in `09`
