# Codex Brief — Close Task 001

## Objective

Close Task 001, **Architecture Foundation**, and merge it into `main` only when the architecture gate is genuinely satisfied.

Do not start Task 002 until this brief is complete.

## Repository context

- Repository: `jingfan-ims-intelligence`
- Current Task 001 branch: `codex/task-001-architecture-foundation`
- Task 001 commit currently reviewed: `1d98bf3`
- Current local `main`: does not contain Task 001
- Working tree at review time: clean
- Do not rewrite or rename existing Radar / Enrichment feeds.

## Current implementation to preserve

Keep the following Task 001 outputs unless a change is required to close a gate:

- `contracts/lead-v1.schema.json`
- `scripts/validate_intelligence.py`
- `tests/fixtures/*.json`
- `tests/test_validator.py`
- `docs/architecture.md`
- `docs/data-contract.md`
- `docs/pipeline.md`
- `docs/repository-audit.md`
- `docs/task-001-review.md`
- `docs/task-delivery-dashboard.html`

Preserve all existing interfaces:

- `intelligence/industrial/ind_latest.json`
- `intelligence/municipal/latest.json`
- `intelligence/industrial/enriched/indctx_latest.json`
- `intelligence/municipal/enriched/ctx_latest.json`
- Historical `daily/` and `enriched/` files

## Required fixes before closure

### 1. Align validator with the declared contract

The validator currently accepts invalid documents in these cases:

- Missing `pipeline_history`
- `qualification.decision = PASS` while the lead remains at `RADAR`
- Extra fields that are forbidden by the JSON Schema
- Inconsistent `enrichment.status` and pipeline stage

Make the smallest reasonable fix. Do not introduce a generic workflow engine or merge framework.

At minimum, enforce:

- A canonical lead has a contiguous `pipeline_history`.
- The first transition is `START -> RADAR`.
- The terminal history state equals `pipeline_stage`.
- `PASS` maps to a qualified path, `REJECT` maps to `REJECTED`, and `REVIEW` maps to `REVIEW` or an explicitly documented equivalent.
- `enrichment.status` cannot claim completion while the pipeline is before enrichment or while required enrichment structure is invalid.
- Unknown fields are rejected or reported as errors consistently with the schema.
- Malformed input produces findings, not a Python exception.

If any rule is intentionally left open, document the exact reason and update the contract documentation.

### 2. Add negative regression tests

Add tests for at least:

- missing `pipeline_history`
- `PASS` at `RADAR`
- `REJECT` without `REJECTED` state
- inconsistent enrichment status/stage
- unexpected top-level property
- malformed nested types that must not crash the validator

Keep all existing tests passing.

### 3. Update audit numbers

Re-run the historical scan over all tracked intelligence JSON files and update the stale counts in `docs/task-001-review.md` and/or `docs/repository-audit.md`.

Do not invent IDs or URLs in historical data. Report legacy defects accurately and separately from canonical Contract v1 failures.

### 4. Perform a secrets review gate

`.hermes/.env` is tracked in Git and must be reviewed as a security risk.

- Do not print or copy secret values.
- Determine whether it contains credentials or tokens.
- If it contains secrets, stop and report the issue; do not silently remove or rotate anything without explicit authorization.
- Record the review result in the closure notes.

## Verification commands

Run from the repository root:

```bash
python -m unittest discover -s tests -v
python scripts/validate_intelligence.py
```

Also run the full historical compatibility scan:

```bash
python scripts/validate_intelligence.py intelligence
```

Expected canonical result:

- All tests pass.
- Nine synthetic fixtures pass.
- Four current latest feeds pass with zero errors and zero warnings.
- Historical legacy defects are reported, not silently changed.

## Merge and branch requirements

Before saying Task 001 is closed:

1. Review the final diff from the Task 001 branch.
2. Confirm the branch contains the fixes and tests above.
3. Confirm the working tree is clean.
4. Merge the branch into `main` using the repository’s normal review process.
5. Re-run the tests and validator on the merged `main`.
6. Confirm `main` contains the Task 001 commit and closure changes.

Do not report “merged” based only on a local feature branch or remote feature branch.

## Customer deliverables

Task 001 is closed only when these customer-facing outputs are available:

- Lead Contract v1 definition
- Pipeline state and transition explanation
- Evidence/provenance rules
- Legacy compatibility statement
- Validator and test result summary
- Known limitations and unresolved Product Owner decisions
- Visual review in `docs/task-delivery-dashboard.html`

The customer-facing message must clearly state:

- what is now reliable
- what remains legacy or manual
- what is still blocked
- why Task 002 is or is not allowed to start

## Closure decision

Use exactly one final status:

- `PASS` — all required gates are satisfied and Task 002 may start.
- `CONDITIONAL PASS` — only explicitly non-blocking documentation or cleanup remains; Task 002 may start with those items tracked.
- `FAIL` — any contract, validator, merge, security, or compatibility gate remains unresolved; Task 002 must not start.

## If PASS

Define Task 002 as the smallest useful next step:

> Build a read-only Industrial Radar → Lead Contract v1 adapter with golden fixtures, field mapping/unmappable-field reporting, and customer-readable output. Preserve all original files and Lead IDs. Do not implement qualification scoring, enrichment automation, CRM integration, or outbound workflow.

## Final response format

Report:

1. Final status: `PASS`, `CONDITIONAL PASS`, or `FAIL`
2. Commit(s) reviewed and merge status
3. Tests and validation results
4. Remaining risks or decisions
5. Customer deliverables produced
6. Whether Task 002 may start
7. If allowed, the exact Task 002 scope
