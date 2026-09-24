"""Pytest configuration and shared fixtures."""

import json
from pathlib import Path
import pytest


@pytest.fixture(scope="session")
def schema():
    """Load the v1 schema."""
    schema_path = Path(__file__).parent.parent / "contracts" / "v1" / "schema.json"
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture(scope="session")
def fixtures_dir():
    """Return path to fixtures directory."""
    return Path(__file__).parent / "fixtures"


def load_fixture(fixture_name: str) -> dict:
    """Load a fixture by name (e.g., 'case_a_valid_radar_lead')."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    fixture_file = fixtures_dir / f"{fixture_name}.json"
    with open(fixture_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def minimal_lead(pipeline_stage="RADAR", pipeline_history=None):
    """Build a minimal valid v1 Lead document for a given stage."""
    doc = {
        "contract_version": "v1",
        "lead_id": "IND-TEST-001",
        "vertical": "industrial",
        "pipeline_stage": pipeline_stage,
        "company": "Test Co",
        "source": {
            "vertical": "industrial",
            "source_report_id": "test-report",
            "source_signal_id": "IND-TEST-001"
        },
        "evidence": {"facts": ["a fact"], "inferences": [], "unknowns": []},
        "pipeline_history": pipeline_history or [
            {"stage": pipeline_stage, "entered_at": "2026-08-22T10:00:00Z"}
        ]
    }
    if pipeline_stage in ("QUALIFICATION", "QUALIFIED", "REVIEW", "REJECTED", "ENRICHMENT",
                          "ENRICHED", "ORCHESTRATION", "SALES_READY", "ENGAGEMENT"):
        doc["qualification"] = {"decision": "PASS"}
    if pipeline_stage in ("ENRICHMENT", "ENRICHED", "ORCHESTRATION", "SALES_READY", "ENGAGEMENT"):
        doc["enrichment"] = {"status": "IN_PROGRESS"}
    return doc
