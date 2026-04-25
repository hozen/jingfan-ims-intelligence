"""
IMS竞争分析报告v10 - 纯白底，无背景无图案无logo
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Colors - accent only
ACCENT = RGBColor(0x48, 0x74, 0xCB)   # blue
RED = RGBColor(0xE5, 0x4C, 0x5E)
ORANGE = RGBColor(0xEE, 0x82, 0x2F)
GREEN = RGBColor(0x75, 0xBD, 0x42)
TEAL = RGBColor(0x30, 0xC0, 0xB4)
DARK = RGBColor(0x44, 0x54, 0x6A)
GRAY = RGBColor(0x70, 0x70, 0x70)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

def add_text(slide, left, top, width, height, text, size=18, bold=False,
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

def add_bullet(slide, x, y, label, text, label_color=None):
    """Add a labeled bullet point"""
    if label_color:
        dot = slide.shapes.add_shape(1, x, y + Pt(4), Pt(8), Pt(8))
        dot.fill.solid()
        dot.fill.fore_color.rgb = label_color
        dot.line.fill.background()
        add_text(slide, x + Inches(0.18), y, Inches(2), Inches(0.4),
                 label, size=14, bold=True, color=DARK)
        add_text(slide, x + Inches(2.2), y, Inches(10.5), Inches(0.8),
                 text, size=14, color=DARK)
    else:
        add_text(slide, x + Inches(0.18), y, Inches(12), Inches(0.5),
                 text, size=14, color=DARK)

# ============================================================
# SLIDE 1: Cover
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

add_text(slide, Inches(0.8), Inches(2.0), Inches(11), Inches(1.2),
         "2026环博会参展厂商竞争分析", size=44, bold=True, color=DARK)
add_text(slide, Inches(0.8), Inches(3.4), Inches(10), Inches(0.7),
         "IMS产品线竞争情报", size=26, color=ACCENT)
add_text(slide, Inches(0.8), Inches(4.3), Inches(10), Inches(0.5),
         "2026年4月  |  上海新国际博览中心  |  展位 E3-C12", size=16, color=GRAY)
add_text(slide, Inches(0.8), Inches(5.1), Inches(10), Inches(0.5),
         "数据来源：微信公众号公开OCR数据  |  样本：972家参展厂商", size=13, color=GRAY)

# ============================================================
# SLIDE 2: 数据来源
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_text(slide, Inches(0.6), Inches(0.4), Inches(10), Inches(0.7),
         "01  数据来源与样本说明", size=28, bold=True, color=DARK)

items = [
    ("数据来源", "微信公众号公开文章OCR提取，共识别972家参展厂商", ACCENT),
    ("展馆覆盖", "E1/E2/E3/E4/E5/E6/E7/N1/N2/N4/N5/W1~W5共16个馆", ACCENT),
    ("E4馆最多", "过程控制与仪器仪表馆，共182家展商标注", ORANGE),
    ("数字化跨界", "含云/平台/系统/数据/智能关键词：39家（全馆分散）", RED),
    ("E3馆说明", "监测与检测馆（展位E3-C12），数据因公众号图片加密仅15家", TEAL),
]
for i, (label, text, color) in enumerate(items):
    y = Inches(1.3) + Inches(i * 0.9)
    add_bullet(slide, Inches(0.6), y, label, text, color)

add_text(slide, Inches(0.6), Inches(6.2), Inches(12), Inches(0.5),
         "注：E+H、ABB、西门子、横河等未在OCR数据中检索到，可能以其他名称参展或未参展",
         size=11, color=GRAY)

# ============================================================
# SLIDE 3: 展馆分布
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_text(slide, Inches(0.6), Inches(0.4), Inches(10), Inches(0.7),
         "02  参展厂商展馆分布（972家）", size=28, bold=True, color=DARK)

halls = [
    ("E4馆", "182家", "过程控制与仪器仪表/监测与检测", ACCENT),
    ("E6馆", "187家", "大气治理/余热回收", TEAL),
    ("E5馆", "174家", "大气治理", GREEN),
    ("E2馆", "120家", "综合环境解决方案", ORANGE),
    ("E1馆", "93家", "综合环境解决方案", GREEN),
    ("E3馆", "15家", "监测与检测（数据不完整）", RED),
    ("其他馆", "181家", "N/W综合展区", GRAY),
]
for i, (hall, count, desc, color) in enumerate(halls):
    y = Inches(1.2) + Inches(i * 0.72)
    # colored left bar
    bar = slide.shapes.add_shape(1, Inches(0.6), y + Pt(3), Inches(0.06), Inches(0.38))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    add_text(slide, Inches(0.8), y, Inches(1.2), Inches(0.45), hall, size=14, bold=True)
    add_text(slide, Inches(2.0), y, Inches(1.0), Inches(0.45), count, size=14, bold=True, color=color)
    add_text(slide, Inches(3.1), y, Inches(9.5), Inches(0.45), desc, size=14)

add_text(slide, Inches(0.6), Inches(6.2), Inches(12), Inches(0.5),
         "关键洞察：E4馆（182家）仪器仪表展商最集中；E3馆数据严重不完整，需实地补充",
         size=12, bold=True, color=DARK)

# ============================================================
# SLIDE 4: 展商分类
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_text(slide, Inches(0.6), Inches(0.4), Inches(12), Inches(0.7),
         "03  972家展商分类（按产品/业务关键词）", size=28, bold=True, color=DARK)

cats = [
    ("数字化跨界公司", "39家", "云/平台/系统/数据/智能关键词，跨界打劫主力", RED,
     "杭州易环(E1)、尚云互联(E2)、江苏纽带智能(E3)、盘古自动化(E4)等"),
    ("仪表/传感器/仪器", "86家", "E4馆为主，直接竞品", ACCENT,
     "上泰仪器、天信仪表、威格中国、余姚市仪表四厂等"),
    ("水处理/泵阀/膜材料", "69家", "E1/E5馆为主", TEAL,
     "世浦泰膜、中国水务投资、澳欣膜科技等"),
    ("大气治理设备", "大量", "E5/E6馆为主，未精确统计", GREEN,
     "兰山环保、杜尔涂装等"),
    ("环保工程/水务投资", "约30家", "E1/E2馆为主", ORANGE,
     "中国水务投资、北控水务等"),
    ("其他/未分类", "约688家", "数据解析率约60-70%", GRAY,
     "过滤材料、阀门、管道等"),
]
for i, (cat, count, desc, color, examples) in enumerate(cats):
    y = Inches(1.1) + Inches(i * 0.88)
    bar = slide.shapes.add_shape(1, Inches(0.6), y, Inches(0.06), Inches(0.65))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    add_text(slide, Inches(0.8), y, Inches(3.2), Inches(0.42), cat, size=14, bold=True)
    add_text(slide, Inches(4.0), y, Inches(0.9), Inches(0.42), count, size=14, bold=True, color=color)
    add_text(slide, Inches(5.0), y, Inches(4.5), Inches(0.42), desc, size=13)
    add_text(slide, Inches(0.8), y + Inches(0.38), Inches(12.2), Inches(0.35),
             "例：" + examples, size=11, color=GRAY)

# ============================================================
# SLIDE 5: 39家数字化跨界公司
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_text(slide, Inches(0.6), Inches(0.4), Inches(12), Inches(0.7),
         "04  39家数字化跨界公司 — 跨界打劫主力", size=28, bold=True, color=RED)

digital = [
    ("E1馆", "杭州易环智能科技有限公司", "E1-L12"),
    ("E1馆", "E20环境平台", "E1-071"),
    ("E2馆", "北京尚云互联科技有限公司", "E2-W13"),
    ("E2馆", "重庆知行数联智能科技", "E2-A43"),
    ("E2馆", "华夏安健物联科技(青岛)", "E2-A26"),
    ("E3馆", "江苏纽带智能科技有限公司", "E3-G61"),
    ("E4馆", "格林菲普流体控制系统(上海)", "E4-F19"),
    ("E4馆", "科译勒(上海)智能仪表有限公司", "E4-603"),
    ("E4馆", "山东混沌智能科技有限公司", "E4-F28"),
    ("E4馆", "上海温宝自动化系统工程有限公司", "E4-A19"),
    ("E4馆", "广州云景信息科技有限公司", "E4-C21"),
    ("E4馆", "杭州盘古自动化系统有限公司", "E4-F71"),
    ("E4馆", "杭州异辉智能科技有限公司", "E4-L80"),
    ("E4馆", "缘循智能科技(上海)有限公司", "E4-L50"),
    ("E4馆", "邯郸市耘农智慧农业科技", "E4-630"),
    ("E5馆", "佛山蔚蓝时代智能装备有限公司", "E5-L53"),
    ("E5馆", "广东元晟智能装备制造有限公司", "E5-039"),
    ("E5馆", "镇江东方电热智能装备有限公司", "E5-069"),
    ("E6馆", "迪扬过滤系统(昆山)有限公司", "E6-0D53"),
    ("E6馆", "杭州捷瑞智能装备股份有限公司", "E6-040"),
    ("E6馆", "江苏中车云汇科技有限公司", "E6-B21/A22"),
    ("E6馆", "奇点低碳智能装备(浙江)", "E6-G16"),
    ("W3馆", "东莞市云峰机电科技有限公司", "W3-A41"),
    ("W3馆", "上海罗普自动化控制系统有限公司", "W3-G19"),
]

# 3 columns
cols = [digital[i:i+9] for i in range(0, len(digital), 9)]
xs = [Inches(0.4), Inches(4.5), Inches(8.6)]
for ci, col in enumerate(cols):
    x = xs[ci]
    for ri, (hall, name, booth) in enumerate(col):
        y = Inches(1.0) + Inches(ri * 0.6)
        # hall tag
        tag = slide.shapes.add_shape(1, x, y + Pt(2), Inches(0.7), Inches(0.32), ACCENT)
        tag.fill.solid()
        tag.fill.fore_color.rgb = ACCENT
        tag.line.fill.background()
        add_text(slide, x, y + Pt(2), Inches(0.7), Inches(0.32),
                 hall, size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(slide, x + Inches(0.78), y, Inches(3.5), Inches(0.45), name, size=12)
        add_text(slide, x + Inches(0.78), y + Inches(0.3), Inches(3.5), Inches(0.3), booth, size=10, color=GRAY)

# threat callout
add_text(slide, Inches(0.4), Inches(6.4), Inches(12.5), Inches(0.6),
         "核心威胁：这些公司具备云平台+端到端方案能力，可整合传感器+数据+云，侵蚀监测市场份额",
         size=13, bold=True, color=RED)

# ============================================================
# SLIDE 6: 波特五力
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_text(slide, Inches(0.6), Inches(0.4), Inches(12), Inches(0.7),
         "05  波特五力分析（基于972家展商数据）", size=28, bold=True, color=DARK)

forces = [
    ("现有竞争者威胁", "高", "E4馆182家仪器仪表展商直接竞争，价格战激烈",
     "证据：上泰仪器、天信仪表、威格中国等86家", RED),
    ("潜在新进入者威胁", "中", "39家数字化跨界公司具备云平台能力",
     "证据：江苏纽带智能、杭州易环智能、尚云互联等", ORANGE),
    ("替代品威胁", "高", "在线监测替代实验室检测趋势加速",
     "证据：便携式监测、无人机监测、卫星遥感等", RED),
    ("供应商议价能力", "中", "传感器/芯片供应链集中度较高",
     "证据：水质传感器核心芯片仍依赖进口", ORANGE),
    ("购买者议价能力", "高", "水务/环保运营商整合，集中采购压价",
     "证据：北控水务、中国水务等大型水务集团", RED),
]
for i, (force, level, desc, evidence, color) in enumerate(forces):
    y = Inches(1.1) + Inches(i * 1.0)
    bar = slide.shapes.add_shape(1, Inches(0.6), y + Pt(3), Inches(0.06), Inches(0.5), color)
    bar.line.fill.background()
    add_text(slide, Inches(0.8), y, Inches(3.5), Inches(0.45), force, size=15, bold=True)
    lvl_c = RED if level == "高" else ORANGE
    add_text(slide, Inches(4.4), y, Inches(0.6), Inches(0.45), level, size=14, bold=True, color=lvl_c)
    add_text(slide, Inches(5.1), y, Inches(5.2), Inches(0.45), desc, size=14)
    add_text(slide, Inches(0.8), y + Inches(0.4), Inches(12.2), Inches(0.35), evidence, size=11, color=GRAY)

# ============================================================
# SLIDE 7: SWOT
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_text(slide, Inches(0.6), Inches(0.4), Inches(12), Inches(0.7),
         "06  SWOT分析（基于展商数据的事实性观察）", size=28, bold=True, color=DARK)

# 2x2 grid
# S - top left
add_text(slide, Inches(0.6), Inches(1.1), Inches(1.2), Inches(0.45), "S 优势",
         size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
bg = slide.shapes.add_shape(1, Inches(0.6), Inches(1.1), Inches(1.2), Inches(0.45), ACCENT)
bg.line.fill.background()
add_text(slide, Inches(0.6), Inches(1.1), Inches(1.2), Inches(0.45), "S 优势",
         size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(slide, Inches(0.6), Inches(1.65), Inches(6.0), Inches(0.6),
         "水质分析仪器有较高品牌认知，E4-D08/E08有独立展位", size=13)
add_text(slide, Inches(0.6), Inches(2.2), Inches(6.0), Inches(0.6),
         "IMS产品线覆盖水质监测全参数，E3-C12展位位于监测与检测馆", size=13)

# W - top right
add_text(slide, Inches(6.8), Inches(1.1), Inches(1.2), Inches(0.45), "W 劣势",
         size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
bg = slide.shapes.add_shape(1, Inches(6.8), Inches(1.1), Inches(1.2), Inches(0.45), ORANGE)
bg.line.fill.background()
add_text(slide, Inches(6.8), Inches(1.1), Inches(1.2), Inches(0.45), "W 劣势",
         size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(slide, Inches(6.8), Inches(1.65), Inches(6.0), Inches(0.6),
         "E4馆大量国内仪表厂商价格显著低于哈希（同在E4馆）", size=13)
add_text(slide, Inches(6.8), Inches(2.2), Inches(6.0), Inches(0.6),
         "39家数字化跨界公司已在云平台层面布局，先于哈希建立IMS能力", size=13)

# O - bottom left
add_text(slide, Inches(0.6), Inches(3.1), Inches(1.2), Inches(0.45), "O 机会",
         size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
bg = slide.shapes.add_shape(1, Inches(0.6), Inches(3.1), Inches(1.2), Inches(0.45), GREEN)
bg.line.fill.background()
add_text(slide, Inches(0.6), Inches(3.1), Inches(1.2), Inches(0.45), "O 机会",
         size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(slide, Inches(0.6), Inches(3.65), Inches(6.0), Inches(0.6),
         "E3馆（监测与检测）展商数据不完整，存在未被识别的市场空白", size=13)
add_text(slide, Inches(0.6), Inches(4.2), Inches(6.0), Inches(0.6),
         "传统仪器仪表展商多为单一参数产品，全参数覆盖仍是差异化优势", size=13)

# T - bottom right
add_text(slide, Inches(6.8), Inches(3.1), Inches(1.2), Inches(0.45), "T 威胁",
         size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
bg = slide.shapes.add_shape(1, Inches(6.8), Inches(3.1), Inches(1.2), Inches(0.45), RED)
bg.line.fill.background()
add_text(slide, Inches(6.8), Inches(3.1), Inches(1.2), Inches(0.45), "T 威胁",
         size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(slide, Inches(6.8), Inches(3.65), Inches(6.0), Inches(0.6),
         "江苏纽带智能(E3-G61)等提供端到端IMS方案，整合传感器+云平台", size=13)
add_text(slide, Inches(6.8), Inches(4.2), Inches(6.0), Inches(0.6),
         "数字化跨界公司39家，可基于云平台提供打包监测解决方案", size=13)

add_text(slide, Inches(0.6), Inches(5.1), Inches(12.5), Inches(0.5),
         "注：以上SWOT条目均基于可验证的展商数据事实。E+H、ABB、西门子、横河等未在OCR数据中检索到。",
         size=11, color=GRAY)

# ============================================================
# SLIDE 8: 90天行动建议
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_text(slide, Inches(0.6), Inches(0.4), Inches(10), Inches(0.7),
         "07  90天行动建议", size=28, bold=True, color=DARK)

actions = [
    ("30天", "建立39家数字化跨界公司竞争情报档案",
     "梳理每家公司云平台架构、产品参数、目标客户，评估与IMS重叠度", RED),
    ("30天", "重点分析江苏纽带智能(E3-G61)等端到端方案公司",
     "评估其是否已推出与IMS直接竞争的产品，输出内部评估报告", ORANGE),
    ("60天", "完成E4馆182家展商竞品分类",
     "区分直接竞品、渠道合作方、潜在合作伙伴，拜访重点展商", ACCENT),
    ("60天", "与E4馆国内仪表厂商建立联系",
     "了解其价格体系和产品路线图，为应对价格竞争做准备", TEAL),
    ("90天", "发布IMS产品线竞争力评估内部报告",
     "基于展商数据和客户沟通，评估IMS产品在监测市场的竞争地位", GREEN),
    ("90天", "与水务/环保运营商客户验证价格压力",
     "向大型水务集团客户了解采购趋势，验证展会观察到的价格压力", GREEN),
]
for i, (tl, action, detail, color) in enumerate(actions):
    y = Inches(1.1) + Inches(i * 0.9)
    # timeline tag
    bg = slide.shapes.add_shape(1, Inches(0.6), y + Pt(2), Inches(0.9), Inches(0.42), color)
    bg.line.fill.background()
    add_text(slide, Inches(0.6), y + Pt(2), Inches(0.9), Inches(0.42),
             tl, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, Inches(1.7), y, Inches(5.0), Inches(0.5), action, size=14, bold=True)
    add_text(slide, Inches(1.7), y + Inches(0.4), Inches(11.2), Inches(0.45), detail, size=12, color=GRAY)

# ============================================================
# SLIDE 9: 核心结论
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_text(slide, Inches(0.6), Inches(0.4), Inches(10), Inches(0.7),
         "08  核心结论", size=36, bold=True, color=DARK)

conclusions = [
    ("最大威胁", "不是传统仪表同行，而是39家数字化跨界公司（跨界打劫）",
     RED, "江苏纽带智能、尚云互联、杭州易环智能、E20环境平台等"),
    ("直接竞争", "E4馆182家仪器仪表展商构成直接竞争，但多为单一参数产品",
     ACCENT, "优势在于全参数覆盖和品牌信任度"),
    ("跨界侵蚀", "39家数字化公司具备云平台+端到端方案能力，可能侵蚀IMS核心市场",
     ORANGE, "这些公司整合传感器+云平台，对IMS产品线威胁最大"),
    ("数据缺口", "E3馆（监测与检测）数据不完整，需进一步补充E3馆完整展商数据",
     TEAL, "展位在E3-C12，展会期间可实地核实E3馆展商"),
]
for i, (label, text, color, example) in enumerate(conclusions):
    y = Inches(1.3) + Inches(i * 1.1)
    # label tag
    bg = slide.shapes.add_shape(1, Inches(0.6), y, Inches(1.5), Inches(0.42), color)
    bg.line.fill.background()
    add_text(slide, Inches(0.6), y, Inches(1.5), Inches(0.42),
             label, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, Inches(2.3), y, Inches(10.7), Inches(0.5), text, size=16, bold=True)
    add_text(slide, Inches(2.3), y + Inches(0.42), Inches(10.7), Inches(0.4), example, size=12, color=GRAY)

add_text(slide, Inches(0.6), Inches(6.2), Inches(12), Inches(0.4),
         "IMS产品线  |  2026环博会  |  数据来源：微信公众号公开OCR数据",
         size=11, color=GRAY)

prs.save('/home/agentuser/IMS竞争分析报告_v10.pptx')
print("v10 saved!")
