#!/usr/bin/env python3
"""
IMS × AOA工艺改造机会分析 PPT
Design: 纯白底/三色(蓝0,126,181|深灰77,77,77|浅灰153,153,153)/微软雅黑
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# Color palette (Hach)
BLUE = RGBColor(0, 126, 181)
DARK_GRAY = RGBColor(77, 77, 77)
LIGHT_GRAY = RGBColor(153, 153, 153)
WHITE = RGBColor(255, 255, 255)

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

def add_shape_rect(slide, x, y, w, h, fill_color=None, line_color=None, line_width=None):
    from pptx.util import Pt
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    shape = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
        if line_width:
            shape.line.width = Pt(line_width)
    else:
        shape.line.fill.background()
    return shape

def add_text_box(slide, text, x, y, w, h, font_size=14, bold=False,
                 color=DARK_GRAY, align=PP_ALIGN.LEFT, font_face="微软雅黑",
                 wrap=True, italic=False):
    txBox = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font_face
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.italic = italic
    return txBox

def add_text_box_lines(slide, lines, x, y, w, h, font_size=14,
                        bold=False, color=DARK_GRAY, align=PP_ALIGN.LEFT,
                        font_face="微软雅黑", line_spacing=None):
    """lines: list of (text, bold, italic) tuples or plain strings"""
    txBox = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = txBox.text_frame
    tf.word_wrap = True
    first = True
    for item in lines:
        if isinstance(item, str):
            txt, b, i = item, bold, False
        else:
            txt, b, i = item
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.alignment = align
        if line_spacing:
            p.line_spacing = Pt(line_spacing)
        run = p.add_run()
        run.text = txt
        run.font.name = font_face
        run.font.size = Pt(font_size)
        run.font.bold = b
        run.font.color.rgb = color
        run.font.italic = i
    return txBox

def add_bullet_list(slide, items, x, y, w, h, font_size=13, color=DARK_GRAY,
                     indent=True, font_face="微软雅黑"):
    """items: list of strings or (text, level) tuples"""
    txBox = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = txBox.text_frame
    tf.word_wrap = True
    first = True
    for item in items:
        if isinstance(item, str):
            txt, level = item, 0
        else:
            txt, level = item
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = txt
        run.font.name = font_face
        run.font.size = Pt(font_size)
        run.font.color.rgb = color
        if indent and level == 0:
            p.bullet = None
    return txBox

# ─────────────────────────────────────────────────────────────
# SLIDE 1: Title
# ─────────────────────────────────────────────────────────────
s = prs.slides.add_slide(prs.slide_layouts[6])  # blank

# Left accent bar
add_shape_rect(s, 0, 0, 0.12, 7.5, fill_color=BLUE)

# Main title
add_text_box(s, "IMS × AOA工艺改造", 0.5, 1.6, 12, 1.0,
             font_size=42, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)
add_text_box(s, "机会分析", 0.5, 2.6, 12, 0.9,
             font_size=42, bold=True, color=BLUE, align=PP_ALIGN.LEFT)

# Subtitle
add_text_box(s, "为什么AOA工艺改造给IMS带来了仪表销售没有的新机会？",
             0.5, 3.8, 11, 0.6,
             font_size=20, bold=False, color=LIGHT_GRAY, align=PP_ALIGN.LEFT)

# Divider line
add_shape_rect(s, 0.5, 4.5, 12.5, 0.03, fill_color=LIGHT_GRAY)

# Source and date
add_text_box(s, "数据来源：中国水协2026年会追踪  |  研究日期：2026-04-22",
             0.5, 4.7, 12, 0.4,
             font_size=11, color=LIGHT_GRAY, align=PP_ALIGN.LEFT)

# Bottom badge
add_shape_rect(s, 0.5, 5.2, 3.2, 0.55, fill_color=BLUE)
add_text_box(s, "彭永臻（中国工程院院士/北京工业大学）", 0.6, 5.25, 3.1, 0.45,
             font_size=12, bold=False, color=WHITE, align=PP_ALIGN.LEFT)

add_text_box(s, "Hach中国IMS产品线", 0.5, 5.9, 12, 0.4,
             font_size=11, color=LIGHT_GRAY, align=PP_ALIGN.LEFT)

# ─────────────────────────────────────────────────────────────
# SLIDE 2: 核心问题
# ─────────────────────────────────────────────────────────────
s = prs.slides.add_slide(prs.slide_layouts[6])

# Top bar
add_shape_rect(s, 0, 0, 13.33, 0.08, fill_color=BLUE)

add_text_box(s, "核心问题", 0.5, 0.35, 12, 0.6,
             font_size=28, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)

# Question box
add_shape_rect(s, 0.5, 1.1, 12.33, 1.3, fill_color=RGBColor(245, 248, 250))
add_text_box(s, "AOA工艺改造给IMS带来了哪些\nAAO时代没有的、必须通过IMS才能解决的新需求？",
             0.7, 1.2, 12, 1.1,
             font_size=22, bold=True, color=BLUE, align=PP_ALIGN.LEFT)

# Two columns
# Left: AAO
add_shape_rect(s, 0.5, 2.65, 5.9, 4.4, fill_color=RGBColor(250, 250, 250))
add_shape_rect(s, 0.5, 2.65, 5.9, 0.5, fill_color=DARK_GRAY)
add_text_box(s, "AAO时代：仪表是", 0.6, 2.68, 5.7, 0.45,
             font_size=16, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
add_text_box(s, "记录工具", 0.6, 3.25, 5.7, 0.6,
             font_size=28, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)

add_text_box_lines(s, [
    ("• 记录数据、合规迎检", False, False),
    ("• 人工巡检，1-2次/天", False, False),
    ("• 仪表之间相互孤立", False, False),
    ("• 靠经验判断DO高低", False, False),
    ("• 报警时无法判断原因", False, False),
], 0.6, 3.9, 5.7, 3.0, font_size=13, color=DARK_GRAY)

# Right: AOA
add_shape_rect(s, 6.9, 2.65, 5.93, 4.4, fill_color=RGBColor(250, 250, 250))
add_shape_rect(s, 6.9, 2.65, 5.93, 0.5, fill_color=BLUE)
add_text_box(s, "AOA时代：仪表是", 7.0, 2.68, 5.7, 0.45,
             font_size=16, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
add_text_box(s, "控制工具", 7.0, 3.25, 5.7, 0.6,
             font_size=28, bold=True, color=BLUE, align=PP_ALIGN.LEFT)

add_text_box_lines(s, [
    ("• 高频数据，5-15分钟/次", False, False),
    ("• 多参数联动分析", False, False),
    ("• 异常根因诊断", False, False),
    ("• 数据驱动工艺优化", False, False),
    ("• 仪表故障 vs 工艺异常", False, False),
], 7.0, 3.9, 5.7, 3.0, font_size=13, color=DARK_GRAY)

# Arrow
add_text_box(s, "→", 6.45, 4.4, 0.5, 0.8,
             font_size=36, bold=True, color=BLUE, align=PP_ALIGN.CENTER)

# Bottom note
add_text_box(s, "彭永臻报告：节能20% · 减污泥量 · 降N₂O碳排放 · TN<3.8mg/L（14.3°C低温）",
             0.5, 7.1, 12.33, 0.35,
             font_size=11, color=LIGHT_GRAY, align=PP_ALIGN.LEFT)

# ─────────────────────────────────────────────────────────────
# SLIDE 3: 工艺原理
# ─────────────────────────────────────────────────────────────
s = prs.slides.add_slide(prs.slide_layouts[6])

add_shape_rect(s, 0, 0, 13.33, 0.08, fill_color=BLUE)

add_text_box(s, "AOA vs AAO：工艺结构差异", 0.5, 0.35, 12, 0.6,
             font_size=28, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)

# AAO flow
add_shape_rect(s, 0.5, 1.2, 12.33, 0.7, fill_color=RGBColor(245, 248, 250))
add_text_box(s, "传统AAO：厌氧 → 缺氧 → 好氧 → 沉淀池 → 出水",
             0.6, 1.25, 12, 0.6, font_size=15, bold=False, color=DARK_GRAY, align=PP_ALIGN.LEFT)

# AOA flow
add_shape_rect(s, 0.5, 2.05, 12.33, 0.7, fill_color=RGBColor(232, 244, 252))
add_text_box(s, "AOA：       厌氧 → 好氧 → 缺氧 → 沉淀池 → 出水",
             0.6, 2.1, 12, 0.6, font_size=15, bold=True, color=BLUE, align=PP_ALIGN.LEFT)

# Core insight box
add_shape_rect(s, 0.5, 2.95, 12.33, 0.75, fill_color=BLUE)
add_text_box(s, "核心差异：好氧区和缺氧区顺序互换 → 曝气控制成为整个工艺的神经中枢",
             0.6, 3.0, 12, 0.65, font_size=15, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

# Three advantages
add_text_box(s, "彭永臻报告的三大优势（全都依赖精确曝气控制）", 0.5, 3.9, 12, 0.5,
             font_size=14, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)

adv_data = [
    ("节能", "曝气量精确到最优值\n能耗显著下降", RGBColor(0, 126, 181)),
    ("减排", "过量曝气→N₂O支路激活\n精确曝气→N₂O排放降低", RGBColor(0, 100, 150)),
    ("深度脱氮", "TN<3.8mg/L（14.3°C低温）\n微小波动直接导致超标", RGBColor(0, 70, 110)),
]

for i, (title, desc, col) in enumerate(adv_data):
    bx = 0.5 + i * 4.2
    add_shape_rect(s, bx, 4.45, 3.9, 2.5, fill_color=RGBColor(250, 250, 250))
    add_shape_rect(s, bx, 4.45, 3.9, 0.5, fill_color=col)
    add_text_box(s, title, bx + 0.1, 4.48, 3.7, 0.45,
                 font_size=16, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    add_text_box(s, desc, bx + 0.15, 5.05, 3.6, 1.8,
                 font_size=12, color=DARK_GRAY, align=PP_ALIGN.LEFT)

# Key contradiction
add_text_box(s, "关键矛盾：最优DO值不是固定值——随进水负荷实时变化",
             0.5, 7.1, 12.33, 0.35,
             font_size=12, bold=True, color=BLUE, align=PP_ALIGN.LEFT)

# ─────────────────────────────────────────────────────────────
# SLIDE 4: 新需求① 多参数联动
# ─────────────────────────────────────────────────────────────
s = prs.slides.add_slide(prs.slide_layouts[6])

add_shape_rect(s, 0, 0, 13.33, 0.08, fill_color=BLUE)

# Badge
add_shape_rect(s, 0.5, 0.35, 0.65, 0.65, fill_color=BLUE)
add_text_box(s, "①", 0.5, 0.35, 0.65, 0.65,
             font_size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

add_text_box(s, "新需求：多参数联动的高频数据", 1.3, 0.4, 11, 0.6,
             font_size=26, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)

add_text_box(s, "AAO时代没有 · AOA时代必须", 1.3, 0.9, 11, 0.4,
             font_size=13, color=LIGHT_GRAY, align=PP_ALIGN.LEFT)

# Question
add_shape_rect(s, 0.5, 1.5, 12.33, 0.9, fill_color=RGBColor(245, 248, 250))
add_text_box(s, "当前DO=2.0mg/L，是高了还是低了？",
             0.7, 1.55, 12, 0.4, font_size=20, bold=True, color=BLUE, align=PP_ALIGN.LEFT)
add_text_box(s, "答案是"取决于其他参数"——单一DO数据没有意义",
             0.7, 1.95, 12, 0.4, font_size=13, color=DARK_GRAY, align=PP_ALIGN.LEFT)

# Two scenarios
scenario_data = [
    ("情景A：NH₃-N=0.5mg/L（充分硝化）", "DO=2.0 → 高了，浪费曝气，增加N₂O",
     RGBColor(230, 240, 250), BLUE, "↓ 降低曝气"),
    ("情景B：NH₃-N=15mg/L（高负荷冲击）", "DO=2.0 → 低了，硝化不完全，TN超标",
     RGBColor(255, 240, 230), RGBColor(180, 60, 0), "↑ 增加曝气"),
]

for i, (cond, result, bg, col, action) in enumerate(scenario_data):
    bx = 0.5 + i * 6.4
    add_shape_rect(s, bx, 2.6, 6.1, 1.5, fill_color=bg)
    add_shape_rect(s, bx, 2.6, 0.06, 1.5, fill_color=col)
    add_text_box(s, cond, bx + 0.2, 2.65, 5.7, 0.5,
                 font_size=13, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)
    add_text_box(s, result, bx + 0.2, 3.1, 5.7, 0.5,
                 font_size=13, color=col, align=PP_ALIGN.LEFT)
    add_text_box(s, action, bx + 0.2, 3.55, 5.7, 0.45,
                 font_size=15, bold=True, color=col, align=PP_ALIGN.LEFT)

# Required instruments
add_text_box(s, "需要的仪表组合（高频数据，5-15分钟/次）", 0.5, 4.3, 12, 0.4,
             font_size=13, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)

instruments = [
    ("LDO II溶解氧传感器", "好氧区出口\n多点布置", BLUE),
    ("NH6000sc氨氮监测", "进水端+好氧区出口\n曝气前馈信号", DARK_GRAY),
    ("NT6800总氮监测", "出水端\n深度脱氮达标保障", BLUE),
    ("进水流量计", "进水流量\n碳氮比判断", DARK_GRAY),
]

for i, (name, desc, col) in enumerate(instruments):
    bx = 0.5 + i * 3.15
    add_shape_rect(s, bx, 4.75, 2.95, 1.55, fill_color=RGBColor(250, 250, 250))
    add_shape_rect(s, bx, 4.75, 2.95, 0.45, fill_color=col)
    add_text_box(s, name, bx + 0.1, 4.77, 2.75, 0.4,
                 font_size=11, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    add_text_box(s, desc, bx + 0.1, 5.25, 2.75, 0.95,
                 font_size=11, color=DARK_GRAY, align=PP_ALIGN.LEFT)

add_text_box(s, "单台仪表只能告诉运行人员"DO是多少"——IMS能告诉"DO是否最优"",
             0.5, 6.5, 12.33, 0.45,
             font_size=13, bold=True, color=BLUE, align=PP_ALIGN.LEFT)

# ─────────────────────────────────────────────────────────────
# SLIDE 5: 新需求② 异常根因诊断
# ─────────────────────────────────────────────────────────────
s = prs.slides.add_slide(prs.slide_layouts[6])

add_shape_rect(s, 0, 0, 13.33, 0.08, fill_color=BLUE)

add_shape_rect(s, 0.5, 0.35, 0.65, 0.65, fill_color=BLUE)
add_text_box(s, "②", 0.5, 0.35, 0.65, 0.65,
             font_size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

add_text_box(s, "新需求：异常根因诊断", 1.3, 0.4, 11, 0.6,
             font_size=26, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)
add_text_box(s, "同样的DO报警，四个不同原因，两类解决方案", 1.3, 0.9, 11, 0.4,
             font_size=13, color=LIGHT_GRAY, align=PP_ALIGN.LEFT)

# The alarm
add_shape_rect(s, 0.5, 1.5, 12.33, 0.65, fill_color=RGBColor(255, 240, 230))
add_shape_rect(s, 0.5, 1.5, 0.08, 0.65, fill_color=RGBColor(200, 50, 0))
add_text_box(s, "⚠ 报警：好氧区DO=0.3mg/L（过低）", 0.7, 1.55, 12, 0.55,
             font_size=17, bold=True, color=RGBColor(180, 50, 0), align=PP_ALIGN.LEFT)

# Four scenarios
header_cols = ["场景", "NH₃-N数据", "TN数据", "原因判断", "解决方案"]
col_widths = [1.8, 2.2, 2.0, 3.5, 2.8]
col_xs = [0.5]
for w in col_widths[:-1]:
    col_xs.append(col_xs[-1] + w + 0.08)

# Header row
for i, (hdr, cx, cw) in enumerate(zip(header_cols, col_xs, col_widths)):
    add_shape_rect(s, cx, 2.3, cw, 0.4, fill_color=BLUE)
    add_text_box(s, hdr, cx + 0.08, 2.32, cw - 0.1, 0.35,
                 font_size=11, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

rows = [
    ("情况A", "NH₃-N=12mg/L↑", "TN缓慢↑", "工艺：进水负荷升高，曝气来不及", "调整曝气策略", RGBColor(240, 248, 255)),
    ("情况B", "NH₃-N=0.3mg/L↓", "TN稳定", "仪表：DO传感器零点漂移", "校准/更换传感器", RGBColor(240, 255, 240)),
    ("情况C", "NH₃-N=8mg/L↑", "TN逐步↑", "工艺：生物活性下降，污泥老化", "调整污泥龄/增加曝气", RGBColor(255, 248, 240)),
    ("情况D", "NH₃-N突降至0", "TN突降", "仪表：NH₃-N传感器故障", "检查/更换传感器", RGBColor(255, 245, 245)),
]

for ri, (scene, nh, tn, cause, solution, bg) in enumerate(rows):
    ry = 2.72 + ri * 0.65
    add_shape_rect(s, 0.5, ry, 12.33, 0.62, fill_color=bg)
    vals = [scene, nh, tn, cause, solution]
    for vi, (val, cx, cw) in enumerate(zip(vals, col_xs, col_widths)):
        col = DARK_GRAY
        if vi == 3:
            col = RGBColor(0, 126, 181)
        elif vi == 4:
            col = RGBColor(180, 60, 0)
        add_text_box(s, val, cx + 0.08, ry + 0.05, cw - 0.1, 0.55,
                     font_size=10.5, color=col, align=PP_ALIGN.LEFT)

# Key insight
add_shape_rect(s, 0.5, 5.4, 12.33, 1.2, fill_color=RGBColor(232, 244, 252))
add_text_box(s, "为什么IMS能做这件事？", 0.7, 5.45, 12, 0.4,
             font_size=14, bold=True, color=BLUE, align=PP_ALIGN.LEFT)
add_text_box(s, "IMS内嵌Hach仪表故障诊断知识库。当DO报警时，自动调取同时间段NH₃-N、TN数据，\n与历史趋势比对，判断是"工艺问题"还是"仪表问题"——准确率远高于人工经验。",
             0.7, 5.85, 12, 0.7,
             font_size=12, color=DARK_GRAY, align=PP_ALIGN.LEFT)

# Bottom
add_text_box(s, "这是单台仪表做不到的——无论仪表多贵、多精准",
             0.5, 6.7, 12.33, 0.45,
             font_size=13, bold=True, color=BLUE, align=PP_ALIGN.LEFT)

# ─────────────────────────────────────────────────────────────
# SLIDE 6: 新需求③ 最优曝气量
# ─────────────────────────────────────────────────────────────
s = prs.slides.add_slide(prs.slide_layouts[6])

add_shape_rect(s, 0, 0, 13.33, 0.08, fill_color=BLUE)

add_shape_rect(s, 0.5, 0.35, 0.65, 0.65, fill_color=BLUE)
add_text_box(s, "③", 0.5, 0.35, 0.65, 0.65,
             font_size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

add_text_box(s, "新需求：数据驱动的最优曝气量寻找", 1.3, 0.4, 11, 0.6,
             font_size=26, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)
add_text_box(s, "IMS积累高频历史数据，才能找到动态最优值", 1.3, 0.9, 11, 0.4,
             font_size=13, color=LIGHT_GRAY, align=PP_ALIGN.LEFT)

# The problem
add_text_box(s, "运行人员的困境", 0.5, 1.5, 12, 0.4,
             font_size=15, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)

add_text_box(s, ""知道DO高了浪费电、增加N₂O，但不知道当前最优DO设定值是多少"",
             0.5, 1.95, 12.33, 0.5,
             font_size=15, color=RGBColor(180, 60, 0), align=PP_ALIGN.LEFT)

# Variables table
var_data = [
    ("条件", "最优DO值", "原因"),
    ("夏季进水浓度低", "1.0~1.5mg/L", "硝化速率快，少量曝气即可"),
    ("冬季低温高负荷", "2.5~3.0mg/L", "硝化速率下降，需更多曝气"),
    ("雨天进水稀释", "动态变化", "碳氮比突变，需实时调整"),
]

add_text_box(s, "最优DO值随条件动态变化——没有固定答案", 0.5, 2.6, 12, 0.4,
             font_size=13, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)

# Table
col_w = [3.2, 3.2, 5.8]
col_x = [0.5, 3.72, 6.94]

for ci, (hdr, cx, cw) in enumerate(zip(["条件", "最优DO值", "原因"], col_x, col_w)):
    add_shape_rect(s, cx, 3.0, cw, 0.4, fill_color=BLUE if ci == 1 else DARK_GRAY)
    add_text_box(s, hdr, cx + 0.1, 3.02, cw - 0.1, 0.35,
                 font_size=12, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

for ri, (cond, opt, reason) in enumerate(var_data):
    ry = 3.42 + ri * 0.55
    bg = RGBColor(250, 250, 250) if ri % 2 == 0 else RGBColor(245, 248, 250)
    add_shape_rect(s, 0.5, ry, 12.33, 0.53, fill_color=bg)
    for ci, (val, cx, cw) in enumerate(zip([cond, opt, reason], col_x, col_w)):
        col = BLUE if ci == 1 else DARK_GRAY
        add_text_box(s, val, cx + 0.1, ry + 0.04, cw - 0.1, 0.45,
                     font_size=11, color=col, align=PP_ALIGN.LEFT)

# Traditional approach
add_shape_rect(s, 0.5, 5.2, 5.8, 1.7, fill_color=RGBColor(255, 245, 240))
add_shape_rect(s, 0.5, 5.2, 5.8, 0.4, fill_color=RGBColor(180, 60, 0))
add_text_box(s, "传统做法（凭经验设保守值）", 0.6, 5.22, 5.6, 0.35,
             font_size=12, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
add_text_box_lines(s, [
    ("→ 曝气总是偏多 → 能耗浪费", False, False),
    ("→ N₂O排放偏高 → 碳排放超标", False, False),
    ("→ 运行人员不敢降低DO，怕出水超标", False, False),
], 0.6, 5.68, 5.6, 1.1, font_size=11, color=RGBColor(180, 60, 0))

# IMS approach
add_shape_rect(s, 6.8, 5.2, 6.03, 1.7, fill_color=RGBColor(232, 244, 252))
add_shape_rect(s, 6.8, 5.2, 6.03, 0.4, fill_color=BLUE)
add_text_box(s, "IMS做法（数据驱动的工艺优化）", 6.9, 5.22, 5.8, 0.35,
             font_size=12, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
add_text_box_lines(s, [
    ("→ 积累高频历史数据（5-15分钟/次）", False, False),
    ("→ 分析不同进水条件下的最优曝气量", False, False),
    ("→ 持续优化，年均曝气能耗降低10-20%", False, False),
], 6.9, 5.68, 5.8, 1.1, font_size=11, color=DARK_GRAY)

add_text_box(s, "单台仪表告诉你"现在DO是多少"——IMS告诉你"结合历史数据，当前最优曝气量应该是多少"",
             0.5, 7.05, 12.33, 0.4,
             font_size=12, bold=True, color=BLUE, align=PP_ALIGN.LEFT)

# ─────────────────────────────────────────────────────────────
# SLIDE 7: 为什么只有IMS能解决
# ─────────────────────────────────────────────────────────────
s = prs.slides.add_slide(prs.slide_layouts[6])

add_shape_rect(s, 0, 0, 13.33, 0.08, fill_color=BLUE)

add_text_box(s, "为什么这些新需求必须通过IMS解决？", 0.5, 0.35, 12, 0.6,
             font_size=26, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)

# Comparison table
headers = ["", "高频数据采集", "多参数联动分析", "异常根因诊断", "趋势优化分析"]
col_ws = [2.3, 2.5, 2.7, 2.9, 2.9]
col_xs = [0.5]
for w in col_ws[:-1]:
    col_xs.append(col_xs[-1] + w)

# Header
for ci, (hdr, cx, cw) in enumerate(zip(headers, col_xs, col_ws)):
    add_shape_rect(s, cx, 1.1, cw, 0.45, fill_color=BLUE if ci == 0 else (DARK_GRAY if ci == 0 else DARK_GRAY))
    add_shape_rect(s, cx, 1.1, cw, 0.45, fill_color=DARK_GRAY)
    add_text_box(s, hdr, cx + 0.08, 1.12, cw - 0.1, 0.4,
                 font_size=11, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

methods = [
    ("人工巡检\n（1-2次/天）", "❌", "❌", "❌", "❌", RGBColor(255, 240, 240)),
    ("Excel记录\n（手工录入）", "✅", "❌", "❌", "❌", RGBColor(255, 250, 235)),
    ("通用SCADA\n（数据采集）", "✅", "❌", "❌", "❌", RGBColor(235, 245, 255)),
    ("DCS/RTC\n（闭环控制）", "✅", "❌", "❌", "❌", RGBColor(235, 245, 255)),
    ("IMS\n（数据+诊断+知识库）", "✅", "✅", "✅", "✅", RGBColor(230, 245, 240)),
]

for ri, (method, *checks, bg) in enumerate(methods):
    ry = 1.58 + ri * 0.78
    add_shape_rect(s, 0.5, ry, 12.33, 0.73, fill_color=bg)
    for ci, (val, cx, cw) in enumerate(zip([method] + list(checks), col_xs, col_ws)):
        is_last = (ci == 4)
        col = BLUE if (is_last and val == "✅") else (RGBColor(180, 60, 0) if (is_last and val == "❌") else DARK_GRAY)
        add_text_box(s, val, cx + 0.08, ry + 0.05, cw - 0.1, 0.65,
                     font_size=11, color=col, align=PP_ALIGN.CENTER)

# Key point
add_shape_rect(s, 0.5, 5.55, 12.33, 1.5, fill_color=BLUE)
add_text_box(s, "IMS是唯一同时具备四类能力的方案", 0.7, 5.6, 12, 0.5,
             font_size=17, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
add_text_box_lines(s, [
    ("IMS = 多参数高频数据整合  +  内嵌Hach仪表故障知识库  +  跨仪表趋势分析  +  仪表健康管理", False, False),
], 0.7, 6.1, 12, 0.5, font_size=13, color=WHITE, align=PP_ALIGN.LEFT)
add_text_box(s, "RTC负责执行（自动调节曝气阀门）  ·  IMS负责判断（告诉RTC什么时候调、调多少）",
             0.7, 6.6, 12, 0.4, font_size=12, color=RGBColor(200, 235, 255), align=PP_ALIGN.LEFT)

# ─────────────────────────────────────────────────────────────
# SLIDE 8: AOA改造机会
# ─────────────────────────────────────────────────────────────
s = prs.slides.add_slide(prs.slide_layouts[6])

add_shape_rect(s, 0, 0, 13.33, 0.08, fill_color=BLUE)

add_text_box(s, "AOA改造给IMS带来的具体机会", 0.5, 0.35, 12, 0.6,
             font_size=26, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)

# The core problem
add_shape_rect(s, 0.5, 1.05, 12.33, 1.1, fill_color=RGBColor(245, 248, 250))
add_text_box(s, "AOA污水厂的核心挑战", 0.7, 1.1, 12, 0.4,
             font_size=14, bold=True, color=BLUE, align=PP_ALIGN.LEFT)
add_text_box(s, "不是"买什么仪表"，而是"如何让仪表数据真正用于工艺控制"",
             0.7, 1.5, 12, 0.55, font_size=14, color=DARK_GRAY, align=PP_ALIGN.LEFT)

# Reality
add_text_box_lines(s, [
    ("现实：上了多台在线仪表（DO、NH₃-N、TN）→ 运行人员还是靠经验、靠巡检记录", False, False),
    ("→ 仪表数据躺在显示屏上，没有被用来做工艺决策", False, False),
    ("→ 花了大钱买仪表，却没有真正实现数据驱动的精确控制", False, False),
], 0.5, 2.25, 12.33, 1.0, font_size=12, color=RGBColor(180, 60, 0), align=PP_ALIGN.LEFT)

# Two opportunity types
add_text_box(s, "机会一：新建AOA污水厂（增量市场）", 0.5, 3.4, 12, 0.45,
             font_size=15, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)

opp1_bullets = [
    "仪表+IMS打包销售：DO/TN/NH₃-N等核心仪表采购时，IMS作为"仪表配套数据平台"捆绑导入",
    "从设计院/可研阶段推动IMS纳入推荐配置清单——仪表品牌锁定=IMS品牌锁定",
    "Hach差异化壁垒：NT6800（总氮）+ LDO II（溶解氧）+ NH6000sc（氨氮）+ IMS一体化方案",
]
for bi, bullet in enumerate(opp1_bullets):
    add_text_box(s, f"• {bullet}", 0.5, 3.9 + bi * 0.48, 12.33, 0.45,
                 font_size=12, color=DARK_GRAY, align=PP_ALIGN.LEFT)

add_text_box(s, "机会二：AAO改AOA（存量改造市场）", 0.5, 5.45, 12, 0.45,
             font_size=15, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)

opp2_bullets = [
    "改造期间仪表换新=IMS进入的最佳时机：工艺参数重新调试，IMS数据是调试工具",
    "客户在改造期愿意尝试新方法；改造投资包含仪表预算，IMS可打包进预算",
    "切入点："您新上的DO仪表和NH₃-N仪表，如果不连IMS，数据每天产生几百个点，没人看"",
]
for bi, bullet in enumerate(opp2_bullets):
    add_text_box(s, f"• {bullet}", 0.5, 5.95 + bi * 0.48, 12.33, 0.45,
                 font_size=12, color=DARK_GRAY, align=PP_ALIGN.LEFT)

# ─────────────────────────────────────────────────────────────
# SLIDE 9: 四个试点污水厂
# ─────────────────────────────────────────────────────────────
s = prs.slides.add_slide(prs.slide_layouts[6])

add_shape_rect(s, 0, 0, 13.33, 0.08, fill_color=BLUE)

add_text_box(s, "四个试点污水厂：优先跟进策略", 0.5, 0.35, 12, 0.6,
             font_size=26, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)

plants = [
    ("北京高碑店", "北京", "★★★★★", "同属北京城市排水集团；Hach北京市场关系深厚；具备集团级IMS采购潜力", BLUE),
    ("北京定福庄", "北京", "★★★★", "与高碑店同属北京城市排水集团；可作为集团级IMS复制案例", BLUE),
    ("天津张贵庄", "天津", "★★★", "天津创业环保是本地主要水务公司；Hach华北重点市场", DARK_GRAY),
    ("合肥王小郢", "合肥", "★★★", "合肥市政污水厂；Hach华东市场；需确认现有客户关系", DARK_GRAY),
]

for i, (name, city, stars, note, col) in enumerate(plants):
    ry = 1.1 + i * 1.5
    add_shape_rect(s, 0.5, ry, 12.33, 1.35, fill_color=RGBColor(250, 250, 250))
    add_shape_rect(s, 0.5, ry, 0.08, 1.35, fill_color=col)
    add_text_box(s, name, 0.72, ry + 0.1, 2.5, 0.5,
                 font_size=17, bold=True, color=col, align=PP_ALIGN.LEFT)
    add_text_box(s, city, 0.72, ry + 0.6, 2.5, 0.4,
                 font_size=12, color=LIGHT_GRAY, align=PP_ALIGN.LEFT)
    add_text_box(s, stars, 3.2, ry + 0.2, 1.5, 0.45,
                 font_size=16, color=RGBColor(255, 180, 0), align=PP_ALIGN.LEFT)
    add_text_box(s, note, 4.7, ry + 0.15, 8.1, 1.1,
                 font_size=12, color=DARK_GRAY, align=PP_ALIGN.LEFT)

# Recommendation
add_shape_rect(s, 0.5, 7.15, 12.33, 0.3, fill_color=BLUE)
add_text_box(s, "优先拜访北京城市排水集团设备部，以高碑店+定福庄打包谈集团级IMS",
             0.7, 7.17, 12, 0.25,
             font_size=11, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

# ─────────────────────────────────────────────────────────────
# SLIDE 10: 核心结论
# ─────────────────────────────────────────────────────────────
s = prs.slides.add_slide(prs.slide_layouts[6])

add_shape_rect(s, 0, 0, 13.33, 0.08, fill_color=BLUE)

add_text_box(s, "核心结论", 0.5, 0.35, 12, 0.6,
             font_size=28, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)

conclusions = [
    ("IMS在AOA中的价值不可替代",
     "多参数联动 · 异常根因诊断 · 最优曝气量——这三件事只有IMS能做，AAO时代不存在这些需求"),
    ("改造窗口期是IMS进入最佳时机",
     "AAO改AOA期间，仪表换新=IMS导入成本最低；运行人员愿意尝试新方法；预算可打包"),
    ("IMS是AOA从经验控制到数据驱动的唯一工具",
     "仪表销售卖的是"这套系统能不能告诉我现在工艺状态正不正常"——而不是"这台仪表测得准不准""),
    ("北京高碑店+定福庄是优先目标",
     "同属北京城市排水集团，集团级IMS采购可能性高；Hach北京仪表渗透率高，成功案例背书强"),
]

for i, (title, body) in enumerate(conclusions):
    ry = 1.1 + i * 1.55
    add_shape_rect(s, 0.5, ry, 12.33, 1.4, fill_color=RGBColor(250, 250, 250))
    add_shape_rect(s, 0.5, ry, 0.08, 1.4, fill_color=BLUE)
    add_shape_rect(s, 0.65, ry + 0.1, 0.55, 0.55, fill_color=BLUE)
    add_text_box(s, str(i + 1), 0.65, ry + 0.1, 0.55, 0.55,
                 font_size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text_box(s, title, 1.35, ry + 0.12, 11.3, 0.5,
                 font_size=16, bold=True, color=DARK_GRAY, align=PP_ALIGN.LEFT)
    add_text_box(s, body, 1.35, ry + 0.65, 11.3, 0.7,
                 font_size=12, color=DARK_GRAY, align=PP_ALIGN.LEFT)

# Bottom divider
add_shape_rect(s, 0.5, 7.3, 12.33, 0.03, fill_color=LIGHT_GRAY)
add_text_box(s, "IMS × AOA工艺改造机会分析  |  数据来源：水协2026年会追踪  |  2026-04-22",
             0.5, 7.38, 12.33, 0.35,
             font_size=10, color=LIGHT_GRAY, align=PP_ALIGN.LEFT)

# Save
output_path = "/home/agentuser/IMS_AOA_Opportunity_Analysis.pptx"
prs.save(output_path)
print(f"Saved: {output_path}")
print(f"Slides: {len(prs.slides)}")
