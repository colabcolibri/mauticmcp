# Audit markdown v11 — review completo para estrutura SQLite

> **Roster ao vivo:** `story-maker` + `story-checker` — [agent-station-map.md](../agent-station-map.md). O slug `backlog-refiner` foi removido.
> **Status:** onda G + **G7** ✅ — inventário em [`skill-references-audit-v11.md`](./skill-references-audit-v11.md)
> **Gatilho:** onda A marcou skills como ✅, mas dezenas de `.md` ainda descreviam delivery como arquivos `docs/us/*.md`, `app-desktop`, `/sync-board`, ou “US file”.  
> **Objetivo:** um agente ou humano consegue seguir **qualquer** markdown do kit sem ambiguidade v1 vs v11.

**Progresso rápido:**

| Onda | Status | Notas |
| ---- | ------ | ----- |
| **G1** | ✅ | rules, lifecycle, start-here, instruction-surfaces, docs/README |
| **H1** | ✅ | 9 agentes Scrum, `/design-pass`, routing v2, workflows |
| **H2** | ✅ | 6 legacy deletados; routing alias permanece |
| **G2** | ✅ | templates P0 + writing-guide |
| **G3** | ✅ | MERIDIAN, usage-guide, agents/workflows H1 |
| **G5** | ✅ | PR template, SECURITY, README |
| **G4** | ✅ | `docs/01_tech_stack.md` → extension + SQLite |
| **G6** | ✅ | `validate_kit_markdown_v11` + `--strict-kit-md` no CI |
| **G7** | ✅ | ver [`skill-references-audit-v11.md`](./skill-references-audit-v11.md) |

**Skills novas:** seguir `.agent/skills/doc.md` + padrão create-skill (description 3ª pessoa com WHAT/WHEN, tabela selective reading, corpo &lt;500 linhas, detalhes em `references/`).

---

## 1. Veredito honesto

| O que dissemos | Realidade |
| -------------- | --------- |
| Onda A ✅ — skills/workflows SQLite | **Parcial:** write paths nos skills principais; templates P0 em G2 |
| Onda H1 ✅ — roster Scrum | **OK** — 9 agentes, aliases legacy, validator atualizado |
| Onda C ✅ — sem `docs/templates/` | **OK** no repo |
| Onda D/E ✅ — scripts | **OK** |

**Conclusão:** onda **G** fechada (protocolo/dogfood + **G7** skills/references/workflows/agents).

---

## 2. Modelo alvo (uma frase por camada)

```txt
Phase docs     → docs/00–11, discovery/, architecture/, decisions/*.json  (Markdown Write)
Delivery       → .meridian/meridian.db                                    (CLI / form upsert)
Board UI       → leitura SQLite via meridian_db_export --format planning
Templates      → .agent/references/templates/                               (forma do body_markdown)
Protocolo      → .agent/MERIDIAN.md, rules/, agents/, skills/, workflows/
```

**Regra de ouro para revisores:** se o texto diz “crie/edite/leia `docs/us/US-XXXX.md`” como caminho **primário** → **P0 bug**. Menção a v1 em “não faça”, “legacy”, ou “branch meridian-v1-old” → **P2 OK**.

---

## 3. Scan automático (baseline jul/2026)

| Padrão | Arquivos afetados (aprox.) | Severidade | Progresso |
| ------ | -------------------------- | ---------- | --------- |
| `docs/us/`, `docs/epics/`, … como write path | ~28 → 0 operacional | P0–P1 | ✅ G2/G3/G6 |
| `app-desktop` como produto ativo | ~18 → 0 | P0–P1 | ✅ G4/G5 |
| `sync-board`, `board.json` | ~12 | P1 | ✅ histórico / proibição |
| “US file”, “must match filename” | ~5 → 0 | P0 | ✅ |
| `validate_meridian.py app-desktop` | ~6 → 0 | P1 | ✅ |

---

## 4. P0 — corrige antes de confiar nos agentes

