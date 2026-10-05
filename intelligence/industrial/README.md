# Industrial Opportunity Radar

Industrial radar discovery, qualification, and report data are maintained separately from the municipal radar. Shared iMS GTM context and evidence rules are in [`../shared/docs/README.md`](../shared/docs/README.md).

## Method and specifications

- DuMate task snapshot: [`docs/prompts/main_prompt_v4.1.md`](docs/prompts/main_prompt_v4.1.md) (exported 2026-09-29; check against the next approved task revision before treating it as current).
- Industrial qualification and output specifications: [`docs/specs/`](docs/specs/).
- The prompt runs three discovery engines: industrial compliance; industrial project/CapEx; and pre-tender early signals. It emphasizes early-stage opportunities, evidence quality, VM/PULL qualification, influence window and entry timing, plus handoff roles.

## Production data contract

- Dated reports: [`daily/`](daily/).
- Current snapshot: [`ind_latest.json`](ind_latest.json). Keep this path and its shape stable for current consumers.
- Enrichment: [`enriched/`](enriched/).
- Existing files retain their historical IDs and shapes; see the repository audit before changing feeds or schemas.

## DuMate source archive

- [`docs/dumate/README.source.md`](docs/dumate/README.source.md) describes the source bundle.
- [`archive/dumate-2026-09-29/`](archive/dumate-2026-09-29/) contains report examples and historical script copies. Do not execute archived scripts as production tooling or treat `examples/latest.json` as the live snapshot.
- The export README records a conflict over whether to regenerate `latest.json`. The repository contract uses `ind_latest.json`; do not create or replace a second industrial latest feed based only on that historical note.

## Important boundary

Do not put archival reports in `daily/` or `enriched/`: those paths feed current downstream processing and can refresh the Pages-backed leads view. Only publish new production data there through the normal review and validation path.
