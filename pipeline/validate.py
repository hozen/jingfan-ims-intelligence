#!/usr/bin/env python3
"""
Lightweight validator for Jingfan IMS GTM Intelligence leads.

Two modes:
  - strict: validates v1 Lead documents against contracts/v1/schema.json
  - legacy-compat: sanity-checks real intelligence/**/*.json files
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple
import jsonschema
from jsonschema import Draft202012Validator


PIPELINE_TRANSITIONS = {
    "RADAR": ["QUALIFICATION"],
    "QUALIFICATION": ["QUALIFIED", "REVIEW", "REJECTED"],
    "REVIEW": ["QUALIFIED", "REJECTED", "REVIEW"],
    "REJECTED": ["REVIEW"],
    "QUALIFIED": ["ENRICHMENT"],
    "ENRICHMENT": ["ENRICHED"],
    "ENRICHED": ["ORCHESTRATION"],
    "ORCHESTRATION": ["SALES_READY"],
    "SALES_READY": ["ENGAGEMENT"],
    "ENGAGEMENT": []
}

VALID_ID_PATTERNS = [
    ("IND-YYYYMMDD-NNN (3-digit industrial)", r"^IND-\d{8}-\d{3}$"),
    ("IND-YYYYMMDD-NN (2-digit industrial legacy)", r"^IND-\d{8}-\d{2}$"),
    ("OP-YYYYMMDD-NNN (municipal)", r"^OP-\d{8}-\d{3}$"),
    ("ML-YYYYMMDD-NNNN (municipal alternative)", r"^ML-\d{8}-\d{4}$"),
    ("H-N (agent-sourced)", r"^H-\d+$"),
]


class ValidationResult:
    def __init__(self):
        self.errors: List[Tuple[str, str, str]] = []
        self.warnings: List[Tuple[str, str, str]] = []
        self.infos: List[Tuple[str, str, str]] = []
        # Tracked independently of findings, so a clean scan doesn't report "0 files checked".
        self.files_scanned: set = set()
        self.leads_scanned: set = set()

    def track_file(self, filename: str):
        self.files_scanned.add(filename)

    def track_lead(self, filename: str, lead_id: str):
        self.files_scanned.add(filename)
        self.leads_scanned.add((filename, lead_id))

    def error(self, filename: str, lead_id: str, message: str):
        self.errors.append((filename, lead_id, message))

    def warning(self, filename: str, lead_id: str, message: str):
        self.warnings.append((filename, lead_id, message))

    def info(self, filename: str, lead_id: str, message: str):
        self.infos.append((filename, lead_id, message))

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def print_report(self, format_type: str = "text", quiet: bool = False):
        if format_type == "json":
            self._print_json_report()
        else:
            self._print_text_report(quiet=quiet)

    def _print_text_report(self, quiet: bool = False):
        for filename, lead_id, msg in self.errors:
            print(f"ERROR [{filename}] {lead_id}: {msg}")
        for filename, lead_id, msg in self.warnings:
            print(f"WARNING [{filename}] {lead_id}: {msg}")
        if not quiet:
            for filename, lead_id, msg in self.infos:
                print(f"INFO [{filename}] {lead_id}: {msg}")

        total_files = len(self.files_scanned)
        total_leads = len(self.leads_scanned)
        print(
            f"\nSUMMARY: {total_files} files, {total_leads} leads checked - "
            f"{len(self.errors)} ERROR, {len(self.warnings)} WARNING, {len(self.infos)} INFO"
        )

    def _print_json_report(self):
        report = {
            "errors": [
                {"file": f, "lead_id": lid, "message": msg}
                for f, lid, msg in self.errors
            ],
            "warnings": [
                {"file": f, "lead_id": lid, "message": msg}
                for f, lid, msg in self.warnings
            ],
            "infos": [
                {"file": f, "lead_id": lid, "message": msg}
                for f, lid, msg in self.infos
            ],
            "summary": {
                "files_scanned": len(self.files_scanned),
                "leads_scanned": len(self.leads_scanned),
                "error_count": len(self.errors),
                "warning_count": len(self.warnings),
                "info_count": len(self.infos)
            }
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))


def load_schema(schema_path: str) -> Dict:
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Schema file not found: {schema_path}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in schema: {e}", file=sys.stderr)
        sys.exit(2)


def validate_strict(paths: List[str], schema: Dict, result: ValidationResult):
    """Validate v1 Lead documents in strict mode."""
    validator = Draft202012Validator(schema)
    seen_ids = {}

    for path_str in paths:
        path = Path(path_str)
        if not path.exists():
            result.error(path_str, "(file-level)", f"File not found")
            continue

        try:
            with open(path, 'r', encoding='utf-8') as f:
                doc = json.load(f)
        except json.JSONDecodeError as e:
            result.error(path_str, "(file-level)", f"Invalid JSON: {e}")
            continue

        lead_id = doc.get("lead_id", "(unknown)")
        result.track_lead(str(path), lead_id)

        # Schema validation
        errors = list(validator.iter_errors(doc))
        for error in errors:
            path_str_short = ".".join(str(p) for p in error.path) if error.path else "root"
            result.error(
                str(path),
                lead_id,
                f"Schema validation: {error.message} at {path_str_short}"
            )

        # Pipeline history validation
        if "pipeline_history" in doc:
            history = doc["pipeline_history"]
            current_stage = doc.get("pipeline_stage")

            # Check that pipeline_history[-1].stage matches pipeline_stage
            if history and history[-1].get("stage") != current_stage:
                result.error(
                    str(path),
                    lead_id,
                    f"pipeline_history[-1].stage ({history[-1].get('stage')}) does not match "
                    f"pipeline_stage ({current_stage})"
                )

            # Check transition validity
            for i in range(len(history) - 1):
                from_stage = history[i].get("stage")
                to_stage = history[i + 1].get("stage")
                if from_stage not in PIPELINE_TRANSITIONS:
                    result.error(
                        str(path),
                        lead_id,
                        f"Unknown stage in pipeline_history: {from_stage}"
                    )
                elif to_stage not in PIPELINE_TRANSITIONS.get(from_stage, []):
                    result.error(
                        str(path),
                        lead_id,
                        f"Invalid transition: {from_stage} -> {to_stage}"
                    )

        # Check for duplicate lead_ids across the run
        if lead_id in seen_ids:
            result.warning(
                str(path),
                lead_id,
                f"Duplicate lead_id (also seen in {seen_ids[lead_id]})"
            )
        else:
            seen_ids[lead_id] = str(path)

        # Evidence validation: warn if empty past RADAR
        if doc.get("pipeline_stage") != "RADAR":
            evidence = doc.get("evidence", {})
            facts = evidence.get("facts", [])
            inferences = evidence.get("inferences", [])
            unknowns = evidence.get("unknowns", [])
            if not facts and not inferences and not unknowns and not evidence.get("items"):
                result.warning(
                    str(path),
                    lead_id,
                    f"All evidence fields empty at stage {doc.get('pipeline_stage')} "
                    f"(soft nudge; may be intentional)"
                )

        # Contact channel validation
        enrichment = doc.get("enrichment")
        if enrichment and enrichment.get("contacts"):
            for contact in enrichment["contacts"]:
                contact_id = contact.get("contact_id", "(unknown)")
                for channel_list in [contact.get("phone", []), contact.get("email", [])]:
                    for channel in channel_list:
                        if not channel.get("value") or not str(channel.get("value")).strip():
                            result.warning(
                                str(path),
                                lead_id,
                                f"Contact {contact_id}: empty channel value"
                            )


def validate_legacy_compat(paths: List[str], result: ValidationResult):
    """Sanity-check legacy intelligence/**/*.json files."""
    import re
    seen_hashes = {}

    for path_str in paths:
        path = Path(path_str)
        if not path.exists():
            result.info(path_str, "(file-level)", "File not found")
            continue

        try:
            with open(path, 'r', encoding='utf-8') as f:
                doc = json.load(f)
        except json.JSONDecodeError as e:
            result.warning(path_str, "(file-level)", f"Invalid JSON: {e}")
            continue

        result.track_file(str(path))

        # Detect top-level structure
        if "signals" in doc:
            leads = doc.get("signals", [])
            lead_key = "id"
        elif "opportunities" in doc:
            leads = doc.get("opportunities", [])
            lead_key = "id"
        elif "leads" in doc:
            leads = doc.get("leads", [])
            lead_key = "lead_id"
        else:
            result.info(path_str, "(file-level)", "Unknown lead array key; skipping detailed checks")
            leads = []
            lead_key = None

        # Byte-identical duplicate check
        try:
            with open(path, 'rb') as f:
                content_hash = hash(f.read())
            if content_hash in seen_hashes:
                result.info(
                    str(path),
                    "(file-level)",
                    f"Byte-identical to {seen_hashes[content_hash]} (expected for *_latest.json mirroring)"
                )
            else:
                seen_hashes[content_hash] = str(path)
        except Exception:
            pass

        # Per-lead checks
        for lead in leads:
            if not lead_key or lead_key not in lead:
                lead_id = "(unknown)"
            else:
                lead_id = lead.get(lead_key)
            result.track_lead(str(path), lead_id)

            # ID format checks
            id_str = str(lead_id)
            matched = False
            for pattern_name, pattern_regex in VALID_ID_PATTERNS:
                if re.match(pattern_regex, id_str):
                    matched = True
                    break

            if not matched:
                if re.match(r"^IND-\d{8}-\d{1}$", id_str):
                    result.warning(
                        str(path),
                        lead_id,
                        f"Non-standard IND ID suffix length (1-digit): {id_str}; expected 2-3 digits"
                    )
                elif re.match(r"^[A-Z]+-", id_str):
                    result.warning(
                        str(path),
                        lead_id,
                        f"Unrecognized ID format: {id_str}"
                    )

            # to_verify type check
            if "to_verify" in lead:
                to_verify = lead["to_verify"]
                if isinstance(to_verify, dict):
                    result.info(str(path), lead_id, "to_verify is object (industrial schema)")
                elif isinstance(to_verify, list):
                    result.info(str(path), lead_id, "to_verify is array (municipal schema)")

            # logic field check
            if "logic" in lead and "logic_rationale" not in lead:
                result.warning(
                    str(path),
                    lead_id,
                    "Lead has 'logic' field but schema defines 'logic_rationale' - schema drift"
                )

            # Contact discovered_by check (enriched files only)
            if "enrichment" in lead and "contacts" in lead.get("enrichment", {}):
                for contact in lead["enrichment"]["contacts"]:
                    discovered_by = contact.get("discovered_by")
                    if isinstance(discovered_by, str):
                        result.warning(
                            str(path),
                            lead_id,
                            f"Contact {contact.get('contact_id', '?')}: discovered_by is string "
                            f"(municipal), should be array (v1 normalized form)"
                        )
                    elif not discovered_by:
                        result.info(
                            str(path),
                            lead_id,
                            f"Contact {contact.get('contact_id', '?')}: discovered_by absent"
                        )

            # H-10 agent-sourced pattern (intentional)
            if id_str == "H-10":
                evidence = lead.get("evidence", {})
                if (not evidence.get("facts") and not evidence.get("inferences") and
                    not evidence.get("unknowns") and not lead.get("source_urls")):
                    result.info(
                        str(path),
                        lead_id,
                        "Agent-sourced lead (H-10 pattern) with minimal evidence - expected pattern"
                    )

            # Enrichment status check
            enrichment = lead.get("enrichment") or lead.get("leads", [{}])[0].get("enrichment")
            if enrichment and enrichment.get("enrichment_status") == "agent_discovered":
                if not evidence.get("facts") and not evidence.get("inferences"):
                    result.info(
                        str(path),
                        lead_id,
                        "Agent-discovered enrichment with minimal facts/inferences - expected pattern"
                    )


def find_intelligence_files(mode: str) -> List[str]:
    """Auto-discover intelligence/**/*.json files."""
    repo_root = Path(__file__).parent.parent
    intelligence_dir = repo_root / "intelligence"
    if not intelligence_dir.exists():
        return []

    files = []
    for subdir in intelligence_dir.rglob("*"):
        if subdir.is_file() and subdir.suffix == ".json":
            files.append(str(subdir))
    return sorted(files)


def main():
    parser = argparse.ArgumentParser(
        description="Validate Jingfan IMS GTM Intelligence leads (strict or legacy-compat mode)"
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=["strict", "legacy-compat"],
        help="Validation mode"
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="File paths to validate (required in strict mode; optional in legacy-compat)"
    )
    parser.add_argument(
        "--schema",
        default="contracts/v1/schema.json",
        help="Path to v1 schema (strict mode only)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Legacy-compat only: auto-discover and scan intelligence/**/*.json"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format"
    )
    parser.add_argument(
        "--strict-warnings",
        action="store_true",
        help="Treat warnings as errors (exit 1)"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress INFO lines"
    )

    args = parser.parse_args()
    result = ValidationResult()

    if args.mode == "strict":
        if not args.paths:
            print("ERROR: --mode strict requires explicit PATH arguments", file=sys.stderr)
            sys.exit(2)
        schema = load_schema(args.schema)
        validate_strict(args.paths, schema, result)
    else:  # legacy-compat
        paths = args.paths if args.paths else (find_intelligence_files("legacy-compat") if args.all else [])
        if not paths:
            print("WARNING: No files to validate", file=sys.stderr)
        validate_legacy_compat(paths, result)

    result.print_report(format_type=args.format, quiet=args.quiet)

    if result.has_errors():
        sys.exit(1)
    elif args.strict_warnings and result.warnings:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