| Arquivo | Problema | Status |
| ------- | -------- | ------ |
| `.agent/rules/MERIDIAN.md` § TIER 1 | paths v1 | ✅ G1 |
| `.agent/references/templates/lifecycle.md` | US file | ✅ G1 |
| `.agent/references/guides/start-here.md` | filename | ✅ G1 |
| `.agent/references/protocol/instruction-surfaces.md` | app-desktop | ✅ G1 |
| `.agent/references/scrum/scrum-meridian-map.md` | docs/sprints | ✅ G2 |
| `.agent/references/templates/as-is-inventory-template.md` | docs/epics, versions | ✅ G2 |
| `.agent/references/templates/projects-manifest-template.md` | us/US-XXXX.md only | ✅ G2 |
| `create-sprint/.../sprint-template.md` | docs/versions | ✅ G2 |
| `create-version/.../version-template.md` | docs/sprints | ✅ G2 |
| `create-user-story/SKILL.md` | description docs/us | ✅ G2 |
| `complete-user-story/.../implementation-template.md` | feat(app-desktop) | ✅ G2 |
| `docs/README.md` | app-desktop | ✅ G1 |
| `docs/04_principles.md` | tokens app-desktop | ✅ G4 parcial |
| `.github/pull_request_template.md` | app-desktop | ✅ G5 |
| `SECURITY.md` | app-desktop | ✅ G5 |
| `README.md` | link docs/versions | ✅ G5 |
| `.agent/rules/AGENTS.md` | app-desktop dogfood | ✅ G2 |
| `.agent/skills/generate-board-json/` | skill morta | ✅ removida |

---

## 5. P1 — desatualizado mas não quebra sempre

| Arquivo | Ação | Status |
| ------- | ---- | ------ |
| `.agent/MERIDIAN.md` | extensão vs monitor | ✅ G3 |
| `.agent/references/guides/usage-guide.md` | app-desktop UI | ✅ G3 |
| `.agent/references/templates/writing-guide.md` | anti-pattern paths | ✅ G2 |
| `README.md` | link docs/versions | ✅ G5 |
| Skills `create-epic/version` | padronizar wording | ✅ G2 |

---

## 6. P2 — manter (contexto legado / proibição)

| Arquivo | Por quê |
| ------- | ------- |
| `MERIDIAN_V2_CUTOVER.md` | histórico |
| `sqlite-delivery-operations.md` | lista o que **não** Write |
| `board-keeper.md` / legacy agents | deletados H2; aliases removidos H3 |
| `kit-improvement-plan.md` | diário de ondas |

---

## 7. Inventário — checklist arquivo a arquivo

Marque `[x]` quando **v11-operacional** (sem P0; P1 aceito ou corrigido).

### 7.1 Protocolo raiz `.agent/`

- [x] `MERIDIAN.md` — G3 (§9 agents, phase table)
- [x] `ARCHITECTURE.md` — H1
- [x] `IDE_ADAPTERS.md` — v11 adapters
- [x] `KIT_README.md` — kit-only distribution
- [x] `DISTRIBUTION.md` — extension + tarball

### 7.2 Rules

- [x] `rules/MERIDIAN.md` — G1 + H1 classifier
- [x] `rules/AGENTS.md` — G2
- [x] `rules/meridian.mdc` — H1 (`/design-pass`)

### 7.3 References (guias)

- [x] `references/start-here.md` — G1
- [x] `references/usage-guide.md` — G3
- [x] `references/agents-help.md` — H1
- [x] `references/commit-after-us-close.md` — SQLite + human commit
- [x] `references/protocol/instruction-surfaces.md` — G1
- [x] `references/scrum-meridian-map.md` — G2 + H1 roles
- [x] `references/scrum-guide-complete.md` — P2 textbook (não operacional)

### 7.4 References/templates (registry)

