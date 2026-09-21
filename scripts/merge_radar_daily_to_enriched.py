#!/usr/bin/env python3
"""Merge Radar daily discoveries into the enriched master (incremental, idempotent).

Purpose
-------
The Radar tasks (industrial: job_1594ac48, municipal: job_14c6b43e) publish
daily JSON files only.  The public lead page is built from the enriched
master (+ genuine new daily rows).  This script closes the loop so a daily
radar run can, by itself:

  1. read the latest enriched master (canonical *_latest_jd_*.json for
     industrial, *_latest.json otherwise),
  2. merge every daily signal/opportunity whose lead id is not yet present
     (or whose record has a stale status) into the master as a proper
     enriched lead,
  3. emit a new canonical master file and keep *_latest.json in sync,
  4. run the public build and print the quality-score distribution so the
     task agent can verify 4-5/5 coverage before pushing.

The script is strictly incremental and idempotent: re-running it against the
same daily files changes nothing.  It never fabricates facts, contacts or
URLs; stage-3 contact evidence must be supplied by the radar task's own
websearch and stored on the daily signal (stage3_handoff / jd_inferences /
contacts) before merging.

Usage
-----
  python3 scripts/merge_radar_daily_to_enriched.py --segment industrial [--dry-run]
  python3 scripts/merge_radar_daily_to_enriched.py --segment municipal [--dry-run]

Legacy behavior preserved:
  * industrial master: emits indctx_latest_jd_<date>.json and mirrors it to
    indctx_latest.json (the public build prefers the _latest_jd_ file);
  * municipal master: updates indctx_latest.json in place.
"""
import argparse
import copy
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

DAILY_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})\.json$")

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def norm(value):
    return re.sub(r"[^\w\u4e00-\u9fff]", "", str(value or "")).lower()


def pick_first(signal, *keys):
    for key in keys:
        if signal.get(key):
            return signal[key]
    return ""


def raw_location(sig):
    loc = sig.get("location")
    if isinstance(loc, dict):
        return str(loc.get("raw") or "")
    return str(loc or "")


def parse_evidence(sig):
    evidence = sig.get("evidence") or {}
    if not isinstance(evidence, dict):
        evidence = {"facts": evidence or []}
    facts = evidence.get("facts") or sig.get("public_facts") or []
    if isinstance(facts, str):
        facts = [facts]
    inferences = evidence.get("inferences") or []
    if isinstance(inferences, str):
        inferences = [inferences]
    unknowns = evidence.get("unknowns") or []
    if isinstance(unknowns, str):
        unknowns = [unknowns]
    return {"facts": list(facts), "inferences": list(inferences), "unknowns": list(unknowns)}


