# Plano de melhoria do kit Meridian (skills, scripts, templates, v11 SQLite)

> **Status:** ondas A–G + H1/H2 ✅ — jul/2026  
> **Contexto:** v10 entregou SQLite + extensão VS Code; v11 remove `board.json` e `/sync-board` — board lê só `.meridian/meridian.db`.  
> **Objetivo:** protocolo coerente, uma fonte de verdade por camada, menos artefatos mortos.

---

## 1. Diagnóstico resumido

### O que funciona

| Camada | Estado |
| ------ | ------ |
| `.meridian/meridian.db` | Fonte de verdade de delivery (US, epic, version, sprint, deps) |
| Extensão `app-visual-studio` | Board, deliverables, form, save validado — lê SQLite via `meridian_db_export.py --format planning` |
| `meridian_db.py` + migrations | Upsert, FK, `story_dependencies`, `board_snapshots` |
| Phase docs `docs/00`–`11` | Markdown — correto |
| `/implement-us` + `implement-gate` CLI | Gate automatizado com exit code |

### O que estava desalinhado (e status)

| Problema | Status |
| -------- | ------ |
| Skills citam `docs/us/*.md` como write path | **Onda G + G7 — ✅** (`markdown-audit-v11.md`, `skill-references-audit-v11.md`) |
| `docs/templates/` espelho frágil | **Onda C — ✅ concluída** |
| Gate só em checklist | **Onda B — ✅ concluída** |
| `board.json` + `/sync-board` + `generate_board.py` | **Onda F2 — ✅ concluída (removidos)** |
| Skill `generate-board-json` | **Removida** |
| `/discover` fora de `agents-help` | pendente (onda A) |

---

## 2. Decisões fechadas

### 2.1 `docs/templates/` — removido ✅

Templates canônicos ficam em `.agent/references/templates/` apenas. `init-project` não cria espelho.

### 2.2 `board.json` e `/sync-board` — removidos ✅ (F2)

**Decisão:** board só no SQLite. Não há export JSON em `docs/kanban/`.

| Removido | Substituído por |
| -------- | --------------- |
| `docs/kanban/board.json` | `user_stories` + `story_dependencies` no DB |
| `generate_board.py` | `record_board_snapshot()` no upsert (auditoria em `board_snapshots`) |
| `/sync-board` workflow | nada — painéis refrescam ao mudar `meridian.db` |
| skill `generate-board-json` | nada |
| comando `meridian.syncBoard` | refresh automático na extensão |

**Legado:** projetos antigos podem ter `board.json` local; validator ignora quando `meridian.db` existe. Arquivo no `.gitignore`.

### 2.3 `/implement-us` — gate CLI ✅

`meridian_db_cli.py implement-gate US-XXXX [--json]` espelha `implement-gate-checklist.md`.

---

## 3. Modelo alvo (v11)

```txt
CAMADA                    FONTE DE VERDADE              QUEM LÊ/ESCREVE
─────────────────────────────────────────────────────────────────────────
Phase docs                docs/00–11, decisions/       Write (markdown)
Discovery                   docs/discovery/              Write (markdown)
Delivery                    .meridian/meridian.db        meridian_db_cli / form
Board (UI)                  meridian.db (planning export) extensão + CLI show/list
Snapshots (auditoria)       board_snapshots              upsert automático
Templates (protocolo)       .agent/references/templates/  Read only (agents)
Workflows                   .agent/workflows/            Human slash → agent
Skills                      .agent/skills/               Agent procedures
Scripts                     .agent/scripts/              CLI, CI, extension
```

**Fluxo US:**

```txt
/create-us     →  meridian_db_cli create-us / --write-form (SQLite)
/review-us     →  show (read-only)
/refine-us     →  update-us / set-ready
/implement-us  →  implement-gate CLI → código
/complete-us   →  update-us com Record + status ✅
(board UI)     →  automático ao salvar no DB — sem slash
```

---

## 4. Ondas de execução

### Onda A — Verdade única SQLite (skills + workflows) — **⚠️ parcial**

Paths nos skills/workflows principais atualizados. **Revisão de conteúdo completa → onda G** (`markdown-audit-v11.md`).

| Arquivo | Mudança |
| ------- | ------- |
| `skills/create-user-story/SKILL.md` | `create-us` / `--write-form`; `sqlite-delivery-operations.md` |
| `skills/refine-user-story/SKILL.md` | `update-us` + `set-ready` |
| `skills/review-user-story/SKILL.md` | `show`; sem Write |
| `skills/implement-user-story/SKILL.md` | `show --full`; gate CLI |
| `skills/complete-user-story/SKILL.md` | `update-us` com Record |
| `skills/create-epic/version/sprint` | SQLite (onda E para CLI dedicado) |
| `workflows/*.md` (delivery) | paths SQLite |
| `MERIDIAN.md`, `rules/MERIDIAN.md` | delivery = DB; sem board.json |
| `references/start-here.md`, `agents-help.md` | árvore v11; sem sync-board |

