# CI security gates bootstrap

> Use with `/security-pass bootstrap` after `01_tech_stack.md` exists.  
> Works with `security-bootstrap.md` (app security in `02`) and `ci-gates-catalog.md` (pipeline gates in `08`).

## Read first

1. `python3 .agent/scripts/meridian_delivery.py quality-profile` — cap audit/CodeQL to declared tier
2. `docs/01_tech_stack.md` — languages, package managers, hosting  
3. `docs/08_environments.md` — existing CI section  
4. `.agent/agents/quality-owner/references/test-strategy/ci-gates-catalog.md`

## Procedure

```txt
1. Run quality-profile — document supply-chain gates only when tier is full (unless human opted in)
2. List languages and lockfiles present in this product repo
3. Map languages → CodeQL matrix rows (include only languages in use)
4. Map lockfiles → Dependabot ecosystems
5. Pick audit command for the documented package manager
6. Update docs/08_environments.md § CI/CD:
   - job name, trigger, scope, status (required | optional | not configured)
7. Update docs/02_security.md § Dependencies if supply-chain policy changes
8. New workflow files or devDeps → separate US; manager confirms before merge
9. Note CI time and package cost when recommending CodeQL, Stryker, or E2E
```

## Output template (`08` § CI/CD)

```md
### CI/CD

| Job | Trigger | Scope | Status |
| --- | ------- | ----- | ------ |
| validate-meridian | PR | `.agent/` governance | required |
| test | PR | _(from 10_test_strategy)_ | required |
| dependency-audit | PR | _(audit command from catalog)_ | optional |
| CodeQL | PR | languages: _(from 01)_ | optional |
```

## Human action required (HAR)

- GitHub Advanced Security org setup  
- First production secrets in CI  
- Private registry tokens for Dependabot  

Stop and flag HAR per `rules/MERIDIAN.md` when console signup is needed.
