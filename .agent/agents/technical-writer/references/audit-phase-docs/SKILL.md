---
name: audit-phase-docs
description: Audits Meridian phase docs against each other and the codebase; reports gaps and optionally applies draft improvements. Use with /audit-docs for brownfield or Meridian-started projects.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Audit phase docs (Meridian)

> **Read-only by default.** With manager approval in the same turn, apply **draft** fixes only — never `approved`.

## Selective reading

| File | When to read |
| ------- | ---------- |
| `.agent/references/templates/phase-docs/{doc}.md` | **Mandatory** — read full guide (what/for/how/revisit) + compare product `docs/` to stub |
| `.agent/skills/init-project/references/doc-templates.md` | Global rules |
| All `docs/0X_*.md` present | **Mandatory** |
| `docs/inventory/as-is.md` | If exists |
| `docs/05_architecture.md` + `docs/architecture/` | Consistency |
| Codebase (sample) | Spot-check claims in docs |

## When to trigger

- Phase docs feel thin after `/init-meridian` or `/document-project`
- Docs may have drifted from code
- Before approving `05_architecture` or starting epics
- Workflow `/audit-docs`
- Manager: “audit docs”, “refine scope”, “review governance”, “improve phase docs”

**Not** for US — use `/review-us`. **Not** for product brief — use `/discover`.

---

## Audit dimensions

| # | Dimension | Check |
| - | --------- | ----- |
| 1 | **Guide compliance** | Product doc matches template guide: sections filled, no silent TBD |
| 2 | **Depth checklist** | Template depth checklist + empty `##` |
| 3 | **Dependency order** | `depends_on` / `blocks` frontmatter |
| 4 | **Cross-doc** | Scope users ↔ `03`; stack ↔ `01`; layers `04` ↔ `05` |
| 5 | **Evidence** | Mode B claims have paths; stale paths flagged |
| 6 | **Gates** | `05` not approved while `04` empty; security gaps |
| 7 | **Inventory** | High rows promoted or explained in scope/architecture |
| 8 | **Quality profile** | `quality-profile` run; if default but `08`/`10` describe CI siege → suggest `qualitySiege` in manifest or `delivery.json` |

---

## Procedure

1. List all phase docs + frontmatter status.
2. Score each doc: `ok` \| `thin` \| `missing` \| `stale` \| `contradiction`.
3. Spot-check codebase for top 5 risks (auth, data store, main app entry).
4. Write **audit report** in chat (table + prioritized fixes).
5. If manager asked to fix or `$ARGUMENTS` contains `apply`:
   - Edit only `draft` or `review` docs
   - Never set `approved`
   - Never create US/epics
6. If apply changed scope, stack, security, or architecture narrative → **mandatory** `/update-decisions-log` (`prepend-decision`) before reporting done; cite affected docs in `--impact`.

---

## Output format

```txt
Phase docs audit:
Package root:
Docs scanned: N
Summary: ok X | thin Y | issues Z

| Doc | Score | Top issue |
| --- | ----- | --------- |

Cross-doc contradictions:
Code vs doc mismatches:
Priority fixes (ordered):
Applied draft fixes: yes | no — [paths]
Next: /document-project | /architecture | /security-pass | human approve 04
```

---

## vs other commands

| Command | Focus |
| ------- | ----- |
| `/audit-docs` | All phase docs + consistency |
| `/document-project` | Create/refresh from codebase |
| `/discover` | Product intent brief |
| `/review-us` | Single US row only |
