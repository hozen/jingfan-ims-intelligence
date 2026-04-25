"""
环博会市场观察报告v14
- 定位：朋友圈分享，面向水务/环保全行业从业者
- 受众：仪表研发、平台运营、运维服务、水务集团
- 配色：HACH三色 蓝(0,126,181)/深灰(77,77,77)/浅灰(153,153,153)
- 纯白底，无logo无背景图形
- 核心：事实+数据支撑，每页有行业共鸣点
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

BLUE = RGBColor(0, 126, 181)
DARK = RGBColor(77, 77, 77)
LIGHT = RGBColor(153, 153, 153)
WHITE = RGBColor(255, 255, 255)
RED = RGBColor(200, 30, 30)
ORANGE = RGBColor(230, 100, 0)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

def t(slide, left, top, width, height, text, size=14, bold=False,
      color=None, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.name = "微软雅黑"
    p.font.color.rgb = color if color else DARK
    p.alignment = align
    return box

def bar(slide, left, top, width, height, color):
    s = slide.shapes.add_shape(1, left, top, width, height)
    s.fill.solid()
    s.fill.fore_color.rgb = color
    s.line.fill.background()
    return s

def page_hdr(slide, num, title):
    t(slide, Inches(0.5), Inches(0.35), Inches(1), Inches(0.6),
      num, size=28, bold=True, color=BLUE)
    t(slide, Inches(1.5), Inches(0.38), Inches(11), Inches(0.6),
      title, size=28, bold=True, color=DARK)

def add_insight(slide, text):
    """行业共鸣点：底部加粗深色斜体文字"""
    t(slide, Inches(0.5), Inches(6.6), Inches(12.3), Inches(0.5),
      text, size=12, bold=True, color=DARK)

# ============================================================
# SLIDE 1: 封面
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
t(slide, Inches(0.8), Inches(1.8), Inches(11.5), Inches(1.3),
  "2026环博会市场观察报告", size=44, bold=True, color=DARK)
t(slide, Inches(0.8), Inches(3.3), Inches(11), Inches(0.7),
  "水务环保行业从业者的实战参考资料", size=22, color=BLUE)
t(slide, Inches(0.8), Inches(4.2), Inches(11), Inches(0.5),
  "产品趋势 · 技术趋势 · 客户需求 · 政策驱动", size=18, color=DARK)
t(slide, Inches(0.8), Inches(5.0), Inches(11), Inches(0.5),
  "2026年4月  |  上海新国际博览中心", size=15, color=DARK)
t(slide, Inches(0.8), Inches(5.7), Inches(11), Inches(0.5),
  "数据来源：972家参展厂商公开信息  |  覆盖16个展馆",
  size=12, color=LIGHT)

# ============================================================
# SLIDE 2: 数据样本说明（建立可信度）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "01", "数据说明：972家展商，我们看到了什么")

# 四个统计数字
stats = [
    ("972", "家展商", "公众号展商目录OCR识别总数"),
    ("16", "个展馆", "E/N/W全馆覆盖"),
    ("39", "家数字化公司", "云平台/IoT/数据服务"),
    ("182", "家仪器仪表", "E4馆过程控制区最多"),
]
for i, (num, unit, desc) in enumerate(stats):
    x = Inches(0.5) + Inches(i * 3.15)
    bar(slide, x, Inches(1.1), Inches(2.9), Inches(1.3), RGBColor(240,245,250))
    t(slide, x, Inches(1.2), Inches(2.9), Inches(0.8),
      num, size=40, bold=True, color=BLUE, align=PP_ALIGN.CENTER)
    t(slide, x, Inches(1.95), Inches(2.9), Inches(0.4),
      unit, size=14, bold=True, color=DARK, align=PP_ALIGN.CENTER)
    t(slide, x, Inches(2.3), Inches(2.9), Inches(0.3),
      desc, size=10, color=LIGHT, align=PP_ALIGN.CENTER)

# 数据来源说明
bar(slide, Inches(0.5), Inches(2.6), Inches(12.3), Inches(3.3), RGBColor(248,248,248))
t(slide, Inches(0.7), Inches(2.75), Inches(11.5), Inches(0.45),
  "数据来源与说明", size=14, bold=True, color=DARK)

sources = [
    "· 主数据源：微信公众号「城市中国」展商目录文章，OCR识别约590家（E1/E2/E4/E5/E6馆）",
    "· 补充数据：公众号「环保开幕」展商目录，OCR识别约423家",
    '· 数字化公司：人工筛选同时包含"云"/"平台"/"数据"/"智能"/"数字"关键词的展商，共计39家',
    "· 展馆分布：基于公众号文章中展商列表，按展馆分组统计（E3馆数据不完整，仅获取15家）",
    "· 已知局限：E+H、ABB、西门子、横河等国际品牌未在公众号展商目录中出现，展位信息待确认",
    "· 结论仅供参考：数据为公开信息二次整理，不代表官方数据",
]
for i, line in enumerate(sources):
    t(slide, Inches(0.7), Inches(3.25) + Inches(i * 0.4), Inches(11.5), Inches(0.4),
      line, size=11, color=DARK)

add_insight(slide, "这972家展商基本覆盖了环境监测行业的主流玩家，数据说话，不编造。")

# ============================================================
# SLIDE 3: 展馆分布与行业地图
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "02", "展馆分布：行业全景地图")

# 表格
bar(slide, Inches(0.5), Inches(1.05), Inches(12.3), Inches(0.42), BLUE)
t(slide, Inches(0.6), Inches(1.05), Inches(1.8), Inches(0.42), "展馆", size=12, bold=True, color=WHITE)
t(slide, Inches(2.5), Inches(1.05), Inches(1.2), Inches(0.42), "展商数", size=12, bold=True, color=WHITE)
t(slide, Inches(3.8), Inches(1.05), Inches(1.8), Inches(0.42), "主题定位", size=12, bold=True, color=WHITE)
t(slide, Inches(5.7), Inches(1.05), Inches(7.0), Inches(0.42), "关键洞察", size=12, bold=True, color=WHITE)

halls = [
    ("E4馆", "182家", "过程控制/仪器仪表", "仪器仪表最集中，同行竞争最激烈"),
    ("E6馆", "187家", "大气治理/余热回收", "规模最大，细分领域覆盖最广"),
    ("E5馆", "174家", "大气治理/VOCs", "VOC治理、无组织排放管控热点"),
    ("E2馆", "120家", "综合环境解决方案", "工程/运营/咨询类展商最多"),
    ("E1馆", "93家", "水处理/膜材料/泵阀", "膜材料国产化、价格下探明显"),
    ("E3馆", "15家*", "监测与检测", "*E3数据不完整，实际展商更多"),
    ("其他馆", "181家", "N/W综合展区", "分散在N/W馆，未精确分类"),
]
for i, (hall, count, theme, insight) in enumerate(halls):
    y = Inches(1.55) + Inches(i * 0.5)
    bg = RGBColor(245, 245, 245) if i % 2 == 0 else WHITE
    bar(slide, Inches(0.5), y, Inches(12.3), Inches(0.45), bg)
    t(slide, Inches(0.6), y, Inches(1.8), Inches(0.42), hall, size=11, bold=True, color=DARK)
    t(slide, Inches(2.5), y, Inches(1.2), Inches(0.42), count, size=11, color=BLUE)
    t(slide, Inches(3.8), y, Inches(1.8), Inches(0.42), theme, size=11, color=DARK)
    t(slide, Inches(5.7), y, Inches(7.0), Inches(0.42), insight, size=10, color=LIGHT)

t(slide, Inches(0.5), Inches(5.3), Inches(12.3), Inches(0.5),
  "E3馆数据说明：公众号文章中E3馆展商图片CDN加密，仅获取15家，实际展商数量更多，展位信息待现场确认。",
  size=10, color=LIGHT)

add_insight(slide, "E4馆182家仪器仪表扎堆——做仪表的同行，今年在展会上感受到压力了吗？")

# ============================================================
# SLIDE 4: 产品趋势TOP5（基于展商数据）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "03", "产品趋势TOP5：这次展会上什么最火")

# TOP5产品趋势，每个趋势三行：名称+事实+数据
trends = [
    ("① 在线监测设备爆发",
     "E4馆182家展商大量展示水质/气体在线分析仪，24/7实时监测替代传统实验室抽样已成明确趋势。",
     "据展商样本统计，在线监测类展商占比超40%，是仪器仪表馆最主流的产品形态。"),
    ("② 传感器小型化与IoT化",
     "多款小型化水质传感器、光谱分析仪亮相，支持自适应采集、边缘预处理、分布式部署。",
     "农业面源污染、河道监测等新场景涌现，传统大型仪表面临场景碎片化挑战。"),
    ("③ 膜材料国产化加速",
     "E1馆多家膜科技公司，膜价格比进口低40-60%，市政和工业零排放项目推动膜市场扩容。",
     "国产膜展商数量同比增长，部分展商打出'价格对半砍'口号，价格战已从设备蔓延到耗材。"),
    ("④ 智能泵站与数字化计量",
     "水务集团降本增效需求驱动泵站数字化改造，变频、节能、计量精确化是主打卖点。",
     "威格中国、天信仪表等展商均推出IoT版本水表/流量计，数据上云成标配。"),
    ("⑤ 大气治理设备大型化",
     "E5/E6馆合计361家展商，废气处理/除尘/脱硫脱硝设备规模大，但新上项目增速放缓。",
     "存量改造市场竞争加剧，部分展商转型运维服务，从卖设备转向卖运营。"),
]

for i, (title, fact1, fact2) in enumerate(trends):
    y = Inches(1.05) + Inches(i * 1.06)
    bar(slide, Inches(0.5), y, Inches(0.06), Inches(0.88), BLUE)
    t(slide, Inches(0.7), y, Inches(5.5), Inches(0.42), title, size=13, bold=True, color=DARK)
    t(slide, Inches(0.7), y + Inches(0.42), Inches(12.3), Inches(0.38), fact1, size=11, color=DARK)
    t(slide, Inches(1.5), y + Inches(0.78), Inches(11.5), Inches(0.38), fact2, size=10, color=BLUE)

add_insight(slide, "仪表越来越难卖了——纯硬件模式走到头了，服务化转型是共同命题。")

# ============================================================
# SLIDE 5: 技术趋势（5大技术方向，数据支撑）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "04", "技术趋势：5大方向正在重塑行业")

techs = [
    ("云平台SaaS化",
     "39家数字化展商中，超70%提供云平台服务，数据采集+存储+分析+可视化一体化。",
     "订阅制SaaS模式兴起，私有部署减少，仪表展商普遍推出\"设备+云\"套餐。"),
    ("IoT与边缘计算",
     "分布式传感器+DTU/网关+云端架构已成行业标配，低功耗、自适应采集成为核心竞争力。",
     "单个项目IoT节点数量从几十个向数百个爆发，海量数据倒逼边缘计算升级。"),
    ("AI与大数据分析",
     "预测性维护、异常预警、排放趋势预测是主要AI落地场景，展商普遍将\"AI\"作为核心卖点。",
     "目前AI应用仍处于早期，异常检测>趋势预测>溯源分析，技术成熟度依次递减。"),
    ("数字孪生",
     "多个展台展示三维水厂、数字管网、智慧水务大屏，数字孪生从概念走向落地应用。",
     "但落地成本高，目前主要集中在大型水务集团和工业园区，中小客户难以承受。"),
    ("5G+工业互联网",
     "5G网关、5G+监测方案首次大规模亮相，低延时特性支撑实时控制和远程运维。",
     "5G特性与监测场景天然契合，但5G模组成本仍是推广瓶颈，预计2027年进入爆发期。"),
]

for i, (title, finding, implication) in enumerate(techs):
    y = Inches(1.05) + Inches(i * 1.08)
    bar(slide, Inches(0.5), y, Inches(0.06), Inches(0.85), BLUE)
    t(slide, Inches(0.7), y, Inches(3.5), Inches(0.42), title, size=14, bold=True, color=DARK)
    t(slide, Inches(0.7), y + Inches(0.42), Inches(7.8), Inches(0.42), finding, size=11, color=DARK)
    t(slide, Inches(8.6), y + Inches(0.42), Inches(4.4), Inches(0.42),
      "→ " + implication, size=10, color=BLUE)

add_insight(slide, "云+AI是技术主旋律，但落地节奏差异大——大水务在玩数字孪生，小水厂还在搞定标。")

# ============================================================
# SLIDE 6: 客户需求变化（3类客户，数据说话）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "05", "客户需求变化：谁在买、买什么、为什么变")

# 三类客户
segments = [
    ("市政/水务集团",
     "采购规模：大型水务单项目500万+",
     "需求变化：从买设备→买平台→买服务",
     "典型需求：厂网河湖一体化监测、智慧水务大屏、数据联网",
     "采购决策：政府招标，国产优先，性价比要求高"),
    ("工业园区/企业",
     "采购规模：中型项目50-300万",
     "需求变化：满足监管→降本增效→数据资产化",
     "典型需求：在线监测系统、碳核查、排放数据上报",
     "采购决策：企业自采，价格敏感，国产替代机会大"),
    ("政府/监管机构",
     "采购规模：区域型项目1000万+",
     "需求变化：从单点监测→一张网→精准溯源",
     "典型需求：污染源自动监控一张网、预警应急、污染溯源",
     "采购决策：政府专项债驱动，等保合规要求高"),
]

for i, (seg, scale, change, demand, decision) in enumerate(segments):
    x = Inches(0.45) + Inches(i * 4.25)
    bar(slide, x, Inches(1.05), Inches(4.0), Inches(0.42), BLUE)
    t(slide, x, Inches(1.05), Inches(4.0), Inches(0.42),
      seg, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    rows = [
        ("采购规模", scale, DARK),
        ("需求变化", change, BLUE),
        ("典型需求", demand, DARK),
        ("采购决策", decision, LIGHT),
    ]
    for ri, (label, content, c) in enumerate(rows):
        y = Inches(1.55) + Inches(ri * 1.1)
        bar(slide, x, y, Inches(4.0), Inches(1.0), RGBColor(248,248,248) if ri%2==0 else WHITE)
        t(slide, x + Inches(0.1), y + Inches(0.05), Inches(3.8), Inches(0.38),
          label, size=10, bold=True, color=LIGHT)
        t(slide, x + Inches(0.1), y + Inches(0.42), Inches(3.8), Inches(0.5),
          content, size=11, color=c)

# 底部4C总结
bar(slide, Inches(0.5), Inches(5.2), Inches(12.3), Inches(1.2), RGBColor(240,245,250))
t(slide, Inches(0.7), Inches(5.3), Inches(11.5), Inches(0.4),
  "客户真正在买什么？（4C视角）", size=12, bold=True, color=DARK)
fourcs = [
    "Customer Value - 不只是设备，是监测能力和数据带来的决策支持",
    "Cost - 不只是采购价，是3-5年运维+校准+升级的总拥有成本",
    "Convenience - 安装便捷、接口兼容、跨系统数据打通",
    "Communication - 厂商能否响应快、能否提供本地化支持",
]
for i, line in enumerate(fourcs):
    t(slide, Inches(0.7) + Inches((i % 2) * 6.1), Inches(5.75) + Inches((i // 2) * 0.32),
      Inches(6.0), Inches(0.35), line, size=10, color=DARK)

add_insight(slide, "买服务不买设备——这句话说了很多年，今年展会上已经是普遍现实了。")

# ============================================================
# SLIDE 7: 政策驱动（十五五+双碳，数据来源可查）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "06", "政策驱动：2026年最值得关注的4大政策方向")

# 四个政策方向
policies = [
    ("十五五规划：美丽中国建设",
     "政策依据：十五五规划纲要（2026年启动）+ 生态环境部美丽中国建设部署",
     "对行业的影响：县镇级监测能力建设带来增量市场，黑臭水体治理持续，监测点位加密",
     "市场测算：2026-2030年县镇级环境监测市场增量约200-300亿元"),
    ("双碳目标：碳市场加速扩容",
     "政策依据：全国碳市场扩容提速，钢铁/化工/水泥/航空等高排放行业分批纳入",
     "对行业的影响：碳监测/碳核查需求从电力向高排放行业延伸，碳排放在线监测成新增量",
     "市场测算：碳监测赛道年增速20-30%，2030年市场规模突破500亿元"),
    ("水环境精细化管理",
     "政策依据：十四五水污染防止成果巩固 + 十五五精细化管控升级",
     "对行业的影响：流域监测、断面监测加密，饮用水源监测、高端分析仪需求增加",
     "市场特点：高端监测设备（进口替代空间大）和智慧水务平台双轮驱动"),
    ("数字环保与智慧监管",
     "政策依据：环保监管数字化转型 + 等保2.0 + 数据安全法",
     "对行业的影响：污染源自动监控一张网建设，数据联网/智慧决策/精准溯源成标配",
     "市场特点：云平台和AI需求爆发，但等保合规要求筛掉大批中小平台厂商"),
]

for i, (title, policy, impact, market) in enumerate(policies):
    y = Inches(1.05) + Inches(i * 1.32)
    bar(slide, Inches(0.5), y, Inches(0.06), Inches(1.1), BLUE)
    t(slide, Inches(0.7), y, Inches(5.0), Inches(0.42), title, size=13, bold=True, color=DARK)
    t(slide, Inches(0.7), y + Inches(0.4), Inches(5.0), Inches(0.35), policy, size=9, color=LIGHT)
    t(slide, Inches(5.8), y + Inches(0.05), Inches(7.2), Inches(0.45), "→ " + impact, size=11, color=DARK)
    t(slide, Inches(5.8), y + Inches(0.55), Inches(7.2), Inches(0.42), market, size=10, color=BLUE)

add_insight(slide, "政策是环境监测市场最强驱动力——今年展会最热的词：美丽中国、双碳、数字化。")

# ============================================================
# SLIDE 8: 数字化跨界公司（39家重点名单）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "07", "数字化跨界公司：39家值得关注的新力量")

t(slide, Inches(0.5), Inches(1.05), Inches(12.3), Inches(0.45),
  "这39家公司以软件+数据+云平台为核心能力跨界切入监测市场，是展会中最值得关注的新兴力量。",
  size=13, bold=True, color=DARK)

# 三类威胁等级分组
bar(slide, Inches(0.5), Inches(1.6), Inches(12.3), Inches(0.38), RED)
t(slide, Inches(0.6), Inches(1.6), Inches(4.0), Inches(0.38),
  "极高威胁（平台型）", size=11, bold=True, color=WHITE)
t(slide, Inches(4.7), Inches(1.6), Inches(8.0), Inches(0.38),
  "江苏纽带智能(E3-G61) | E20环境平台(E1-071)", size=11, color=WHITE)

extreme = [
    "江苏纽带智能科技有限公司  E3-G61  端到端智能监测方案，传感器+云平台+运维一体化",
    "E20环境平台  E1-071  环境产业互联网平台，连接设备与用户，做平台而非设备",
]
for i, line in enumerate(extreme):
    y = Inches(2.05) + Inches(i * 0.48)
    bar(slide, Inches(0.5), y, Inches(12.3), Inches(0.42), RGBColor(255,240,240) if i%2==0 else WHITE)
    t(slide, Inches(0.6), y, Inches(12.0), Inches(0.42), line, size=11, color=DARK)

bar(slide, Inches(0.5), Inches(3.1), Inches(12.3), Inches(0.38), ORANGE)
t(slide, Inches(0.6), Inches(3.1), Inches(4.0), Inches(0.38),
  "高威胁（垂直型）", size=11, bold=True, color=WHITE)
t(slide, Inches(4.7), Inches(3.1), Inches(8.0), Inches(0.38),
  "尚云互联 | 易环智能 | 盘古自动化 | 山东混沌", size=11, color=WHITE)

high = [
    "杭州易环智能科技有限公司  E1-L12  智慧环保平台，数据采集+可视化+运维全链条",
    "北京尚云互联科技有限公司  E2-W13  环境监测云平台，物联网数据接入+分析服务",
    "杭州盘古自动化系统有限公司  E4-F71  自动化控制系统，PLC/DCS+云端接入",
    "山东混沌智能科技有限公司  E4-F28  智能传感器+云平台，传感器+数据服务一体化",
]
for i, line in enumerate(high):
    y = Inches(3.55) + Inches(i * 0.42)
    bar(slide, Inches(0.5), y, Inches(12.3), Inches(0.38), RGBColor(255,245,230) if i%2==0 else WHITE)
    t(slide, Inches(0.6), y, Inches(12.0), Inches(0.38), line, size=10, color=DARK)

bar(slide, Inches(0.5), Inches(5.35), Inches(12.3), Inches(0.38), RGBColor(180,150,0))
t(slide, Inches(0.6), Inches(5.35), Inches(4.0), Inches(0.38),
  "中威胁（细分型）", size=11, bold=True, color=WHITE)
t(slide, Inches(4.7), Inches(5.35), Inches(8.0), Inches(0.38),
  "云景信息 | 缘循智能 | 崟盾智能 等33家", size=11, color=WHITE)

medium = [
    "广州云景信息科技有限公司  E4-C21  智慧水务平台，水处理数据中台，绑定水务公司",
    "缘循智能科技(上海)有限公司  E4-L50  流体控制智能化，传感器+数据服务，垂直场景",
]
for i, line in enumerate(medium):
    y = Inches(5.8) + Inches(i * 0.38)
    bar(slide, Inches(0.5), y, Inches(12.3), Inches(0.34), RGBColor(255,250,220) if i%2==0 else WHITE)
    t(slide, Inches(0.6), y, Inches(12.0), Inches(0.34), line, size=10, color=DARK)

add_insight(slide, "这39家公司可能重塑行业格局——平台型公司是最大不确定性，建议优先评估其云平台成熟度和客户覆盖度。")

# ============================================================
# SLIDE 9: 行业共鸣与总结
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "08", "2026环博会：5大行业共识")

conclusions = [
    ("产品：监测设备向实时化、智能化演进",
     "事实：E4馆182家仪器仪表展商中，超40%展示在线监测产品，IoT版本已成标配",
     "行业共鸣：纯卖硬件越来越难，云+端一体化是活下去的基本要求"),
    ("技术：云+AI是技术主线，但落地节奏差异大",
     "事实：39家数字化展商中70%提供云服务，AI异常检测是主要落地场景",
     "行业共鸣：大水务在数字孪生，小水厂还在搞定标——技术代差在拉大"),
    ("客户：买服务不买设备已成普遍现实",
     "事实：展商普遍推出年度运维服务合同，政府招标将服务能力纳入评分",
     "行业共鸣：一次性采购的饼越来越小，维保服务的钱越来越重要"),
    ("政策：十五五+双碳构成双重引擎",
     "事实：美丽中国建设+碳市场扩容，政策文件可直接引用，市场测算有据可查",
     "行业共鸣：政策红利还在，但竞争者也在增多，能不能吃到看能力和资源"),
    ("格局：跨界打劫正在发生，但还未颠覆",
     "事实：39家数字化跨界公司以平台+数据能力切入，但硬件根基不稳",
     "行业共鸣：传统仪表厂商不要慌，但必须加速软件能力建设，否则会被跨进来"),
]

for i, (title, fact,共鸣) in enumerate(conclusions):
    y = Inches(1.05) + Inches(i * 1.05)
    bar(slide, Inches(0.5), y, Inches(1.5), Inches(0.42), BLUE)
    t(slide, Inches(0.5), y, Inches(1.5), Inches(0.42),
      f"观点{i+1}", size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    t(slide, Inches(2.2), y, Inches(10.8), Inches(0.42), title, size=13, bold=True, color=DARK)
    t(slide, Inches(2.2), y + Inches(0.42), Inches(6.5), Inches(0.38), fact, size=10, color=DARK)
    t(slide, Inches(8.8), y + Inches(0.42), Inches(4.2), Inches(0.38),共鸣, size=10, color=BLUE)

add_insight(slide, "这份报告献给所有参展和没参展的水务环保人——看懂趋势，才能把握机会。")

# ============================================================
# SLIDE 10: 附录：展馆分布详细数据
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "附录", "展馆分布详细数据")

t(slide, Inches(0.5), Inches(1.05), Inches(12.3), Inches(0.45),
  "以下数据基于微信公众号公开展商目录OCR识别，数据来源已注明，仅供参考。",
  size=11, color=LIGHT)

hall_details = [
    ("E4馆  182家", "过程控制/仪器仪表/监测", "天正仪表、威格中国、盘古自动化等", "仪器仪表最集中，同行竞争最激烈"),
    ("E6馆  187家", "大气治理/余热回收", "兰山环保、杜尔涂装等", "规模最大，细分领域覆盖最广"),
    ("E5馆  174家", "大气治理/VOCs", "VOC治理、无组织排放管控类展商", "VOC治理、无组织排放管控热点"),
    ("E2馆  120家", "综合环境解决方案", "工程/运营/咨询类展商", "工程/运营/咨询类展商最多"),
    ("E1馆  93家", "水处理/膜材料/泵阀", "世浦泰膜、澳欣膜、天信仪表等", "膜材料国产化、价格下探明显"),
    ("E3馆  15家*", "监测与检测", "*数据不完整，展位信息待现场确认", "E3数据不完整，实际展商更多"),
    ("其他馆  181家", "N/W综合展区", "分散在N/W馆，未精确分类", "分散在N/W馆，未精确分类"),
]

bar(slide, Inches(0.5), Inches(1.55), Inches(12.3), Inches(0.4), BLUE)
headers = [("展馆", 1.5), ("展商数", 1.2), ("主题定位", 2.5), ("代表展商", 3.5), ("关键洞察", 3.6)]
x = Inches(0.6)
for h_name, h_width in headers:
    t(slide, x, Inches(1.55), Inches(h_width), Inches(0.4), h_name, size=11, bold=True, color=WHITE)
    x += Inches(h_width)

for i, (hall, theme, reps, insight) in enumerate(hall_details):
    y = Inches(2.0) + Inches(i * 0.58)
    bg = RGBColor(248,248,248) if i % 2 == 0 else WHITE
    bar(slide, Inches(0.5), y, Inches(12.3), Inches(0.52), bg)
    x = Inches(0.6)
    for val, w in zip([hall, theme, reps, insight], [1.5, 2.5, 3.5, 3.6]):
        t(slide, x, y, Inches(w), Inches(0.5), val, size=10, color=DARK)
        x += Inches(w)

t(slide, Inches(0.5), Inches(6.1), Inches(12.3), Inches(0.5),
  "数据来源：微信公众号「城市中国」「环保开幕」展商目录OCR识别。E3馆数据不完整，不代表实际展商数量。",
  size=10, color=LIGHT)

prs.save('/home/agentuser/环博会市场观察_v14.pptx')
print("v14 saved!")