### Onda B — `implement-gate` CLI — **✅ concluída**

### Onda C — Remover `docs/templates/` — **✅ concluída**

### Onda D — Reorganizar scripts — **✅ concluída (jul/2026)**

Subpastas `lib/`, `migrate/`, `test/`, `dev/` com shims na raiz para CI/extensão.

### Onda E — Epic / version / sprint no CLI — **✅ concluída (jul/2026)**

`meridian_db_cli.py create-epic`, `version-create`, `sprint-create`.

### Onda G — Audit markdown v11 — **✅ concluída (G1–G7 + H1/H2)**

Revisão sistemática — ver `markdown-audit-v11.md` e `skill-references-audit-v11.md`.

Sub-ondas: G1 ✅ · H1 ✅ · H2 ✅ · G2–G7 ✅ · G6 guardrail CI ✅

### Onda H — Agent roster e workflow — **✅ H1 + H2 concluídas**

Roster Scrum v11 — ver `agent-roster-and-workflow-v11.md`. H2/H3 = legacy removido (arquivos + aliases).

| Entregável | Status |
| ---------- | ------ |
| `developer` — dono de `/implement-us` | ✅ H1 |
| `design-system-owner` — `09_design_system.md` | ✅ H1 |
| `scrum-master` sem código de produto | ✅ H1 |
| Workflow `/design-pass` | ✅ H1 |
| Routing + agents-help + INDEX + validator | ✅ H1 |

### Onda F — Board só SQLite — **✅ F2 concluída**

| Item | Status |
| ---- | ------ |
| Remover `board.json` do dogfood | ✅ |
| Remover `generate_board.py` | ✅ |
| Remover `/sync-board` + skill | ✅ |
| `record_board_snapshot()` no upsert | ✅ |
| Validator ignora board.json com DB | ✅ |
| Extensão sem `meridian.syncBoard` | ✅ |
| `.gitignore` `docs/kanban/board.json` | ✅ |
| `board-schema.md` → shape SQLite | ✅ |

---

## 5. Inventário atualizado

### Skills removidas

| Skill | Motivo |
| ----- | ------ |
| `generate-board-json` | board não é mais JSON em disco |

### Workflows removidos

| Workflow | Motivo |
| -------- | ------- |
| `sync-board` | board lê DB direto |

### Scripts removidos

| Script | Motivo |
| ------ | ------ |
| `generate_board.py` | substituído por `board_snapshots` no upsert |

### Extensão

| Área | Status |
| ---- | ------ |
| `sync-board.ts` | removido |
| `meridian-context.ts` | watcher só em `meridian.db` |
| `generate-board.ts` | mantém mapeamento de tipos (testes); sem `writeBoardJson` |

---

## 6. Ordem de execução (atualizada)

```txt
1. Onda B — implement-gate CLI          ✅
2. Onda C — remover docs/templates      ✅
3. Onda F2 — remover board.json/sync    ✅
4. Onda A — skills/workflows SQLite     ✅
5. Onda D — reorganizar scripts            ✅
6. Onda E — CLI epic/version/sprint        ✅
7. Onda G — audit markdown v11 (completo)  ✅
8. Onda H — agent roster + workflow       ✅
```

---

## 7. Critérios de “pronto”

- [x] `/implement-us` documenta `implement-gate` CLI
- [x] `docs/templates/` ausente; init não recria
- [x] `board.json` e `/sync-board` removidos; extensão sem comando sync
- [x] Nenhuma skill de delivery cita `Write docs/us/` como caminho primário
- [x] Nenhuma referência ativa a `generate-board-json` ou `generate_board.py`
- [x] `agents-help.md` e guias (`start-here`, `usage-guide`) listam fluxo v11
- [x] `validate_meridian.py . --sqlite-only` passa
- [x] Testes: schema, story_dependencies, implement_gate
- [ ] Extensão: board + form + save em `meridian-teste`
- [x] `sync_cursor_kit.sh` sem app-desktop templates

---

## 8. Perguntas abertas

1. **CLI único** `meridian` com subcomandos vs vários scripts na raiz?
2. **Epic/version/sprint** — prioridade de CLI dedicado vs só `--write-form`?
3. **`board_snapshots`** — reter histórico indefinido ou política de purge?

---

## 9. Próximo passo imediato

1. **Extensão** — validar board + form + save em `meridian-teste` (único critério aberto em §7)
2. **Opcional** — CLI único `meridian` com subcomandos (§8 pergunta 1)
3. **Manutenção** — novos skills delivery seguem `skill-references-audit-v11.md` §6

---

*Documento vivo — atualizar após cada onda. Maintainer map: `.agent/references/protocol/instruction-surfaces.md`.*
