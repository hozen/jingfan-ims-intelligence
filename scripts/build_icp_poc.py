#!/usr/bin/env python3
"""Build a read-only ICP intelligence POC from existing enriched snapshots."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDUSTRIAL = ROOT / "intelligence/industrial/enriched/indctx_latest.json"
MUNICIPAL = ROOT / "intelligence/municipal/enriched/ctx_latest.json"
OUTPUT = ROOT / "customer/water-clay-poc/index.html"
DATA_OUTPUT = ROOT / "customer/water-clay-poc/profiles.json"


def text(value, fallback="UNKNOWN"):
    if value is None or value == "" or value == []:
        return fallback
    if isinstance(value, list):
        return "；".join(map(str, value))
    return str(value)


def mapping(value):
    return value if isinstance(value, dict) else {}


def industrial_penetration(account, project):
    group = text(account.get("group_name"), "")
    ownership = [account.get("account_name")]
    if group and not group.lower().startswith("unknown"):
        ownership.extend(x.strip() for x in group.split("→") if x.strip())
    capacity = mapping(account.get("production_capacity"))
    return {
        "ownership": [x for x in ownership if x],
        "subsidiaries": list(mapping(capacity.get("breakdown")).keys()),
        "upstream": [], "downstream": [],
        "project_partners": [x for x in [project.get("epc_contractor"), project.get("design_institute"), project.get("water_treatment_contractor")] if x and not str(x).lower().startswith("unknown")],
        "gaps": ["上游原料/设备供应商", "下游核心客户/应用行业", "股权比例与最终受益主体"],
    }


def municipal_penetration(account, organizations):
    organization = next((x for x in organizations if x.get("account_id") == account.get("account_id")), {})
    return {
        "ownership": [x for x in [account.get("account_name") or organization.get("organization_name")] if x],
        "subsidiaries": [], "upstream": [], "downstream": [], "project_partners": [],
        "gaps": ["主管或出资主体", "母集团/城投平台", "区域子公司与项目公司", "所属水厂/污水厂/运营单位", "股权比例"],
    }


def industrial_profiles(raw):
    projects = {x.get("project_id"): x for x in raw.get("projects", [])}
    accounts = {x.get("account_id"): x for x in raw.get("accounts", [])}
    contacts = raw.get("contacts", [])
    actions = raw.get("next_best_actions", [])
    profiles = []
    for lead in raw.get("leads", []):
        signal = lead.get("original_signal", {})
        project = projects.get((lead.get("project_ids") or [None])[0], {})
        account = accounts.get((lead.get("account_ids") or [None])[0], {})
        linked_contacts = [c for c in contacts if lead.get("lead_id") in c.get("lead_ids", [])]
        facts = signal.get("evidence", {}).get("facts", [])
        inferences = signal.get("evidence", {}).get("inferences", [])
        unknowns = signal.get("evidence", {}).get("unknowns", []) + lead.get("missing_roles", [])
        recommendation_raw = lead.get("ims_recommendation")
        recommendation = mapping(recommendation_raw)
        penetration = industrial_penetration(account, project)
        profiles.append({
            "id": lead.get("lead_id"), "market": "工业", "account": account.get("account_name") or signal.get("company"),
            "project": project.get("project_name") or signal.get("opportunity"), "industry": account.get("industry") or signal.get("industry"),
            "location": account.get("plant_location") or signal.get("location"), "stage": project.get("project_status") or signal.get("opportunity_stage"),
            "priority": signal.get("priority", "UNKNOWN"), "score": recommendation.get("priority_score"),
            "use_case": signal.get("potential_ims_use_case"), "logic": signal.get("logic"),
            "behavior": (["企业穿透：" + " → ".join(penetration["ownership"])] if penetration["ownership"] else []) + facts,
            "inferences": inferences, "unknowns": unknowns + ["企业穿透待补：" + x for x in penetration["gaps"]],
            "water": mapping(project.get("water_system_details")), "procurement": mapping(project.get("estimated_procurement_window")),
            "ecosystem": [{"role": "业主", "name": project.get("owner")}, {"role": "EPC", "name": project.get("epc_contractor")}, {"role": "设计院", "name": project.get("design_institute")}, {"role": "水处理承包商", "name": project.get("water_treatment_contractor")}],
            "contact_coverage": {"total": len(linked_contacts), "verified": sum(bool(c.get("human_verified")) for c in linked_contacts), "cross_agent": sum(bool(c.get("cross_agent_confirmation")) for c in linked_contacts)},
            "recommendation": recommendation, "sources": lead.get("enrichment_sources", []) or signal.get("source_urls", []),
            "penetration": penetration,
            "next_action": next((a.get("action") for a in actions if a.get("lead_id") == lead.get("lead_id")), recommendation.get("recommended_action") or (recommendation_raw if isinstance(recommendation_raw, str) else None)),
        })
    return profiles


def municipal_profiles(raw):
    projects = {x.get("lead_id") or x.get("id"): x for x in raw.get("projects", [])}
    accounts = raw.get("accounts", [])
    contacts = raw.get("contacts", [])
    actions = raw.get("next_best_actions", [])
    profiles = []
    for lead in raw.get("leads", []):
        lead_id = lead.get("id") or lead.get("lead_id")
        project = projects.get(lead_id, {})
        account = next((a for a in accounts if lead_id in a.get("project_ids", [])), {})
        linked_contacts = [c for c in contacts if lead_id in c.get("lead_ids", []) or c.get("contact_id") in account.get("contact_ids", [])]
        facts = account.get("new_facts", [])
        penetration = municipal_penetration(account, raw.get("organizations", []))
        profiles.append({
            "id": lead_id, "market": "市政", "account": account.get("account_name") or lead.get("name"), "project": project.get("name") or lead.get("name"),
            "industry": account.get("account_type", "市政水务"), "location": "".join(filter(None, [account.get("province"), account.get("city")])),
            "stage": project.get("stage") or lead.get("opportunity_stage"), "priority": lead.get("match_priority", "UNKNOWN"), "score": lead.get("score"),
            "use_case": lead.get("iMS_use_case"), "logic": next((f.get("iMS_impact") for f in facts if f.get("iMS_impact")), "现有 enriched 文件未提供完整机会逻辑"),
            "behavior": (["企业穿透：" + " → ".join(penetration["ownership"])] if penetration["ownership"] else []) + [f.get("fact") for f in facts if f.get("fact")],
            "inferences": [], "unknowns": (account.get("missing_roles", []) or raw.get("missing_roles", [])) + ["企业穿透待补：" + x for x in penetration["gaps"]],
            "water": {}, "procurement": {}, "ecosystem": [{"role": "客户主体", "name": account.get("account_name")}],
            "contact_coverage": {"total": len(linked_contacts), "verified": sum(bool(c.get("human_verified")) for c in linked_contacts), "cross_agent": sum(bool(c.get("cross_agent_confirmation")) for c in linked_contacts)},
            "recommendation": {}, "sources": [f.get("source") for f in facts if f.get("source")],
            "penetration": penetration,
            "next_action": next((a.get("action") for a in actions if a.get("account") == account.get("account_name")), "确认最关键的组织角色和当前项目窗口"),
        })
    return profiles


def build():
    industrial = json.loads(INDUSTRIAL.read_text(encoding="utf-8"))
    municipal = json.loads(MUNICIPAL.read_text(encoding="utf-8"))
    profiles = industrial_profiles(industrial) + municipal_profiles(municipal)
    return profiles, {"industrial_updated": industrial.get("metadata", {}).get("last_update"), "municipal_updated": municipal.get("metadata", {}).get("date")}


def render(profiles, metadata):
    payload = json.dumps({"profiles": profiles, "metadata": metadata}, ensure_ascii=False).replace("</", "<\\/")
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Water Clay · ICP Intelligence POC</title><style>
:root{{--nav:#102b27;--accent:#0c806d;--bg:#f3f6f3;--surface:#fff;--ink:#18312d;--muted:#687b76;--line:#dce5df;--warn:#9a6410}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.55 system-ui,"Microsoft YaHei",sans-serif}}button,input,select{{font:inherit}}header{{background:var(--nav);color:#fff;padding:22px 26px}}header h1{{margin:0;font-size:22px}}header p{{margin:4px 0 0;color:#bed0ca}}.toolbar{{display:flex;gap:10px;padding:14px 22px;background:var(--surface);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:2}}.toolbar input{{flex:1;min-width:140px}}.toolbar input,.toolbar select{{padding:9px 11px;border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--ink)}}.layout{{display:grid;grid-template-columns:320px 1fr;max-width:1450px;margin:auto;min-height:700px}}aside{{border-right:1px solid var(--line);background:var(--surface)}}#count{{padding:12px 16px;color:var(--muted)}}.lead{{display:block;width:100%;border:0;border-top:1px solid var(--line);background:transparent;text-align:left;padding:13px 16px;cursor:pointer;color:var(--ink)}}.lead:hover,.lead.active{{background:#e5f2ee}}.lead span,.lead small{{display:block}}.lead small{{color:var(--muted)}}main{{padding:24px;min-width:0}}.hero{{background:var(--nav);color:#fff;padding:24px;border-radius:16px}}.hero h2{{margin:4px 0;font-size:25px}}.hero p{{margin:0;color:#c9d8d4}}.kpis,.columns{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:14px}}.panel{{background:var(--surface);padding:18px;border-radius:13px;border:1px solid var(--line)}}.panel h3{{margin:0 0 10px;font-size:16px}}.kpi b{{display:block;font-size:21px;color:var(--accent)}}.kpi small,.muted{{color:var(--muted)}}.wide{{grid-column:span 2}}ul{{margin:0;padding-left:19px}}li{{margin:7px 0}}.tag{{display:inline-block;background:#dcefe9;color:#075e50;padding:2px 8px;border-radius:999px;margin-right:5px}}.unknown{{color:var(--warn)}}.eco{{display:grid;grid-template-columns:110px 1fr;padding:7px 0;border-bottom:1px solid var(--line)}}.sources a{{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--accent)}}.graph{{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:12px 0}}.node{{background:#e5f2ee;padding:8px 12px;border-radius:9px}}.arrow{{color:var(--muted)}}.relation-grid{{display:grid;grid-template-columns:130px 1fr;gap:8px;padding:8px 0}}@media(max-width:850px){{.layout{{grid-template-columns:1fr}}aside{{border-right:0;max-height:310px;overflow:auto}}.columns,.kpis{{grid-template-columns:1fr}}.wide{{grid-column:auto}}.toolbar{{position:static;flex-wrap:wrap}}}}</style></head><body>
<header><h1>Water Clay · ICP Client Intelligence POC</h1><p>直接读取现有 industrial / municipal enriched 快照，不修改源数据</p></header><div class="toolbar"><input id="q" aria-label="搜索" placeholder="搜索客户、项目、行业或地区"><select id="market" aria-label="市场"><option value="">全部市场</option><option>工业</option><option>市政</option></select><select id="priority" aria-label="优先级"><option value="">全部优先级</option><option>P0</option><option>P1</option><option>P2</option><option>A</option><option>B</option><option>C</option></select></div>
<div class="layout"><aside><div id="count"></div><div id="list"></div></aside><main id="detail"></main></div><script id="data" type="application/json">{payload}</script><script>
const DATA=JSON.parse(document.getElementById('data').textContent), q=document.getElementById('q'), market=document.getElementById('market'), priority=document.getElementById('priority'), list=document.getElementById('list'), detail=document.getElementById('detail'), count=document.getElementById('count');let selected=null;const esc=v=>String(v??'UNKNOWN').replace(/[&<>"']/g,m=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[m]));const arr=v=>Array.isArray(v)?v:[];function filtered(){{let s=q.value.trim().toLowerCase();return DATA.profiles.filter(p=>(!market.value||p.market===market.value)&&(!priority.value||p.priority===priority.value)&&(!s||JSON.stringify([p.account,p.project,p.industry,p.location]).toLowerCase().includes(s)))}}function renderList(){{let rows=filtered();count.textContent=`显示 ${{rows.length}} / ${{DATA.profiles.length}} 条客户项目`;list.innerHTML=rows.map(p=>`<button class="lead ${{p.id===selected?'active':''}}" data-id="${{esc(p.id)}}"><b>${{esc(p.account)}}</b><span>${{esc(p.project)}}</span><small>${{esc(p.market)}} · ${{esc(p.priority)}} · ${{esc(p.stage)}}</small></button>`).join('');list.querySelectorAll('button').forEach(b=>b.onclick=()=>{{selected=b.dataset.id;renderList();renderDetail(DATA.profiles.find(p=>p.id===selected))}});if(!rows.some(p=>p.id===selected)&&rows[0]){{selected=rows[0].id;renderList();renderDetail(rows[0])}}}}function bullets(xs,empty='暂无记录'){{return arr(xs).length?`<ul>${{xs.map(x=>`<li>${{esc(typeof x==='string'?x:JSON.stringify(x))}}</li>`).join('')}}</ul>`:`<p class="muted">${{empty}}</p>`}}function renderDetail(p){{if(!p)return;let w=p.water||{{}}, pc=p.procurement||{{}}, r=p.recommendation||{{}};detail.innerHTML=`<section class="hero"><span class="tag">${{esc(p.market)}}</span><span class="tag">${{esc(p.priority)}}</span><h2>${{esc(p.account)}}</h2><p>${{esc(p.project)}} · ${{esc(p.location)}}</p></section><div class="kpis"><section class="panel kpi"><small>项目阶段</small><b>${{esc(p.stage)}}</b></section><section class="panel kpi"><small>机会评分（源文件）</small><b>${{esc(p.score)}}</b></section><section class="panel kpi"><small>角色情报覆盖</small><b>${{p.contact_coverage.total}}</b><small>人工验证 ${{p.contact_coverage.verified}} · 跨 Agent ${{p.contact_coverage.cross_agent}}</small></section></div><div class="columns"><section class="panel wide"><h3>为什么值得关注</h3><p>${{esc(p.logic)}}</p><p><b>iMS 场景：</b>${{esc(p.use_case)}}</p></section><section class="panel"><h3>采购窗口</h3><p><b>${{esc(pc.window)}}</b></p><p>${{esc(pc.rationale)}}</p></section><section class="panel"><h3>可观察客户行为</h3>${{bullets(p.behavior)}}</section><section class="panel"><h3>系统推断</h3>${{bullets(p.inferences)}}</section><section class="panel"><h3>水系统</h3><p>${{esc(w.description)}}</p><p><b>规模：</b>${{esc(w.design_scale)}}</p><p><b>工艺：</b>${{esc(w.treatment_process)}}</p></section><section class="panel"><h3>项目生态</h3>${{arr(p.ecosystem).map(x=>`<div class="eco"><b>${{esc(x.role)}}</b><span>${{esc(x.name)}}</span></div>`).join('')}}</section><section class="panel wide"><h3>关键 UNKNOWN / 角色缺口</h3><div class="unknown">${{bullets(p.unknowns)}}</div></section><section class="panel"><h3>建议下一步</h3><p>${{esc(p.next_action||r.recommended_action)}}</p></section><section class="panel wide sources"><h3>证据入口</h3>${{arr(p.sources).slice(0,15).map(u=>`<a href="${{esc(u)}}" target="_blank" rel="noreferrer">${{esc(u)}}</a>`).join('')||'<p class="muted">源文件未提供 URL</p>'}}</section></div>`}}[q,market,priority].forEach(x=>x.oninput=renderList);renderList();
</script></body></html>'''


def main():
    profiles, metadata = build()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(render(profiles, metadata), encoding="utf-8")
    DATA_OUTPUT.write_text(json.dumps({"profiles": profiles, "metadata": metadata}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(profiles)} profiles: {OUTPUT}")


if __name__ == "__main__":
    main()
