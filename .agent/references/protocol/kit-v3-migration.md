# Kit v3 migration — skills only, no workflows

> **v3.1:** `.agent/workflows/` removed. Invoke **`/skill-name`** (e.g. `/us-create`) or **`@agent`**.

## Invoke

| Task | Skill slash | Agent |
| ---- | ----------- | ----- |
| Create US | `/us-create` | `@story-maker` |
| Refine US | `/us-refine` | `@story-maker` |
| Review US | `/us-review` | `@story-checker` |
| Database | `/data-engineering` | `@data-engineer` |
| Status | `/project-status` | `@scrum-master` |

Full map: `agents-help.md`.

## After upgrade

```bash
./.agent/scripts/sync_kit.sh
python3 .agent/scripts/validate_meridian.py . --sqlite-only --strict-kit-md
```

Legacy names like `/create-us` are **gone** — use skill name `/us-create`.
