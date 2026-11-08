# Screen flow checklist

> Use with `/design-flow`. Persist in `docs/09_design_system.md` § Screen flows — not a side markdown in drafts.

## Preconditions

- [ ] `00_scope` names UI surfaces (web, native, extension, marketing)
- [ ] `03_user_types` names who does the job
- [ ] `05_architecture` names frontend module / route ownership
- [ ] Skip entire skill for CLI-only / headless products

## Inventory

- [ ] List **jobs** (from user types), not screens first
- [ ] Each job has a **primary screen** and named **supporting** screens (sheet, dialog, empty)
- [ ] No two primary screens share the same job without a written split (e.g. list vs detail)
- [ ] Every Must UI US maps to a row in the flow table (or is marked out of this pass)

## Per flow

For each primary flow, fill:

| Field | Pass when |
| ----- | --------- |
| Name | Verb + object (`Review sprint board`, not `Dashboard`) |
| Surfaces | Which of web / app / extension actually run it |
| Entry | Deep link, nav item, notification, or post-login default |
| Happy path | 3–7 steps; no “etc.” |
| Empty | First-run or zero data — what the user can do |
| Error | Failure that the user can recover from (retry, message) |
| Blocked | Auth, permission, or HAR — not a silent blank |
| Loading | Skeleton vs spinner; where it lives |
| Exit | Success landing or back target |

- [ ] Happy path does not hide empty/error as an afterthought
- [ ] Destructive actions have a confirm **or** an undo — documented
- [ ] Back/up is defined (stack, close sheet, or route) — no trap

## Information architecture

- [ ] Navigation model named: sidebar, top tabs, bottom tabs, stack, command palette, host chrome (IDE)
- [ ] Primary nav has **≤7** top-level items per surface (split or nest if more)
- [ ] Settings / rare tools are not mixed into the primary job chrome
- [ ] Density matches `04_principles` mood (work tool vs marketing)
- [ ] One visual focal point per screen (title + primary action); secondary actions are quieter

## Anti-patterns (fail)

- Kitchen-sink home: every capability on first paint
- Desktop table pasted into a 375px webview with only `overflow-x: scroll` and no stacked alternative
- Modal on modal; sheet that contains another full IA
- Different labels for the same job across surfaces
- Flow documented as a component list (`Button`, `Card`) instead of jobs

## Diagram

- [ ] One mermaid `flowchart` **or** `sequenceDiagram` per primary flow in `09`
- [ ] Nodes are screens/states, not React component names

## Handoff

| Gap type | Next |
| -------- | ---- |
| Missing rows in `09` | Stay on `/design-flow` |
| Tokens / type clash | `/design-theme` |
| Component inventory empty | `/design-pass` / `/design-showcase` |
| Missing product slice | `/create-us` or `/refine-us` |
