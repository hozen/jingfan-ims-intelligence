"""
环博会市场观察报告v12
- 聚焦环博会整体趋势：产品/技术/客户需求/政策
- 纯白底，HACH三色(蓝0,126,181 / 深灰77,77,77 / 浅灰153,153,153)
- 无logo无背景图形
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

BLUE = RGBColor(0, 126, 181)
DARK = RGBColor(77, 77, 77)
LIGHT = RGBColor(153, 153, 153)
WHITE = RGBColor(255, 255, 255)

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

# ============================================================
# SLIDE 1: Cover
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
t(slide, Inches(0.8), Inches(2.0), Inches(11.5), Inches(1.3),
  "2026环博会市场观察", size=44, bold=True, color=DARK)
t(slide, Inches(0.8), Inches(3.5), Inches(11), Inches(0.7),
  "产品 · 技术 · 客户需求 · 政策驱动", size=24, color=BLUE)
t(slide, Inches(0.8), Inches(4.4), Inches(11), Inches(0.5),
  "2026年4月  |  上海新国际博览中心", size=16, color=DARK)
t(slide, Inches(0.8), Inches(5.2), Inches(11), Inches(0.5),
  "数据来源：微信公众号公开OCR数据  |  样本：972家参展厂商", size=13, color=LIGHT)

# ============================================================
# SLIDE 2: 数据样本说明
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "01", "数据样本说明")

items = [
    ("数据来源", "微信公众号文章OCR提取，共识别972家参展厂商"),
    ("展馆覆盖", "E1~E7 / N1~N5 / W1~W5 共16个馆"),
    ("最大展馆", "E6馆（大气治理/余热）187家、E5馆（大气治理）174家"),
    ("监测重点馆", "E4馆（过程控制与仪器仪表）182家、E3馆（监测与检测）15家*"),
    ("数字化展商", "含云/平台/系统/数据/智能关键词：39家（全馆分散）"),
]
for i, (label, text) in enumerate(items):
    y = Inches(1.25) + Inches(i * 0.88)
    bar(slide, Inches(0.5), y + Pt(5), Pt(8), Pt(8), BLUE)
    t(slide, Inches(0.72), y, Inches(2.0), Inches(0.5), label, size=15, bold=True, color=DARK)
    t(slide, Inches(2.75), y, Inches(10.3), Inches(0.8), text, size=15, color=DARK)

t(slide, Inches(0.5), Inches(6.3), Inches(12.5), Inches(0.5),
  "* E3馆数据因公众号图片CDN加密仅获取15家，实际展商数量更多",
  size=11, color=LIGHT)

# ============================================================
# SLIDE 3: 展商类型分布
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "02", "展商类型分布")

cats = [
    ("大气治理设备", "~360家", "E5/E6馆为主，废气处理、除尘、脱硫脱硝",
     "兰山环保、杜尔涂装等"),
    ("仪表/传感器/仪器", "86家", "E4馆为主，过程控制与在线监测",
     "上泰仪器、天信仪表、威格中国、余姚市仪表四厂等"),
    ("水处理/泵阀/膜材料", "69家", "E1/E5馆为主，市政与工业水处理",
     "世浦泰膜、中国水务投资、澳欣膜科技等"),
    ("数字化跨界公司", "39家", "全馆分散，具备云平台+数据能力",
     "江苏纽带智能、杭州易环智能、尚云互联、盘古自动化等"),
    ("环保工程/水务投资", "~30家", "E1/E2馆为主，BOT/PPP模式",
     "中国水务投资、北控水务等"),
]
for i, (cat, count, desc, examples) in enumerate(cats):
    y = Inches(1.05) + Inches(i * 1.05)
    bar(slide, Inches(0.5), y, Inches(0.06), Inches(0.85), BLUE)
    t(slide, Inches(0.7), y, Inches(3.0), Inches(0.45), cat, size=14, bold=True, color=DARK)
    t(slide, Inches(3.8), y, Inches(1.2), Inches(0.45), count, size=14, bold=True, color=BLUE)
    t(slide, Inches(5.1), y, Inches(4.5), Inches(0.45), desc, size=13, color=DARK)
    t(slide, Inches(0.7), y + Inches(0.42), Inches(12.3), Inches(0.35),
      "代表：" + examples, size=11, color=LIGHT)

t(slide, Inches(0.5), Inches(6.3), Inches(12.5), Inches(0.5),
  "洞察：大气治理展商数量最多（占比最高），仪器仪表次之，数字化跨界虽少但威胁最大",
  size=12, bold=True, color=DARK)

# ============================================================
# SLIDE 4: 产品趋势
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "03", "产品趋势")

trends = [
    ("在线监测设备爆发",
     "E4馆182家展商中大量展示在线水质/气体监测分析仪，替代传统实验室检测",
     "反映市场需求从抽样检测向24/7实时监测转变"),
    ("大气治理设备大型化",
     "E5/E6馆361家展商，废气处理、除尘、脱硫脱硝设备展出规模大",
     "说明存量市场依然巨大，改造升级需求持续"),
    ("膜材料与分离技术",
     "E1馆多家膜科技公司（澳欣膜、赫尔膜、世浦泰等），膜技术应用从市政向工业延伸",
     "工业零排放、盐碱资源化等新场景拉动膜市场"),
    ("智能泵站与计量设备",
     "水处理板块大量泵阀、流量计、液位计展商，智能化、节能型产品为主",
     "水务公司降本增效需求推动泵站数字化改造"),
    ("传感器小型化与低功耗",
     "多款在线水质传感器、光谱分析仪亮相，体积小、安装方便、支持IoT",
     "分布式监测、河道监测等新场景驱动传感器创新"),
]
for i, (title, desc, implication) in enumerate(trends):
    y = Inches(1.05) + Inches(i * 1.08)
    bar(slide, Inches(0.5), y, Inches(0.06), Inches(0.85), BLUE)
    t(slide, Inches(0.7), y, Inches(4.5), Inches(0.45), title, size=14, bold=True, color=DARK)
    t(slide, Inches(0.7), y + Inches(0.42), Inches(7.0), Inches(0.5), desc, size=12, color=DARK)
    t(slide, Inches(7.8), y + Inches(0.42), Inches(5.2), Inches(0.5),
      "→ " + implication, size=11, color=LIGHT)

# ============================================================
# SLIDE 5: 技术趋势
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "04", "技术趋势")

tech = [
    ("云平台与SaaS化",
     "39家数字化展商大量展示云平台、数据中台、SaaS服务",
     "监测数据上云、平台化运营成为主流，私有部署向订阅制转型"),
    ("IoT与边缘计算",
     "分布式传感器+DTU/网关+云端架构在多个展商方案中出现",
     "低功耗、自适应采集、边缘预处理的IoT监测节点成标配"),
    ("AI与大数据分析",
     "展商展示预测性维护、异常预警、排放趋势预测等AI能力",
     "从数据采集向数据挖掘、辅助决策演进，AI+监测加速融合"),
    ("数字孪生与可视化",
     "多个展台展示三维水厂、数字管网、智慧水务大屏",
     "数字孪生从概念走向落地，成为运营管理标配工具"),
    ("5G+工业互联网",
     "5G网关、5G+监测方案在展会上亮相，解决传统有线方案痛点",
     "5G低延时特性支撑实时控制与高清视频监控融合"),
]
for i, (title, desc, implication) in enumerate(tech):
    y = Inches(1.05) + Inches(i * 1.08)
    bar(slide, Inches(0.5), y, Inches(0.06), Inches(0.85), BLUE)
    t(slide, Inches(0.7), y, Inches(4.0), Inches(0.45), title, size=14, bold=True, color=DARK)
    t(slide, Inches(0.7), y + Inches(0.42), Inches(7.0), Inches(0.5), desc, size=12, color=DARK)
    t(slide, Inches(7.8), y + Inches(0.42), Inches(5.2), Inches(0.5),
      "→ " + implication, size=11, color=LIGHT)

# ============================================================
# SLIDE 6: 客户需求趋势
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "05", "客户需求趋势")

needs = [
    ("从单点监测到全链路管控",
     "客户不再满足于单台仪器，要求数据联网、平台整合、跨系统打通",
     "水务集团、管网公司推动厂网河湖一体化监测需求"),
    ("从买设备到买服务",
     "设备采购向运维服务、数据服务、Saas订阅模式转变",
     "展商普遍推出年度服务合同、远程运维、数据分析增值服务"),
    ("国产替代加速",
     "E4馆大量国内仪表厂商（同在E4-D08/E08区域的哈希也面临竞争）",
     "价格敏感客户、西部/农村市场优先选用国产性价比方案"),
    ("数据合规与安全",
     "工业互联网安全、等保2.0要求推动监测数据安全需求",
     "客户开始关注数据主权、传输安全、备份恢复等合规要求"),
    ("双碳目标驱动碳监测",
     "碳排放监测、碳足迹、碳核查相关展商增加",
     "钢铁、化工、水泥等高耗能行业碳监测需求浮现"),
]
for i, (title, desc, implication) in enumerate(needs):
    y = Inches(1.05) + Inches(i * 1.08)
    bar(slide, Inches(0.5), y, Inches(0.06), Inches(0.85), BLUE)
    t(slide, Inches(0.7), y, Inches(4.5), Inches(0.45), title, size=14, bold=True, color=DARK)
    t(slide, Inches(0.7), y + Inches(0.42), Inches(7.0), Inches(0.5), desc, size=12, color=DARK)
    t(slide, Inches(7.8), y + Inches(0.42), Inches(5.2), Inches(0.5),
      "→ " + implication, size=11, color=LIGHT)

# ============================================================
# SLIDE 7: 政策驱动
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "06", "政策驱动：十五五规划重点方向")

policies = [
    ("水环境精细化管理",
     "十四五水污染防治向十五五过渡，黑臭水体治理、农村污水治理持续",
     "流域监测、断面监测、饮用水源监测需求持续增长"),
    ("大气多污染物协同控制",
     "臭氧与PM2.5协同管控，VOCS监测、无组织排放监管加强",
     "大气监测从点源向面源、从浓度向成因精细化管控发展"),
    ("双碳目标与碳市场扩容",
     "全国碳市场覆盖行业扩大，碳监测/碳核查需求从电力向其他行业延伸",
     "碳排放在线监测、碳足迹管理、碳资产开发成为新增长点"),
    ("美丽中国建设",
     "美丽中国先行区、示范县建设推动全域环境基础设施建设",
     "县、镇一级监测能力建设带来增量市场，特别是水质监测"),
    ("数字环保与智慧监管",
     "环保监管数字化转型，污染源自动监控一张网建设",
     "数据联网、智慧决策、精准溯源成为监管标配要求"),
]
for i, (title, desc, implication) in enumerate(policies):
    y = Inches(1.05) + Inches(i * 1.08)
    bar(slide, Inches(0.5), y, Inches(0.06), Inches(0.85), BLUE)
    t(slide, Inches(0.7), y, Inches(4.5), Inches(0.45), title, size=14, bold=True, color=DARK)
    t(slide, Inches(0.7), y + Inches(0.42), Inches(7.0), Inches(0.5), desc, size=12, color=DARK)
    t(slide, Inches(7.8), y + Inches(0.42), Inches(5.2), Inches(0.5),
      "→ " + implication, size=11, color=LIGHT)

# ============================================================
# SLIDE 8: 数字化跨界公司动向
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "07", "数字化跨界公司动向（39家）")

digital = [
    ("江苏纽带智能", "E3-G61", "端到端智能监测方案，整合传感器+云平台"),
    ("杭州易环智能", "E1-L12", "智慧环保平台，数据采集+可视化+运维"),
    ("北京尚云互联", "E2-W13", "环境监测云平台，物联网数据接入+分析"),
    ("E20环境平台", "E1-071", "环境产业互联网平台，连接设备与用户"),
    ("杭州盘古自动化", "E4-F71", "自动化控制系统，PLC/DCS+云端接入"),
    ("山东混沌智能", "E4-F28", "智能传感器+云平台一体化方案"),
    ("缘循智能科技", "E4-L50", "流体控制智能化，传感器+数据服务"),
    ("广州云景信息", "E4-C21", "智慧水务平台，水处理数据中台"),
    ("重庆知行数联", "E2-A43", "智慧城市数据服务，环境数据整合"),
]

# Left: table header
y = Inches(1.1)
bar(slide, Inches(0.5), y, Inches(12.3), Inches(0.4), BLUE)
t(slide, Inches(0.6), y, Inches(3.0), Inches(0.4), "公司名称", size=12, bold=True, color=WHITE)
t(slide, Inches(3.7), y, Inches(1.2), Inches(0.4), "展位", size=12, bold=True, color=WHITE)
t(slide, Inches(5.0), y, Inches(7.8), Inches(0.4), "核心业务", size=12, bold=True, color=WHITE)

for i, (name, booth, biz) in enumerate(digital):
    y = Inches(1.6) + Inches(i * 0.5)
    bg_c = RGBColor(240, 240, 240) if i % 2 == 0 else WHITE
    bar(slide, Inches(0.5), y, Inches(12.3), Inches(0.45), bg_c)
    t(slide, Inches(0.6), y, Inches(3.0), Inches(0.42), name, size=12, bold=True, color=DARK)
    t(slide, Inches(3.7), y, Inches(1.2), Inches(0.42), booth, size=12, color=BLUE)
    t(slide, Inches(5.0), y, Inches(7.8), Inches(0.42), biz, size=11, color=DARK)

t(slide, Inches(0.5), Inches(6.3), Inches(12.5), Inches(0.5),
  "洞察：这些公司以软件+数据+云平台为核心能力，跨界切入监测硬件市场，是展会中最值得关注的新兴力量",
  size=12, bold=True, color=DARK)

# ============================================================
# SLIDE 9: 总结与启示
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
t(slide, Inches(0.5), Inches(0.35), Inches(10), Inches(0.7),
  "总结与启示", size=36, bold=True, color=DARK)

conclusions = [
    ("产品趋势", "在线监测替代实验室、传感器小型化、膜材料应用扩展",
     "监测设备向实时化、智能化、集成化发展"),
    ("技术趋势", "云平台SaaS化、IoT+边缘计算、AI大数据分析、数字孪生",
     "技术架构从单机设备向平台化、数字化转型"),
    ("客户需求", "买服务不买设备、全链路管控、国产替代、碳监测",
     "客户需求从产品向服务、从单点向平台迁移"),
    ("政策驱动", "十五五美丽中国、双碳目标、数字化监管",
     "政策持续推动环境监测市场扩容与升级"),
    ("最值得关注的群体", "39家数字化跨界公司——软件+数据+云平台能力",
     "这类公司可能重塑监测行业竞争格局"),
]
for i, (label, items_text, implication) in enumerate(conclusions):
    y = Inches(1.2) + Inches(i * 1.05)
    bar(slide, Inches(0.5), y, Inches(1.5), Inches(0.42), BLUE)
    t(slide, Inches(0.5), y, Inches(1.5), Inches(0.42),
      label, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    t(slide, Inches(2.2), y, Inches(5.5), Inches(0.5), items_text, size=13, bold=True, color=DARK)
    t(slide, Inches(2.2), y + Inches(0.42), Inches(10.7), Inches(0.42),
      "→ " + implication, size=11, color=LIGHT)

t(slide, Inches(0.5), Inches(6.3), Inches(12), Inches(0.4),
  "2026环博会市场观察  |  数据来源：微信公众号公开OCR数据",
  size=11, color=LIGHT)

prs.save('/home/agentuser/环博会市场观察_v12.pptx')
print("v12 saved!")
