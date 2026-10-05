# Lead Radar Organization — Plan

## Status

Approved and implemented as a documentation and historical archive migration. Production feed integration remains out of scope.

## Steps

1. **Reconcile sources:** compared both ZIP manifests and repository market docs/feeds; recorded source ZIP hashes, entry hashes, dispositions, and destinations in `intelligence/shared/docs/dumate-import-manifest.json`.
2. **Resolve authority:** preserved municipal v3.5 as repository-current; stored DuMate v3.4.2 as historical. Stored industrial v4.1 as an exported task snapshot, not an unqualified current task promise.
3. **Organize documentation:** added market entry-point READMEs, shared context, and one shared evidence-check specification. Preserved reports and old script copies under dated market archive paths; excluded full memory dumps and runtime-specific configuration.
4. **Protect existing contracts:** all copied exports are outside production latest, `daily/`, and `enriched/` paths and outside Pages source/workflow paths.
5. **Review the resulting diff:** import operation checked that destination files did not already exist with different bytes; source disposition is recorded for every archive entry.
6. **Record validation:** static import integrity and path-isolation checks are recorded in `VALIDATION.md`. Live Pages fetching was unavailable, so external rendering remains unverified.

## Dependencies

- User review of `SPEC.md` (approved).
- Live-site access was unavailable; repository-side deployment isolation was checked instead.

## Not in this plan

Changing radar production feeds, refreshing `latest` snapshots, modifying the customer dashboard, changing Pages workflows, enabling a schedule, pushing to GitHub, or merging/deploying.
