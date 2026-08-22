# Pipeline — GTM State Machine, Validator, and Test Reference

## 1. The Five GTM Stages

| Business stage | Answers | pipeline_stage values |
|---|---|---|
| **Radar** | Is there potentially something happening? | `RADAR` |
| **Qualification** | Is this worth spending more intelligence resources on? | `QUALIFICATION`, `QUALIFIED`, `REVIEW`, `REJECTED` |
| **Enrichment** | Who is involved, and who should sales engage? | `ENRICHMENT`, `ENRICHED` |
| **Orchestration** | Is this intelligence complete and coherent for sales action? | `ORCHESTRATION`, `SALES_READY` |
| **Engagement** | Hand off to human sales | `ENGAGEMENT` |

## 2. Pipeline Stage Enum (10 values)

`RADAR, QUALIFICATION, QUALIFIED, REVIEW, REJECTED, ENRICHMENT, ENRICHED, ORCHESTRATION, SALES_READY, ENGAGEMENT`

## 3. Transition Graph

```
RADAR         -> QUALIFICATION
QUALIFICATION -> QUALIFIED | REVIEW | REJECTED
REVIEW        -> QUALIFIED | REJECTED | REVIEW      (re-review self-loop)
REJECTED      -> REVIEW                              (reopen — see docs/OPEN_QUESTIONS.md #2)
QUALIFIED     -> ENRICHMENT
ENRICHMENT    -> ENRICHED
ENRICHED      -> ORCHESTRATION
ORCHESTRATION -> SALES_READY
SALES_READY   -> ENGAGEMENT
ENGAGEMENT    -> (terminal for Week 1)
```

Enforced in code as `PIPELINE_TRANSITIONS` in `pipeline/validate.py`. Any adjacent pair in `pipeline_history` not in this table is an ERROR in strict mode. This is not expressible in JSON Schema alone (it requires comparing adjacent array items against an external graph), so it's validator logic, not a schema constraint.

## 4. Recording Conventions

- **`pipeline_history`**: append-only log of every stage this Lead has passed through. Required, ≥1 entry. `pipeline_history[-1].stage` must equal the top-level `pipeline_stage`.
- **`provenance`**: general actor/action audit log (who did what, when) — distinct from `pipeline_history`, which only tracks stage changes. Use `provenance` for things like "agent X enriched contacts" or "human Y verified this contact."

## 5. Validator (`pipeline/validate.py`)

### Modes

- **`strict`**: validates v1 Lead documents against `contracts/v1/schema.json`, plus the transition-graph and evidence/contact checks below.
- **`legacy-compat`**: sanity-checks real `intelligence/**/*.json` files (never run through the v1 schema — legacy files were never meant to satisfy it).

### CLI Reference

```
python pipeline/validate.py --mode {strict|legacy-compat} [PATH ...]
    [--schema contracts/v1/schema.json]   # strict mode schema path
    [--all]                                # legacy-compat: auto-discover intelligence/**/*.json
    [--format {text|json}]                 # default: text
    [--strict-warnings]                    # WARNINGs also cause non-zero exit
    [-q | --quiet]                         # suppress INFO lines
```

`--mode strict` requires explicit PATH argument(s) — there is no implicit default, to avoid silently validating nothing.

### Output Format

```
<SEVERITY> [<file>] <lead_id>: <message>
...
SUMMARY: <N> files, <M> leads checked - <e> ERROR, <w> WARNING, <i> INFO
```

`--format json` emits the same findings as `{errors: [...], warnings: [...], infos: [...], summary: {...}}`.

### Exit Codes

- `0`: no ERRORs (WARNING/INFO never fail by default)
- `1`: ≥1 ERROR, or ≥1 WARNING when `--strict-warnings` is set
- `2`: usage error (bad args, missing schema file, unparseable JSON)

### Strict Mode Checks

1. Full JSON Schema validation (all errors collected, not just the first)
2. `pipeline_history` transition-graph walk — invalid adjacent pair is an ERROR; `pipeline_stage` disagreeing with `pipeline_history[-1].stage` is an ERROR
3. Duplicate `lead_id` across the files passed in one run — WARNING
4. All-empty evidence (`facts`/`inferences`/`unknowns`/`items` all empty) past RADAR stage — WARNING (soft nudge, not a hard gate)
5. Empty contact channel `value` — WARNING

### Legacy-Compat Mode: Findings Table

Real production data has known irregularities (see `docs/ARCHITECTURE.md` §2). Each is classified deliberately:

| Case | Severity | Why |
|---|---|---|
| `IND-YYYYMMDD-NN` 2-digit suffix (e.g. `IND-20260820-06`) | WARNING | Legitimate, already used downstream — never ERROR |
| `H-N` style ID (e.g. `H-10`) | WARNING | Agent-sourced outside the radar pipeline — expected |
| Unrecognized ID format entirely | WARNING | Generic catch-all, less specific message |
| `to_verify` object (industrial) vs array (municipal) | INFO | Each vertical's own `schema.json` already sanctions its own type |
| `logic` field present instead of `logic_rationale` | WARNING | Data violates its *own* file's schema.json — real (if long-known) drift |
| Contact `discovered_by` string (municipal) vs array (industrial) | WARNING | Not sanctioned by either legacy schema; v1 contract mandates array |
| Report-level qualification field absent | *silently ignored* | True of 100% of legacy files — repeating it per-file is pure noise |
| `report_id` format inconsistency (dashed/undashed/version suffix) | *silently ignored* | Known, accepted, non-actionable |
| Byte-identical `*_latest.json` duplicates (e.g. `ctx_0821.json` == `ctx_latest.json`) | INFO (in `--all` scan) | Expected/intentional mirroring convention |
| `H-10`-pattern empty evidence/logic/source_urls | INFO | Known, intentional agent-sourced pattern |
| `rejected_signals[]` unlinked to any `lead_id` | *not checked* | Out of Week 1 scope — no per-lead qualification record exists yet to link it to |

## 6. Running the Tests

```bash
pip install -r pipeline/requirements.txt
pytest tests/ -v
```

Test files:
- `tests/test_schema_validity.py` — schema structure + all 9 fixtures validate cleanly
- `tests/test_state_transitions.py` — every valid/invalid transition, conditional-required fields
- `tests/test_evidence.py` — facts/inferences/unknowns, structured evidence items, conflicting evidence
- `tests/test_missing_data_handling.py` — UNKNOWN contacts, minimal valid leads, null vs absent
- `tests/test_provenance_and_multi_agent.py` — provenance entries, N agents on 1 Lead, dedup signaling
- `tests/test_cli.py` — validator exit codes, `--format json`, `--strict-warnings`, `-q`
- `tests/test_legacy_compatibility.py` — real `intelligence/**/*.json` scanned end-to-end, asserts zero ERRORs

### Validator Demo Commands

```bash
python pipeline/validate.py --mode strict tests/fixtures/*.json
python pipeline/validate.py --mode legacy-compat --all
```

## 7. Extending the Validator in Future Weeks

- New checks should default to WARNING/INFO unless there's a strong reason to hard-fail (ERROR blocks CI/agent workflows).
- Adding a new pipeline stage or transition requires updating both `contracts/v1/schema.json` (enum + docs) and `PIPELINE_TRANSITIONS` in `pipeline/validate.py` — keep them in sync.
- New severity-table rows (legacy-compat mode) should be added to the table in this document, not just the code, so the classification rationale stays visible.
- This validator is intentionally not a generic rules engine — new checks are still hand-written Python, per "boring technology" and "avoid premature abstraction."
