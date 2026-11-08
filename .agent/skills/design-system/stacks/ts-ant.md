# Implementation model — `ts-ant`

> React + Ant Design 5+. Stack id: **`ts-ant`**.

## Paths

| Layer | Path | Editable |
| ----- | ---- | -------- |
| Primitives | `antd` components | **No** |
| Composed | `src/components/app/*` | **Yes** |
| Theme | `ConfigProvider` `theme` prop + optional `theme/token` file | **Yes** |
| Showcase | `src/pages/design/*` | **Yes** |

## Bootstrap

```bash
npm install antd
```

Import styles once: `import 'antd/dist/reset.css'` (or CSS-in-JS per antd 5 docs).

## Theme — light + dark

**File:** `src/theme/antd-theme.ts`

```ts
import { theme, ThemeConfig } from "antd";

export const lightTheme: ThemeConfig = {
  algorithm: theme.defaultAlgorithm,
  token: {
    colorPrimary: "#1677ff",
    borderRadius: 6,
    fontSize: 14,
  },
};

export const darkTheme: ThemeConfig = {
  algorithm: theme.darkAlgorithm,
  token: {
    colorPrimary: "#1668dc",
  },
};
```

**Root:**

```tsx
import { ConfigProvider, theme as antTheme } from "antd";
const [dark, setDark] = useState(false);
<ConfigProvider theme={dark ? darkTheme : lightTheme}>
```

Prefer **token** changes over global `.ant-*` CSS overrides.

## Composed templates

| Template | antd |
| -------- | ---- |
| `AppDialog` | `Modal` with `title`, `footer`, children as body |
| `AppFormField` | `Form.Item` + `Input` / `Select` |
| `AppButton` | `Button` `type="primary" \| "default" \| "dashed"` |
| `AppCard` | `Card` |

`Modal` props map to config-driven API: `open`, `onCancel`, `title`, `footer`.

## Showcase

- Tokens: `Flex` + `div` swatches using `token.colorPrimary` via `theme.useToken()`
- Components: composed wrappers

## Responsive

- `Grid` `xs={24} md={12}`
- `Modal` `width={isMobile ? '100%' : 520}`

## Implement-us checklist

- [ ] `ConfigProvider` at app root
- [ ] `theme.algorithm` for dark, not manual hex per component
- [ ] Composed in `components/app/`
