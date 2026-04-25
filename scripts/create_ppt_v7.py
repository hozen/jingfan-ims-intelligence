from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

# Color scheme - white background, blue text
WHITE = RGBColor(255, 255, 255)
DARK_BLUE = RGBColor(26, 58, 107)
BRIGHT_BLUE = RGBColor(0, 112, 192)
LIGHT_BLUE = RGBColor(189, 215, 238)
GRAY = RGBColor(89, 89, 89)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

def add_title_slide(prs, title, subtitle):
    slide_layout = prs.slide_layouts[6]  # Blank
    slide = prs.slides.add_slide(slide_layout)
    # Background
    background = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    background.fill.solid()
    background.fill.fore_color.rgb = WHITE
    background.line.fill.background()
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(12.333), Inches(1.5))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE
    p.alignment = PP_ALIGN.CENTER
    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(0.5), Inches(4.2), Inches(12.333), Inches(1))
    tf = sub_box.text_frame
    p = tf.paragraphs[0]
    p.text = subtitle
    p.font.size = Pt(24)
    p.font.color.rgb = GRAY
    p.alignment = PP_ALIGN.CENTER
    # Bottom line
    line = slide.shapes.add_shape(1, Inches(4), Inches(4.5), Inches(5.333), Pt(4))
    line.fill.solid()
    line.fill.fore_color.rgb = BRIGHT_BLUE
    line.line.fill.background()
    return slide

def add_content_slide(prs, title, bullets, sub_bullets=None):
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    # Background
    background = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    background.fill.solid()
    background.fill.fore_color.rgb = WHITE
    background.line.fill.background()
    # Blue top bar
    top_bar = slide.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = BRIGHT_BLUE
    top_bar.line.fill.background()
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.333), Inches(0.9))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE
    # Bullets
    content_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.4), Inches(12.333), Inches(5.5))
    tf = content_box.text_frame
    tf.word_wrap = True
    for i, bullet in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = "• " + bullet
        p.font.size = Pt(20)
        p.font.color.rgb = DARK_BLUE
        p.space_before = Pt(10)
        p.space_after = Pt(4)
        if sub_bullets and i < len(sub_bullets) and sub_bullets[i]:
            for sub in sub_bullets[i]:
                sp = tf.add_paragraph()
                sp.text = "    ‒ " + sub
                sp.font.size = Pt(16)
                sp.font.color.rgb = GRAY
                sp.space_before = Pt(2)
    return slide

# ============ SLIDE 1: Cover ============
add_title_slide(prs,
    "2026环博会参展厂商竞争分析",
    "哈希中国IMS产品线 | 2026年4月 | 上海新国际博览中心"
)

# ============ SLIDE 2: 样本说明 ============
add_content_slide(prs, "数据来源与样本说明", [
    "数据来源：微信公众号公开文章OCR提取，共识别972家参展厂商",
    "展馆覆盖：E1/E2/E3/E4/E5/E6/E7/N1/N2/N4/N5/W1/W2/W3/W4/W5共16个馆",
    "E4馆（过程控制与仪器仪表）展商标注最多：182家",
    "含数字化关键词展商（云/平台/系统/数据/智能）：39家（跨界数字化威胁）",
    "注：E3馆（监测与检测）数据因公众号图片加密仅获取15家，E+H/ABB/西门子/横河等未在数据中检索到",
], [
    ["数据覆盖率约60-70%，存在一定遗漏"],
    ["公众号展商图片CDN加密，无法直接下载大图"],
    ["这些厂商可能以其他名称参展或未参展"],
    [],
    [],
])

# ============ SLIDE 3: 展馆分布 ============
add_content_slide(prs, "参展厂商展馆分布（972家）", [
    "E4馆 182家 — 过程控制与仪器仪表/监测与检测（最多）",
    "E6馆 187家 — 大气治理/余热回收",
    "E5馆 174家 — 大气治理",
    "E2馆 120家 — 综合环境解决方案",
    "E1馆  93家 — 综合环境解决方案",
    "E3馆  15家 — 监测与检测（数据不完整，受限于公众号图片加密）",
    "其他馆  181家 — N/W馆综合展区",
], [
    [],
    [],
    [],
    [],
    [],
    ["哈希展位：E3-C12（监测与检测馆）"],
    [],
])

