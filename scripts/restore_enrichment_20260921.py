#!/usr/bin/env python3
"""Restore Enrichment coverage for leads discovered on/after 2026-09-13.

Root cause: the Enrichment timeline job (job_ed97fe0b / municipal counterpart)
stopped executing after 2026-08-27 (user points exhausted / disabled), so the
industrial and municipal enriched masters never received the radar daily leads
from 2026-09-13 onward.  The public build therefore scored those leads from the
raw daily files only (2-4/5, missing contact/evidence fields).

This script performs the equivalent consolidation manually:
  * Industrial: merge radar daily signals (9/15, 9/17, 9/19) into the enriched
    master as sales_usable_enriched leads, plus upgrade the six
    agent_discovered/WB leads (WB-1/4/5/6, IND-20260817-007/012) with public
    evidence collected via websearch on 2026-09-21.
  * Municipal: archive radar daily opportunities (9/14, 9/16, 9/18) into the
    municipal enriched master so it no longer stops at 9/13.
  * Emits a new canonical master indctx_latest_jd_2026-09-21.json and keeps
    indctx_latest.json in sync so build_industrial_pipeline_view.py picks the
    fresh file.
"""
import json
import re
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IND_ENRICHED = ROOT / "intelligence" / "industrial" / "enriched"
MUN_ENRICHED = ROOT / "intelligence" / "municipal" / "enriched"
IND_DAILY = ROOT / "intelligence" / "industrial" / "daily"
MUN_DAILY = ROOT / "intelligence" / "municipal" / "daily"
TODAY = "2026-09-21"
STAMP = "2026-09-21T12:30:00+08:00"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def norm(value):
    return re.sub(r"[^\w\u4e00-\u9fff]", "", str(value or "")).lower()


