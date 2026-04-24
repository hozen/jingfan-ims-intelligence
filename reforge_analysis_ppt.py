#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reforge Growth Loop 框架分析：Hach进华为鸿蒙生态
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

BLUE = RGBColor(0, 126, 181)
DARK_GRAY = RGBColor(77, 77, 77)
LIGHT_GRAY = RGBColor(153, 153, 153)
WHITE = RGBColor(255, 255, 255)
ORANGE = RGBColor(230, 126, 34)
GREEN = RGBColor(39, 174, 96)
RED = RGBColor(231, 76, 60)
LIGHT_BLUE_BG = RGBColor(240, 248, 255)
LIGHT_ORANGE = RGBColor(255, 248, 240)
LIGHT_GREEN = RGBColor(240, 255, 240)
LIGHT_RED = RGBColor(255, 240, 240)

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

def rect(s, x, y, w, h, fill=None):
    shape = s.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    shape.line.fill.background()
    return shape

def txt(s, text, x, y, w, h, sz=14, bold=False, col=DARK_GRAY,
        align=PP_ALIGN.LEFT):
    txBox = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = "Microsoft YaHei"
    run.font.size = Pt(sz)
    run.font.bold = bold
    run.font.color.rgb = col
    return txBox

def bullets(s, items, x, y, w, h, sz=13, col=DARK_GRAY):
    txBox = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = txBox.text_frame
    tf.word_wrap = True
    first = True
    for item in items:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = f"• {item}"
        run.font.name = "Microsoft YaHei"
        run.font.size = Pt(sz)
        run.font.color.rgb = col
    return txBox

def header_bar(slide, title):
    rect(slide, 0, 0, 13.33, 0.9, fill=BLUE)
    txt(slide, title, 0.4, 0.15, 12.5, 0.6, sz=24, bold=True, col=WHITE)

def add_slide_number(slide, num, total):
    txt(slide, f"{num}/{total}", 12.5, 7.1, 0.7, 0.3, sz=10, col=LIGHT_GRAY, align=PP_ALIGN.RIGHT)

TOTAL = 9

# ========== SLIDE 1: Title ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
rect(slide, 0, 0, 13.33, 7.5, fill=WHITE)
rect(slide, 0, 0, 13.33, 0.08, fill=BLUE)
rect(slide, 0, 6.8, 13.33, 0.7, fill=BLUE)
txt(slide, "Reforge Growth Loop 框架", 0.6, 1.6, 12, 0.8, sz=28, bold=True, col=BLUE, align=PP_ALIGN.CENTER)
txt(slide, "Hach × 华为鸿蒙生态市场切入策略分析", 0.6, 2.5, 12, 1.0, sz=36, bold=True, col=DARK_GRAY, align=PP_ALIGN.CENTER)
txt(slide, "战略视角 · 环路思维 · 自我驱动增长", 0.6, 3.6, 12, 0.5, sz=18, col=LIGHT_GRAY, align=PP_ALIGN.CENTER)
rect(slide, 3.5, 4.3, 6.33, 0.04, fill=BLUE)
txt(slide, "Hach中国IMS产品线 · 2026-04-23", 0.6, 4.6, 12, 0.5, sz=16, col=LIGHT_GRAY, align=PP_ALIGN.CENTER)
txt(slide, "方法论：Brian Balfour / Reforge Growth Loop", 0.6, 5.2, 12, 0.4, sz=14, col=LIGHT_GRAY, align=PP_ALIGN.CENTER)
txt(slide, "Hach中国IMS产品线", 0.6, 6.9, 6, 0.4, sz=14, col=WHITE)

# ========== SLIDE 2: 框架核心 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
rect(slide, 0, 0, 13.33, 7.5, fill=WHITE)
header_bar(slide, "一、Reforge核心：漏斗 vs 环路")

