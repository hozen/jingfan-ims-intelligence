# Open Questions — Product Owner Decisions Needed

Per the engineering mandate for this task: business logic, GTM methodology, qualification criteria, ICP, scoring models, sales process, and enrichment strategy are Product Owner decisions, not engineering decisions. Where the contract design surfaced a business-logic call, it was deliberately left as a stored slot rather than a computed default. This document lists every such call.

## 1. Qualification Scoring Mechanism

The v1 contract's `qualification` object stores a **decision** (PASS/REVIEW/REJECT) plus reason/confidence/decided_by — it does not define **how** that decision is computed. No scoring model, weighting, or rule engine exists. The task brief lists candidate dimensions (ICP Fit, Pain/Need, Timing, IMS Fit, Commercial Relevance) but explicitly says not to build a sophisticated scoring algorithm yet, since "the business rules are still being validated."

**Decision needed**: How should qualification decisions actually be made in the near term (manual? Cloud-Agent-assisted with a simple checklist? something else)? This determines Week 2 scope.

## 2. Should REJECTED -> REVIEW Reopening Be Allowed?

The transition graph (`docs/PIPELINE.md` §3) allows a REJECTED lead to reopen into REVIEW. This was included as a reasonable default (common in sales practice — new evidence can revive a previously rejected opportunity) but disallowing it entirely is equally defensible.

**Decision needed**: Confirm whether REJECTED leads should ever be reopenable, and if so, under what conditions (new evidence required? time limit? human approval only?).

## 3. Should Municipal and Industrial Vocabularies Be Unified?

Two places where the two verticals use genuinely different vocabularies, left un-unified in v1:

- **Project stage**: industrial uses a 7-value English enum (Early Trigger -> ... -> Completed/Too Late); municipal uses free-text Chinese stage descriptions. The contract's `project.status` stays free text for both, with an optional unused `normalized_stage` slot.
- **Priority/scoring**: industrial uses P1/P2/P3; municipal uses 一级/二级/三级 plus a 0-100 numeric score. No unified cross-vertical priority field was created — each vertical's native value passes through opaquely.

**Decision needed**: Is a unified vocabulary/scale wanted for cross-vertical reporting or prioritization? If so, what's the mapping (this is a business judgment about relative severity/urgency across two different markets, not an engineering one)?

## 4. `.hermes/.env` Committed Secrets

`.hermes/.env` (live API keys, email password) is committed to git via an explicit `.gitignore` negation. This is a real security exposure, flagged prominently in `docs/ARCHITECTURE.md` §5 but **not remediated** in this task — rotating credentials and rewriting git history are both destructive, high-blast-radius operations that need explicit authorization.

**Decision needed**: Should these credentials be rotated and removed from git history? If so, this should be a dedicated, carefully-scoped follow-up task (not bundled into further GTM-pipeline work), since it affects the running Hermes agent's ability to operate.

## 5. Does `contracts/v1` Become the Agents' Direct Write Target?

Currently, `contracts/v1/schema.json` is a downstream layer: Cloud Agents continue producing radar/enrichment output in the existing per-vertical formats, and (in a future week) something converts that into v1 Lead documents. An alternative future is that Cloud Agents eventually write v1 Lead documents directly, replacing the per-vertical schemas as the write target.

**Decision needed**: Is the long-term intent to migrate Cloud Agent output to write v1 directly, or to keep v1 as a permanent downstream normalization layer? This affects how much investment goes into the conversion step vs. agent prompt/output changes in later weeks.

## 6. Sales Feedback Ownership and Cadence

The contract has a `sales_feedback` slot (outcome, notes, next_step) but Engagement automation is explicitly out of scope. Someone (a human, presumably) needs to actually fill this in after sales engagement happens.

**Decision needed**: Who updates `sales_feedback`, how often, and through what mechanism (manual JSON edit? a future lightweight form? something else)? Also: should the outcome enum match the task brief's suggested taxonomy exactly (ACCEPTED / INFORMATION_INSUFFICIENT / CUSTOMER_MISMATCH / PROJECT_TOO_LATE / CONTACT_INCORRECT / ALREADY_AWARDED / NO_IMS_NEED / OTHER) rather than the current placeholder (IN_PROGRESS/WON/LOST/NO_RESPONSE/DISQUALIFIED_BY_SALES/OTHER)? Both are compatible with the schema's `additionalProperties: false` pattern once decided — but the exact production vocabulary is a sales-process decision.

## 7. `report_id` Format Inconsistency

Radar `report_id` values are inconsistent across time and vertical (dashed vs undashed dates, version suffixes like `-wk2-review`, `-v32`). This was noted during the audit and deliberately left alone (`docs/PIPELINE.md` §5 — "silently ignored" in the validator).

**Decision needed**: Confirm this is acceptable to leave alone indefinitely, or whether a `report_id` convention should be standardized going forward (this would be a low-risk, low-priority cleanup, not blocking).

## 8. Legacy Schema Drift (`logic` vs `logic_rationale`, etc.)

The existing `intelligence/industrial/schema.json` requires `logic_rationale`, but real data consistently uses `logic` instead. This and a few similar drifts (documented in `docs/ARCHITECTURE.md`) were left as-is and flagged as WARNING by the validator rather than fixed.

**Decision needed**: Should the legacy `schema.json` files be updated to match actual agent output (i.e., fix the schema), or should agent prompts be updated to match the schema (i.e., fix the data)? Either is a reasonable choice; picking one is a small but real decision affecting Cloud Agent instructions.