- [x] `templates/INDEX.md` — H1 + G2
- [x] `templates/TEMPLATE_SOURCES.md` — registry
- [x] `templates/writing-guide.md` — G2
- [x] `templates/section-contracts.md` — v11 body_markdown
- [x] `templates/sqlite-delivery-operations.md` — proibições Write
- [x] `templates/board-schema.md` — histórico import
- [x] `templates/doc-templates.md` — init
- [x] `templates/us-template.md` — shape only
- [x] `templates/epic-template.md` — shape only
- [x] `templates/refine-checklist.md` — SQLite ready gate
- [x] `templates/implement-gate-checklist.md` — developer gate
- [x] `templates/decision-template.md` — JSON prepend
- [x] `templates/decision-schema.md` — JSON schema
- [x] `templates/lifecycle.md` — G1
- [x] `templates/version-template.md` — G2
- [x] `templates/sprint-template.md` — G2
- [x] `templates/review-checklist.md` — H1
- [x] `templates/implementation-template.md` — G2
- [x] `templates/discovery-folder-guide.md` — H1
- [x] `templates/as-is-inventory-template.md` — G2
- [x] `templates/projects-manifest-template.md` — G2
- [x] `templates/architecture-folder-guide.md` — H1
- [x] `templates/code-quality-at-us-time.md` — refine gate

### 7.5 Agents (v11 roster — 9)

- [x] 9 agentes v11 — **H1** · legacy deletados **H2**

### 7.6 Workflows (18)

- [x] Todos workflows operacionais — **H1** (incl. `design-pass.md`)
- [x] `discover.md`, `update-decisions-log.md` — v11 OK

### 7.7 Skills — SKILL.md

> **Inventário arquivo a arquivo (honesto):** [`skill-references-audit-v11.md`](./skill-references-audit-v11.md) §1–§2.  
> Resumo: 9 skills delivery ✅ CLI; 5 skills phase/routing 👁 grep; `us-implement` banner ✅ G7.

- [x] Delivery skills (create → complete + epic/version/sprint) — [`skill-references-audit-v11.md`](./skill-references-audit-v11.md) §1
- [x] G7 fechado — §5 skill-references-audit ✅

### 7.8 Skills — references/

> Tabela completa: [`skill-references-audit-v11.md`](./skill-references-audit-v11.md) §2.

- [x] 9 arquivos delivery (us, epic, version, sprint, implementation, 3 checklists) — cabeçalho v11
- [x] `init-project/references/doc-templates.md` — grep OK
- [x] `security-review` + `design-system` refs — cabeçalho v11 G7

### 7.9 Scripts docs

- [x] `scripts/README.md` — validator + migrate lane documented

### 7.10 Dogfood `docs/`

- [x] `docs/README.md` — G1
- [x] `docs/00_scope.md` — histórico `app-desktop` removido OK
- [x] `docs/01_tech_stack.md` — G4 extension + SQLite
- [x] `docs/05_architecture.md` — seção removed monitor OK
- [x] `docs/02_security.md` — G4 extension + SQLite write scope
- [x] `docs/03_user_types.md` — v11 personas (sem Vite monitor)
- [x] `docs/07_api_contracts.md` — OK
- [x] `docs/08_environments.md` — OK
- [x] `docs/04_principles.md` — G4 parcial (app-desktop → extension)
- [x] `templates/writing-guide.md` — G2
- [x] `docs/09_design_system.md` — stub G1

### 7.11 Repo root / CI / extensão

- [x] `README.md` — G5 + delivery SQLite na hipótese
- [x] `SECURITY.md` — G5
- [x] `.github/pull_request_template.md` — G5

---

## 8. Ondas de execução (onda G)

```txt
G1 — P0 bloqueantes          ✅
H1 — roster Scrum              ✅
G2 — Templates + skill refs    ✅
G3 — Agents/workflows grep     ✅
G5 — Repo root, CI, SECURITY   ✅
G4 — Dogfood docs/00–11               ✅
G6 — Guardrail CI grep               ✅
G7 — Skills + references + CLI       ✅
```

**Inventário G7 (arquivo a arquivo):** [`skill-references-audit-v11.md`](./skill-references-audit-v11.md) — não duplicar checklist §7 aqui.

---

## 9. Guardrail (G6) — implementado

Função `validate_kit_markdown_v11()` em `validate_meridian.py`:

