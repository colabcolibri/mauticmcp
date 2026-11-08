# Implementation model — `ts-chakra`

> React + Chakra UI v2. Stack id: **`ts-chakra`**.

## Paths

| Layer | Path | Editable |
| ----- | ---- | -------- |
| Primitives | `@chakra-ui/react` | **No** |
| Composed | `src/components/app/*` | **Yes** |
| Theme | `src/theme/index.ts` | **Yes** |
| Provider | `ChakraProvider` at root | **Yes** |
| Showcase | `src/pages/design/*` | **Yes** |

## Bootstrap

```bash
npm install @chakra-ui/react @emotion/react @emotion/styled framer-motion
```

## Theme — light + dark

**File:** `src/theme/index.ts`

```ts
import { extendTheme, type ThemeConfig } from "@chakra-ui/react";

const config: ThemeConfig = {
  initialColorMode: "system",
  useSystemColorMode: true,
};

export const theme = extendTheme({
  config,
  colors: {
    brand: {
      50: "#e6f2ff",
      500: "#3182ce",
      600: "#2b6cb0",
    },
  },
  semanticTokens: {
    colors: {
      "bg.canvas": { default: "gray.50", _dark: "gray.900" },
      "text.muted": { default: "gray.600", _dark: "gray.400" },
    },
  },
  components: {
    Button: { defaultProps: { colorScheme: "brand" } },
  },
});
```

**Toggle:** `useColorMode()` + `IconButton` with `aria-label="Toggle color mode"`.

Map `09` tokens to `semanticTokens` or `colors.brand`.

## Composed templates

| Template | Chakra |
| -------- | ------ |
| `AppDialog` | `Modal`, `ModalOverlay`, `ModalContent`, `ModalHeader`, `ModalBody`, `ModalFooter` |
| `AppFormField` | `FormControl`, `FormLabel`, `Input`, `FormErrorMessage` |
| `AppCard` | `Card` or `Box` with `borderWidth` |

## Showcase

- Token page: `SimpleGrid` of `Box bg="brand.500"` + `Text` `fontSize` steps
- Components page: composed imports only

## Responsive

- `Stack direction={{ base: 'column', md: 'row' }}`
- `Modal` `size={{ base: 'full', md: 'lg' }}`

## Implement-us checklist

- [ ] `extendTheme` single file
- [ ] `semanticTokens` for cross-mode colors
- [ ] `components` overrides in theme, not per-file hacks
