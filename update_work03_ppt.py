#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 Work-03 华为鸿蒙PPT：添加二次供水泵房和水质净化厂内容
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

BLUE = RGBColor(0, 126, 181)
DARK_GRAY = RGBColor(77, 77, 77)
LIGHT_GRAY = RGBColor(153, 153, 153)
WHITE = RGBColor(255, 255, 255)

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

def bullets(s, items, x, y, w, h, sz=13, col=DARK_GRAY, bullet_char="•"):
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
        run.text = f"{bullet_char} {item}"
        run.font.name = "Microsoft YaHei"
        run.font.size = Pt(sz)
        run.font.color.rgb = col
    return txBox

def add_slide_number(slide, num, total):
    txt(slide, f"{num}/{total}", 12.5, 7.1, 0.7, 0.3, sz=10, col=LIGHT_GRAY, align=PP_ALIGN.RIGHT)

def header_bar(slide, title):
    rect(slide, 0, 0, 13.33, 0.9, fill=BLUE)
    txt(slide, title, 0.4, 0.15, 12, 0.6, sz=26, bold=True, col=WHITE)

# ========== SLIDE 1: Title ==========
slide_layout = prs.slide_layouts[6]  # Blank
slide = prs.slides.add_slide(slide_layout)
rect(slide, 0, 0, 13.33, 7.5, fill=WHITE)
rect(slide, 0, 0, 13.33, 0.08, fill=BLUE)
rect(slide, 0, 6.8, 13.33, 0.7, fill=BLUE)
txt(slide, "华为鸿蒙生态水质仪表市场情报简报", 0.6, 2.0, 12, 1.2, sz=40, bold=True, col=BLUE, align=PP_ALIGN.CENTER)
txt(slide, "Hach中国IMS产品线 · 环博会特别版", 0.6, 3.3, 12, 0.6, sz=22, col=DARK_GRAY, align=PP_ALIGN.CENTER)
txt(slide, "2026年4月23日", 0.6, 4.0, 12, 0.5, sz=18, col=LIGHT_GRAY, align=PP_ALIGN.CENTER)
txt(slide, "包含：二次供水泵房 + 水质净化厂 最新核实情报", 0.6, 4.6, 12, 0.5, sz=14, col=LIGHT_GRAY, align=PP_ALIGN.CENTER)
txt(slide, "Hach中国IMS产品线", 0.6, 6.9, 6, 0.4, sz=14, col=WHITE)

# ========== SLIDE 2: 战略驱动力 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
rect(slide, 0, 0, 13.33, 7.5, fill=WHITE)
header_bar(slide, "深圳环水 × 华为：战略合作的驱动力")
bullets(slide, [
    "深圳环水集团 × 华为技术：2025-01-23 坂田基地签约",
    "深圳环水需要：数字化转型、国产化背书、智慧水务标杆",
    "华为需要：水务关键场景落地鸿蒙生态",
    "双方互需 → 战略合作 → 加速推进鸿蒙水务落地",
], 0.5, 1.1, 6.0, 2.5, sz=14)
txt(slide, "关键人物", 0.5, 3.6, 3, 0.4, sz=14, bold=True, col=BLUE)
bullets(slide, [
    "龚利民（深圳环水总裁）× 李俊风（华为公共事业军团总裁）",
    "技术落地执行：马丹红（深圳水务科技自控工程部部长）",
], 0.5, 4.0, 6.5, 1.2, sz=13)
txt(slide, "已验证落地案例", 7.0, 1.1, 5.8, 0.4, sz=14, bold=True, col=BLUE)
bullets(slide, [
    "章阁净水厂（2025-12）：全国首座鸿蒙水厂",
    "五指耙水厂（2026-03）：30万吨/天，全国首座鸿蒙智慧水厂",
    "大沙河流域（2026-03）",
    "百合星城泵房（2025-12）：全国首座开源鸿蒙二次供水泵房",
    "茜坑水厂三期（2026-03）：全国首个开源鸿蒙智慧水质净化厂",
    "荷坳水厂（2026-03招标中）",
], 7.0, 1.5, 5.8, 2.8, sz=13)
txt(slide, "数据来源：深圳政府在线、南方都市报、21世纪经济报道、IT之家、ZAKER", 0.5, 7.0, 12, 0.3, sz=10, col=LIGHT_GRAY)
add_slide_number(slide, 2, 7)

# ========== SLIDE 3: 竞争格局 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
rect(slide, 0, 0, 13.33, 7.5, fill=WHITE)
header_bar(slide, "竞争格局：谁已接入 / 传言接入")