# Left: 漏斗
txt(slide, "漏斗思维（传统）", 0.5, 1.1, 5.5, 0.4, sz=16, bold=True, col=RED)
rect(slide, 0.5, 1.5, 5.5, 2.8, fill=LIGHT_RED)
txt(slide, "获客 → 激活 → 留存 → 收入 → 推荐", 1.0, 1.7, 4.5, 0.5, sz=13, col=DARK_GRAY)
txt(slide, "本质：线性消耗模型", 1.0, 2.2, 4.5, 0.3, sz=12, bold=True, col=RED)
bullets(slide, [
    "持续外部投入才能维持增长",
    "停止投入 = 停止增长",
    "获客成本越来越高（边际递增）",
    "转化率逐层下降（漏斗流失）",
    "可预测但不可持续",
], 1.0, 2.5, 4.8, 2.0, sz=12)

# Right: 环路
txt(slide, "环路思维（Reforge）", 7.2, 1.1, 5.5, 0.4, sz=16, bold=True, col=GREEN)
rect(slide, 7.2, 1.5, 5.6, 2.8, fill=LIGHT_GREEN)
txt(slide, "用户 → 价值 → 吸引新用户 → 更大价值", 7.7, 1.7, 4.8, 0.5, sz=13, col=DARK_GRAY)
txt(slide, "本质：闭环自驱模型", 7.7, 2.2, 4.8, 0.3, sz=12, bold=True, col=GREEN)
bullets(slide, [
    "输出成为下一次输入（复利效应）",
    "边际成本递减（网络效应）",
    "一旦跑通，自我驱动增长",
    "留存是环路的核心",
    "增长不是花钱买而是做出来",
], 7.7, 2.5, 4.8, 2.0, sz=12)

# Bottom key insight
rect(slide, 0.5, 4.6, 12.3, 1.0, fill=LIGHT_BLUE_BG)
txt(slide, "💡 核心洞察：", 0.7, 4.7, 2, 0.4, sz=13, bold=True, col=BLUE)
txt(slide, "对于Hach进鸿蒙生态，核心问题不是"怎么卖"（漏斗思维），而是"如何嵌入生态的某个环路"（环路思维）。", 2.5, 4.7, 10, 0.8, sz=13, col=DARK_GRAY)

txt(slide, "方法论来源：Brian Balfour, \"Growth Loops are the New Funnels\", Reforge Blog, 2018-07-31", 0.5, 7.0, 12, 0.3, sz=10, col=LIGHT_GRAY)
add_slide_number(slide, 2, TOTAL)

# ========== SLIDE 3: 四种环路 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
rect(slide, 0, 0, 13.33, 7.5, fill=WHITE)
header_bar(slide, "二、四种基础增长环路")

loops = [
    ("内容环路", "内容→搜索引擎流量→用户注册→用户生成内容→更多内容", "知乎、B站、Stack Overflow", "白皮书→试用申请→案例生产→SEO增强", GREEN),
    ("病毒环路", "用户使用→分享行为→新用户进入→快速激活→更多分享", "Hotmail、LinkedIn网络效应", "标杆水厂案例→行业口碑→其他水厂主动了解", BLUE),
    ("付费环路", "付费获客→用户产生收入→部分收入再投入→边际成本递减", "Slack早期、Dropbox", "单客户LTV>CAC时，覆盖获客成本后循环投入", ORANGE),
    ("升级环路", "用户使用→产生价值信号→推动同事/朋友加入→团队扩散", "Slack、Figma", "IMS使用深度→甲方运维团队扩散→更多点位增购", RED),
]

x_positions = [0.5, 6.9]
y_positions = [1.1, 3.9]