def build_lead_from_industrial_signal(sig, source_file, today):
    """Map an industrial radar daily signal into an enriched lead row."""
    evidence = parse_evidence(sig)
    opportunity = pick_first(sig, "opportunity", "opportunity_project", "project", "trigger")
    location = sig.get("location") or {}
    if not isinstance(location, dict):
        location = {"raw": location}
    stage3 = sig.get("stage3_handoff") or {}
    if not isinstance(stage3, dict):
        stage3 = {}
    # Carry every sales-usable field the radar already recorded.  Nothing is
    # invented here: missing values stay missing and are reported by the build.
    handoff_evidence = []
    for role, label in (("account_owner", "业主"), ("design_institute", "设计院"), ("epc", "EPC"), ("instrument_integrator", "仪表集成商")):
        node = stage3.get(role) or {}
        if isinstance(node, dict):
            eval_tag = str(node.get("evaluation") or "UNKNOWN").upper()
            note = str(node.get("note") or "").strip()
            if eval_tag != "UNKNOWN" and note and note.lower() != "n/a":
                handoff_evidence.append("[%s] %s: %s" % (label, eval_tag, note))
    signal = copy.deepcopy(sig)
    signal["opportunity"] = opportunity
    signal["evidence"] = evidence
    signal["source_urls"] = list(dict.fromkeys([u for u in (sig.get("source_urls") or []) if u]))
    signal["estimated_time_window"] = pick_first(sig, "estimated_time_window", "influence_window")
    signal["time_window_basis"] = pick_first(sig, "time_window_basis", "influence_window_evidence")
    if isinstance(signal["time_window_basis"], dict):
        signal["time_window_basis"] = signal["time_window_basis"].get("note") or signal["time_window_basis"].get("source") or ""
    pull = sig.get("pull_box") or {}
    if isinstance(pull, dict):
        for key, pull_key in (("customer_requirement", "P"), ("operational_pain_points", "L1"), ("sales_summary", "L2")):
            if pull.get(pull_key):
                signal[key] = str(pull[pull_key])
    jd_inferences = signal.get("jd_inferences") or []
    if not jd_inferences and handoff_evidence:
        jd_inferences = [{
            "job_title": "下游利益相关方角色（Radar stage3_handoff）",
            "role_duties": "；".join(handoff_evidence)[:300],
            "software_need": "",
            "confidence": "MEDIUM",
            "source_url": (sig.get("source_urls") or [""])[0],
        }]
    first_seen = today
    if isinstance(sig.get("continuity"), dict) and sig["continuity"].get("first_seen"):
        first_seen = sig["continuity"]["first_seen"]
    lead = {
        "lead_id": sig.get("id"),
        "original_signal": signal,
        "enrichment_status": "sales_usable_enriched",
        "record_status": "active",
        "status": "active",
        "status_reason": "Radar daily merged by merge_radar_daily_to_enriched",
        "first_seen": first_seen,
        "last_updated": today,
        "source_lead_ids": [sig.get("id")],
        "source_files": [source_file],
        "segments": ["industrial"],
        "region_raw": [str(location.get("raw") or "")],
        "industry_raw": [str(sig.get("industry") or "")],
        "location": location,
        "industry": sig.get("industry") or "",
        "customer_requirement": signal.get("customer_requirement") or "",
        "operational_pain_points": signal.get("operational_pain_points") or "",
        "sales_summary": signal.get("sales_summary") or "",
        "estimated_time_window": signal.get("estimated_time_window") or "",
        "time_window_basis": signal.get("time_window_basis") or "",
        "jd_inferences": jd_inferences,
        "next_validation_questions": ((stage3.get("next_validation_action") or "") if isinstance(stage3, dict) else ""),
        "history": [{"date": source_file.replace(".json", ""), "source_file": source_file, "record_id": sig.get("id"), "name": opportunity}],
        "priority": pick_first(sig, "priority", "signal_tier") or "P2",
    }
    return lead


def build_lead_from_municipal_opportunity(item, source_file, today, seq):
    """Map a municipal radar daily opportunity into an enriched lead row."""
    name = item.get("name") or item.get("opportunity") or ""
    lid = item.get("id") or item.get("opportunity_id") or "MUN-DAILY-%s-%03d" % (source_file.replace(".json", ""), seq)
    facts = item.get("public_facts") or []
    if isinstance(facts, str):
        facts = [facts]
    action_triad = item.get("action_triad") or {}
    if not isinstance(action_triad, dict):
        action_triad = {}
    logic = item.get("logic_chain_check") or item.get("ai_judgment") or ""
    demand = item.get("ai_judgment") or (action_triad.get("talk_what") if action_triad else None) or logic
    source_url = item.get("source_url") or ""
    signal = {
        "company": name,
        "opportunity": name,
        "industry": "市政水务",
        "opportunity_stage": item.get("opportunity_stage"),
        "priority": item.get("priority") or item.get("score"),
        "potential_ims_use_case": item.get("potential_ims_use_case"),
        "logic": logic,
        "to_verify": item.get("to_verify") or item.get("agent_checklist"),
        "customer_need": logic,
        "demand_hypothesis": demand,
        "contact_hint": action_triad.get("find_who") if action_triad else None,
        "estimated_time_window": item.get("estimated_time_window"),
        "time_window_basis": item.get("estimated_time_window_basis") or item.get("time_window_basis"),
        "source_urls": [source_url] if source_url else [],
        "evidence": {"facts": list(facts), "inferences": [item.get("ai_judgment")] if item.get("ai_judgment") else [], "unknowns": []},
        "action_triad": action_triad,
        "enrichment": item.get("enrichment") or item.get("stage3_enrichment") or {},
    }
    first_seen = today
    if isinstance(item.get("continuity"), dict) and item["continuity"].get("first_seen"):
        first_seen = item["continuity"]["first_seen"]
    lead = {
        "lead_id": lid,
        "original_signal": signal,
        "enrichment_status": "consolidated_from_radar_daily",
        "record_status": "active",
        "status": "active",
        "status_reason": "Radar daily merged by merge_radar_daily_to_enriched",
        "first_seen": first_seen,
        "last_updated": today,
        "source_lead_ids": [lid],
        "source_files": [source_file],
        "segments": ["municipal"],
        "region_raw": [str(item.get("region") or item.get("location") or "")],
        "industry_raw": ["市政水务"],
        "location": item.get("region") or item.get("location") or name,
        "industry": "市政水务",
        "customer_requirement": item.get("potential_ims_use_case") or "",
        "next_validation_questions": (action_triad.get("talk_what") if action_triad else "") or "",
        "history": [{"date": source_file.replace(".json", ""), "source_file": source_file, "record_id": lid, "name": name}],
    }
    return lead


