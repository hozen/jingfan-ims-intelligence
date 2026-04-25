"""
IMS竞争分析报告v9 - 基于哈希模板配色，无品牌元素
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Hach brand colors only (no branding names)
HACH_DARK = RGBColor(0x44, 0x54, 0x6A)
HACH_BLUE = RGBColor(0x48, 0x74, 0xCB)
HACH_ORANGE = RGBColor(0xEE, 0x82, 0x2F)
HACH_YELLOW = RGBColor(0xF2, 0xBA, 0x02)
HACH_GREEN = RGBColor(0x75, 0xBD, 0x42)
HACH_TEAL = RGBColor(0x30, 0xC0, 0xB4)
HACH_RED = RGBColor(0xE5, 0x4C, 0x5E)
HACH_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
HACH_LIGHT = RGBColor(0xE7, 0xE6, 0xE6)
HACH_GRAY = RGBColor(0x70, 0x70, 0x70)

FONT_CN = "微软雅黑"
FONT_EN = "Msyh"

prs = Presentation('/home/agentuser/.hermes/cache/documents/doc_3aadc0f19433_2023新版PPT中文模板-电脑办公系统版本.pptx')

def clear_slide(slide):
    for shape in slide.shapes:
        sp = shape._element
        sp.getparent().remove(sp)

def add_rect(slide, left, top, width, height, fill_color):
    shape = slide.shapes.add_shape(1, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape

def add_text(slide, left, top, width, height, text, size=14, bold=False,
             color=None, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.name = FONT_CN
    p.font.color.rgb = color if color else HACH_DARK
    p.alignment = align
    return box

# ============================================================
# SLIDE 1: Cover
# ============================================================
slide1 = prs.slides[1]
clear_slide(slide1)

add_rect(slide1, 0, 0, prs.slide_width, prs.slide_height, HACH_LIGHT)
add_rect(slide1, 0, 0, Inches(0.12), prs.slide_height, HACH_BLUE)
add_rect(slide1, Inches(0.5), Inches(5.8), Inches(5), Pt(4), HACH_ORANGE)

add_text(slide1, Inches(0.6), Inches(2.0), Inches(10), Inches(1.2),
         "2026环博会参展厂商竞争分析", size=40, bold=True, color=HACH_DARK)
add_text(slide1, Inches(0.6), Inches(3.3), Inches(10), Inches(0.8),
         "IMS产品线竞争情报", size=24, bold=False, color=HACH_BLUE)
add_text(slide1, Inches(0.6), Inches(4.2), Inches(10), Inches(0.5),
         "2026年4月  |  上海新国际博览中心  |  展位 E3-C12", size=16, color=HACH_DARK)
add_text(slide1, Inches(0.6), Inches(5.0), Inches(10), Inches(0.5),
         "数据来源：微信公众号公开数据OCR提取  |  样本：972家参展厂商",
         size=12, color=HACH_GRAY)

# ============================================================
# SLIDE 2: 样本说明
# ============================================================
slide2 = prs.slides[4]
clear_slide(slide2)

add_rect(slide2, 0, 0, prs.slide_width, Inches(0.8), HACH_BLUE)
add_text(slide2, Inches(0.3), Inches(0.1), Inches(0.5), Inches(0.6),
         "01", size=28, bold=True, color=HACH_WHITE)
add_text(slide2, Inches(0.9), Inches(0.15), Inches(10), Inches(0.6),
         "数据来源与样本说明", size=26, bold=True, color=HACH_WHITE)

bullets = [
    ("数据来源", "微信公众号公开文章OCR提取，共识别972家参展厂商"),
    ("展馆覆盖", "E1/E2/E3/E4/E5/E6/E7/N1/N2/N4/N5/W1/W2/W3/W4/W5共16个馆"),
    ("E4馆最多", "过程控制与仪器仪表馆，共182家展商标注"),
    ("数字化跨界展商", "含云/平台/系统/数据/智能关键词：39家（全馆分散）"),
    ("E3馆说明", "监测与检测馆（展位E3-C12），数据因公众号图片加密仅获取15家"),
]
dot_colors = [HACH_BLUE, HACH_ORANGE, HACH_GREEN, HACH_TEAL, HACH_RED]
y_start = Inches(1.1)
for i, (label, text) in enumerate(bullets):
    y = y_start + Inches(i * 1.0)
    dot = add_rect(slide2, Inches(0.4), y + Pt(6), Pt(12), Pt(12), dot_colors[i])
    add_text(slide2, Inches(0.65), y, Inches(1.8), Inches(0.5),
             label, size=16, bold=True, color=HACH_DARK)
    add_text(slide2, Inches(2.5), y, Inches(10.3), Inches(0.8), text, size=15)

add_text(slide2, Inches(0.4), Inches(6.5), Inches(12), Inches(0.5),
         "注：E+H、ABB、西门子、横河等未在OCR数据中检索到，可能以其他名称参展或未参展",
         size=11, color=HACH_GRAY)

# ============================================================
# SLIDE 3: 展馆分布
# ============================================================
slide3 = prs.slides[4]
clear_slide(slide3)

add_rect(slide3, 0, 0, prs.slide_width, Inches(0.8), HACH_BLUE)
add_text(slide3, Inches(0.3), Inches(0.1), Inches(0.5), Inches(0.6),
         "02", size=28, bold=True, color=HACH_WHITE)
add_text(slide3, Inches(0.9), Inches(0.15), Inches(10), Inches(0.6),
         "参展厂商展馆分布（972家）", size=26, bold=True, color=HACH_WHITE)

hall_data = [
    ("E4馆", "182家", "过程控制与仪器仪表/监测与检测", HACH_BLUE),
    ("E6馆", "187家", "大气治理/余热回收", HACH_TEAL),
    ("E5馆", "174家", "大气治理", HACH_GREEN),
    ("E2馆", "120家", "综合环境解决方案", HACH_ORANGE),
    ("E1馆", "93家", "综合环境解决方案", HACH_YELLOW),
    ("E3馆", "15家", "监测与检测（数据不完整）", HACH_RED),
    ("其他馆", "181家", "N/W综合展区", HACH_GRAY),
]
y_start = Inches(1.1)
for i, (hall, count, desc, color) in enumerate(hall_data):
    y = y_start + Inches(i * 0.75)
    add_rect(slide3, Inches(0.4), y + Pt(4), Inches(0.08), Inches(0.35), color)
    add_text(slide3, Inches(0.6), y, Inches(1.2), Inches(0.5), hall, size=16, bold=True)
    add_text(slide3, Inches(1.8), y, Inches(1.0), Inches(0.5), count, size=16, bold=True, color=color)
    add_text(slide3, Inches(2.9), y, Inches(9.5), Inches(0.5), desc, size=14)

add_rect(slide3, Inches(0.4), Inches(6.2), Inches(12.4), Inches(0.9), HACH_LIGHT)
add_text(slide3, Inches(0.6), Inches(6.3), Inches(12), Inches(0.6),
         "关键洞察：E4馆（182家）仪器仪表展商最集中；E3馆数据严重不完整，需实地补充",
         size=13, bold=True)

# ============================================================
# SLIDE 4: 展商分类
# ============================================================
slide4 = prs.slides[4]
clear_slide(slide4)

add_rect(slide4, 0, 0, prs.slide_width, Inches(0.8), HACH_BLUE)
add_text(slide4, Inches(0.3), Inches(0.1), Inches(0.5), Inches(0.6),
         "03", size=28, bold=True, color=HACH_WHITE)
add_text(slide4, Inches(0.9), Inches(0.15), Inches(10), Inches(0.6),
         "972家展商分类（按产品/业务关键词）", size=26, bold=True, color=HACH_WHITE)

categories = [
    ("数字化跨界公司", "39家", "云/平台/系统/数据/智能关键词，跨界打劫主力", HACH_RED,
     "杭州易环(E1)、尚云互联(E2)、江苏纽带智能(E3)、盘古自动化(E4)等"),
    ("仪表/传感器/仪器", "86家", "E4馆为主，直接竞品", HACH_BLUE,
     "上泰仪器、天信仪表、威格中国、余姚市仪表四厂等"),
    ("水处理/泵阀/膜材料", "69家", "E1/E5馆为主", HACH_TEAL,
     "世浦泰膜、中国水务投资、澳欣膜科技等"),
    ("大气治理设备", "大量", "E5/E6馆为主，未精确统计", HACH_GREEN,
     "兰山环保、杜尔涂装等"),
    ("环保工程/水务投资", "约30家", "E1/E2馆为主", HACH_ORANGE,
     "中国水务投资、北控水务等"),
    ("其他/未分类", "约688家", "数据解析率约60-70%", HACH_GRAY,
     "过滤材料、阀门、管道等"),
]
y_start = Inches(1.05)
for i, (cat, count, desc, color, examples) in enumerate(categories):
    y = y_start + Inches(i * 0.88)
    add_rect(slide4, Inches(0.4), y, Inches(0.08), Inches(0.7), color)
    add_text(slide4, Inches(0.6), y, Inches(3.0), Inches(0.45), cat, size=15, bold=True)
    add_text(slide4, Inches(3.6), y, Inches(1.0), Inches(0.45), count, size=15, bold=True, color=color)
    add_text(slide4, Inches(4.7), y, Inches(4.5), Inches(0.45), desc, size=13)
    add_text(slide4, Inches(0.6), y + Inches(0.4), Inches(12.2), Inches(0.4),
             "例：" + examples, size=11, color=HACH_GRAY)

# ============================================================
# SLIDE 5: 39家数字化跨界公司
# ============================================================
slide5 = prs.slides[4]
clear_slide(slide5)

add_rect(slide5, 0, 0, prs.slide_width, Inches(0.8), HACH_RED)
add_text(slide5, Inches(0.3), Inches(0.1), Inches(0.5), Inches(0.6),
         "04", size=28, bold=True, color=HACH_WHITE)
add_text(slide5, Inches(0.9), Inches(0.15), Inches(10), Inches(0.6),
         "39家数字化跨界公司 — 跨界打劫主力", size=26, bold=True, color=HACH_WHITE)

digital_exhibitors = [
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

cols = [digital_exhibitors[i:i+9] for i in range(0, len(digital_exhibitors), 9)]
col_x = [Inches(0.3), Inches(4.5), Inches(8.7)]

for ci, col in enumerate(cols):
    x = col_x[ci]
    for ri, (hall, name, booth) in enumerate(col):
        y = Inches(1.0) + Inches(ri * 0.62)
        add_rect(slide5, x, y + Pt(2), Inches(0.65), Inches(0.35), HACH_BLUE)
        add_text(slide5, x, y + Pt(2), Inches(0.65), Inches(0.35),
                 hall, size=10, bold=True, color=HACH_WHITE, align=PP_ALIGN.CENTER)
        add_text(slide5, x + Inches(0.72), y, Inches(3.5), Inches(0.5), name, size=12)
        add_text(slide5, x + Inches(0.72), y + Inches(0.32), Inches(3.5), Inches(0.3),
                 booth, size=10, color=HACH_GRAY)

add_rect(slide5, Inches(0.3), Inches(6.5), Inches(12.7), Inches(0.7), HACH_RED)
add_text(slide5, Inches(0.5), Inches(6.6), Inches(12.3), Inches(0.5),
         "核心威胁：这些公司具备云平台+端到端方案能力，可整合传感器+数据+云，侵蚀监测市场份额",
         size=13, bold=True, color=HACH_WHITE)

# ============================================================
# SLIDE 6: 波特五力
# ============================================================
slide6 = prs.slides[4]
clear_slide(slide6)

add_rect(slide6, 0, 0, prs.slide_width, Inches(0.8), HACH_BLUE)
add_text(slide6, Inches(0.3), Inches(0.1), Inches(0.5), Inches(0.6),
         "05", size=28, bold=True, color=HACH_WHITE)
add_text(slide6, Inches(0.9), Inches(0.15), Inches(10), Inches(0.6),
         "波特五力分析（基于972家展商数据）", size=26, bold=True, color=HACH_WHITE)

forces = [
    ("现有竞争者威胁", "高", "E4馆182家仪器仪表展商直接竞争，价格战激烈",
     "上泰仪器、天信仪表、威格中国等86家", HACH_RED),
    ("潜在新进入者威胁", "中", "39家数字化跨界公司具备云平台能力",
     "江苏纽带智能、杭州易环智能、尚云互联等", HACH_ORANGE),
    ("替代品威胁", "高", "在线监测替代实验室检测趋势加速",
     "便携式监测、无人机监测、卫星遥感等", HACH_RED),
    ("供应商议价能力", "中", "传感器/芯片供应链集中度较高",
     "水质传感器核心芯片仍依赖进口", HACH_ORANGE),
    ("购买者议价能力", "高", "水务/环保运营商整合，集中采购压价",
     "北控水务、中国水务等大型水务集团", HACH_RED),
]
y_start = Inches(1.05)
for i, (force, level, desc, examples, color) in enumerate(forces):
    y = y_start + Inches(i * 1.0)
    add_rect(slide6, Inches(0.4), y + Pt(3), Inches(0.08), Inches(0.55), color)
    add_text(slide6, Inches(0.6), y, Inches(3.5), Inches(0.45), force, size=15, bold=True)
    lvl_color = HACH_RED if level == "高" else HACH_ORANGE
    add_rect(slide6, Inches(4.1), y + Pt(3), Inches(0.5), Inches(0.35), lvl_color)
    add_text(slide6, Inches(4.1), y + Pt(3), Inches(0.5), Inches(0.35),
             level, size=12, bold=True, color=HACH_WHITE, align=PP_ALIGN.CENTER)
    add_text(slide6, Inches(4.75), y, Inches(5.0), Inches(0.45), desc, size=14)
    add_text(slide6, Inches(0.6), y + Inches(0.42), Inches(12.2), Inches(0.4),
             "证据：" + examples, size=11, color=HACH_GRAY)

# ============================================================
# SLIDE 7: SWOT
# ============================================================
slide7 = prs.slides[4]
clear_slide(slide7)

add_rect(slide7, 0, 0, prs.slide_width, Inches(0.8), HACH_BLUE)
add_text(slide7, Inches(0.3), Inches(0.1), Inches(0.5), Inches(0.6),
         "06", size=28, bold=True, color=HACH_WHITE)
add_text(slide7, Inches(0.9), Inches(0.15), Inches(10), Inches(0.6),
         "SWOT分析（基于展商数据的事实性观察）", size=26, bold=True, color=HACH_WHITE)

# S
add_rect(slide7, Inches(0.3), Inches(0.95), Inches(6.3), Inches(0.45), HACH_BLUE)
add_text(slide7, Inches(0.4), Inches(0.97), Inches(1.0), Inches(0.4),
         "S 优势", size=15, bold=True, color=HACH_WHITE)
add_text(slide7, Inches(0.4), Inches(1.45), Inches(6.0), Inches(0.6),
         "水质分析仪器有较高品牌认知，在E4-D08/E08有独立展位", size=13)
add_text(slide7, Inches(0.4), Inches(2.0), Inches(6.0), Inches(0.6),
         "IMS产品线覆盖水质监测全参数，E3-C12展位位于监测与检测馆", size=13)

# W
add_rect(slide7, Inches(6.8), Inches(0.95), Inches(6.3), Inches(0.45), HACH_ORANGE)
add_text(slide7, Inches(6.9), Inches(0.97), Inches(1.0), Inches(0.4),
         "W 劣势", size=15, bold=True, color=HACH_WHITE)
add_text(slide7, Inches(6.9), Inches(1.45), Inches(6.0), Inches(0.6),
         "E4馆大量国内仪表厂商价格显著低于哈希（同在E4馆）", size=13)
add_text(slide7, Inches(6.9), Inches(2.0), Inches(6.0), Inches(0.6),
         "39家数字化跨界公司已在云平台层面布局，可能先于哈希建立 IMS 能力", size=13)

# O
add_rect(slide7, Inches(0.3), Inches(2.9), Inches(6.3), Inches(0.45), HACH_GREEN)
add_text(slide7, Inches(0.4), Inches(2.92), Inches(1.0), Inches(0.4),
         "O 机会", size=15, bold=True, color=HACH_WHITE)
add_text(slide7, Inches(0.4), Inches(3.4), Inches(6.0), Inches(0.6),
         "E3馆（监测与检测）展商数据不完整，存在未被识别的市场空白", size=13)
add_text(slide7, Inches(0.4), Inches(3.95), Inches(6.0), Inches(0.6),
         "传统仪器仪表展商多为单一参数产品，全参数覆盖仍是差异化优势", size=13)

# T
add_rect(slide7, Inches(6.8), Inches(2.9), Inches(6.3), Inches(0.45), HACH_RED)
add_text(slide7, Inches(6.9), Inches(2.92), Inches(1.0), Inches(0.4),
         "T 威胁", size=15, bold=True, color=HACH_WHITE)
add_text(slide7, Inches(6.9), Inches(3.4), Inches(6.0), Inches(0.6),
         "江苏纽带智能(E3-G61)等提供端到端IMS方案，整合传感器+云平台", size=13)
add_text(slide7, Inches(6.9), Inches(3.95), Inches(6.0), Inches(0.6),
         "数字化跨界公司39家，可基于云平台提供打包监测解决方案", size=13)

add_text(slide7, Inches(0.4), Inches(4.8), Inches(12.5), Inches(0.5),
         "注：以上SWOT条目均基于可验证的展商数据事实。E+H、ABB、西门子、横河等未在OCR数据中检索到。",
         size=11, color=HACH_GRAY)

# ============================================================
# SLIDE 8: 90天行动建议
# ============================================================
slide8 = prs.slides[4]
clear_slide(slide8)

add_rect(slide8, 0, 0, prs.slide_width, Inches(0.8), HACH_BLUE)
add_text(slide8, Inches(0.3), Inches(0.1), Inches(0.5), Inches(0.6),
         "07", size=28, bold=True, color=HACH_WHITE)
add_text(slide8, Inches(0.9), Inches(0.15), Inches(10), Inches(0.6),
         "90天行动建议", size=26, bold=True, color=HACH_WHITE)

actions = [
    ("30天", "建立39家数字化跨界公司竞争情报档案",
     "梳理每家公司的云平台架构、产品参数、目标客户，评估与IMS重叠度", HACH_RED),
    ("30天", "重点分析江苏纽带智能(E3-G61)等端到端方案公司",
     "评估其是否已推出与IMS直接竞争的产品，输出内部评估报告", HACH_ORANGE),
    ("60天", "完成E4馆182家展商竞品分类",
     "区分直接竞品（仪器仪表）、渠道合作方、潜在合作伙伴，拜访重点展商", HACH_BLUE),
    ("60天", "与E4馆国内仪表厂商建立联系",
     "了解其价格体系和产品路线图，为应对价格竞争做准备", HACH_TEAL),
    ("90天", "发布IMS产品线竞争力评估内部报告",
     "基于展商数据和客户沟通，评估IMS产品在监测市场的竞争地位", HACH_GREEN),
    ("90天", "与水务/环保运营商客户验证价格压力",
     "向大型水务集团客户了解采购趋势，验证展会观察到的价格压力", HACH_YELLOW),
]
y_start = Inches(1.0)
for i, (timeline, action, detail, color) in enumerate(actions):
    y = y_start + Inches(i * 0.88)
    add_rect(slide8, Inches(0.3), y + Pt(2), Inches(0.9), Inches(0.45), color)
    add_text(slide8, Inches(0.3), y + Pt(2), Inches(0.9), Inches(0.45),
             timeline, size=12, bold=True, color=HACH_WHITE, align=PP_ALIGN.CENTER)
    add_text(slide8, Inches(1.35), y, Inches(5.0), Inches(0.5), action, size=14, bold=True)
    add_text(slide8, Inches(1.35), y + Inches(0.42), Inches(11.5), Inches(0.45),
             detail, size=12, color=HACH_GRAY)

# ============================================================
# SLIDE 9: 核心结论
# ============================================================
slide9 = prs.slides[5]
clear_slide(slide9)

add_rect(slide9, 0, 0, prs.slide_width, prs.slide_height, HACH_LIGHT)
add_rect(slide9, 0, 0, Inches(0.12), prs.slide_height, HACH_BLUE)
add_rect(slide9, Inches(0.5), Inches(6.2), Inches(5), Pt(4), HACH_ORANGE)

add_text(slide9, Inches(0.6), Inches(0.8), Inches(12), Inches(0.8),
         "核心结论", size=36, bold=True, color=HACH_DARK)

conclusions = [
    ("最大威胁", "不是传统仪表同行，而是39家数字化跨界公司（跨界打劫）",
     HACH_RED, "江苏纽带智能、尚云互联、杭州易环智能、E20环境平台等"),
    ("直接竞争", "E4馆182家仪器仪表展商构成直接竞争，但多为单一参数产品",
     HACH_BLUE, "优势在于全参数覆盖和品牌信任度"),
    ("跨界侵蚀", "39家数字化公司具备云平台+端到端方案能力，可能侵蚀IMS核心市场",
     HACH_ORANGE, "这些公司整合传感器+云平台，对IMS产品线威胁最大"),
    ("数据缺口", "E3馆（监测与检测）数据不完整，需进一步补充E3馆完整展商数据",
     HACH_TEAL, "展位在E3-C12，展会期间可实地核实E3馆展商"),
]
y_start = Inches(1.8)
for i, (label, text, color, example) in enumerate(conclusions):
    y = y_start + Inches(i * 0.95)
    add_rect(slide9, Inches(0.5), y, Inches(1.5), Inches(0.4), color)
    add_text(slide9, Inches(0.5), y, Inches(1.5), Inches(0.4),
             label, size=13, bold=True, color=HACH_WHITE, align=PP_ALIGN.CENTER)
    add_text(slide9, Inches(2.15), y, Inches(10.7), Inches(0.5), text, size=15, bold=True)
    add_text(slide9, Inches(2.15), y + Inches(0.38), Inches(10.7), Inches(0.4),
             example, size=12, color=HACH_GRAY)

add_text(slide9, Inches(0.5), Inches(6.8), Inches(12), Inches(0.4),
         "IMS产品线  |  2026环博会  |  数据来源：微信公众号公开OCR数据",
         size=11, color=HACH_GRAY)

prs.save('/home/agentuser/IMS竞争分析报告_v9.pptx')
print("v9 saved!")
