import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_intelligence import validate_document, validate_transition  # noqa: E402


FIXTURES = ROOT / "tests" / "fixtures"


def load(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def errors(findings):
    return [item for item in findings if item.severity == "ERROR"]


class CanonicalContractTests(unittest.TestCase):
    def test_all_synthetic_fixtures_are_valid(self):
        for path in sorted(FIXTURES.glob("*.json")):
            with self.subTest(path=path.name):
                self.assertEqual([], errors(validate_document(json.loads(path.read_text(encoding="utf-8")))))

    def test_invalid_schema_missing_identity(self):
        data = load("case_a_valid_radar.json")
        del data["lead_id"]
        self.assertTrue(any(item.path == "lead_id" for item in errors(validate_document(data))))

    def test_legacy_lead_id_compatibility(self):
        for lead_id in ("IND-20260820-06", "IND-20260821-001", "OPP-2026-08-10-001", "OP-20260821-001", "ML-20260821-0006"):
            data = load("case_a_valid_radar.json")
            data["lead_id"] = lead_id
            self.assertFalse(errors(validate_document(data)), lead_id)

    def test_invalid_state_transition(self):
        self.assertFalse(validate_transition("RADAR", "SALES_READY"))
        data = load("case_a_valid_radar.json")
        data["pipeline_stage"] = "SALES_READY"
        data["pipeline_history"][0]["to"] = "SALES_READY"
        findings = errors(validate_document(data))
        self.assertTrue(any("invalid pipeline transition" in item.message for item in findings))

    def test_evidence_url_and_reference_validation(self):
        data = load("case_b_qualified.json")
        data["evidence"][0]["source_url"] = "not a url"
        data["qualification"]["evidence_refs"] = ["missing"]
        findings = errors(validate_document(data))
        self.assertTrue(any(item.path.endswith("source_url") for item in findings))
        self.assertTrue(any("unknown evidence reference" in item.message for item in findings))

    def test_missing_optional_data_is_allowed(self):
        data = load("case_a_valid_radar.json")
        data.pop("company")
        data.pop("project")
        self.assertFalse(errors(validate_document(data)))

    def test_provenance_required_and_references_checked(self):
        data = load("case_b_qualified.json")
        data["qualification"]["provenance_ref"] = "missing"
        self.assertTrue(any("provenance" in item.path for item in errors(validate_document(data))))

    def test_duplicate_evidence_warning(self):
        data = load("case_a_valid_radar.json")
        duplicate = copy.deepcopy(data["evidence"][0])
        duplicate["evidence_id"] = "ev-a-2"
        data["evidence"].append(duplicate)
        findings = validate_document(data)
        self.assertTrue(any(item.severity == "WARNING" and "duplicate evidence" in item.message for item in findings))

    def test_conflicting_evidence_is_preserved(self):
        data = load("case_f_conflicting_evidence.json")
        self.assertFalse(errors(validate_document(data)))
        self.assertEqual("UNRESOLVED", data["conflicts"][0]["status"])
        self.assertEqual(2, len(data["conflicts"][0]["values"]))

    def test_multi_agent_contributions_are_preserved(self):
        data = load("case_h_multi_agent.json")
        self.assertFalse(errors(validate_document(data)))
        self.assertEqual(2, len(data["provenance"]))
        self.assertEqual(2, len({item["agent"] for item in data["provenance"]}))

    def test_contact_unknown_not_found_semantics(self):
        data = load("case_g_contact_not_found.json")
        self.assertFalse(errors(validate_document(data)))
        bad = copy.deepcopy(data)
        bad["enrichment"]["contacts"][0]["phone"] = "13800000000"
        self.assertTrue(any("NOT_FOUND requires null" in item.message for item in errors(validate_document(bad))))

    def test_missing_pipeline_history_is_rejected(self):
        data = load("case_a_valid_radar.json")
        del data["pipeline_history"]
        findings = errors(validate_document(data))
        self.assertTrue(any(item.path == "pipeline_history" for item in findings))

    def test_pass_decision_at_radar_is_rejected(self):
        data = load("case_b_qualified.json")
        data["pipeline_stage"] = "RADAR"
        data["pipeline_history"] = data["pipeline_history"][:1]
        findings = errors(validate_document(data))
        self.assertTrue(any(item.path == "qualification.decision" and "inconsistent" in item.message for item in findings))

    def test_reject_decision_without_rejected_state_is_rejected(self):
        data = load("case_e_rejected.json")
        data["pipeline_stage"] = "REVIEW"
        data["pipeline_history"][-1]["to"] = "REVIEW"
        findings = errors(validate_document(data))
        self.assertTrue(any(item.path == "qualification.decision" and "inconsistent" in item.message for item in findings))

    def test_enrichment_status_before_enrichment_is_rejected(self):
        data = load("case_d_enriched_epc_contacts.json")
        data["pipeline_stage"] = "QUALIFIED"
        data["pipeline_history"] = data["pipeline_history"][:3]
        findings = errors(validate_document(data))
        self.assertTrue(any(item.path == "enrichment.status" and "inconsistent" in item.message for item in findings))

    def test_unexpected_top_level_property_is_rejected(self):
        data = load("case_a_valid_radar.json")
        data["unexpected"] = "not in schema"
        findings = errors(validate_document(data))
        self.assertTrue(any(item.path == "unexpected" and item.message == "unexpected property" for item in findings))

    def test_malformed_nested_types_produce_findings_without_crashing(self):
        data = load("case_d_enriched_epc_contacts.json")
        data["provenance"][0]["evidence_refs"] = 42
        data["enrichment"]["contacts"] = {"not": "an array"}
        data["conflicts"] = [{"field": "x", "values": 42, "status": "UNRESOLVED"}]
        findings = validate_document(data)
        self.assertGreaterEqual(len(errors(findings)), 3)


class LegacyCompatibilityTests(unittest.TestCase):
    def test_current_latest_interfaces_are_accepted(self):
        paths = [
            ROOT / "intelligence" / "industrial" / "ind_latest.json",
            ROOT / "intelligence" / "municipal" / "latest.json",
            ROOT / "intelligence" / "industrial" / "enriched" / "indctx_latest.json",
            ROOT / "intelligence" / "municipal" / "enriched" / "ctx_latest.json",
        ]
        for path in paths:
            with self.subTest(path=path):
                findings = validate_document(json.loads(path.read_text(encoding="utf-8-sig")))
                self.assertFalse(errors(findings))


if __name__ == "__main__":
    unittest.main()
