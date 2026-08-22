# Repository audit — Task 001

Audit basis: `main` at `23fa316` on 2026-08-21, including repository history and GitHub repository settings.

## What exists

| Component | Current role | Classification | Compatibility / action | Migration risk |
|---|---|---|---|---|
| `intelligence/industrial/ind_latest.json` | Mutable industrial radar snapshot; current agent handoff. | KEEP | Preserve path and existing shape. Validate in compatibility mode. | High if renamed or made strict. |
| `intelligence/industrial/daily/` | Industrial history plus cumulative/review variants. | KEEP | Preserve IDs and files; document shape drift. | High if normalized in place. |
| `intelligence/municipal/latest.json` | Mutable municipal radar snapshot. | KEEP | Preserve path and existing shape. | High if renamed or made strict. |
| `intelligence/municipal/daily/` | Municipal dated radar history. | KEEP | Preserve all observed `OPP-*` and `OP-*` IDs. | High if IDs are regenerated. |
| `intelligence/*/schema.json` | Legacy radar report schemas. | REFACTOR (later) | Keep unchanged in Task 001. They describe intended report shapes but do not match every historical/current file. Version before tightening. | High: current reports contain enum/key drift. |
| `intelligence/industrial/enriched/indctx_latest.json` | Denormalized industrial lead/project/account/contact snapshot. | KEEP | Preserve path and collections; canonical v1 is parallel. | High: likely consumed by cloud agents. |
| `intelligence/municipal/enriched/ctx_latest.json` | Denormalized municipal enrichment snapshot. | KEEP | Preserve path and collections. | High: likely consumed by cloud agents. |
| Dated enrichment snapshots | Audit trail of enrichment evolution. | KEEP | Treat as immutable history. | Medium if rewritten/deduplicated. |
| `contracts/lead-v1.schema.json` | Canonical single-lead, stage-aware exchange contract. | ADD | Use for new contract experiments and future adapters. | Low while additive. |
| `scripts/validate_intelligence.py` | Human-readable canonical and legacy validation. | ADD | Run locally; CI is intentionally not added without workflow approval. | Low. |
| Synthetic fixtures/tests | Contract boundaries and regression safety. | ADD | Non-confidential examples only. | Low. |
| Presentation-generation scripts | Historical report/deck tooling; no direct intelligence pipeline logic. | KEEP | Do not refactor in this phase. Generated PPT/PDF files remain ignored. | Low for Task 001; dependencies are undocumented. |
| `.hermes/` config, skills, memory, cron | Existing Cloud Agent runtime/handoff context. | KEEP | Do not rewrite or replace. Runtime outputs remain ignored. | High if removed; secrets/config require separate security review. |
| `wiki/`, `works/` | Ignored local output locations. | DEPRECATE as interfaces | Do not use them for machine contracts. No tracked content currently establishes an interface. | Low. |
| GitHub Pages | No Pages site is configured. | DEPRECATE as current assumption | Do not claim Pages availability; reconsider only when a read-only publication need is approved. | None currently. |
| GitHub Actions | No workflows are configured. | ADD (future decision) | A validation workflow is useful later, but Task 001 avoids introducing an unreviewed automation dependency. | Low. |

## Observed compatibility facts

- Industrial daily files use `date`, `report_date`, or `run_date`; some are daily-only, some cumulative, and one is a Week 2 review artifact.
- Industrial suffix width varies (`IND-20260820-06` and `IND-20260821-001`). IDs must not be reformatted.
- Municipal opportunity IDs include `OPP-2026-08-10-001`, `OPP-20260819-001`, and `OP-20260820-001`. Enriched municipal lead IDs also use `ML-YYYYMMDD-NNNN`.
- Some industrial enrichment snapshots preserve older source IDs such as `ZJ-3`, `SMIC-1`, and `H-1`; these are provenance-bearing legacy identities, not candidates for silent replacement.
- Radar schemas and emitted data have drifted. Examples include industrial `logic` versus schema `logic_rationale`, missing `market_segment` in current signals, changed `top_5_match` keys, industry vocabulary expansion, and municipal optional fields added outside the original schema.
- Enrichment snapshots have no repository schema and combine master/current state, relationship graphs, agent statistics, quality notes, and next actions.
- The `latest` files duplicate dated snapshots by convention; no script currently verifies synchronization.
- Git history is the only built-in change/provenance mechanism. Record-level AI/model/run provenance is inconsistent in legacy data.
- No README, tests, package manifest, CI workflow, database, backend, or UI existed before Task 001.

## Current to target map

| Current | Target evolution |
|---|---|
| Report-level radar JSON | Preserve; later adapt selected opportunities into canonical Lead v1. |
| Snapshot-level enrichment JSON | Preserve; later ingest contributions incrementally against stable lead IDs. |
| Prose facts/inferences/unknowns and URL lists | Structured evidence IDs with source metadata and claim references. |
| Implicit stages (`opportunity_stage`, enrichment status) | Explicit lightweight `pipeline_stage` plus validated history. |
| Agent identity mostly in metadata/text | Append-only record-level provenance contributions. |
| Manual shape inspection | Dependency-free validator and synthetic regression suite. |

## Product Owner decisions required

1. Select the canonical municipal ID convention for newly created leads (`OPP`, `OP`, or `ML`) and define whether radar opportunity IDs and enriched lead IDs represent the same identity.
2. Approve qualification definitions and evidence thresholds for `PASS`, `REVIEW`, and `REJECT`; v1 intentionally has no score.
3. Decide whether and under what conditions `REJECTED` leads can be reopened.
4. Define the minimum evidence/readiness bar for `ENRICHED` and `SALES_READY`.
5. Define who may resolve evidence conflicts and whether human-reviewed values outrank sources or remain separate assertions.
6. Confirm which four latest feeds have external consumers and their refresh/atomicity expectations.
7. Decide whether GitHub Pages should be enabled and whether any intelligence can safely be public.
8. Approve a future CI workflow and branch protection policy.

## Risks and technical debt

- Existing schemas are not reliable validators for all files labelled by their directories; enforcing them now would break current cloud-agent outputs.
- A full compatibility scan of 35 legacy intelligence files reports 23 missing-ID errors and 5 malformed/empty URL warnings, concentrated in municipal reports dated 2026-08-10 through 2026-08-18. These historical files were not rewritten because assigning IDs or replacing unavailable URLs would invent provenance-sensitive data.
- Mutable latest snapshots can drift from dated files and have no atomic publishing check.
- Duplicate opportunity detection and legacy-to-canonical ID mapping remain manual.
- Legacy contacts and evidence do not consistently carry record-level source/provenance references.
- `.hermes/.env` is tracked by ignore exception. Its contents were not inspected in this audit; tracking environment files is a security risk that needs a separate, authorized secrets review.
- Presentation scripts have no declared dependency lock or automated verification.

## Recommended Task 002

Build a read-only adapter for one approved feed (recommended: industrial radar) that converts selected legacy signals into Lead Contract v1 without changing source files or IDs. Add golden tests, an explicit mapping report for fields that cannot be represented, and Product Owner-approved qualification handoff criteria. Do not implement qualification scoring or enrichment automation in that task.