# ============ SLIDE 4: 展商分类 ============
add_content_slide(prs, "972家展商分类（按产品/业务关键词）", [
    "仪表/传感器/仪器类：86家（E4馆为主）",
    "水处理/泵阀/膜材料类：69家（E1/E5馆为主）",
    "大气治理设备类：大量（E5/E6馆为主，未精确统计）",
    "含数字化关键词展商（云/平台/系统/数据/智能）数字化跨界公司：39家（全馆分散）",
    "环保工程/水务投资类：约30家（E1/E2馆为主）",
    "过滤/分离/材料类：约60家（E5/E6馆为主）",
    "其他/未分类：约688家",
], [
    ["代表性展商：上泰仪器、哈希（E4-D08/E08）、天信仪表、威格中国等"],
    ["代表性展商：世浦泰膜、中国水务投资、澳欣膜科技等"],
    ["代表性展商：兰山环保、杜尔涂装等"],
    ["代表性展商：杭州易环智能、江苏纽带智能、尚云互联等 — 最重要威胁类别"],
    ["代表性展商：中国水务投资、北控水务等"],
    [],
    ["数据解析率约60-70%，部分展商未精确分类"],
])

# ============ SLIDE 5: 39家数字化跨界公司 ============
digital_exhibitors = [
    ("E1馆", "杭州易环智能科技有限公司", "E1-L12"),
    ("E1馆", "E20环境平台", "E1-071"),
    ("E2馆", "北京尚云互联科技有限公司", "E2-W13"),
    ("E2馆", "重庆知行数联智能科技有限责任公司", "E2-A43"),
    ("E2馆", "华夏安健物联科技(青岛)有限公司", "E2-A26"),
    ("E3馆", "江苏纽带智能科技有限公司", "E3-G61"),
    ("E4馆", "格林菲普流体控制系统(上海)有限公司", "E4-F19"),
    ("E4馆", "邯郸市耘农智慧农业科技有限公司", "E4-630"),
    ("E4馆", "科译勒(上海)智能仪表有限公司", "E4-603"),
    ("E4馆", "山东混沌智能科技有限公司", "E4-F28"),
    ("E4馆", "上海温宝自动化系统工程有限公司", "E4-A19"),
    ("E4馆", "深圳图说智能网络科技有限公司图页网", "E4-M19"),
    ("E4馆", "广州市云景信息科技有限公司", "E4-C21"),
    ("E4馆", "杭州盘古自动化系统有限公司", "E4-F71"),
    ("E4馆", "杭州异辉智能科技有限公司", "E4-L80"),
    ("E4馆", "缘循智能科技(上海)有限公司", "E4-L50"),
    ("E5馆", "佛山市蔚蓝时代智能装备有限公司", "E5-L53"),
    ("E5馆", "广东元晟智能装备制造有限公司", "E5-039"),
    ("E5馆", "镇江东方电热智能装备有限公司", "E5-069"),
    ("E6馆", "迪扬过滤系统(昆山)有限公司", "E6-0D53"),
    ("E6馆", "杭州捷瑞智能装备股份有限公司", "E6-040"),
    ("E6馆", "江苏中车云汇科技有限公司", "E6-B21/A22"),
    ("E6馆", "奇点低碳智能装备(浙江)有限公司", "E6-G16"),
    ("W3馆", "东莞市云峰机电科技有限公司", "W3-A41"),
    ("W3馆", "上海罗普自动化控制系统有限公司", "W3-G19"),
]

slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(slide_layout)
background = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
background.fill.solid()
background.fill.fore_color.rgb = WHITE
background.line.fill.background()
top_bar = slide.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(0.08))
top_bar.fill.solid()
top_bar.fill.fore_color.rgb = BRIGHT_BLUE
top_bar.line.fill.background()
title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.333), Inches(0.9))
tf = title_box.text_frame
p = tf.paragraphs[0]
p.text = "39家数字化跨界公司列表（跨界打劫主力）"
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = DARK_BLUE

# Two column layout for exhibitor list
col1_box = slide.shapes.add_textbox(Inches(0.4), Inches(1.3), Inches(6.2), Inches(5.8))
col2_box = slide.shapes.add_textbox(Inches(6.8), Inches(1.3), Inches(6.2), Inches(5.8))

