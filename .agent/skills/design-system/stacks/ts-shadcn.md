# Implementation model — `ts-shadcn`

> React + Tailwind CSS + shadcn/ui (Radix primitives). Stack id: **`ts-shadcn`**.

## Paths

| Layer | Path | Editable |
| ----- | ---- | -------- |
| Primitives | `src/components/ui/*` or `components/ui/*` | **No** — `npx shadcn@latest add` only |
| Composed | `src/components/app/*` | **Yes** |
| Theme | `src/app/globals.css` or `src/index.css` | **Yes** |
| Tailwind | `tailwind.config.ts`, `postcss.config.*` | **Yes** (token mapping) |
| Showcase | `src/app/design/**` (App Router) or `src/pages/design/**` (Pages) | **Yes** |

## Bootstrap commands

```bash
npx shadcn@latest init
npx shadcn@latest add button dialog sheet input label select card tabs separator badge
```

Record `components.json` aliases (`@/components`) in `09`.

## Theme — light + dark

**File:** `globals.css`

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --destructive: 0 84.2% 60.2%;
    --border: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --destructive: 0 62.8% 30.6%;
    --border: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}
```

**Dark toggle:** `next-themes` `<ThemeProvider attribute="class" defaultTheme="system">` on root layout. Document in `09` § Responsive behavior.

**Tailwind:** colors use `hsl(var(--primary))` pattern from shadcn init.

## Semantic token map (09 → CSS)

| 09 semantic | CSS var |
| ----------- | ------- |
| background | `--background` |
| foreground | `--foreground` |
| primary | `--primary` |
| muted | `--muted` / `--muted-foreground` |
| destructive | `--destructive` |
| border | `--border` |

## Composed templates

| Template | Primitives used |
| -------- | ---------------- |
| `AppDialog` | `dialog` |
| `AppSheet` | `sheet` |
| `AppButton` | `button` (optional wrapper for icon+label defaults) |
| `AppFormField` | `label` + `input` or `select` |
| `AppCard` | `card` |

Follow `component-composition-pattern.md` — config-driven props.

## Showcase routes

| Route | Content |
| ----- | ------- |
| `app/design/page.tsx` | Index + `ThemeToggle` |
| `app/design/tokens/page.tsx` | Swatches using `bg-primary`, `text-muted-foreground`, type scale |
| `app/design/components/page.tsx` | Import only from `@/components/app/*` |
| `app/design/patterns/page.tsx` | `AppPageHeader` + form/list mocks |

## Responsive

- Tailwind breakpoints: `sm` 640, `md` 768, `lg` 1024, `xl` 1280
- Dialog: `sm:max-w-lg` etc. on `DialogContent`
- Tables: `overflow-x-auto` wrapper

## Implement-us checklist

- [ ] Primitives added via CLI, not hand-copied into `ui/`
- [ ] Theme vars in `globals.css`; no hex in `app/*`
- [ ] `App*` in `components/app/` only
- [ ] Showcase uses composed imports
- [ ] Dark mode tested if in scope
