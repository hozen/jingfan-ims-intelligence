# Task 001 review brief — Architecture and contracts foundation

## Review objective

Confirm that the repository can continue serving existing Cloud Agent workflows while introducing a stable, evidence-first contract for the IMS GTM MVP. This change set stops at the Week 1 architecture boundary and does not implement new business methodology.

Open the visual summary at [`docs/ims-gtm-mvp-map.html`](ims-gtm-mvp-map.html) for a Chinese overview of completed and remaining MVP work.

## What this stage delivers

- A documented audit of current industrial and municipal radar/enrichment interfaces.
- An additive Lead Contract v1 covering identity, pipeline state, evidence, provenance, qualification, enrichment, conflicts, duplicate relationships, and future sales feedback.
- A lightweight state model for Radar through Engagement.
- A dependency-free validator with human-readable `ERROR`, `WARNING`, and `INFO` findings.
- Nine synthetic fixtures and twelve automated regression tests.
- Compatibility validation for all four current mutable `latest` interfaces.
- Documentation for architecture, pipeline boundaries, data contracts, risks, Product Owner decisions, and the smallest recommended next task.

## Compatibility promise

This stage does not rename, rewrite, migrate, or delete existing intelligence files. It does not change the four current `latest` paths. The canonical v1 contract is parallel and opt-in so future adapters can be tested before any consumer migration.

## Reviewer checklist

### Product / methodology

- [ ] Choose the canonical municipal Lead ID convention (`OPP`, `OP`, or `ML`).
- [ ] Define evidence requirements for qualification `PASS`, `REVIEW`, and `REJECT`.
- [ ] Define completion criteria for `ENRICHED` and `SALES_READY`.
- [ ] Decide whether a `REJECTED` Lead can be reopened and by whom.
- [ ] Decide who can resolve conflicting evidence.

### Architecture / engineering

- [ ] Confirm the four `latest` interfaces and identify all external consumers.
- [ ] Review the additive Lead Contract v1 for sufficient optionality and traceability.
- [ ] Review the explicit state transitions and rejection semantics.
- [ ] Decide whether Task 002 may add a read-only industrial Radar-to-v1 adapter.
- [ ] Decide whether GitHub Actions validation and branch protection should be enabled.
- [ ] Schedule a separate secrets review for the tracked `.hermes/.env`; its contents were not inspected in Task 001.

## How to verify

```bash
python -m unittest discover -s tests -v
python scripts/validate_intelligence.py
```

Expected result: 12 tests pass, and nine synthetic fixtures plus four current latest feeds validate with zero errors and zero warnings. Legacy feeds are reported as compatibility-mode inputs.

## Known historical data issues

A broader scan of 35 legacy intelligence files found 23 missing-ID errors and five malformed or empty source URL warnings, concentrated in municipal reports dated 2026-08-10 through 2026-08-18. Task 001 deliberately does not invent replacement IDs or URLs.

## Recommended next task — do not execute before review

Create a read-only adapter for the industrial Radar feed that maps selected signals to Lead Contract v1 while preserving source files and Lead IDs. Use golden tests and explicitly report unmappable fields. Qualification scoring and enrichment automation should remain out of scope until Product Owner rules are approved.
