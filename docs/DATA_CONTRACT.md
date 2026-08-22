# Data Contract — iMS GTM Intelligence Lead v1

Full field reference for `contracts/v1/schema.json`. For the "why", see `contracts/v1/README.md`. For the pipeline state machine, see `docs/PIPELINE.md`.

## Why a New Contract Layer

The existing per-vertical radar schemas (`intelligence/{industrial,municipal}/schema.json`) describe **radar-stage output only** — they have no concept of qualification, enrichment status, or pipeline stage. As leads advance through Qualification → Enrichment → Orchestration → Engagement, a richer, unified representation is needed that:

1. Works the same way regardless of vertical (industrial vs municipal)
2. Captures evidence, provenance, and confidence at every stage
3. Supports multiple agents contributing to the same lead
4. Never requires fabricating data to satisfy the schema

Rather than retrofitting this onto the two divergent radar schemas, `contracts/v1/schema.json` is a **new, additive layer** consumed downstream of radar.

## Design Principles

- **Evidence-based**: every claim traces to a source
- **UNKNOWN over fabrication**: `"UNKNOWN"` / empty arrays are valid; invented data is not
- **Backward compatible**: legacy lead IDs (including non-standard ones) remain valid
- **Additive evolution**: `extensions` escape hatch avoids forking the schema for experiments
- **No premature scoring**: qualification decision is stored, not computed
- **Vertical flexibility**: industrial and municipal keep their native vocabularies (no forced unification of priority scales or stage names)

## Entity Reference

### Root: Lead

| Field | Type | Required | Notes |
|---|---|---|---|
| `contract_version` | `"v1"` | yes | enables v2+ evolution |
| `lead_id` | string | yes | loose — see "Lead ID Compatibility" below |
| `vertical` | `industrial` \| `municipal` | yes | |
| `pipeline_stage` | enum (10 values) | yes | see `docs/PIPELINE.md` |
| `company` | string | yes | may be `"UNKNOWN"` |
| `source` | `source_reference` | yes | traceability to the originating radar file |
| `evidence` | `evidence` | yes | facts/inferences/unknowns |
| `pipeline_history` | `pipeline_transition[]` | yes, ≥1 item | audit trail of stage transitions |
| `qualification` | `qualification` | conditional | required once `pipeline_stage` ≥ QUALIFICATION |
| `enrichment` | `enrichment` | conditional | required once `pipeline_stage` ≥ ENRICHMENT |
| `provenance` | `provenance_entry[]` | no | general actor/action log |
| `sales_feedback` | `sales_feedback` | no | never required, even at ENGAGEMENT |
| `possible_duplicate` / `duplicate_of` | bool / string | no | orchestration-stage dedup signal |
| `created_at` / `updated_at` | date-time | no | |
| `extensions` | object | no | unvalidated escape hatch |

### `source_reference`
Links back to the legacy radar file: `vertical`, `source_report_id`, `source_signal_id` (required); `source_file`, `retrieved_at` (optional).

### `evidence`
`facts[]`, `inferences[]`, `unknowns[]` (all required, may be empty — mirrors the existing industrial radar schema exactly). Optional `items[]` (structured `evidence_item` objects) and `source_urls[]`.

### `evidence_item`
`type` (FACT/INFERENCE/UNKNOWN/AGENT_DISCOVERY/PUBLIC_RECORD/HUMAN_VERIFIED) and `detail` are required. Optional `source`, `source_agent`, `source_url`, `date`, `confidence` (HIGH/MEDIUM/LOW/UNKNOWN). **Conflicting evidence items are stored side by side, never auto-resolved** — see `tests/fixtures/case_f_conflicting_evidence.json`.

### `qualification`
`decision` (PASS/REVIEW/REJECT) is the only required field. Optional `decided_at`, `decided_by`, `reason`, `confidence`, `notes`. **Deliberately has no score, weight, or rule fields** — it records a decision once made; how the decision is reached is a Product Owner call (see `docs/OPEN_QUESTIONS.md`).

### `enrichment`
`status` (NOT_STARTED/IN_PROGRESS/COMPLETED/AGENT_DISCOVERED) is required. Optional sub-objects: `company_intelligence`, `project_intelligence[]`, `organization_relationships[]`, `contacts[]`, `missing_roles[]`, `next_best_actions[]`, `enrichment_sources[]`, `agent_contributions[]`.

