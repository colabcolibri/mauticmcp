# ts-playwright

**Focus:** E2E with Playwright; unit via Vitest or Jest alongside

## Layout

```txt
tests/e2e/
  *.spec.ts
playwright.config.ts
```

## Commands

```bash
npx playwright test
npx playwright test --ui   # debug
```

## US Plan citation

`docs/10_test_strategy.md` — § Runners (`ts-playwright`), § Pyramid (e2e slice)

## Notes

- Page objects optional for 3+ flows
- Run against staging URL from `08_environments.md`