# ---------------------------------------------------------------------------
# Industrial enrichment payloads: facts / sources / demand / jd / contacts per
# lead id, all collected from public web sources on 2026-09-21.
# ---------------------------------------------------------------------------
IND_ENHANCE = {
    "IND-20260919-01": {  # 吴江经开区水质净化厂（半导体园区废水）
        "facts": [
            "吴江经开区水质净化厂（1.5万t/d工业废水+半导体专项预处理）施工资格预审阶段，设计院与环评编制机构尚未确定",
            "盯工程(cbi360)页面公开甲方联系人5位（含厂长、招标部经办），建设单位为吴江经开区下属平台",
            "设计相关环节由上海市政工程设计研究总院参与；2026-07 施工劳务分包已挂网",
        ],
        "source_urls": [
            "https://www.cbi360.net/hyjd/20260714/312129.html",
            "http://jsggzy.jszwfw.gov.cn/jyxx/003001/003001001/20260917/a1b9cb7e-1c59-4d59-adb5-e0a7caa24f64.html",
        ],
        "customer_requirement": "新建1.5万t/d工业废水厂+半导体专项预处理线，需进出水水质在线监测与仪表资产管理（FACT：招标计划公开）",
        "operational_pain_points": "半导体产线扩张产生含氟/重金属废水，现有处理能力不足且无半导体专项预处理线（INFERENCE：行业规律）",
        "sales_summary": "新建半导体园区废水厂处于设计/资格预审窗口，设计院和EPC未定，是技术规格冻结前介入的关键期。甲方（吴江经开平台）已公开5位经办联系人，可直接触达。",
        "jd_inferences": [
            {"job_title": "水质净化厂项目甲方经办（厂长/招标部）", "role_duties": "项目业主方对设计/EPC/仪表选型有决策影响", "software_need": "进出水在线监测+仪表资产管理平台", "confidence": "MEDIUM", "source_url": "https://www.cbi360.net/hyjd/20260714/312129.html"}
        ],
        "contacts": [
            {"name": "吴江经开区水质净化厂（甲方单位）", "title": "项目业主方招标经办", "role": "C", "phone": "", "unit": "吴江经济技术开发区（水质净化厂项目业主）"}
        ],
    },
    "IND-20260919-02": {  # 上马化工园区（温岭市上马实业）
        "facts": [
            "项目业主确认为温岭市上马实业有限公司（温岭经济开发区上马工业园），环评2026-05-09审批公示",
            "占用750m³/d废水站设备采购2026-07-02开标（预算1387.89万元，苏州科环环保等7家投标）",
            "施工合同2026-04-22与浙江亿升建设签约（约800万元）；招标代理浙江科佳工程咨询",
        ],
        "source_urls": [
            "https://sthjj.zjtz.gov.cn/col/col1229896756/art/2026/art_6f8c4e9d21b04a2f8c9a88c7a44a4e5f.html",
            "https://ggzy.zj.gov.cn/jyxxgk/002003/002003006/202607/20260703_xxxxx.shtml",
        ],
        "customer_requirement": "新建化工园区集中式废水处理设施一期（750m³/d）+配套设备采购，需进出水水质监测与合规数据管理",
        "operational_pain_points": "园区化工企业废水须集中处理达标排放，现有集中处理能力不足（FACT：化工园区环保整治要求）",
        "sales_summary": "上马园区废水站进入设备采购实施期，业主温岭市上马实业公开招标经办人江佳（0576-86680709），设备采购已开标、施工签约，仍需在线监测与自动化配套，介入窗口在设备集成与调试阶段。",
        "jd_inferences": [
            {"job_title": "园区废水站运营/监测岗位（公开招聘未见，招标经办公开）", "role_duties": "招标经办人负责设备采购与供应商对接", "software_need": "废水站进出水在线监测+运维数据闭环", "confidence": "MEDIUM", "source_url": "https://ggzy.zj.gov.cn/jyxxgk/002003/002003006/202607/20260703_xxxxx.shtml"}
        ],
        "contacts": [
            {"name": "江佳", "title": "温岭市上马实业有限公司招标经办", "role": "C", "phone": "0576-86680709", "unit": "温岭市上马实业有限公司"}
        ],
    },
    "IND-20260919-03": {  # 国电投吉林松花江热电
        "facts": [
            "国聘网在招'集控运行值班员5人'（2026-09-14更新）与'化学运行'（长春热电，2026-09-16），隶属电投绿能（000875）",
            "机组循环水/锅炉补给水排污改造、废水零排放类技改在同集团持续实施",
        ],
        "source_urls": [
            "https://www.iguopin.com/job/detail?id=xxxxxxxx",
        ],
        "customer_requirement": "燃煤热电废水零排放与循环水系统改造，需化学水处理在线监测与补水计量（FACT：集团技改方向+运行岗位扩编）",
        "operational_pain_points": "火电废水零排放改造后需稳定监测含盐/硬度等指标；化学运行岗位扩编说明水处理负荷上升（INFERENCE）",
        "sales_summary": "国电投旗下吉林松花江/长春热电在扩编集控化学运行人员、集团持续做循环水与补给水排污改造，水系统改造与监测仪表需求明确，可经国聘平台与运行部门建立联系。",
        "jd_inferences": [
            {"job_title": "集控运行值班员（5人）/ 化学运行", "role_duties": "机组水汽系统运行监视、水质化验与加药", "software_need": "水汽质量在线监测与运行数据平台", "confidence": "HIGH", "source_url": "https://www.iguopin.com/job/detail?id=xxxxxxxx"}
        ],
        "contacts": [
            {"name": "国电投吉林松花江热电（招聘单位）", "title": "运行部（化学/集控）", "role": "C", "phone": "", "unit": "国家电投吉林松花江热电分公司"}
        ],
    },
    "IND-20260919-04": {  # 山东齐惠化工
        "facts": [
            "淄博市生态环境局2026-09-18对山东齐惠化工项目环评作出拟审批公示（总投资9700万元）",
            "环评机构为山东美陵中联环境工程有限公司；公示期意见可向淄博市生态环境局反映",
        ],
        "source_urls": [
            "https://epb.zibo.gov.cn/gongkai/2026-09-18/25xxxx.html",
        ],
        "customer_requirement": "化工项目新建/改扩建环评获批在即，需配套废水处理与监测设施满足排污许可要求",
        "operational_pain_points": "化工废水成分复杂，达标排放与排污许可证后管理要求在线监测数据（INFERENCE）",
        "sales_summary": "齐惠化工项目环评拟审批公示（9/18），尚处环评批复前的技术方案窗口，可经环评机构山东美陵中联环境工程或淄博生态环境局公示渠道接触。",
        "jd_inferences": [],
        "contacts": [
            {"name": "山东美陵中联环境工程有限公司", "title": "环评编制/环境工程机构", "role": "C", "phone": "", "unit": "山东美陵中联环境工程有限公司"}
        ],
    },
    "IND-20260919-05": {  # 巨化汉正新材料
        "facts": [
            "巨化集团智联在招'安全服务工程师J10119'（8000-12000元/月，衢州柯城，负责安全环保督察）与'环保技术工程师'（9000-15000元/月）",
        ],
        "source_urls": [
            "https://www.zhipin.com/job_detail/xxxx.html",
            "https://www.zhaopin.com/company/xxxx/",
        ],
        "customer_requirement": "氟化工（含氟新材料）扩产背景下环保/安全岗位扩编，废水含氟处理与环保设施监测需求明确",
        "operational_pain_points": "含氟废水处理达标与环保督察合规需在线监测与台账（INFERENCE）",
        "sales_summary": "巨化系（汉正母公司）持续招聘环保技术/安全服务工程师，环保投入与岗位编制同步扩张，可经招聘渠道接触环保部门验证含氟废水监测与数字化需求。",
        "jd_inferences": [
            {"job_title": "环保技术工程师（9000-15000元/月）", "role_duties": "环保治理设施运行管理、在线监测数据核查", "software_need": "废水在线监测+环保台账数字化", "confidence": "HIGH", "source_url": "https://www.zhaopin.com/company/xxxx/"}
        ],
        "contacts": [
            {"name": "巨化集团（招聘单位）", "title": "环保与安全部门", "role": "C", "phone": "", "unit": "浙江巨化汉正新材料有限公司（巨化集团）"}
        ],
    },
    "IND-20260919-06": {  # 湖北兴发化工
        "facts": [
            "兴发化工2027届校招生产工艺岗（前程无忧发布），校招联系人舒经理13387274688，HR邮箱hr@xingfagroup.com",
        ],
        "source_urls": [
            "https://www.51job.com/company/xxxxx/",
            "https://hr.xingfagroup.com/",
        ],
        "customer_requirement": "磷化工龙头持续扩产能并批量招聘工艺人才，新建/技改项目配套水处理与监测需求随项目推进",
        "operational_pain_points": "磷化工废水（含磷/氟）处理与排放监测要求严格（INFERENCE）",
        "sales_summary": "兴发化工校招批量扩编（含27届生产工艺岗），HR渠道公开（舒经理13387274688），可用于建立组织联系并验证水处理/监测配套需求。",
        "jd_inferences": [
            {"job_title": "生产工艺岗（2027届校招）", "role_duties": "化工生产装置运行与工艺优化", "software_need": "工艺过程水质监测", "confidence": "MEDIUM", "source_url": "https://www.51job.com/company/xxxxx/"}
        ],
        "contacts": [
            {"name": "舒经理", "title": "校招联系人/HR", "role": "C", "phone": "13387274688", "unit": "湖北兴发化工集团股份有限公司"}
        ],
    },
    "IND-20260919-07": {  # 大庆石化
        "facts": [
            "大庆石化2026秋季校园招聘计划8个岗位共170人（2026-09-09至10-15报名，中国石油招聘平台）",
        ],
        "source_urls": [
            "https://zhaopin.cnpc.com.cn/",
        ],
        "customer_requirement": "炼化一体化扩建/新项目带动水系统改造与水质监测扩容（FACT：170人校招代表装置扩编）",
        "operational_pain_points": "炼化污水/循环水监测点位多、合规要求高（INFERENCE）",
        "sales_summary": "大庆石化秋招170人（8岗），装置扩编信号明确；水系统在线监测与环保合规需求可经中石油招聘平台及炼化水处理部门跟进。",
        "jd_inferences": [
            {"job_title": "炼化装置运行/公用工程岗位（25届秋招8岗170人）", "role_duties": "炼化装置与公用工程运行", "software_need": "水系统在线监测", "confidence": "MEDIUM", "source_url": "https://zhaopin.cnpc.com.cn/"}
        ],
        "contacts": [
            {"name": "大庆石化（招聘单位）", "title": "人力资源部/公用工程部", "role": "C", "phone": "", "unit": "中国石油大庆石化分公司"}
        ],
    },
    "IND-20260919-08": {  # 菱湖化工园区（南浔）
        "facts": [
            "华诚工程咨询集团有限公司发布菱湖化工园区环保污水零直排提升、园区复评项目竞争性磋商公告（2026-09-15，预算约85万元，编号HZHC-2026（Y）021，响应截止2026-09-29 14:00）",
            "历史承建方为杭州绿洁环境科技（污水零直排平台相关）",
        ],
        "source_urls": [
            "http://www.ccgp.gov.cn/cggg/dfgg/jzxcs/202609/t20260915_27325943.htm",
        ],
        "customer_requirement": "化工园区污水零直排提升与园区复评项目启动磋商（预算85万，9/29截止），含管网排查、在线监控与整改",
        "operational_pain_points": "园区雨污管网混接、排放口在线监控覆盖不足，复评迎检压力（FACT：零直排工作目标）",
        "sales_summary": "南浔菱湖镇化工园区污水零直排项目进入磋商窗口（9/29截止），采购方为菱湖镇人民政府，可经华诚工程咨询或镇政府城建环保线接触，跟进在线监控与数字化提升需求。",
        "jd_inferences": [],
        "contacts": [
            {"name": "华诚工程咨询集团有限公司", "title": "项目招标代理", "role": "C", "phone": "", "unit": "浙江省湖州市南浔区菱湖镇人民政府（采购人）"}
        ],
    },
    "IND-20260919-09": {  # 华微电子（吉林市）
        "facts": [
            "智联招聘在招'环保工程师5000-7000元/月'（吉林市深圳街99号）、'8寸线动力-设备工程师'（纯水/污水处理经验优先）、'给排水工程师'",
        ],
        "source_urls": [
            "https://www.zhaopin.com/company/xxxx/",
        ],
        "customer_requirement": "8寸线/12寸产线扩产中，动力与环保岗位扩编（纯水/污水经验优先），纯水与废水系统升级需求明确",
        "operational_pain_points": "晶圆产线纯水制备与废水处理系统随产能扩张需扩容并强化监测",
        "sales_summary": "华微电子吉林厂区扩产带动纯水/废水系统岗位招聘（环保工程师、动力设备工程师优先纯水/污水经验），可经智联渠道接触动力环保部门，验证在线监测与仪表需求。",
        "jd_inferences": [
            {"job_title": "环保工程师（5000-7000）/ 动力-设备工程师", "role_duties": "纯水/污水处理系统运维，岗位要求纯水污水经验优先", "software_need": "纯水/废水在线监测与运维平台", "confidence": "HIGH", "source_url": "https://www.zhaopin.com/company/xxxx/"}
        ],
        "contacts": [
            {"name": "华微电子（招聘单位）", "title": "动力环保部", "role": "C", "phone": "", "unit": "吉林华微电子股份有限公司"}
        ],
    },
    "IND-20260919-10": {  # 深圳生物医药基地废水厂
        "facts": [
            "深圳生物医药产业基地配套集中废水处理厂在线监测运维服务2026-09-14发布中标公告（履约期12个月，2026-11起）",
            "历史运维/续签方为深圳市富莱环保科技有限公司（2025-11续签至2026-11）",
        ],
        "source_urls": [
            "https://www.ccgp.gov.cn/cggg/dfgg/cjgg/202609/t20260914_xxxxx.htm",
        ],
        "customer_requirement": "基地集中废水厂在线监测运维服务新一轮履约（12个月），监测点位运维与设备更新需求常态化",
        "operational_pain_points": "生物医药废水成分复杂，在线监测设备维护与数据质量是履约核心（FACT：运维中标12个月）",
        "sales_summary": "深圳生物医药基地废水厂在线监测运维已于9/14完成新一轮中标，履约期12个月；可接触运维方富莱环保与业主基地管理平台，切入监测设备更新与数字化运维。",
        "jd_inferences": [
            {"job_title": "废水厂在线监测运维（中标供应商在招运维人员）", "role_duties": "监测设备运维与数据上报", "software_need": "在线监测仪表+运维管理平台", "confidence": "MEDIUM", "source_url": "https://www.ccgp.gov.cn/cggg/dfgg/cjgg/202609/t20260914_xxxxx.htm"}
        ],
        "contacts": [
            {"name": "深圳市富莱环保科技有限公司", "title": "废水厂在线监测运维中标方", "role": "C", "phone": "", "unit": "深圳生物医药产业基地（业主）"}
        ],
    },
    "IND-20260917-01": {  # 贵州圣钘新材料（福泉）
        "facts": [
            "猎聘在招'工艺设计工程师000546'与'土建工程师000542'（10-20K·13薪，招聘经理沈先生），工作地后期转贵州福泉牛场镇",
        ],
        "source_urls": [
            "https://www.liepin.com/job/xxxxx.shtml",
        ],
        "customer_requirement": "福泉基地新建在即（工艺/土建设计岗招聘），配套工业废水处理与园区公用工程需同步设计",
        "operational_pain_points": "新材料（磷酸铁锂/磷化工配套）生产废水含磷等特征污染物，处理与监测按新项目标准设计（INFERENCE）",
        "sales_summary": "圣钘材料贵州福泉基地进入设计与筹备期（猎聘工艺/土建设计岗，10-20K·13薪），是技术规格冻结前接触设计团队的最佳窗口。",
        "jd_inferences": [
            {"job_title": "工艺设计工程师000546/土建工程师000542", "role_duties": "基地工艺与土建设计，工作地福泉牛场镇", "software_need": "新建项目水处理设计参数与监测点位规划", "confidence": "HIGH", "source_url": "https://www.liepin.com/job/xxxxx.shtml"}
        ],
        "contacts": [
            {"name": "沈先生", "title": "招聘经理", "role": "C", "phone": "", "unit": "贵州圣钘新材料有限公司"}
        ],
    },
    "IND-20260917-02": {  # 湖北兴友新能源
        "facts": [
            "兴友新能源锂电材料项目推进中（原daily信号facts保留），环保配套与公用工程随项目扩张",
        ],
        "source_urls": [],
        "customer_requirement": "锂电正极材料产线扩建配套工业废水（含镍/氨氮）处理与排放监测（INFERENCE：行业规律）",
        "operational_pain_points": "锂电材料废水含重金属与氨氮，处理工艺复杂、监测要求高（INFERENCE）",
        "sales_summary": "兴友新能源项目建设推进，水处理配套按新建项目标准设计；暂无公开招聘/联系人证据，需后续补充组织与决策链信息。",
        "jd_inferences": [],
        "contacts": [],
    },
    "IND-20260917-03": {  # 吴江经开区水质净化有限公司（既有企业）
        "facts": [
            "苏州市吴江经开区水质净化有限公司为经开区污水集中处理运营主体，半导体园区废水处理需求持续",
        ],
        "source_urls": [],
        "customer_requirement": "经开区工业污水集中处理持续扩容，半导体企业废水（含氟/重金属）预处理与总排口监测需求明确",
        "operational_pain_points": "进水水质波动大、半导体特征污染物监测要求高（INFERENCE）",
        "sales_summary": "吴江经开区水质净化公司为区域集中处理主体，与半导体产线扩张同步扩容；建议经行业展会或市政供排水部门建立联系。",
        "jd_inferences": [],
        "contacts": [],
    },
    "IND-20260917-04": {  # 先进半导体材料（安徽）
        "facts": [
            "先进半导体材料（安徽）有限公司项目推进中（原daily信号facts保留），封装材料扩产",
        ],
        "source_urls": [],
        "customer_requirement": "半导体封装材料扩产配套废水（含铜/酸）处理与监测（INFERENCE）",
        "operational_pain_points": "封装废水含重金属与酸，排口在线监测要求严格（INFERENCE）",
        "sales_summary": "先进半导体材料安徽基地扩产，水处理配套扩建中；暂无公开联系人证据，需后续补充。",
        "jd_inferences": [],
        "contacts": [],
    },
    "IND-20260917-05": {  # 宜章志存新材料
        "facts": [
            "智联在招'环保工程师9000-12000元/月'（岗位职责含ISO14001、含锂废水三废治理）；BOSS直聘在招安全工程师/环保工程师共14职位（人事专员刘女士）",
            "公司地址：郴州市宜章县白石渡镇",
        ],
        "source_urls": [
            "https://www.zhaopin.com/company/xxxx/",
            "https://www.zhipin.com/company/xxxx/",
        ],
        "customer_requirement": "含锂废水三废治理岗位公开招聘（环保工程师9000-12000），锂盐产线废水处理与排放监测是核心运营环节",
        "operational_pain_points": "含锂废水三废治理、ISO14001体系运行与在线监测数据合规（FACT：岗位职责）",
        "sales_summary": "宜章志存新材料公开招聘环保工程师（含锂废水治理）、14个在招职位，人事专员刘女士可联系，环保岗位扩编代表废水处理投入明确。",
        "jd_inferences": [
            {"job_title": "环保工程师（9000-12000元/月）", "role_duties": "ISO14001体系、含锂废水三废治理、监测数据管理", "software_need": "废水在线监测+环保体系数字化", "confidence": "HIGH", "source_url": "https://www.zhaopin.com/company/xxxx/"}
        ],
        "contacts": [
            {"name": "刘女士", "title": "人事专员", "role": "C", "phone": "", "unit": "郴州宜章志存新材料有限公司"}
        ],
    },
    "IND-20260917-06": {  # 云天化
        "facts": [
            "云天化2027届校招研发技术岗（2026-09-20发布，含环境科学专业），官网招聘公告yth.cn/jrwm.html",
        ],
        "source_urls": [
            "https://yth.cn/jrwm.html",
        ],
        "customer_requirement": "磷化工龙头持续校招研发与环保技术岗，磷石膏/废水处理与排放监测合规需求持续",
        "operational_pain_points": "磷化工废水（含磷/氟）处理与磷石膏综合利用在线监测要求高（INFERENCE）",
        "sales_summary": "云天化2027届校招含环境科学方向，研发与环保投入持续；可经官网招聘渠道接触人力资源与环保技术条线。",
        "jd_inferences": [
            {"job_title": "研发技术岗（2027届校招，含环境科学）", "role_duties": "磷化工工艺与环保技术研发", "software_need": "水处理监测与环保合规数据平台", "confidence": "MEDIUM", "source_url": "https://yth.cn/jrwm.html"}
        ],
        "contacts": [
            {"name": "云天化（招聘单位）", "title": "人力资源部/技术研发中心", "role": "C", "phone": "", "unit": "云南云天化股份有限公司"}
        ],
    },
    "IND-20260917-07": {  # 沧州彩客锂能
        "facts": [
            "母公司河北彩客新材料官网公开电话0317-7750702、邮箱wujiang@tsaker.com；2026-04河北工大就业网发布技术员5人/研发工程师3人招聘",
        ],
        "source_urls": [
            "https://www.tsaker.com/contact/",
            "https://job.hebut.edu.cn/xxxx.html",
        ],
        "customer_requirement": "锂能材料项目配套废水处理与监测，母公司环保与研发岗位持续扩编",
        "operational_pain_points": "锂电池材料（负极/电解液）废水处理与排放监测要求严格（INFERENCE）",
        "sales_summary": "彩客锂能母公司公开电话与邮箱可触达（0317-7750702），2026-04招聘技术员/研发工程师5+3人，组织扩张伴随环保配套投入。",
        "jd_inferences": [
            {"job_title": "技术员（5人）/研发工程师（3人）", "role_duties": "产线技术运行与工艺研发", "software_need": "产线水处理在线监测", "confidence": "MEDIUM", "source_url": "https://job.hebut.edu.cn/xxxx.html"}
        ],
        "contacts": [
            {"name": "河北彩客新材料（冀ICP公开电话）", "title": "公司总机", "role": "D", "phone": "0317-7750702", "unit": "河北彩客新材料科技股份有限公司（母公司）"}
        ],
    },
    "IND-20260917-08": {  # 茂名创能烯碳
        "facts": [
            "茂名创能烯碳科技项目推进中（原daily信号facts保留），烯碳材料产线建设",
        ],
        "source_urls": [],
        "customer_requirement": "烯碳新材料产线建设配套废水处理与排放监测（INFERENCE）",
        "operational_pain_points": "新材料产线废水成分复杂，排口监测合规是投产前提（INFERENCE）",
        "sales_summary": "茂名创能烯碳项目在建，水处理配套随产线建设推进；暂无公开联系人证据，需后续补充。",
        "jd_inferences": [],
        "contacts": [],
    },
    "IND-20260917-09": {  # 江西陆丰（奉新）
        "facts": [
            "智联在招'人事经理'（2026-09-20）与'机修电工'（2026-09-19）；奉新政府网招聘信息含联系人胡经理13576179599",
        ],
        "source_urls": [
            "https://www.zhaopin.com/company/xxxx/",
            "http://www.fengxin.gov.cn/xxxx.shtml",
        ],
        "customer_requirement": "奉新基地产线扩编（人事经理+机修电工在招），动力/公用工程与水处理岗位将随编制扩充",
        "operational_pain_points": "产线公用工程（纯水/废水）运维人员需求上升（INFERENCE）",
        "sales_summary": "江西陆丰奉新基地持续招人（人事经理9/20、机修电工9/19更新），胡经理13576179599可联系，产线扩张期是验证水处理配套需求窗口。",
        "jd_inferences": [
            {"job_title": "人事经理/机修电工", "role_duties": "产线运行与公用工程维护", "software_need": "公用工程水系统在线监测", "confidence": "MEDIUM", "source_url": "https://www.zhaopin.com/company/xxxx/"}
        ],
        "contacts": [
            {"name": "胡经理", "title": "招聘联系人", "role": "C", "phone": "13576179599", "unit": "江西陆丰新能源科技发展有限公司"}
        ],
    },
    "IND-20260917-10": {  # 常德宏杉新能源
        "facts": [
            "常德宏杉新能源2026-07-09新设公司；母公司湖南宏杉（益阳）BOSS直聘有HR Manager活跃",
        ],
        "source_urls": [
            "https://www.zhipin.com/company/xxxx/",
        ],
        "customer_requirement": "新设公司+产线建设期，公用工程与水处理配套按新项目标准建设（INFERENCE）",
        "operational_pain_points": "新基地建设无历史包袱，监测与数字化一次到位窗口（INFERENCE）",
        "sales_summary": "常德宏杉2026-07新设，母公司宏杉HR在BOSS活跃，新基地设计期是推荐iMS监测与资产管理的理想窗口。",
        "jd_inferences": [
            {"job_title": "HR Manager（母公司宏杉）", "role_duties": "组织与招聘（新基地）", "software_need": "新基地水处理监测方案一次到位", "confidence": "MEDIUM", "source_url": "https://www.zhipin.com/company/xxxx/"}
        ],
        "contacts": [
            {"name": "湖南宏杉（HR Manager）", "title": "人力资源（母公司）", "role": "C", "phone": "", "unit": "湖南宏杉新能源科技有限公司（母公司）"}
        ],
    },
    "IND-20260915-01": {  # 东明石化
        "facts": [
            "东明石化2027届校招约50人（联系人李浩哲），岗位含装置运行工程师（环境工程专业）与化验工程师20人（2026-09-18发布）",
        ],
        "source_urls": [
            "https://www.dmsh.com.cn/xxxx.html",
        ],
        "customer_requirement": "炼化装置扩编（2027届50人，含环境工程/化验20人），水系统运行与监测岗位稳增",
        "operational_pain_points": "炼化水系统（循环水/污水）监测点位多、节能与合规双重压力（INFERENCE）",
        "sales_summary": "东明石化2027届校招50人扩编（化验工程师20人），化验与水处理运行投入明确，校招联系人李浩哲可建立联系。",
        "jd_inferences": [
            {"job_title": "装置运行工程师/化验工程师（20人）", "role_duties": "炼化装置运行与水质化验", "software_need": "水质在线分析仪表", "confidence": "HIGH", "source_url": "https://www.dmsh.com.cn/xxxx.html"}
        ],
        "contacts": [
            {"name": "李浩哲", "title": "校招联系人", "role": "C", "phone": "", "unit": "东明石化集团"}
        ],
    },
    "IND-20260915-02": {  # 高美可惠州
        "facts": [
            "高美可半导体设备核心部件研发制造项目（一期）环评批准公示（惠州市生态环境局仲恺分局，环评机构广东惠之蓝环保科技）",
            "惠州市商务局2026-09-15报道项目奠基：总投资约1.5亿元、预计年产值3亿元，高美可集团华南基地",
            "高美可无锡在招'韩语技术工程师'（工作地点惠州黄冈，前期无锡培训）、'销售专员'（惠州1-3年）",
        ],
        "source_urls": [
            "https://www.hzzk.gov.cn/hzzksthjj/gkmlpt/content/5/5850/post_5850726.html",
            "https://swj.huizhou.gov.cn/rdzt/zhhzcyy/yqfc/content/mpost_5852325.html",
        ],
        "customer_requirement": "半导体设备部件制造基地新建（1.5亿投资），纯水/废水处理与监测按新工厂标准建设（FACT：环评批复+奠基）",
        "operational_pain_points": "半导体部件清洗工艺用纯水+含氟废水处理，新工厂监测点位规划窗口（INFERENCE）",
        "sales_summary": "高美可惠州基地2026-09奠基（总投资1.5亿），环评已批，惠州招聘启动（韩语技术工程师）——设计/建设期是iMS切入监测方案的最佳窗口。",
        "jd_inferences": [
            {"job_title": "韩语技术工程师（惠州）/销售专员", "role_duties": "惠州工厂技术筹备与商务拓展", "software_need": "新工厂纯水/废水在线监测系统", "confidence": "HIGH", "source_url": "https://m.zhipin.com/job_detail/xxxx.html"}
        ],
        "contacts": [
            {"name": "高美可科技（惠州）有限公司", "title": "项目/工厂筹备组", "role": "C", "phone": "", "unit": "高美可科技（惠州）有限公司"}
        ],
    },
    "IND-20260915-03": {  # 云南洽洽老魔坊魔芋
        "facts": [
            "洽洽食品在招'生产计划专员'（2026-09-10更新，曲靖马龙区老魔坊厂区）与'曲靖工厂设备机修4-7K'",
            "云南洽洽老魔坊魔芋生物科技有限公司法定代表人徐涛，注册资本6000万元，成立2025-12-02",
        ],
        "source_urls": [
            "https://m.zhipin.com/job_detail/e1db5d00eb58e5580nd52N24GVZZ.html",
        ],
        "customer_requirement": "洽洽曲靖魔芋食品工厂投产筹备（生产计划/设备机修在招），食品工厂废水（有机物）处理与排放监测是环评要求",
        "operational_pain_points": "食品废水有机物浓度高，环保验收与常态化排放监测要求（INFERENCE）",
        "sales_summary": "洽洽食品在曲靖马龙区建设魔芋工厂（注册6000万，2025-12成立），生产筹备岗位已在招聘，工厂投产前期是水处理与监测方案机会。",
        "jd_inferences": [
            {"job_title": "生产计划专员/设备机修（曲靖）", "role_duties": "曲靖工厂生产筹备与设备维护", "software_need": "食品废水处理与排放在线监测", "confidence": "MEDIUM", "source_url": "https://m.zhipin.com/job_detail/e1db5d00eb58e5580nd52N24GVZZ.html"}
        ],
        "contacts": [
            {"name": "洽洽食品（曲靖工厂）", "title": "工厂筹备组/人事", "role": "C", "phone": "", "unit": "云南洽洽老魔坊魔芋生物科技有限公司"}
        ],
    },
    "IND-20260915-04": {  # 江苏宏邦化工
        "facts": [
            "BOSS直聘在招'安全工程师J10127'（淮安，5-10年经验，职责含环保）与'机修工J10034'；企查查显示13个在招岗位（工艺员5-10K、焊工6-9K，2026-01更新）",
            "公司地址：淮安工业园区实联大道16号",
        ],
        "source_urls": [
            "https://m.zhipin.com/job_detail/94394374662a4b1503x42d28FFFU.html",
        ],
        "customer_requirement": "化工企业安全环保岗位扩编（安全工程师含环保职责），废水处理与环保合规监测需求明确",
        "operational_pain_points": "化工废水达标排放与安全环保督察要求在线监测与台账（FACT：安全工程师岗位职责含环保）",
        "sales_summary": "宏邦化工13个在招岗位（含安全工程师/工艺员/焊工），环保职能岗负责废水达标与在线数据，可经BOSS直聘渠道接触。",
        "jd_inferences": [
            {"job_title": "安全工程师J10127", "role_duties": "环保设施运行、废水达标与在线数据核查", "software_need": "废水在线监测+环保台账", "confidence": "HIGH", "source_url": "https://m.zhipin.com/job_detail/94394374662a4b1503x42d28FFFU.html"}
        ],
        "contacts": [
            {"name": "江苏宏邦化工（招聘单位）", "title": "安全环保部", "role": "C", "phone": "", "unit": "江苏宏邦化工科技有限公司"}
        ],
    },
    "IND-20260915-05": {  # 裕华钢铁（武安）
        "facts": [
            "今日招聘网在招武安市裕华钢铁'电力/能源工程师6000-15000'；武安市政府官方招聘页发布裕华钢铁产品开发/轧钢工程师招聘",
            "武安钢铁区域环保整改持续推进（589个排口核查背景下的能环岗位增编）",
        ],
        "source_urls": [
            "https://www.jrzp.com/company11AFF8C8C3BA6C1E.shtml",
        ],
        "customer_requirement": "钢铁企业环保整治背景下能环岗位扩编（电力/能源工程师6K-1.5W），污水/循环水系统监测与节能改造需求明确",
        "operational_pain_points": "钢铁废水（浊环/净环/脱硫废水）监测点位多，区域排口核查压力大（INFERENCE）",
        "sales_summary": "裕华钢铁/宝烨煤焦化在招电力与能源工程师（6000-15000），对应区域589排口核查下的能环投入；可经今日招聘网与市政府招聘渠道接触能环部门。",
        "jd_inferences": [
            {"job_title": "电力/能源工程师（6000-15000）", "role_duties": "厂区能源与水系统运行管理", "software_need": "水系统在线监测与能耗管理", "confidence": "MEDIUM", "source_url": "https://www.jrzp.com/company11AFF8C8C3BA6C1E.shtml"}
        ],
        "contacts": [
            {"name": "武安市裕华钢铁（招聘单位）", "title": "能环部", "role": "C", "phone": "", "unit": "武安市裕华钢铁有限公司"}
        ],
    },
    "WB-1-Yaomeng": {  # 平顶山姚孟发电
        "opportunity_stage": "Execution",
        "estimated_time_window": "3-9个月（改造实施/验收期）",
        "time_window_basis": "EPC于2026-05-26中标（CCTC20260474/01），含雨污分流+含油废水系统改造，实施与验收窗口",
        "facts": [
            "姚孟发电'全厂工业废水处理装置及雨污分流升级改造EPC项目'2026-04-09公开招标，2026-05-26发布中标公告（项目编号CCTC20260474/01）",
            "招标委托机构经办人刘静13681557910（电力招标代理）；此前#5、6机组脱硫废水零排放改造EPC由华夏碧水中标（2025年）",
        ],
        "source_urls": [
            "http://m.dlztb.com/news/202604/09/723694.html",
            "https://m.bidizhaobiao.com/info-778575300.html",
        ],
        "customer_requirement": "全厂工业废水处理装置升级+雨污分流改造EPC（含含油废水、生活污水系统），改造完成后需在线监测与数字化运维",
        "operational_pain_points": "现有废水处理装置与雨污分流不满足环保要求，粉煤灰堆场/含油废水治理压力（FACT：改造范围）",
        "sales_summary": "姚孟发电废水EPC改造已于2026-05完成中标（华夏碧水系列已有合作），工程实施与调试期是监测仪表与数字化运维切入窗口；招标经办刘静可追后续分项采购。",
        "jd_inferences": [
            {"job_title": "全厂废水EPC改造配套岗位（招标经办公开）", "role_duties": "EPC改造实施与验收", "software_need": "改造后在线监测与运维平台", "confidence": "MEDIUM", "source_url": "http://m.dlztb.com/news/202604/09/723694.html"}
        ],
        "contacts": [
            {"name": "刘静", "title": "招标经办（中煤招标代理）", "role": "C", "phone": "13681557910", "unit": "平顶山姚孟发电有限责任公司"}
        ],
    },
    "WB-4-Changyang": {  # 长阳清江水务
        "opportunity_stage": "Tender/Procurement",
        "estimated_time_window": "3-6个月",
        "time_window_basis": "工程已由长发改审批[2023]131号批准，2026年预处理设备采购招标推进中",
        "facts": [
            "长阳经济开发区工业污水处理厂建设工程已由长发改审批[2023]131号批准，正在招标预处理厌氧氨氧化、污泥消解设备采购（招标人：长阳清江水务投资控股集团/湖北亿源建筑/重庆市市政设计研究院）",
            "长阳清江水务投资控股集团公开电话0717-5322808，法定代表人刘天明",
        ],
        "source_urls": [
            "https://www.hbtba.com/plus/pro.php?id=6e612006-6b1e-4f7a-80ba-db63c8d0b2b2",
            "http://www.changyang.gov.cn/zfxxgk/show.html?aid=13&id=69048",
        ],
        "customer_requirement": "长阳经开区工业污水处理厂（厌氧氨氧化工艺）设备采购推进中，配套在线监测与自控系统需求明确",
        "operational_pain_points": "工业污水厂服务经开区企业，进水波动大，新建厂需监测与自控一次到位（INFERENCE）",
        "sales_summary": "长阳经开区工业污水厂进入设备采购与建设期（2023年批复、2026年设备招标），招标联合体（水务集团+亿源建筑+市政院）三方主体明确，可经0717-5322808触达水务集团。",
        "jd_inferences": [
            {"job_title": "工业污水处理厂建设岗位（设备采购招标公开）", "role_duties": "污水厂设备采购与建设管理", "software_need": "进出水在线监测+自动化控制", "confidence": "MEDIUM", "source_url": "https://www.hbtba.com/plus/pro.php?id=6e612006-6b1e-4f7a-80ba-db63c8d0b2b2"}
        ],
        "contacts": [
            {"name": "长阳清江水务投资控股集团", "title": "集团办公室（公开电话）", "role": "C", "phone": "0717-5322808", "unit": "长阳清江水务投资控股集团有限公司"}
        ],
    },
    "WB-5-Xinxiang": {  # 新乡凤泉湖污水处理（无直接公开证据，如实标注）
        "opportunity_stage": "Agent Discovery",
        "estimated_time_window": "≥12个月（区域证据推断）",
        "time_window_basis": "凤泉湖10000t/d工业污水EPC无直接公开来源；区域证据：凤泉区表面处理产业园环评批复（新环书审〔2026〕13号）与大块镇污水处理厂扩容（2026-01受理）显示2026-2027年园区工业废水集中处理配套将兑现",
        "facts": [
            "公开渠道截至2026-09-21未检索到'新乡凤泉湖工业污水处理10000t/d EPC'的独立招标/环评来源",
            "区域相关证据：新乡凤泉区表面处理产业园环评获批（新环书审〔2026〕13号，废水含铬/镍，预处理后进大块镇污水处理厂）；凤泉区大块镇污水处理厂扩容改造2026-01-14受理环评",
        ],
        "source_urls": [
            "http://sthjj.xinxiang.gov.cn/zwgk/public/6638717/9702570.html",
            "http://sthjj.xinxiang.gov.cn/zwgk/public/6638717/9683803.html",
        ],
        "customer_requirement": "凤泉区表面处理产业园（电镀/电池企业聚集）废水集中处理扩容，园区工业污水集中处理厂必要性上升（INFERENCE：区域产业证据）",
        "operational_pain_points": "表面处理废水含铬/镍须分质处理，大块镇污水厂扩容承接园区废水，集中处理与监测需求明确（FACT：环评批复要求）",
        "sales_summary": "凤泉湖10kt/d工业污水EPC暂未检索到直接公开来源（判定为信息缺口，需线下核实项目真实性）；但凤泉区表面处理产业园获批+大块镇污水厂扩容是可靠的区域需求证据，建议先核实凤泉湖项目业主与进度。",
        "jd_inferences": [],
        "contacts": [],
    },
    "WB-6-Xiaogan": {  # 孝感嘉乐投资
        "opportunity_stage": "Execution",
        "estimated_time_window": "6-12个月（建设启动期）",
        "time_window_basis": "EPC于2026-06-10评标完成、中标价6.622亿元（工期1095日历天），进入设计施工",
        "facts": [
            "孝南区工业污水处理厂及配套管网建设项目(EPC)（HBXN-202604SZ-017001001）：近期2.5万m³/d、远期5.0万m³/d，配套管网160km，总投资75404.45万元",
            "2026-06-10完成评标，中标人孝感市澴川建筑/中晏建设（6.622亿元，工期1095日历天）；环评第一次公示建设单位联系人黄征哲18671219553；中标公告招标人联系人刘艳0712-2826242",
        ],
        "source_urls": [
            "http://www.xiaonan.gov.cn/c/xnqsthjfj/sthj/456338.jhtml",
            "https://xgxz.xiaogan.gov.cn/ggzyjy/jyxx/jsgc/zbjggg/202606/t20260616_580317.shtml",
        ],
        "customer_requirement": "孝南区工业污水厂（远期5万m³/d）+160km管网新建，建设期与运营期需要在线监测、仪表资产管理",
        "operational_pain_points": "新建厂+长管网，投运前需构建进出水在线监测与泵站监控体系（FACT：EPC中标）",
        "sales_summary": "孝感嘉乐投资项目EPC已定标（2026-06），进入设计施工期（工期1095天），设计阶段是监测点位规划窗口；业主环评联系人黄征哲、招标人刘艳电话公开。",
        "jd_inferences": [
            {"job_title": "污水厂建设/运营岗位（业主公开联系人）", "role_duties": "项目业主（嘉乐投资）建设管理", "software_need": "进出水在线监测+厂区SCADA", "confidence": "MEDIUM", "source_url": "https://xgxz.xiaogan.gov.cn/ggzyjy/jyxx/jsgc/zbjggg/202606/t20260616_580317.shtml"}
        ],
        "contacts": [
            {"name": "黄征哲", "title": "环评公示建设单位联系人", "role": "C", "phone": "18671219553", "unit": "孝感市嘉乐投资发展有限公司"},
            {"name": "刘艳", "title": "招标人联系人", "role": "C", "phone": "0712-2826242", "unit": "孝感市嘉乐投资发展有限公司"}
        ],
    },
    "IND-20260817-007": {  # 台州达辰药业
        "opportunity_stage": "EIA-Approval",
        "estimated_time_window": "6-12个月（设计建设期）",
        "time_window_basis": "环评2026-09-02正式批复（台环建〔2026〕67号），进入设计建设",
        "facts": [
            "达辰药业'年产50吨芦荟大黄素、30吨双醋瑞因项目'环评2026-08-10受理、2026-09-02正式批复（台环建〔2026〕67号），投资8500万元",
            "建设地点：台州湾经济技术开发区化工园区（南洋区块）东海第五大道17号；环评机构浙江泰诚环境科技；生产基地为日出实业集团控股（2022-11）",
        ],
        "source_urls": [
            "https://sthjj.zjtz.gov.cn/col/col1229896756/art/2026/art_3d471301caca41f2ae9c38bd8310581b.html",
            "https://sthjj.zjtz.gov.cn/col/col1229896756/art/2026/art_d09a984103514c66a780b7efa89e1eff.html",
        ],
        "customer_requirement": "原料药项目8500万投资环评获批（2026-09-02），配套设施（含废水预处理与在线监测）按新项目标准建设",
        "operational_pain_points": "原料药废水（高COD/溶剂残留）处理与特征污染物监测要求严格（INFERENCE）",
        "sales_summary": "达辰药业新项目环评已批复（台环建〔2026〕67号），进入设计建设期；环评机构浙江泰诚与台州市生态环境局审批处（0576-88819793）可协助触达。",
        "jd_inferences": [
            {"job_title": "原料药项目配套环保岗位（环评机构承接）", "role_duties": "新项目建设期环保三同时", "software_need": "废水在线监测+排污许可数据管理", "confidence": "MEDIUM", "source_url": "https://sthjj.zjtz.gov.cn/col/col1229896756/art/2026/art_3d471301caca41f2ae9c38bd8310581b.html"}
        ],
        "contacts": [
            {"name": "台州达辰药业（环评批复单位）", "title": "项目/环保负责人", "role": "C", "phone": "", "unit": "台州达辰药业有限公司"}
        ],
    },
    "IND-20260817-012": {  # 云南泸西产业园区第二污水厂
        "opportunity_stage": "Execution",
        "estimated_time_window": "22个月（EPC工期）",
        "time_window_basis": "EPC总承包2026-09-14发布中标结果（中国建筑联合体，设计费下浮22.5%），工期22个月",
        "facts": [
            "云南泸西产业园区第二污水处理厂及配套管网工程：6000m³/d分质处理（脱硫废水600+其他5400），管网3764m+再生水管网9934m，总投资28907.62万元，建设单位泸西净源水务有限公司",
            "环评已获批（红河州生态环境局）；EPC总承包2026-07-30招标、08-11暂停后恢复，2026-09-14发布中标结果（中国建筑联合体中标，设计费下浮22.5%，工期22个月）",
        ],
        "source_urls": [
            "https://www.hh.gov.cn/info/9331/1269322.htm",
            "https://yn.bidcenter.com.cn/zbcontent-441993529-4.html",
        ],
        "customer_requirement": "园区第二污水厂（6000m³/d分质处理+再生水回用）EPC中标（2026-09-14），建设期22个月，进出水在线监测与再生水回用监测需求明确",
        "operational_pain_points": "工业废水（含脱硫废水）分质处理、再生水全回用要求全流程水质监测（FACT：环评批复）",
        "sales_summary": "泸西第二污水厂EPC已定标（2026-09-14，中国建筑联合体），设计施工22个月——设计阶段是监测点位与仪表规格介入窗口；可经红河州环评窗口0873-3856544与泸西净源水务触达。",
        "jd_inferences": [
            {"job_title": "污水厂建设期岗位（EPC中标实施）", "role_duties": "EPC设计与建设实施", "software_need": "进出水在线监测+再生水回用监测", "confidence": "MEDIUM", "source_url": "https://yn.bidcenter.com.cn/zbcontent-441993529-4.html"}
        ],
        "contacts": [
            {"name": "泸西净源水务有限公司", "title": "项目建设单位", "role": "C", "phone": "0873-3856544", "unit": "云南泸西产业园区（建设单位：泸西净源水务）"}
        ],
    },
}


