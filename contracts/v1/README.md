# iMS GTM Intelligence Lead Contract — v1

## What This Is

A unified JSON Schema (Draft 2020-12) for representing GTM leads at the qualification, enrichment, orchestration, and engagement stages. Designed to be **additive** — layered on top of, not replacing, the existing per-vertical radar schemas in `intelligence/{industrial,municipal}/schema.json`.

The contract encodes:
- **Evidence-first architecture** — facts, inferences, unknowns; no fabrication; UNKNOWN over hallucination
- **Pipeline state** — 10-stage model from RADAR through ENGAGEMENT, with explicit transition rules
- **Backward-compatible lead IDs** — accepts IND-YYYYMMDD-NNN (3-digit), IND-YYYYMMDD-NN (2-digit, legacy 2026-08-20 batch), OP-/ML-YYYYMMDD-* (municipal), and even non-standard agent-sourced formats
- **Multi-agent provenance** — tracks which agents contributed what, marks cross-agent confirmations, dedup signals
- **Staged enrichment** — company intelligence, project details, EPC/design-institute organizational relationships, role-oriented contacts
- **Qualification without scoring** — contract stores the eventual decision (PASS/REVIEW/REJECT), not the mechanism for reaching it — scoring model design is out of scope for Week 1

## Relationship to Existing Radar Schemas

Radar-stage leads continue to be produced by Cloud Agents in their native format:
- `intelligence/industrial/daily/*.json` → industrial radar schema
- `intelligence/municipal/daily/*.json` → municipal radar schema

These schemas are **not touched** and remain authoritative for radar-stage output.

Once a lead advances past RADAR (into QUALIFICATION), a v1 Lead contract document is created or updated, embedding the original radar signal as `source` metadata and adding downstream intelligence as qualification/enrichment/orchestration progresses.

## Design Principles

- **Evidence-based**: every claim is traceable to a source (URL, agent, public record, human verification)
- **UNKNOWN over fabrication**: missing contact info is recorded as `"UNKNOWN"` or `not_found` rather than invented
- **Backward compatible**: existing lead IDs remain valid; validator warns on non-standard formats but never rejects
- **Additive evolution**: v1 can grow to v2 without breaking existing v1 documents (via `extensions` escape hatch if needed)
- **No premature optimization**: qualification scoring model, revenue estimates, probability weighting — all explicitly out of scope for Week 1
- **Vertical flexibility**: each market (industrial/municipal) preserves its native priority/stage/industry vocabularies; no forced unification yet

## Key Fields

| Field | Type | Required | Purpose |
|---|---|---|---|
| `contract_version` | string | ✓ | Always `"v1"` — enables future v2 evolution |
| `lead_id` | string | ✓ | Stable, unique lead identifier (backward-compatible with legacy ID formats) |
| `vertical` | enum | ✓ | `"industrial"` or `"municipal"` |
| `pipeline_stage` | enum | ✓ | One of 10 stages: RADAR, QUALIFICATION, QUALIFIED, REVIEW, REJECTED, ENRICHMENT, ENRICHED, ORCHESTRATION, SALES_READY, ENGAGEMENT |
| `company` | string | ✓ | Account/company name (may be `"UNKNOWN"`) |
| `source` | object | ✓ | Traceability: links back to the radar file and original signal/opportunity ID |
| `evidence` | object | ✓ | Facts, inferences, unknowns — core claim support |
| `pipeline_history` | array | ✓ | Append-only log of stage transitions — used to validate state machine |
| `qualification` | object | conditional | Required once stage ≥ QUALIFICATION; stores decision (PASS/REVIEW/REJECT) + reason + confidence |
| `enrichment` | object | conditional | Required once stage ≥ ENRICHMENT; contains company/project/contact/org intelligence |
| `provenance` | array | optional | General audit log (distinct from pipeline_history) |
| `sales_feedback` | object | optional | Sales outcome (WON/LOST/NO_RESPONSE), only filled post-ENGAGEMENT |
| `extensions` | object | optional | Escape hatch for experimental/vertical-specific fields (unvalidated, intentional) |

## The `extensions` Escape Hatch

If you need to store data not yet covered by the v1 schema:
```json
{
  "...rest of lead...": "...",
  "extensions": {
    "my_custom_field": "any value",
    "experimental_scoring": {"model": "v0.1", "score": 75},
    "vertical_specific": {"industrial_only_thing": "..."}
  }
}
```

Contents of `extensions` are not validated by the schema and not part of the official contract. Use this instead of forking the schema or creating a v1.1 patch. When the field stabilizes, we can promote it to the top level in v2.

## Validator and Tests

- **`pipeline/validate.py`** — validates v1 Lead documents in two modes:
  - `--mode strict`: full JSON Schema validation against this schema, plus state-transition graph checks
  - `--mode legacy-compat`: sanity checks against real `intelligence/**/*.json` files (warns on inconsistencies but never rejects legacy data)
- **`tests/`** — pytest suite covering schema validity, state transitions, evidence handling, multi-agent provenance, and backward compatibility with existing lead IDs
- **`tests/fixtures/`** — 9 synthetic, non-confidential example leads (cases A–I) demonstrating the contract in practice

Run tests with:
```bash
pip install -r pipeline/requirements.txt
pytest tests/ -v
```

See `docs/PIPELINE.md` for the full validator CLI reference.

## Out of Scope — Week 1

- **Qualification scoring model** — the contract stores the decision; how to compute it is a business/product decision, not an engineering one yet
- **Radar Agent** — continue using existing Cloud Agent radar workflows
- **Enrichment Agent** — continue using existing Cloud Agent enrichment workflows
- **Orchestration/merge logic** — contract supports dedup signaling (`possible_duplicate`, `duplicate_of`); orchestration orchestration rules are future work
- **Engagement automation** — sales handoff remains manual; feedback loop exists but is not automated
- **CRM / SaaS / workflow engine** — this is GTM intelligence infrastructure, not a product for external customers

## Backward Compatibility

- Existing `intelligence/{industrial,municipal}/schema.json` files remain unchanged and authoritative for radar-stage output
- Existing lead IDs (including non-standard `H-10`, 2-digit-suffix `IND-20260820-06`, etc.) are preserved and accepted
- Cloud Agent workflows continue unchanged; they produce radar output exactly as before
- v1 contract documents are created/updated additively downstream; no in-place mutation of legacy files

## Next Steps

See `docs/DATA_CONTRACT.md` for full field reference and design rationale. See `tests/fixtures/` for worked examples of each pipeline stage.

For open questions — qualification mechanism, unification of industrial/municipal vocabularies, `.hermes/.env` secrets exposure — see `docs/OPEN_QUESTIONS.md`.
