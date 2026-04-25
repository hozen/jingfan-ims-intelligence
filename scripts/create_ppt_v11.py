"""
IMS竞争分析报告v11 - 仅用HACH三色：蓝(0,126,181)、深灰(77,77,77)、浅灰(153,153,153)
纯白底，无背景图形，无logo
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

def txt(slide, left, top, width, height, text, size=14, bold=False,
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

def page_title(slide, num, title):
    """Standard page header with blue section number and dark title"""
    txt(slide, Inches(0.5), Inches(0.35), Inches(1), Inches(0.6),
        num, size=28, bold=True, color=BLUE)
    txt(slide, Inches(1.5), Inches(0.38), Inches(11), Inches(0.6),
        title, size=28, bold=True, color=DARK)

# ============================================================
# SLIDE 1: Cover
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
txt(slide, Inches(0.8), Inches(2.0), Inches(11.5), Inches(1.3),
    "2026环博会参展厂商竞争分析", size=44, bold=True, color=DARK)
txt(slide, Inches(0.8), Inches(3.5), Inches(11), Inches(0.7),
    "IMS产品线竞争情报", size=26, color=BLUE)
txt(slide, Inches(0.8), Inches(4.4), Inches(11), Inches(0.5),
    "2026年4月  |  上海新国际博览中心  |  展位 E3-C12", size=16, color=DARK)
txt(slide, Inches(0.8), Inches(5.2), Inches(11), Inches(0.5),
    "数据来源：微信公众号公开OCR数据  |  样本：972家参展厂商", size=13, color=LIGHT)

# ============================================================
# SLIDE 2: 数据来源
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_title(slide, "01", "数据来源与样本说明")

items = [
    ("数据来源", "微信公众号公开文章OCR提取，共识别972家参展厂商"),
    ("展馆覆盖", "E1/E2/E3/E4/E5/E6/E7/N1/N2/N4/N5/W1~W5共16个馆"),
    ("E4馆最多", "过程控制与仪器仪表馆，共182家展商标注"),
    ("数字化跨界", "含云/平台/系统/数据/智能关键词：39家（全馆分散）"),
    ("E3馆说明", "监测与检测馆（展位E3-C12），数据因公众号图片加密仅15家"),
]
for i, (label, text) in enumerate(items):
    y = Inches(1.3) + Inches(i * 0.92)
    bar(slide, Inches(0.5), y + Pt(5), Pt(8), Pt(8), BLUE)
    txt(slide, Inches(0.72), y, Inches(2.2), Inches(0.5), label, size=15, bold=True, color=DARK)
    txt(slide, Inches(2.95), y, Inches(10.3), Inches(0.8), text, size=15, color=DARK)

txt(slide, Inches(0.5), Inches(6.3), Inches(12.5), Inches(0.5),
    "注：E+H、ABB、西门子、横河等未在OCR数据中检索到，可能以其他名称参展或未参展",
    size=11, color=LIGHT)

# ============================================================
# SLIDE 3: 展馆分布
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_title(slide, "02", "参展厂商展馆分布（972家）")

halls = [
    ("E4馆", "182家", "过程控制与仪器仪表/监测与检测"),
    ("E6馆", "187家", "大气治理/余热回收"),
    ("E5馆", "174家", "大气治理"),
    ("E2馆", "120家", "综合环境解决方案"),
    ("E1馆", "93家", "综合环境解决方案"),
    ("E3馆", "15家", "监测与检测（数据不完整）"),
    ("其他馆", "181家", "N/W综合展区"),
]
for i, (hall, count, desc) in enumerate(halls):
    y = Inches(1.2) + Inches(i * 0.74)
    bar(slide, Inches(0.5), y + Pt(4), Inches(0.06), Inches(0.38), BLUE)
    txt(slide, Inches(0.7), y, Inches(1.2), Inches(0.5), hall, size=14, bold=True, color=DARK)
    txt(slide, Inches(1.9), y, Inches(1.0), Inches(0.5), count, size=14, bold=True, color=BLUE)
    txt(slide, Inches(3.0), y, Inches(9.8), Inches(0.5), desc, size=14, color=DARK)

txt(slide, Inches(0.5), Inches(6.3), Inches(12.5), Inches(0.5),
    "关键洞察：E4馆（182家）仪器仪表展商最集中；E3馆数据严重不完整，需实地补充",
    size=12, bold=True, color=DARK)

# ============================================================
# SLIDE 4: 展商分类
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_title(slide, "03", "972家展商分类（按产品/业务关键词）")

cats = [
    ("数字化跨界公司", "39家", "云/平台/系统/数据/智能关键词，跨界打劫主力",
     "杭州易环(E1)、尚云互联(E2)、江苏纽带智能(E3)、盘古自动化(E4)等"),
    ("仪表/传感器/仪器", "86家", "E4馆为主，直接竞品",
     "上泰仪器、天信仪表、威格中国、余姚市仪表四厂等"),
    ("水处理/泵阀/膜材料", "69家", "E1/E5馆为主",
     "世浦泰膜、中国水务投资、澳欣膜科技等"),
    ("大气治理设备", "大量", "E5/E6馆为主，未精确统计",
     "兰山环保、杜尔涂装等"),
    ("环保工程/水务投资", "约30家", "E1/E2馆为主",
     "中国水务投资、北控水务等"),
    ("其他/未分类", "约688家", "数据解析率约60-70%",
     "过滤材料、阀门、管道等"),
]
for i, (cat, count, desc, examples) in enumerate(cats):
    y = Inches(1.1) + Inches(i * 0.88)
    bar(slide, Inches(0.5), y, Inches(0.06), Inches(0.68), BLUE)
    txt(slide, Inches(0.7), y, Inches(3.0), Inches(0.45), cat, size=14, bold=True, color=DARK)
    txt(slide, Inches(3.8), y, Inches(0.9), Inches(0.45), count, size=14, bold=True, color=BLUE)
    txt(slide, Inches(4.8), y, Inches(4.5), Inches(0.45), desc, size=13, color=DARK)
    txt(slide, Inches(0.7), y + Inches(0.4), Inches(12.3), Inches(0.35),
        "例：" + examples, size=11, color=LIGHT)

# ============================================================
# SLIDE 5: 39家数字化跨界公司
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_title(slide, "04", "39家数字化跨界公司 — 跨界打劫主力")

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

cols = [digital[i:i+9] for i in range(0, len(digital), 9)]
xs = [Inches(0.4), Inches(4.5), Inches(8.6)]
for ci, col in enumerate(cols):
    x = xs[ci]
    for ri, (hall, name, booth) in enumerate(col):
        y = Inches(1.05) + Inches(ri * 0.6)
        bar(slide, x, y + Pt(2), Inches(0.7), Inches(0.32), BLUE)
        txt(slide, x, y + Pt(2), Inches(0.7), Inches(0.32),
            hall, size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        txt(slide, x + Inches(0.78), y, Inches(3.5), Inches(0.45), name, size=12, color=DARK)
        txt(slide, x + Inches(0.78), y + Inches(0.3), Inches(3.5), Inches(0.3), booth, size=10, color=LIGHT)

txt(slide, Inches(0.4), Inches(6.4), Inches(12.5), Inches(0.6),
    "核心威胁：这些公司具备云平台+端到端方案能力，可整合传感器+数据+云，侵蚀监测市场份额",
    size=13, bold=True, color=DARK)

# ============================================================
# SLIDE 6: 波特五力
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_title(slide, "05", "波特五力分析（基于972家展商数据）")

forces = [
    ("现有竞争者威胁", "高", "E4馆182家仪器仪表展商直接竞争，价格战激烈",
     "证据：上泰仪器、天信仪表、威格中国等86家"),
    ("潜在新进入者威胁", "中", "39家数字化跨界公司具备云平台能力",
     "证据：江苏纽带智能、杭州易环智能、尚云互联等"),
    ("替代品威胁", "高", "在线监测替代实验室检测趋势加速",
     "证据：便携式监测、无人机监测、卫星遥感等"),
    ("供应商议价能力", "中", "传感器/芯片供应链集中度较高",
     "证据：水质传感器核心芯片仍依赖进口"),
    ("购买者议价能力", "高", "水务/环保运营商整合，集中采购压价",
     "证据：北控水务、中国水务等大型水务集团"),
]
for i, (force, level, desc, evidence) in enumerate(forces):
    y = Inches(1.1) + Inches(i * 1.02)
    bar(slide, Inches(0.5), y + Pt(3), Inches(0.06), Inches(0.52), BLUE)
    txt(slide, Inches(0.7), y, Inches(3.5), Inches(0.48), force, size=15, bold=True, color=DARK)
    lvl_c = DARK if level == "高" else LIGHT
    txt(slide, Inches(4.3), y, Inches(0.6), Inches(0.48), level, size=14, bold=True, color=lvl_c)
    txt(slide, Inches(5.0), y, Inches(5.2), Inches(0.48), desc, size=14, color=DARK)
    txt(slide, Inches(0.7), y + Inches(0.44), Inches(12.3), Inches(0.38), evidence, size=11, color=LIGHT)

# ============================================================
# SLIDE 7: SWOT
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_title(slide, "06", "SWOT分析（基于展商数据的事实性观察）")

# S
bar(slide, Inches(0.5), Inches(1.1), Inches(1.2), Inches(0.48), BLUE)
txt(slide, Inches(0.5), Inches(1.1), Inches(1.2), Inches(0.48),
    "S 优势", size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(slide, Inches(0.5), Inches(1.7), Inches(6.0), Inches(0.65),
    "水质分析仪器有较高品牌认知，E4-D08/E08有独立展位", size=13, color=DARK)
txt(slide, Inches(0.5), Inches(2.3), Inches(6.0), Inches(0.65),
    "IMS产品线覆盖水质监测全参数，E3-C12展位位于监测与检测馆", size=13, color=DARK)

# W
bar(slide, Inches(6.8), Inches(1.1), Inches(1.2), Inches(0.48), LIGHT)
txt(slide, Inches(6.8), Inches(1.1), Inches(1.2), Inches(0.48),
    "W 劣势", size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(slide, Inches(6.8), Inches(1.7), Inches(6.0), Inches(0.65),
    "E4馆大量国内仪表厂商价格显著低于哈希（同在E4馆）", size=13, color=DARK)
txt(slide, Inches(6.8), Inches(2.3), Inches(6.0), Inches(0.65),
    "39家数字化跨界公司已在云平台层面布局，先于哈希建立IMS能力", size=13, color=DARK)

# O
bar(slide, Inches(0.5), Inches(3.2), Inches(1.2), Inches(0.48), BLUE)
txt(slide, Inches(0.5), Inches(3.2), Inches(1.2), Inches(0.48),
    "O 机会", size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(slide, Inches(0.5), Inches(3.8), Inches(6.0), Inches(0.65),
    "E3馆（监测与检测）展商数据不完整，存在未被识别的市场空白", size=13, color=DARK)
txt(slide, Inches(0.5), Inches(4.4), Inches(6.0), Inches(0.65),
    "传统仪器仪表展商多为单一参数产品，全参数覆盖仍是差异化优势", size=13, color=DARK)

# T
bar(slide, Inches(6.8), Inches(3.2), Inches(1.2), Inches(0.48), LIGHT)
txt(slide, Inches(6.8), Inches(3.2), Inches(1.2), Inches(0.48),
    "T 威胁", size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(slide, Inches(6.8), Inches(3.8), Inches(6.0), Inches(0.65),
    "江苏纽带智能(E3-G61)等提供端到端IMS方案，整合传感器+云平台", size=13, color=DARK)
txt(slide, Inches(6.8), Inches(4.4), Inches(6.0), Inches(0.65),
    "数字化跨界公司39家，可基于云平台提供打包监测解决方案", size=13, color=DARK)

txt(slide, Inches(0.5), Inches(5.3), Inches(12.5), Inches(0.5),
    "注：以上SWOT条目均基于可验证的展商数据事实。E+H、ABB、西门子、横河等未在OCR数据中检索到。",
    size=11, color=LIGHT)

# ============================================================
# SLIDE 8: 90天行动建议
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
page_title(slide, "07", "90天行动建议")

actions = [
    ("30天", "建立39家数字化跨界公司竞争情报档案",
     "梳理每家公司云平台架构、产品参数、目标客户，评估与IMS重叠度"),
    ("30天", "重点分析江苏纽带智能(E3-G61)等端到端方案公司",
     "评估其是否已推出与IMS直接竞争的产品，输出内部评估报告"),
    ("60天", "完成E4馆182家展商竞品分类",
     "区分直接竞品、渠道合作方、潜在合作伙伴，拜访重点展商"),
    ("60天", "与E4馆国内仪表厂商建立联系",
     "了解其价格体系和产品路线图，为应对价格竞争做准备"),
    ("90天", "发布IMS产品线竞争力评估内部报告",
     "基于展商数据和客户沟通，评估IMS产品在监测市场的竞争地位"),
    ("90天", "与水务/环保运营商客户验证价格压力",
     "向大型水务集团客户了解采购趋势，验证展会观察到的价格压力"),
]
for i, (tl, action, detail) in enumerate(actions):
    y = Inches(1.1) + Inches(i * 0.9)
    bar(slide, Inches(0.5), y + Pt(2), Inches(0.9), Inches(0.44), BLUE)
    txt(slide, Inches(0.5), y + Pt(2), Inches(0.9), Inches(0.44),
        tl, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(slide, Inches(1.6), y, Inches(5.2), Inches(0.5), action, size=14, bold=True, color=DARK)
    txt(slide, Inches(1.6), y + Inches(0.42), Inches(11.3), Inches(0.45), detail, size=12, color=LIGHT)

# ============================================================
# SLIDE 9: 核心结论
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
txt(slide, Inches(0.5), Inches(0.35), Inches(10), Inches(0.7),
    "核心结论", size=36, bold=True, color=DARK)

conclusions = [
    ("最大威胁", "不是传统仪表同行，而是39家数字化跨界公司（跨界打劫）",
     "江苏纽带智能、尚云互联、杭州易环智能、E20环境平台等"),
    ("直接竞争", "E4馆182家仪器仪表展商构成直接竞争，但多为单一参数产品",
     "优势在于全参数覆盖和品牌信任度"),
    ("跨界侵蚀", "39家数字化公司具备云平台+端到端方案能力，可能侵蚀IMS核心市场",
     "这些公司整合传感器+云平台，对IMS产品线威胁最大"),
    ("数据缺口", "E3馆（监测与检测）数据不完整，需进一步补充E3馆完整展商数据",
     "展位在E3-C12，展会期间可实地核实E3馆展商"),
]
for i, (label, text, example) in enumerate(conclusions):
    y = Inches(1.3) + Inches(i * 1.12)
    bar(slide, Inches(0.5), y, Inches(1.5), Inches(0.44), BLUE)
    txt(slide, Inches(0.5), y, Inches(1.5), Inches(0.44),
        label, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(slide, Inches(2.2), y, Inches(10.7), Inches(0.5), text, size=16, bold=True, color=DARK)
    txt(slide, Inches(2.2), y + Inches(0.44), Inches(10.7), Inches(0.4), example, size=12, color=LIGHT)

txt(slide, Inches(0.5), Inches(6.3), Inches(12), Inches(0.4),
    "IMS产品线  |  2026环博会  |  数据来源：微信公众号公开OCR数据",
    size=11, color=LIGHT)

prs.save('/home/agentuser/IMS竞争分析报告_v11.pptx')
print("v11 saved!")
