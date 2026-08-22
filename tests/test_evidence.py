"""Test evidence-first architecture: facts/inferences/unknowns, evidence_items, conflicts."""

from jsonschema import Draft202012Validator
from conftest import minimal_lead, load_fixture


class TestBasicEvidenceHappyPath:
    def test_facts_inferences_unknowns_all_present(self, schema):
        doc = minimal_lead("RADAR")
        doc["evidence"] = {
            "facts": ["fact one", "fact two"],
            "inferences": ["inference one"],
            "unknowns": ["unknown one"]
        }
        validator = Draft202012Validator(schema)
        assert list(validator.iter_errors(doc)) == []

    def test_empty_arrays_allowed_at_radar(self, schema):
        """Empty evidence arrays are schema-valid (radar might discover with minimal info)."""
        doc = minimal_lead("RADAR")
        doc["evidence"] = {"facts": [], "inferences": [], "unknowns": []}
        validator = Draft202012Validator(schema)
        assert list(validator.iter_errors(doc)) == []

    def test_missing_required_evidence_key_fails(self, schema):
        doc = minimal_lead("RADAR")
        doc["evidence"] = {"facts": [], "inferences": []}  # missing unknowns
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(doc))
        assert len(errors) > 0


class TestStructuredEvidenceItems:
    def test_evidence_item_optional_structured_form(self, schema):
        doc = minimal_lead("RADAR")
        doc["evidence"]["items"] = [
            {
                "type": "FACT",
                "detail": "Confirmed via public filing",
                "source": "SEC filing",
                "confidence": "HIGH"
            }
        ]
        validator = Draft202012Validator(schema)
        assert list(validator.iter_errors(doc)) == []

    def test_evidence_item_requires_type_and_detail(self, schema):
        doc = minimal_lead("RADAR")
        doc["evidence"]["items"] = [{"source": "some source"}]  # missing type, detail
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(doc))
        assert len(errors) > 0

    def test_evidence_item_invalid_type_fails(self, schema):
        doc = minimal_lead("RADAR")
        doc["evidence"]["items"] = [{"type": "MADE_UP_TYPE", "detail": "x"}]
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(doc))
        assert len(errors) > 0


class TestDuplicateEvidenceAllowed:
    def test_duplicate_facts_strings_are_schema_valid(self, schema):
        """Schema does not deduplicate facts; duplicate strings are technically valid
        (a validator-level WARNING could flag this in a future iteration, not Week 1 scope)."""
        doc = minimal_lead("RADAR")
        doc["evidence"] = {
            "facts": ["Company X announced expansion", "Company X announced expansion"],
            "inferences": [],
            "unknowns": []
        }
        validator = Draft202012Validator(schema)
        assert list(validator.iter_errors(doc)) == []


class TestConflictingEvidenceNotAutoResolved:
    def test_fixture_f_has_two_contradictory_evidence_items(self):
        """Fixture F should store both sides of a contradiction without resolving it."""
        fixture = load_fixture("case_f_conflicting_evidence")
        contact = fixture["enrichment"]["contacts"][0]
        assert len(contact["evidence"]) == 2
        details = [item["detail"] for item in contact["evidence"]]
        assert "2000 m³/day" in details[0]
        assert "1200 m³/day" in details[1]
        assert "conflict_note" in contact
        assert contact["human_verified"] is False

    def test_conflicting_evidence_items_both_pass_schema(self, schema):
        doc = minimal_lead("ENRICHED")
        doc["enrichment"]["contacts"] = [{
            "contact_id": "CT-001",
            "name": "Test Person",
            "discovered_by": ["Agent1"],
            "evidence": [
                {"type": "FACT", "detail": "Capacity is 2000 m3/day", "confidence": "HIGH"},
                {"type": "FACT", "detail": "Capacity is 1200 m3/day", "confidence": "MEDIUM"}
            ],
            "conflict_note": "Sources disagree on capacity figure"
        }]
        validator = Draft202012Validator(schema)
        assert list(validator.iter_errors(doc)) == []