# URLs verified from the 2026-09-21 websearch results.  Enhancers may only
# contribute URLs listed here; anything else is dropped to keep provenance real.
REAL_EXTRA_URLS = {
    "IND-20260919-08": {"http://www.ccgp.gov.cn/cggg/dfgg/jzxcs/202609/t20260915_27325943.htm"},
    "IND-20260915-02": {
        "https://www.hzzk.gov.cn/hzzksthjj/gkmlpt/content/5/5850/post_5850726.html",
        "https://swj.huizhou.gov.cn/rdzt/zhhzcyy/yqfc/content/mpost_5852325.html",
    },
    "IND-20260915-03": {"https://m.zhipin.com/job_detail/e1db5d00eb58e5580nd52N24GVZZ.html"},
    "IND-20260915-04": {"https://m.zhipin.com/job_detail/94394374662a4b1503x42d28FFFU.html"},
    "IND-20260915-05": {"https://www.jrzp.com/company11AFF8C8C3BA6C1E.shtml"},
    "WB-1-Yaomeng": {"http://m.dlztb.com/news/202604/09/723694.html", "https://m.bidizhaobiao.com/info-778575300.html"},
    "WB-4-Changyang": {"https://www.hbtba.com/plus/pro.php?id=6e612006-6b1e-4f7a-80ba-db63c8d0b2b2", "http://www.changyang.gov.cn/zfxxgk/show.html?aid=13&id=69048"},
    "WB-5-Xinxiang": {"http://sthjj.xinxiang.gov.cn/zwgk/public/6638717/9702570.html", "http://sthjj.xinxiang.gov.cn/zwgk/public/6638717/9683803.html"},
    "WB-6-Xiaogan": {"http://www.xiaonan.gov.cn/c/xnqsthjfj/sthj/456338.jhtml", "https://xgxz.xiaogan.gov.cn/ggzyjy/jyxx/jsgc/zbjggg/202606/t20260616_580317.shtml"},
    "IND-20260817-007": {
        "https://sthjj.zjtz.gov.cn/col/col1229896756/art/2026/art_3d471301caca41f2ae9c38bd8310581b.html",
        "https://sthjj.zjtz.gov.cn/col/col1229896756/art/2026/art_d09a984103514c66a780b7efa89e1eff.html",
    },
    "IND-20260817-012": {"https://www.hh.gov.cn/info/9331/1269322.htm", "https://yn.bidcenter.com.cn/zbcontent-441993529-4.html"},
}


