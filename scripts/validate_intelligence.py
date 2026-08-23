#!/usr/bin/env python3
"""Dependency-free validation for canonical v1 leads and legacy intelligence feeds."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
STAGES = {
    "RADAR", "QUALIFICATION", "QUALIFIED", "REVIEW", "REJECTED",
    "ENRICHMENT", "ENRICHED", "ORCHESTRATION", "SALES_READY", "ENGAGEMENT",
}
TRANSITIONS = {
    None: {"RADAR"},
    "RADAR": {"QUALIFICATION", "REJECTED"},
    "QUALIFICATION": {"QUALIFIED", "REVIEW", "REJECTED"},
    "REVIEW": {"QUALIFICATION", "QUALIFIED", "REJECTED"},
    "QUALIFIED": {"ENRICHMENT", "REJECTED"},
    "ENRICHMENT": {"ENRICHED", "REVIEW", "REJECTED"},
    "ENRICHED": {"ORCHESTRATION", "REJECTED"},
    "ORCHESTRATION": {"SALES_READY", "REVIEW", "REJECTED"},
    "SALES_READY": {"ENGAGEMENT", "REVIEW", "REJECTED"},
    "ENGAGEMENT": {"REVIEW", "REJECTED"},
    "REJECTED": set(),
}
LEGACY_ID = re.compile(
    r"^(IND-\d{8}-\d{1,4}|OPP?-\d{4}-?\d{2}-?\d{2}-\d{3,4}|"
    r"ML-\d{8}-\d{4}|[A-Z]{1,12}(?:-[A-Za-z0-9]+)+)$"
)
EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
TOP_LEVEL_FIELDS = {
    "contract_version", "lead_id", "lead_type", "created_at", "updated_at",
    "pipeline_stage", "company", "project", "signal", "evidence",
    "qualification", "enrichment", "provenance", "pipeline_history",
    "duplicate_of", "conflicts", "sales_feedback",
}
QUALIFICATION_STAGES = {
    "PASS": {"QUALIFIED", "ENRICHMENT", "ENRICHED", "ORCHESTRATION", "SALES_READY", "ENGAGEMENT"},
    "REVIEW": {"REVIEW"},
    "REJECT": {"REJECTED"},
}
ENRICHMENT_STAGES = {
    "PENDING": {"ENRICHMENT", "REVIEW"},
    "IN_PROGRESS": {"ENRICHMENT", "REVIEW"},
    "PARTIAL": {"ENRICHMENT", "REVIEW"},
    "COMPLETE": {"ENRICHED", "ORCHESTRATION", "SALES_READY", "ENGAGEMENT"},
}


@dataclass(frozen=True)
class Finding:
    severity: str
    path: str
    message: str

    def __str__(self) -> str:
        location = f" [{self.path}]" if self.path else ""
        return f"{self.severity}{location}: {self.message}"


def finding(severity: str, path: str, message: str) -> Finding:
    return Finding(severity, path, message)


def valid_timestamp(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return "T" in value
    except ValueError:
        return False


def valid_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def valid_url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def require(obj: dict[str, Any], keys: Iterable[str], base: str, out: list[Finding]) -> None:
    for key in keys:
        if key not in obj:
            out.append(finding("ERROR", f"{base}.{key}".strip("."), "missing required field"))


def reject_unknown(obj: dict[str, Any], allowed: set[str], base: str, out: list[Finding]) -> None:
    for key in sorted(set(obj) - allowed):
        out.append(finding("ERROR", f"{base}.{key}".strip("."), "unexpected property"))


def as_list(value: Any, path: str, out: list[Finding]) -> list[Any]:
    if isinstance(value, list):
        return value
    out.append(finding("ERROR", path, "must be an array"))
    return []


def validate_transition(previous: str | None, current: str) -> bool:
    return current in TRANSITIONS.get(previous, set())


def _validate_contact(contact: Any, index: int, evidence_ids: set[str], provenance_ids: set[str], out: list[Finding]) -> None:
    base = f"enrichment.contacts[{index}]"
    if not isinstance(contact, dict):
        out.append(finding("ERROR", base, "contact must be an object"))
        return
    reject_unknown(contact, {"contact_id", "name", "title", "organization", "role_category", "phone", "phone_status", "email", "email_status", "confidence", "evidence_refs", "provenance_ref"}, base, out)
    require(contact, ("contact_id", "name", "title", "organization", "role_category", "phone", "phone_status", "email", "email_status", "confidence", "evidence_refs"), base, out)
    for channel in ("phone", "email"):
        status = contact.get(f"{channel}_status")
        value = contact.get(channel)
        if status not in {"KNOWN", "UNKNOWN", "NOT_FOUND", "WITHHELD"}:
            out.append(finding("ERROR", f"{base}.{channel}_status", "invalid availability status"))
        if status == "KNOWN" and not value:
            out.append(finding("ERROR", f"{base}.{channel}", "KNOWN requires a value"))
        if status in {"UNKNOWN", "NOT_FOUND", "WITHHELD"} and value is not None:
            out.append(finding("ERROR", f"{base}.{channel}", f"{status} requires null"))
    phone = contact.get("phone")
    if phone and (len(re.sub(r"\D", "", str(phone))) < 7 or re.search(r"[^0-9+()\-\s]", str(phone))):
        out.append(finding("WARNING", f"{base}.phone", "phone format appears malformed"))
    email = contact.get("email")
    if email and not EMAIL.fullmatch(str(email)):
        out.append(finding("WARNING", f"{base}.email", "email format appears malformed"))
    for ref in as_list(contact.get("evidence_refs", []), f"{base}.evidence_refs", out):
        if ref not in evidence_ids:
            out.append(finding("ERROR", f"{base}.evidence_refs", f"unknown evidence reference: {ref}"))
    prov = contact.get("provenance_ref")
    if prov is not None and prov not in provenance_ids:
        out.append(finding("ERROR", f"{base}.provenance_ref", f"unknown provenance reference: {prov}"))


def validate_v1(data: Any) -> list[Finding]:
    out: list[Finding] = []
    if not isinstance(data, dict):
        return [finding("ERROR", "", "lead document must be an object")]
    reject_unknown(data, TOP_LEVEL_FIELDS, "", out)
    required = ("contract_version", "lead_id", "lead_type", "created_at", "updated_at", "pipeline_stage", "evidence", "provenance", "pipeline_history")
    require(data, required, "", out)
    if data.get("contract_version") != "1.0":
        out.append(finding("ERROR", "contract_version", "must equal 1.0"))
    lead_id = data.get("lead_id")
    if not isinstance(lead_id, str) or not LEGACY_ID.fullmatch(lead_id):
        out.append(finding("ERROR", "lead_id", "unsupported Lead ID format"))
    if data.get("lead_type") not in {"industrial", "municipal", "other"}:
        out.append(finding("ERROR", "lead_type", "must be industrial, municipal, or other"))
    for key in ("created_at", "updated_at"):
        if key in data and not valid_timestamp(data[key]):
            out.append(finding("ERROR", key, "must be an ISO 8601 date-time"))
    stage = data.get("pipeline_stage")
    if stage not in STAGES:
        out.append(finding("ERROR", "pipeline_stage", "invalid pipeline stage"))

    for key, allowed in (
        ("company", {"company_name", "normalized_company_name", "location", "industry"}),
        ("project", {"project_name", "project_type", "project_location", "project_stage", "estimated_timing"}),
        ("signal", {"signal_type", "signal_description", "signal_date"}),
    ):
        value = data.get(key)
        if value is not None:
            if not isinstance(value, dict):
                out.append(finding("ERROR", key, "must be an object"))
            else:
                reject_unknown(value, allowed, key, out)

    evidence = as_list(data.get("evidence", []), "evidence", out)
    evidence_ids: set[str] = set()
    fingerprints: set[tuple[str, str]] = set()
    for index, item in enumerate(evidence):
        base = f"evidence[{index}]"
        if not isinstance(item, dict):
            out.append(finding("ERROR", base, "must be an object"))
            continue
        reject_unknown(item, {"evidence_id", "source_name", "source_url", "source_type", "published_at", "retrieved_at", "evidence_text", "evidence_summary", "confidence", "contributed_by"}, base, out)
        require(item, ("evidence_id", "source_name", "source_url", "source_type", "retrieved_at", "evidence_summary", "confidence"), base, out)
        evidence_id = item.get("evidence_id")
        if evidence_id in evidence_ids:
            out.append(finding("ERROR", f"{base}.evidence_id", f"duplicate evidence ID: {evidence_id}"))
        elif isinstance(evidence_id, str):
            evidence_ids.add(evidence_id)
        url = item.get("source_url")
        if url is not None and not valid_url(url):
            out.append(finding("ERROR", f"{base}.source_url", "must be an HTTP(S) URL"))
        if "retrieved_at" in item and not valid_timestamp(item["retrieved_at"]):
            out.append(finding("ERROR", f"{base}.retrieved_at", "must be an ISO 8601 date-time"))
        published = item.get("published_at")
        if published is not None and not (valid_timestamp(published) or valid_date(published)):
            out.append(finding("ERROR", f"{base}.published_at", "must be an ISO 8601 date or date-time"))
        fp = (str(url).rstrip("/"), str(item.get("evidence_summary", "")).strip().casefold())
        if fp in fingerprints:
            out.append(finding("WARNING", base, "obvious duplicate evidence (same URL and summary)"))
        fingerprints.add(fp)

    provenance = data.get("provenance", [])
    if not isinstance(provenance, list) or not provenance:
        out.append(finding("ERROR", "provenance", "must contain at least one contribution"))
        provenance = []
    provenance_ids: set[str] = set()
    for index, item in enumerate(provenance):
        base = f"provenance[{index}]"
        if not isinstance(item, dict):
            out.append(finding("ERROR", base, "must be an object"))
            continue
        reject_unknown(item, {"contribution_id", "generated_by", "agent", "model", "run_id", "generated_at", "prompt_version", "evidence_refs", "notes"}, base, out)
        require(item, ("contribution_id", "generated_by", "agent", "run_id", "generated_at"), base, out)
        contribution_id = item.get("contribution_id")
        if contribution_id in provenance_ids:
            out.append(finding("ERROR", f"{base}.contribution_id", f"duplicate contribution ID: {contribution_id}"))
        elif isinstance(contribution_id, str):
            provenance_ids.add(contribution_id)
        if item.get("generated_by") not in {"AI", "HUMAN", "SYSTEM", "IMPORT"}:
            out.append(finding("ERROR", f"{base}.generated_by", "invalid generator type"))
        if "generated_at" in item and not valid_timestamp(item["generated_at"]):
            out.append(finding("ERROR", f"{base}.generated_at", "must be an ISO 8601 date-time"))
        for ref in as_list(item.get("evidence_refs", []), f"{base}.evidence_refs", out):
            if ref not in evidence_ids:
                out.append(finding("ERROR", f"{base}.evidence_refs", f"unknown evidence reference: {ref}"))

    qualification = data.get("qualification")
    if qualification is not None:
        if not isinstance(qualification, dict):
            out.append(finding("ERROR", "qualification", "must be an object"))
        else:
            reject_unknown(qualification, {"decision", "dimensions", "reasoning", "evidence_refs", "confidence", "qualified_at", "provenance_ref", "rule_version", "prompt_version"}, "qualification", out)
            require(qualification, ("decision", "reasoning", "confidence", "qualified_at", "evidence_refs", "provenance_ref"), "qualification", out)
            decision = qualification.get("decision")
            if decision not in {"PASS", "REVIEW", "REJECT"}:
                out.append(finding("ERROR", "qualification.decision", "must be PASS, REVIEW, or REJECT"))
            elif stage not in QUALIFICATION_STAGES[decision]:
                allowed = ", ".join(sorted(QUALIFICATION_STAGES[decision]))
                out.append(finding("ERROR", "qualification.decision", f"{decision} is inconsistent with pipeline stage {stage}; expected one of: {allowed}"))
            dimensions = qualification.get("dimensions")
            if dimensions is not None:
                if not isinstance(dimensions, dict):
                    out.append(finding("ERROR", "qualification.dimensions", "must be an object"))
                else:
                    reject_unknown(dimensions, {"icp_fit", "pain", "timing", "ims_fit", "commercial_relevance"}, "qualification.dimensions", out)
            if "qualified_at" in qualification and not valid_timestamp(qualification["qualified_at"]):
                out.append(finding("ERROR", "qualification.qualified_at", "must be an ISO 8601 date-time"))
            for ref in as_list(qualification.get("evidence_refs", []), "qualification.evidence_refs", out):
                if ref not in evidence_ids:
                    out.append(finding("ERROR", "qualification.evidence_refs", f"unknown evidence reference: {ref}"))
            if qualification.get("provenance_ref") not in provenance_ids:
                out.append(finding("ERROR", "qualification.provenance_ref", "unknown provenance reference"))

    enrichment = data.get("enrichment")
    if enrichment is not None:
        if not isinstance(enrichment, dict):
            out.append(finding("ERROR", "enrichment", "must be an object"))
        else:
            reject_unknown(enrichment, {"status", "organizations", "contacts", "notes"}, "enrichment", out)
            require(enrichment, ("status", "organizations", "contacts"), "enrichment", out)
            status = enrichment.get("status")
            if status not in ENRICHMENT_STAGES:
                out.append(finding("ERROR", "enrichment.status", "invalid enrichment status"))
            elif stage not in ENRICHMENT_STAGES[status]:
                allowed = ", ".join(sorted(ENRICHMENT_STAGES[status]))
                out.append(finding("ERROR", "enrichment.status", f"{status} is inconsistent with pipeline stage {stage}; expected one of: {allowed}"))
            contacts = as_list(enrichment.get("contacts", []), "enrichment.contacts", out)
            organizations = as_list(enrichment.get("organizations", []), "enrichment.organizations", out)
            for index, contact in enumerate(contacts):
                _validate_contact(contact, index, evidence_ids, provenance_ids, out)
            for oi, org in enumerate(organizations):
                base = f"enrichment.organizations[{oi}]"
                if not isinstance(org, dict):
                    out.append(finding("ERROR", base, "organization must be an object"))
                    continue
                reject_unknown(org, {"organization_id", "name", "relationship_type", "relationship_description", "confidence", "evidence_refs"}, base, out)
                require(org, ("organization_id", "name", "relationship_type", "confidence", "evidence_refs"), base, out)
                for ref in as_list(org.get("evidence_refs", []), f"{base}.evidence_refs", out):
                    if ref not in evidence_ids:
                        out.append(finding("ERROR", f"{base}.evidence_refs", f"unknown evidence reference: {ref}"))

    history = as_list(data.get("pipeline_history", []), "pipeline_history", out)
    if not history:
        out.append(finding("ERROR", "pipeline_history", "must contain START -> RADAR and all subsequent transitions"))
    previous: str | None = None
    for index, transition in enumerate(history):
        base = f"pipeline_history[{index}]"
        if not isinstance(transition, dict):
            out.append(finding("ERROR", base, "must be an object"))
            continue
        reject_unknown(transition, {"from", "to", "at", "reason", "provenance_ref"}, base, out)
        require(transition, ("from", "to", "at", "provenance_ref"), base, out)
        source, target = transition.get("from"), transition.get("to")
        if source != previous:
            out.append(finding("ERROR", f"{base}.from", f"expected {previous!r}, got {source!r}"))
        if not validate_transition(source, target):
            out.append(finding("ERROR", base, f"invalid pipeline transition: {source or 'START'} -> {target}"))
        if transition.get("provenance_ref") not in provenance_ids:
            out.append(finding("ERROR", f"{base}.provenance_ref", "unknown provenance reference"))
        if "at" in transition and not valid_timestamp(transition["at"]):
            out.append(finding("ERROR", f"{base}.at", "must be an ISO 8601 date-time"))
        previous = target
    if history and stage in STAGES and previous != stage:
        out.append(finding("ERROR", "pipeline_stage", f"does not match history terminal stage {previous}"))

    for index, conflict in enumerate(as_list(data.get("conflicts", []), "conflicts", out)):
        if not isinstance(conflict, dict):
            out.append(finding("ERROR", f"conflicts[{index}]", "must be an object"))
            continue
        reject_unknown(conflict, {"field", "values", "status", "resolution"}, f"conflicts[{index}]", out)
        values = as_list(conflict.get("values", []), f"conflicts[{index}].values", out)
        if len(values) < 2:
            out.append(finding("ERROR", f"conflicts[{index}]", "must preserve at least two conflicting values"))
        else:
            for vi, value in enumerate(values):
                if not isinstance(value, dict):
                    out.append(finding("ERROR", f"conflicts[{index}].values[{vi}]", "must be an object"))
                    continue
                reject_unknown(value, {"value", "evidence_refs"}, f"conflicts[{index}].values[{vi}]", out)
                for ref in as_list(value.get("evidence_refs", []), f"conflicts[{index}].values[{vi}].evidence_refs", out):
                    if ref not in evidence_ids:
                        out.append(finding("ERROR", f"conflicts[{index}].values[{vi}].evidence_refs", f"unknown evidence reference: {ref}"))

    for index, feedback in enumerate(as_list(data.get("sales_feedback", []), "sales_feedback", out)):
        base = f"sales_feedback[{index}]"
        if not isinstance(feedback, dict):
            out.append(finding("ERROR", base, "must be an object"))
            continue
        reject_unknown(feedback, {"outcome", "recorded_at", "recorded_by", "notes"}, base, out)

    if not evidence:
        out.append(finding("WARNING", "evidence", "lead has no evidence yet"))
    return out


def validate_legacy(data: Any) -> list[Finding]:
    out: list[Finding] = []
    if not isinstance(data, dict):
        return [finding("ERROR", "", "legacy report must be an object")]
    if "signals" in data:
        items, collection = data.get("signals"), "signals"
    elif "opportunities" in data:
        items, collection = data.get("opportunities"), "opportunities"
    elif "metadata" in data and "leads" in data:
        items, collection = data.get("leads"), "leads"
    else:
        return [finding("ERROR", "", "unrecognized document shape")]
    if not isinstance(items, list):
        return [finding("ERROR", collection, "must be an array")]
    seen: set[str] = set()
    for index, item in enumerate(items):
        base = f"{collection}[{index}]"
        if not isinstance(item, dict):
            out.append(finding("ERROR", base, "must be an object"))
            continue
        lead_id = item.get("lead_id") or item.get("id")
        if not lead_id:
            out.append(finding("ERROR", base, "missing legacy lead ID"))
        elif lead_id in seen:
            out.append(finding("WARNING", base, f"duplicate legacy lead ID in collection: {lead_id}"))
        else:
            seen.add(str(lead_id))
        urls: list[Any] = []
        if "source_url" in item:
            urls.append(item["source_url"])
        urls.extend(item.get("source_urls", []))
        for url in urls:
            if not valid_url(url):
                out.append(finding("WARNING", base, f"malformed source URL: {url!r}"))
    out.append(finding("INFO", "", "legacy interface accepted; canonical v1 fields are not required"))
    return out


def validate_document(data: Any) -> list[Finding]:
    if isinstance(data, dict) and "contract_version" in data:
        return validate_v1(data)
    return validate_legacy(data)


def default_paths() -> list[Path]:
    paths = sorted((ROOT / "tests" / "fixtures").glob("*.json"))
    paths.extend([
        ROOT / "intelligence" / "industrial" / "ind_latest.json",
        ROOT / "intelligence" / "municipal" / "latest.json",
        ROOT / "intelligence" / "industrial" / "enriched" / "indctx_latest.json",
        ROOT / "intelligence" / "municipal" / "enriched" / "ctx_latest.json",
    ])
    return paths


def expand_paths(paths: Iterable[Path]) -> list[Path]:
    expanded: list[Path] = []
    for path in paths:
        if path.is_dir():
            expanded.extend(sorted(item for item in path.rglob("*.json") if item.name != "schema.json"))
        else:
            expanded.append(path)
    return expanded


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="JSON files (defaults to fixtures and current latest feeds)")
    parser.add_argument("--strict-warnings", action="store_true", help="return non-zero when warnings exist")
    args = parser.parse_args(argv)
    paths = expand_paths(args.paths) if args.paths else default_paths()
    error_count = warning_count = 0
    for path in paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
            findings = validate_document(data)
        except (OSError, json.JSONDecodeError) as exc:
            findings = [finding("ERROR", "", str(exc))]
        print(f"\n{path}")
        if not findings:
            print("OK")
        for item in findings:
            print(item)
            error_count += item.severity == "ERROR"
            warning_count += item.severity == "WARNING"
    print(f"\nValidated {len(paths)} file(s): {error_count} error(s), {warning_count} warning(s)")
    return 1 if error_count or (args.strict_warnings and warning_count) else 0


if __name__ == "__main__":
    sys.exit(main())