# Left column
txt(slide, "已验证接入", 0.5, 1.1, 6, 0.4, sz=14, bold=True, col=BLUE)
bullets(slide, [
    "三川智慧（超声波/电磁水表）：华为技术认证，对接华为云IoT",
    "博铭维（管网机器人）：全链路鸿蒙生态，年会有主题论坛",
    "尚易科技：鸿蒙边缘网关合作方，IPC3528已验证",
    "深圳10余家仪表厂商：五指耙水厂项目，通过网关方案接入",
    "华龙讯达：二次供水泵房集成商，基于开源鸿蒙自研工业OS",
], 0.5, 1.5, 6.3, 2.5, sz=13)

# Right column
txt(slide, "传言接入（未公开证实）", 7.0, 1.1, 6, 0.4, sz=14, bold=True, col=BLUE)
bullets(slide, [
    "吉林光大分析技术：主营二次供水多参数监测仪（非工业水厂）",
    "  → 产品定位：民用Residential二次供水，与Hach不同赛道",
    "  → 鸿蒙认证：全网无公开证据，消息来源较明确",
    "  → 判断：可能有内部测试认证，未对外公开",
    "汉威科技：有水质在线检测设备，水协年会有展示，鸿蒙关系不明",
], 7.0, 1.5, 6.0, 2.5, sz=13)

txt(slide, "IMS视角", 0.5, 4.3, 6, 0.4, sz=14, bold=True, col=BLUE)
rect(slide, 0.5, 4.7, 12.3, 1.0, fill=RGBColor(240, 248, 255))
txt(slide, "Hach核心竞品——吉林光大（非直接竞争但影响市场认知）、汉威科技（直接竞争）", 0.7, 4.8, 12, 0.7, sz=13, col=DARK_GRAY)
txt(slide, "华龙讯达是集成商，不是仪表竞争者——但其方案影响终端甲方对仪表的选型偏好", 0.7, 5.3, 12, 0.5, sz=13, col=DARK_GRAY)
add_slide_number(slide, 3, 7)

# ========== SLIDE 4: 二次供水泵房案例 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
rect(slide, 0, 0, 13.33, 7.5, fill=WHITE)
header_bar(slide, "新增案例：全国首座开源鸿蒙智慧二次供水泵房（龙岗区）")

# Project info table
txt(slide, "项目信息", 0.5, 1.1, 3, 0.4, sz=13, bold=True, col=BLUE)
project_info = [
    ("地点", "龙岗区百合星城一期"),
    ("主管部门", "龙岗区水务局"),
    ("集成商", "华龙讯达信息技术股份有限公司（总经理：龙小昂）"),
    ("操作系统", "华龙工鸿操作系统（基于开源鸿蒙自主研发）"),
    ("核心芯片", "龙芯芯片（100%全栈国产）"),
    ("投运时间", "2025年12月18日"),
]
y = 1.5
for label, value in project_info:
    txt(slide, f"{label}：", 0.5, y, 1.5, 0.35, sz=12, bold=True, col=DARK_GRAY)
    txt(slide, value, 2.0, y, 4.8, 0.35, sz=12, col=DARK_GRAY)
    y += 0.35

# Architecture
txt(slide, "技术架构", 7.0, 1.1, 3, 0.4, sz=13, bold=True, col=BLUE)
rect(slide, 7.0, 1.5, 5.8, 1.8, fill=RGBColor(245, 248, 252))
arch_lines = [
    "传感器/PLC/控制柜（国产PLC替代进口）",
    "    → 华龙工鸿操作系统（龙芯芯片）",
    "    → 分布式软总线（万物智联、内生安全）",
    "    → 边缘计算（断网仍可自主执行恒压供水）",
    "    → 云-边-端一体化",
    "    → 鸿蒙手机\"碰一碰\"近场连接",
]
y = 1.55
for line in arch_lines:
    txt(slide, line, 7.1, y, 5.6, 0.28, sz=11, col=DARK_GRAY)
    y += 0.28

# Results
txt(slide, "效果数据", 0.5, 4.0, 3, 0.4, sz=13, bold=True, col=BLUE)
result_data = [
    ("能耗下降", "10%"),
    ("核心控制器（PLC）采购成本降低", "5%"),
    ("人力运维成本减少", "近80%"),
    ("水质达标率", "显著提升"),
    ("断网极端情况", "可自主执行恒压供水逻辑"),
]
y = 4.4
for label, value in result_data:
    txt(slide, f"{label}：", 0.5, y, 3.5, 0.3, sz=12, bold=True, col=DARK_GRAY)
    txt(slide, value, 4.0, y, 3, 0.3, sz=12, col=BLUE)
    y += 0.3

# Key features
txt(slide, "关键特征", 7.0, 3.5, 3, 0.4, sz=13, bold=True, col=BLUE)
bullets(slide, [
    "鸿蒙手机\"碰一碰\"：贴近面板 → 数据同步 → 参数调节一键完成",
    "100%全栈国产：龙芯芯片 + 华龙工鸿OS + 国产PLC",
    "规模化信号：龙岗区47座泵房已完成立项，逐步推进鸿蒙化改造",
], 7.0, 3.9, 5.8, 1.5, sz=12)