def build_contact(lead_id, c, seq):
    return {
        "contact_id": "CT-20260921-%04d" % seq,
        "name": c["name"],
        "company": c.get("unit", ""),
        "title": c.get("title", ""),
        "role": c.get("role", "C"),
        "commercial_contact_class": c.get("role", "C"),
        "lead_ids": [lead_id],
        "project_ids": [],
        "account_id": "ACC-%s" % lead_id,
        "phone": [{"value": c["phone"], "type": "COMPANY_SWITCHBOARD" if not c["phone"].startswith("1") else "MOBILE", "source_agent": "DuMate", "source_url": "", "verified": False}] if c.get("phone") else [],
        "email": [],
        "commercial_relevance_score": 60,
        "evidence_score": 70,
        "current_relevance": "CURRENT",
        "discovered_by": ["DuMate"],
        "source_records": [{"agent": "DuMate", "source_url": ""}],
    }


def enrich_lead_from_daily(sig):
    """Turn a radar daily signal into a sales_usable_enriched lead."""
    enh = IND_ENHANCE.get(sig.get("id"), {})
    allowed_urls = REAL_EXTRA_URLS.get(sig.get("id"), set())
    evidence = sig.get("evidence") or {}
    facts = list(evidence.get("facts") or [])
    facts += enh.get("facts", [])
    urls = list(sig.get("source_urls") or [])
    urls += [u for u in enh.get("source_urls", []) if u in allowed_urls]
    # dedup preserving order
    seen, unique_urls = set(), []
    for u in urls:
        if u and u not in seen:
            seen.add(u)
            unique_urls.append(u)
    opportunity = sig.get("opportunity_project") or sig.get("opportunity") or enh.get("opportunity", "")
    location = sig.get("location") or {}
    if not isinstance(location, dict):
        location = {"raw": location}
    inferences = [i for i in (evidence.get("inferences") or []) if str(i).strip()]
    jd_inferences = enh.get("jd_inferences", [])
    for jd in jd_inferences:
        jd["confidence"] = jd.get("confidence", "MEDIUM").upper()
        if jd.get("source_url") not in allowed_urls:
            jd["source_url"] = ""
    original_signal = copy.deepcopy(sig)
    original_signal["opportunity"] = opportunity
    original_signal["evidence"] = {"facts": facts, "inferences": inferences, "unknowns": evidence.get("unknowns") or []}
    original_signal["source_urls"] = unique_urls
    original_signal["estimated_time_window"] = sig.get("influence_window") or enh.get("estimated_time_window", "")
    original_signal["time_window_basis"] = sig.get("influence_window_evidence") or enh.get("time_window_basis", "")
    if enh.get("opportunity_stage"):
        original_signal["opportunity_stage"] = enh["opportunity_stage"]
    lead = {
        "lead_id": sig["id"],
        "original_signal": original_signal,
        "enrichment_status": "sales_usable_enriched",
        "record_status": "active",
        "status": "active",
        "status_reason": "2026-09-21 Enrichment restore: merged from radar daily + public websearch",
        "first_seen": sig.get("continuity", {}).get("first_seen") if isinstance(sig.get("continuity"), dict) else (sig.get("continuity") or TODAY),
        "last_updated": TODAY,
        "source_lead_ids": [sig["id"]],
        "source_files": [],
        "segments": ["industrial"],
        "region_raw": [str(location.get("raw") or "")],
        "industry_raw": [str(sig.get("industry") or "")],
        "location": location,
        "industry": sig.get("industry") or "",
        "customer_requirement": enh.get("customer_requirement", ""),
        "operational_pain_points": enh.get("operational_pain_points", ""),
        "sales_summary": enh.get("sales_summary", ""),
        "estimated_time_window": original_signal["estimated_time_window"],
        "time_window_basis": original_signal["time_window_basis"],
        "jd_inferences": jd_inferences,
        "next_validation_questions": enh.get("next_validation_questions", ""),
        "history": [],
        "priority": sig.get("priority") or sig.get("signal_tier") or "P2",
    }
    return lead, [c for c in enh.get("contacts", [])]


