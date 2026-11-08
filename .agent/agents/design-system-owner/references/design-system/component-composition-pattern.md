# Component composition pattern — all UI stacks

> **Mandatory** for every composed component in product code and showcase pages. Applies to `/design-pass`, `/design-showcase`, and `/implement-us` with UI.

## Names (use in Plan and `09`)

| Term | Meaning |
| ---- | ------- |
| **Primitive** | Installed library component (`components/ui/dialog.tsx`, MUI `Dialog`, `st.dialog`) — **immutable** |
| **Composed template** | Product-owned wrapper that assembles primitives from props — **where agents write** |
| **Composition pattern** | Build UI by nesting primitives + slots, not copying source |
| **Variant API** | Size/intent/style via props (`variant`, `size`) mapping to classes or theme — often **CVA** on shadcn |
| **Config-driven API** | Single component accepts structured props (`title`, `description`, `body`, `footerActions`) and renders the tree |

Industry labels: *compound components*, *wrapper components*, *facade components*, *headless + styled shell*.

---

## Golden rule — never edit installed primitives

```txt
IF library installed via CLI / package manager (shadcn, MUI, Chakra, antd, Streamlit, …)
THEN agents MUST NOT modify files under the primitive install path
ELSE derive composed templates that IMPORT primitives
```

| Stack | Primitive path (read-only) | Composed path (write here) |
| ----- | -------------------------- | --------------------------- |
| shadcn | `components/ui/**` | `components/app/**` or `components/composed/**` |
| MUI/Chakra/antd | imports from package | `components/app/**` |
| Django templ | `templates/ui/*.html` base copies | `templates/composed/*.html` |
| Python factories | thin re-exports only | `ui/composed/*.py` |
| Go templ | `views/ui/*.templ` | `views/composed/*.templ` |
| Rust | module `ui` primitives | `components/app/*.rs` |

**Allowed on primitives:** none, except regenerating via official CLI (`shadcn add`) when a new primitive is needed.

**Token changes:** theme/CSS vars / `createTheme` / `ConfigProvider` — not edits inside `components/ui/button.tsx`.

---

## Composed template contract

Every reusable dialog, sheet, form section, empty state, or data card follows:

### 1. Props (config-driven)

```ts
// Example — TypeScript; adapt types per language
type AppDialogProps = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: React.ReactNode;
  description?: React.ReactNode;
  body: React.ReactNode;           // text, form, or rich markup
  footer?: React.ReactNode;        // actions slot
  variant?: "default" | "destructive";
  size?: "sm" | "md" | "lg";
};
```

| Prop | Role |
| ---- | ---- |
| `title` | Header — string or node |
| `description` | Optional subtitle / helper |
| `body` | Main content — children, HTML, or form |
| `footer` | Actions — buttons, links |
| `variant` / `size` | Visual intent without forking primitive |

Python/Go/Rust: same fields as function parameters or struct fields.

### 2. Single assembly point

One composed file owns layout: header → body → footer. Call sites pass data only.

```txt
// Good
<AppDialog title="Delete item" body={<p>…</p>} footer={<Button>…</Button>} />

// Bad — copying DialogHeader/DialogFooter markup at every call site
```

### 3. Variants map to tokens

Variants change classes or theme tokens — not duplicate components (`DeleteDialog.tsx`, `ConfirmDialog.tsx` × 10). One `AppDialog` + `variant` prop.

shadcn: CVA on the **composed** wrapper if needed; prefer primitive's existing `variant` props.

### 4. Accessibility preserved

Composed template must forward `aria-*`, focus trap, and labels from primitives. Do not strip Radix/MUI a11y behavior.

### 5. Showcase entry

Each composed template appears on the design catalog page with:

- all `variant` values
- all `size` values
- states: default, disabled, loading, error (when applicable)
- mobile width snapshot note in `09`

---

## File naming

| Pattern | Example |
| ------- | ------- |
| `App{Primitive}.tsx` | `AppDialog.tsx`, `AppSheet.tsx` |
| `app_{primitive}.py` | `app_dialog.py` |
| `{name}.templ` | `app_dialog.templ` |

Export from barrel `components/app/index.ts` (or language equivalent).

---

## Dialog example (shadcn — reference implementation)

```tsx
// components/app/AppDialog.tsx — COMPOSED (write here)
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

export function AppDialog({
  open,
  onOpenChange,
  title,
  description,
  body,
  footer,
  size = "md",
}: AppDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className={sizeClasses[size]}>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          {description ? <DialogDescription>{description}</DialogDescription> : null}
        </DialogHeader>
        <div className="py-4">{body}</div>
        {footer ? <DialogFooter>{footer}</DialogFooter> : null}
      </DialogContent>
    </Dialog>
  );
}
```

`components/ui/dialog.tsx` stays shadcn-generated — **never edited** for product copy or layout hacks.

---

## Anti-patterns

| Anti-pattern | Fix |
| ------------ | --- |
| Edit `components/ui/button.tsx` for brand color | Change CSS vars / theme |
| Copy-paste Dialog markup in 20 pages | Use `AppDialog` |
| `variant` as separate component files | One component, variant prop |
| Inline styles for semantic colors | Token classes (`bg-primary`, `text-muted-foreground`) |
| Showcase page duplicates primitives | Showcase imports **composed** templates only |

---

## `09_design_system.md` section

Document under **Components**:

- Primary stack id (from `ui-stack-catalog.md`)
- Primitive path (read-only)
- Composed path convention
- List of `App*` templates with prop contract table
- Link to showcase route per template
