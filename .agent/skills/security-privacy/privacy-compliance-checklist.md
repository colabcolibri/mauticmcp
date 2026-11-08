# Privacy compliance checklist — LGPD (Brazil) and GDPR (EU/EEA)

> **Not legal advice.** Use this checklist to deepen `docs/02_security.md` during `/privacy-pass`. Canonical law text and regulator guidance live at the official URLs below — prefer these over blogs or law-firm marketing pages.

---

## When to run

| Mode | Trigger |
| ---- | ------- |
| `bootstrap` | After `01_tech_stack` when `00_scope` mentions users, PII, SaaS, or compliance |
| `full` | Before human sets `02_security` to `approved` |
| `US-XXXX` | Must US with PII/LGPD/GDPR acceptance |

Mark **N/A** per jurisdiction only when the manager confirms scope in writing (decision log if material).

---

## LGPD (Brazil) — Lei nº 13.709/2018

### Checklist

- [ ] **Roles** — controlador and operador identified for each processing activity
- [ ] **Legal bases** — Art. 7 (and Art. 11 if sensitive data) mapped per purpose
- [ ] **Titular rights** — Art. 18 channels documented (access, correction, deletion, portability, …)
- [ ] **Encarregado** — named contact or documented N/A with rationale
- [ ] **Privacy notice** — how transparency (Art. 9) is provided to titulares
- [ ] **Retention** — periods and deletion/anonymization procedure
- [ ] **Security** — Art. 46 measures aligned with `02` technical sections
- [ ] **Suboperadores** — subprocessors listed (hosting, email, analytics, payments)
- [ ] **RIPD** — required or not; if yes, status and encarregado involvement
- [ ] **International transfer** — mechanism if data leaves Brazil (Res. CD/ANPD nº 19/2024+)
- [ ] **Incidentes** — internal procedure; when to communicate to ANPD

### Referências oficiais — LGPD

| Resource | URL |
| -------- | --- |
| ANPD — portal | https://www.gov.br/anpd/pt-br |
| Lei 13.709/2018 (LGPD) — ANPD | https://www.gov.br/anpd/pt-br/centrais-de-conteudo/legislacao/lei-no-13-709-de-14-de-agosto-de-2018 |
| Lei 13.709 — Planalto | http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm |
| Marco Civil da Internet (Lei 12.965/2014) | http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm |
| Guias e materiais educativos ANPD | https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes |
| Documentos técnicos e orientativos ANPD | https://www.gov.br/anpd/pt-br/centrais-de-conteudo/documentos-tecnicos-orientativos |
| Comunicação de incidente de segurança | https://www.gov.br/anpd/pt-br/assuntos/incidente-de-seguranca |
| Guia — atuação do encarregado (PDF, 2024) | https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/copy_of_guia_da_atuacao_do_encarregado_anpd.pdf |
| Documentos e publicações (índice) | https://www.gov.br/anpd/pt-br/documentos-e-publicacoes |

---

## GDPR (European Union / EEA) — Regulation (EU) 2016/679

### Checklist

- [ ] **Territorial scope** — Art. 3 documented (establishment or targeting EU/EEA)
- [ ] **Roles** — controller and processor (Art. 4); processor agreements Art. 28
- [ ] **Lawful bases** — Art. 6 per purpose; Art. 9 if special categories
- [ ] **Transparency** — Arts. 12–14 privacy information provided
- [ ] **Data subject rights** — Arts. 15–22 workflows (access, erasure, portability, …)
- [ ] **DPO** — appointed or documented N/A (Arts. 37–39)
- [ ] **Records of processing** — Art. 30 where required
- [ ] **DPIA** — Art. 35 when high risk
- [ ] **Retention** — storage limitation (Art. 5(1)(e))
- [ ] **Subprocessors** — listed with transfer mechanism if outside EEA
- [ ] **Transfers** — Chapter V mechanism per destination (SCCs, adequacy, …)
- [ ] **Breach** — Arts. 33–34 notification procedure
- [ ] **Lead supervisory authority** — if cross-border (one-stop-shop) when applicable

### Official references — GDPR

| Resource | URL |
| -------- | --- |
| GDPR Regulation (EU) 2016/679 — EUR-Lex | https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng |
| Consolidated text CELEX 32016R0679 | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679 |
| European Data Protection Board (EDPB) | https://www.edpb.europa.eu/ |
| EDPB guidelines (controllers/processors) | https://www.edpb.europa.eu/guidelines-relevant-controllers-and-processors_en |
| EDPB documents register | https://www.edpb.europa.eu/documents_en |
| EU data protection — European Commission | https://commission.europa.eu/law/law-topic/data-protection_en |
| EDPB — role and structure | https://www.edpb.europa.eu/about-edpb/the-european-data-protection-board_en |
| EU institutions — EDPB profile | https://european-union.europa.eu/institutions-law-budget/institutions-and-bodies/search-all-eu-institutions-and-bodies/european-data-protection-board-edpb_en |

---

## Cross-jurisdiction notes

| Topic | LGPD (BR) | GDPR (EU) |
| ----- | --------- | --------- |
| Authority | ANPD | National SA + EDPB coordination |
| DPO label | Encarregado | DPO |
| Impact assessment | RIPD | DPIA |
| Breach notify | ANPD procedure | Art. 33 SA (+ Art. 34 titulares) |

Products serving **both** Brazil and EU must document **both** sections in `02_security.md`.

---

## Out of scope for this checklist

- UK GDPR post-Brexit (ICO) — future kit module
- US state privacy laws (CCPA/CPRA, …)
- HIPAA, PCI-DSS — use `security-pass` / sector checklists
- Generating production privacy policy text (legal review required)
