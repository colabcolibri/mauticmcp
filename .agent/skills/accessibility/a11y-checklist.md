# Accessibility checklist — `/a11y-pass`

> Oriented to **WCAG 2.2 Level AA** as default target unless scope says otherwise. Stack-agnostic.

## Bootstrap

- [ ] Target conformance level stated (A / AA / AAA / partial with rationale)
- [ ] Keyboard-only navigation required for all primary flows
- [ ] Focus visible style defined (token or pattern — not color-only)

## Full pass

- [ ] Semantic structure: headings, landmarks, lists — not div-only IA
- [ ] Form labels, errors, and required fields programmatically associated
- [ ] Images and icons: decorative vs informative alt policy
- [ ] Color contrast minimum documented (normal / large text) using design tokens
- [ ] Status and errors not conveyed by color alone
- [ ] Touch targets minimum size for mobile (document px or relative rule)
- [ ] Motion: `prefers-reduced-motion` respect for non-essential animation
- [ ] Modals: focus trap and return focus on close
- [ ] Live regions for async updates when UX requires announcements
- [ ] Skip link or equivalent for repetitive navigation (web)
- [ ] Documented exceptions with owner and remediation US

## US alignment

- [ ] UI US Acceptance cites a11y checks testable against this baseline
- [ ] `/design-review` scheduled before close on Must UI US

## Out of scope

- Formal VPAT / third-party audit procurement (human)
- Native platform store accessibility review (note as HAR if required)