def ensure_link_entities(master, lead, company, project_name):
    """Create project/account entities for a lead if missing (idempotent)."""
    lid = lead["lead_id"]
    pid = "PRJ-%s" % lid
    aid = "ACC-%s" % lid
    projects = master.get("projects") or []
    accounts = master.get("accounts") or []
    pids = {p.get("project_id") for p in projects}
    aids = {a.get("account_id") for a in accounts}
    if pid not in pids:
        projects.append({
            "project_id": pid, "lead_id": lid, "account_id": aid,
            "project_name": project_name or "", "owner": company or "",
            "investment_amount": "unknown",
            "project_status": "merged from radar daily",
            "water_system_details": {"confirmed": False, "description": lead.get("customer_requirement", "")},
        })
    if aid not in aids:
        accounts.append({
            "account_id": aid, "lead_id": lid, "account_name": company or "",
            "group_name": "", "industry": lead.get("industry", ""),
            "plant_location": "", "products": [], "contact_ids": [],
        })
    lead["project_ids"] = [pid]
    lead["account_ids"] = [aid]
    master["projects"] = projects
    master["accounts"] = accounts


def canonical_path(segment):
    directory = ROOT / "intelligence" / segment / "enriched"
    files = sorted(directory.glob("indctx*.json"), key=lambda p: p.name)
    if not files:
        raise SystemExit("no enriched master found under %s" % directory)
    canonical = next((p for p in reversed(files) if "_latest_jd_" in p.name), None)
    if canonical is None:
        canonical = next((p for p in files if p.name.endswith("_latest.json")), None)
    if canonical is None:
        canonical = files[-1]
    return directory, canonical


def resolve_merge_point(master, segment, since):
    """Determine the daily merge window start date.

    Only daily files *after* the given point are merged, so historical rows
    that already render well via the daily branch are never touched.  Priority:
    explicit --since > master merge metadata > legacy previous_version.
    """
    if since:
        return since
    meta = master.get("metadata") or {}
    if meta.get("merge_point"):
        return meta["merge_point"]
    prev = meta.get("previous_version")
    if prev and re.fullmatch(r"\d{8}", str(prev)):
        return "%s-%s-%s" % (str(prev)[:4], str(prev)[4:6], str(prev)[6:8])
    gen = meta.get("generated_date")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(gen)):
        return str(gen)
    return "2000-01-01"


