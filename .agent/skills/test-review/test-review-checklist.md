# Test review checklist

> Use with `/test-review`. Read-only audit.

## Preconditions

- [ ] US loaded via `show US-XXXX --full`
- [ ] `10_test_strategy.md` read when product uses automated tests

## US field checks

- [ ] `tests` field set appropriately (`required` | `optional` | `n/a`)
- [ ] `tests_status` matches reality (`pending` | `done`)
- [ ] Planned section has concrete steps (not generic placeholder)

## Executed evidence

- [ ] Record § Executed lists commands run and outcomes
- [ ] Automated tests referenced by path exist
- [ ] E2E steps match strategy runner

## Strategy compliance

- [ ] Test level matches pyramid (no e2e-only for pure logic)
- [ ] New suites follow folder layout in `10`
- [ ] Coverage expectations met or gap documented

## Before complete-us

- [ ] All security/design review gates done if US scope requires
- [ ] Gaps classified: doc | refine | implement

## Gap classification

| Type | Route to |
| ---- | -------- |
| Strategy outdated | `/test-pass` |
| Weak Plan/Planned | `/refine-us` |
| Missing tests | `/implement-us` |
| Ready to close | `/complete-us` |
