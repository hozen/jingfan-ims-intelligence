# Lead Radar Organization — Specification

## Problem

DuMate is ending, and its industrial and municipal lead radar instructions, context, and export samples need a durable home in `jingfan-ims-intelligence`. The repository already has separate market data feeds, versioned prompt history, legacy schemas, a canonical Lead Contract, and a Pages-backed leads view. The migration must preserve those interfaces and must not unintentionally change the published web service.

## Intended outcome

Manage the industrial and municipal radars as separate, documented sources of lead intelligence in the existing repository, with shared guidance maintained once and clear provenance for any imported DuMate material.

## Scope

- Inventory the two DuMate export archives against tracked and untracked local repository content before copying files.
- Keep each market's discovery method, qualification rules, output examples, and prompt history in that market's existing `intelligence/<market>/docs/` area.
- Put genuinely shared radar rules in one shared documentation location; market documents link to them.
- Preserve raw market daily/latest feeds, identifiers, and established consumer paths. Do not rewrite old records to fit a schema.
- Treat archive examples and historical snapshots as archival material until date, identity, and duplicate status have been checked.
- Record import source, archive filename, source path, source date/version, destination, content hash, and disposition for every imported file.
- Reconcile prompt versions with repository history before designating an active prompt. The DuMate municipal v3.4.2 export is older than the repository's v3.5 prompt history and must not replace it.
- Keep this migration additive to the Lead Contract v1. A market-specific adapter may be proposed separately; it must not silently alter radar feeds or IDs.

## Explicit exclusions

- No changes to `.github/workflows/**`, `customer/industrial-leads/**`, `scripts/build_industrial_pipeline_view.py`, Pages configuration, or deployment behavior as part of the documentation/archive migration.
- No writes to established `latest` feeds or daily/enriched trigger paths during the archive-only migration. These paths can trigger the data refresh workflow and, through generated customer files, a Pages deployment.
- No conversion of industrial and municipal source reports into one common report schema.
- No credentials, private keys, local machine paths, personal memory dump, DuMate job identifiers, or platform-specific scheduler configuration in the repository.
- No push, deployment, or release action.

## Constraints and compatibility

- Preserve current production feed paths, including `intelligence/industrial/ind_latest.json` and `intelligence/municipal/latest.json`, unless a separate consumer migration is approved.
- Keep existing schemas and historical records unchanged; the repository audit documents schema drift and externally consumed feed risk.
- Keep GitHub Pages served files and its deployment workflow untouched. The in-repository page source is `customer/industrial-leads/`; the refresh workflow watches radar daily/enriched data and can regenerate these served files.
- Do not assume a clean worktree. Changes must be isolated from existing user modifications and must not overwrite them.
- The current checkout is `feat/water-clay-self-hosted` with pre-existing modifications and untracked artifacts. Work only in new feature files or explicitly reviewed destinations.

## Acceptance criteria

1. Industrial and municipal discovery methods, qualification stages, shared evidence rules, source materials, and active-vs-archived prompt versions are discoverable from repository documentation.
2. Each imported artifact has a recorded disposition and provenance; duplicate, stale, conflicting, or example-only data are not silently treated as current production data.
3. Existing latest-feed names, IDs, schemas, and report data remain unchanged by the migration.
4. No migration change touches Pages source files, deployment workflows, generated website data, or trigger paths that cause the lead refresh workflow to run.
5. A local diff/path audit demonstrates that only approved documentation and archive paths changed; web-service compatibility is reported as verified only to the extent supported by local workflow/source checks and an accessible live-site check.
6. The approved implementation has a validation record with the files inspected, paths changed, compatibility checks performed, outcomes, and any unavailable live checks clearly identified.

## Open decisions

- Whether to adapt new selected leads into Lead Contract v1 is a separate follow-on feature.