txt(slide, "数据来源：IT之家 2025-12-18（https://www.sohu.com/a/966792652_114760）；ZAKER新闻 2025-12-02", 0.5, 7.0, 12, 0.3, sz=10, col=LIGHT_GRAY)
add_slide_number(slide, 4, 7)

# ========== SLIDE 5: 水质净化厂案例 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
rect(slide, 0, 0, 13.33, 7.5, fill=WHITE)
header_bar(slide, "新增案例：全国首个开源鸿蒙智慧水质净化厂（龙华区茜坑水厂三期）")

txt(slide, "项目信息", 0.5, 1.1, 3, 0.4, sz=13, bold=True, col=BLUE)
info_items = [
    ("地点", "龙华区茜坑水厂三期"),
    ("主管部门", "龙华区水务"),
    ("系统名称", "\"三通两可视\"智慧管控系统"),
    ("投运状态", "2026年3月24日系统突破"),
]
y = 1.5
for label, value in info_items:
    txt(slide, f"{label}：", 0.5, y, 1.5, 0.35, sz=12, bold=True, col=DARK_GRAY)
    txt(slide, value, 2.0, y, 5, 0.35, sz=12, col=DARK_GRAY)
    y += 0.35

txt(slide, "关键信息", 0.5, 3.5, 3, 0.4, sz=13, bold=True, col=BLUE)
bullets(slide, [
    "每一台设备都拥有了智能化能力",
    "打破有限空间作业设备孤岛与数据壁垒",
    "实现各类设备互联互通",
    "系统赋能再生水系统提质降本",
], 0.5, 3.9, 6, 1.8, sz=13)

txt(slide, "IMS战略意义", 7.0, 1.1, 4, 0.4, sz=13, bold=True, col=BLUE)
rect(slide, 7.0, 1.5, 5.8, 3.5, fill=RGBColor(240, 248, 255))
significance = [
    ("技术路径确认", "龙岗/龙华案例再次证明：网关方案是唯一现实路径。华龙讯达也是加网关+替代PLC，不是让每种仪表单独认证。"),
    ("场景差异", "二次供水泵房（民用Residential）与工业水厂（工业Industrial）竞品格局不同。"),
    ("规模化信号", "龙岗区47座泵房立项，开源鸿蒙从试点进入批量复制阶段——时间窗口在缩小。"),
    ("IMS机会", "二次供水泵房对水质在线监测（余氯/浊度/pH）有需求，与IMS产品定位高度吻合。"),
]
y = 1.6
for label, content in significance:
    txt(slide, f"{label}：", 7.1, y, 1.6, 0.3, sz=11, bold=True, col=BLUE)
    txt(slide, content, 7.1, y + 0.28, 5.6, 0.5, sz=11, col=DARK_GRAY)
    y += 0.82

txt(slide, "数据来源：龙华区政府网站 (szlhq.gov.cn) 2026-03-24", 0.5, 7.0, 12, 0.3, sz=10, col=LIGHT_GRAY)
add_slide_number(slide, 5, 7)

# ========== SLIDE 6: 技术路径 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
rect(slide, 0, 0, 13.33, 7.5, fill=WHITE)
header_bar(slide, "技术路径：五指耙水厂实证分析")

txt(slide, "项目背景", 0.5, 1.1, 3, 0.4, sz=13, bold=True, col=BLUE)
bullets(slide, [
    "深圳深水宝安水务集团五指耙水厂改扩建工程（30万吨/天）",
    "原有8类具身智能机器人 + 智能井盖 + 摄像头 + 消火栓等终端",
    "来自10余厂商，协议不兼容，数据孤岛严重",
], 0.5, 1.5, 6.3, 1.5, sz=13)

txt(slide, "技术方案：水鸿WaterHMOS分布式架构", 0.5, 3.1, 6, 0.4, sz=13, bold=True, col=BLUE)
bullets(slide, [
    "核心定位：打破多厂商设备协议壁垒，统一数据调度",
    "不是要求每家仪表厂商单独接入，而是系统集成层统一消化",
    "接入方式：鸿蒙边缘网关（IPC3528/RK3568）+ B-LINK近场连接",
], 0.5, 3.5, 6.3, 1.5, sz=13)

txt(slide, "具体接入架构", 0.5, 5.1, 3, 0.4, sz=13, bold=True, col=BLUE)
rect(slide, 0.5, 5.5, 6.3, 0.8, fill=RGBColor(245, 248, 252))
txt(slide, "仪表设备（MODBUS RTU/TCP） → 鸿蒙边缘网关 → 华为云IoT → WaterHMOS平台", 0.6, 5.6, 6.1, 0.6, sz=12, col=DARK_GRAY)