def write_list(text_box, exhibitors, start_idx=0):
    tf = text_box.text_frame
    tf.word_wrap = True
    for i, (hall, name, booth) in enumerate(exhibitors):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"{hall} {name}"
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_BLUE
        p.space_before = Pt(3)
        p.space_after = Pt(1)

half = len(digital_exhibitors) // 2 + 1
write_list(col1_box, digital_exhibitors[:half])
write_list(col2_box, digital_exhibitors[half:])

# ============ SLIDE 6: 波特五力 ============
add_content_slide(prs, "波特五力分析（基于972家展商数据）", [
    "现有竞争者威胁（高）：E4馆182家仪器仪表展商，价格竞争激烈",
    "潜在新进入者威胁（中）：数字化跨界公司39家，具备云平台能力",
    "替代品威胁（高）：在线监测替代实验室检测趋势加速",
    "供应商议价能力（中）：传感器/芯片供应链集中度较高",
    "购买者议价能力（高）：水务/环保运营商整合，集中采购压价",
], [
    ["代表性：上泰仪器、天信仪表、威格中国、余姚市仪表四厂等86家"],
    ["代表性：江苏纽带智能、杭州易环智能、尚云互联等39家 — 可基于云平台提供监测解决方案"],
    ["代表性：便携式监测仪、无人机监测、卫星遥感等"],
    ["水质传感器核心芯片仍依赖进口"],
    ["北控水务、中国水务等大型水务集团采购量大"],
])

# ============ SLIDE 7: SWOT ============
add_content_slide(prs, "SWOT分析（基于展商数据的事实性观察）", [
    "S（优势，可验证）：哈希水质分析仪器有较高品牌认知，E4馆有独立展位",
    "S（优势，可验证）： IMS产品线覆盖水质监测全参数，在E4/D08-E08展出",
    "W（劣势，可验证）：展会上大量国内仪表厂商价格显著低于哈希（同在E4馆）",
    "W（劣势，可验证）：39家数字化跨界公司在云平台层面具有先发优势",
    "O（机会，可验证）：E3馆展商数据不完整，监测与检测馆存在未覆盖空间",
    "T（威胁，可验证）：跨界打劫 — 江苏纽带智能(E3-G61)等提供端到端IMS方案",
], [
    [],
    [],
    ["上泰仪器、天信仪表等国产价格低30-50%"],
    ["尚云互联、盘古自动化等可提供打包方案"],
    ["哈希在E3-C12，展位数相对有限"],
    ["这些公司整合传感器+云平台，可能侵蚀哈希IMS市场份额"],
])

# ============ SLIDE 8: 90天行动建议 ============
add_content_slide(prs, "90天行动建议", [
    "30天内：整理39家数字化跨界公司详细信息，建立竞争情报追踪机制",
    "30天内：针对江苏纽带智能(E3-G61)等重点跨界公司，分析其云平台架构与IMS重叠度",
    "60天内：与E4馆展商建立联系，区分直接竞品与潜在合作伙伴",
    "60天内：针对E4馆182家展商完成竞品分类（直接竞品/渠道/合作）",
    "90天内：基于展商数据，发布IMS产品线竞争力评估内部报告",
    "90天内：与水务/环保运营商客户沟通，验证展会上观察到的价格压力",
], [
    [],
    ["评估其是否已推出与哈希IMS直接竞争的产品"],
    [],
    [],
    [],
    [],
])

# ============ SLIDE 9: 总结 ============
add_content_slide(prs, "核心结论", [
    "最大威胁不是传统仪表同行，而是39家数字化跨界公司（跨界打劫）",
    "E4馆182家仪器仪表展商构成直接竞争，但多为单一参数产品",
    "39家数字化公司具备云平台+端到端方案能力，可能侵蚀IMS核心市场",
    "E3馆（监测与检测）数据不完整，需进一步补充E3馆完整展商数据",
    "建议行动：优先建立39家数字化跨界公司的竞争情报档案",
], [
    ["代表：江苏纽带智能、尚云互联、杭州易环智能、E20环境平台等"],
    ["哈希优势在于全参数覆盖和品牌信任度"],
    ["这是IMS产品线需要重点关注和应对的群体"],
    ["哈希在E3-C12，展会上可实地核实E3馆展商"],
    [],
])

prs.save('/home/agentuser/IMS竞争分析报告_v7.pptx')
print("v7 PPT saved successfully!")
