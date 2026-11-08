# Database phase doc checklist

## `06_database.md` structure

- [ ] Storage model stated (Postgres, SQLite, Supabase, files-only, etc.)
- [ ] Entity list matches `05` boundaries — no orphan tables
- [ ] Migration tool and folder documented
- [ ] One migration per change; timestamp `YYYYMMDDHHMMSS`
- [ ] Backup / restore expectations for prod
- [ ] Who may write (roles, service accounts) — align with `02`

## Gates

- [ ] No destructive reset commands documented as normal ops
- [ ] RLS / tenancy noted when multi-tenant
- [ ] Index strategy for hot paths referenced in US Plans when known

## Handoff

- [ ] App code changes → `developer` via `/implement-us` only
- [ ] Threat model gaps → `security-champion`
