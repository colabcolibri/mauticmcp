# Supply chain checklist

> Use with `/dependency-audit`. Report only — run audit CLIs when manager approves.

## Inventory

- [ ] Lockfile(s) committed for each package manager in use
- [ ] No duplicate conflicting lockfiles without documented reason
- [ ] Direct dependencies listed in `01_tech_stack` or `08_environments`

## Hygiene

- [ ] Pinning strategy documented (exact vs range)
- [ ] Dev vs prod dependency separation clear
- [ ] No git+http or unversioned git deps without decision log entry

## Audit commands (by stack)

| Stack | Typical command |
| ----- | ---------------- |
| npm/pnpm | `npm audit` / `pnpm audit` |
| pip/poetry | `pip-audit` / `poetry audit` |
| cargo | `cargo audit` |
| go | `govulncheck ./...` |

## CI posture

- [ ] `08_environments` names when audit runs (PR, nightly, release)
- [ ] Fail vs warn policy documented

## US scope

- [ ] New dependencies in US appear in Plan
- [ ] License compatibility noted for copyleft deps when applicable

## Gap classification

| Type | Route to |
| ---- | -------- |
| Policy missing | `/security-pass` or update `02` |
| Env/CI gap | update `08_environments` |
| Vulnerable dep fix | `/implement-us` US |
