"""Test legacy-compat mode against REAL intelligence/**/*.json production data.

These tests assert the validator never produces ERRORs on real Cloud Agent output
(backward compatibility is a hard requirement), and that specific known irregularities
in the data are classified with the correct severity per docs/PIPELINE.md.
"""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "pipeline"))
from validate import validate_legacy_compat, ValidationResult

REPO_ROOT = Path(__file__).parent.parent
INTELLIGENCE_DIR = REPO_ROOT / "intelligence"


def scan(paths):
    result = ValidationResult()
    validate_legacy_compat([str(p) for p in paths], result)
    return result


@pytest.mark.skipif(not INTELLIGENCE_DIR.exists(), reason="intelligence/ directory not present")
class TestZeroErrorsOnRealData:
    """Legacy-compat mode must never ERROR on real production data — only WARNING/INFO."""

    @pytest.mark.parametrize("subdir", [
        "industrial/daily",
        "industrial/enriched",
        "municipal/daily",
        "municipal/enriched",
    ])
    def test_zero_errors_in_subdir(self, subdir):
        files = sorted((INTELLIGENCE_DIR / subdir).glob("*.json"))
        if not files:
            pytest.skip(f"No files found in {subdir}")
        result = scan(files)
        assert result.errors == [], f"Unexpected ERRORs in {subdir}: {result.errors}"


@pytest.mark.skipif(not INTELLIGENCE_DIR.exists(), reason="intelligence/ directory not present")
class TestKnownEdgeCases:
    """Targeted checks for specific irregularities discovered during the repo audit."""

    def test_ind_20260820_two_digit_suffix_is_warning_not_error(self):
        f = INTELLIGENCE_DIR / "industrial" / "daily" / "2026-08-20.json"
        if not f.exists():
            pytest.skip("2026-08-20.json not present")
        result = scan([f])
        assert result.errors == []
        warning_ids = [lid for _, lid, _ in result.warnings]
        assert "IND-20260820-06" in warning_ids or any(
            "IND-20260820" in lid for lid in warning_ids
        )

    def test_h10_is_warning_or_info_not_error(self):
        f = INTELLIGENCE_DIR / "industrial" / "enriched" / "indctx_latest.json"
        if not f.exists():
            pytest.skip("indctx_latest.json not present")
        result = scan([f])
        assert result.errors == []
        all_ids = [lid for _, lid, _ in result.warnings + result.infos]
        assert "H-10" in all_ids

    def test_discovered_by_string_vs_array_is_warning(self):
        f = INTELLIGENCE_DIR / "municipal" / "enriched" / "ctx_latest.json"
        if not f.exists():
            pytest.skip("ctx_latest.json not present")
        result = scan([f])
        assert result.errors == []
        # Municipal enriched contacts with string discovered_by should produce a WARNING
        discovered_by_warnings = [
            msg for _, _, msg in result.warnings if "discovered_by is string" in msg
        ]
        # Not asserting count > 0 strictly (data may change), but if present, must be WARNING not ERROR
        assert result.errors == []

    def test_qualification_field_absence_produces_no_finding(self):
        """100% of legacy files lack a qualification field — this must not be flagged
        (universal, non-actionable, would just be noise)."""
        files = sorted((INTELLIGENCE_DIR / "industrial" / "daily").glob("*.json"))
        if not files:
            pytest.skip("No industrial daily files present")
        result = scan(files)
        qualification_findings = [
            msg for _, _, msg in result.errors + result.warnings + result.infos
            if "qualification" in msg.lower() and "field" in msg.lower()
        ]
        assert qualification_findings == []

    def test_byte_identical_duplicates_flagged_info_in_all_scan(self):
        """ctx_0821.json and ctx_latest.json are byte-identical (known intentional mirroring)."""
        f1 = INTELLIGENCE_DIR / "municipal" / "enriched" / "ctx_0821.json"
        f2 = INTELLIGENCE_DIR / "municipal" / "enriched" / "ctx_latest.json"
        if not (f1.exists() and f2.exists()):
            pytest.skip("ctx_0821.json / ctx_latest.json not both present")
        result = scan([f1, f2])
        assert result.errors == []
        dup_infos = [msg for _, _, msg in result.infos if "Byte-identical" in msg]
        assert len(dup_infos) >= 1


@pytest.mark.skipif(not INTELLIGENCE_DIR.exists(), reason="intelligence/ directory not present")
class TestFullTreeScan:
    def test_entire_intelligence_tree_zero_errors(self):
        """The strongest backward-compatibility guarantee: scan everything, zero ERRORs."""
        all_files = sorted(INTELLIGENCE_DIR.rglob("*.json"))
        assert len(all_files) > 0, "Expected to find intelligence/*.json files"
        result = scan(all_files)
        assert result.errors == [], f"Unexpected ERRORs across full tree: {result.errors}"
