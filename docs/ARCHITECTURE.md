# Architecture — Jingfan IMS GTM Intelligence

Week 1 (Architecture Freeze) audit and target architecture. See `docs/PIPELINE.md` for the pipeline/state-machine detail and `docs/DATA_CONTRACT.md` for the full contract field reference.

## 1. What This System Is

An AI-native GTM intelligence system for Jingfan IMS (industrial water-treatment instrumentation, China market). The business methodology — Radar → Qualification → Enrichment → Orchestration → Engagement — is already running, operated by human + Cloud Agent collaboration. This repository is the shared coordination layer between those agents.

This is **not** a generic marketing automation SaaS, not a Clay competitor, not a CRM. It is infrastructure for turning an already-validated business methodology into a reliable, evidence-based, progressively automated pipeline.

## 2. Repository Audit (as of 2026-08-22)

### Repository Structure (before this task)

```
.
├── .gitignore
├── .hermes/          — Cloud Agent runtime (Hermes: cron, config, skills, credentials)
├── intelligence/      — core GTM lead data (industrial + municipal verticals)
├── scripts/           — PPTX/deck generation scripts (26 files)
├── wiki/               — separate market-research knowledge base (unrelated to leads)
└── works/              — PPTX deliverables (10 files)
```

No README ever existed. No dependency manifests (requirements.txt/package.json) anywhere. No `.github/` directory or CI, ever. No GitHub Pages configured.

### `intelligence/` — the core data layer

```
intelligence/
├── industrial/
│   ├── schema.json          — JSON Schema for daily radar output (industrial)
│   ├── ind_latest.json      — current radar snapshot
│   ├── daily/                — dated radar reports (mixed naming: YYYY-MM-DD.json / ind_YYYY-MM-DD.json)
│   └── enriched/              — enrichment-stage output (indctx_*.json)
└── municipal/
    ├── schema.json          — JSON Schema for daily radar output (municipal)
    ├── latest.json          — current radar snapshot
    ├── daily/                — dated radar reports (YYYY-MM-DD.json)
    └── enriched/              — enrichment-stage output (ctx_*.json)
```

Key findings:
- Radar-stage and enrichment-stage are **already separated** by convention (enrichment files never mutate the daily radar file). Git history shows the team actively enforces this — a commit exists specifically to undo a case where a radar-only signal was mistakenly placed in `enriched/`.
- Both verticals' `schema.json` files are **documentary, not strictly enforced** — real data deviates in several ways (extra fields, `to_verify` type mismatch between verticals, `logic` vs `logic_rationale` field-name drift).
- **No qualification stage exists anywhere in the current data** — no PASS/REVIEW/REJECT field on any lead, confirmed by direct grep. `rejected_signals[]` exists per report but isn't linked to any `lead_id`.
- Lead IDs are mostly consistent (`IND-YYYYMMDD-NNN`, `OP-YYYYMMDD-NNN`) but have real, legitimate exceptions: the entire 2026-08-20 industrial batch uses 2-digit suffixes (`IND-20260820-06`, etc. — already verified and used downstream), one non-conforming agent-sourced ID (`H-10`), and municipal has a second prefix (`ML-YYYYMMDD-NNNN`) alongside `OP-`.
- Multi-agent provenance already exists informally in industrial enriched files: `agent_statistics` tracks 4 named agents (DuMate, WorkBuddy, Perplexity, Claude), pairwise overlap, cross-agent confirmation counts, merge counts. Municipal enriched files have much thinner provenance (single-string `discovered_by`, no `agent_statistics` block).

### `wiki/` — unrelated knowledge base

A separate Zettelkasten-style market-research wiki (2026 IE Expo, competitor tracking, PPT-deliverable notes), with its own schema conventions (`wiki/SCHEMA.md`), its own memory files (`wiki/_memories/`), served by a custom static-site generator. **Not part of the GTM lead pipeline.**

### `.hermes/` — the Cloud Agent runtime

"Hermes" is the runtime that actually executes the Cloud Agents against this repo — 3 scheduled cron jobs (mail-triage/task-cycling every 10-15 min, a daily filing monitor for a specific stock). This is the infrastructure referred to as "Cloud Agents" throughout the task brief.

**Critical finding**: `.hermes/.env` contains live API keys (MiniMax, Gemini, Tavily, email credentials, etc.) and **is committed to git** — the root `.gitignore` has an explicit negation (`!.hermes/.env`) forcing it to be tracked, annotated "完整恢复所需" (needed for full recovery). This is a real secrets-in-git exposure. See §5 (Risks) below — this is flagged, not remediated, in this task.

### `scripts/` and `works/`

26 PPTX/deck-generation scripts and their 10 output decks. Confirmed via grep that no script reads or writes `intelligence/*.json` — fully decoupled from the lead pipeline.

## 3. KEEP / REFACTOR / ADD / DEPRECATE

