# Municipal Public Signal Radar

Municipal radar discovery, qualification, and report data are maintained separately from the industrial radar. Shared iMS GTM context and evidence rules are in [`../shared/docs/README.md`](../shared/docs/README.md).

## Method and specifications

- Repository prompt lineage: [`docs/README.md`](docs/README.md). The repository contains municipal prompt v3.5.
- DuMate's v3.4.2 task snapshot and its v3.3/v3.4 materials are retained under [`docs/archive/dumate-2026-09-29/`](docs/archive/dumate-2026-09-29/) as historical references; they do not supersede v3.5.
- The municipal method uses six discovery radar families, then qualification and public-source enrichment. The action triad, project stage, timing window, logic-chain check, and municipal/industrial boundary are explicit gates.

## Production data contract

- Dated reports: [`daily/`](daily/).
- Current snapshot: [`latest.json`](latest.json). Preserve the existing filename, IDs, and shape for current consumers.
- Enrichment: [`enriched/`](enriched/).
- Keep municipal reports and IDs distinct from industrial reports; do not normalize old records in place.

## DuMate source archive

- [`archive/dumate-2026-09-29/`](archive/dumate-2026-09-29/) contains the 2026-09-28 report examples and a historical merge-script copy. These are reference materials, not production inputs.
- Keep archive reports out of `daily/` and `enriched/`. Changes to those paths can refresh the Pages-backed leads view through the repository workflow.
