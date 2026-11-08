# Implementation model — `ts-mui`

> React + Material UI v5/v6. Stack id: **`ts-mui`**.

## Paths

| Layer | Path | Editable |
| ----- | ---- | -------- |
| Primitives | `@mui/material` imports | **No** (package) |
| Composed | `src/components/app/*` | **Yes** |
| Theme | `src/theme/theme.ts` | **Yes** |
| Provider | `src/app/providers.tsx` or root `main.tsx` | **Yes** |
| Showcase | `src/pages/design/*` or `src/routes/design/*` | **Yes** |

## Bootstrap

```bash
npm install @mui/material @emotion/react @emotion/styled
npm install @fontsource/roboto  # or project font
```

## Theme — light + dark

**File:** `src/theme/theme.ts`

```ts
import { createTheme, ThemeOptions } from "@mui/material/styles";

const base: ThemeOptions = {
  typography: { fontFamily: "Roboto, sans-serif" },
  shape: { borderRadius: 8 },
};

export const lightTheme = createTheme({
  ...base,
  palette: {
    mode: "light",
    primary: { main: "#1976d2" },
    secondary: { main: "#9c27b0" },
    error: { main: "#d32f2f" },
    background: { default: "#fafafa", paper: "#fff" },
  },
});

export const darkTheme = createTheme({
  ...base,
  palette: {
    mode: "dark",
    primary: { main: "#90caf9" },
    background: { default: "#121212", paper: "#1e1e1e" },
  },
});
```

**Provider:**

```tsx
import { ThemeProvider, CssBaseline } from "@mui/material";
// Toggle: useState mode 'light' | 'dark' or useColorScheme (MUI v6)
<ThemeProvider theme={mode === "dark" ? darkTheme : lightTheme}>
  <CssBaseline />
  {children}
</ThemeProvider>
```

Map `09` semantics to `palette.primary`, `palette.text.secondary`, `palette.error`, `palette.background`.

**Component defaults:** use `theme.components` overrides — never patch files in `node_modules`.

## Composed templates

| Template | MUI primitives |
| -------- | -------------- |
| `AppDialog` | `Dialog`, `DialogTitle`, `DialogContent`, `DialogActions` |
| `AppButton` | `Button` with default `variant` / `size` |
| `AppFormField` | `FormControl`, `FormLabel`, `TextField`, `FormHelperText` |
| `AppCard` | `Card`, `CardHeader`, `CardContent` |

Props: `title`, `description`, `body`, `footer`, `variant`, `open`, `onClose`.

## Showcase

- `/design/tokens` — `Box` grid with `bgcolor: 'primary.main'`, typography variants `h1`–`body2`
- `/design/components` — composed only
- Dark: theme toggle switches `ThemeProvider` theme

## Responsive

- `useMediaQuery(theme.breakpoints.down('md'))`
- `Dialog` `fullScreen={isMobile}`

## Implement-us checklist

- [ ] Single `theme.ts` source
- [ ] `CssBaseline` once at root
- [ ] Composed wrappers in `components/app/`
- [ ] No `sx={{ color: '#fff' }}` for brand — use `theme.palette`
