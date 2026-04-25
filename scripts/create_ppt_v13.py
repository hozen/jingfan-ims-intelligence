"""
环博会市场观察报告v13
- B2B工业市场研究框架：3C/PESTEL/4P/STP/价值链
- 纯白底，HACH三色：蓝(0,126,181) / 深灰(77,77,77) / 浅灰(153,153,153)
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

def section_tag(slide, x, y, text, color=BLUE, width=Inches(1.5)):
    bar(slide, x, y, width, Inches(0.42), color)
    t(slide, x, y, width, Inches(0.42),
      text, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# ============================================================
# SLIDE 1: Cover
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
t(slide, Inches(0.8), Inches(1.8), Inches(11.5), Inches(1.3),
  "2026环博会市场观察报告", size=44, bold=True, color=DARK)
t(slide, Inches(0.8), Inches(3.3), Inches(11), Inches(0.7),
  "基于B2B工业市场研究框架的深度分析", size=22, color=BLUE)
t(slide, Inches(0.8), Inches(4.2), Inches(11), Inches(0.5),
  "产品趋势 · 技术趋势 · 客户需求 · 政策驱动", size=18, color=DARK)
t(slide, Inches(0.8), Inches(5.0), Inches(11), Inches(0.5),
  "2026年4月  |  上海新国际博览中心", size=15, color=DARK)
t(slide, Inches(0.8), Inches(5.7), Inches(11), Inches(0.5),
  "数据来源：微信公众号公开OCR数据  |  样本：972家参展厂商  |  覆盖16个展馆",
  size=12, color=LIGHT)

# ============================================================
# SLIDE 2: 报告框架
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "00", "分析框架：B2B工业市场研究方法论")

# 3C
bar(slide, Inches(0.5), Inches(1.1), Inches(3.8), Inches(2.2), RGBColor(240,245,250))
bar(slide, Inches(0.5), Inches(1.1), Inches(3.8), Inches(0.45), BLUE)
t(slide, Inches(0.5), Inches(1.1), Inches(3.8), Inches(0.45),
  "3C分析框架", size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
cc_items = [
    "Company（公司）：我们有什么产品/技术能力",
    "Customer（客户）：客户需求在哪里、怎么变",
    "Competitor（竞争）：竞争格局如何、威胁在哪里",
]
for i, item in enumerate(cc_items):
    t(slide, Inches(0.65), Inches(1.65) + Inches(i * 0.5), Inches(3.5), Inches(0.5),
      "· " + item, size=12, color=DARK)

# PESTEL
bar(slide, Inches(4.6), Inches(1.1), Inches(3.8), Inches(2.2), RGBColor(240,245,250))
bar(slide, Inches(4.6), Inches(1.1), Inches(3.8), Inches(0.45), BLUE)
t(slide, Inches(4.6), Inches(1.1), Inches(3.8), Inches(0.45),
  "PESTEL政策框架", size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
pestel = ["P=政治/政策：十五五规划、双碳目标",
          "E=经济：投资驱动、运营降本需求",
          "S=社会：公众环保意识提升",
          "T=技术：IoT/AI/云/数字孪生",
          "E=环境：污染物协同管控要求",
          "L=法律：等保2.0、数据合规"]
for i, item in enumerate(pestel):
    t(slide, Inches(4.75), Inches(1.6) + Inches(i * 0.27), Inches(3.5), Inches(0.4),
      item, size=10, color=DARK)

# STP
bar(slide, Inches(8.7), Inches(1.1), Inches(4.0), Inches(2.2), RGBColor(240,245,250))
bar(slide, Inches(8.7), Inches(1.1), Inches(4.0), Inches(0.45), BLUE)
t(slide, Inches(8.7), Inches(1.1), Inches(4.0), Inches(0.45),
  "STP市场细分", size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
stp = ["S细分：市政/工业/农村",
       "T目标：政府监管/企业自测",
       "P定位：水务集团/工业园区"]
for i, item in enumerate(stp):
    t(slide, Inches(8.85), Inches(1.65) + Inches(i * 0.5), Inches(3.7), Inches(0.5),
      "· " + item, size=12, color=DARK)

# Bottom: 4P
bar(slide, Inches(0.5), Inches(3.5), Inches(12.3), Inches(2.7), RGBColor(240,245,250))
bar(slide, Inches(0.5), Inches(3.5), Inches(12.3), Inches(0.45), BLUE)
t(slide, Inches(0.5), Inches(3.5), Inches(12.3), Inches(0.45),
  "4P营销组合 + 价值链分析（本报告结构）", size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

fourps = [
    ("Product（产品）", "展商类型分布、产品趋势", "P1/P2页"),
    ("Price（价格）", "国产替代、价格战、订阅制", "客户需求页"),
    ("Place（渠道）", "展馆分布、区域市场覆盖", "样本说明页"),
    ("Promotion（推广）", "数字化跨界公司动向", "P7页"),
]
for i, (name, desc, page) in enumerate(fourps):
    x = Inches(0.65) + Inches(i * 3.1)
    t(slide, x, Inches(4.05), Inches(2.8), Inches(0.4),
      name, size=12, bold=True, color=BLUE)
    t(slide, x, Inches(4.45), Inches(2.8), Inches(0.6),
      desc, size=11, color=DARK)
    t(slide, x, Inches(5.0), Inches(2.8), Inches(0.4),
      "→ 见" + page, size=10, color=LIGHT)

t(slide, Inches(0.5), Inches(6.3), Inches(12.5), Inches(0.5),
  "本报告将PESTEL、3C、STP框架融入每一页的趋势分析，而非机械套用，确保分析有深度而非堆砌框架",
  size=11, bold=True, color=DARK)

# ============================================================
# SLIDE 3: 数据样本与展馆分布
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "01", "数据样本：972家参展商 · 16个展馆")

# Stats row
stats = [
    ("972", "家展商", "OCR识别总数"),
    ("16", "个展馆", "E/N/W全馆覆盖"),
    ("39", "家数字化公司", "云/平台/数据/智能"),
    ("182", "家仪器仪表", "E4馆过程控制"),
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

# Hall table
bar(slide, Inches(0.5), Inches(2.6), Inches(12.3), Inches(0.42), BLUE)
t(slide, Inches(0.6), Inches(2.6), Inches(2.0), Inches(0.42), "展馆", size=12, bold=True, color=WHITE)
t(slide, Inches(2.7), Inches(2.6), Inches(1.2), Inches(0.42), "展商数", size=12, bold=True, color=WHITE)
t(slide, Inches(4.0), Inches(2.6), Inches(1.5), Inches(0.42), "主题定位", size=12, bold=True, color=WHITE)
t(slide, Inches(5.6), Inches(2.6), Inches(7.0), Inches(0.42), "代表展商/关键特征", size=12, bold=True, color=WHITE)

halls = [
    ("E4馆", "182家", "过程控制/仪器仪表/监测", "仪器仪表最集中，同行竞争最激烈"),
    ("E6馆", "187家", "大气治理/余热回收", "规模最大，细分领域最广"),
    ("E5馆", "174家", "大气治理/VOCs", "VOC治理、无组织排放管控"),
    ("E2馆", "120家", "综合环境解决方案", "工程/运营/咨询类展商最多"),
    ("E1馆", "93家", "综合环境解决方案", "水处理、膜材料、泵阀"),
    ("E3馆", "15家*", "监测与检测", "*数据不完整，展位E3-C12"),
    ("其他馆", "181家", "N/W综合展区", "分散在N/W馆，未精确分类"),
]
for i, (hall, count, theme, note) in enumerate(halls):
    y = Inches(3.1) + Inches(i * 0.45)
    bg = RGBColor(245, 245, 245) if i % 2 == 0 else WHITE
    bar(slide, Inches(0.5), y, Inches(12.3), Inches(0.42), bg)
    t(slide, Inches(0.6), y, Inches(2.0), Inches(0.42), hall + " " + count, size=11, bold=True, color=DARK)
    t(slide, Inches(2.7), y, Inches(1.2), Inches(0.42), count, size=11, color=BLUE)
    t(slide, Inches(4.0), y, Inches(1.5), Inches(0.42), theme, size=11, color=DARK)
    t(slide, Inches(5.6), y, Inches(7.0), Inches(0.42), note, size=10, color=LIGHT)

t(slide, Inches(0.5), Inches(6.35), Inches(12.5), Inches(0.5),
  "* E3馆数据因公众号图片CDN加密仅获取15家，实际展商数量更多。E+H、ABB、西门子、横河等未在OCR数据中检索到",
  size=10, color=LIGHT)

# ============================================================
# SLIDE 4: 展商类型深度分析（3C视角）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "02", "展商类型深度分析（3C框架：产品-客户-竞争）")

# Three columns: 产品 / 客户 / 竞争
cols = [
    ("产品趋势（Company）", BLUE, [
        ("仪表/传感器", "86家", "小型化、智能化、IoT化", "天信仪表、威格中国"),
        ("数字化跨界", "39家", "云+端一体化、软件定义硬件", "江苏纽带智能、盘古自动化"),
        ("水处理/膜", "69家", "膜材料国产化、价格下探", "世浦泰膜、澳欣膜"),
        ("大气治理", "~360家", "设备大型化、节能化", "兰山环保、杜尔涂装"),
    ]),
    ("客户需求（Customer）", RGBColor(0, 100, 60), [
        ("买服务不买设备", "趋势明显", "从一次性采购到年度服务合同", ""),
        ("全链路管控", "需求升级", "从单点监测到厂网河湖一体化", ""),
        ("国产替代", "价格敏感", "西部/农村市场优先选国产", ""),
        ("碳监测", "新增长点", "高耗能行业碳核查需求浮现", ""),
    ]),
    ("竞争格局（Competitor）", RGBColor(180, 60, 0), [
        ("E4馆直接竞争", "182家", "国内品牌价格低30-50%", ""),
        ("跨界打劫", "39家", "软件+云平台切入监测市场", ""),
        ("国际品牌", "若干", "E+H/ABB/西门子等（展位未确认）", ""),
        ("工程商整合", "约30家", "解决方案打包蚕食硬件份额", ""),
    ]),
]

for ci, (col_title, col_color, items) in enumerate(cols):
    x = Inches(0.45) + Inches(ci * 4.3)
    bar(slide, x, Inches(1.05), Inches(4.0), Inches(0.45), col_color)
    t(slide, x, Inches(1.05), Inches(4.0), Inches(0.45),
      col_title, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    for ri, (item1, item2, item3, item4) in enumerate(items):
        y = Inches(1.6) + Inches(ri * 1.3)
        bar(slide, x, y, Inches(4.0), Inches(1.2), RGBColor(248,248,248) if ri%2==0 else WHITE)
        t(slide, x + Inches(0.1), y + Inches(0.05), Inches(3.8), Inches(0.4),
          item1, size=12, bold=True, color=DARK)
        t(slide, x + Inches(0.1), y + Inches(0.42), Inches(1.5), Inches(0.35),
          item2, size=11, bold=True, color=col_color)
        t(slide, x + Inches(1.6), y + Inches(0.42), Inches(2.3), Inches(0.35),
          item3, size=11, color=DARK)
        t(slide, x + Inches(0.1), y + Inches(0.78), Inches(3.8), Inches(0.35),
          item4, size=10, color=LIGHT)

# ============================================================
# SLIDE 5: 产品趋势
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "03", "产品趋势：监测设备从单机向平台化演进")

products = [
    ("在线监测设备爆发", True,
     "E4馆182家展商大量展示在线水质/气体监测分析仪，",
     "24/7实时监测替代传统实验室抽样检测已成明确趋势。",
     "客户需求：数据联网、自动报警、远程校准"),
    ("传感器小型化与低功耗", True,
     "多款小型化水质传感器、光谱分析仪亮相，",
     "支持IoT、自适应采集、边缘预处理，",
     "分布式监测、河道监测、农业面源污染监测等新场景涌现"),
    ("膜材料与分离技术", False,
     "E1馆多家膜科技公司，膜技术从市政向工业延伸，",
     "工业零排放、盐碱资源化、废水资源化推动膜市场扩容，",
     "国产膜价格比进口低40-60%，加速替代"),
    ("智能泵站与计量设备", False,
     "水处理板块大量泵阀、流量计、液位计展商，",
     "智能化（变频、节能）、计量精确化是主打卖点，",
     "水务公司降本增效需求驱动泵站数字化改造"),
    ("大气治理设备大型化", False,
     "E5/E6馆361家展商，废气处理/除尘/脱硫脱硝设备规模大，",
     "存量改造市场依然巨大，",
     "但增量放缓，新上项目减少，存量竞争加剧"),
]
for i, (title, is_hot, line1, line2, line3) in enumerate(products):
    y = Inches(1.05) + Inches(i * 1.12)
    color = BLUE if is_hot else RGBColor(180, 180, 180)
    bar(slide, Inches(0.5), y, Inches(0.06), Inches(0.9), color)
    t(slide, Inches(0.7), y, Inches(5.0), Inches(0.45), title, size=14, bold=True, color=DARK)
    t(slide, Inches(0.7), y + Inches(0.42), Inches(12.3), Inches(0.4), line1, size=12, color=DARK)
    t(slide, Inches(1.5), y + Inches(0.78), Inches(11.5), Inches(0.4), line2, size=11, color=BLUE)
    t(slide, Inches(1.5), y + Inches(1.0), Inches(11.5), Inches(0.35), line3, size=11, color=LIGHT)

t(slide, Inches(0.5), Inches(6.4), Inches(12.5), Inches(0.5),
   "洞察：监测产品正从单机设备向联网平台演进，纯硬件公司面临整合压力",
   size=12, bold=True, color=DARK)

# ============================================================
# SLIDE 6: 技术趋势（PESTEL-T维度）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "04", "技术趋势（PESTEL-T技术维度）")

tech = [
    ("云平台SaaS化", "39家数字化展商中大部分提供云平台服务，数据采集+存储+分析+可视化一体化",
     "监测设备从卖硬件向卖服务转变，订阅制SaaS模式兴起，私有部署减少"),
    ("IoT与边缘计算", "分布式传感器+DTU/网关+云端架构已成标配，低功耗、自适应采集成为核心竞争力",
     "IoT监测节点数量爆发，海量数据接入倒逼边缘计算能力升级"),
    ("AI与大数据分析", "展商展示预测性维护、异常预警、排放趋势预测等AI能力，从数据采集向数据挖掘演进",
     "AI+监测加速融合，异常检测、趋势预测、溯源分析是当前主要AI应用场景"),
    ("数字孪生", "多个展台展示三维水厂、数字管网、智慧水务大屏，数字孪生从概念走向落地",
     "数字孪生成为运营管理标配工具，支撑仿真优化与决策支持"),
    ("5G+工业互联网", "5G网关、5G+监测方案亮相，解决传统有线方案痛点，低延时支撑实时控制",
     "5G特性与监测场景天然契合，融合方案将持续增加"),
]
for i, (title, finding, implication) in enumerate(tech):
    y = Inches(1.05) + Inches(i * 1.1)
    bar(slide, Inches(0.5), y, Inches(0.06), Inches(0.85), BLUE)
    t(slide, Inches(0.7), y, Inches(3.5), Inches(0.42), title, size=14, bold=True, color=DARK)
    t(slide, Inches(0.7), y + Inches(0.42), Inches(8.0), Inches(0.42), finding, size=12, color=DARK)
    t(slide, Inches(8.8), y + Inches(0.42), Inches(4.2), Inches(0.42),
      "→ " + implication, size=11, color=BLUE)

t(slide, Inches(0.5), Inches(6.4), Inches(12.5), Inches(0.5),
  "技术趋势结论：监测行业正经历从硬件主导向软件定义的技术架构转型，云+AI是核心驱动力",
  size=12, bold=True, color=DARK)

# ============================================================
# SLIDE 7: 客户需求趋势（STP+4C框架）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "05", "客户需求趋势（STP市场细分 + 4C视角）")

# Two sections
t(slide, Inches(0.5), Inches(1.05), Inches(6.0), Inches(0.5),
  "STP市场细分：三类目标客户需求差异明显", size=14, bold=True, color=BLUE)
stp_data = [
    ("市政/水务集团", "需求：厂网河湖一体化监测平台，数据联网，智慧水务",
     "痛点：数据孤岛、运维成本高、人才缺乏", "→ 需要整体解决方案+长期运维服务"),
    ("工业园区/企业", "需求：满足监管要求的在线监测系统，碳核查，排放数据上报",
     "痛点：一次性投资大、进口品牌贵", "→ 性价比优先，国产替代机会大"),
    ("政府/监管机构", "需求：一张网监管平台，污染源追溯，预警应急",
     "痛点：数据质量参差不齐，信息安全", "→ 等保合规，数据主权要求高"),
]
for i, (seg, need, pain, ins) in enumerate(stp_data):
    y = Inches(1.55) + Inches(i * 1.25)
    bar(slide, Inches(0.5), y, Inches(6.2), Inches(1.15), RGBColor(245,248,252))
    t(slide, Inches(0.6), y + Inches(0.05), Inches(6.0), Inches(0.4),
      seg, size=12, bold=True, color=DARK)
    t(slide, Inches(0.6), y + Inches(0.45), Inches(6.0), Inches(0.3), need, size=10, color=DARK)
    t(slide, Inches(0.6), y + Inches(0.75), Inches(6.0), Inches(0.3), pain, size=10, color=RGBColor(180,60,0))
    t(slide, Inches(0.6), y + Inches(0.95), Inches(6.0), Inches(0.3), ins, size=10, bold=True, color=BLUE)

# 4C
t(slide, Inches(6.9), Inches(1.05), Inches(6.0), Inches(0.5),
  "4C客户价值视角：客户真正买的是什么？", size=14, bold=True, color=BLUE)
fourcs = [
    ("Customer Value\n客户价值", "不只是设备，是监测能力\n和数据带来的决策支持"),
    ("Cost\n总拥有成本", "不只是采购价，是3-5年\n运维+校准+升级成本"),
    ("Convenience\n便利性", "安装便捷、接口兼容、\n跨系统数据打通"),
    ("Communication\n沟通", "厂商能否响应快、\n提供本地化支持"),
]
for i, (title, desc) in enumerate(fourcs):
    x = Inches(6.9) + Inches(i % 2 * 3.1)
    y = Inches(1.6) + Inches(i // 2 * 1.9)
    bar(slide, x, y, Inches(2.9), Inches(1.75), RGBColor(245,248,252))
    bar(slide, x, y, Inches(2.9), Inches(0.4), BLUE)
    t(slide, x, y, Inches(2.9), Inches(0.4),
      title, size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    t(slide, x + Inches(0.1), y + Inches(0.5), Inches(2.7), Inches(1.1),
      desc, size=11, color=DARK, align=PP_ALIGN.CENTER)

t(slide, Inches(0.5), Inches(6.4), Inches(12.5), Inches(0.5),
  "洞察：客户买的是监测能力而非监测设备，纯硬件销售模式面临严峻挑战",
  size=12, bold=True, color=DARK)

# ============================================================
# SLIDE 8: 政策驱动（PESTEL-P/E维度）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "06", "政策驱动（PESTEL政策+经济维度）")

policies = [
    ("十五五规划：美丽中国建设", "P=政治",
     "美丽中国先行区、示范县建设推动全域环境基础设施建设，",
     "县镇级监测能力建设带来增量市场，黑臭水体治理持续，监测点位加密"),
    ("双碳目标：碳市场扩容", "E=经济",
     "全国碳市场覆盖行业扩大，碳监测/碳核查需求从电力向钢铁/化工/水泥延伸，",
     "碳排放在线监测、碳足迹管理、碳资产开发成为新增长赛道，年增速预估20-30%"),
    ("水环境精细化管理", "P=政治",
     "十四五水污染防止向十五五精细化管控过渡，流域监测、断面监测需求持续，",
     "饮用水源监测、地表水自动监测网络加密，推动高端监测设备需求"),
    ("大气多污染物协同控制", "P=政治",
     "臭氧与PM2.5协同管控，VOCS监测、无组织排放监管加强，",
     "大气监测从点源向面源、从浓度监测向成因精细化管控发展"),
    ("数字环保与智慧监管", "T=技术",
     "环保监管数字化转型，污染源自动监控一张网建设，",
     "数据联网、智慧决策、精准溯源成为监管标配，推动云平台和AI需求"),
]
for i, (title, tag, line1, line2) in enumerate(policies):
    y = Inches(1.05) + Inches(i * 1.08)
    bar(slide, Inches(0.5), y, Inches(0.06), Inches(0.85), BLUE)
    t(slide, Inches(0.7), y, Inches(5.5), Inches(0.42), title, size=14, bold=True, color=DARK)
    t(slide, Inches(6.3), y, Inches(1.2), Inches(0.42), tag, size=10, color=BLUE)
    t(slide, Inches(0.7), y + Inches(0.42), Inches(8.5), Inches(0.42), line1, size=12, color=DARK)
    t(slide, Inches(0.7), y + Inches(0.78), Inches(12.3), Inches(0.38),
      "→ " + line2, size=11, color=BLUE)

t(slide, Inches(0.5), Inches(6.4), Inches(12.5), Inches(0.5),
  "政策结论：政策是环境监测市场最强驱动力，十五五+双碳构成双重引擎，数字化监管是技术主线",
  size=12, bold=True, color=DARK)

# ============================================================
# SLIDE 9: 数字化跨界公司深度分析（竞争威胁）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_hdr(slide, "07", "数字化跨界公司：最值得关注的竞争威胁（39家）")

t(slide, Inches(0.5), Inches(1.05), Inches(12.5), Inches(0.45),
  "这39家公司以软件+数据+云平台为核心能力，跨界切入监测硬件市场，是展会中最值得关注的新兴力量",
  size=13, bold=True, color=DARK)

# Table header
bar(slide, Inches(0.5), Inches(1.55), Inches(12.3), Inches(0.42), BLUE)
headers = [("公司名称", 2.5), ("展位", 1.0), ("核心能力", 2.5), ("切入方式", 3.0), ("威胁等级", 1.5)]
x = Inches(0.6)
for h_name, h_width in headers:
    t(slide, x, Inches(1.55), Inches(h_width), Inches(0.42), h_name, size=11, bold=True, color=WHITE)
    x += Inches(h_width)

companies = [
    ("江苏纽带智能科技有限公司", "E3-G61", "端到端智能监测方案", "传感器+云平台+运维一体化", "极高"),
    ("杭州易环智能科技有限公司", "E1-L12", "智慧环保平台", "数据采集+可视化+运维全链条", "高"),
    ("北京尚云互联科技有限公司", "E2-W13", "环境监测云平台", "物联网数据接入+分析服务", "高"),
    ("E20环境平台", "E1-071", "环境产业互联网平台", "连接设备与用户，做平台而非设备", "高"),
    ("杭州盘古自动化系统有限公司", "E4-F71", "自动化控制系统", "PLC/DCS+云端接入，硬件整合", "中高"),
    ("山东混沌智能科技有限公司", "E4-F28", "智能传感器+云平台", "传感器+数据服务软件一体化", "中高"),
    ("广州云景信息科技有限公司", "E4-C21", "智慧水务平台", "水处理数据中台，绑定水务公司", "中"),
    ("缘循智能科技(上海)有限公司", "E4-L50", "流体控制智能化", "传感器+数据服务，垂直场景", "中"),
]

threat_colors = {"极高": RGBColor(200, 30, 30), "高": RGBColor(230, 100, 0),
                 "中高": RGBColor(200, 150, 0), "中": RGBColor(100, 150, 0)}

for i, (name, booth, ability, entry, threat) in enumerate(companies):
    y = Inches(2.05) + Inches(i * 0.5)
    bg = RGBColor(248,248,248) if i % 2 == 0 else WHITE
    bar(slide, Inches(0.5), y, Inches(12.3), Inches(0.45), bg)
    x = Inches(0.6)
    data = [name, booth, ability, entry, threat]
    widths = [2.5, 1.0, 2.5, 3.0, 1.5]
    for j, (val, w) in enumerate(zip(data, widths)):
        c = threat_colors.get(val, DARK) if j == 4 else DARK
        bold = j == 4
        t(slide, x, y, Inches(w), Inches(0.42), val, size=10, bold=bold, color=c)
        x += Inches(w)

t(slide, Inches(0.5), Inches(6.3), Inches(12.5), Inches(0.5),
  "战略启示：数字化跨界公司是最大不确定性来源，建议优先评估其云平台成熟度和客户覆盖度，重点防范平台型公司",
  size=12, bold=True, color=DARK)

# ============================================================
# SLIDE 10: 总结与战略启示
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
t(slide, Inches(0.5), Inches(0.35), Inches(10), Inches(0.7),
  "总结与战略启示", size=36, bold=True, color=DARK)

conclusions = [
    ("产品趋势", BLUE,
     "监测设备向实时化、智能化、平台化演进，",
     "纯硬件公司面临整合压力，需向设备+服务转型"),
    ("技术趋势", BLUE,
     "云平台SaaS化、IoT、AI分析、数字孪生是技术主线，",
     "技术架构从单机向云端迁移是大势所趋"),
    ("客户需求", RGBColor(0, 100, 60),
     "客户买的是监测能力而非监测设备，",
     "全链路管控、买服务不买设备是核心需求转变"),
    ("政策驱动", RGBColor(180, 60, 0),
     "十五五+双碳+数字化监管构成三重政策引擎，",
     "碳监测和县镇级监测是增量市场机会"),
    ("最值得关注的群体", RGBColor(150, 30, 150),
     "39家数字化跨界公司——平台+数据+服务能力，",
     "可能重塑监测行业竞争格局，是最大不确定性因素"),
]
for i, (label, color, line1, line2) in enumerate(conclusions):
    y = Inches(1.15) + Inches(i * 1.08)
    bar(slide, Inches(0.5), y, Inches(1.5), Inches(0.42), color)
    t(slide, Inches(0.5), y, Inches(1.5), Inches(0.42),
      label, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    t(slide, Inches(2.2), y, Inches(10.8), Inches(0.5), line1, size=14, bold=True, color=DARK)
    t(slide, Inches(2.2), y + Inches(0.48), Inches(10.8), Inches(0.45),
      "→ " + line2, size=12, color=color)

t(slide, Inches(0.5), Inches(6.6), Inches(12), Inches(0.4),
  "2026环博会市场观察报告  |  数据来源：微信公众号公开OCR数据  |  样本：972家参展厂商",
  size=11, color=LIGHT)

prs.save('/home/agentuser/环博会市场观察_v13.pptx')
print("v13 saved!")
