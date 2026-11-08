# Agentic trust policy — earned "right to not read"

> When agents and humans may rely on automated gates instead of line-by-line diff review.  
> **Delivery bootstrap:** `python3 .agent/scripts/meridian_delivery.py bootstrap`

## Where enforcement lives

| Scope | Source of truth |
| ----- | --------------- |
| Protocol (all Meridian projects) | US acceptance, `validate_meridian.py`, implement gate, independent review |
| Product CI | `docs/08_environments.md` § CI/CD + `docs/10_test_strategy.md` |
| Stack-specific optional gates | `ci-gates-catalog.md` — derived from `01_tech_stack.md` |

Each product documents its own CI jobs. The Meridian monorepo documents TS extension + kit Python in root `.github/workflows/` as one reference implementation.

## Permanent human review

These change classes keep human approval regardless of CI green:

| Change class | Why |
| ------------ | --- |
| `docs/05_architecture.md` or `docs/architecture/*` | Structural product decisions |
| Phase docs `00`–`11` rule changes | Business and compliance contracts |
| Normative modules in `02_security` | Auditor-facing correctness |
| `section-contracts.md` or validator rules | Oráculo for all US |
| Secrets, auth, dependency policy | Security posture |

Use **`requires_human_approval`** for spec and architecture diffs.

## Earned trust tiers

Track consecutive clean PRs (documented CI green + independent review) before relaxing diff review:

| Tier | Change class | Relax after | Human still reads |
| ---- | ------------ | ----------- | ----------------- |
| 0 | Default / unknown | — | Spec + diff |
| 1 | Docs-only (`docs/` prose, status unchanged) | 10 clean PRs | Spec + checklist |
| 2 | Kit scripts (`.agent/scripts/`) | 20 clean PRs | US acceptance + CI scores |
| 3 | Application code (paths in `01_tech_stack`) | 30 clean PRs | US acceptance + coverage/mutation trend |
| 4 | Validator / delivery schema | — | Always (tier 0) |

**Clean PR:** documented CI jobs pass; reviewer ≠ implementer agent; no hotfix within 48h.

## What to read instead of every diff

1. US acceptance criteria and spec deltas (before implement)
2. Test plan and **Executed** record (on close)
3. Coverage / mutation scores when in `10_test_strategy`
4. Independent reviewer output (`/security-review`, `/test-review`, Bugbot)
5. Exceptions and escalations

## Independent review

Implementer agent ≠ sole reviewer. Options: separate review pass, `CODEOWNERS` maintainer, `/review-us` or `/security-review` with read-only context.

## When CI fails

Fix code or tests. To change a gate, open a US — avoid one-off CI bypass.

## Related

- `agentic-quality-model.md` — ordered gauntlet and `qualitySiege` profiles
- `docs/10_test_strategy.md`, `docs/08_environments.md` — per product
- `.agent/agents/quality-owner/references/test-strategy/references/ci-gates-catalog.md`
- EPIC-18 — HAR and human gates
