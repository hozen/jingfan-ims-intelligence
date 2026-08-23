# Codex Prompt — Fix Task 001 Final Gate

Work in the local repository `D:\OneDrive\文档\ChatGPT\ims-gtm`.

## Objective

Fix the remaining Task 001 closure blockers found in the final review. Do not start Task 002.

Task 001 is already merged into `main`, but its final acceptance status remains `FAIL` until the validator and customer dashboard are corrected.

## Current repository state

- Branch: `main`
- Current merge commit: `d8232a4` — `Merge Task 001 closure gates`
- Task 001 closure commit: `be54a9e` — `Close Task 001 architecture gate`
- Working tree was clean at review time.
- Existing Radar, Enrichment, historical intelligence, and agent handoff files must not be rewritten or renamed.

## Blocking issue 1 — validator must not crash on malformed transitions

In `scripts/validate_intelligence.py`, `validate_transition()` can raise `TypeError` when `pipeline_history[].from` or `pipeline_history[].to` is an unhashable value such as an object or array.

Example invalid input:

```json
{
  "pipeline_history": [
    {"from": null, "to": {}, "at": "2026-08-21T08:00:00+08:00", "provenance_ref": "run-a"}
  ]
}
```

Required behavior:

- Return a human-readable `ERROR` finding.
- Never raise a Python exception for malformed transition values.
- Preserve the existing valid transition behavior.

Add a regression test that directly covers object/array values in `from` and `to`.

## Blocking issue 2 — validator must enforce required nested fields

The JSON Schema requires these fields, but the dependency-free validator currently allows empty objects:

- `company: {}` must require `company_name`
- `project: {}` must require `project_name`
- `signal: {}` must require `signal_type` and `signal_description`

Implement the smallest consistent fix in the validator. Keep optional objects optional; only validate required fields when the object is present.

Add regression tests for all three cases.

Also verify that malformed types still produce findings rather than exceptions.

## Dashboard and closure documentation

Update `docs/task-delivery-dashboard.html` so it does not claim final `PASS` until these fixes and verification are complete.

After successful verification, update it to show:

- `PASS`
- 21 or more tests, according to the actual test count
- Task 001 merged into `main`
- The final validator gate is closed
- Task 002 is authorized only for the previously defined read-only Industrial Radar adapter

Update `docs/task-001-closure.md` only after the fixes pass. Record the actual final test count and verification results. Do not leave “PASS” language if any required check fails.

## Required verification

Run from the repository root:

```bash
python -m unittest discover -s tests -v
python scripts/validate_intelligence.py
python scripts/validate_intelligence.py intelligence
```

Expected results:

- All tests pass.
- Canonical fixtures and four latest feeds: 0 errors, 0 warnings.
- Historical directory scan: legacy defects may remain, but the count must be reported accurately and no validator exception may occur.
- Working tree is clean after commit.

## Scope restrictions

Do not:

- Start Task 002.
- Build an adapter, scoring engine, enrichment automation, CRM integration, outreach workflow, database, SaaS layer, or provider abstraction.
- Rewrite historical intelligence data.
- Remove or weaken existing regression tests.
- Claim `PASS` based only on the normal happy-path fixtures.

## Final response

Report:

1. Files changed
2. Exact fixes made
3. Test count and results
4. Canonical and historical validation results
5. Updated dashboard/closure status
6. Whether Task 001 is now `PASS`
7. Whether Task 002 may start

If any check fails, report `FAIL` and stop without starting Task 002.
