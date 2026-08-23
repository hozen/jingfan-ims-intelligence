# Data contracts

`lead-v1.schema.json` is the canonical additive exchange contract for a single opportunity as it moves through the GTM pipeline. It does not replace the existing radar report schemas or the existing `latest.json`/`ind_latest.json`/`ctx_latest.json`/`indctx_latest.json` feeds.

Contract rules:

- `lead_id` is stable across every stage. Existing IDs are accepted; new industrial IDs should use `IND-YYYYMMDD-NNN` and new municipal IDs should follow the Product Owner-approved convention once selected.
- Unknown optional facts may be omitted or set to `null`. Contact channels pair a nullable value with `KNOWN`, `UNKNOWN`, `NOT_FOUND`, or `WITHHELD`.
- Evidence and provenance are append-only contributions. References use `evidence_id` and `contribution_id`; updates do not replace a whole lead.
- Qualification is a decision contract, not a scoring algorithm.
- Conflicting claims remain explicit in `conflicts` until resolved.
- `sales_feedback` is only a future-compatible object; Task 001 does not implement engagement analytics.

The validator implements the operational checks that JSON Schema alone cannot express, including reference integrity, duplicate evidence, contact consistency, and state transitions.