for i, (name, formula, case, b2b_case, col) in enumerate(loops):
    x = x_positions[i % 2]
    y = y_positions[i // 2]
    rect(slide, x, y, 6.0, 2.5, fill=LIGHT_BLUE_BG)
    rect(slide, x, y, 6.0, 0.45, fill=col)
    txt(slide, f"环路{i+1}：{name}", x + 0.2, y + 0.05, 5.5, 0.4, sz=14, bold=True, col=WHITE)
    txt(slide, formula, x + 0.2, y + 0.55, 5.6, 0.4, sz=11, col=DARK_GRAY)
    txt(slide, f"案例：{case}", x + 0.2, y + 0.95, 5.6, 0.3, sz=10, col=LIGHT_GRAY)
    txt(slide, f"B2B适配：{b2b_case}", x + 0.2, y + 1.3, 5.6, 0.6, sz=11, bold=True, col=col)

    txt(slide, '关键：每条环路回答一个问题——客户的什么行为会触发下一个用户的获取？', 0.5, 6.7, 12, 0.3, sz=12, bold=True, col=BLUE)
add_slide_number(slide, 3, TOTAL)

# ========== SLIDE 4: Hach现状诊断 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
rect(slide, 0, 0, 13.33, 7.5, fill=WHITE)
header_bar(slide, "三、Hach进鸿蒙：现状环路诊断（5问）")

questions = [
    ("用户是谁？", "深圳/广东水务集团运维部门 + 设备科 + IT/信息化部门", "IMS产品线潜在决策者"),
    ("核心行为是什么？", "① 安装IMS软件 ② 上报设备数据 ③ 使用数据分析运维问题", "试用转化率0%——试用这个行为没有闭环"),
    ("这个行为如何带来新用户？", "目前没有环路——销售驱动的漏斗，不存在客户自动带来客户机制", "没有自发传播路径"),
    ("环路的时间周期？", "项目周期：3-6个月/客户 | 生态认证周期：6-12个月", "短期无环路，长期待构建"),
    ("环路的瓶颈在哪里？", "① 没有标杆案例产生内容 ② 没有数据锁定效应 ③ 没有进入生态目录", "试用失败→无案例→无说服力→新客户不敢用"),
]

y = 1.1
for q, a, implication in questions:
    rect(slide, 0.5, y, 12.3, 1.0, fill=LIGHT_BLUE_BG if questions.index((q,a)) % 2 == 0 else WHITE)
    txt(slide, f"Q{i+1}: {q}", 0.7, y + 0.1, 2.5, 0.35, sz=13, bold=True, col=BLUE)
    txt(slide, a, 3.3, y + 0.1, 5.5, 0.6, sz=12, col=DARK_GRAY)
    txt(slide, f"→ {implication}", 9.0, y + 0.1, 3.6, 0.6, sz=11, col=ORANGE)
    y += 1.05

txt(slide, "诊断结论：Hach目前处于"零环路"状态——完全依赖销售漏斗，增长不可持续。", 0.5, 6.5, 12, 0.5, sz=14, bold=True, col=RED)
add_slide_number(slide, 4, TOTAL)

# ========== SLIDE 5: 推荐环路 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
rect(slide, 0, 0, 13.33, 7.5, fill=WHITE)
header_bar(slide, "四、推荐策略：双环路联动 + 增长链")

# Loop A: 标杆效应
txt(slide, "环路A：生态标杆效应环路", 0.5, 1.1, 6, 0.4, sz=14, bold=True, col=GREEN)
rect(slide, 0.5, 1.5, 6.0, 2.4, fill=LIGHT_GREEN)
txt(slide, "深圳水务标杆案例落地", 0.7, 1.6, 5.5, 0.35, sz=12, bold=True, col=DARK_GRAY)
bullets(slide, [
    "IMS数据在水务场景产生实际运维价值",
    "甲方主动在行业会议分享案例",
    "其他水务集团来参观/了解",
    "了解后启动试用/试点",
    "标杆案例积累 → 更多甲方主动找来",
], 0.7, 1.95, 5.6, 1.8, sz=11)

# Loop B: 数据价值
txt(slide, "环路B：IMS数据价值环路", 7.0, 1.1, 6, 0.4, sz=14, bold=True, col=BLUE)
rect(slide, 7.0, 1.5, 6.0, 2.4, fill=LIGHT_BLUE_BG)
txt(slide, "数据持续产出 → 客户粘性增强", 7.2, 1.6, 5.5, 0.35, sz=12, bold=True, col=DARK_GRAY)
bullets(slide, [
    "IMS持续接入更多设备数据",
    "AI预测准确率提升（故障预警）",
    "甲方运维效率可量化改善",
    "客户续费 + 增购更多点位",
    "数据积累 → 模型更强 → 更多价值",
], 7.2, 1.95, 5.6, 1.8, sz=11)

# Chain arrow
txt(slide, "增长链（双环路联动）", 0.5, 4.1, 12, 0.4, sz=14, bold=True, col=DARK_GRAY)
rect(slide, 0.5, 4.5, 12.3, 1.2, fill=LIGHT_ORANGE)
txt(slide, "环路A（标杆效应）", 1.0, 4.65, 3.0, 0.4, sz=13, bold=True, col=GREEN)
txt(slide, "→ 标杆案例增强环路B的说服力", 4.2, 4.65, 5, 0.4, sz=12, col=DARK_GRAY)
txt(slide, "环路B（数据价值）", 1.0, 5.1, 3.0, 0.4, sz=13, bold=True, col=BLUE)
txt(slide, "→ 数据价值为标杆案例提供量化证明", 4.2, 5.1, 5, 0.4, sz=12, col=DARK_GRAY)
txt(slide, "两条环路相互增强，形成复利效应", 9.5, 4.85, 3.3, 0.4, sz=12, bold=True, col=ORANGE)

# Key action
rect(slide, 0.5, 5.9, 12.3, 0.7, fill=BLUE)
txt(slide, "立即行动：优先跑通环路A——找到第1个愿意公开分享的深圳标杆客户", 0.7, 6.0, 11.8, 0.5, sz=14, bold=True, col=WHITE)
add_slide_number(slide, 5, TOTAL)

# ========== SLIDE 6: Hach环路设计 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
rect(slide, 0, 0, 13.33, 7.5, fill=WHITE)
header_bar(slide, "五、Hach × 鸿蒙生态：环路嵌入策略")

# Embed into Huawei ecosystem loop
txt(slide, "战略定位：嵌入华为鸿蒙生态的已有环路，而非自建", 0.5, 1.1, 12, 0.4, sz=14, bold=True, col=BLUE)
rect(slide, 0.5, 1.5, 12.3, 0.05, fill=BLUE)

# Table header
headers = ["策略层次", "具体动作", "目标效果", "时间节点"]
col_widths = [2.5, 4.5, 3.5, 2.0]
x = 0.5
y = 1.7
for i, (h, w) in enumerate(zip(headers, col_widths)):
    rect(slide, x, y, w, 0.4, fill=BLUE)
    txt(slide, h, x + 0.1, y + 0.05, w - 0.2, 0.35, sz=12, bold=True, col=WHITE, align=PP_ALIGN.CENTER)
    x += w

# Table rows
rows = [
    ("1. 嵌入生态标杆环路", "与深圳水务/尚易合作，打造开源鸿蒙水厂标杆", "成为华为官方宣传的水务IMS合作伙伴", "0-6个月"),
    ("2. 构建内容环路", "将标杆案例写成技术文章/行业分享 → SEO流量", "甲方主动找到Hach", "3-9个月"),
    ("3. 激活数据价值环路", "IMS数据在甲方产生真实价值 → 续费+增购", "单客户LTV提升3-5倍", "6-18个月"),
    ("4. 触发升级环路", "甲方运维团队使用IMS → 依赖度提升 → 部门内扩散", "从1个点位扩展到全厂", "6-24个月"),
    ("5. 形成增长链", "标杆→内容→数据价值→更多标杆（循环强化）", "自我驱动的复合增长", "12-36个月"),
]

y = 2.1
for i, (col1, col2, col3, col4) in enumerate(rows):
    fill = LIGHT_BLUE_BG if i % 2 == 0 else WHITE
    x = 0.5
    for j, (val, w) in enumerate(zip([col1, col2, col3, col4], col_widths)):
        col_color = DARK_GRAY
        if j == 0:
            col_color = BLUE
        rect(slide, x, y, w, 0.8, fill=fill)
        txt(slide, val, x + 0.1, y + 0.1, w - 0.2, 0.65, sz=11, col=col_color)
        x += w
    y += 0.8

txt(slide, "核心逻辑：先嵌入生态已有环路（借力），再逐步构建私有环路（锁定）", 0.5, 6.5, 12, 0.4, sz=13, bold=True, col=ORANGE)
add_slide_number(slide, 6, TOTAL)

# ========== SLIDE 7: 漏斗思维 vs 环路思维 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
rect(slide, 0, 0, 13.33, 7.5, fill=WHITE)
header_bar(slide, "六、思维转换：漏斗 → 环路（对比）")

# Header
headers2 = ["维度", "漏斗思维（错误）", "环路思维（正确）"]
col_widths2 = [2.5, 4.8, 5.2]
x = 0.5
y = 1.1
for h, w in zip(headers2, col_widths2):
    rect(slide, x, y, w, 0.45, fill=BLUE)
    txt(slide, h, x + 0.1, y + 0.07, w - 0.2, 0.35, sz=13, bold=True, col=WHITE, align=PP_ALIGN.CENTER)
    x += w

rows2 = [
    ("核心问题", "如何让更多人知道Hach？", "Hach的客户如何带来更多客户？"),
    ("增长动力", "销售团队 + 渠道投入", "标杆客户的示范效应"),
    ("营销投入", "持续花钱维持曝光", "一次性投入打造标杆，后续自动获客"),
    ("客户关系", "买卖关系（卖完结束）", "共生关系（客户成功=自我增长）"),
    ("对华为生态", "找华为要渠道支持", "让华为水务生态需要Hach作为标杆案例"),
    ("IMS试用", "销售驱动完成任务式试用", "甲方业务需求驱动，数据价值自然显现"),
    ("成功指标", "展会到场人数/名片数量", "标杆客户数量/案例内容被引用次数"),
]

y = 1.55
for i, (d1, d2, d3) in enumerate(rows2):
    fill = LIGHT_BLUE_BG if i % 2 == 0 else WHITE
    x = 0.5
    rect(slide, x, y, col_widths2[0], 0.55, fill=fill)
    txt(slide, d1, x + 0.1, y + 0.1, col_widths2[0] - 0.2, 0.4, sz=12, bold=True, col=BLUE)
    x += col_widths2[0]
    rect(slide, x, y, col_widths2[1], 0.55, fill=LIGHT_RED if i % 2 == 0 else RGBColor(255,235,235))
    txt(slide, d2, x + 0.1, y + 0.1, col_widths2[1] - 0.2, 0.4, sz=11, col=RED)
    x += col_widths2[1]
    rect(slide, x, y, col_widths2[2], 0.55, fill=LIGHT_GREEN if i % 2 == 0 else RGBColor(235,255,235))
    txt(slide, d3, x + 0.1, y + 0.1, col_widths2[2] - 0.2, 0.4, sz=11, col=GREEN)
    y += 0.55

txt(slide, "转变关键：停止问"我们如何推广"，开始问"客户成功之后会发生什么"", 0.5, 6.5, 12, 0.4, sz=13, bold=True, col=BLUE)
add_slide_number(slide, 7, TOTAL)

# ========== SLIDE 8: 行动路线图 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
rect(slide, 0, 0, 13.33, 7.5, fill=WHITE)
header_bar(slide, "七、行动路线图（0-36个月）")

phases = [
    ("0-3个月\n跑通环路A", ORANGE, [
        "找到第1个深圳标杆客户（即使亏本）",
        "与尚易科技/深圳水务科技马丹红团队对接",
        "IMS数据通过华为云IoT网关测试",
        "明确华为生态对Hach的具体门槛要求",
    ]),
    ("3-9个月\n构建内容环路", BLUE, [
        "标杆案例整理成技术文章",
        "通过水协年会/行业会议传播",
        "与华为官宣合作（成为生态合作伙伴）",
        "内容SEO积累，开始有甲方主动咨询",
    ]),
    ("9-18个月\n激活数据价值", GREEN, [
        "IMS在甲方稳定运行，AI预测价值显现",
        "推动甲方运维团队扩散使用",
        "标杆案例被华为官方宣传引用",
        "启动第二个标杆客户（第一个的经验复制）",
    ]),
    ("18-36个月\n形成增长链", RED, [
        "双环路联动（标杆效应+数据价值）",
        "增长开始自我驱动",
        "进入华为水务生态核心目录",
        "竞争对手难以追赶的护城河",
    ]),
]

x_positions2 = [0.5, 3.5, 6.5, 9.5]
for i, (title, col, actions) in enumerate(phases):
    x = x_positions2[i]
    rect(slide, x, 1.1, 3.0, 0.7, fill=col)
    txt(slide, title, x + 0.1, 1.2, 2.8, 0.5, sz=13, bold=True, col=WHITE, align=PP_ALIGN.CENTER)
    y = 1.8
    for action in actions:
        rect(slide, x, y, 3.0, 0.65, fill=LIGHT_BLUE_BG)
        txt(slide, f"→ {action}", x + 0.1, y + 0.1, 2.8, 0.5, sz=11, col=DARK_GRAY)
        y += 0.68
    # Arrow to next
    if i < 3:
        txt(slide, "▶", x + 3.05, 2.0, 0.3, 0.3, sz=14, col=LIGHT_GRAY, align=PP_ALIGN.CENTER)

txt(slide, "里程碑：第1个标杆客户落地 = 环路跑通的标志（0-3个月核心目标）", 0.5, 6.5, 12, 0.4, sz=13, bold=True, col=ORANGE)
add_slide_number(slide, 8, TOTAL)

# ========== SLIDE 9: 总结 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
rect(slide, 0, 0, 13.33, 7.5, fill=WHITE)
header_bar(slide, "八、Reforge框架核心要点总结")

# Key takeaways
takeaways = [
    ("01", "环路 > 漏斗", "漏斗消耗资源，环路创造增长。Hach目前是漏斗，目标是环路。", GREEN),
    ("02", "留存是核心", "没有留存的环路是"漏水的环路"。IMS数据价值是留存锚点。", BLUE),
    ("03", "标杆 > 营销", "1个有影响力的标杆客户，比任何广告投放都有效。", ORANGE),
    ("04", "嵌入 > 自建", "先嵌入华为鸿蒙已有生态环路，借力比自建更快。", RED),
    ("05", "复利效应", "双环路联动后，增长开始自我驱动，竞争对手难以复制。", BLUE),
]

y = 1.2
for num, title, desc, col in takeaways:
    rect(slide, 0.5, y, 12.3, 0.9, fill=LIGHT_BLUE_BG)
    rect(slide, 0.5, y, 0.7, 0.9, fill=col)
    txt(slide, num, 0.5, y + 0.2, 0.7, 0.5, sz=18, bold=True, col=WHITE, align=PP_ALIGN.CENTER)
    txt(slide, title, 1.4, y + 0.1, 3, 0.4, sz=14, bold=True, col=col)
    txt(slide, desc, 1.4, y + 0.5, 11, 0.35, sz=12, col=DARK_GRAY)
    y += 0.95

txt(slide, "方法论来源：Brian Balfour / Reforge Growth Loop Framework | Reforge.com", 0.5, 7.0, 8, 0.3, sz=10, col=LIGHT_GRAY)
txt(slide, "Hach中国IMS产品线 · 2026-04-23", 9.5, 7.0, 3.5, 0.3, sz=10, col=LIGHT_GRAY, align=PP_ALIGN.RIGHT)
add_slide_number(slide, 9, TOTAL)

# Save
output_path = '/home/agentuser/reforge_hach_hongmeng_analysis.pptx'
prs.save(output_path)
print(f"Saved to {output_path}")
print(f"Total slides: {len(prs.slides)}")
