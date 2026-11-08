# Implementation model — `ts-tailwind-headless`

> React + Tailwind + Radix UI / Headless UI (no shadcn CLI). Stack id: **`ts-tailwind-headless`**.

## Paths

| Layer | Path | Editable |
| ----- | ---- | -------- |
| Primitives | `src/components/ui/*` — **copied once** from Radix/Headless docs | **Rarely** — treat as read-only after first commit |
| Composed | `src/components/app/*` | **Yes** |
| Theme | `src/styles/tokens.css` + `tailwind.config.ts` | **Yes** |
| Showcase | `src/app/design/**` | **Yes** |

## Bootstrap

```bash
npm install tailwindcss @radix-ui/react-dialog @radix-ui/react-slot class-variance-authority clsx tailwind-merge
```

Copy Radix dialog/button patterns into `components/ui/` **once** — then freeze.

## Theme — light + dark

**File:** `src/styles/tokens.css`

```css
:root {
  --color-bg: 255 255 255;
  --color-fg: 15 23 42;
  --color-primary: 37 99 235;
  --color-muted: 100 116 139;
  --color-destructive: 220 38 38;
  --radius-md: 0.375rem;
}
.dark {
  --color-bg: 15 23 42;
  --color-fg: 248 250 252;
  --color-primary: 96 165 250;
}
```

**tailwind.config.ts:**

```ts
theme: {
  extend: {
    colors: {
      background: "rgb(var(--color-bg) / <alpha-value>)",
      foreground: "rgb(var(--color-fg) / <alpha-value>)",
      primary: "rgb(var(--color-primary) / <alpha-value>)",
    },
  },
},
```

**Dark:** `class="dark"` on `<html>` via `next-themes` or manual toggle.

## Composed templates

Build `AppDialog` wrapping `@radix-ui/react-dialog` primitives in `ui/dialog.tsx` (your frozen primitive), composed layer adds title/body/footer props.

Use `cva` for variants on **composed** layer.

## Showcase

Same route map as `ts-shadcn` — no shadcn CLI; you own `ui/*` but still don't edit for product copy.

## Implement-us checklist

- [ ] Tokens in CSS vars + Tailwind extend
- [ ] Primitives stable; product logic only in `app/`
- [ ] `cn()` helper for class merging