- `company_intelligence`: `legal_name` required; `aliases`, `industry`, `location`, `ownership_type`, `water_system_ownership` (A/B/C/D/N-A), `notes` optional.
- `project`: `project_id`, `name`, `status` required (`status` stays free text — no forced normalization across verticals); optional `normalized_stage` (industrial's 7-stage vocabulary, left unpopulated by default), `epc_contractor`, `design_institute`, `estimated_time_window`, `source_lead_ids[]` (dedup signal).
- `organization_relationship` + `org_role`: unifies industrial's nested owner/EPC/design-institute model and municipal's flat dict into one shape — `owner[]`, `epc[]`, `design_institute[]`, `other[]` arrays of `{role_exists, role_title, person, contact_id, organization_name}`.
- `contact`: `contact_id`, `name`, `discovered_by` required (`discovered_by` is a **mandatory array** in v1 — normalizes the legacy string/array inconsistency between verticals). Role-oriented (A/B/C/D classification), not executive-title-oriented. `phone[]`/`email[]` as `contact_channel` objects. `evidence_score`/`commercial_relevance_score` (0-100). `human_verified`, `verification_status`, `cross_agent_confirmation`, `possible_duplicate`, `conflict_note` all preserved from the existing informal model.
- `agent_contribution`: tracks which agent contributed what to a given lead — supports N agents on 1 Lead (Radar Agent + Qualification Agent + multiple Enrichment Agents + Human Review, all on the same Lead, per the task brief).

### `provenance_entry`
General audit log, distinct from `pipeline_history`: `actor`, `actor_type` (AGENT/HUMAN/SYSTEM), `action`, `timestamp` required.

### `pipeline_transition`
`stage`, `entered_at` required; optional `actor`, `notes`. See `docs/PIPELINE.md` for the transition graph these are validated against.

### `sales_feedback`
Deliberately thin — `engaged_at`, `sales_owner`, `outcome` (IN_PROGRESS/WON/LOST/NO_RESPONSE/DISQUALIFIED_BY_SALES/OTHER), `feedback_notes`, `next_step`. Not a CRM opportunity object. Designed so a richer outcome taxonomy (ACCEPTED/INFORMATION_INSUFFICIENT/CUSTOMER_MISMATCH/PROJECT_TOO_LATE/CONTACT_INCORRECT/ALREADY_AWARDED/NO_IMS_NEED, as sketched in the task brief) can be added later without breaking existing documents — see `docs/OPEN_QUESTIONS.md`.

## Lead ID Compatibility

`lead_id` is `{"type": "string", "minLength": 1}` at the schema level — **no regex pattern is enforced**, specifically so all of the following (confirmed present in real data) validate without modification:

| Format | Example | Source |
|---|---|---|
| `IND-YYYYMMDD-NNN` (3-digit) | `IND-20260821-001` | Industrial standard |
| `IND-YYYYMMDD-NN` (2-digit) | `IND-20260820-06` | Legacy 2026-08-20 batch, already verified/used downstream |
| `OP-YYYYMMDD-NNN` | `OP-20260821-005` | Municipal standard |
| `ML-YYYYMMDD-NNNN` | `ML-20260821-0006` | Municipal alternative prefix |
| `H-N` | `H-10` | Agent-sourced, outside the radar pipeline |

Format conformance is checked only by `pipeline/validate.py` (as a WARNING, never an error) — see `docs/PIPELINE.md` for the exact severity table.

## Versioning Strategy

- `contract_version: "v1"` is a `const` on every document.
- Non-breaking additions (new optional fields) can be added to v1 in place.
- Breaking changes (new required fields, removed fields, changed types) require a v2 schema; v1 documents remain valid indefinitely.
- Experimental or vertical-specific fields that don't yet warrant a schema change go in `extensions` (unvalidated).

## Worked Examples

See `tests/fixtures/case_a_valid_radar_lead.json` through `case_i_duplicate_opportunity_different_sources.json` for complete worked examples of each pipeline stage and edge case (conflicting evidence, missing contacts, multi-agent enrichment, duplicate detection).
