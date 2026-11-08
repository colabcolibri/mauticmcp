# Design review checklist

> Use with `/design-review`. Read-only audit — fixes go to other workflows.

## Preconditions

- [ ] `09_design_system.md` exists
- [ ] `01_tech_stack.md` matches documented stack id
- [ ] Showcase routes listed in `09` (or explicitly "not yet built")

## Contract compliance

- [ ] Semantic tokens used — no random hex in feature components
- [ ] Primitives path untouched (diff grep: no product edits under `components/ui/` for shadcn)
- [ ] Feature UI uses composed `App*` templates where inventory exists
- [ ] New dialogs/forms not copy-pasting primitive markup at call sites

## Visual

- [ ] Colors match `09` § Colors (spot-check primary, background, destructive)
- [ ] No feature hex / one-off palette vs token source
- [ ] Typography matches `09` roles — no extra ad-hoc sizes
- [ ] Spacing rhythm — no cramped or broken layouts
- [ ] No horizontal overflow on mobile width (375px)

## Flow and surfaces

- [ ] Screen matches a `09` § Screen flows row (or gap filed)
- [ ] Empty / error / loading exist if the flow documents them
- [ ] Narrow layout follows `09` § Responsive (not desktop IA squeezed)

## States

- [ ] Hover/focus visible on interactive elements
- [ ] Disabled and error states where applicable
- [ ] Loading states for async actions (if in scope)

## Accessibility

- [ ] Keyboard reachability for main flows
- [ ] Form labels associated with controls
- [ ] Contrast not obviously below AA on body text

## Showcase (if built)

- [ ] Each `09` inventory row has a live demo
- [ ] Showcase shows all documented variants
- [ ] Showcase imports composed templates only

## Gap classification

| Type | Route to |
| ---- | -------- |
| Doc outdated | `/design-pass` |
| Flow / IA gap | `/design-flow` |
| Theme / type drift | `/design-theme` |
| Missing catalog | `/design-showcase` |
| Code drift | `/refine-us` + `/implement-us` |
| US missing 09 refs | `/refine-us` |

## Report template

```txt
Compliant: yes | partial | no
Blockers:
Doc gaps:
Code gaps:
Recommended US:
```
