# Meridian security checklists

Use with `02_security.md`. Mark each item in the doc or report gaps explicitly.

Every item must have a clear pass/fail. If an item does not apply, mark N/A and state why — "N/A" alone is not acceptable.

---

## 1. Secrets and credentials

- [ ] `.env` and `.env.*` in `.gitignore` before first commit
- [ ] `.env.example` committed — no real values, all keys documented with description
- [ ] No secrets hardcoded in source, tests, docs, scripts, or CI config
- [ ] Logs do not write tokens, API keys, passwords, or PII — even on error paths
- [ ] Key rotation plan defined: frequency, who is responsible, procedure
- [ ] Secrets manager or vault strategy named (AWS SSM, GCP Secret Manager, Vault, Doppler, etc.) when applicable — not "will add later"

---

## 2. Data classification and sensitivity

- [ ] Data types inventoried: public, internal, confidential, regulated
- [ ] PII identified and mapped (name, email, phone, location, device ID, biometric, behavioral data)
- [ ] Regulated data mapped: LGPD / GDPR / HIPAA / PCI-DSS — at least one compliance posture explicitly stated
- [ ] Storage locations defined for each data type: DB, object storage, cache, logs, third-party services
- [ ] Retention and deletion policy: how long each type is kept, who triggers deletion, how it is verified
- [ ] Data minimization: only collecting what is strictly needed for each feature — not "collect now, decide later"

---

## 3. Threat modeling

Threat modeling is not a checklist item — it is a structured exercise. Use STRIDE as a minimum framework: **S**poofing, **T**ampering, **R**epudiation, **I**nformation disclosure, **D**enial of service, **E**levation of privilege.

For each major surface (API, admin panel, file upload, webhooks, background jobs, auth flow):

- [ ] Threat actors identified: anonymous user, authenticated user, privileged user, internal service, compromised third-party dependency
- [ ] At least one STRIDE threat mapped per surface — not just "injection" generically
- [ ] Mitigations documented for each threat — not just identified
- [ ] Trust boundaries explicit: what the system trusts, what it must verify, where the perimeter is
- [ ] Worst-case scenario documented per surface: data breach, account takeover, privilege escalation, data loss
- [ ] Business logic threats considered: can a user abuse valid features in unintended ways? (e.g. bulk actions, state transitions, price manipulation)

---

## 4. Authentication

- [ ] Auth model defined and named: session cookie, JWT, OAuth2, OIDC, SSO, API key — not "TBD"
- [ ] Token/session expiration strategy: access token lifetime, refresh flow, forced invalidation on logout
- [ ] Password hashing algorithm named: bcrypt, argon2id, scrypt — MD5/SHA1/SHA256 alone are not acceptable
- [ ] Password policy defined: minimum length, complexity rules (or rationale for not having them)
- [ ] MFA: current status (active / planned / N/A) and scope (all users / admins only / optional)
- [ ] Account lockout or rate-limiting on failed attempts: threshold, lockout duration, alert on abuse
- [ ] Credential recovery flow documented: how "forgot password" works, token expiry, no user enumeration
- [ ] Session fixation prevented: new session ID issued on login

---

## 5. Authorization

- [ ] Permission model aligned with `03_user_types.md` — every role explicitly listed
- [ ] Model type named: RBAC, ABAC, ownership-based, or hybrid — not implicit
- [ ] Least privilege enforced: each role documented with exactly what it can and cannot do
- [ ] Every sensitive route/action checks authorization server-side — not client-side only
- [ ] IDOR (Insecure Direct Object Reference) mitigated: resource ownership verified before access, not just existence
- [ ] Multi-tenant isolation: data from one tenant cannot be accessed by another, even by accident (if applicable)
- [ ] Privileged operations (delete, export, impersonate, admin promote) require explicit role check — not just authentication

---

## 6. Input validation and output encoding

- [ ] Server-side validation on all inputs — client-side validation is convenience, not security
- [ ] Validation library or schema named (zod, joi, pydantic, yup, etc.) — not ad-hoc checks
- [ ] File uploads: size limit, type allowlist (not just extension), storage outside webroot, virus scan strategy
- [ ] Output encoding context-appropriate: HTML escaping in templates, JSON encoding in APIs, attribute encoding in HTML attributes
- [ ] SQL/NoSQL injection: parameterized queries or ORM with no raw string concatenation containing user input
- [ ] Command injection: no user input passed to shell commands — use argument arrays, not interpolated strings
- [ ] Path traversal: user-supplied file paths normalized and validated against an allowlist of base directories

---

## 7. Fail secure and error handling

This is the OWASP 2025 A10 category (Exceptional Conditions). Systems that fail open are as dangerous as systems with broken auth.

- [ ] Default behavior on error is **deny**, not allow — fail secure, not fail open
- [ ] Authentication and authorization failures return generic errors — no stack traces, no internal paths, no user enumeration signals
- [ ] Exceptions do not bypass security checks — catch blocks do not silently grant access
- [ ] Timeout and unavailability of dependent services (auth provider, DB, cache) cause the request to fail safely — not to proceed unauthenticated
- [ ] Error responses are consistent in timing to prevent timing-based enumeration (login, password reset)
- [ ] All unhandled exceptions are logged with context, but the response to the user is generic

