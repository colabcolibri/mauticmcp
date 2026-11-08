# Type hierarchy checklist

> Use with `/design-theme`. Persist in `09` § Typography (ramp table). One role → one size/weight/line-height.

## Ramp (roles, not a size dump)

Fill every role the product uses. Do not add sizes that have no role.

| Role | Typical use | Integrity rule |
| ---- | ----------- | -------------- |
| display | Marketing hero or rare splash | Optional; forbidden in dense work tools unless `09` allows it |
| h1 | Screen title — **one** per view | Do not style body copy as h1 |
| h2 | Section | Must be smaller/lighter than h1 |
| h3 | Sub-section | Must not match h2 size |
| body | Default reading | One size; not three “almost body” sizes |
| label | Form labels, chips | Distinct from body (size or weight) |
| caption / meta | IDs, timestamps | Smallest **readable** role; not disabled-looking body |
| code | Mono | Family documented; size relative to body |

- [ ] **≤2** font families (UI + mono). A third family needs a written exception in `09`
- [ ] Scale is stepped (e.g. 1.125 / 1.2 / 1.25), not 13/14/15/16/17px adjacent “tweaks”
- [ ] Weight map: regular for body, medium/semibold for labels or titles — not random 400/500/600/700 on one screen
- [ ] Line-height: titles tighter than body; body ≥1.4 for paragraphs
- [ ] Measure: body max width in `ch` or layout token (avoid full-bleed paragraphs on ultrawide)

## Hierarchy integrity (fail)

- Skipping: h1 then caption used as the paragraph
- Promoting: five competing “titles” on one screen
- Native vs web: web uses `px` locked while native uses Dynamic Type / `sp` with no mapping note
- Mixing `em`/`rem`/`px` in feature CSS with no rule
- Decorative font for body in a work tool (mood clash with `04`)

## Platform notes

| Platform | Document in `09` |
| -------- | ---------------- |
| Web | Root `rem`; headings as real `h1`–`h3` (a11y), styled via tokens |
| Native | How Dynamic Type / font scaling maps to the ramp |
| Extension / host | Inherit `editor` / workbench font unless `09` says otherwise |

## Pairing

- [ ] Title and body pairing stated (same family vs serif+sans)
- [ ] Numeric/tabular lining if dashboards show columns of numbers