| Component | Action | What it does | Still useful? | Compatibility implications | Migration risk |
|---|---|---|---|---|---|
| `intelligence/{industrial,municipal}/schema.json` | **KEEP** | Documents (loosely) the daily radar output shape | Yes — actively referenced, matches most real data | None — untouched | None |
| `intelligence/{industrial,municipal}/{daily,enriched}/*.json` | **KEEP** | Real production GTM data, updated daily by Cloud Agents | Yes — this is the business | None — untouched | None |
| `wiki/` | **KEEP** | Separate market-research knowledge base | Yes, for its own purpose | None — untouched, unrelated system | None |
| `works/`, `scripts/` | **KEEP** | PPTX deck generation and outputs | Yes, for its own purpose | None — untouched, unrelated system | None |
| `.hermes/` (cron/config/skills/runtime) | **KEEP** (functionally untouched) | Runs the scheduled Cloud Agents against this repo | Yes — this is the automation layer | None — untouched | None |
| `.hermes/.env` committed secrets | **FLAG — no action taken** | Live API keys tracked in git | N/A — this is a risk, not a feature | Remediation (rotation + history rewrite) is destructive; explicitly out of scope for this task | High if exploited; zero if left alone (status quo) |
| Per-vertical schema vs. real-data drift (`logic`/`logic_rationale`, `to_verify` type mismatch) | **FLAG, not fixed** | Existing documentation gap | Low priority | None — pre-existing, low-risk | None (left alone) |
| Qualification stage (PASS/REVIEW/REJECT) | **ADD** | Did not exist | New capability needed for pipeline | Purely additive | None |
| Unified Lead/Evidence/Provenance/Enrichment/Pipeline-state contract | **ADD** | New `contracts/v1/schema.json` | Foundation for Weeks 2-4 | Additive layer, does not replace per-vertical schemas | None |
| Validator (`pipeline/validate.py`) | **ADD** | Strict mode (v1 contract) + legacy-compat mode (sanity-checks real data, never gates it) | Enables CI-style checks later | New tool, opt-in | None |
| Fixtures + tests (`tests/`) | **ADD** | Synthetic examples + pytest suite | Regression safety net | New, isolated | None |
| Docs (`docs/`) | **ADD** | Architecture, data contract, pipeline, open questions | Repo had zero engineering docs | New, isolated | None |
| Radar Agent | **explicitly NOT built** | — | Out of scope per task brief | — | — |
| Qualification scoring model | **explicitly NOT built** | — | Out of scope — business decision pending | — | — |
| Enrichment Agent | **explicitly NOT built** | — | Out of scope per task brief | — | — |
| CRM / SaaS UI / generic workflow engine | **explicitly NOT built** | — | Explicitly out of scope | — | — |

## 4. Target Architecture

```
Public / External Sources
          |
        RADAR  (Cloud Agents, existing — UNCHANGED)
          |
  intelligence/{industrial,municipal}/daily/*.json   (existing schema, UNCHANGED)
          |
    QUALIFICATION  (contracts/v1 Lead created here — NEW, additive)
          |
   PASS / REVIEW / REJECT
          |
      ENRICHMENT  (Cloud Agents populate contracts/v1 enrichment fields — existing agents, new target shape)
          |
  intelligence/{industrial,municipal}/enriched/*.json   (existing shape, UNCHANGED — still produced)
          |
     ORCHESTRATION  (dedup signaling via possible_duplicate/duplicate_of — NEW)
          |
      SALES_READY
          |
      ENGAGEMENT  (human sales — sales_feedback captured when available — NEW, optional)
```

`contracts/v1/` is a **downstream, additive layer**. Radar output continues to be produced exactly as before, in the existing per-vertical schemas. Nothing in `intelligence/` changes. A v1 Lead document is created once a lead advances into QUALIFICATION, referencing the original radar signal via `source`.

### GitHub's Role

GitHub remains the shared coordination layer between Cloud Agents (per the task brief's "Agent A → GitHub → Agent B → GitHub → Agent C/Human" model). This task does not introduce new infrastructure — no CI, no GitHub Pages, no new services — consistent with "prefer boring technology" and "GitHub already solves the current collaboration requirement."

### GitHub Pages

Not currently configured (confirmed via `gh api .../pages` → 404). Not introduced by this task. If a read-only machine/human interface is wanted later (e.g., serving `contracts/v1/schema.json` or a dashboard), that's a Week 5+ decision, not Week 1.

## 5. Critical Risk: `.hermes/.env` Secrets in Git

`.hermes/.env` contains live credentials (MiniMax, Gemini, Tavily API keys; email password) and is force-tracked in git via an explicit `.gitignore` negation. This means:
- Anyone with read access to the repository (including this clone) can read live API keys and an email password.
- If the repository is ever made public, forked, or shared beyond its current access list, these credentials are immediately exposed.

**This task does not remediate this** — key rotation and git-history rewriting are both destructive operations requiring explicit user decision, and are out of scope for a Week 1 engineering-foundation task. See `docs/OPEN_QUESTIONS.md` item 5.

## 6. Out of Scope (this task, per task brief)

Radar Agent, qualification scoring model, Enrichment Agent, Orchestration/merge engine, Engagement automation, generic Workflow Builder, Trigger→Condition→Action engine, Clay-style spreadsheet product, email/WeChat/SMS outreach automation, billing, credit system, multi-tenancy, provider marketplace, customer-facing SaaS, sophisticated UI, local Ollama migration, CRM integration.

## 7. Related Docs

- `docs/DATA_CONTRACT.md` — full v1 contract field reference
- `docs/PIPELINE.md` — pipeline state machine, validator CLI reference, legacy-compat findings table
- `docs/OPEN_QUESTIONS.md` — business-logic decisions not made by engineering
- `contracts/v1/README.md` — contract overview and versioning approach
