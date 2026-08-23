# Data Contract v1

The canonical unit is one Lead/Opportunity in `contracts/lead-v1.schema.json`. It is additive: current daily and latest report documents remain supported.

## Identity and optionality

`lead_id`, `lead_type`, timestamps, stage, evidence collection, and provenance collection form the required envelope. A lead's ID never changes with its stage. The contract accepts observed industrial IDs with one-to-four digit suffixes and observed municipal `OPP`, `OP`, and `ML` forms. It also tolerates historical prefixed identifiers so existing records are not silently renumbered.

Company, project, and signal objects are optional because a legitimate public signal may not identify all three. Unknown optional values can be omitted or `null`; agents must not synthesize values to satisfy validation.

## Evidence

Each evidence item has a stable `evidence_id`, source metadata, HTTP(S) URL, retrieval time, summary, and confidence. Published time and verbatim text are optional. Claims in qualification, enrichment, provenance, and conflict objects refer to evidence IDs. Identical URL-and-summary pairs produce a warning.

## Provenance

`provenance` is an append-only list of contributions, not one owner per lead. Each contribution identifies whether it came from AI, a human, a system, or an import, plus agent, run, generation time, optional model and prompt version, and evidence references. Human-reviewed contributions therefore remain distinguishable from AI-generated contributions.

## Qualification

The required decision is `PASS`, `REVIEW`, or `REJECT`, with reasoning, evidence references, confidence, time, and provenance. The five future dimensions are optional narrative fields. No BANT assumption or opportunity-score formula exists in v1.

Decision and pipeline state are cross-validated: `PASS` requires `QUALIFIED` or a later qualified-path stage, `REVIEW` requires `REVIEW`, and `REJECT` requires `REJECTED`. Every canonical lead must include a non-empty, contiguous `pipeline_history` beginning with `START -> RADAR`; its terminal state must equal `pipeline_stage`.

## Enrichment

Enrichment holds project-related organizations and role-oriented contacts. Organization relationships include owner, facility, EPC, design institute, system integrator, and engineering contractor. Contact phone and email values pair with explicit availability states. `NOT_FOUND` and `UNKNOWN` require `null`; they are not placeholder strings.

`PENDING`, `IN_PROGRESS`, and `PARTIAL` enrichment are valid only in `ENRICHMENT` or `REVIEW`. `COMPLETE` is valid only from `ENRICHED` onward. The validator also rejects unknown properties consistently with the schema and reports malformed nested structures as findings rather than raising an exception.

## Merge principles

V1 defines representation and validation, not a generic merge engine:

1. Append stronger/new evidence; do not silently overwrite existing claims.
2. Keep unresolved alternatives in `conflicts`, each with evidence references.
3. Keep all contributing agents/runs in `provenance`.
4. Link suspected duplicates with `duplicate_of`; do not auto-merge or create a replacement ID.
5. Distinguish human contributions with `generated_by: HUMAN`.
6. Prefer absent/null plus status over fabricated completeness.

The future `sales_feedback` object supports the agreed outcome vocabulary without implementing analytics or engagement automation.
