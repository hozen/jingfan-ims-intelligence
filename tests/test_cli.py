"""Test pipeline/validate.py CLI behavior: exit codes, output formats."""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
VALIDATE_PY = REPO_ROOT / "pipeline" / "validate.py"
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"


def run_validator(args):
    """Run the validator CLI and return (exit_code, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, str(VALIDATE_PY)] + args,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


class TestStrictModeExitCodes:
    def test_valid_fixtures_exit_zero(self):
        fixture_paths = [str(p) for p in sorted(FIXTURES_DIR.glob("*.json"))]
        code, stdout, stderr = run_validator(["--mode", "strict"] + fixture_paths)
        assert code == 0, f"stdout: {stdout}\nstderr: {stderr}"

    def test_broken_doc_exits_one(self, tmp_path):
        broken_doc = {
            "contract_version": "v1",
            "lead_id": "BROKEN-001",
            # missing required fields: vertical, pipeline_stage, company, source, evidence, pipeline_history
        }
        broken_file = tmp_path / "broken.json"
        broken_file.write_text(json.dumps(broken_doc), encoding="utf-8")
        code, stdout, stderr = run_validator(["--mode", "strict", str(broken_file)])
        assert code == 1
        assert "ERROR" in stdout

    def test_missing_path_arg_exits_two(self):
        code, stdout, stderr = run_validator(["--mode", "strict"])
        assert code == 2


class TestLegacyCompatModeExitCodes:
    def test_real_legacy_data_exits_zero(self):
        """WARNINGs/INFOs on real legacy data should not fail the build by default."""
        code, stdout, stderr = run_validator(["--mode", "legacy-compat", "--all"])
        assert code == 0, f"Legacy-compat scan should have 0 ERRORs.\nstdout: {stdout}"

    def test_strict_warnings_flag_can_flip_exit_code(self):
        """--strict-warnings makes warnings fail the build (used for demonstrating the flag
        exists and works on real data known to contain WARNING-level findings)."""
        code_normal, stdout_normal, _ = run_validator(["--mode", "legacy-compat", "--all"])
        code_strict, stdout_strict, _ = run_validator(["--mode", "legacy-compat", "--all", "--strict-warnings"])
        if "WARNING" in stdout_normal:
            assert code_strict == 1
            assert code_normal == 0


class TestOutputFormats:
    def test_json_format_is_valid_json(self):
        fixture_paths = [str(p) for p in sorted(FIXTURES_DIR.glob("*.json"))]
        code, stdout, stderr = run_validator(["--mode", "strict", "--format", "json"] + fixture_paths)
        parsed = json.loads(stdout)
        assert "summary" in parsed
        assert "errors" in parsed
        assert "warnings" in parsed
        assert "infos" in parsed

    def test_text_format_has_summary_line(self):
        fixture_paths = [str(p) for p in sorted(FIXTURES_DIR.glob("*.json"))]
        code, stdout, stderr = run_validator(["--mode", "strict"] + fixture_paths)
        assert "SUMMARY:" in stdout

    def test_quiet_suppresses_info_lines(self):
        code, stdout, stderr = run_validator(["--mode", "legacy-compat", "--all", "-q"])
        # quiet suppresses INFO but not ERROR/WARNING/SUMMARY lines
        lines = [l for l in stdout.splitlines() if l.startswith("INFO")]
        assert lines == []
