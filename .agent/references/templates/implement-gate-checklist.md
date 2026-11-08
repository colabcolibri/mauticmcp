# Implement gate checklist — before product code

Use with `/implement-us US-XXXX` **before** any Write on product code for that story.

**Hard block:** if any required row fails → do **not** implement; report blocker and next command (`/review-us`, `/refine-us`, `/status`, etc.).

---

## Required gates

| # | Check | Pass when |
| - | ----- | --------- |
| 1 | `05_architecture.md` | `status: approved` |
| 2 | Epic + version | `epic:` and `version:` exist in folders |
| 3 | `ready` | Frontmatter `ready: true` (set only by `/review-us` / `story-checker`) |
| 4 | Sprint scope | `sprint: vX-SY` on US (canonical) or US in sprint `stories:` — sprint `planned`/`active`, same `version` |
| 5 | `## Plan` | Present; not placeholder; Approach has ≥2 explanatory bullets |
| 6 | Architecture refs | Each ref resolves to § in `05_architecture.md` **or** `docs/architecture/*.md` |
| 7 | `depends_on` | Every listed US has `status: ✅` |
| 8 | Story status | `❌` or `🔶` (not ✅ closed; not 🧊 frozen or 🚫 deprecated without manager waiver) |
| 9 | Session scope | One US id cited; manager did not bundle unrelated features |
| 10 | `04_principles.md` | Read DRY + SRP sections this session |
| 11 | Code quality | Implementation reuses existing modules per Approach; no copy-paste duplication; layer boundaries respected |
| 12 | UI vs `09` | If Acceptance is visual: `09` exists; do not invent tokens or a new type size; follow documented flow row |

---

## After gate passes

1. Read full US via `meridian_delivery.py show US-XXXX --full` (Intent + Plan).
2. Read every Architecture ref path/§ before coding.
3. Read `docs/04_principles.md` (DRY, SRP) — apply during implementation.
4. Implement against Acceptance + Planned steps only.
4. Do **not** mark `✅` in chat — close with `/complete-us` after review.
5. Partial work → `🔶` + `Missing:` in Acceptance; no `/complete-us` yet.

---

## Block messages (use verbatim pattern)

```txt
Blocked — cannot implement US-XXXX:
Reason: ready is false (run /review-us US-XXXX after /refine-us)
```

```txt
Blocked — cannot implement US-XXXX:
Reason: depends_on US-YYYY not ✅
```
