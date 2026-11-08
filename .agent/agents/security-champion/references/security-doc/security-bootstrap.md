# Security bootstrap guide

> Use with `/security-pass bootstrap` after `01_tech_stack.md` exists.

## Read first

1. `00_scope.md` — exposure, users, compliance hints
2. `01_tech_stack.md` — surfaces table, data layer, hosting
3. `02_security.md` — current stub (from init)

## Procedure

```txt
1. Fill § Security posture summary from scope + stack
2. Map each application surface (web, API, CLI, extension) to auth row
3. If local-only / no network: state trust boundary explicitly
4. Data classification: infer PII from user types interview
5. Threat model: one row per surface from 01 § Application surfaces
6. Secrets: list env vars from 08 stub or .env.example if exists
7. Dependencies: copy package manager + lockfile from 01
8. AI safety: if Meridian kit present, fill agent write-scope table
9. Move unknowns to § Gaps — never leave section empty silently
10. Walk security-doc-checklist.md
```

## Stack signals

| Signal in `01` | Pre-fill in `02` |
| -------------- | ---------------- |
| OAuth library | Authentication § OAuth2/OIDC |
| Postgres + RLS | Authorization + data protection |
| VS Code extension | Agent safety + local write scope |
| Public REST API | Rate limiting + OWASP table required |
| No auth | Authentication “none” + justify protected assets |

## Output

Report which sections were inferred vs need manager input.
