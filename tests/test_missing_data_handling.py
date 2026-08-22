"""Test UNKNOWN/NOT_FOUND handling — evidence over fabrication, never require invented data."""

from jsonschema import Draft202012Validator
from conftest import minimal_lead, load_fixture


class TestUnknownContactPasses:
    def test_fixture_g_unknown_contact_is_valid(self, schema):
        fixture = load_fixture("case_g_missing_contact_unknown")
        validator = Draft202012Validator(schema)
        assert list(validator.iter_errors(fixture)) == []

    def test_fixture_g_contact_name_is_unknown_string(self):
        fixture = load_fixture("case_g_missing_contact_unknown")
        contact = fixture["enrichment"]["contacts"][0]
        assert contact["name"] == "UNKNOWN"
        assert contact["title"] == "UNKNOWN"

    def test_contact_with_only_required_fields_is_valid(self, schema):
        """A contact needs only contact_id, name, discovered_by — everything else optional."""
        doc = minimal_lead("ENRICHED")
        doc["enrichment"]["contacts"] = [{
            "contact_id": "CT-MINIMAL-001",
            "name": "UNKNOWN",
            "discovered_by": ["SomeAgent"]
        }]
        validator = Draft202012Validator(schema)
        assert list(validator.iter_errors(doc)) == []


class TestMinimalValidLead:
    def test_minimal_radar_lead_passes(self, schema):
        """A lead with only required top-level fields should validate."""
        doc = minimal_lead("RADAR")
        validator = Draft202012Validator(schema)
        assert list(validator.iter_errors(doc)) == []

    def test_company_unknown_is_valid(self, schema):
        doc = minimal_lead("RADAR")
        doc["company"] = "UNKNOWN"
        validator = Draft202012Validator(schema)
        assert list(validator.iter_errors(doc)) == []


class TestAbsentVsNullFields:
    def test_absent_optional_fields_do_not_fail(self, schema):
        """Optional fields (provenance, sales_feedback, extensions) can be entirely absent."""
        doc = minimal_lead("RADAR")
        assert "provenance" not in doc
        assert "sales_feedback" not in doc
        validator = Draft202012Validator(schema)
        assert list(validator.iter_errors(doc)) == []

    def test_null_value_for_typed_field_fails(self, schema):
        """Explicit null is not the same as absent — a string field set to null should fail."""
        doc = minimal_lead("RADAR")
        doc["company"] = None
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(doc))
        assert len(errors) > 0

    def test_water_system_ownership_unknown_not_in_enum_by_design(self, schema):
        """company_intelligence.water_system_ownership uses A/B/C/D/N-A (existing legacy enum);
        genuinely unknown ownership should be represented by omitting the field, not by
        inventing a value outside the legacy vocabulary."""
        ci_def = schema["$defs"]["company_intelligence"]
        assert "water_system_ownership" not in ci_def.get("required", [])