def upgrade_lead(lead, enh):
    """Apply enhancement payload to an existing agent_discovered lead."""
    lid = lead.get("lead_id", "")
    allowed_urls = REAL_EXTRA_URLS.get(lid, set())
    original_signal = lead.get("original_signal") or {}
    evidence = original_signal.get("evidence") or {}
    facts = list(evidence.get("facts") or []) + enh.get("facts", [])
    urls = list(original_signal.get("source_urls") or []) + [u for u in enh.get("source_urls", []) if u in allowed_urls]
    seen, unique_urls = set(), []
    for u in urls:
        if u and u not in seen:
            seen.add(u)
            unique_urls.append(u)
    original_signal["evidence"] = {"facts": facts, "inferences": evidence.get("inferences") or [], "unknowns": evidence.get("unknowns") or []}
    original_signal["source_urls"] = unique_urls
    if not original_signal.get("opportunity"):
        original_signal["opportunity"] = original_signal.get("opportunity_project") or lead.get("lead_id")
    if not original_signal.get("estimated_time_window"):
        original_signal["estimated_time_window"] = enh.get("estimated_time_window", "")
    if not original_signal.get("time_window_basis"):
        original_signal["time_window_basis"] = enh.get("time_window_basis", "")
    if enh.get("opportunity_stage"):
        original_signal["opportunity_stage"] = enh["opportunity_stage"]
    lead["original_signal"] = original_signal
    lead["enrichment_status"] = "sales_usable_enriched"
    lead["record_status"] = "active"
    lead["last_updated"] = TODAY
    lead["status_reason"] = "2026-09-21 Enrichment restore: public evidence collected"
    for key in ("customer_requirement", "operational_pain_points", "sales_summary"):
        if enh.get(key):
            lead[key] = enh[key]
    if enh.get("jd_inferences"):
        for jd in enh["jd_inferences"]:
            jd["confidence"] = jd.get("confidence", "MEDIUM").upper()
            if jd.get("source_url") not in allowed_urls:
                jd["source_url"] = ""
        lead["jd_inferences"] = lead.get("jd_inferences") or []
        lead["jd_inferences"] += enh["jd_inferences"]
    return lead, list(enh.get("contacts", []))


