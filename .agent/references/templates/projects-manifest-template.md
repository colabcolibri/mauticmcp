# Projects manifest template (monorepo / multi-product)

> **Optional artifact** — `.meridian/projects.json` at kit root. Declares Meridian **products** (each = one folder named exactly `docs`). Works with automatic discovery (A + B).

Read before creating or editing `.meridian/projects.json`.

---

## When to use

| Situation | Action |
| --------- | ------ |
| Single `docs/` at repo root | Manifest **optional** — discovery finds it |
| Several `docs/` folders (any layout) | Manifest **recommended** — names, default, exclude |
| Folder named `docs-extra` or other | **Never** auto-included — only exact name `docs` |

---

## File location

```txt
.meridian/projects.json
```

Relative to kit root (where `.agent/MERIDIAN.md` lives).

---

## Template

```json
{
  "version": 1,
  "default": "main",
  "projects": [
    {
      "id": "main",
      "name": "Main product",
      "docs": "docs",
      "qualitySiege": "standard"
    },
    {
      "id": "app-osc",
      "name": "App OSC",
      "docs": "apps/app-osc/docs"
    }
  ],
  "exclude": []
}
```

### Fields

| Field | Required | Meaning |
| ----- | -------- | ------- |
| `version` | yes | Schema version (`1`) |
| `default` | no | `id` of active project when none chosen |
| `projects` | no | Declared products (merged with discovery) |
| `projects[].id` | yes | Stable slug (`[a-z0-9-]+`) |
| `projects[].name` | yes | Human label in picker / status bar |
| `projects[].docs` | yes | Path to folder **`docs`** relative to kit root |
| `projects[].qualitySiege` | no | `kit` \| `standard` \| `full` — optional robust validation stack (see `agentic-quality-model.md`) |
| `exclude` | no | `docs` paths to drop (even if discovered) |

### `docs` path rules

- Must point to a directory whose **name is exactly** `docs`
- Examples: `docs`, `app-desktop/docs`, `apps/app-osc/docs`, `sistema-phomenta/docs`
- **Not** `docs-extra`, `documentation`, `doc` — those are ignored by discovery

---

## Discovery (B) — automatic

When the manifest is absent or incomplete, scan kit root for folders named **`docs`** only:

1. Walk the tree (depth limit, skip `node_modules`, `.git`, etc.)
2. For each `…/docs`, apply Meridian fingerprint:
   - `00_scope.md` exists, **or**
   - `us/US-XXXX.md` exists
3. Add to project list with inferred `id` / `name` from parent folder

`docs-extra` is never discovered (wrong folder name).

---

## Merge A + B

```txt
manifest.projects (validated on disk)
  ∪ discovery (fingerprint Meridian docs/)
  − exclude
  → sorted project list
```

| Source wins for | Rule |
| --------------- | ---- |
| `id`, `name`, `default` | Manifest |
| Unknown `docs/` paths | Discovery adds |
| Excluded paths | Removed last |

---

## Active project

One **active** `docs/` at a time for board, validate, sync, agent context.

| Priority | Source |
| -------- | ------ |
| 1 | VS Code setting `meridian.activeProject` |
| 2 | Last picker choice (workspace state) |
| 3 | Workspace folder matches a package `docs/` |
| 4 | `default` in manifest |
| 5 | Only one project → auto |
| 6 | Quick Pick if still ambiguous |

| Switch | Where |
| ------ | ----- |
| **Board / Deliverables toolbar** | First row **Project** — dropdown when N>1; shows `docs/` path and US count |
| Command | **Meridian: Select Active Project** |
| Status bar | Project name prefix when N>1 (click to switch) |
| Setting | `meridian.activeProject` — pin id in workspace settings |

**Persistence:** after first choice, reopening Board or Deliverables loads the **same** project — no repeat Quick Pick.

Validate target: **package folder** that owns `docs/` (e.g. `apps/app-osc`, not monorepo root).

---

## Agent rules

| Do | Don't |
| -- | ----- |
| Read `.meridian/projects.json` when present | Assume `docs/` is always at repo root |
| Run `validate_meridian.py` on package folder | Validate monorepo root when docs live in packages |
| Confirm active project before US work | Mix US from two `docs/` trees in one session |
| Use `exclude` for stray `docs/` folders | Rename `docs-extra` to `docs` unless it is a real product |

---

## Examples

**Single repo:**

```json
{
  "version": 1,
  "default": "main",
  "projects": [{ "id": "main", "name": "My App", "docs": "docs" }]
}
```

**Monorepo with exclude:**

```json
{
  "version": 1,
  "default": "osc",
  "projects": [
    { "id": "osc", "name": "App OSC", "docs": "apps/app-osc/docs" },
    { "id": "sistema", "name": "Sistema", "docs": "apps/sistema-phomenta/docs" }
  ],
  "exclude": []
}
```

Legacy `docs-extra` needs no exclude — discovery never picks it.

---

## qualitySiege (optional)

Declares whether this product uses the **optional robust validation stack** beyond Meridian kit gates.

| Value | Meaning |
| ----- | ------- |
| `kit` | Validator + delivery + kit tests only (default when omitted) |
| `standard` | + product unit/integration, typecheck, lint per `10_test_strategy.md` |
| `full` | + audit, CodeQL, coverage advisory, mutation pilot, independent review policy |

Agents resolve via `python3 .agent/scripts/meridian_delivery.py quality-profile`.

**Validator:** `validate_meridian.py` warns when `10_test_strategy.md` is `approved` but no `qualitySiege` is declared (stays effective `kit`). Declare explicitly even if tier is `kit`.

**Single-product repo without manifest:** set `.meridian/delivery.json` → `options.qualitySiege` instead.

```json
{
  "version": 1,
  "connector": "sqlite",
  "package_root": ".",
  "options": {
    "qualitySiege": "standard"
  }
}
```

Manifest entry for a project **wins** over `delivery.json` when both exist.
