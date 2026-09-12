#!/usr/bin/env python3
"""Create the public, mobile-first lead index from Radar and DuMate JSON."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "customer" / "industrial-leads"
PAGE, DATA = OUT / "index.html", OUT / "leads-data.json"

def mask_name(value):
    if not isinstance(value, str) or not value.strip(): return value
    return value[0] + "*" * (len(value.strip()) - 1)

def display_contact_name(value):
    """Keep public organisations readable; mask personal names only."""
    if not isinstance(value, str): return value
    if any(token in value for token in ("公司", "集团", "机构", "中心", "热线", "办公室", "委员会", "研究院", "大学", "局")):
        return value
    return mask_name(value)

def safe(value):
    if isinstance(value, dict): return {k: safe(v) for k, v in value.items()}
    if isinstance(value, list): return [safe(v) for v in value]
    if not isinstance(value, str): return value
    value = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[邮箱已隐藏]", value)
    value = re.sub(r"(?<!\d)(1[3-9]\d)\d{4}(\d{4})(?!\d)", r"\1****\2", value)
    return re.sub(r"(?<=[：:])([\u4e00-\u9fff])([\u4e00-\u9fff]{1,3})", lambda m: m[1] + "*" * len(m[2]), value)

def read(path): return json.loads(path.read_text(encoding="utf-8"))

def municipal_category(signal):
    text = " ".join(str(x or "") for x in (signal.get("company"), signal.get("opportunity"), signal.get("logic")))
    if any(x in text for x in ("水务集团", "联合水务", "首创环保", "北控", "全国", "跨区域")): return "水务集团／跨区域"
    if any(x in text for x in ("自来水", "供水", "二次供水", "净水")): return "供水／二次供水"
    if any(x in text for x in ("污水", "再生水", "排水", "管网")): return "污水／再生水／管网"
    return "其他市政水务"

def industrial_category(signal):
    text = " ".join(str(x or "") for x in (signal.get("industry"), signal.get("company"), signal.get("opportunity"), signal.get("project"))).lower()
    for name, words in (("半导体", ("半导体", "晶圆", "芯片", "fab")), ("新能源／电池", ("电池", "锂", "新能源")), ("化工／材料", ("化工", "材料", "石化")), ("冶金／钢铁", ("钢铁", "冶金", "金属")), ("工业园区／工业污水", ("园区", "工业污水", "废水"))):
        if any(word in text for word in words): return name
    return "其他工业"

def contacts_for(item, contacts):
    result=[]
    contact_ids=item.get("contact_ids") or []
    # Some Dumate records contain contacts keyed by lead_id but omit the
    # redundant contact_ids association on the lead itself.
    if not contact_ids and item.get("lead_id"):
        contact_ids=[cid for cid, contact in contacts.items() if contact.get("lead_id")==item["lead_id"]]
    for cid in contact_ids:
        if cid in contacts:
            contact=safe(json.loads(json.dumps(contacts[cid], ensure_ascii=False))); contact["name"]=display_contact_name(contact.get("name")); contact.pop("email", None)
            phone=contact.get("phone")
            if phone and not isinstance(phone, list):
                contact["phone"]=[phone if isinstance(phone, dict) else {"value":phone}]
            result.append(contact)
    return result

def enriched_rows(segment, directory, patterns):
    files=sorted({p for pattern in patterns for p in directory.glob(pattern)}, key=lambda p:p.name)
    latest, history={},{}
    for path in files:
        source=read(path); contacts={x.get("contact_id"):x for x in source.get("contacts",[])}; projects={x.get("project_id"):x for x in source.get("projects",[])}; accounts={x.get("account_id"):x for x in source.get("accounts",[])}
        stamp=source.get("metadata",{}).get("last_update") or source.get("metadata",{}).get("generated_date") or path.stem
        for item in source.get("leads",[]):
            if item.get("lead_id"):
                history.setdefault(item["lead_id"],[]).append({"file":path.name,"date":stamp}); latest[item["lead_id"]]=(item,contacts,projects,accounts,stamp)
    rows=[]
    for lead_id,(item,contacts,projects,accounts,stamp) in latest.items():
        signal=safe(item.get("original_signal") or {}); evidence=signal.get("evidence") or {}
        # Dumate stores sales-facing enrichment beside original_signal.  Keep it
        # with the signal used by the public view instead of dropping it during
        # the JSON build.
        for key in ("customer_requirement", "customer_need", "current_solution",
                    "operational_pain_points", "pain_points", "sales_summary", "time_window_basis",
                    "validation_questions", "next_validation_questions", "demand_hypothesis", "demand_signals",
                    "prior_attempts", "why_unresolved"):
            if item.get(key) is not None:
                signal[key] = safe(item[key])
        if not signal.get("to_verify"):
            signal["to_verify"] = (signal.get("next_validation_questions")
                                   if signal.get("next_validation_questions") is not None
                                   else signal.get("validation_questions"))
        linked_projects=[safe(projects[x]) for x in item.get("project_ids") or [] if x in projects]
        linked_accounts=[safe(accounts[x]) for x in item.get("account_ids") or [] if x in accounts]
        if not signal.get("location") and linked_projects:
            signal["location"]=linked_projects[0].get("location")
        if not signal.get("industry") and segment=="municipal" and linked_accounts:
            account_type=str(linked_accounts[0].get("type") or "")
            signal["industry"]="市政水务／二次供水" if "water_utility" in account_type else account_type
        if not signal.get("industry") and segment=="municipal" and linked_projects:
            plant_type=str((linked_projects[0].get("water_system_details") or {}).get("plant_type") or "").lower()
            if plant_type=="wastewater": signal["industry"]="市政污水／管网"
            elif plant_type in ("water_supply", "drinking_water"): signal["industry"]="市政供水"
        if not signal.get("location"):
            place_text=" ".join(str(signal.get(k) or "") for k in ("company", "opportunity"))
            place=re.search(r"([\u4e00-\u9fff]{2,8}县)", place_text) or re.search(r"([\u4e00-\u9fff]{2,8}市)", place_text)
            if place: signal["location"]=place.group(1)+"（省市未记录）"
        for key in ("facts","inferences","unknowns"):
            if evidence.get(key) is not None and not isinstance(evidence[key],list): evidence[key]=[evidence[key]]
        category=municipal_category(signal) if segment=="municipal" else industrial_category(signal); date=item.get("last_updated") or item.get("first_seen") or stamp
        rows.append({"segment":segment,"category":category,"date":date,"lead":{"lead_id":lead_id,"company":{"company_name":signal.get("company"),"location":signal.get("location"),"industry":signal.get("industry")},"project":{"project_name":signal.get("opportunity"),"project_stage":signal.get("opportunity_stage")},"signal":{"signal_description":signal.get("opportunity"),"signal_date":date,"evidence":[{"source_url":u,"evidence_summary":"原始数据来源"} for u in signal.get("source_urls",[])]}},"enriched_record":{"original_signal":signal,"enrichment_status":item.get("enrichment_status"),"projects":linked_projects,"accounts":linked_accounts},"enriched_contacts":contacts_for(item,contacts),"history":history.get(lead_id,[])})
    return rows

def industrial_rows():
    rows=[]; by_id={}
    for item in read(OUT/"pipeline-manifest.json").get("leads",[]):
        if item.get("stage1")=="SOURCE_NOT_LINKED": continue
        lead=safe(item.get("lead") or {}); lead_id=lead.get("lead_id")
        if not lead_id: continue
        signal=lead.get("signal") or {}; row={"segment":"industrial","category":industrial_category({**(lead.get("company") or {}),**(lead.get("project") or {})}),"date":item.get("date") or signal.get("signal_date") or "未记录","lead":lead,"enriched_record":None,"enriched_contacts":[],"history":[]}; rows.append(row); by_id[lead_id]=row
    for row in enriched_rows("industrial",ROOT/"intelligence"/"industrial"/"enriched",("indctx*.json",)):
        if row["lead"]["lead_id"] in by_id: by_id[row["lead"]["lead_id"]].update(row)
        else: rows.append(row); by_id[row["lead"]["lead_id"]]=row
    for path in sorted((ROOT/"intelligence"/"industrial"/"daily").glob("*.json")):
        daily=read(path); match=re.search(r"\d{4}-\d{2}-\d{2}",path.name); date=daily.get("report_date") or daily.get("date") or (match.group(0) if match else "未记录")
        for signal in daily.get("signals",[]):
            lead_id=signal.get("id")
            if not lead_id: continue
            radar=safe(signal)
            if lead_id in by_id:
                if not by_id[lead_id].get("enriched_record"): by_id[lead_id]["enriched_record"]={"original_signal":radar,"enrichment_status":"radar_daily"}
                continue
            lead={"lead_id":lead_id,"company":{"company_name":signal.get("company"),"location":signal.get("location"),"industry":signal.get("industry")},"project":{"project_name":signal.get("project") or signal.get("opportunity") or signal.get("trigger"),"project_stage":signal.get("opportunity_stage")},"signal":{"signal_description":signal.get("trigger"),"signal_date":date,"evidence":[{"source_url":x,"evidence_summary":"工业雷达日报"} for x in signal.get("source_urls",[])]}}
            row={"segment":"industrial","category":industrial_category(signal),"date":date,"lead":lead,"enriched_record":{"original_signal":radar,"enrichment_status":"radar_daily"},"enriched_contacts":[],"history":[]}; rows.append(row); by_id[lead_id]=row
    return rows

def normalize(value):
    return re.sub(r"[^\w\u4e00-\u9fff]", "", str(value or "")).lower()

def municipal_rows():
    """Use the municipal master file, plus genuine new daily discoveries."""
    directory=ROOT/"intelligence"/"municipal"/"enriched"
    patterns=("indctx*.json",) if list(directory.glob("indctx*.json")) else ("ctx*.json",)
    rows=enriched_rows("municipal",directory,patterns)
    known=[normalize(v) for row in rows for v in (row["lead"]["company"].get("company_name"),row["lead"]["project"].get("project_name")) if normalize(v)]
    def already_known(value):
        return any(value in key or key in value or (len(value)>8 and len(key)>8 and value[:8]==key[:8]) for key in known)
    industrial_terms=("半导体","电池","化工","工业污水","工业园区","工业废水","石化")
    for path in sorted((ROOT/"intelligence"/"municipal"/"daily").glob("*.json")):
        daily=read(path); date=daily.get("date") or re.search(r"\d{4}-\d{2}-\d{2}",path.name).group(0)
        for number,item in enumerate(daily.get("opportunities",[]),1):
            name=item.get("name") or item.get("opportunity")
            compact=normalize(name)
            if not name or any(word in str(name) for word in industrial_terms) or (compact and already_known(compact)):
                continue
            facts=item.get("public_facts") or []
            if not isinstance(facts,list): facts=[facts]
            signal=safe({"company":name,"opportunity":name,"opportunity_stage":item.get("opportunity_stage"),"priority":item.get("priority"),"score":item.get("score") or item.get("public_signal_score"),"potential_ims_use_case":item.get("potential_ims_use_case"),"logic":item.get("logic_chain_check") or item.get("ai_judgment"),"to_verify":item.get("to_verify") or item.get("agent_checklist"),"source_urls":[item.get("source_url")] if item.get("source_url") else [],"evidence":{"facts":facts,"inferences":[item.get("ai_judgment")] if item.get("ai_judgment") else []}})
            lead={"lead_id":item.get("id") or f"MUN-DAILY-{date}-{number:03d}","company":{"company_name":name,"location":None,"industry":None},"project":{"project_name":name,"project_stage":item.get("opportunity_stage")},"signal":{"signal_description":name,"signal_date":date,"evidence":[{"source_url":u,"evidence_summary":"市政雷达日报"} for u in signal["source_urls"]]}}
            rows.append({"segment":"municipal","category":municipal_category(signal),"date":date,"lead":lead,"enriched_record":{"original_signal":signal,"enrichment_status":"radar_daily"},"enriched_contacts":[],"history":[{"file":path.name,"date":date}]})
            known.append(compact)
    return rows

def model():
    rows=industrial_rows()+municipal_rows(); rows.sort(key=lambda x:(str(x["date"]),x["lead"]["lead_id"]),reverse=True); return {"leads":rows}

def page():
    css=r''':root{--ink:#17212b;--muted:#647582;--line:#d9e4e8;--bg:#f4f7f8;--blue:#0e628c;--mun:#176a49}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}main{max-width:1180px;margin:auto;padding:16px}h1,h2,h3,p{margin:0}h1{font-size:clamp(25px,5vw,36px)}.muted{font-size:14px;color:var(--muted)}.toolbar{padding:8px 0}.search{width:100%;padding:12px;border:1px solid #b8cbd4;border-radius:10px;background:#fff;font:inherit}.filters{display:flex;gap:7px;overflow-x:auto;padding:9px 0 2px}.filter{flex:0 0 auto;border:1px solid #b8cbd4;border-radius:99px;padding:6px 11px;background:#fff;font:14px inherit;cursor:pointer}.filter.selected{background:var(--blue);border-color:var(--blue);color:#fff}.filter.municipal.selected{background:var(--mun);border-color:var(--mun)}.layout{display:grid;grid-template-columns:335px minmax(0,1fr);gap:14px;align-items:start}.list,.detail,details{background:#fff;border:1px solid var(--line);border-radius:13px}.list{position:sticky;top:12px;max-height:calc(100vh - 24px);overflow:auto}.day{padding:8px 12px;background:#f7fafb;border-bottom:1px solid var(--line);font-size:13px;font-weight:700;color:var(--muted)}.row{display:block;width:100%;padding:10px 12px;text-align:left;border:0;border-bottom:1px solid #edf2f4;background:#fff;font:inherit;cursor:pointer}.row.active,.row:hover{background:#e8f4f8}.row b,.row span,.row small{display:block;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}.row small{color:var(--muted);font-size:13px}.tag{display:inline-block;margin:5px 5px 0 0;padding:2px 7px;border-radius:99px;background:#e8f2f7;color:var(--blue);font-size:12px}.tag.mun{background:#e7f5ed;color:var(--mun)}.detail{padding:16px}.detail h2{font-size:25px;line-height:1.25}.matrix{display:grid;grid-template-columns:120px 1fr;border:1px solid var(--line);border-radius:10px;overflow:hidden;margin-top:12px}.matrix div{padding:8px 10px;border-bottom:1px solid var(--line)}.matrix div:nth-last-child(-n+2){border-bottom:0}.matrix .k{background:#f5f8fa;color:var(--muted);font-size:13px}.section{margin-top:12px;padding:13px;border:1px solid;border-radius:12px}.section.blue{background:#edf7fb;border-color:#b8dbe9}.section.amber{background:#fff8e8;border-color:#e7d39b}.section.green{background:#eef8f1;border-color:#badcc5}.section h3{font-size:17px;margin-bottom:7px}.section ul{margin:0;padding-left:20px}.section li+li{margin-top:7px}.contact{padding:9px 0;border-bottom:1px solid #cfe3d5}.contact:last-child{border:0}details{margin-top:12px;padding:11px}summary{cursor:pointer;color:var(--blue);font-weight:700}.empty{padding:20px;color:var(--muted)}a{color:var(--blue);word-break:break-all}@media(max-width:760px){main{padding:12px}.layout{display:block}.list{position:static;max-height:none;margin-bottom:12px}.detail{padding:13px}.matrix{grid-template-columns:96px 1fr}.filters{padding-bottom:8px}}'''
    js=r'''const data=await fetch('./leads-data.json?'+Date.now(),{cache:'no-store'}).then(r=>r.json()),esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])),list=document.querySelector('.list'),detail=document.querySelector('.detail'),search=document.querySelector('#search'),segment=document.querySelector('#segment'),category=document.querySelector('#category');let seg='all',cat='all',chosen=0;const labels={all:'全部线索',industrial:'工业',municipal:'市政'};function cats(){return [...new Set(data.leads.filter(x=>seg==='all'||x.segment===seg).map(x=>x.category))].sort()}function makeFilters(){segment.innerHTML=['all','industrial','municipal'].map(x=>`<button class="filter ${x===seg?'selected':''} ${x==='municipal'?'municipal':''}" data-s="${x}">${labels[x]}（${x==='all'?data.leads.length:data.leads.filter(r=>r.segment===x).length}）</button>`).join('');category.innerHTML=`<button class="filter selected" data-c="all">全部类别</button>`+cats().map(x=>`<button class="filter" data-c="${esc(x)}">${esc(x)}</button>`).join('');segment.querySelectorAll('button').forEach(b=>b.onclick=()=>{seg=b.dataset.s;cat='all';makeFilters();render()});category.querySelectorAll('button').forEach(b=>b.onclick=()=>{cat=b.dataset.c;category.querySelectorAll('button').forEach(x=>x.classList.toggle('selected',x===b));render()})}function rows(){const q=search.value.trim().toLowerCase();return data.leads.map((r,i)=>({r,i})).filter(x=>(seg==='all'||x.r.segment===seg)&&(cat==='all'||x.r.category===cat)&&(!q||JSON.stringify(x.r).toLowerCase().includes(q)))}function render(){const rs=rows(),days=[...new Set(rs.map(x=>x.r.date))].sort().reverse();list.innerHTML=days.length?days.map(d=>`<div class="day">${esc(d)}</div>`+rs.filter(x=>x.r.date===d).map(x=>`<button class="row" data-i="${x.i}"><b>${esc(x.r.lead.company?.company_name||'名称未记录')}</b><span>${esc(x.r.lead.project?.project_name||x.r.lead.signal?.signal_description||'项目未记录')}</span><small><i class="tag ${x.r.segment==='municipal'?'mun':''}">${labels[x.r.segment]}／${esc(x.r.category)}</i></small></button>`).join('')).join(''):'<div class="empty">没有匹配线索</div>';list.querySelectorAll('.row').forEach(b=>b.onclick=()=>show(+b.dataset.i,true));const visible=rs.map(x=>x.i);show(visible.includes(chosen)?chosen:visible[0]||0)}const facts=x=>(x||[]).map(v=>`<li>${esc(typeof v==='string'?v:JSON.stringify(v))}</li>`).join('')||'<li>未记录</li>';function show(i,scroll=false){chosen=i;const r=data.leads[i],l=r.lead||{},e=r.enriched_record||{},s=e.original_signal||{},ev=s.evidence||{},contacts=r.enriched_contacts||[],sources=s.source_urls||l.signal?.evidence?.map(x=>x.source_url).filter(Boolean)||[];list.querySelectorAll('.row').forEach(x=>x.classList.toggle('active',+x.dataset.i===i));const matrix=a=>`<div class="matrix">${a.map(([k,v])=>`<div class="k">${esc(k)}</div><div>${esc(v||'未记录')}</div>`).join('')}</div>`;detail.innerHTML=`<h2>${esc(l.company?.company_name||s.company||'名称未记录')}</h2><p class="muted">${esc(l.lead_id)} · ${esc(r.date)} <i class="tag ${r.segment==='municipal'?'mun':''}">${labels[r.segment]}／${esc(r.category)}</i></p>${matrix([['项目',l.project?.project_name||s.opportunity],['项目阶段',s.opportunity_stage||l.project?.project_stage],['行业／地区',`${s.industry||l.company?.industry||'未记录'} / ${s.location||l.company?.location||'未记录'}`],['优先级／时间窗口',`${s.priority||s.signal_tier||'未记录'} / ${s.estimated_time_window||'未记录'}`]])}<section class="section blue"><h3>项目背景与公开事实</h3><ul>${facts(ev.facts?.length?ev.facts:[l.signal?.signal_description].filter(Boolean))}</ul></section><section class="section amber"><h3>客户需求与待核实事项</h3>${matrix([['客户需求',s.customer_requirement||s.customer_need],['当前方案／痛点',(ev.inferences||[]).join('；')],['待核实',(Array.isArray(s.to_verify)?s.to_verify:Object.values(s.to_verify||{})).join('；')]])}</section><section class="section green"><h3>软件机会与建议行动</h3>${matrix([['潜在应用',s.potential_ims_use_case],['判断逻辑',s.logic],['建议行动',e.ims_recommendation?.recommended_action||s.pull_box?.next_validation_question]])}</section><section class="section green"><h3>联系人（${contacts.length}）</h3>${contacts.length?contacts.map(c=>`<div class="contact"><b>${esc(c.name||'姓名未记录')}</b> · ${esc(c.title||c.role||'职务未记录')}<br>${esc((c.phone||[]).map(p=>p.value).join('；')||'联系方式未公开')}</div>`).join(''):'<p class="muted">原始资料未关联联系人。</p>'}</section><details><summary>原始资料字段与来源</summary>${matrix(Object.entries(e).filter(([k])=>k!=='original_signal').map(([k,v])=>[k,typeof v==='string'?v:JSON.stringify(v)]))}<ul>${sources.map(x=>`<li><a target="_blank" rel="noreferrer" href="${esc(x)}">${esc(x)}</a></li>`).join('')||'<li>未记录来源链接</li>'}</ul></details>`;if(scroll)detail.scrollIntoView({behavior:'smooth',block:'start'})}search.oninput=render;makeFilters();render();if(matchMedia('(min-width:761px)').matches)setInterval(()=>location.reload(),300000);'''
    js = js.replace("const labels=", "for(const r of data.leads){for(const c of r.enriched_contacts||[]){if(c.phone&&!Array.isArray(c.phone))c.phone=[typeof c.phone==='object'?c.phone:{value:c.phone}]}}const labels=")
    js = js.replace("(c.phone||[]).map(p=>p.value).join('；')", "(Array.isArray(c.phone)?c.phone:(c.phone?[c.phone]:[])).map(p=>typeof p==='object'?(p.value||p.number||p.mobile||''):p).filter(Boolean).join('；')")
    old_contact = '''<b>${esc(c.name||'姓名未记录')}</b> · ${esc(c.title||c.role||'职务未记录')}<br>${esc((Array.isArray(c.phone)?c.phone:(c.phone?[c.phone]:[])).map(p=>typeof p==='object'?(p.value||p.number||p.mobile||''):p).filter(Boolean).join('；')||'联系方式未公开')}'''
    new_contact = '''<b>${esc(c.name||'姓名未记录')}</b> · ${esc(c.title||c.role||'职务未记录')}${c.unit?`<br><span class="muted">${esc(c.unit)}</span>`:''}<br>${esc((Array.isArray(c.phone)?c.phone:(c.phone?[c.phone]:[])).map(p=>typeof p==='object'?(p.value||p.number||p.mobile||''):p).filter(Boolean).join('；')||'联系方式未公开')}'''
    js = js.replace(old_contact, new_contact)
    js = js.replace("s=e.original_signal||{},ev=s.evidence||{},contacts", "s=e.original_signal||{},ev=s.evidence||{},project=(e.projects||[])[0]||{},account=(e.accounts||[])[0]||{},water=project.water_system_details||{},contacts")
    js = js.replace("<section class=\"section amber\"><h3>客户需求与待核实事项</h3>${matrix([['客户需求',s.customer_requirement||s.customer_need],['当前方案／痛点',(ev.inferences||[]).join('；')],['待核实',(Array.isArray(s.to_verify)?s.to_verify:Object.values(s.to_verify||{})).join('；')]])}</section>", "<section class=\"section blue\"><h3>项目与系统现状</h3>${matrix([['现有平台',account.existing_digital_platform||account.digitalization_status],['仪表／系统要求',water.instrument_requirements],['当前合作／进展',account.latest_signal]])}</section><section class=\"section amber\"><h3>客户需求与待核实事项</h3>${matrix([['客户明确需求',s.customer_requirement||s.customer_need],['重点待核实',(Array.isArray(s.to_verify)?s.to_verify:Object.values(s.to_verify||{})).join('；')],['建议优先确认',account.action_needed||s.pull_box?.next_validation_question]])}</section>")
    js = js.replace("['判断逻辑',s.logic]", "['判断摘要',(ev.inferences||[]).map(x=>String(x).split('。')[0]).filter(Boolean).slice(0,2).join('；')||s.logic]")
    js = js.replace("['优先级／时间窗口',`${s.priority||s.signal_tier||'未记录'} / ${s.estimated_time_window||'未记录'}`]", "['优先级／时间窗口',`${s.priority||s.signal_tier||'未记录'} / ${s.estimated_time_window||'未记录'}`],['时间窗口依据',s.time_window_basis]")
    js = js.replace("<section class=\"section blue\"><h3>项目与系统现状</h3>", "<section class=\"section green\"><h3>销售摘要</h3>${matrix([['机会概述',s.sales_summary],['需求假设',s.demand_hypothesis],['既往尝试',s.prior_attempts],['未解决原因',s.why_unresolved]])}</section><section class=\"section blue\"><h3>项目与系统现状</h3>")
    js = js.replace("['现有平台',account.existing_digital_platform||account.digitalization_status],['仪表／系统要求',water.instrument_requirements]", "['当前方案',s.current_solution||account.existing_digital_platform||account.digitalization_status],['业务痛点',s.operational_pain_points||s.pain_points||water.instrument_requirements]")
    # Raw nested JSON made the disclosure table wider than the page.  The lead
    # fields are rendered above; keep this disclosure as a compact provenance
    # summary and the usable source links.
    old_details = '''<details><summary>原始资料字段与来源</summary>${matrix(Object.entries(e).filter(([k])=>k!=='original_signal').map(([k,v])=>[k,typeof v==='string'?v:JSON.stringify(v)]))}<ul>${sources.map(x=>`<li><a target="_blank" rel="noreferrer" href="${esc(x)}">${esc(x)}</a></li>`).join('')||'<li>未记录来源链接</li>'}</ul></details>'''
    new_details = '''<details><summary>原始资料与来源</summary>${matrix([['数据状态',e.enrichment_status],['关联项目／账户',`${(e.projects||[]).length} / ${(e.accounts||[]).length}`],['关联联系人',contacts.length],['公开来源',sources.length]])}<ul>${sources.map(x=>`<li><a target="_blank" rel="noreferrer" href="${esc(x)}">${esc(x)}</a></li>`).join('')||'<li>未记录来源链接</li>'}</ul></details>'''
    js = js.replace(old_details, new_details)
    css += '.matrix div{min-width:0;overflow-wrap:anywhere;word-break:break-word}'
    mobile_css = r'''@media(max-width:760px){.back-to-list{display:inline-block;margin:0 0 12px;padding:6px 10px;border:1px solid #b8cbd4;border-radius:8px;background:#fff;color:#0e628c;font:inherit}.show-detail .list{display:none}.show-detail .detail{margin-top:0}}@media(min-width:761px){.back-to-list{display:none}}'''
    mobile_js = r'''if(matchMedia('(max-width:760px)').matches){document.addEventListener('click',event=>{if(event.target.closest('.row'))setTimeout(()=>{document.body.classList.add('show-detail');if(!detail.querySelector('.back-to-list'))detail.insertAdjacentHTML('afterbegin','<button class="back-to-list" type="button">← 返回线索列表</button>');window.scrollTo(0,0)},0)});detail.addEventListener('click',event=>{if(event.target.closest('.back-to-list')){document.body.classList.remove('show-detail');window.scrollTo(0,0)}})}'''
    return f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>靖帆IMS Intelligence</title><style>{css}{mobile_css}</style><main><h1>靖帆IMS Intelligence</h1><p class="muted">工业与市政线索 · 数据自动同步仓库 JSON</p><div class="toolbar"><input id="search" class="search" placeholder="搜索公司、项目、省份、城市、事实或联系人"><div id="segment" class="filters"></div><div id="category" class="filters"></div></div><div class="layout"><aside class="list"></aside><article class="detail"></article></div></main><script type="module">{js}{mobile_js}</script></html>'

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True); DATA.write_text(json.dumps(model(),ensure_ascii=False,indent=2),encoding="utf-8"); PAGE.write_text(page(),encoding="utf-8")