def merge_daily(segment, dry_run, since=None):
    today = datetime.now().strftime("%Y-%m-%d")
    directory, master_path = canonical_path(segment)
    master = read(master_path)
    merge_point = resolve_merge_point(master, segment, since)
    leads = {l.get("lead_id"): l for l in master.get("leads", []) if l.get("lead_id")}
    daily_dir = ROOT / "intelligence" / segment / "daily"
    daily_files = sorted((p for p in daily_dir.glob("*.json") if DAILY_NAME.match(p.name)),
                         key=lambda p: p.name)
    added, updated, skipped, filtered = 0, 0, 0, 0
    max_daily = merge_point

    def lookup_known(value):
        return any(norm(value) and (norm(value) == k or norm(value) in k or k in norm(value)) for k in leads)

    for path in daily_files:
        fname = path.name
        m = DAILY_NAME.match(fname)
        if m is None:
            filtered += 1
            continue
        fdate = m.group(1)
        if fdate <= merge_point:
            filtered += 1
            continue
        if fdate > max_daily:
            max_daily = fdate
        try:
            daily = read(path)
        except Exception as exc:  # noqa: BLE001
            print("WARN: skip %s (%s)" % (fname, exc))
            continue
        if segment == "industrial":
            signals = daily.get("signals") or []
            for sig in signals:
                lid = sig.get("id")
                if not lid:
                    continue
                if lid in leads:
                    skipped += 1
                    continue
                lead = build_lead_from_industrial_signal(sig, fname, today)
                leads[lid] = lead
                ensure_link_entities(master, lead, sig.get("company"), lead["original_signal"].get("opportunity", ""))
                added += 1
        else:
            items = daily.get("opportunities") or daily.get("signals") or []
            for number, item in enumerate(items, 1):
                lid = item.get("id") or item.get("opportunity_id")
                name = item.get("name") or item.get("opportunity") or ""
                if not lid or not name:
                    continue
                if lid in leads or (name and lookup_known(name)):
                    skipped += 1
                    continue
                lead = build_lead_from_municipal_opportunity(item, fname, today, number)
                leads[lead["lead_id"]] = lead
                ensure_link_entities(master, lead, name, name)
                added += 1

    master["leads"] = list(leads.values())

    # keep top-level audit fields from being stale
    meta = master.get("metadata") or {}
    meta["generated_date"] = today
    meta["last_update"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    meta["note"] = "merge_radar_daily_to_enriched: incremental radar daily merge (window after %s; %d added, %d skipped, %d pre-window)" % (merge_point, added, skipped, filtered)
    master["metadata"] = meta
    history = master.get("enrichment_history") or []
    if added:
        history.append({
            "date": today, "version": "radar-daily-merge",
            "agent": "merge_radar_daily_to_enriched",
            "action": "incremental radar daily merge",
            "new_leads_added": added, "new_contacts_added": 0,
            "sources": [p.name for p in daily_files if p.name > merge_point],
            "notes": "automated merge of radar daily output into enriched master (window after %s)" % merge_point,
        })
    master["enrichment_history"] = history

    if dry_run:
        print("[dry-run] %s: would add %d lead(s), skip %d, pre-window %d (merge point %s)" % (segment, added, skipped, filtered, merge_point))
        return master, master_path, False

    if segment == "industrial":
        out_jd = directory / ("indctx_latest_jd_%s.json" % today)
        master["metadata"]["merge_point"] = max_daily if max_daily > merge_point else merge_point
        write(out_jd, master)
        write(directory / "indctx_latest.json", master)
        print("industrial: leads=%d (+%d), skipped=%d, pre-window=%d -> %s (latest.json synced)" % (
            len(leads), added, skipped, filtered, out_jd.name))
    else:
        master["metadata"]["merge_point"] = max_daily if max_daily > merge_point else merge_point
        write(master_path, master)
        print("municipal: leads=%d (+%d), skipped=%d, pre-window=%d -> %s" % (len(leads), added, skipped, filtered, master_path.name))
    return master, master_path, True


def run_build_and_report():
    """Run the public build and report the quality distribution."""
    print("== running build_industrial_pipeline_view.py ==")
    build = ROOT / "scripts" / "build_industrial_pipeline_view.py"
    subprocess.run([sys.executable, str(build)], cwd=str(ROOT), check=True)
    data_file = ROOT / "customer" / "industrial-leads" / "leads-data.json"
    if not data_file.exists():
        print("WARN: leads-data.json not found after build")
        return
    data = read(data_file)
    rows = data.get("leads", [])
    dist = {}
    for row in rows:
        dist[row.get("quality_score") or 0] = dist.get(row.get("quality_score") or 0, 0) + 1
    print("quality distribution (all %d rows): %s" % (len(rows), dict(sorted(dist.items(), reverse=True))))
    low = [r for r in rows if (r.get("quality_score") or 0) <= 3]
    if low:
        print("rows <=3: %d -> %s" % (len(low), [(r.get("lead", {}) or {}).get("lead_id") for r in low][:10]))


def main():
    parser = argparse.ArgumentParser(description="Merge radar daily into enriched master")
    parser.add_argument("--segment", choices=("industrial", "municipal"), required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--since", default=None, help="YYYY-MM-DD: only merge daily files after this date")
    args = parser.parse_args()
    master, master_path, changed = merge_daily(args.segment, args.dry_run, since=args.since)
    print("master: %s (%d leads)" % (master_path.name, len(master.get("leads") or [])))
    if changed and not args.dry_run:
        run_build_and_report()


if __name__ == "__main__":
    main()