# Architecture

## Current architecture

Cloud research agents write JSON reports into GitHub. Other agents and humans read the repository's dated files and four mutable `latest` snapshots. Industrial and municipal radar reports have separate schemas and vocabularies. Enrichment snapshots use denormalized collections (`leads`, `projects`, `accounts`, `contacts`, and relationship/context collections) and currently have no formal schema.

GitHub is the persistence, history, handoff, and review layer. There is no database, service, queue, GitHub Actions workflow, or configured GitHub Pages site. Presentation-generation scripts are historical downstream tooling; their generated files are ignored.

```text
Cloud Radar Agents ──> legacy radar reports ──> Cloud Enrichment Agents
        │                       │                         │
        └──────────────────── Git history <──────────────┘
                                │
                         agents / humans
```

## Target MVP foundation

Task 001 adds an optional canonical single-lead exchange contract and local validation. Existing report feeds stay authoritative for current consumers.

```text
Public sources
      │
Cloud Radar Agents ──> existing report feeds (preserved)
      │
      └──────────────> Lead Contract v1
                            │
                 qualification / enrichment contributions
                            │
                   validator + Git review
                            │
                 orchestration / human sales (future)
```

Major components:

- Existing `intelligence/`: current radar and enrichment exchange interfaces.
- New `contracts/`: stable, stage-aware, evidence/provenance-first contracts.
- New `scripts/validate_intelligence.py`: dependency-free canonical and compatibility checks.
- New `tests/fixtures/`: non-confidential boundary examples.
- Git: traceability and multi-agent collaboration. Pages may later expose read-only artifacts but is not required for the MVP foundation.

No Radar Agent, scoring engine, merge engine, workflow engine, CRM integration, outbound automation, database, or UI is introduced.
