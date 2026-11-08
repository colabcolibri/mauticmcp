# ts-vitest

**Unit:** Vitest · **E2E:** Playwright (when UI in scope)

## Layout

```txt
src/
  **/*.test.ts          # colocated or __tests__/
e2e/
  *.spec.ts             # Playwright
vitest.config.ts
playwright.config.ts    # if e2e
```

## Commands

```bash
npm run test            # vitest
npm run test:e2e        # playwright (if configured)
```

## US Plan citation

`docs/10_test_strategy.md` — § Runners (`ts-vitest`), § Layout

## Notes

- Prefer colocated `*.test.ts` for units
- Mock at module boundary; avoid testing implementation details