txt(slide, "接入效果", 7.0, 1.1, 3, 0.4, sz=13, bold=True, col=BLUE)
effect_data = [
    ("运维效率提升", "30%+"),
    ("误报率降低", "30%"),
    ("能耗下降", "10%（泵房案例）"),
    ("人力运维成本减少", "近80%（泵房案例）"),
]
y = 1.5
for label, value in effect_data:
    txt(slide, f"{label}：", 7.0, y, 2.5, 0.3, sz=12, bold=True, col=DARK_GRAY)
    txt(slide, value, 9.5, y, 3, 0.3, sz=12, col=BLUE)
    y += 0.35

txt(slide, "启示", 7.0, 3.6, 3, 0.4, sz=13, bold=True, col=BLUE)
rect(slide, 7.0, 4.0, 5.8, 1.2, fill=RGBColor(255, 248, 240))
txt(slide, "深圳水务接受网关方案：仪表厂只需保证MODBUS输出，无需单独HarmonyOS Connect认证。网关方案是最快可用路径。", 7.2, 4.1, 5.5, 1.0, sz=12, col=DARK_GRAY)

txt(slide, "数据来源：深圳水务科技公司、中国水网(h2o-china.com) 2024-12报道；IT之家 2025-12-18；ZAKER 2025-12-02", 0.5, 7.0, 12, 0.3, sz=10, col=LIGHT_GRAY)
add_slide_number(slide, 6, 7)

# ========== SLIDE 7: Hach切入路径 + 关键未知 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
rect(slide, 0, 0, 13.33, 7.5, fill=WHITE)
header_bar(slide, "Hach切入路径：行动建议 + 关键未知项")

# Left: 行动建议
txt(slide, "立即行动（0-3个月）", 0.5, 1.1, 6, 0.4, sz=13, bold=True, col=BLUE)
bullets(slide, [
    "联系尚易科技：了解Hach + IPC3528网关集成可行性",
    "联系深圳水务科技马丹红团队：了解仪表接入具体要求",
    "Hach仪表MODBUS数据通过网关测试：验证数据上传",
], 0.5, 1.5, 6.3, 1.4, sz=12)

txt(slide, "中期（3-6个月）", 0.5, 3.0, 6, 0.4, sz=13, bold=True, col=BLUE)
bullets(slide, [
    "成为深圳水务鸿蒙生态合作伙伴",
    "与华为云IoT完成兼容性测试",
    "数据手册标注「支持鸿蒙生态接入」",
], 0.5, 3.4, 6.3, 1.2, sz=12)

txt(slide, "风险提示", 0.5, 4.7, 6, 0.4, sz=13, bold=True, col=BLUE)
rect(slide, 0.5, 5.1, 6.3, 0.9, fill=RGBColor(255, 240, 240))
txt(slide, "若深圳市场实质门槛形成（Hach尚未接入）→ 短期内无法在深投标\n时间差 = 竞争对手抢单窗口期", 0.7, 5.2, 6.0, 0.7, sz=12, col=DARK_GRAY)

# Right: 关键未知
txt(slide, "需即时关注", 7.0, 1.1, 6, 0.4, sz=13, bold=True, col=BLUE)
bullets(slide, [
    "吉林光大认证传言的具体来源：是否光大官方宣传？",
    "深圳是否有明确文件要求仪表必须支持鸿蒙接入",
    "另外两个试点城市（销售提到4个城市：深圳+成都+？）",
    "龙岗区47座泵房改造招标信息：哪些厂商中标、仪表品牌",
    "华龙讯达与华为的正式合作关系",
], 7.0, 1.5, 5.8, 2.2, sz=12)

txt(slide, "例行监控", 7.0, 3.9, 6, 0.4, sz=13, bold=True, col=BLUE)
bullets(slide, [
    "水协2026年会后续报道：马丹红演讲全文、参展商名单",
    "深圳水务鸿蒙生态合作伙伴名单更新",
    "华为云IoT水务行业合作伙伴名单",
    "龙岗区47座泵房招标进展",
], 7.0, 4.3, 5.8, 1.6, sz=12)

txt(slide, "IMS建议：以网关方案快速切入深圳市场，同步布局华为云IoT认证 | 情报截止：2026-04-23", 0.5, 7.0, 12.5, 0.3, sz=10, col=LIGHT_GRAY)
add_slide_number(slide, 7, 7)

# Save
output_path = '/home/agentuser/wiki/projects/work-03-hongmeng/briefing_updated.pptx'
prs.save(output_path)
print(f"Saved to {output_path}")
print(f"Total slides: {len(prs.slides)}")