| Padrão | Severidade |
| ------ | ---------- |
| `validate_meridian.py app-desktop` | erro com `--strict-kit-md` |
| `/sync-board`, `generate-board-json`, `must match filename` | idem |
| `Write/Create/… docs/(us\|epics\|versions\|sprints)/` como caminho primário | idem |
| `app-desktop` sem contexto legacy/negado | idem |

**Flags:** default = WARN; `--strict-kit-md` = ERROR (usado no CI).

**Allowlist:** `references/plans/*`, templates históricos, linhas com `never` / `do not` / `removed` / `→` (markdown bold ignorado).

```bash
python3 .agent/scripts/validate_meridian.py . --strict-kit-md
```

---

## 10. Vocabulário v11 (cola para revisores)

| Evitar (v1) | Usar (v11) |
| ----------- | ---------- |
| `docs/us/US-XXXX.md` | `user_stories` row / `meridian_db_cli show US-XXXX` |
| `process-manager` + código | `scrum-master` + `developer` |
| `board-keeper` | `backlog-refiner` |
| `architecture-guardian` | `technical-architect` |
| `security-steward` | `security-champion` |
| `documentation-strategist` | `technical-writer` |
| `scope-architect` | `product-owner` |
| `implementation-specialist` / `design-steward` | `developer` / `design-system-owner` |
| `docs/epics/EPIC-XX.md` | `epics` table / `epic-create` |
| `docs/versions/vX.md` | `versions` table / `version-create` |
| `docs/sprints/vX-SY.md` | `sprints` table / `sprint-create` |
| `board.json` | `meridian_db_export --format planning` |
| `/sync-board` | _(removido)_ |
| `app-desktop` monitor | `app-visual-studio` extension |
| US file / filename | US id / `body_markdown` column |
| `validate_meridian.py app-desktop` | `validate_meridian.py . --sqlite-only` |

---

## 11. Critério de “pronto” (onda G)

- [x] G7 skills/references — [`skill-references-audit-v11.md`](./skill-references-audit-v11.md) §5 ✅
- [x] Zero P0 no grep com allowlist (guardrail CI)
- [x] Vocabulário de agentes alinhado com **`agent-roster-and-workflow-v11.md`** (H1 ✅)
- [x] Guardrail G6 no CI (`--strict-kit-md`)
- [x] Novo agente: `/create-us` → só SQLite (`us-create` skill)

---

## 12. Onda H — agentes e workflow

**H1 ✅ concluída.** Ver [`agent-roster-and-workflow-v11.md`](./agent-roster-and-workflow-v11.md).

| Agente | Papel | Workflow principal |
| ------ | ----- | ------------------ |
| `developer` | Development Team — incremento | `/implement-us` |
| `design-system-owner` | Enabler UI | `/design-pass` |
| `scrum-master` | Facilitação processo | `/status`, `/daily-with-ai` |
| `backlog-refiner` | Backlog refinement | `/create-us` … `/complete-us` |
| `product-owner` | Discovery + scope + epic | `/discover`, `/create-epic` |

**H2/H3 ✅** — 6 agentes legacy deletados; aliases de chat removidos; validator sempre ativo no kit.

---

## 13. H2 + H3 — remoção de legado

| Onda | Status |
| ---- | ------ |
| H2 | 6 arquivos `agents/*` legacy deletados |
| H3 | `agent-aliases-h2.md` deletado; aliases removidos de `meridian-routing` |
| Gate | `validate_meridian.py` — checagem de arquivos + slugs em docs operacionais (sempre no kit) |

- [x] `--strict-kit-md` sem erros
- [x] Zero arquivos legacy em `agents/`
- [x] Zero aliases de chat (H3)

---

## 14. `.meridian/` e git

| Artefato | Git? | Motivo |
| -------- | ---- | ------ |
| `.meridian/meridian.db` | **Não** (gitignore) | Delivery local |
| `.meridian/delivery.json` | **Sim** (quando existir) | Connector profile (`connector: sqlite` default) |
| `.meridian/projects.json` | **Sim** (quando existir) | Manifest multi-produto |

Baseline para novos projetos: `init-project/references/gitignore-baseline.md`. Referência operacional: `commit-after-us-close.md` § Scope.