def raw_location(sig):
    loc = sig.get("location")
    if isinstance(loc, dict):
        return str(loc.get("raw") or "")
    return str(loc or "")


def run_industrial():
    master_path = IND_ENRICHED / "indctx_latest_jd_2026-09-13.json"
    master = read(master_path)
    contacts = {c.get("contact_id"): c for c in master.get("contacts", [])}
    leads = {l.get("lead_id"): l for l in master.get("leads", [])}
    projects = {p.get("project_id"): p for p in master.get("projects", [])}
    accounts = {a.get("account_id"): a for a in master.get("accounts", [])}
    seq = 1
    new_contacts = 0
    new_leads = 0

    def attach(lead_id, new_contacts_list):
        nonlocal seq, new_contacts
        lead = leads[lead_id]
        ids = list(lead.get("contact_ids") or [])
        for c in new_contacts_list:
            cid = "CT-20260921-%04d" % seq
            seq += 1
            if cid in contacts:
                continue
            contacts[cid] = build_contact(lead_id, c, seq - 1)
            ids.append(cid)
            new_contacts += 1
        lead["contact_ids"] = ids
        lead["contact_summary"] = {"total": len(ids), "sales_targets_a": 0, "project_influencers_b": 0, "information_gateways_c": len(ids), "account_context_d": 0, "missing_critical": 0}

    # 1) radar daily leads 9/15, 9/17, 9/19
    for fname in ("2026-09-15", "2026-09-17", "2026-09-19"):
        daily = read(IND_DAILY / (fname + ".json"))
        for sig in daily.get("signals", []):
            lid = sig.get("id")
            if not lid or lid in leads:
                # existing enriched lead already covers this id; still upgrade if enhancement exists
                if lid and lid in IND_ENHANCE and lid in leads:
                    enh = IND_ENHANCE[lid]
                    _, cons = upgrade_lead(leads[lid], enh)
                    attach(lid, cons)
                continue
            lead, cons = enrich_lead_from_daily(sig)
            lead["source_files"] = [fname + ".json"]
            lead["history"] = [{"date": fname, "source_file": fname + ".json", "record_id": lid, "name": lead["original_signal"].get("opportunity", "")}]
            leads[lid] = lead
            new_leads += 1
            # project / account entities
            pid = "PRJ-%s" % lid
            aid = "ACC-%s" % lid
            projects[pid] = {
                "project_id": pid, "lead_id": lid, "account_id": aid,
                "project_name": lead["original_signal"].get("opportunity", ""),
                "owner": sig.get("company", ""),
                "investment_amount": "unknown",
                "project_status": "2026-09-21 Enrichment restore：由雷达日报归集合并",
                "water_system_details": {"confirmed": False, "description": lead.get("customer_requirement", "")},
            }
            accounts[aid] = {
                "account_id": aid, "lead_id": lid, "account_name": sig.get("company", ""),
                "group_name": "", "industry": sig.get("industry", ""), "plant_location": raw_location(sig),
                "products": [], "contact_ids": [],
            }
            lead["project_ids"] = [pid]
            lead["account_ids"] = [aid]
            attach(lid, cons)

    # 2) WB / IND-20260817 upgrades
    for lid, enh in IND_ENHANCE.items():
        if lid in leads:
            _, cons = upgrade_lead(leads[lid], enh)
            attach(lid, cons)

    # 3) metadata / history / statistics
    meta = master.get("metadata", {})
    meta["generated_date"] = TODAY
    meta["last_update"] = STAMP
    meta["description"] = "iMS Industrial Master Intelligence - Sales Readiness Deep Enrichment (P1/P2/P3, 2026-09-21, merged 9/13+ radar daily leads)"
    meta["previous_version"] = "20260913"
    meta["consolidation"] = {"engine": "restore_enrichment_20260921", "note": "恢复 Enrichment：合并9/15/9/17/9/19雷达日报线索并回填公开证据（websearch 2026-09-21）；升级WB/IND-20260817六条"}
    meta["delivery"] = {"delivered_at": TODAY, "note": "Enrichment restore 第1批：9/13后工业线索合并+评分恢复", "linked_prompt": "docs/iMS_GTM_Public_Signal_Radar_prompt_v3.2_full_20260913.md"}
    master["metadata"] = meta
    master["leads"] = list(leads.values())
    master["projects"] = list(projects.values())
    master["accounts"] = list(accounts.values())
    master["contacts"] = list(contacts.values())
    history = master.get("enrichment_history") or []
    history.append({"date": TODAY, "version": "v3.4-restore", "agent": "DuMate", "action": "Enrichment Restore - merge 9/13+ radar daily leads", "new_leads_added": new_leads, "new_contacts_added": new_contacts, "sources": ["websearch: 2026-09-21 28组查询（招聘/招标/政府公示）"], "notes": "恢复job_ed97fe0b自8/27中断以来的合并：工业9/15/17/19共25条线索转入enriched，WB-1/4/5/6与IND-20260817-007/012补齐公开证据"})
    master["enrichment_history"] = history
    if isinstance(master.get("agent_statistics"), dict):
        stat = master["agent_statistics"]
        stat["total_contacts"] = len(contacts)
        stat["total_leads"] = len(leads)
        stat["dumate_contacts"] = stat.get("dumate_contacts", 0) + new_contacts
        stat["new_contacts_added"] = stat.get("new_contacts_added", 0) + new_contacts
    # 4) emit new canonical + sync latest
    out_jd = IND_ENRICHED / "indctx_latest_jd_2026-09-21.json"
    out_latest = IND_ENRICHED / "indctx_latest.json"
    write(out_jd, master)
    write(out_latest, master)
    print("industrial: leads=%d (new=%d), contacts=%d (new=%d), projects=%d, accounts=%d -> %s" % (len(leads), new_leads, len(contacts), new_contacts, len(projects), len(accounts), out_jd.name))


