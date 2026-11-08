# Showcase US slices (all stacks)

> `/design-showcase` uses this default breakdown. Adapt paths per `stacks/{stack-id}.md`.

## Standard slices

| Slice | Title pattern | Delivers (code via `/implement-us`) |
| ----- | ------------- | ----------------------------------- |
| DS-S1 | Wire theme tokens (light + dark) | Theme files from stack ref § Theme |
| DS-S2 | Design catalog shell | Index route + nav |
| DS-S3 | Token gallery page | Colors, typography, spacing live |
| DS-S4 | Component gallery page | All `App*` + states |
| DS-S5 | Layout patterns page | Form, list, detail, empty (if scope) |

Skip DS-S5 for minimal internal tools. Skip dark slice inside DS-S1 if `09` says light-only.

## Acceptance template (per slice)

```markdown
- [ ] Files match paths in stacks/{id}.md
- [ ] Light theme renders per 09 § Colors
- [ ] Dark theme toggles via stack-native mechanism (if in scope)
- [ ] No edits under primitive read-only path
- [ ] Route documented in 09 § Showcase catalog
```

## MoSCoW

- DS-S1, DS-S2, DS-S4: **Must** for UI products with showcase
- DS-S3: **Should**
- DS-S5, dark: **Could** unless `00_scope` requires

## Epic

Attach to design enabler epic or product epic per manager choice. `depends_on`: previous slice US.
