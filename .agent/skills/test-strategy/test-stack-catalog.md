# Test stack catalog

> Pick one **test stack id** for `/test-pass bootstrap`. Direction-level only — not vendor encyclopedia.

| id | When to pick | Unit default | E2E default |
| -- | ------------ | ------------ | ----------- |
| `ts-vitest` | Vite + TypeScript (recommended for modern TS) | Vitest | Playwright |
| `ts-jest` | Next.js or CRA-style Jest preset | Jest | Playwright |
| `ts-playwright` | E2E-first TS monorepo | Vitest or Jest | Playwright |
| `py-pytest` | Python backend or Django/FastAPI | pytest | pytest + Playwright optional |

## Signals from `01_tech_stack.md`

| Signal | Likely id |
| ------ | --------- |
| Vite, Vitest mentioned | `ts-vitest` |
| Next.js, Jest in package.json | `ts-jest` |
| Python, pytest | `py-pytest` |
| UI e2e mandatory, TS | add Playwright via `ts-playwright` notes |

## File map

Each id has `stacks/{id}.md` with folder layout and US Plan citation pattern.

CI pipeline gates (CodeQL, Dependabot, audit): `ci-gates-catalog.md` — use at `/test-pass bootstrap` or `/security-pass bootstrap`.
