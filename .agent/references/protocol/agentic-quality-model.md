# Agentic quality model — from article to Meridian

> Pedagogical bridge: [“O direito de não ler o código”](https://raphamoura.dev/blog/o-direito-de-nao-ler-o-codigo/) → ordered gates, spec as oracle, earned trust.  
> **Material profile:** `.meridian/projects.json` → `projects[].qualitySiege` or `delivery.json` → `options.qualitySiege`  
> **CLI:** `python3 .agent/scripts/meridian_delivery.py quality-profile`

## Core idea

Confidence is **earned by change class**, not assumed. Humans and agents may skip line-by-line diff review only when:

1. The **spec** (US acceptance, phase docs) is the oracle
2. **Automated gates** match the declared profile (`qualitySiege`)
3. An **independent reviewer** is not the implementer (see `agentic-trust-policy.md`)

Meridian separates **kit protocol** (all products) from **optional product siege** (per-project opt-in).

## Ordered gauntlet (layers)

Build gates in this order — do not skip lower layers when documenting `08` / `10`:

| Layer | Profile minimum | What it proves |
| ----- | --------------- | -------------- |
| 1 — Kit | `kit` | US/delivery/schema valid; kit tests green |
| 2 — Product tests | `standard` | Runners in `10` execute; typecheck/lint when stack requires |
| 3 — Supply chain | `full` | Audit, Dependabot, CodeQL per `01` |
| 4 — Depth | `full` | Coverage advisory, mutation on critical modules |
| 5 — Review | `full` | Independent pass; trust tiers in `agentic-trust-policy.md` |

Details per gate: `ci-gates-catalog.md`. Stack signals: `docs/01_tech_stack.md`.

## Profiles (`qualitySiege`)

| Value | When to use | Agent documents |
| ----- | ----------- | --------------- |
| `kit` | Docs-only, early discovery, or no app code in scope | Kit gates only; `10` may be absent |
| `standard` | Product ships code with unit/integration tests | `10` runners + `08` CI for tests, typecheck, lint |
| `full` | High-trust agentic delivery; “siege” article model | All of `standard` + audit, CodeQL, coverage advisory, mutation pilot, review policy |

**Default when unset:** `kit` — explicit opt-in avoids imposing CodeQL/mutation on every consumer.

Existing repos **keep working** without changes: agents resolve `kit` and cap bootstrap recommendations. Nothing breaks; optional siege stays off until you declare it.

### Where to declare

| Repo shape | Source of truth |
| ---------- | --------------- |
| Multi-product monorepo | `.meridian/projects.json` → `projects[].qualitySiege` per product |
| Single product (no manifest) | `.meridian/delivery.json` → `options.qualitySiege` |
| Both set | Manifest entry for that `docs/` path **wins** over `delivery.json` |

Example manifest entry:

```json
{
  "id": "main",
  "name": "My App",
  "docs": "docs",
  "qualitySiege": "standard"
}
```

## Article → Meridian map

| Article concept | Meridian artifact |
| --------------- | ----------------- |
| Spec as oracle | US acceptance + `section-contracts.md` + validator |
| Ordered CI siege | `ci-gates-catalog.md` + profile tiers above |
| Mutation vs coverage | `10_test_strategy.md` — coverage finds gaps; mutation tests test quality |
| Independent reviewer | `agentic-trust-policy.md`, CODEOWNERS, `/test-review`, `/security-review` |
| Earned no-read | Trust tiers; permanent human review for arch/security/schema |

## Agent workflow hooks

| Step | Action |
| ---- | ------ |
| `/status` | Report `qualitySiege` + source |
| `/test-pass bootstrap` | Run `quality-profile`; document gates **up to** profile only |
| `/security-pass bootstrap` | Same; audit/CodeQL rows only when `full` (or explicitly in `standard` + decision) |
| `/refine-us` | Must US with `tests: required` → map each AC to runner layer in Plan |
| `/implement-us` | Cite profile in Plan; `full` → mutation/coverage on touched critical paths |
| `/complete-us` | Record lists gates that ran vs profile |

## Raising the profile

1. Human sets `qualitySiege` in manifest or `delivery.json`
2. `/test-pass bootstrap` + `/security-pass bootstrap` refresh `08` / `10`
3. Implement CI in US with approval for new devDeps/workflows
4. `prepend-decision` when policy changes affect all contributors

## Migrating existing projects

Brownfield and pre-v15 repos do not have `qualitySiege`. Treat migration as **declare → align docs → align CI** (not a one-shot script).

### Step 0 — discover current effective tier

```bash
python3 .agent/scripts/meridian_delivery.py quality-profile
```

If `source` is `default (no qualitySiege declared)`, the CLI still returns `kit` — that is conservative until a human opts in.

**Inference guide** (for the review conversation — agents use this in bootstrap output; they do **not** auto-write the JSON):

| Evidence in repo | Suggested tier |
| ---------------- | -------------- |
| Only Meridian kit; no `10` or `10` not in scope | `kit` (explicit or leave default) |
| `10_test_strategy.md` approved + unit/integration CI in `08` | `standard` |
| Above + audit, CodeQL, coverage/mutation, review policy in `08`/`10` | `full` |

### Where the review happens

| Moment | Who | What |
| ------ | --- | ---- |
| `/status` | `scrum-master` | Reports `qualitySiege` + `source`; flags when still default |
| `/test-pass bootstrap` | `quality-owner` | Proposes tier from `10`/`08`; asks manager to declare before documenting gates above tier |
| `/security-pass bootstrap` | `security-champion` | Same for audit/CodeQL rows |
| `/audit-docs` | `technical-writer` | Optional hygiene: manifest/delivery missing `qualitySiege` while `08`/`10` describe CI siege |
| `validate_meridian.py` | CI + pre-commit | **WARN** when `10` is `approved` but profile undeclared (effective `kit`) |
| Raising tier | Manager + `prepend-decision` | Log when team commits to new gates affecting everyone |
| CI/workflows missing for declared tier | `developer` via US | Implement after declaration — doc/bootstrap does not silently add workflows |

No mandatory US for **declaring** `kit` on a docs-only project. US is required when **raising** tier implies new devDeps, workflows, or policy.

### How to update the JSON

**Single product** (no `.meridian/projects.json`):

Edit `.meridian/delivery.json`:

```json
{
  "version": 1,
  "connector": "sqlite",
  "package_root": ".",
  "options": {
    "qualitySiege": "standard"
  }
}
```

**Monorepo** (manifest at kit root):

Add per product in `.meridian/projects.json` — do not remove existing fields:

```json
{
  "id": "app-osc",
  "name": "App OSC",
  "docs": "apps/app-osc/docs",
  "qualitySiege": "standard"
}
```

Products can differ: one `kit`, another `full`.

**Verify:**

```bash
python3 .agent/scripts/meridian_delivery.py quality-profile --package-root <package>
```

`source` must point to your edit (manifest or delivery), not `default`.

### After declaring

1. `/test-pass bootstrap` and `/security-pass bootstrap` — refresh `10` / `08` to match tier
2. If CI lags declaration → open US to implement missing jobs
3. Commit `.meridian/projects.json` or `delivery.json` (manifest is not gitignored)

CI and pre-commit run `validate_meridian.py` — undeclared profile with approved `10` surfaces as WARN.

## Related

- `agentic-trust-policy.md` — tiers and permanent human review
- `ci-gates-catalog.md` — gate commands and stack matrix
- `projects-manifest-template.md` — `qualitySiege` field
- `test-strategy-checklist.md` — AC ↔ test mapping