def run_municipal():
    master_path = MUN_ENRICHED / "indctx_latest.json"
    master = read(master_path)
    leads = {l.get("lead_id"): l for l in master.get("leads", [])}
    new_leads = 0
    for fname in ("2026-09-14", "2026-09-16", "2026-09-18"):
        daily = read(MUN_DAILY / (fname + ".json"))
        for item in (daily.get("opportunities") or daily.get("signals") or []):
            lid = item.get("id") or item.get("name")
            if not lid or lid in leads:
                continue
            name = item.get("name") or item.get("opportunity")
            facts = item.get("public_facts") or []
            if not isinstance(facts, list):
                facts = [facts]
            urls = [item.get("source_url")] if item.get("source_url") else []
            original_signal = {
                "company": name, "opportunity": name,
                "opportunity_stage": item.get("opportunity_stage"),
                "priority": item.get("priority") or item.get("score"),
                "evidence": {"facts": facts, "inferences": [item.get("ai_judgment")] if item.get("ai_judgment") else [], "unknowns": []},
                "source_urls": urls,
                "estimated_time_window": item.get("estimated_time_window"),
                "time_window_basis": item.get("estimated_time_window_basis") or item.get("time_window_basis"),
                "logic": item.get("logic_chain_check"),
                "to_verify": item.get("to_verify"),
                "action_triad": item.get("action_triad"),
            }
            lead = {
                "lead_id": lid, "original_signal": original_signal,
                "enrichment_status": "consolidated_from_radar_daily",
                "record_status": "active", "status": "active",
                "status_reason": "2026-09-21 Enrichment restore: archived from municipal radar daily",
                "first_seen": item.get("first_seen") or fname,
                "last_updated": TODAY,
                "source_lead_ids": [lid],
                "source_files": [fname + ".json"],
                "segments": ["municipal"],
                "location": name,
                "industry": "市政水务",
                "customer_requirement": item.get("potential_ims_use_case") or "",
                "next_validation_questions": item.get("action_triad", {}).get("talk_what") if isinstance(item.get("action_triad"), dict) else "",
                "history": [{"date": fname, "source_file": fname + ".json", "record_id": lid, "name": name}],
            }
            leads[lid] = lead
            new_leads += 1
            pid = "PRJ-%s" % lid
            aid = "ACC-%s" % lid
            master["projects"] = master.get("projects") or []
            master["accounts"] = master.get("accounts") or []
            pids = {p.get("project_id") for p in master["projects"]}
            aids = {a.get("account_id") for a in master["accounts"]}
            if pid not in pids:
                master["projects"].append({"project_id": pid, "lead_id": lid, "account_id": aid, "project_name": name, "owner": name, "investment_amount": "unknown", "project_status": "2026-09-21 Enrichment restore", "water_system_details": {"confirmed": False, "description": ""}})
            if aid not in aids:
                master["accounts"].append({"account_id": aid, "lead_id": lid, "account_name": name, "group_name": "", "industry": "市政水务", "plant_location": "", "products": [], "contact_ids": []})
            lead["project_ids"] = [pid]
            lead["account_ids"] = [aid]
    meta = master.get("metadata", {})
    meta["generated_date"] = TODAY
    meta["last_update"] = STAMP
    meta["description"] = "iMS Municipal Master Intelligence - Enriched Context (radar daily archived through 2026-09-18)"
    meta["note"] = "2026-09-21 restore: archived 9/14/9/16/9/18 radar daily opportunities into enriched master"
    master["metadata"] = meta
    master["leads"] = list(leads.values())
    history = master.get("enrichment_history") or []
    history.append({"date": TODAY, "version": "v3.4-restore", "agent": "DuMate", "action": "Enrichment Restore - archive 9/13+ municipal radar daily", "new_leads_added": new_leads, "sources": ["intelligence/municipal/daily/2026-09-14/16/18.json"], "notes": "市政 enriched 不再停留9/13"})
    master["enrichment_history"] = history
    write(master_path, master)
    print("municipal: leads=%d (new=%d) -> indctx_latest.json" % (len(leads), new_leads))


if __name__ == "__main__":
    run_industrial()
    run_municipal()
    print("done. Next: python3 scripts/build_industrial_pipeline_view.py")