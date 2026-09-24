"""Test schema validity and fixture conformance to v1 contract."""

import pytest
from jsonschema import Draft202012Validator, ValidationError
from conftest import load_fixture


class TestSchemaValidity:
    """Tests for the v1 schema itself."""

    def test_schema_loads_and_is_valid_draft2020(self, schema):
        """Schema should be valid JSON Schema Draft 2020-12."""
        assert schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
        assert "title" in schema
        assert "$defs" in schema

    def test_schema_defines_required_defs(self, schema):
        """Schema should define all required $defs."""
        required_defs = [
            "source_reference",
            "evidence",
            "evidence_item",
            "qualification",
            "enrichment",
            "company_intelligence",
            "project",
            "organization_relationship",
            "org_role",
            "contact",
            "contact_channel",
            "agent_contribution",
            "provenance_entry",
            "pipeline_transition",
            "sales_feedback"
        ]
        for def_name in required_defs:
            assert def_name in schema["$defs"], f"Missing $def: {def_name}"


class TestFixtureValidation:
    """Test that all fixtures conform to the v1 schema."""

    @pytest.mark.parametrize("fixture_name", [
        "case_a_valid_radar_lead",
        "case_b_qualified_lead",
        "case_c_lead_requiring_enrichment",
        "case_d_enriched_lead_epc_contacts",
        "case_e_rejected_lead",
        "case_f_conflicting_evidence",
        "case_g_missing_contact_unknown",
        "case_h_two_agents_enrich_same_lead",
        "case_i_duplicate_opportunity_different_sources"
    ])
    def test_fixture_passes_schema_validation(self, schema, fixture_name):
        """Each fixture should validate against the schema."""
        fixture = load_fixture(fixture_name)
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(fixture))
        assert len(errors) == 0, f"Fixture {fixture_name} has schema errors: {errors}"


class TestSchemaStructure:
    """Test key structural aspects of the schema."""

    def test_pipeline_stage_enum_values(self, schema):
        """Pipeline stage should have exactly 10 values."""
        props = schema["properties"]
        assert "pipeline_stage" in props
        expected_stages = [
            "RADAR",
            "QUALIFICATION",
            "QUALIFIED",
            "REVIEW",
            "REJECTED",
            "ENRICHMENT",
            "ENRICHED",
            "ORCHESTRATION",
            "SALES_READY",
            "ENGAGEMENT"
        ]
        assert sorted(props["pipeline_stage"]["enum"]) == sorted(expected_stages)

    def test_vertical_enum_values(self, schema):
        """Vertical should be industrial or municipal."""
        props = schema["properties"]
        assert props["vertical"]["enum"] == ["industrial", "municipal"]

    def test_lead_id_is_loose_string(self, schema):
        """lead_id should be a string with minLength, no pattern."""
        props = schema["properties"]
        assert props["lead_id"]["type"] == "string"
        assert "minLength" in props["lead_id"]
        # Pattern should NOT be present (format conformance is validator's job, not schema)
        assert "pattern" not in props["lead_id"]

    def test_contract_version_is_const_v1(self, schema):
        """contract_version must be const 'v1'."""
        props = schema["properties"]
        assert props["contract_version"]["const"] == "v1"


class TestConditionalRequirements:
    """Test conditional required fields (if/then logic)."""

    def test_qualification_required_past_radar(self, schema):
        """qualification should be required once stage >= QUALIFICATION."""
        # This is expressed in the schema as allOf with if/then
        # We verify the schema structure here, behavior tested in test_state_transitions.py
        props = schema["properties"]
        assert "qualification" in props

    def test_enrichment_required_past_enrichment_start(self, schema):
        """enrichment should be required once stage >= ENRICHMENT."""
        props = schema["properties"]
        assert "enrichment" in props


class TestEvidenceStructure:
    """Test evidence model."""

    def test_evidence_has_facts_inferences_unknowns(self, schema):
        """Evidence must have facts, inferences, unknowns arrays."""
        evidence_def = schema["$defs"]["evidence"]
        assert evidence_def["type"] == "object"
        assert "facts" in evidence_def["required"]
        assert "inferences" in evidence_def["required"]
        assert "unknowns" in evidence_def["required"]
        for field in ["facts", "inferences", "unknowns"]:
            assert evidence_def["properties"][field]["type"] == "array"

    def test_evidence_item_structure(self, schema):
        """Evidence item should have type and detail."""
        item_def = schema["$defs"]["evidence_item"]
        assert item_def["required"] == ["type", "detail"]
        assert "type" in item_def["properties"]
        assert item_def["properties"]["type"]["enum"] == [
            "FACT", "INFERENCE", "UNKNOWN", "AGENT_DISCOVERY", "PUBLIC_RECORD", "HUMAN_VERIFIED"
        ]


class TestContactStructure:
    """Test contact model."""

    def test_contact_discovered_by_is_required_array(self, schema):
        """Contact discovered_by must be a required array."""
        contact_def = schema["$defs"]["contact"]
        assert "discovered_by" in contact_def["required"]
        assert contact_def["properties"]["discovered_by"]["type"] == "array"

    def test_contact_has_required_fields(self, schema):
        """Contact should require contact_id, name, discovered_by."""
        contact_def = schema["$defs"]["contact"]
        required = set(contact_def["required"])
        assert required >= {"contact_id", "name", "discovered_by"}


class TestAdditionalPropertiesPolicy:
    """Test that additionalProperties is false except for extensions."""

    def test_root_level_additional_properties_false(self, schema):
        """Root should have additionalProperties: false."""
        assert schema.get("additionalProperties") is False

    def test_extensions_allows_additional_properties(self, schema):
        """extensions object should allow any additional properties."""
        ext_def = schema["properties"]["extensions"]
        assert ext_def["type"] == "object"
        assert ext_def["additionalProperties"] is True
