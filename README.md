# Jingfan IMS GTM Intelligence

This private repository is the shared, evidence-oriented coordination layer for the Jingfan IMS GTM workflow:

`Radar -> Qualification -> Enrichment -> Orchestration -> Engagement`

Cloud agents continue to discover and research opportunities. The repository preserves their structured outputs, stable lead identities, evidence, and provenance so later agents and humans can validate and extend the same opportunity without replacing its history.

## Current interfaces

- `intelligence/industrial/ind_latest.json` and `intelligence/industrial/daily/*.json`: industrial radar reports.
- `intelligence/municipal/latest.json` and `intelligence/municipal/daily/*.json`: municipal radar reports.
- `intelligence/industrial/enriched/indctx_latest.json`: industrial enrichment snapshot.
- `intelligence/municipal/enriched/ctx_latest.json`: municipal enrichment snapshot.
- `intelligence/*/schema.json`: legacy radar report schemas.
- `contracts/lead-v1.schema.json`: additive canonical Lead Contract v1 for new stage-aware exchange.

Do not rename or rewrite the four latest feeds without a consumer migration plan. GitHub Pages is not currently configured and GitHub Actions currently has no workflows; files are consumed directly through GitHub/repository access.

## Validate and test

Requires Python 3.11+ and no third-party packages.

```bash
python -m unittest discover -s tests -v
```

Validate all synthetic fixtures plus the four current latest feeds:

```bash
python scripts/validate_intelligence.py
```

Validate selected files:

```bash
python scripts/validate_intelligence.py path/to/lead.json
```

See `docs/architecture.md`, `docs/pipeline.md`, `docs/data-contract.md`, and `docs/repository-audit.md` before changing interfaces or business-stage semantics.

For architecture/product review, start with `docs/task-001-review.md` and open `docs/ims-gtm-mvp-map.html` for the Chinese visual report-out.

For task-by-task customer deliverables, acceptance gates, evidence, and next-step readiness, open `docs/task-delivery-dashboard.html`.