---

## 8. Logging and monitoring

Logging must be **affirmative** — not just "we don't log secrets", but "we do log these events".

- [ ] Security events logged: login success, login failure, logout, password change, permission denied, admin actions
- [ ] Log entries include: timestamp (UTC), user id or session id, action, resource, result (success/failure), IP
- [ ] Logs do not contain: passwords, tokens, API keys, PII beyond what is necessary for audit
- [ ] Log storage: where logs go, retention period, who has access
- [ ] Alerting defined: which events trigger alerts, who receives them, what the response is
- [ ] Audit trail for privileged actions: admin operations are traceable to a specific user and time

---

## 9. Business logic security

Business logic vulnerabilities do not appear in scanners. They require understanding what the system is supposed to do and finding ways to abuse valid features.

- [ ] State transitions validated server-side: cannot skip steps (e.g. checkout without payment, approve without review)
- [ ] Numeric inputs validated for range, sign, and overflow: prices, quantities, discounts cannot be negative or absurdly large
- [ ] Bulk or batch operations rate-limited and authorized: mass export, mass delete, mass invite require explicit permission
- [ ] Idempotency considered for sensitive operations: double-submitting a payment or action does not double-execute
- [ ] Race conditions considered for state-changing operations: optimistic locking or DB-level constraints where needed
- [ ] User-controlled references cannot affect other users' data: IDs, slugs, emails passed as input are validated against ownership

---

## 10. OWASP Top 10 — 2025 (mark N/A with reason if not applicable)

- [ ] **A01 Broken Access Control** — authorization enforced server-side on every route; IDOR mitigated
- [ ] **A02 Security Misconfiguration** — debug disabled in prod, default credentials changed, security headers set, CORS explicit
- [ ] **A03 Software Supply Chain** — lockfile committed, dependencies audited, CI integrity checks, no unverified packages
- [ ] **A04 Cryptographic Failures** — TLS everywhere, no weak ciphers (no TLS 1.0/1.1), sensitive data encrypted at rest
- [ ] **A05 Injection** — SQL, NoSQL, OS, LDAP, template injection mitigated; parameterized queries used
- [ ] **A06 Insecure Design** — threat model completed; business logic reviewed; no security-by-obscurity
- [ ] **A07 Identification and Authentication Failures** — covered in section 4 above
- [ ] **A08 Software and Data Integrity Failures** — unsigned updates rejected; serialization inputs validated; CI pipeline protected
- [ ] **A09 Security Logging and Monitoring Failures** — covered in section 8 above
- [ ] **A10 Exceptional Conditions** — fail-secure behavior documented; error paths do not grant access; timeouts handled

---

## 11. Infrastructure and network

- [ ] Hosting environment defined: cloud provider, region, self-hosted — not "TBD"
- [ ] Network segmentation: public-facing resources separated from internal services
- [ ] Firewall / security groups: only necessary ports open; principle of least network access
- [ ] TLS/HTTPS enforced on all public endpoints; HSTS header with adequate max-age
- [ ] Security headers set: `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`
- [ ] DDoS mitigation strategy: CDN, rate limiting, cloud shield — or N/A with documented rationale
- [ ] WAF (Web Application Firewall): in place, planned, or not applicable — documented
- [ ] Backups: frequency defined, storage location separate from primary, restoration tested at least once

---

## 12. Dependencies and supply chain

- [ ] Single lockfile committed (`package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`, etc.) — no floating versions
- [ ] Dependency audit tool named and scheduled: `npm audit`, `pip-audit`, `trivy`, `osv-scanner`
- [ ] Update strategy defined: manual review, Dependabot, Renovate — not "we'll update when needed"
- [ ] No packages from unknown, abandoned, or unmaintained sources — maintainer and license verified
- [ ] CI fails on high/critical severity vulnerabilities — not just warns
- [ ] SBOM (Software Bill of Materials) considered for regulated or high-risk contexts

---

## 13. Git and CI/CD

- [ ] `.gitignore` committed before secrets or `node_modules` ever touch the repo
- [ ] Secret scanning active: GitHub secret scanning, truffleHog, gitleaks — or equivalent
- [ ] Branch protection: main/master requires PR review; no direct push
- [ ] Pre-commit hooks: lint, type check, secret scan — documented and enforced
- [ ] CI pipeline: runs tests, security checks, and dependency audit on every PR
- [ ] Production deploy requires passing CI — no bypass path exists
- [ ] Environment variables injected by CI secrets — not stored in repo or image
- [ ] Docker images (if applicable): base image pinned by digest, not just tag; no secrets in layers

---

## 14. AI agents (Meridian-specific)

- [ ] No unnecessary sensitive files in agent context window — scope context to what the task requires
- [ ] No unapproved destructive commands executed autonomously (`rm -rf`, `db drop`, `DELETE FROM`, etc.)
- [ ] No private or regulated data sent to external AI APIs without explicit user consent and documentation in `02_security.md`
- [ ] Agent actions that affect production (deploy, migrate, delete) require explicit human confirmation
- [ ] Security-relevant decisions registered via `prepend-decision`
- [ ] Agent-generated code is reviewed before merge — not auto-merged without human review
