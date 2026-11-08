# Environments & release checklist

## `08_environments.md`

- [ ] Local setup reproducible (clone → run) without tribal steps
- [ ] Env var **names** documented; secrets in vault only
- [ ] Staging vs production differences explicit
- [ ] CI pipeline summary (lint, test, build) matches `10` tier
- [ ] Deploy mechanism named (Vercel, Fly, k8s, etc.) — human triggers
- [ ] Rollback procedure per environment
- [ ] Health check / smoke after deploy

## Operational law

- [ ] Doc states: **agents do not push or release to production**
- [ ] Incident contact or on-call placeholder for human team

## Coordination

- [ ] `quality-owner` consulted when adding CI gates
- [ ] `security-champion` when deploy touches secrets or network exposure
