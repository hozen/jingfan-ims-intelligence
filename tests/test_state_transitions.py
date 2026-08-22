"""Test pipeline state machine validation."""

import sys
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).parent.parent / "pipeline"))
from validate import PIPELINE_TRANSITIONS
from conftest import minimal_lead


class TestValidTransitions:
    """Every valid transition in the graph should be accepted by schema validation."""

    @pytest.mark.parametrize("from_stage,to_stage", [
        ("RADAR", "QUALIFICATION"),
        ("QUALIFICATION", "QUALIFIED"),
        ("QUALIFICATION", "REVIEW"),
        ("QUALIFICATION", "REJECTED"),
        ("REVIEW", "QUALIFIED"),
        ("REVIEW", "REJECTED"),
        ("REVIEW", "REVIEW"),
        ("REJECTED", "REVIEW"),
        ("QUALIFIED", "ENRICHMENT"),
        ("ENRICHMENT", "ENRICHED"),
        ("ENRICHED", "ORCHESTRATION"),
        ("ORCHESTRATION", "SALES_READY"),
        ("SALES_READY", "ENGAGEMENT"),
    ])
    def test_transition_is_in_graph(self, from_stage, to_stage):
        assert to_stage in PIPELINE_TRANSITIONS[from_stage]


class TestInvalidTransitions:
    """Invalid transitions should be detectable via the transition graph."""

    @pytest.mark.parametrize("from_stage,to_stage", [
        ("RADAR", "SALES_READY"),   # skips stages
        ("RADAR", "ENGAGEMENT"),    # skips stages
        ("QUALIFIED", "RADAR"),     # backward
        ("ENGAGEMENT", "RADAR"),    # terminal stage, no transitions out
        ("ENRICHED", "QUALIFIED"),  # backward
    ])
    def test_invalid_transition_not_in_graph(self, from_stage, to_stage):
        assert to_stage not in PIPELINE_TRANSITIONS.get(from_stage, [])

    def test_engagement_is_terminal(self):
        """ENGAGEMENT should have no valid outgoing transitions in Week 1."""
        assert PIPELINE_TRANSITIONS["ENGAGEMENT"] == []


class TestPipelineHistoryStageMismatch:
    """pipeline_history[-1].stage should match top-level pipeline_stage."""

    def test_matching_stage_is_valid(self, schema):
        doc = minimal_lead("QUALIFIED", pipeline_history=[
            {"stage": "RADAR", "entered_at": "2026-08-20T10:00:00Z"},
            {"stage": "QUALIFICATION", "entered_at": "2026-08-21T10:00:00Z"},
            {"stage": "QUALIFIED", "entered_at": "2026-08-22T10:00:00Z"},
        ])
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(doc))
        assert len(errors) == 0

    def test_pipeline_history_requires_min_one_item(self, schema):
        doc = minimal_lead("RADAR")
        doc["pipeline_history"] = []
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(doc))
        assert len(errors) > 0


class TestConditionalRequiredFields:
    """qualification/enrichment become required at certain stages."""

    def test_qualified_without_qualification_object_fails(self, schema):
        doc = minimal_lead("QUALIFIED")
        del doc["qualification"]
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(doc))
        assert len(errors) > 0

    def test_radar_without_qualification_object_is_valid(self, schema):
        doc = minimal_lead("RADAR")
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(doc))
        assert len(errors) == 0

    def test_enrichment_stage_without_enrichment_object_fails(self, schema):
        doc = minimal_lead("ENRICHMENT")
        del doc["enrichment"]
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(doc))
        assert len(errors) > 0

    def test_qualified_without_enrichment_object_is_valid(self, schema):
        """enrichment not required until ENRICHMENT stage."""
        doc = minimal_lead("QUALIFIED")
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(doc))
        assert len(errors) == 0


class TestInvalidPipelineStageEnum:
    def test_unknown_stage_value_fails(self, schema):
        doc = minimal_lead("RADAR")
        doc["pipeline_stage"] = "NOT_A_REAL_STAGE"
        doc["pipeline_history"] = [{"stage": "NOT_A_REAL_STAGE", "entered_at": "2026-08-22T10:00:00Z"}]
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(doc))
        assert len(errors) > 0
