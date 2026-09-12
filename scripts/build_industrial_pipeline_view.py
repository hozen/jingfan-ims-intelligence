#!/usr/bin/env python3
"""Build the mobile-first, fact-first industrial lead view."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "customer/industrial-leads/index.html"
DATA = ROOT / "customer/industrial-leads/leads-data.json"
MANIFEST = ROOT / "customer/industrial-leads/pipeline-manifest.json"
ENRICHED = ROOT / "intelligence/industrial/enriched/indctx_latest.json"
DAILY = ROOT / "intelligence/industrial/daily"

def mask_name(value):
    if not value or not isinstance(value, str):
        return value
    chars = list(value.strip())
    if len(chars) <= 1:
        return "*" if chars else value
    return chars[0] + "*" * (len(chars) - 1)

def redact_contact_text(value):
    """Keep public contact context while masking personal names and hiding email."""
    if not isinstance(value, str):
        return value
    value = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[邮箱已隐藏]", value)
    return re.sub(r"(?<=[：:])([\u4e00-\u9fff])([\u4e00-\u9fff]{1,3})", lambda m: m.group(1) + "*" * len(m.group(2)), value)

def redact_daily_stage3(value):
    if isinstance(value, dict):
        return {k: redact_daily_stage3(v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact_daily_stage3(v) for v in value]
    return redact_contact_text(value)

def load_enriched_history():
    """Return the newest usable DuMate record for every Lead ID plus its provenance."""
    paths = sorted(p for p in ENRICHED.parent.glob("indctx*.json") if p.name != ENRICHED.name)
    paths.append(ENRICHED)  # latest is deliberately applied last
    records, history = {}, {}
    for path in paths:
        source = json.loads(path.read_text(encoding="utf-8"))
        contacts = {c.get("contact_id"): c for c in source.get("contacts", [])}
        projects = {p.get("project_id"): p for p in source.get("projects", [])}
        accounts = {a.get("account_id"): a for a in source.get("accounts", [])}
        snapshot_date = source.get("metadata", {}).get("generated_date") or path.stem
        for item in source.get("leads", []):
            lead_id = item.get("lead_id")
            if not lead_id:
                continue
            signal = item.get("original_signal") or {}
            if signal.get("to_verify") is not None and not isinstance(signal["to_verify"], list):
                signal["to_verify"] = [signal["to_verify"]]
            evidence = signal.get("evidence") or {}
            for field in ("facts", "inferences", "unknowns"):
                if evidence.get(field) is not None and not isinstance(evidence[field], list):
                    evidence[field] = [evidence[field]]
            history.setdefault(lead_id, []).append({"file": path.name, "date": snapshot_date})
            records[lead_id] = {"item": item, "contacts": contacts, "projects": projects, "accounts": accounts}
    return records, history

def model():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    # Fixture outputs without a linked industrial discovery record are useful
    # for testing only; they must not enter the industrial sales view.
    manifest["leads"] = [
        row for row in manifest["leads"]
        if row.get("stage1") != "SOURCE_NOT_LINKED"
    ]
    # Water Clay is an ICP-profile service, not a lead-stage service.  Keep the
    # industrial Radar and DuMate facts, but remove inherited pipeline wording.
    for row in manifest["leads"]:
        if row.get("stage3") == "BLOCKED":
            row["stage3"] = "NOT_RECORDED"
            row["stage3_detail"] = "DuMate 资料尚未补充。"
    enriched_records, enriched_history = load_enriched_history()
    existing = {row["lead"]["lead_id"] for row in manifest["leads"]}
    rows_by_id = {row["lead"]["lead_id"]: row for row in manifest["leads"]}
    for lead_id, bundle in enriched_records.items():
        item, contacts = bundle["item"], bundle["contacts"]
        projects, accounts = bundle["projects"], bundle["accounts"]
        if item.get("lead_id") in existing:
            continue
        sig = item.get("original_signal") or {}
        evidence = sig.get("evidence") or {}
        snapshot_dates = enriched_history.get(lead_id, [])
        snapshot_date = snapshot_dates[-1]["date"] if snapshot_dates else "未记录"
        row_lead = {"lead_id": item.get("lead_id"), "company": {"company_name": sig.get("company"), "location": sig.get("location"), "industry": sig.get("industry")}, "project": {"project_name": sig.get("opportunity"), "project_stage": sig.get("opportunity_stage")}, "signal": {"signal_description": sig.get("opportunity"), "signal_date": item.get("first_discovered") or snapshot_date}, "evidence": [{"source_url": url, "evidence_summary": "Enriched source URL"} for url in sig.get("source_urls", [])]}
        enriched_contacts = []
        for cid in item.get("contact_ids", []):
            if cid not in contacts:
                continue
            contact = json.loads(json.dumps(contacts[cid], ensure_ascii=False))
            contact["name"] = mask_name(contact.get("name"))
            contact.pop("email", None)
            enriched_contacts.append(contact)
        manifest["leads"].append({"date": row_lead["signal"]["signal_date"], "lead": row_lead, "stage1": "ENRICHED_SOURCE", "stage2": "NOT_RECORDED", "stage3": "ENRICHED", "stage2_detail": "Enriched record contains no Stage 2 decision for this Lead ID.", "stage3_detail": "DuMate 已补充资料。", "stage3_result": None, "enriched_record": item, "enriched_contacts": enriched_contacts, "enriched_projects": [projects[x] for x in item.get("project_ids", []) if x in projects], "enriched_accounts": [accounts[x] for x in item.get("account_ids", []) if x in accounts], "dumate_history": enriched_history.get(lead_id, []), "legacy_match": True})
        existing.add(item.get("lead_id"))
        rows_by_id[item.get("lead_id")] = manifest["leads"][-1]
    for path in sorted(DAILY.glob("*.json")):
        daily = json.loads(path.read_text(encoding="utf-8"))
        match = re.search(r"\d{4}-\d{2}-\d{2}", path.name)
        report_date = daily.get("report_date") or daily.get("date") or (match.group(0) if match else "未记录")
        for signal in daily.get("signals", []):
            lead_id = signal.get("id")
            if not lead_id:
                continue
            project = signal.get("project") or signal.get("opportunity") or signal.get("trigger")
            stage3 = signal.get("stage3_enrichment") or {}
            safe_signal = json.loads(json.dumps(signal, ensure_ascii=False))
            if "stage3_enrichment" in safe_signal:
                safe_signal["stage3_enrichment"] = redact_daily_stage3(stage3)
            display_record = {
                "original_signal": safe_signal,
                "enrichment_status": "RADAR_DAILY",
                "ims_recommendation": {
                    "ims_fit": signal.get("ims_fit"),
                    "recommended_action": (signal.get("pull_box") or {}).get("next_validation_question"),
                },
            }
            if stage3:
                display_record["日报附带资料"] = redact_daily_stage3(stage3)
            if lead_id in existing:
                # The legacy manifest often contains only a short summary.  A
                # same-ID Radar record is the authoritative discovery detail;
                # add it unless DuMate has already supplied a richer record.
                row = rows_by_id[lead_id]
                if not row.get("enriched_record"):
                    row["enriched_record"] = display_record
                    row["daily_contacts"] = redact_daily_stage3(stage3.get("contacts", {})) if isinstance(stage3, dict) else {}
                    row["daily_stage3"] = bool(stage3)
                    row["source_kind"] = "daily_radar"
                    if stage3:
                        row["stage3"] = "DAILY_ENRICHMENT"
                        row["stage3_detail"] = "日报附带资料，不等同于 DuMate 补充。"
                continue
            manifest["leads"].append({
                "date": report_date,
                "lead": {
                    "lead_id": lead_id,
                    "company": {"company_name": signal.get("company"), "location": signal.get("location"), "industry": signal.get("industry")},
                    "project": {"project_name": project, "project_stage": signal.get("opportunity_stage")},
                    "signal": {"signal_description": signal.get("trigger") or project, "signal_date": report_date},
                    "evidence": [{"source_url": url, "evidence_summary": "Radar daily source"} for url in signal.get("source_urls", [])],
                },
                "stage1": "RADAR_DAILY",
                "stage2": "NOT_RECORDED",
                "stage3": "DAILY_ENRICHMENT" if stage3 else "NOT_RECORDED",
                "stage2_detail": "日报未附国内团队判断。",
                "stage3_detail": "日报附带资料，不等同于 DuMate 补充。" if stage3 else "日报未附补充资料。",
                "stage3_result": None,
                "enriched_record": display_record,
                "enriched_contacts": [],
                "daily_contacts": redact_daily_stage3(stage3.get("contacts", {})) if isinstance(stage3, dict) else {},
                "daily_stage3": bool(stage3),
                "source_kind": "daily_radar",
                "legacy_match": True,
            })
            existing.add(lead_id)
            rows_by_id[lead_id] = manifest["leads"][-1]
    manifest["lead_count"] = len(manifest["leads"])
    manifest["enriched_contact_count"] = sum(len(x.get("enriched_contacts", [])) for x in manifest["leads"])
    return manifest

def page(m):
    leads = m["leads"]
    yes = sum(x.get("stage2") == "YES" for x in leads)
    enriched = sum(x.get("stage3") == "ENRICHED" for x in leads)
    css = r'''
:root{color-scheme:light;--ink:#17212b;--muted:#657582;--line:#dbe4e9;--bg:#f3f7f8;--blue:#0e628c;--green:#176a49;--amber:#8a5a11;--red:#a13b3b}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}main{max-width:1180px;margin:auto;padding:18px}h1,h2,h3,p{margin:0}h1{font-size:clamp(25px,5vw,36px);line-height:1.2}.muted{color:var(--muted);font-size:14px}.intro{margin:5px 0 16px}.toolbar{position:sticky;top:0;z-index:2;background:rgba(243,247,248,.96);padding:8px 0 12px}.search{width:100%;border:1px solid #b9cbd4;border-radius:12px;padding:13px 14px;font:inherit;background:#fff}.stats{display:flex;gap:8px;overflow:auto;margin:12px 0}.stat{min-width:105px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:9px 12px}.stat b{display:block;font-size:21px}.layout{display:grid;grid-template-columns:335px minmax(0,1fr);gap:14px;align-items:start}aside,.detail,.box{background:#fff;border:1px solid var(--line);border-radius:14px}.list{overflow:hidden;position:sticky;top:76px;max-height:calc(100vh - 92px);overflow-y:auto}.day{font-size:13px;font-weight:700;color:var(--muted);padding:10px 12px 5px;background:#f7fafb;border-bottom:1px solid #edf2f4}.row{display:block;width:100%;padding:11px 12px;text-align:left;border:0;border-bottom:1px solid #edf2f4;background:#fff;cursor:pointer;font:inherit}.row:hover,.active{background:#e9f4f8}.row b,.row span,.row small{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.row b{font-size:15px}.row span{font-weight:600}.row small{color:var(--muted);font-size:13px}.detail{padding:16px}.detail-head{padding-bottom:12px;border-bottom:1px solid var(--line)}.detail h2{font-size:24px;line-height:1.25}.badges{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}.badge{border-radius:99px;padding:4px 9px;font-size:13px;font-weight:700}.green{background:#e8f6ee;color:var(--green)}.amber{background:#fff4d9;color:var(--amber)}.red{background:#fdecec;color:var(--red)}.blue{background:#e7f1f7;color:var(--blue)}.facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin:12px 0}.fact{background:#f7fafb;border-radius:10px;padding:9px 10px}.fact label{display:block;color:var(--muted);font-size:13px}.box{padding:13px;margin-top:12px}.box h3{font-size:17px;margin-bottom:7px}.box ul{margin:0;padding-left:20px}.box li+li{margin-top:7px}details{margin-top:10px}summary{cursor:pointer;font-weight:700;color:var(--blue)}a{color:var(--blue);word-break:break-all}.empty{padding:20px;color:var(--muted)}.prompt{background:#fff8e8;border-color:#e6d49f;white-space:pre-wrap;font-family:inherit;font-size:14px}
@media(max-width:760px){main{padding:12px}.layout{display:block}.list{position:static;max-height:none;margin-bottom:12px}.detail{padding:13px;scroll-margin-top:10px}.facts{grid-template-columns:1fr 1fr}.row{padding:10px 11px}.toolbar{top:0}.detail h2{font-size:22px}}
'''
    js = r'''
const d=await fetch('./leads-data.json?'+Date.now(),{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error('线索数据加载失败');return r.json()}),list=document.querySelector('aside'),detail=document.querySelector('.detail'),search=document.querySelector('#search');let activeFilter='all';
document.head.insertAdjacentHTML('beforeend','<style>.filters{display:flex;gap:7px;overflow:auto;padding:8px 0 2px}.filter{white-space:nowrap;border:1px solid #b9cbd4;border-radius:99px;padding:8px 12px;background:#fff;color:#17212b;font:inherit;cursor:pointer}.filter.selected{background:#0e628c;border-color:#0e628c;color:#fff}.reports{margin-top:14px}</style>');
document.querySelector('.toolbar').insertAdjacentHTML('beforeend','<div class="filters" aria-label="筛选线索"><button class="filter selected" data-filter="all">全部</button><button class="filter" data-filter="contacts">已有联系人资料</button><button class="filter" data-filter="yes">国内团队已确认</button><button class="filter" data-filter="todo">待国内团队确认</button><button class="filter export" type="button">导出当前结果 PDF</button></div>');
document.querySelector('[data-filter="all"]').textContent=`全部（${d.leads.length}）`;document.querySelector('[data-filter="contacts"]').textContent=`已有联系人资料（${d.leads.filter(r=>(r.enriched_contacts||[]).length>0).length}）`;document.querySelector('[data-filter="yes"]').textContent=`国内团队已确认（${d.leads.filter(r=>r.stage2==='YES').length}）`;document.querySelector('[data-filter="todo"]').textContent=`待国内团队确认（${d.leads.filter(r=>r.stage2!=='YES').length}）`;
document.querySelector('main').insertAdjacentHTML('beforeend','<section class="box reports"><h2>报告与原始文件</h2><p class="muted">点击后在 GitHub 中打开，可复制或分享给其他人。</p><ul><li><a target="_blank" rel="noreferrer" href="https://github.com/hozen/jingfan-ims-intelligence/blob/main/docs/task-002-review.md">Task 002 评审报告</a></li><li><a target="_blank" rel="noreferrer" href="https://github.com/hozen/jingfan-ims-intelligence/blob/main/docs/task-002-vv-report.md">Task 002 验证报告</a></li><li><a target="_blank" rel="noreferrer" href="https://github.com/hozen/jingfan-ims-intelligence/blob/main/docs/water-clay-audit.md">Water Clay 审计报告</a></li><li><a target="_blank" rel="noreferrer" href="https://github.com/hozen/jingfan-ims-intelligence/blob/main/docs/stage-pipeline-integration.md">三阶段串联说明</a></li><li><a target="_blank" rel="noreferrer" href="https://github.com/hozen/jingfan-ims-intelligence/blob/main/customer/industrial-leads/pipeline-manifest.json">当前完整线索清单 JSON</a></li></ul></section>');
document.head.insertAdjacentHTML('beforeend','<style>.filters{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))}.filter{min-width:0}.stats{display:none}@media(max-width:760px){.filters{grid-template-columns:1fr}}</style>');
document.querySelector('.stats').remove();
document.querySelector('.layout').before(document.querySelector('.reports'));
document.querySelector('.reports').innerHTML='<h2>原始雷达报告</h2><p class="muted">这里是仓库中的原始报告，可直接打开、复制和分享。</p><ul><li><a target="_blank" rel="noreferrer" href="https://github.com/hozen/jingfan-ims-intelligence/blob/main/intelligence/industrial/reports/IND_Radar_Daily_2026-09-10.md">工业雷达日报 2026-09-10</a></li><li><a target="_blank" rel="noreferrer" href="https://github.com/hozen/jingfan-ims-intelligence/blob/main/intelligence/industrial/reports/IND_GTM_Radar_20260821_v4.md">工业 GTM 雷达报告 v4</a></li><li><a target="_blank" rel="noreferrer" href="https://github.com/hozen/jingfan-ims-intelligence/blob/main/intelligence/industrial/reports/IND_Radar_Intel_20260821_v3.md">工业雷达情报报告 v3</a></li><li><a target="_blank" rel="noreferrer" href="https://github.com/hozen/jingfan-ims-intelligence/blob/main/intelligence/industrial/reports/IND_Radar_Intel_20260821_v2.md">工业雷达情报报告 v2</a></li><li><a target="_blank" rel="noreferrer" href="https://github.com/hozen/jingfan-ims-intelligence/blob/main/intelligence/industrial/reports/IND_Radar_Intel_20260821.md">工业雷达情报报告</a></li><li><a target="_blank" rel="noreferrer" href="https://github.com/hozen/jingfan-ims-intelligence/blob/main/intelligence/industrial/reports/Week1_2026-08-14.md">工业雷达第一周报告</a></li></ul>';
document.head.insertAdjacentHTML('beforeend','<style>.toolbar{position:static;background:transparent}.filters{display:flex;gap:5px;padding:6px 0}.filter{font-size:13px;padding:5px 9px}@media(max-width:760px){.filters{display:flex;overflow-x:auto}.filter{flex:0 0 auto}}</style>');
document.head.insertAdjacentHTML('beforeend','<style>.all-fields{display:grid;gap:8px}.field{padding:8px 0;border-bottom:1px solid #edf2f4}.field>b{display:block;color:#657582;font-size:13px;margin-bottom:3px}.field ul{margin:4px 0 0;padding-left:20px}</style>');
document.head.insertAdjacentHTML('beforeend','<style>.fact-section{border-radius:14px;padding:14px;margin-top:12px;border:1px solid}.fact-section.blue{background:#eef7fb;border-color:#b8d8e6}.fact-section.amber{background:#fff8e8;border-color:#e7d39b}.fact-section.green{background:#eef8f1;border-color:#b8d9c2}.fact-section h3{font-size:17px;margin:0 0 10px}.fact-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.fact-line{padding:8px 10px;background:rgba(255,255,255,.62);border-radius:9px}.fact-line label{display:block;color:#657582;font-size:13px}.fact-section ul{margin:5px 0 0;padding-left:20px}.contact-line{padding:9px 0;border-bottom:1px solid rgba(60,80,60,.15)}.lead-matrix{display:grid;grid-template-columns:115px minmax(0,1fr) 115px minmax(0,1fr);border:1px solid #d5e0e6;border-radius:10px;overflow:hidden;margin-top:12px}.lead-matrix>div{padding:8px 10px;border-right:1px solid #d5e0e6;border-bottom:1px solid #d5e0e6}.lead-matrix>div:nth-last-child(-n+4){border-bottom:0}.lead-matrix>div:nth-child(4n){border-right:0}.lead-matrix .k{color:#657582;background:#f5f8fa;font-size:13px}.decision-line{display:grid;grid-template-columns:155px minmax(0,1fr);border:1px solid #d5e0e6;border-radius:10px;overflow:hidden;margin-top:8px}.decision-line>div{padding:8px 10px}.decision-line .k{color:#657582;background:#f5f8fa;font-size:13px;border-right:1px solid #d5e0e6}@media(max-width:760px){.fact-grid{grid-template-columns:1fr}.lead-matrix{grid-template-columns:92px minmax(0,1fr)}.lead-matrix>div{border-right:0}.lead-matrix>div:nth-child(4n){border-right:0}.lead-matrix>div:nth-last-child(-n+4){border-bottom:1px solid #d5e0e6}.lead-matrix>div:nth-last-child(-n+2){border-bottom:0}.decision-line{grid-template-columns:112px minmax(0,1fr)}}</style>');
document.head.insertAdjacentHTML('beforeend','<style>.stage-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:7px;margin:12px 0}.stage-card{border:1px solid #dbe4e9;border-radius:11px;padding:9px;background:#f7fafb;min-height:96px}.stage-card h3{font-size:14px;margin:0 0 5px;color:#0e628c}.stage-card p{font-size:13px}.stage-card em{display:block;font-style:normal;font-weight:700;margin-bottom:4px}.stage-wait{color:#8a5a11}@media(max-width:760px){.stage-grid{grid-template-columns:1fr 1fr}.stage-card:last-child{grid-column:span 2}}</style>');
document.querySelector('.layout').after(document.querySelector('.reports'));
document.querySelector('.reports').innerHTML='<details><summary>原始雷达报告（不影响线索浏览）</summary><p class="muted">这些是仓库里的原始报告，可打开、复制和分享。</p><ul><li><a target="_blank" rel="noreferrer" href="https://github.com/hozen/jingfan-ims-intelligence/blob/main/intelligence/industrial/reports/IND_Radar_Daily_2026-09-10.md">工业雷达日报 2026-09-10</a></li><li><a target="_blank" rel="noreferrer" href="https://github.com/hozen/jingfan-ims-intelligence/blob/main/intelligence/industrial/reports/IND_GTM_Radar_20260821_v4.md">工业 GTM 雷达报告 v4</a></li><li><a target="_blank" rel="noreferrer" href="https://github.com/hozen/jingfan-ims-intelligence/blob/main/intelligence/industrial/reports/IND_Radar_Intel_20260821_v3.md">工业雷达情报报告 v3</a></li><li><a target="_blank" rel="noreferrer" href="https://github.com/hozen/jingfan-ims-intelligence/blob/main/intelligence/industrial/reports/IND_Radar_Intel_20260821_v2.md">工业雷达情报报告 v2</a></li><li><a target="_blank" rel="noreferrer" href="https://github.com/hozen/jingfan-ims-intelligence/blob/main/intelligence/industrial/reports/IND_Radar_Intel_20260821.md">工业雷达情报报告</a></li><li><a target="_blank" rel="noreferrer" href="https://github.com/hozen/jingfan-ims-intelligence/blob/main/intelligence/industrial/reports/Week1_2026-08-14.md">工业雷达第一周报告</a></li></ul></details>';
const esc=x=>String(x??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
const status=(x,type)=>{const map={DISCOVERED:'已发现',ENRICHED_SOURCE:'已有补充资料',SOURCE_NOT_LINKED:'未找到对应发现记录',NOT_RUN:'还未判断',NOT_RECORDED:'没有记录',YES:'已确认可以跟进',ENRICHED:'已完成资料补充',BLOCKED:'暂时不能补充资料'};return `<span class="badge ${type}">${esc(map[x]||x||'没有记录')}</span>`};
const filteredRows=()=>{const q=search.value.trim().toLowerCase();return d.leads.map((r,i)=>({r,i})).filter(({r})=>(activeFilter==='all'||(activeFilter==='contacts'&&(r.enriched_contacts||[]).length>0)||(activeFilter==='yes'&&r.stage2==='YES')||(activeFilter==='todo'&&r.stage2!=='YES'))&&(!q||JSON.stringify(r).toLowerCase().includes(q)))};
function renderList(){const rows=filteredRows(),days=[...new Set(rows.map(x=>x.r.date))].sort((a,b)=>String(b).localeCompare(String(a)));list.innerHTML=days.length?days.map(day=>`<div class="day">${esc(day)}</div>`+rows.filter(x=>x.r.date===day).map(x=>`<button class="row" data-i="${x.i}"><b>${esc(x.r.lead.lead_id)}</b><span>${esc(x.r.lead.company?.company_name||'公司名称未记录')}</span><small>${esc(x.r.lead.project?.project_name||x.r.lead.signal?.signal_description||'项目名称未记录')}</small></button>`).join('')).join(''):'<div class="empty">没有找到匹配线索</div>';list.querySelectorAll('.row').forEach(x=>x.onclick=()=>{sessionStorage.setItem('industrial-leads-selected',x.dataset.i);show(+x.dataset.i,true);});}
function show(i,focus=false){const r=d.leads[i],l=r.lead,z=r.stage3_result||{},ev=l.evidence||[],unknowns=z.unknowns||[];list.querySelectorAll('.row').forEach(x=>x.classList.toggle('active',+x.dataset.i===i));const evidence=ev.length?ev.map(x=>`<li><b>${esc(x.document_title||x.source_type||'来源记录')}</b><br>${esc(x.verbatim_evidence||x.evidence_summary||'没有摘录原文')}<br><a href="${esc(x.canonical_url||x.source_url||'#')}" target="_blank" rel="noreferrer">打开来源</a></li>`).join(''):'<li>没有证据记录</li>';const gap=unknowns.length?unknowns.map(x=>`<li>${esc(typeof x==='string'?x:x.description||JSON.stringify(x))}</li>`).join(''):'<li>Water Clay 没有登记未知项。</li>';const prompt=`请补充线索 ${l.lead_id}：\n1. 找到 Stage 1 原始发现记录，并确认与公司、项目、日期是否一致。\n2. 给出 Stage 2 判断：YES（可以跟进）/ REVIEW（需要人工复核）/ NO（不跟进），并写明事实依据。\n3. 如果是 YES，再补充：项目当前进度、业主/设计/施工/供应商、采购负责人或技术负责人姓名及公开联系方式。\n4. 每条信息附来源链接和原文摘录；没有找到就明确写“未找到”，不要推测。`;detail.innerHTML=`<div class="detail-head"><h2>${esc(l.company?.company_name||'公司名称未记录')}</h2><p class="muted">${esc(l.lead_id)} · ${esc(r.date)} · ${esc(l.company?.location||'地区未记录')}</p><div class="badges">${status(r.stage1,'blue')}${status(r.stage2,r.stage2==='YES'?'green':'amber')}${status(r.stage3,r.stage3==='ENRICHED'?'green':'red')}</div></div><div class="facts"><div class="fact"><label>项目</label>${esc(l.project?.project_name||'未记录')}</div><div class="fact"><label>当前进度（记录值）</label>${esc(l.project?.project_stage||z.main_project_stage?.value||'未记录')}</div><div class="fact"><label>线索来源日期</label>${esc(l.signal?.signal_date||r.date||'未记录')}</div><div class="fact"><label>证据条数</label>${ev.length} 条</div></div><div class="box"><h3>现在能确认的事实</h3><p>${esc(l.signal?.signal_description||'没有信号描述')}</p><p class="muted">${esc(r.stage3_detail||r.stage2_detail||'没有补充说明')}</p></div><details class="box" open><summary>查看来源证据（${ev.length} 条）</summary><ul>${evidence}</ul></details><details class="box"><summary>查看缺口</summary><ul>${r.stage1==='SOURCE_NOT_LINKED'?'<li>这条记录没有找到对应的 Stage 1 原始发现记录。</li>':''}${r.stage2!=='YES'?'<li>没有这条 Lead ID 的 Stage 2 明确判断，因此不能确认是否值得跟进。</li>':''}${r.stage3!=='ENRICHED'?'<li>没有 Stage 3 补充结果；原因是 Stage 2 尚未明确为“可以跟进”。</li>':''}${gap}</ul></details><details class="box prompt"><summary>给工业雷达的补充要求（可复制）</summary>${esc(prompt)}</details>`;if(focus)detail.scrollIntoView({behavior:'smooth',block:'start'});}
const baseShow=show;show=(i,focus=false)=>{baseShow(i,focus);const r=d.leads[i],e=r.enriched_record,cs=r.enriched_contacts||[];if(!e)return;const s=e.original_signal||{},f=s.evidence||{},rec=e.ims_recommendation||{},phones=c=>{const p=(c.phone||[]).map(x=>x.value).join('、'),m=(c.email||[]).map(x=>x.value).join('、');return [p&&`电话：${esc(p)}`,m&&`邮箱：${esc(m)}`].filter(Boolean).join('；')||'没有公开联系方式'};detail.insertAdjacentHTML('beforeend',`<div class="box"><h3>销售常用信息</h3><div class="facts"><div class="fact"><label>行业</label>${esc(s.industry||'未记录')}</div><div class="fact"><label>线索级别</label>${esc(s.signal_tier||'未记录')}</div><div class="fact"><label>机会阶段</label>${esc(s.opportunity_stage||'未记录')}</div><div class="fact"><label>优先级</label>${esc(s.priority||'未记录')}</div><div class="fact"><label>预计时间</label>${esc(s.estimated_time_window||'未记录')}</div><div class="fact"><label>水系统归属</label>${esc(s.water_system_ownership||'未记录')}</div></div><p>${esc(s.potential_ims_use_case||'未记录')}</p></div><div class="box"><h3>联系人（${cs.length} 人）</h3><ul>${cs.length?cs.map(c=>`<li><b>${esc(c.name||'姓名未记录')}</b> · ${esc(c.title||'职务未记录')}<br>${phones(c)}<br><span class="muted">来源：${esc((c.discovered_by||[]).join('、')||'未记录')}；证据状态：${esc(c.verification_status||'未记录')}</span></li>`).join(''):'<li>没有关联联系人。</li>'}</ul></div><details class="box"><summary>项目事实、推断与待核实项</summary><p><b>已记录事实</b></p><ul>${(f.facts||[]).map(x=>`<li>${esc(x)}</li>`).join('')||'<li>未记录</li>'}</ul><p><b>待核实</b></p><ul>${(f.unknowns||e.missing_roles||[]).map(x=>`<li>${esc(x)}</li>`).join('')||'<li>未记录</li>'}</ul></details><div class="box"><h3>补充资料中的行动建议</h3><p>${esc(rec.recommended_action||'未记录')}</p></div>`);};
const oldShow=show;const keyNames={lead_id:'线索编号',company:'公司',company_name:'公司名称',account:'账户',location:'地点',industry:'行业',opportunity:'项目机会',signal_tier:'线索级别',engine:'雷达引擎',evidence:'证据',facts:'已记录事实',inferences:'推断',unknowns:'未知项',potential_ims_use_case:'潜在软件用例',logic:'判断逻辑',opportunity_stage:'机会阶段',estimated_time_window:'预计时间窗口',priority:'优先级',water_system_ownership:'水系统归属',incrementality_status:'新增机会状态',to_verify:'待核实',continuity:'连续性变化',enrichment_status:'资料补充状态',contact_ids:'联系人编号',contact_summary:'联系人概况',missing_roles:'缺失角色',enrichment_sources:'资料来源',ims_recommendation:'软件建议',recommended_action:'建议行动',priority_score:'优先级分数',time_sensitivity:'时间紧迫性',name:'姓名',title:'职务',role:'角色',role_description:'角色说明',contact_status:'联系人状态',current_historical:'当前/历史',evidence_score:'证据分数',commercial_relevance_score:'商业相关性'};
const label=k=>keyNames[k]||k;const renderAll=v=>Array.isArray(v)?(v.length?`<ul>${v.map(x=>`<li>${renderAll(x)}</li>`).join('')}</ul>`:'<span class="muted">未记录</span>'):v&&typeof v==='object'?`<div class="all-fields">${Object.entries(v).map(([k,x])=>`<div class="field"><b>${esc(label(k))}</b><div>${renderAll(x)}</div></div>`).join('')}</div>`:esc(v??'未记录');
show=(i,focus=false)=>{oldShow(i,focus);const e=d.leads[i].enriched_record;if(e)detail.insertAdjacentHTML('beforeend',`<details class="box"><summary>查看全部资料字段（已按字段排版）</summary>${renderAll(e)}</details>`);};
const baseList=renderList;renderList=()=>{baseList();const visible=[...list.querySelectorAll('.row')].map(x=>+x.dataset.i),selected=+sessionStorage.getItem('industrial-leads-selected');if(visible.length&&!visible.includes(selected))show(visible[0]);};
const stagesShow=show;show=(i,focus=false)=>{stagesShow(i,focus);const r=d.leads[i],l=r.lead,e=r.enriched_record,z=r.stage3_result||{},s=e?.original_signal||{},c=(r.enriched_contacts||[]).length,stage1=l.signal?.signal_description||s.opportunity||'未记录',stage2=r.stage2==='YES'?'国内团队已确认':(r.stage2_detail||'等待国内团队判断'),stage3=e?'DuMate 资料已补充':(z.schema_version?'辅助证据已核验':'等待资料补充'),stage4=e?.ims_recommendation?.recommended_action||z.next_action||'待人工安排负责人和下一步行动',stage5='待人工记录联系结果';detail.insertAdjacentHTML('afterbegin',`<div class="stage-grid"><div class="stage-card"><h3>Stage 1 · Radar</h3><em>发现事实</em><p>${esc(stage1)}</p><p class="muted">来源证据：${(l.evidence||[]).length} 条</p></div><div class="stage-card"><h3>Stage 2 · Qualification</h3><em>${esc(r.stage2==='YES'?'已确认':'待判断')}</em><p>${esc(stage2)}</p></div><div class="stage-card"><h3>Stage 3 · Enrichment</h3><em>${esc(e?'已补充':'待补充')}</em><p>${esc(stage3)}</p><p class="muted">联系人：${c} 人</p></div><div class="stage-card"><h3>Stage 4 · Orchestration</h3><em class="stage-wait">人工安排</em><p>${esc(stage4)}</p></div><div class="stage-card"><h3>Stage 5 · Engagement</h3><em class="stage-wait">未开始</em><p>${esc(stage5)}</p></div></div>`);};
show=(i,focus=false)=>{const r=d.leads[i],l=r.lead,e=r.enriched_record||{},s=e.original_signal||{},sev=s.evidence||{},z=r.stage3_result||{},ev=l.evidence||[],facts=sev.facts||[],inferences=sev.inferences||[],unknowns=sev.unknowns||[],contacts=r.enriched_contacts||[],sources=s.source_urls||ev.map(x=>x.source_url||x.canonical_url).filter(Boolean),recommendation=typeof e.ims_recommendation==='string'?e.ims_recommendation:e.ims_recommendation?.recommended_action||z.next_action||'',imsFit=e.ims_opportunity_level||s.ims_opportunity_level||e.ims_recommendation?.ims_fit||'未评估',matrix=(a)=>`<div class="lead-matrix">${a.map(([k,v])=>`<div class="k">${esc(k)}</div><div>${esc(v||'未记录')}</div>`).join('')}</div>`,decision=(k,v)=>`<div class="decision-line"><div class="k">${esc(k)}</div><div>${esc(v||'未记录')}</div></div>`,items=a=>a&&a.length?`<ul>${a.map(x=>`<li>${esc(typeof x==='string'?x:JSON.stringify(x))}</li>`).join('')}</ul>`:'<p class="muted">未记录</p>',contactHtml=contacts.length?contacts.map(c=>`<div class="contact-line"><b>${esc(c.name||'姓名未记录')}</b> · ${esc(c.title||c.role||'职务未记录')}<br>${(c.phone||[]).map(x=>`电话：${esc(x.value)}`).join('；')||'联系方式未公开'}<br><span class="muted">来源：${esc((c.discovered_by||[]).join('、')||c.source||'未记录')} · 验证：${esc(c.verification_status||c.contact_status||'未记录')}</span></div>`).join(''):'<p class="muted">未记录联系人</p>';list.querySelectorAll('.row').forEach(x=>x.classList.toggle('active',+x.dataset.i===i));detail.innerHTML=`<div class="detail-head"><h2>${esc(l.company?.company_name||s.company||'公司名称未记录')}</h2><p class="muted">${esc(l.lead_id)} · ${esc(r.date||l.signal?.signal_date)} · ${esc(l.company?.location||s.location||'地区未记录')}</p><div class="badges">${status(r.stage2,r.stage2==='YES'?'green':'amber')}<span class="badge blue">${esc(s.priority||s.signal_tier||'优先级未记录')}</span><span class="badge blue">${esc(e.enrichment_status||r.stage3||'资料状态未记录')}</span></div></div>${matrix([['行业 / 地区',`${s.industry||l.company?.industry||'未记录'} / ${s.location||l.company?.location||'未记录'}`],['来源引擎',s.engine],['窗口 / 时点',s.estimated_time_window||l.signal?.signal_date||r.date],['类型',s.signal_type||l.signal?.signal_type],['项目实体 / 有效性',s.continuity?.status||s.incrementality_status||'未记录'],['投资 / 产能',s.investment_or_capacity],['主项目阶段',s.opportunity_stage||l.project?.project_stage],['相关包阶段',s.related_procurement_phase]])}<section class="fact-section blue"><h3>项目背景 / 已确认事实</h3>${items(facts.length?facts:[l.signal?.signal_description].filter(Boolean))}</section><section class="fact-section amber"><h3>客户需求与现有方案</h3>${matrix([['客户要完成什么',s.customer_requirement||s.customer_need],['目前 / 已尝试方案',s.current_solution||s.existing_solution],['客户痛点 / 方案问题',inferences.join('；')],['为什么是现在',s.logic||l.signal?.signal_description]])}</section><section class="fact-section green"><h3>iMS 机会判断</h3>${matrix([['iMS机会可能性',imsFit],['Opportunity Stage',s.opportunity_stage||l.project?.project_stage],['为什么与iMS相关',s.logic],['iMS具体作用',s.potential_ims_use_case],['机会成立条件',(s.to_verify||unknowns).join('；')],['商业入口',recommendation]])}${decision('AI Recommendation',recommendation)}${decision('VM Decision',r.stage2==='YES'?'YES':r.stage2||'未记录')}</section><section class="fact-section green"><h3>联系人与补充资料</h3>${matrix([['资料状态',e.enrichment_status||r.stage3],['联系人数量',contacts.length+' 人'],['缺失角色',(e.missing_roles||[]).join('、')],['判断依据',r.stage2_detail]])}<h3 style="margin-top:12px">联系人</h3>${contactHtml}</section><section class="fact-section blue"><h3>下一步</h3>${items([recommendation,...(s.to_verify||unknowns)].filter(Boolean))}<h3 style="margin-top:12px">来源</h3>${items(sources)}</section><details class="box"><summary>查看全部资料字段（按字段排版）</summary>${renderAll(e)}</details>`;if(focus)detail.scrollIntoView({behavior:'smooth',block:'start'});};
const qualityShow=show;show=(i,focus=false)=>{qualityShow(i,focus);const r=d.leads[i],daily=r.source_kind==='daily_radar',hasEnrichment=Boolean(r.enriched_record)&&!daily,unlinked=r.stage1==='SOURCE_NOT_LINKED',judgement=r.stage2==='YES'?(unlinked?'国内判断 YES，待关联':'已确认可以跟进'):(r.stage2==='NOT_RECORDED'?'国内判断未记录':'国内判断待补'),enrichment=daily?(r.daily_stage3?'Radar 日报附带资料':'Radar 日报，待补充'):(hasEnrichment?'DuMate 资料已补充':'资料未补充'),badges=detail.querySelector('.badges');badges.innerHTML=`<span class="badge ${unlinked?'amber':'blue'}">${esc(unlinked?'原始发现未关联':'原始发现已关联')}</span><span class="badge ${unlinked?'amber':r.stage2==='YES'?'green':'amber'}">${esc(judgement)}</span><span class="badge blue">${esc(enrichment)}</span>`;const supplement=[...detail.querySelectorAll('section')].find(x=>x.querySelector('h3')?.textContent==='联系人与补充资料');if(supplement&&!hasEnrichment){const cells=supplement.querySelectorAll('.lead-matrix>div');for(let n=0;n<cells.length;n+=2)if(cells[n].textContent==='资料状态')cells[n+1].textContent=enrichment;}if(daily&&supplement&&Object.keys(r.daily_contacts||{}).length)supplement.insertAdjacentHTML('beforeend',`<details class="box"><summary>日报附带的联系人与项目资料</summary>${renderAll(r.daily_contacts)}</details>`);if((r.dumate_history||[]).length)detail.insertAdjacentHTML('beforeend',`<details class="box"><summary>DuMate 历史快照（${r.dumate_history.length} 次）</summary>${renderAll(r.dumate_history)}</details>`);};
document.querySelector('[data-filter="yes"]').textContent=`国内判断 YES（${d.leads.filter(r=>r.stage2==='YES').length}，待关联）`;
document.querySelector('.export').onclick=()=>{const rows=filteredRows();if(!rows.length){alert('当前条件没有可导出的线索。');return;}const criteria=[search.value.trim()&&`搜索：${search.value.trim()}`,activeFilter!=='all'&&`筛选：${document.querySelector(`[data-filter="${activeFilter}"]`).textContent}`].filter(Boolean).join(' · ')||'全部线索';const card=({r})=>{const l=r.lead||{},e=r.enriched_record||{},s=e.original_signal||{},facts=(s.evidence||{}).facts||[l.signal?.signal_description].filter(Boolean),contacts=r.enriched_contacts||[];return `<article><h2>${esc(l.company?.company_name||s.company||'公司名称未记录')}</h2><p class="meta">${esc(l.lead_id)} · ${esc(r.date||'日期未记录')} · ${esc(l.company?.location||s.location||'地区未记录')}</p><dl><dt>项目</dt><dd>${esc(l.project?.project_name||s.opportunity||s.project||'未记录')}</dd><dt>项目阶段</dt><dd>${esc(s.opportunity_stage||l.project?.project_stage||'未记录')}</dd><dt>iMS 机会</dt><dd>${esc(e.ims_recommendation?.ims_fit||s.ims_fit||'未评估')}</dd><dt>国内判断</dt><dd>${esc(r.stage2||'未记录')}</dd></dl><h3>已确认事实</h3><ul>${facts.map(x=>`<li>${esc(typeof x==='string'?x:JSON.stringify(x))}</li>`).join('')||'<li>未记录</li>'}</ul>${contacts.length?`<h3>联系人（已脱敏）</h3><ul>${contacts.map(c=>`<li>${esc(c.name||'姓名未记录')} · ${esc(c.title||c.role||'职务未记录')} · ${esc((c.phone||[]).map(x=>x.value).join('；')||'联系方式未公开')}</li>`).join('')}</ul>`:''}<h3>下一步</h3><p>${esc(typeof e.ims_recommendation==='string'?e.ims_recommendation:e.ims_recommendation?.recommended_action||s.pull_box?.next_validation_question||'未记录')}</p></article>`};const win=window.open('','_blank');if(!win){alert('浏览器拦截了新窗口，请允许弹窗后重试。');return;}win.document.write(`<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>工业线索导出</title><style>body{font:14px/1.6 system-ui,"Microsoft YaHei",sans-serif;color:#17212b;margin:28px auto;max-width:800px}h1{font-size:26px;margin:0}h2{font-size:18px;margin:0}.meta{color:#657582}article{break-inside:avoid;border-top:1px solid #ccd7dc;padding:18px 0}dl{display:grid;grid-template-columns:110px 1fr;margin:10px 0}dt{color:#657582}dd{margin:0}h3{font-size:15px;margin:12px 0 4px}ul{margin:0;padding-left:20px}@page{size:A4;margin:14mm}@media print{body{margin:0}}</style><h1>工业线索导出</h1><p class="meta">${esc(criteria)} · ${rows.length} 条 · ${new Date().toLocaleString('zh-CN')}</p>${rows.map(card).join('')}</html>`);win.document.close();win.focus();setTimeout(()=>win.print(),250);};
search.oninput=()=>{sessionStorage.setItem('industrial-leads-search',search.value);renderList();};
document.querySelectorAll('[data-filter]').forEach(b=>b.onclick=()=>{activeFilter=b.dataset.filter;document.querySelectorAll('[data-filter]').forEach(x=>x.classList.toggle('selected',x===b));renderList();});
const savedSearch=sessionStorage.getItem('industrial-leads-search')||'';search.value=savedSearch;renderList();
const savedLead=sessionStorage.getItem('industrial-leads-selected');show(savedLead&&d.leads[+savedLead]?+savedLead:0);
if(window.matchMedia('(min-width:761px)').matches){setInterval(()=>location.reload(),60000);}
'''
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#f3f7f8"><title>工业线索</title><style>{css}</style></head><body><main><p class="muted">IMS GTM · 销售线索</p><h1>工业线索</h1><p class="intro muted">按日期找线索。页面只显示资料里已经写明的事实。</p><div class="toolbar"><input id="search" class="search" aria-label="搜索线索" placeholder="搜索公司、项目或线索编号…"></div><div class="stats"><div class="stat"><b>{len(leads)}</b><span>全部线索</span></div><div class="stat"><b>{yes}</b><span>已确认可跟进</span></div><div class="stat"><b>{enriched}</b><span>已补充资料</span></div></div><div class="layout"><aside class="list" aria-label="线索列表"></aside><section class="detail" aria-live="polite"></section></div><p class="muted" style="margin-top:12px">资料负责人：国内团队 · 电脑端每 60 秒自动检查更新 · 本页不自动猜测、不自动改变线索状态</p></main><script type="module">{js}</script></body></html>'''

if __name__ == "__main__":
    m = model()
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(m, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"), encoding="utf-8")
    PAGE.write_text(page(m), encoding="utf-8")
    print(f"Built mobile fact-first page for {len(m['leads'])} records")
