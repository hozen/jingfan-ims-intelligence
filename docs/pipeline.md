# GTM pipeline state model

The model is an explicit state contract, not a workflow engine.

| State | Meaning | Normal next state(s) |
|---|---|---|
| `RADAR` | A potential public signal was discovered. | `QUALIFICATION`, `REJECTED` |
| `QUALIFICATION` | Evidence is being assessed for further investment. | `QUALIFIED`, `REVIEW`, `REJECTED` |
| `QUALIFIED` | Qualification result is `PASS`. | `ENRICHMENT`, `REJECTED` |
| `REVIEW` | Evidence or a decision requires human/agent review. | `QUALIFICATION`, `QUALIFIED`, `REJECTED` |
| `ENRICHMENT` | Project, ecosystem, and role-oriented contact research is active. | `ENRICHED`, `REVIEW`, `REJECTED` |
| `ENRICHED` | The current enrichment pass is complete enough for consolidation. | `ORCHESTRATION`, `REJECTED` |
| `ORCHESTRATION` | Evidence, conflicts, relationships, and readiness are being consolidated. | `SALES_READY`, `REVIEW`, `REJECTED` |
| `SALES_READY` | A human sales workflow can act on the package. | `ENGAGEMENT`, `REVIEW`, `REJECTED` |
| `ENGAGEMENT` | Human-led sales engagement is underway. | `REVIEW`, `REJECTED` |
| `REJECTED` | Evidence invalidated or disqualified the opportunity. | none in v1 |

Every lead starts with `START -> RADAR`. `pipeline_history` must be contiguous, its final state must equal `pipeline_stage`, and every transition records time and provenance. A qualification `REJECT` maps to pipeline state `REJECTED`; this avoids ambiguity between a decision verb and a durable state.

Stage boundaries:

- Radar discovers; it does not perform deep contact enrichment.
- Qualification decides `PASS`, `REVIEW`, or `REJECT`; v1 defines no numeric scoring logic.
- Enrichment researches company/project structure, EPC/ecosystem relationships, and relevant operational roles.
- Orchestration consolidates without silently overwriting evidence or unresolved conflicts.
- Engagement remains human-led; no autonomous outreach is authorized.

Reopening a rejected lead is intentionally undefined pending Product Owner policy.
