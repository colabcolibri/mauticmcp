# ts-jest

**Unit:** Jest · **E2E:** Playwright or Cypress

## Layout

```txt
src/
  **/__tests__/**/*.test.ts
e2e/ or tests/e2e/
jest.config.ts
```

## Commands

```bash
npm test
npm run test:e2e
```

## US Plan citation

`docs/10_test_strategy.md` — § Runners (`ts-jest`)

## Notes

- Next.js: use `next/jest` preset when applicable
- Snapshot tests sparingly — prefer behavior assertions
