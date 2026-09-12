import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_icp_poc


class ICPPOCTests(unittest.TestCase):
    def test_builds_real_industrial_and_municipal_profiles(self):
        profiles, metadata = build_icp_poc.build()
        self.assertGreaterEqual(len(profiles), 60)
        self.assertEqual({"工业", "市政"}, {x["market"] for x in profiles})
        self.assertTrue(all(x["id"] and x["project"] for x in profiles))
        self.assertTrue(metadata["industrial_updated"])
        self.assertTrue(all("penetration" in x for x in profiles))
        industrial = next(x for x in profiles if x["market"] == "工业" and x["penetration"]["ownership"])
        self.assertGreaterEqual(len(industrial["penetration"]["ownership"]), 1)
        municipal = next(x for x in profiles if x["market"] == "市政")
        self.assertIn("主管或出资主体", municipal["penetration"]["gaps"])

    def test_poc_avoids_exposing_contact_details(self):
        profiles, _ = build_icp_poc.build()
        serialized = str(profiles)
        self.assertNotIn("phone", serialized)
        self.assertNotIn("email", serialized)


if __name__ == "__main__":
    unittest.main()
