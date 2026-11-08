# CI gates catalog — stack-aware reference

> Kit reference for agents. Use during `/test-pass bootstrap` or `/security-pass bootstrap` after reading `docs/01_tech_stack.md` of the **active product** (monorepo: check `.meridian/projects.json`).
>
> **Profile first:** `python3 .agent/scripts/meridian_delivery.py quality-profile` — document only gates up to `qualitySiege` (`kit` | `standard` | `full`). See `agentic-quality-model.md`.

## Ordered gauntlet (by profile)

| Order | Gate family | `kit` | `standard` | `full` |
| ----- | ----------- | ----- | ---------- | ------ |
| 1 | Kit validator + delivery bootstrap + kit tests | ✓ | ✓ | ✓ |
| 2 | Product unit/integration per `10` | — | ✓ | ✓ |
| 3 | Typecheck / lint when stack requires | — | ✓ | ✓ |
| 4 | Dependency audit + Dependabot | — | — | ✓ |
| 5 | CodeQL per `01` languages | — | — | ✓ |
| 6 | Coverage advisory / mutation pilot | — | — | ✓ |
| 7 | Independent review (`agentic-trust-policy.md`) | — | — | ✓ |

Do not recommend layer 4–7 when profile is `kit` or `standard` unless human explicitly raises profile in manifest.

## How Meridian splits responsibilities

| Layer | Location | Agent documents in |
| ----- | -------- | ------------------- |
| **Kit** | `.agent/` (installed by `install-meridian-kit.sh`) | Workflows reference kit scripts; validator always applies |
| **Product** | `docs/` + application code of the active project | `08_environments.md` § CI/CD, `10_test_strategy.md` § runners |
| **Reference implementation** | Meridian monorepo root (when this repo is the product) | `.github/workflows/` — example for TS extension + kit Python |

`install-meridian-kit.sh` copies `.agent/` only. Product CI lives in each repo's `docs/08_environments.md` and optional `.github/workflows/`.

## When to add each gate

| Gate | Read signal in `01` | Document in | Human opts in by |
| ---- | ------------------- | ----------- | ---------------- |
| Governance validator | Always (Meridian) | `08` | Pre-commit or CI step |
| Unit/integration tests | Stack + `10` pyramid | `10` + `08` | Runner + CI job |
| Typecheck / lint | TS/JS in `01` | `10` + `08` | devDeps + CI step |
| Dependency audit | Lockfile in `01` | `08` + `02` | CI step (command below) |
| CodeQL | Languages in `01` | `08` | GitHub workflow per matrix row |
| Dependabot | Lockfile ecosystem | `08` or repo config | `.github/dependabot.yml` |
| Coverage / mutation | `10` policy | `10` | devDeps + advisory CI |

Optional gates: agent **documents** in phase docs first; implementation (workflow file, devDependencies) goes in a US with human approval when new packages are required.

## CodeQL language matrix

Derive `language` values from `01_tech_stack.md` — one matrix entry per language used in **this** product:

| Signal in `01` | CodeQL `language` | Typical use |
| -------------- | ----------------- | ----------- |
| TypeScript / JavaScript | `javascript-typescript` | Node, React, VS Code extension |
| Python | `python` | Django, FastAPI, kit scripts |
| Go | `go` | Go services |
| Java / Kotlin | `java` | JVM backends |
| Ruby | `ruby` | Rails |
| C# | `csharp` | .NET |
| Rust | `rust` | Check CodeQL release notes for support level |

**Examples**

- Next.js frontend + Python API → `[javascript-typescript, python]`
- Go microservice only → `[go]`
- Meridian monorepo (dogfood) → `[javascript-typescript, python]` — see `.github/workflows/codeql.yml`

## Dependabot and audit

| Lockfile / signal | Dependabot `package-ecosystem` | Directory |
| ----------------- | ------------------------------ | --------- |
| `pnpm-lock.yaml` | `npm` | folder containing lockfile |
| `package-lock.json` | `npm` | same |
| `go.mod` | `gomod` | module root |
| `Gemfile.lock` | `bundler` | `/` |
| Poetry / `requirements.txt` | `pip` | `/` |
| `.github/workflows/*.yml` | `github-actions` | `/` |

| Package manager | Audit command to document in `08` |
| --------------- | --------------------------------- |
| pnpm | `pnpm audit --prod --audit-level=high` |
| npm | `npm audit --audit-level=high --omit=dev` |
| pip | `pip-audit` or OSV-Scanner |
| go | `govulncheck ./...` |

## Kit gates (all Meridian products)

| Gate | Command |
| ---- | ------- |
| Governance | `python3 .agent/scripts/validate_meridian.py . --sqlite-only --strict-kit-md` |
| Kit tests | `python3 .agent/scripts/run_kit_tests.py` |
| Quality profile | `python3 .agent/scripts/meridian_delivery.py quality-profile` — WARN in validator if `10` approved and tier undeclared |
| Delivery DB | `python3 .agent/scripts/meridian_delivery.py bootstrap` |

## Optional gates — cost note for manager

Before recommending optional tooling, state trade-off in US or bootstrap output:

- **Stryker / mutmut / PIT** — extra devDependencies; CI time
- **CodeQL** — GitHub Actions minutes; language matrix must match `01`
- **Playwright E2E** — browser install; slower CI

## Bootstrap procedure

```txt
1. Resolve active product: docs/ of package root (monorepo: projects.json)
2. Run quality-profile — note qualitySiege and cap optional gates
3. Read docs/01_tech_stack.md
4. test-stack-catalog.md → fill docs/10_test_strategy.md (pyramid, runners, coverage policy)
5. This catalog → list applicable gates **up to profile tier**
6. Write docs/08_environments.md § CI/CD table (jobs, paths, status: required | optional | not configured)
7. New workflows or devDeps → US with human approval in Plan
```

## Related

- `agentic-quality-model.md` — tiers, article map, when to raise profile
- `test-stack-catalog.md` — unit/e2e runners
- `ci-gates-bootstrap.md` — `/security-pass bootstrap` procedure for `08` CI rows
- `.github/workflows/README.md` — Meridian monorepo workflow map (when dogfooding this repo)
