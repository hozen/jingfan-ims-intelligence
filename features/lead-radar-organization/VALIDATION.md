# Lead Radar Organization — Validation Record

## Current status

Documentation and archive migration completed. Existing production feeds and Pages inputs were not changed by this feature.

## Initial repository evidence

- Current branch: `feat/water-clay-self-hosted`.
- The worktree already contains multiple modified and untracked files. These are pre-existing and must be preserved.
- Pages workflow source at `.github/workflows/deploy-industrial-leads-pages.yml` deploys `customer/industrial-leads/` on pushes to `main` that touch that directory or the workflow.
- `.github/workflows/refresh-industrial-leads.yml` watches industrial/municipal `daily/` and `enriched/` paths and `customer/industrial-leads/pipeline-manifest.json`; it rebuilds `customer/industrial-leads/index.html` and `leads-data.json` and pushes generated changes.
- Therefore changing radar daily/enriched files can indirectly update and redeploy the Pages service. The planned archive-only migration must stay outside these trigger paths and avoid generated page files.
- The repo's `docs/architecture.md` and `docs/repository-audit.md` describe legacy schema drift, established latest-feed compatibility requirements, and a policy of additive canonicalization.
- The DuMate municipal bundle carries prompt v3.4.2; repository municipal prompt history includes v3.5.
- The live URL could not be fetched by the available web reader during this review. Live rendering/availability remains unverified.
- Before this feature started, the worktree already showed modifications under `customer/industrial-leads/`, industrial/municipal `daily/` and `enriched/`, and `intelligence/municipal/latest.json`. These pre-existing changes were left untouched. The full worktree must not be pushed as a batch without separately reviewing those paths, since existing workflows can refresh and deploy the leads page from them.

## Migration integrity results

- Both source ZIP hashes and all 31 entry hashes were rechecked against the import manifest.
- All 26 copied destinations matched their recorded destination hashes.
- All 5 copied JSON files parsed successfully.
- Ten DuMate task-ID/private-key-path references were redacted from imported Markdown; source and destination hashes are both recorded.
- No migrated file targets a `daily/` or `enriched/` workflow path. No task identifiers or host-specific key paths remain in the imported documentation/archive tree.
- No push or deployment was performed.

## Completed checks

| Check | Evidence | Result |
|---|---|---|
| Import provenance | `intelligence/shared/docs/dumate-import-manifest.json` records source archive hashes and all 31 source entries, including copied/excluded/curated/duplicate dispositions | Pass |
| Destination safety | Import aborted on any pre-existing destination with different content; destinations were absent before copying | Pass |
| Feed isolation | No imported files were written under either market's `daily/`, `enriched/`, or latest-feed paths | Pass |
| Pages isolation | No imported files were written under `customer/industrial-leads/` or `.github/workflows/` | Pass |
| Live Pages verification | Browser reader could not access the supplied URL; no push or deployment was performed | Unverified externally |
| Pre-existing worktree preservation | Feature wrote only new feature/docs/archive paths and one additive prompt-index paragraph; no pre-existing changed implementation file was a destination | Pass by scoped path review |

## Required checks after approved implementation

| Check | Evidence required | Status |
|---|---|---|
| Import provenance | Ledger covers every archive entry with source hash and disposition | Pass |
| Scope isolation | Changed paths limited to approved docs/archive paths and feature records | Pass |
| Feed compatibility | Feed/latest/enriched files were not write targets | Pass |
| Pages isolation | No Pages source, workflow, pipeline manifest, daily, or enriched paths were write targets | Pass |
| Dirty-worktree preservation | Feature used new paths and an additive docs index update; no pre-existing changed implementation file was used as a destination | Pass by scoped path review |
| Live Pages verification | Public URL retrieval | Unverified: reader could not access URL |
