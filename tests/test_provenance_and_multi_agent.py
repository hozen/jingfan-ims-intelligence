"""Test provenance tracking and multi-agent contribution to the same lead."""

from jsonschema import Draft202012Validator
from conftest import minimal_lead, load_fixture


class TestProvenanceEntryShape:
    def test_provenance_entry_requires_actor_type_action_timestamp(self, schema):
        doc = minimal_lead("RADAR")
        doc["provenance"] = [{"actor": "test-agent"}]  # missing actor_type, action, timestamp
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(doc))
        assert len(errors) > 0

    def test_valid_provenance_entry_passes(self, schema):
        doc = minimal_lead("RADAR")
        doc["provenance"] = [{
            "actor": "qualification_agent",
            "actor_type": "AGENT",
            "action": "Initial radar discovery",
            "timestamp": "2026-08-22T10:00:00Z"
        }]
        validator = Draft202012Validator(schema)
        assert list(validator.iter_errors(doc)) == []

    def test_actor_type_enum_restricted(self, schema):
        doc = minimal_lead("RADAR")
        doc["provenance"] = [{
            "actor": "someone",
            "actor_type": "ROBOT",  # not in enum
            "action": "did something",
            "timestamp": "2026-08-22T10:00:00Z"
        }]
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(doc))
        assert len(errors) > 0


class TestMultiAgentContribution:
    def test_fixture_h_has_two_agent_contributions(self):
        fixture = load_fixture("case_h_two_agents_enrich_same_lead")
        agents = [ac["agent_name"] for ac in fixture["enrichment"]["agent_contributions"]]
        assert "DuMate" in agents
        assert "WorkBuddy" in agents

    def test_fixture_h_cross_agent_confirmed_contact(self):
        fixture = load_fixture("case_h_two_agents_enrich_same_lead")
        contacts = fixture["enrichment"]["contacts"]
        confirmed = [c for c in contacts if c.get("cross_agent_confirmation")]
        assert len(confirmed) == 1
        assert set(confirmed[0]["discovered_by"]) == {"DuMate", "WorkBuddy"}

    def test_one_lead_can_have_many_agent_contributions_schema(self, schema):
        """Confirms architecture supports N agents contributing to 1 Lead (not 1:1)."""
        doc = minimal_lead("ENRICHED")
        doc["enrichment"]["agent_contributions"] = [
            {"agent_name": "RadarAgent"},
            {"agent_name": "QualificationAgent"},
            {"agent_name": "EnrichmentAgentA"},
            {"agent_name": "EnrichmentAgentB"},
            {"agent_name": "HumanReviewer"}
        ]
        validator = Draft202012Validator(schema)
        assert list(validator.iter_errors(doc)) == []


class TestDuplicateSignaling:
    def test_fixture_i_marks_possible_duplicate(self):
        fixture = load_fixture("case_i_duplicate_opportunity_different_sources")
        assert fixture["possible_duplicate"] is True
        assert fixture["duplicate_of"] == "IND-FIXTURE-I-SIBLING"

    def test_duplicate_of_references_sibling_lead_id(self, schema):
        doc = minimal_lead("ORCHESTRATION")
        doc["possible_duplicate"] = True
        doc["duplicate_of"] = "IND-OTHER-002"
        validator = Draft202012Validator(schema)
        assert list(validator.iter_errors(doc)) == []
